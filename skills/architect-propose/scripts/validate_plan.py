"""Validate whether an Architect change package satisfies build prerequisites.

This script validates only the completeness and executability of proposal-stage
artifacts. It no longer saves or compares a workspace snapshot.
"""

from __future__ import annotations

import argparse
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
    "  - Command:",
    "  - Expected result:",
    "- Completion condition:",
)
REQUIRED_SECTION_MARKERS = {
    "00-overview.md": ("## Build entry condition",),
    "01-context-and-baseline.md": ("## Execution Preconditions",),
}


def validate_package(package_root: Path) -> list[str]:
    """Validate required documents, required sections, and task fields.

    Args:
        package_root: Change package root directory.

    Returns:
        Validation error list. An empty list means the package passes.
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
        for required_heading in REQUIRED_SECTION_MARKERS.get(document_path.name, ()):
            if required_heading not in content:
                errors.append(
                    f"Missing required section '{required_heading}' in "
                    f"{document_path.name}"
                )

    task_plan = package_root / "06-task-plan.md"
    if task_plan.is_file():
        content = task_plan.read_text(encoding="utf-8")
        tasks = [section for section in content.split("\n## T-") if section.strip()]
        if len(tasks) < 2:
            errors.append("Task plan must contain at least one '## T-' task heading.")
        for field in TASK_FIELDS:
            if field not in content:
                errors.append(f"Task plan is missing required field: {field}")
    return errors


def main() -> int:
    """Parse CLI arguments and print the package validation result."""
    parser = argparse.ArgumentParser(
        description="Validate an Architect change package before build.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--change", required=True)
    arguments = parser.parse_args()

    package_root = (
        arguments.repo_root.resolve()
        / ".architect"
        / arguments.change
    )
    errors = validate_package(package_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID: {package_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
