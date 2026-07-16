"""Capture a Git baseline snapshot for an Architect change package."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run_git(repository_root: Path, *arguments: str) -> str:
    """Run a Git command and return its standard output.

    Args:
        repository_root: Root directory of the Git repository.
        *arguments: Arguments passed to the Git command.

    Returns:
        The command stdout with surrounding whitespace removed.

    Raises:
        RuntimeError: Raised when the Git command exits with a non-zero status.
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
    """Return the working tree state while ignoring the change package path.

    The proposal stage creates or updates files under `.agent-architect/changes/`.
    Those package files should not be treated as unrelated working tree drift.

    Args:
        repository_root: Root directory of the Git repository.
        change_name: Name of the Architect change package.

    Returns:
        Filtered `git status --porcelain=v1` output.
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


def build_snapshot(repository_root: Path, change_name: str) -> dict[str, object]:
    """Build the JSON-serializable baseline snapshot payload.

    Args:
        repository_root: Root directory used to collect Git metadata.
        change_name: Name of the Architect change package.

    Returns:
        A JSON-ready dictionary describing the baseline revision and worktree.
    """
    return {
        "head": run_git(repository_root, "rev-parse", "HEAD"),
        "branch": run_git(repository_root, "branch", "--show-current"),
        "working_tree": working_tree_state(repository_root, change_name),
        "ignored_change_path": f".agent-architect/changes/{change_name}/",
    }


def main() -> int:
    """Parse CLI arguments and print the baseline snapshot JSON."""
    parser = argparse.ArgumentParser(
        description="Emit a Git baseline snapshot for an Architect change package.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--change", required=True)
    arguments = parser.parse_args()
    repository_root = arguments.repo_root.resolve()

    try:
        snapshot = build_snapshot(repository_root, arguments.change)
    except RuntimeError as error:
        parser.error(str(error))

    print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
