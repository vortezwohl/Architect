---
name: architect-build
description: "Manual-only skill. Use only when the user explicitly invokes the architect-build skill to execute the full sealed plan in order, strictly follow the stored design and task package, proactively restore core design context when context shrinks, and update execution state and logs truthfully. Do not auto-trigger from a generic implementation request."
---

# Architect Build

Use this skill only as a manually selected implementation stage. Its job is to
execute the sealed plan from start to finish and keep execution state and logs
truthfully aligned with actual progress. It does not redesign the plan,
question the stored solution, or invoke sibling skills automatically. It is
stage 3 and the final stage of the one-way flow `architect-design ->
architect-propose -> architect-build`.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-build`.
- Do not auto-switch into `architect-design` or `architect-propose`.
- Do not reopen earlier stages from this skill.

## Strict Boundary

- Do not select a new architecture, pattern, concept, dependency direction, or
  lifecycle behavior.
- Do not edit task or design Markdown files after the plan is sealed.
- Do not modify a source path outside the boundary of the tasks currently being
  executed.
- Do not silently skip a required status update or log update.
- Do not claim progress, completion, or task-declared execution result that did
  not actually happen.
- Do not reinterpret execution friction as a reason to redesign during Build.

## Core Outcome

Execute the stored package as one engineering run, not as a new design pass:

- load the sealed plan, full task sequence, current state, and current log;
- execute all recorded tasks in order until the stored plan is fully run;
- perform only the work allowed by each `T-xxx` task and its cited `D-xxx`
  units;
- proactively restate the core design context needed by the current tasks when
  the live context has been compressed or diluted;
- update task status as work actually advances;
- update the execution log with actual actions, results, and task-declared
  execution results as they happen;
- keep moving through the stored execution path instead of questioning the
  sealed solution.

## Start Condition

Before any source edit, read the sealed plan, current execution state, current
execution log, task catalog, every pending `T-xxx` task, and every referenced
`D-xxx` document needed for the current execution window. Use them as the
execution source of truth for this run. Continue from the recorded execution
point instead of re-evaluating the plan.

When the live conversation no longer contains the active objective, the current
task, the cited design rules, the current execution state, or the latest
factual log evidence, proactively rebuild a compact working context from the
package. That rebuilt context must include exactly those five items. Do not
rely on memory when the package already contains the needed context.

## Execution Loop

Run through the remaining task sequence in recorded order within the same
manual `architect-build` invocation:

1. Announce the next `T-xxx` task, its cited `D-xxx` units, allowed paths,
   symbols, operations, `MUST DO`, and `MUST NOT DO` rules.
2. Restate the task's required design context before editing. That restated
   context must include the task objective, the cited `D-xxx` rules, the
   allowed change boundary, the current execution state, and the latest
   relevant factual log entry.
3. Perform the declared atomic steps for that task. Do not add an unapproved
   helper, wrapper, pattern, file, state transition, or error behavior.
4. Immediately update task state when the task meaningfully changes status:
   started, in progress, or completed.
5. Immediately append log entries that record actual actions taken, affected
   scope, actual results, and actual task-declared execution results.
6. Perform only the task-declared execution-result steps already recorded in the sealed
   task, then record the real result in state and log without embellishment.
7. Continue directly to the next recorded task until all remaining tasks in the
   plan have been executed.

## Completion Standard

Finish only after the full recorded task sequence has been executed, every
required task-declared execution result has been recorded truthfully, and the
state and log accurately reflect what actually happened across the entire run.
The final report must distinguish completed evidence from remaining risk,
without reopening design judgment during Build.
