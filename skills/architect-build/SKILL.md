---
name: architect-build
description: "Implement one sealed Markdown-first Architect plan task at a time with centralized task state, exact file-boundary checks, checkpoint rollback, and interruption recovery. Use only after Architect Propose validation succeeds."
---

# Architect Build

Build only the sealed design and task contract. Build does not design, extend,
reinterpret, migrate, or repair the plan. It either executes one bounded task
exactly as written or restores the task checkpoint and reports the discrepancy.

## Strict Boundary

- Do not select a new architecture, pattern, concept, dependency direction, or
  lifecycle behavior.
- Do not edit task or design Markdown files after the plan is sealed.
- Do not modify a source path outside the active task's exact boundary.
- Do not continue after a scope breach, incomplete detail, design contradiction,
  missing approval, or failed recovery.
- Do not mark a task complete before scope validation and the task's actual
  verification evidence are recorded.

## Preflight

Before any source edit, select one plan and run:

```text
python scripts/build_control.py preflight --repo-root <root> --plan <name>
```

Preflight requires an exclusive Git worktree, a valid sealed package, valid
encoding, matching plan digest, complete centralized state, and exact task
documents. Read the manifest, context, design catalog, impact boundaries, task
catalog, verification plan, active task, and every `D-xxx` document referenced
by that task.

If `.state/execution-state.json` reports an active task, do not inspect partial
implementation as a continuation point. First run:

```text
python scripts/build_control.py recover --repo-root <root> --plan <name>
```

Recovery restores the task checkpoint and marks the attempt rolled back so a
memoryless agent resumes only from verified completed tasks.

## Task Execution Loop

For exactly one pending task:

1. Announce its `T-xxx` ID, cited `D-xxx` units, allowed paths, symbols,
   operations, `MUST DO`, and `MUST NOT DO` rules.
2. Create a checkpoint and acquire the exclusive lock:

   ```text
   python scripts/build_control.py start --repo-root <root> --plan <name> --task <T-xxx>
   ```

3. Perform one declared atomic step. Do not add an unapproved helper, wrapper,
   pattern, file, state transition, or error behavior.
4. After every atomic edit, check scope:

   ```text
   python scripts/build_control.py scope-check --repo-root <root> --plan <name> --task <T-xxx>
   ```

5. Run the task's listed verification command and compare the actual result with
   its expected result.
6. Record actual evidence only after scope and verification pass:

   ```text
   python scripts/build_control.py complete --repo-root <root> --plan <name> --task <T-xxx> --evidence <actual-result>
   ```

7. Continue only with the next pending task after the current task is completed.

## Mandatory Scope-Breach Recovery

When scope checking reports any unexpected path, the controller immediately
records the breach and restores the task checkpoint. Do not manually repair the
extra file and keep the task attempt alive.

```text
python scripts/build_control.py rollback --repo-root <root> --plan <name> --task <T-xxx> --reason <manual-recovery-cause>
```

The controller restores the entire source tree to the task checkpoint, verifies
the restoration digest, records the event, releases the lock, and marks the
attempt rolled back. The explicit rollback command exists for manual recovery
after another detected failure. If restoration fails, the task is blocked and
Build must return the exact evidence to Propose or Design.

## Required Return to Design

Return to `architect-design` when a task requires a concept or rule not covered
by an approved `D-xxx` unit. Return to `architect-propose` when the approved
design remains valid but the plan omitted a file, symbol, task, precondition,
verification rule, or impact boundary. Report the document, ID, code evidence,
and smallest required correction. Do not modify the sealed plan silently.

## Completion Standard

Finish only after all centralized task states are `completed`, the verification
plan's required checks have actual recorded results, the final plan preflight
succeeds, and the final report distinguishes completed evidence from remaining
risk.
