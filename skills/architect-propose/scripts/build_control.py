"""Control task-scoped Architect Build state, checkpoints, and recovery.

The controller never chooses a design or expands a task boundary. It snapshots
the exclusive workspace before a task, detects every changed source path, and
restores the complete task checkpoint before another attempt can continue.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import os
import re
import shutil

from plan_protocol import (
    PlanProtocolError,
    load_state,
    read_utf8,
    write_state,
    write_utf8,
)
from validate_plan import validate_package


TASK_PATH_PATTERN = re.compile(r"^(T-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
CONTROL_DIRECTORY_NAMES = {
    ".architect",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
TRANSIENT_FILE_NAMES = {".coverage"}


def timestamp() -> str:
    """Return a generated timestamp for factual execution events.

    Returns:
        Local timestamp with millisecond precision.
    """

    return datetime.now().strftime("%Y-%m-%d:%H:%M:%S.%f")[:-3]


def selected_package(repo_root: Path, plan_name: str) -> Path:
    """Return the selected plan package root.

    Args:
        repo_root: Repository root that owns ``.architect``.
        plan_name: Selected plan package name.

    Returns:
        Plan package root.

    Raises:
        PlanProtocolError: Raised when the package does not exist.
    """

    package = repo_root / ".architect" / plan_name
    if not package.is_dir():
        raise PlanProtocolError(f"Plan package does not exist: {package}")
    return package


def validate_exclusive_git_workspace(repo_root: Path) -> None:
    """Require a Git worktree before a destructive rollback-capable task starts.

    Args:
        repo_root: Candidate Git worktree root.

    Raises:
        PlanProtocolError: Raised when the repository has no Git metadata.
    """

    if not (repo_root / ".git").exists():
        raise PlanProtocolError(
            "Build requires an exclusive Git worktree for deterministic rollback.",
        )


def is_control_path(relative_path: Path) -> bool:
    """Return whether a path belongs to Architect control data.

    Args:
        relative_path: Repository-relative path.

    Returns:
        ``True`` when the path is excluded from source checkpoints.
    """

    return any(part in CONTROL_DIRECTORY_NAMES for part in relative_path.parts)


def source_files(repo_root: Path) -> dict[str, Path]:
    """Collect every regular source file outside Git and Architect control paths.

    Args:
        repo_root: Exclusive repository worktree root.

    Returns:
        Repository-relative POSIX paths mapped to source file paths.

    Raises:
        PlanProtocolError: Raised when a symbolic link would make restoration unsafe.
    """

    files: dict[str, Path] = {}
    for root, directories, filenames in os.walk(repo_root):
        root_path = Path(root)
        relative_root = root_path.relative_to(repo_root)
        directories[:] = [
            directory
            for directory in directories
            if not is_control_path(relative_root / directory)
        ]
        for filename in filenames:
            path = root_path / filename
            relative_path = path.relative_to(repo_root)
            if is_control_path(relative_path):
                continue
            if path.name in TRANSIENT_FILE_NAMES:
                continue
            if path.is_symlink():
                raise PlanProtocolError(
                    f"Symbolic links are not supported by checkpoint recovery: {relative_path}",
                )
            if path.is_file():
                files[relative_path.as_posix()] = path
    return files


def digest_file(path: Path) -> str:
    """Return the SHA-256 digest for one source file.

    Args:
        path: Existing regular source file.

    Returns:
        Lower-case SHA-256 digest.
    """

    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest(repo_root: Path) -> dict[str, str]:
    """Return a deterministic digest manifest for every checkpointed source file.

    Args:
        repo_root: Exclusive repository worktree root.

    Returns:
        Source path to SHA-256 digest mapping.
    """

    return {
        relative_path: digest_file(path)
        for relative_path, path in sorted(source_files(repo_root).items())
    }


def task_document(package: Path, task_id: str) -> Path:
    """Find the unique Markdown task document for one generated task identifier.

    Args:
        package: Selected plan package root.
        task_id: Generated task identifier.

    Returns:
        Unique task Markdown path.

    Raises:
        PlanProtocolError: Raised when no unique task file exists.
    """

    paths = list((package / "06-tasks").glob(f"{task_id}-*.md"))
    if len(paths) != 1 or not TASK_PATH_PATTERN.fullmatch(paths[0].name):
        raise PlanProtocolError(f"Task document is missing or ambiguous: {task_id}")
    return paths[0]


def allowed_paths(package: Path, task_id: str) -> set[str]:
    """Parse exact file boundaries from a task's Markdown boundary table.

    Args:
        package: Selected plan package root.
        task_id: Generated task identifier.

    Returns:
        Exact repository-relative paths allowed to change in the task.

    Raises:
        PlanProtocolError: Raised when the required boundary table is malformed.
    """

    lines = read_utf8(task_document(package, task_id)).splitlines()
    collecting = False
    paths: set[str] = set()
    for line in lines:
        if line == "## ExactChangeBoundary":
            collecting = True
            continue
        if collecting and line.startswith("## "):
            break
        if not collecting or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or cells[0] in {"Path", "---"} or set(cells[0]) == {"-"}:
            continue
        if len(cells) != 4 or not cells[0] or any("{{" in cell for cell in cells):
            raise PlanProtocolError(f"Malformed exact change boundary in {task_id}")
        path = Path(cells[0])
        if path.is_absolute() or ".." in path.parts:
            raise PlanProtocolError(f"Unsafe boundary path in {task_id}: {cells[0]}")
        paths.add(path.as_posix())
    if not paths:
        raise PlanProtocolError(f"Task has no exact allowed paths: {task_id}")
    return paths


def checkpoint_root(package: Path, checkpoint_id: str) -> Path:
    """Return the path reserved for one generated checkpoint.

    Args:
        package: Selected plan package root.
        checkpoint_id: Generated checkpoint identifier.

    Returns:
        Checkpoint directory path.
    """

    return package / ".state" / "checkpoints" / checkpoint_id


def create_checkpoint(repo_root: Path, package: Path, task_id: str, attempt: int) -> str:
    """Copy the complete source tree into a task-level recovery checkpoint.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        task_id: Generated task identifier.
        attempt: One-based task attempt number.

    Returns:
        Generated checkpoint identifier.
    """

    checkpoint_id = f"{task_id}-attempt-{attempt:03d}"
    root = checkpoint_root(package, checkpoint_id)
    if root.exists():
        raise PlanProtocolError(f"Checkpoint already exists: {checkpoint_id}")
    files_root = root / "files"
    manifest = source_manifest(repo_root)
    for relative_path, source_path in source_files(repo_root).items():
        target_path = files_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
    write_utf8(root / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
    return checkpoint_id


def load_checkpoint_manifest(package: Path, checkpoint_id: str) -> dict[str, str]:
    """Load one checkpoint's expected complete source manifest.

    Args:
        package: Selected plan package root.
        checkpoint_id: Existing checkpoint identifier.

    Returns:
        Source path to digest mapping.

    Raises:
        PlanProtocolError: Raised when checkpoint data is absent or invalid.
    """

    path = checkpoint_root(package, checkpoint_id) / "manifest.json"
    try:
        payload = json.loads(read_utf8(path))
    except (OSError, json.JSONDecodeError) as error:
        raise PlanProtocolError(f"Invalid checkpoint manifest: {checkpoint_id}") from error
    if not isinstance(payload, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in payload.items()
    ):
        raise PlanProtocolError(f"Invalid checkpoint source manifest: {checkpoint_id}")
    return payload


def restore_checkpoint(repo_root: Path, package: Path, checkpoint_id: str) -> None:
    """Restore every checkpointed source file and remove task-attempt additions.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        checkpoint_id: Existing checkpoint identifier.

    Raises:
        PlanProtocolError: Raised when restoration cannot reproduce the checkpoint.
    """

    expected = load_checkpoint_manifest(package, checkpoint_id)
    checkpoint_files = checkpoint_root(package, checkpoint_id) / "files"
    for relative_path, current_path in source_files(repo_root).items():
        if relative_path not in expected:
            current_path.unlink()
    for relative_path in expected:
        source_path = checkpoint_files / relative_path
        if not source_path.is_file():
            raise PlanProtocolError(
                f"Checkpoint source file is missing: {checkpoint_id}/{relative_path}",
            )
        target_path = repo_root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
    remove_empty_directories(repo_root)
    if source_manifest(repo_root) != expected:
        raise PlanProtocolError(f"Checkpoint restoration verification failed: {checkpoint_id}")


def remove_empty_directories(repo_root: Path) -> None:
    """Remove empty source directories while preserving Git and Architect controls.

    Args:
        repo_root: Exclusive repository worktree root.
    """

    for root, directories, _ in os.walk(repo_root, topdown=False):
        path = Path(root)
        relative_path = path.relative_to(repo_root)
        if not relative_path.parts or is_control_path(relative_path):
            continue
        try:
            path.rmdir()
        except OSError:
            pass


def changed_paths(repo_root: Path, package: Path, checkpoint_id: str) -> set[str]:
    """Return every source path that differs from a task checkpoint.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        checkpoint_id: Existing checkpoint identifier.

    Returns:
        Changed, created, or deleted repository-relative source paths.
    """

    before = load_checkpoint_manifest(package, checkpoint_id)
    after = source_manifest(repo_root)
    return {
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    }


def append_log(package: Path, event: str, task_id: str, detail: str) -> None:
    """Append one generated factual event to the immutable execution log.

    Args:
        package: Selected plan package root.
        event: Fixed event name.
        task_id: Related generated task identifier.
        detail: Observed factual detail.
    """

    path = package / "08-execution-log.md"
    content = read_utf8(path)
    entry = (
        f"\n## {timestamp()} {event} {task_id}\n"
        f"- Detail: {detail}\n"
    )
    write_utf8(path, content + entry)


def write_lock(package: Path, task_id: str) -> None:
    """Acquire the plan's exclusive Build lock.

    Args:
        package: Selected plan package root.
        task_id: Task that owns the lock.

    Raises:
        PlanProtocolError: Raised when another active lock exists.
    """

    path = package / ".state" / "lock.json"
    if path.exists():
        raise PlanProtocolError("Build lock exists; run recover before continuing.")
    write_utf8(path, json.dumps({"TaskId": task_id, "LockedAt": timestamp()}))


def remove_lock(package: Path) -> None:
    """Release the exclusive Build lock when a task attempt ends.

    Args:
        package: Selected plan package root.
    """

    path = package / ".state" / "lock.json"
    if path.exists():
        path.unlink()


def preflight(repo_root: Path, package: Path) -> None:
    """Verify that static plan content is buildable before task execution.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.

    Raises:
        PlanProtocolError: Raised when the plan or worktree is not ready.
    """

    validate_exclusive_git_workspace(repo_root)
    errors = validate_package(package)
    if errors:
        raise PlanProtocolError("Plan preflight failed: " + " | ".join(errors))


def ensure_static_plan_is_sealed(package: Path) -> None:
    """Reject an active task when immutable plan documents drift after preflight.

    Args:
        package: Selected plan package root.

    Raises:
        PlanProtocolError: Raised when a static plan document no longer validates.
    """

    errors = validate_package(package)
    if errors:
        raise PlanProtocolError("Static plan drift detected: " + " | ".join(errors))


def start_task(repo_root: Path, package: Path, task_id: str) -> None:
    """Start one pending task after creating a complete source checkpoint.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        task_id: Task selected for execution.

    Raises:
        PlanProtocolError: Raised when state, locking, or boundaries are invalid.
    """

    preflight(repo_root, package)
    state = load_state(package)
    if state.get("CurrentTask") is not None:
        raise PlanProtocolError("A task is already active; run recover before continuing.")
    tasks = state.get("Tasks")
    if not isinstance(tasks, dict) or task_id not in tasks:
        raise PlanProtocolError(f"Task is not registered in centralized state: {task_id}")
    task_state = tasks[task_id]
    if not isinstance(task_state, dict) or task_state.get("State") not in {"pending", "rolled-back"}:
        raise PlanProtocolError(f"Task is not ready to start: {task_id}")
    allowed_paths(package, task_id)
    attempt = int(task_state.get("Attempt", 0)) + 1
    write_lock(package, task_id)
    checkpoint_id = create_checkpoint(repo_root, package, task_id, attempt)
    task_state.update(
        {
            "Attempt": attempt,
            "CheckpointId": checkpoint_id,
            "StartedAt": timestamp(),
            "State": "active",
        },
    )
    state["CurrentTask"] = task_id
    write_state(package, state)
    append_log(package, "TASK_STARTED", task_id, f"CheckpointId={checkpoint_id}")


def check_scope(repo_root: Path, package: Path, task_id: str) -> set[str]:
    """Verify the active task has changed only its exact declared file paths.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        task_id: Active task identifier.

    Returns:
        Current changed source paths when scope validation passes.

    Raises:
        PlanProtocolError: Raised when the task is inactive or has crossed scope.
    """

    state = load_state(package)
    if state.get("CurrentTask") != task_id:
        raise PlanProtocolError(f"Task is not active: {task_id}")
    task_state = state["Tasks"][task_id]
    checkpoint_id = task_state.get("CheckpointId")
    if not isinstance(checkpoint_id, str):
        raise PlanProtocolError(f"Active task has no checkpoint: {task_id}")
    try:
        ensure_static_plan_is_sealed(package)
    except PlanProtocolError as error:
        rollback_task(repo_root, package, task_id, str(error))
        raise
    changed = changed_paths(repo_root, package, checkpoint_id)
    unexpected = changed - allowed_paths(package, task_id)
    if unexpected:
        detail = ", ".join(sorted(unexpected))
        task_state["State"] = "rollback-required"
        task_state["LastDiscrepancy"] = detail
        write_state(package, state)
        append_log(package, "SCOPE_BREACH", task_id, detail)
        rollback_task(repo_root, package, task_id, f"Scope breach: {detail}")
        raise PlanProtocolError(
            f"Task crossed its exact boundary and was rolled back: {detail}",
        )
    task_state["State"] = "scope-verified"
    write_state(package, state)
    return changed


def rollback_task(repo_root: Path, package: Path, task_id: str, reason: str) -> None:
    """Restore an active task to its checkpoint before another attempt is allowed.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.
        task_id: Active or rollback-required task identifier.
        reason: Recorded factual cause for the rollback.

    Raises:
        PlanProtocolError: Raised when no recoverable checkpoint exists.
    """

    state = load_state(package)
    tasks = state.get("Tasks")
    if not isinstance(tasks, dict) or task_id not in tasks:
        raise PlanProtocolError(f"Task is not registered: {task_id}")
    task_state = tasks[task_id]
    checkpoint_id = task_state.get("CheckpointId")
    if not isinstance(checkpoint_id, str):
        raise PlanProtocolError(f"Task has no recoverable checkpoint: {task_id}")
    restore_checkpoint(repo_root, package, checkpoint_id)
    task_state["State"] = "rolled-back"
    task_state["LastDiscrepancy"] = reason
    state["CurrentTask"] = None
    write_state(package, state)
    remove_lock(package)
    append_log(package, "TASK_ROLLED_BACK", task_id, reason)


def complete_task(package: Path, task_id: str, evidence: str) -> None:
    """Mark a scope-verified task complete after Build records actual evidence.

    Args:
        package: Selected plan package root.
        task_id: Scope-verified task identifier.
        evidence: Actual command result or factual verification reference.

    Raises:
        PlanProtocolError: Raised when state or verification evidence is invalid.
    """

    if not evidence.strip():
        raise PlanProtocolError("Completion requires non-empty verification evidence.")
    ensure_static_plan_is_sealed(package)
    state = load_state(package)
    if state.get("CurrentTask") != task_id:
        raise PlanProtocolError(f"Task is not active: {task_id}")
    task_state = state["Tasks"][task_id]
    if task_state.get("State") != "scope-verified":
        raise PlanProtocolError(f"Task must pass scope verification before completion: {task_id}")
    task_state["State"] = "completed"
    task_state["CompletedAt"] = timestamp()
    task_state["VerificationEvidence"] = [evidence]
    state["CurrentTask"] = None
    write_state(package, state)
    remove_lock(package)
    append_log(package, "TASK_COMPLETED", task_id, evidence)


def recover_active_task(repo_root: Path, package: Path) -> None:
    """Rollback an interrupted active task before a memoryless agent continues.

    Args:
        repo_root: Exclusive repository worktree root.
        package: Selected plan package root.

    Raises:
        PlanProtocolError: Raised when no active task exists.
    """

    state = load_state(package)
    task_id = state.get("CurrentTask")
    if not isinstance(task_id, str):
        raise PlanProtocolError("No active task requires recovery.")
    rollback_task(repo_root, package, task_id, "Interrupted task recovery")


def main() -> int:
    """Parse Build control commands and return a deterministic exit status.

    Returns:
        Process exit status.
    """

    parser = argparse.ArgumentParser(
        description="Control Architect Build task state and checkpoint recovery.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("preflight", "recover"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--repo-root", required=True, type=Path)
        command_parser.add_argument("--plan", required=True)
    for command in ("start", "scope-check", "rollback", "complete"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("--repo-root", required=True, type=Path)
        command_parser.add_argument("--plan", required=True)
        command_parser.add_argument("--task", required=True)
        if command == "rollback":
            command_parser.add_argument("--reason", required=True)
        if command == "complete":
            command_parser.add_argument("--evidence", required=True)
    arguments = parser.parse_args()
    try:
        repo_root = arguments.repo_root.resolve()
        package = selected_package(repo_root, arguments.plan)
        if arguments.command == "preflight":
            preflight(repo_root, package)
            print(f"READY: {package}")
        elif arguments.command == "start":
            start_task(repo_root, package, arguments.task)
            print(f"STARTED: {arguments.task}")
        elif arguments.command == "scope-check":
            changed = check_scope(repo_root, package, arguments.task)
            print(f"SCOPE_VALID: {arguments.task} -> {', '.join(sorted(changed))}")
        elif arguments.command == "rollback":
            rollback_task(repo_root, package, arguments.task, arguments.reason)
            print(f"ROLLED_BACK: {arguments.task}")
        elif arguments.command == "complete":
            complete_task(package, arguments.task, arguments.evidence)
            print(f"COMPLETED: {arguments.task}")
        else:
            recover_active_task(repo_root, package)
            print(f"RECOVERED: {package}")
    except PlanProtocolError as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
