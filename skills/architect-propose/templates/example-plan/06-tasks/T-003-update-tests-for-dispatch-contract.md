# Task: T-003-update-tests-for-dispatch-contract

## Metadata
- DocumentType: Task
- DocumentId: T-003
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## DesignSources
- SubdesignRefs: D-001, D-002
- RuleRefs: R-D001-001, R-D002-001, R-D002-002, R-D002-N001, R-D002-N002
- ProhibitedNewConcepts: No new test-only dispatch behavior and no new public
  error envelope variant.

## Preconditions
- T-001 and T-002 have completed.
- Registry-based dispatch and shared error normalization are implemented.
- Existing tests still reflect the old branch-owned behavior and must be
  updated to the new internal structure without changing external assertions.

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedImplementationDetail |
| --- | --- | --- | --- |
| tests/test_dispatch_flow.py | dispatch success and failure coverage | modify | Update or add assertions that prove registry-based routing preserves caller-visible behavior. |
| tests/test_dispatch_registry.py | registry lookup coverage | create | Add focused coverage for deterministic registry selection. |

## ExplicitlyOutOfScope
- Do not introduce new production behavior.
- Do not relax existing public contract assertions.
- Do not redesign task ordering or design rules.

## MUST DO
- M-T003-001: Add focused coverage for the registry boundary.
- M-T003-002: Preserve caller-visible success and error assertions in the updated tests.

## MUST NOT DO
- N-T003-001: Do not rewrite tests to assert only internal details.
- N-T003-002: Do not remove caller-visible error contract assertions.

## AtomicSteps
1. Update existing request-flow tests so they still assert the public contract.
2. Add focused registry lookup tests for the new explicit boundary.
3. Keep internal-structure assertions secondary to caller-visible behavior.

## ExecutionBoundaryRules
- Tests must reflect the approved design and the preserved contracts.
- Do not add a new test harness framework.
- Keep assertions deterministic and easy to map back to D-001 and D-002.

## TaskDeclaredExecutionResults
- CommandOrProcedure: Run the dispatch-related test suite or the equivalent
  repository test target that covers request routing and error normalization.
- ExpectedRecordedResult: The relevant tests pass while preserving the caller-
  visible request and error contract expectations.

## CompletionCondition
Test coverage proves that registry-based dispatch preserves the existing
caller-visible contract and that deterministic registry selection is covered.
