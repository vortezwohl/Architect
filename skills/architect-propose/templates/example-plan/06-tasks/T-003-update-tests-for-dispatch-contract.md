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
- ProhibitedNewConcepts: No test-only dispatch behavior or public error variant.

## Preconditions
- T-001 and T-002 have completed and preserve caller-visible behavior.

## FunctionalBoundary
- TargetFunctionality: Prove deterministic registry routing and preserved public
  request and error behavior.
- ProtectedRelatedFunctionality: Production behavior, public contract assertions,
  and the existing test harness semantics remain unchanged.
- ExplicitNonGoals: New production behavior and a new test framework are outside
  this task.
- CompatibilityObligations: Tests continue to assert existing caller-visible
  success and error behavior.
- HardStopCondition: Stop if required coverage needs production behavior changes
  or a protected contract relaxation.

## CodeImpactScope
| ExpectedPath | SymbolOrArea | ExpectedChange | EvidenceOrReason |
| --- | --- | --- | --- |
| tests/test_dispatch_flow.py | request/error assertions | Update contract coverage | D-002 requires stable external failures. |
| tests/test_dispatch_registry.py | lookup coverage | Add focused selection tests | D-001 requires deterministic registry selection. |

## ImpactScopeAdaptationRules
- CoverageIntent: Cover request-flow and registry behavior with the existing test facilities.
- AdaptiveExpansionRule: Add a fixture or helper only after confirming it does
  not alter production behavior or test-harness semantics.
- AssessmentAndLogRequirement: Record every adaptation, its evidence, and the
  boundary-preservation verification.

## MUST DO
- M-T003-001: Add focused coverage for the registry boundary.
- M-T003-002: Preserve caller-visible success and error assertions in updated tests.

## MUST NOT DO
- N-T003-001: Do not rewrite tests to assert only internal details.
- N-T003-002: Do not remove caller-visible error contract assertions.

## AtomicSteps
1. Update request-flow tests without relaxing public assertions.
2. Add focused deterministic registry lookup coverage.

## FunctionalBoundaryEscalation
- TriggerCondition: No compliant minimal implementation can preserve the stated functional boundary.
- RequiredAnalysis: Show attempted in-boundary designs, protected functionality, code impact scope evidence, and why each rejected alternative fails.
- Recommendation: Select `2` because it is the best supported path for this conflict.
- ApprovalQuestion: Reply with `1` to preserve current coverage and stop this task, `2` to add focused contract tests, `3` to approve the described compatibility fixture, or `4` to approve the described test-semantics change.
- DecisionScope: Only the explicitly analyzed functional conflict and its minimum necessary implementation scope.
- RecordRequirement: Record the selected path, rationale, actual affected code, and verification in execution state and log.

### DecisionOptions
| Number | Path | FunctionalImpact | CompatibilityImpact | Verification |
| --- | --- | --- | --- | --- |
| 1 | Preserve current coverage and leave T-003 blocked. | New contract remains unproven. | Existing tests remain unchanged. | Confirm no test behavior was changed. |
| 2 | Add focused dispatch-contract tests. | Proves target behavior. | Existing test semantics remain unchanged. | Run focused and full relevant test suites. |
| 3 | Add the smallest compatibility fixture for both paths. | Proves both contract paths. | Existing fixtures remain valid. | Verify both fixture modes and regression coverage. |
| 4 | Change the described test semantics after approval. | Alters the protected test contract. | Existing expectations may change. | Verify the approved revised test contract. |

## TaskDeclaredExecutionResults
- CommandOrProcedure: Run dispatch-related request, error, and registry tests.
- ExpectedRecordedResult: Tests prove deterministic selection and preserved
  caller-visible behavior.

## CompletionCondition
Coverage proves the approved target functionality without changing protected behavior.
