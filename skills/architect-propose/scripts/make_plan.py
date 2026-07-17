"""Create a deterministic Markdown-first Architect plan package.

The command generates only stable directory structure and deterministic fields.
Architect Propose fills the remaining agent placeholders after the user-approved
design bundle is available.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from plan_protocol import (
    ROOT_DOCUMENTS,
    current_timestamp,
    replace_generated_fields,
    validate_plan_name,
    write_state,
    write_utf8,
)


ROOT_TEMPLATE_FILES = tuple(ROOT_DOCUMENTS)


def allocate_plan_name(repo_root: Path, requested_name: str) -> tuple[str, Path]:
    """Allocate the first non-conflicting plan directory name.

    Args:
        repo_root: Target repository root.
        requested_name: Requested kebab-case plan name.

    Returns:
        Allocated name and empty package root path.
    """

    architect_root = repo_root / ".architect"
    candidate_name = requested_name
    suffix = 2
    while (architect_root / candidate_name).exists():
        candidate_name = f"{requested_name}-{suffix}"
        suffix += 1
    return candidate_name, architect_root / candidate_name


def create_plan(
    repo_root: Path,
    requested_name: str,
    document_language: str,
) -> tuple[str, Path]:
    """Create the fixed plan package skeleton and centralized state file.

    Args:
        repo_root: Target repository root.
        requested_name: Requested kebab-case plan name.
        document_language: Language tag for agent-authored prose.

    Returns:
        Allocated plan name and created package root.
    """

    validate_plan_name(requested_name)
    templates_root = Path(__file__).resolve().parent.parent / "templates"
    allocated_name, package_root = allocate_plan_name(repo_root, requested_name)
    created_at = current_timestamp()
    package_root.mkdir(parents=True)
    (package_root / "03-designs").mkdir()
    (package_root / "06-tasks").mkdir()

    replacements = {
        "PlanName": allocated_name,
        "CreatedAt": created_at,
        "DocumentLanguage": document_language,
    }
    for template_name in ROOT_TEMPLATE_FILES:
        content = (templates_root / template_name).read_text(encoding="utf-8")
        write_utf8(
            package_root / template_name,
            replace_generated_fields(content, replacements),
        )

    write_state(
        package_root,
        {
            "CurrentTask": None,
            "PlanDigest": "",
            "Tasks": {},
        },
    )
    return allocated_name, package_root


def main() -> int:
    """Parse command arguments and print the created plan package location.

    Returns:
        Process exit status.
    """

    parser = argparse.ArgumentParser(
        description="Create a deterministic Architect plan package.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--language", required=True)
    arguments = parser.parse_args()
    allocated_name, package_root = create_plan(
        repo_root=arguments.repo_root.resolve(),
        requested_name=arguments.plan,
        document_language=arguments.language,
    )
    print(f"CREATED: {allocated_name} -> {package_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
