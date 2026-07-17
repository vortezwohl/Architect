---
name: architect-propose
description: "Manual-only skill. Use only when the user explicitly invokes the architect-propose skill to turn one already approved design bundle into one new independent sealed plan package under `.architect/`. One approved design bundle may contain multiple D-xxx subdesigns, and one resulting plan may contain multiple T-xxx tasks. Do not auto-trigger from a design or implementation request."
---

# Architect Propose

Use this skill only as a manually selected plan-packaging stage. Its job is to
store an already approved design bundle as a structured execution package and
initialize the package state and execution log. It does not redesign, implement
code, or invoke sibling skills automatically. It is stage 2 of the one-way
flow `architect-design -> architect-propose -> architect-build`.

## Defined Terms

- `approved design bundle`: the complete approved output from one
  `architect-design` invocation.
- `D-xxx subdesign`: one approved architectural decision inside that bundle.
- `independent plan`: one new future `.architect/<plan-name>/` package created
  from exactly one approved design bundle.
- `T-xxx task`: one recorded execution task inside that independent plan. A
  single independent plan may contain multiple `T-xxx` tasks derived from one
  or more approved `D-xxx` subdesigns.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-propose`.
- Do not auto-switch into `architect-build`.
- If planning finishes and the user wants to continue, the only forward next
  stage is `architect-build`, invoked manually by the user.

## Strict Boundary

- Create or update only `.architect/<plan-name>/` after user authorization.
- Do not edit application code, tests, runtime configuration, or unrelated
  documentation.
- Do not invent or revise a design unit, concept, boundary, anti-pattern, or
  rule.
- Do not reopen, revise, or repair the approved design from this skill.
- Do not create a task that cannot cite approved `D-xxx` design units and their
  concrete rules.
- Do not seal a package while any required design input, task boundary, state
  initialization, or log initialization is incomplete.

## Required Input

Before creating a package, require all of the following:

1. The complete approved design bundle with `D-xxx` identifiers.
2. Recorded approval evidence that covers every referenced design unit.
3. Compatibility intent, objective, non-goals, affected surfaces, and risks.
4. A kebab-case plan name, provided by the user or safely derived from the
   approved design.
5. The user's document language, inferred from the current interaction unless
   the user explicitly requests another language.

## Core Outcome

Create one structured package that later execution can follow without
reinterpreting design intent:

- store the full approved design bundle in stable package files;
- record every approved `D-xxx` subdesign from that bundle inside the new
  independent plan;
- translate the approved `D-xxx` subdesigns into one or more atomic `T-xxx`
  tasks without adding new design decisions;
- order the tasks as one complete execution sequence for a later Build run;
- initialize centralized task state before Build starts;
- initialize the execution log before Build starts;
- leave a sealed package whose content, state, and log all agree on what is
  ready to execute.

## Deterministic Package Creation

Use repository-provided Python plan tooling, not manual package creation, for
all initial package structure, identifier allocation, sealing, and final
validation. The agent must not hand-create the initial package directory tree,
the initial package files, task state, or plan digest. In this repository's
native setup, the required helper commands are:

```text
python scripts/make_plan.py --repo-root <root> --plan <name> --language <tag>
python scripts/plan_control.py add-design --repo-root <root> --plan <name> --slug <slug>
python scripts/plan_control.py add-task --repo-root <root> --plan <name> --slug <slug>
```

Initialize the package root with `make_plan.py`, allocate design documents and
task documents with `plan_control.py`, seal with `plan_control.py seal`, and
perform final validation with `validate_plan.py`. In another runtime, use an
equivalent repository wrapper only if it preserves the same contract.

The agent may fill only script-created files and script-created document slots.
The agent must not manually create the initial package directory tree, initial
package files, initial task state, or plan digest. Do not add or rename
fields, headings, files, identifiers, or directories manually.

If any script or validator reports invalid UTF-8, a UTF-8 BOM, or suspicious
encoding markers, immediately correct the corrupted content and rerun the
relevant script until the package is clean.

## Package Contract

The package root is:

```text
.architect/<plan-name>/
```

For a concrete directory-level reference, inspect `templates/example-plan/`.
That example mirrors one complete sealed plan package file-for-file and
directory-for-directory, except that it lives under `templates/` for study
rather than under `.architect/` for live execution.

It must contain these artifacts:

- `00-plan-manifest.md`
- `01-context-and-contract.md`
- `02-design-catalog.md`
- `03-designs/D-xxx-<slug>.md`
- `04-impact-and-boundaries.md`
- `05-task-catalog.md`
- `06-tasks/T-xxx-<slug>.md`
- `07-verification-plan.md`
- `08-execution-log.md`
- `.state/execution-state.json`

Initialize `.state/execution-state.json` and `08-execution-log.md` as part of
package creation. Build should start from these recorded artifacts, not infer
missing state from memory.

Every `T-xxx` document must state exact paths, symbols, operations, approved
subdesign references, approved rule references, task-specific `MUST DO`,
task-specific `MUST NOT DO`, atomic steps, status update expectations, log
expectations, task-declared execution-result steps, and a completion
condition. Together, the task set must form one complete execution path that
Build can run through in order.

If packaging reveals a need for a new pattern, dependency direction, state
transition, error contract, or file outside the approved boundary, preserve the
approved inputs as they are. Do not invent the missing decision, do not reopen
earlier stages from this skill, do not silently redesign the package, and do
not record unapproved design content as if it were approved.

## Sealing and Validation

After all placeholders are filled, seal the package and validate it:

```text
python scripts/plan_control.py seal --repo-root <root> --plan <name>
python scripts/validate_plan.py --repo-root <root> --plan <name>
```

Do not redesign the package after a validation failure. Stop, inspect the
reported evidence, correct the package from approved inputs, correct any
encoding corruption immediately if reported, and validate again.

## Completion Standard

Finish only after validation succeeds. Report the package path, actual
validation result, initialized state/log artifacts, remaining risk, and whether
the user may manually invoke `architect-build` as the next stage for the
selected plan.
