"""Initialize an Architect change package directory and template files.

This script only performs deterministic directory and file creation.
It does not fill template content and does not overwrite an existing package.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CHANGE_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEMPLATE_FILES = (
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


def validate_change_name(change_name: str) -> None:
    """Validate that the change name satisfies the kebab-case constraint.

    Args:
        change_name: User-provided change name.

    Raises:
        ValueError: Raised when the change name does not satisfy the constraint.
    """
    if not CHANGE_NAME_PATTERN.fullmatch(change_name):
        raise ValueError(
            "Change name must be kebab-case and contain only lowercase "
            "letters, numbers, and hyphens."
        )


def copy_templates(templates_root: Path, package_root: Path) -> None:
    """Copy template files into the target change package directory.

    Args:
        templates_root: Template directory.
        package_root: Target change package directory.
    """
    for template_name in TEMPLATE_FILES:
        template_path = templates_root / template_name
        target_path = package_root / template_name
        content = template_path.read_text(encoding="utf-8")
        target_path.write_text(content, encoding="utf-8")


def initialize_package(repo_root: Path, change_name: str) -> Path:
    """Create the change package directory and write template files.

    Args:
        repo_root: Target repository root.
        change_name: Change package name.

    Returns:
        The created change package directory.

    Raises:
        FileExistsError: Raised when the target change package already exists.
        FileNotFoundError: Raised when the template directory or files are missing.
    """
    templates_root = Path(__file__).resolve().parent.parent / "templates"
    if not templates_root.is_dir():
        raise FileNotFoundError(f"Templates directory not found: {templates_root}")

    package_root = repo_root / ".architect" / change_name
    if package_root.exists():
        raise FileExistsError(f"Change package already exists: {package_root}")

    (repo_root / ".architect").mkdir(parents=True, exist_ok=True)
    package_root.mkdir()
    copy_templates(templates_root, package_root)
    return package_root


def main() -> int:
    """Parse CLI arguments and initialize the change package."""
    parser = argparse.ArgumentParser(
        description="Create an Architect change package from bundled templates.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--change", required=True)
    arguments = parser.parse_args()

    repo_root = arguments.repo_root.resolve()
    validate_change_name(arguments.change)
    package_root = initialize_package(repo_root, arguments.change)
    print(f"INITIALIZED: {package_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
