---
name: architect-build
description: "Implement a validated architecture change package produced by Architect Propose. Use when the user wants to build or continue a named .architect/<change-name>/ package with strict baseline checks, task-scoped edits, task-level verification, and implementation logging."
---

# Architect Build

Build only what the approved change package specifies. The package is the implementation contract; it is not a suggestion or a starting point for new architecture work.

## Strict boundary

- Do not select a new architecture, introduce unplanned abstractions, or expand file scope.
- Do not implement when the change package fails preflight.
- Do not mark a task complete before its specified verification succeeds.
- Do not continue after a baseline mismatch, design contradiction, missing detail, or task-scope expansion. Return to `$architect-propose` with a precise discrepancy.

## Input and selection

Accept an optional kebab-case change name. If omitted:

1. Infer it from explicit conversation context.
2. Auto-select only when exactly one active package exists under `.architect/`.
3. Otherwise ask the user to select a package.

Always announce the selected package and the way to override it.

## Preflight

Before editing any project file:

1. Read every package artifact and `.state/source-snapshot.json`.
2. Run `python scripts/preflight_change.py --repo-root <project-root> --change <change-name>`.
3. Stop if preflight reports missing artifacts, unresolved markers, incomplete task fields, Git `HEAD` drift, branch drift, or working-tree drift.
4. Confirm that the next unfinished task has one exact scope and verification path.

## Task execution loop

For one pending task at a time:

1. Announce the task ID and its allowed files.
2. Make only the specified changes to the listed files and symbols.
3. Compare the changed-file set with the task's allowed-file set. Stop on any extra file.
4. Run the task's verification commands and record the actual result.
5. If verification succeeds, update the task status in `06-task-plan.md` and append an entry to `08-implementation-log.md` using the repository's controlled file-operation tool.
6. If verification fails, do not update status. Diagnose the failure within the task boundary; stop if resolving it needs a design or scope change.
7. Move to the next task only after the current one is complete and logged.

## Required discrepancy response

Pause and return to `architect-propose` when any of the following occurs:

- The source baseline changed after proposal.
- A caller, contract, state transition, error path, or migration surface was omitted.
- The task requires an additional file, symbol, dependency, or abstraction.
- The package does not define a relevant behavior or verification result.
- Existing code or framework constraints contradict the detailed design.

Report the exact artifact section, task ID, observed code evidence, and the smallest required package correction. Do not repair the package silently while building.

## Completion standard

Finish only when all tasks are verified and logged, package-level verification passes, compatibility and rollback checks have been run as specified, and the final report distinguishes actual validation from remaining risk.
