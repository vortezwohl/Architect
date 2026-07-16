"""?????? Architect ?????????????????"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


REQUIRED_FILES = (
    "00-overview.md",
    "01-context-and-baseline.md",
    "02-compatibility-contract.md",
    "03-architecture-decision.md",
    "04-impact-map.md",
    "05-detailed-design.md",
    "06-task-plan.md",
    "07-verification-plan.md",
    "08-implementation-log.md",
    ".state/source-snapshot.json",
)
UNRESOLVED_MARKERS = (
    "[REQUIRED]",
    "TODO",
    "TBD",
    "to be decided",
    "as needed",
)
TASK_FIELDS = (
    "- Allowed files:",
    "- Exact symbols or contracts:",
    "- Preconditions:",
    "- Change steps:",
    "- Prohibited changes:",
    "- Verification:",
    "- Completion condition:",
)


def run_git(repository_root: Path, *arguments: str) -> str:
    """?????????? Git ???

    Args:
        repository_root: Git ??????
        *arguments: Git ????????

    Returns:
        ?????????????

    Raises:
        RuntimeError: Git ????????
    """
    result = subprocess.run(
        ["git", *arguments],
        cwd=repository_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Git command failed.")
    return result.stdout.strip()


def working_tree_state(repository_root: Path, change_name: str) -> str:
    """?????????????????

    Args:
        repository_root: Git ??????
        change_name: ????????

    Returns:
        ??????????? Git porcelain ???
    """
    prefix = f".agent-architect/changes/{change_name}/"
    status_lines = run_git(
        repository_root,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    ).splitlines()
    return "\n".join(
        line
        for line in status_lines
        if prefix not in line.replace("\\", "/")
    )


def validate_documents(package_root: Path) -> list[str]:
    """????????????????????

    Args:
        package_root: ???????

    Returns:
        ????????????
    """
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (package_root / relative_path).is_file():
            errors.append(f"Missing required artifact: {relative_path}")

    for document_path in package_root.glob("*.md"):
        content = document_path.read_text(encoding="utf-8")
        for marker in UNRESOLVED_MARKERS:
            if marker.casefold() in content.casefold():
                errors.append(f"Unresolved marker '{marker}' in {document_path.name}")

    task_plan = package_root / "06-task-plan.md"
    if task_plan.is_file():
        task_content = task_plan.read_text(encoding="utf-8")
        if "\n## T-" not in task_content:
            errors.append("Task plan must contain at least one '## T-' task heading.")
        for field in TASK_FIELDS:
            if field not in task_content:
                errors.append(f"Task plan is missing required field: {field}")
    return errors


def validate_baseline(
    repository_root: Path,
    package_root: Path,
    change_name: str,
) -> list[str]:
    """???? Git ??????????????

    Args:
        repository_root: ??????????
        package_root: ???????
        change_name: ????????

    Returns:
        ????????????
    """
    snapshot_path = package_root / ".state" / "source-snapshot.json"
    try:
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"Invalid source snapshot JSON: {error}"]

    current = {
        "head": run_git(repository_root, "rev-parse", "HEAD"),
        "branch": run_git(repository_root, "branch", "--show-current"),
        "working_tree": working_tree_state(repository_root, change_name),
    }
    errors: list[str] = []
    for key, current_value in current.items():
        if snapshot.get(key) != current_value:
            errors.append(
                f"Baseline drift for '{key}': expected {snapshot.get(key)!r}, "
                f"found {current_value!r}"
            )
    return errors


def main() -> int:
    """????????????????????????"""
    parser = argparse.ArgumentParser(
        description="Preflight an Architect change package before implementation.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--change", required=True)
    arguments = parser.parse_args()

    repository_root = arguments.repo_root.resolve()
    package_root = repository_root / ".agent-architect" / "changes" / arguments.change
    errors = validate_documents(package_root)
    if not errors and package_root.is_dir():
        try:
            errors.extend(
                validate_baseline(
                    repository_root,
                    package_root,
                    arguments.change,
                )
            )
        except RuntimeError as error:
            errors.append(str(error))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"PREFLIGHT PASSED: {package_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
