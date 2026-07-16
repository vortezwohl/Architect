---
name: architect-propose
description: "Create a sealed Markdown-first plan package from an approved Architect Design bundle. Use when every design unit, compatibility boundary, and approval evidence is known and the user wants deterministic artifacts, atomic implementation tasks, centralized state, and build-ready validation under .architect/."
---

# Architect Propose

Convert approved design units into a dense, Markdown-first implementation
contract. Markdown files are the single source of truth for design and task
intent. `.state/execution-state.json` is the only mutable task-status source.

## Strict Boundary

- Create or update only `.architect/<plan-name>/` after user authorization.
- Do not edit application code, tests, runtime configuration, or unrelated
  documentation.
- Do not invent a design unit, concept, boundary, anti-pattern, or rule.
- Do not create a task that cannot cite approved `D-xxx` design units and their
  concrete rules.
- Do not mark a package buildable while a placeholder, encoding error, unknown
  decision, incomplete boundary, or unresolved approval remains.

## Required Input

Before creating a package, require all of the following:

1. The complete approved Design bundle with `D-xxx` identifiers.
2. Approval evidence that explicitly covers every referenced design unit.
3. Compatibility intent, objective, non-goals, affected surfaces, and risks.
4. A kebab-case plan name, provided by the user or safely derived from the
   approved design.
5. The user's document language, inferred from the current interaction unless
   the user explicitly requests another language.

## Deterministic Package Creation

Use the bundled commands rather than manually creating identifiers, timestamps,
directories, state records, or hashes:

```text
python scripts/make_plan.py --repo-root <root> --plan <name> --language <tag>
python scripts/plan_control.py add-design --repo-root <root> --plan <name> --slug <slug>
python scripts/plan_control.py add-task --repo-root <root> --plan <name> --slug <slug>
```

The commands generate English metadata fields, IDs, filenames, timestamps,
state records, and content digests. Agent-authored prose fills only
`{{AGENT:...}}` areas in the user's document language. Do not add or rename
fields, headings, files, identifiers, or directories manually.

## Package Layout

```text
.architect/<plan-name>/
|-- 00-plan-manifest.md
|-- 01-context-and-contract.md
|-- 02-design-catalog.md
|-- 03-designs/D-001-<slug>.md
|-- 04-impact-and-boundaries.md
|-- 05-task-catalog.md
|-- 06-tasks/T-001-<slug>.md
|-- 07-verification-plan.md
|-- 08-execution-log.md
`-- .state/
    |-- execution-state.json
    `-- checkpoints/
```

`02-design-catalog.md` provides design navigation and approval coverage.
`03-designs/` holds complete design units. `05-task-catalog.md` provides task
order and dependencies without duplicating task content. `06-tasks/` contains
one atomic implementation intention per file. `07-verification-plan.md` stays
whole because it is supporting evidence, not the source of design decisions.

## Task Contract

Every `T-xxx` document must state exact paths, symbols, operations, permitted
design changes, out-of-scope changes, approved design references, approved rule
references, task-specific `MUST DO`, task-specific `MUST NOT DO`, atomic steps,
scope recovery, local verification, and a completion condition.

Task rules must express design constraints. For example, "the state machine is
the only transition owner" is valid; "make the feature work" is not. A task
that needs a new pattern, dependency direction, state transition, error
contract, or file outside the approved boundary must return to Design.

## Sealing and Validation

After all placeholders are filled, seal the package and validate it:

```text
python scripts/plan_control.py seal --repo-root <root> --plan <name>
python scripts/validate_plan.py --repo-root <root> --plan <name>
```

Sealing assigns deterministic rule IDs and a plan digest. Validation rejects
invalid UTF-8, BOMs, suspicious encoding markers, unresolved placeholders,
incorrect English metadata fields, missing counterexamples or anti-patterns,
unapproved design references, incomplete task boundaries, state drift, and
digest drift. Do not automatically rewrite semantic prose; stop, inspect the
reported text, correct it from evidence, then validate again.

## Completion Standard

Finish only after validation succeeds and report the package path, actual
validation result, remaining risk, and the `$architect-build <plan-name>`
handoff. Do not imply that a sealed package proves the implementation is done.
