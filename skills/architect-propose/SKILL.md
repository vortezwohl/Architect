---
name: architect-propose
description: "Create a build-ready architecture change package from a user-approved Architect Design decision. Use when the architecture, compatibility intent, and scope are confirmed and the user wants precise Markdown artifacts, source baseline capture, impact mapping, atomic tasks, and verification criteria under .agent-architect/changes/."
---

# Architect Propose

Convert an approved architecture decision into a project-local, build-ready change package. The package is the contract consumed by `architect-build`; it must remove operational ambiguity instead of restating a high-level design.

## Strict boundary

- Do not edit application code, tests, runtime configuration, or unrelated documentation.
- Create or update only `.agent-architect/changes/<change-name>/` after explicit user authorization.
- Do not silently make an architecture decision. If approval evidence or compatibility intent is missing, return to `$architect-design`.
- Do not mark a package build-ready while placeholders, unresolved decisions, incomplete task scope, or missing verification remain.

## Input contract

Require all of the following before creating artifacts:

1. A kebab-case change name.
2. User-approved architecture decision.
3. Recorded compatibility intent and contract boundary.
4. Objective, non-goals, and known affected surfaces.

If a change directory already exists, ask whether the user wants to continue it or create a distinct change. Never overwrite an existing package without explicit authorization.

## Package layout

Create this directory under the target project root:

```text
.agent-architect/changes/<change-name>/
|-- 00-overview.md
|-- 01-context-and-baseline.md
|-- 02-compatibility-contract.md
|-- 03-architecture-decision.md
|-- 04-impact-map.md
|-- 05-detailed-design.md
|-- 06-task-plan.md
|-- 07-verification-plan.md
|-- 08-implementation-log.md
`-- .state/
    `-- source-snapshot.json
```

Use the bundled `templates/` files as the initial structure. The templates are intentionally incomplete; replace every `[REQUIRED]` marker with evidence-backed content before validation.

## Workflow

1. Confirm the input contract and the target project root.
2. Create `.agent-architect/changes/<change-name>/` and `.state/` using the repository's controlled file-operation tool.
3. Copy every Markdown template into the package.
4. Run `python scripts/capture_baseline.py --repo-root <project-root>` and write its JSON output to `.state/source-snapshot.json` using the controlled file-operation tool.
4. Run `python scripts/capture_baseline.py --repo-root <project-root> --change <change-name>` and write its JSON output to `.state/source-snapshot.json` using the controlled file-operation tool.
6. Complete the package in dependency order:
   - Context and baseline.
   - Compatibility contract.
   - Architecture decision.
   - Impact map.
   - Detailed design.
   - Atomic task plan.
   - Verification plan.
7. Make every task independently executable. Each task must state allowed files, exact symbols, change steps, preconditions, prohibited changes, verification command, expected result, and completion condition.
8. Run `python scripts/validate_plan.py --repo-root <project-root> --change <change-name>`.
9. If validation fails, repair the package only; do not begin implementation.
10. Report the package path, actual validation result, remaining risks, and the `$architect-build <change-name>` handoff.

## Operational ambiguity gate

A package is not build-ready when any of the following is true:

- A required document is missing.
- A `[REQUIRED]`, `TODO`, `TBD`, `to be decided`, `as needed`, or equivalent unresolved marker remains.
- A task lacks explicit file scope, symbol scope, implementation steps, verification command, expected result, or completion condition.
- Compatibility behavior, migration, rollback, error handling, concurrency semantics, or state transitions are relevant but undocumented.
- The design needs an unrecorded judgment during implementation.

Use ?operationally unambiguous? to mean that `architect-build` can either execute a bounded task exactly as written or stop with a precise discrepancy. It is not a claim that future code or external systems can never change.

## Completion standard

Finish only after the validator passes, the baseline snapshot exists, the package contains a user-approved architecture decision, every task has a bounded verification path, and all known uncertainty is either resolved or explicitly blocks build.
