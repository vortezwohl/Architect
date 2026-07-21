# Context and Contract

## Metadata
- Document Type: Context and Contract
- Document ID: CONTEXT
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Observed Facts
- The current request entry path mixes request parsing, handler selection, and
  error shaping in one branch-heavy flow.
- Handler selection rules are duplicated across multiple conditional branches.
- Existing callers already depend on the current request payload shape and the
  current error envelope shape.
- The approved design bundle requires one future `architect-build` run to execute multiple
  ordered tasks, not one isolated patch.

## Approved Input Limits
- Use only the approved design bundle recorded in this plan.
- Record only repository evidence and user-approved compatibility boundaries.
- Do not add new design ideas, fallback architectures, or unapproved patterns
  during packaging.

## Compatibility Intent
- Preserve the external request contract and the external error envelope.
- Internal branching may be restructured as long as external behavior remains
  contract-compatible.

## Functional Boundary
- Requested Functionality: Replace branch-owned dispatch selection with an explicit
  registry while preserving the current request and error behavior.
- Protected Functionality: Handler business rules, transport behavior,
  storage behavior, and caller-visible request and error semantics remain
  unchanged.
- Explicit Non-Goals: Runtime plugins, storage/schema changes, transport redesign,
  and a new public extension model are outside this plan.
- Compatibility Guarantees: Existing callers continue to send the same payload
  and receive the same success and error envelope.
- Mandatory Stop Condition: Stop if registry-based routing cannot be completed without
  changing protected caller-visible behavior or an explicit non-goal.

## Preserved Contracts
- Request payload schema stays unchanged.
- Public handler invocation contract stays unchanged.
- Error responses remain explicit, typed, and stable for current callers.

## Explicitly Permitted Contract Changes
- None approved in this design bundle.

## Execution Constraints
- The `architect-build` stage must execute tasks in recorded order.
- The `architect-build` stage may make minimal local design decisions only when
  they preserve the functional boundary.
- The `architect-build` stage must update task state and execution log truthfully as work progresses.
