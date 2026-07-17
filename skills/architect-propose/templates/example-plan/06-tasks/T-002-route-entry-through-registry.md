# Task: T-002-route-entry-through-registry

## Metadata
- DocumentType: Task
- DocumentId: T-002
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## DesignSources
- SubdesignRefs: D-001, D-002
- RuleRefs: R-D001-001, R-D001-N001, R-D002-001, R-D002-002, R-D002-N001, R-D002-N002
- ProhibitedNewConcepts: No new transport contract, no branch-specific error
  envelope, no alternate dispatch path beside the registry.

## Preconditions
- T-001 has completed and the registry boundary exists.
- The current request entry function still owns caller-facing behavior.
- D-001 and D-002 are both approved and recorded in this plan.

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedImplementationDetail |
| --- | --- | --- | --- |
| src/service/entry.py | handle_request | modify | Replace branch-owned handler selection with registry delegation while preserving external request behavior. |
| src/service/error_contract.py | normalize_dispatch_error | create | Add one shared normalization point for handler failures before returning to callers. |

## ExplicitlyOutOfScope
- Do not introduce new request fields.
- Do not change handler business rules.
- Do not update tests in this task.

## MUST DO
- M-T002-001: Delegate handler selection to the registry created in T-001.
- M-T002-002: Normalize failures through one shared error contract before returning.

## MUST NOT DO
- N-T002-001: Do not leave a second dispatch branch structure active beside the registry.
- N-T002-002: Do not leak raw internal exceptions to callers.

## AtomicSteps
1. Update `handle_request` to use `DispatchRegistry` for handler selection.
2. Add `normalize_dispatch_error` as the single outward error normalization
   point.
3. Remove now-redundant branch-owned dispatch logic from the entry flow.
4. Keep the public request and error contract unchanged.

## ExecutionBoundaryRules
- Keep routing and error normalization explicit in code.
- Do not alter storage, deployment, or transport configuration.
- Do not redesign the approved registry pattern during implementation.

## TaskDeclaredExecutionResults
- CommandOrProcedure: Inspect `handle_request` and verify that selection goes
  through the registry and that outward failures pass through one normalization
  function.
- ExpectedRecordedResult: Entry wiring delegates selection to the registry, no
  duplicate branch logic remains, and the external error envelope stays stable.

## CompletionCondition
Request entry delegates dispatch through the registry and applies one shared
error normalization contract without changing the caller-visible interface.
