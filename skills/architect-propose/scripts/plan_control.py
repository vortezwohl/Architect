"""Manage deterministic design and task artifacts inside an Architect plan.

Agents use this command to allocate immutable identifiers and to seal a plan
after they fill the approved Markdown placeholders. It intentionally does not
invent design content, approval evidence, task boundaries, or task-declared
execution-result steps.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from plan_protocol import (
    PlanProtocolError,
    compute_plan_digest,
    find_placeholders,
    load_state,
    markdown_documents,
    next_document_id,
    parse_metadata,
    read_utf8,
    replace_generated_fields,
    write_state,
    write_utf8,
)


SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def package_root(repo_root: Path, plan_name: str) -> Path:
    """Return one selected plan package root and verify its manifest exists.

    Args:
        repo_root: Target repository root.
        plan_name: Selected plan name.

    Returns:
        Existing plan package root.

    Raises:
        PlanProtocolError: Raised when the selected package is not initialized.
    """

    root = repo_root / ".architect" / plan_name
    if not (root / "00-plan-manifest.md").is_file():
        raise PlanProtocolError(f"Plan package does not exist: {root}")
    return root


def add_document(package: Path, kind: str, slug: str) -> Path:
    """Allocate and create one deterministic design or task document.

    Args:
        package: Existing plan package root.
        kind: ``design`` or ``task``.
        slug: Generated-file suffix requested by the user-facing plan author.

    Returns:
        Created Markdown document path.

    Raises:
        PlanProtocolError: Raised when the requested kind or slug is invalid.
    """

    if not SLUG_PATTERN.fullmatch(slug):
        raise PlanProtocolError("Slug must use lower-case kebab-case.")
    settings = parse_metadata(package / "00-plan-manifest.md")
    if kind == "design":
        directory_name = "03-designs"
        template_name = "03-design.md"
        prefix = "D"
    elif kind == "task":
        directory_name = "06-tasks"
        template_name = "06-task.md"
        prefix = "T"
    else:
        raise PlanProtocolError(f"Unsupported document kind: {kind}")

    directory = package / directory_name
    document_id = next_document_id(directory.glob("*.md"), prefix)
    target = directory / f"{document_id}-{slug}.md"
    template = (
        Path(__file__).resolve().parent.parent / "templates" / template_name
    )
    content = replace_generated_fields(
        template.read_text(encoding="utf-8"),
        {
            "DocumentId": document_id,
            "Slug": slug,
            "PlanName": settings.plan_name,
            "CreatedAt": settings.created_at,
            "DocumentLanguage": settings.document_language,
        },
    )
    write_utf8(target, content)

    if kind == "task":
        state = load_state(package)
        tasks = state.setdefault("Tasks", {})
        if not isinstance(tasks, dict):
            raise PlanProtocolError("Execution state Tasks must be an object.")
        tasks[document_id] = {
            "State": "pending",
            "RecordedExecutionResults": [],
        }
        write_state(package, state)
    return target


def assign_rule_ids(path: Path) -> None:
    """Assign deterministic rule identifiers to completed MUST-rule bullets.

    Args:
        path: Design or task Markdown document whose rule sections are complete.

    Raises:
        PlanProtocolError: Raised when a rule placeholder remains unresolved.
    """

    metadata = parse_metadata(path)
    content = read_utf8(path)
    lines = content.splitlines()
    section = None
    must_do_index = 0
    must_not_do_index = 0
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped in {"### MUST DO", "## MUST DO"}:
            section = "must_do"
        elif stripped in {"### MUST NOT DO", "## MUST NOT DO"}:
            section = "must_not_do"
        elif stripped.startswith("## ") or stripped.startswith("### "):
            section = None

        if section and line.startswith("- "):
            rule_text = line[2:].strip()
            if rule_text.startswith("{{RULE:"):
                raise PlanProtocolError(f"Unresolved rule placeholder in {path}")
            if not rule_text:
                raise PlanProtocolError(f"Empty rule in {path}")
            compact_document_id = metadata.document_id.replace("-", "")
            if metadata.document_type == "Design":
                if section == "must_do":
                    must_do_index += 1
                    rule_id = f"R-{compact_document_id}-{must_do_index:03d}"
                else:
                    must_not_do_index += 1
                    rule_id = f"R-{compact_document_id}-N{must_not_do_index:03d}"
            elif metadata.document_type == "Task":
                if section == "must_do":
                    must_do_index += 1
                    rule_id = f"M-{compact_document_id}-{must_do_index:03d}"
                else:
                    must_not_do_index += 1
                    rule_id = f"N-{compact_document_id}-{must_not_do_index:03d}"
            else:
                raise PlanProtocolError(f"Rules are not supported in {path}")
            if not rule_text.startswith(("R-", "M-", "N-")):
                line = f"- {rule_id}: {rule_text}"
        output.append(line)
    write_utf8(path, "\n".join(output))


def seal_plan(package: Path) -> str:
    """Assign rule IDs, reject unresolved placeholders, and seal plan digest.

    Args:
        package: Existing plan package root.

    Returns:
        Computed immutable plan digest.

    Raises:
        PlanProtocolError: Raised when any plan document is incomplete.
    """

    for path in list((package / "03-designs").glob("*.md")) + list(
        (package / "06-tasks").glob("*.md"),
    ):
        assign_rule_ids(path)

    unresolved: dict[Path, list[str]] = {}
    for path in markdown_documents(package):
        if path.name == "08-execution-log.md":
            continue
        tokens = find_placeholders(path)
        if path.name == "00-plan-manifest.md":
            tokens = [
                token
                for token in tokens
                if token != "{{GENERATED:PlanDigest}}"
            ]
        if tokens:
            unresolved[path] = tokens
    if unresolved:
        locations = ", ".join(
            f"{path.name}: {', '.join(tokens)}"
            for path, tokens in unresolved.items()
        )
        raise PlanProtocolError(f"Plan contains unresolved placeholders: {locations}")

    digest = compute_plan_digest(package)
    manifest_path = package / "00-plan-manifest.md"
    manifest = read_utf8(manifest_path)
    manifest = re.sub(
        r"^- PlanDigest: .+$",
        f"- PlanDigest: {digest}",
        manifest,
        flags=re.MULTILINE,
    )
    write_utf8(manifest_path, manifest)
    state = load_state(package)
    state["PlanDigest"] = digest
    write_state(package, state)
    return digest


def main() -> int:
    """Parse subcommands for deterministic plan artifact management.

    Returns:
        Process exit status.
    """

    parser = argparse.ArgumentParser(
        description="Manage deterministic Architect plan artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("add-design", "add-task"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--repo-root", required=True, type=Path)
        command_parser.add_argument("--plan", required=True)
        command_parser.add_argument("--slug", required=True)
    seal_parser = subparsers.add_parser("seal")
    seal_parser.add_argument("--repo-root", required=True, type=Path)
    seal_parser.add_argument("--plan", required=True)
    arguments = parser.parse_args()
    try:
        package = package_root(arguments.repo_root.resolve(), arguments.plan)
        if arguments.command == "add-design":
            path = add_document(package, "design", arguments.slug)
            print(f"CREATED: {path}")
        elif arguments.command == "add-task":
            path = add_document(package, "task", arguments.slug)
            print(f"CREATED: {path}")
        else:
            digest = seal_plan(package)
            print(f"SEALED: {package} -> {digest}")
    except PlanProtocolError as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
