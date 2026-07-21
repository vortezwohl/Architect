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
- ProhibitedNewConcepts: No transport contract, branch-specific error envelope,
  or alternate dispatch path beside the registry.

## Preconditions
- T-001 has completed and D-001 and D-002 remain approved.

## FunctionalBoundary
- TargetFunctionality: Route request entry through the registry and one error
  normalization point.
- ProtectedRelatedFunctionality: Public request fields, handler business rules,
  error envelope, storage, deployment, and transport behavior remain unchanged.
- ExplicitNonGoals: New request fields, storage changes, and test rewrites are
  outside this task.
- CompatibilityObligations: Existing callers receive the same successful and
  failed response semantics.
- HardStopCondition: Stop if registry routing or normalization cannot preserve
  the existing public contract.

## CodeImpactScope
| ExpectedPath | SymbolOrArea | ExpectedChange | EvidenceOrReason |
| --- | --- | --- | --- |
| src/service/entry.py | handle_request | Route through registry | D-001 moves selection ownership. |
| src/service/error_contract.py | normalize_dispatch_error | Add normalization | D-002 freezes outward failures. |

## ImpactScopeAdaptationRules
- CoverageIntent: Cover entry wiring, normalization, and any direct contract test
  helper needed to prove preserved behavior.
- AdaptiveExpansionRule: Expand only after assessing callers and protected
  behavior, then choose the smallest viable implementation.
- AssessmentAndLogRequirement: Record each adaptation with alternatives,
  affected code, functional-boundary check, and verification.

## MUST DO
- M-T002-001: Delegate handler selection to the registry created in T-001.
- M-T002-002: Normalize failures through one shared error contract before returning.

## MUST NOT DO
- N-T002-001: Do not leave a second dispatch branch structure active beside the registry.
- N-T002-002: Do not leak raw internal exceptions to callers.

## AtomicSteps
1. Route handler selection through the registry.
2. Normalize outward failures through one shared point.
3. Remove redundant branch-owned dispatch logic while preserving public behavior.

## FunctionalBoundaryEscalation
- TriggerCondition: No compliant minimal implementation can preserve the stated functional boundary.
- RequiredAnalysis: Show attempted in-boundary designs, protected functionality, code impact scope evidence, and why each rejected alternative fails.
- Recommendation: Select `2` because it is the best supported path for this conflict.
- ApprovalQuestion: Reply with `1` to preserve the current contract and stop this task, or `2` to approve the scoped adapter path.
- DecisionScope: Only the explicitly analyzed functional conflict and its minimum necessary implementation scope.
- RecordRequirement: Record the selected path, rationale, actual affected code, and verification in execution state and log.

### DecisionOptions
| Number | Path | FunctionalImpact | CompatibilityImpact | Verification |
| --- | --- | --- | --- | --- |
| 1 | Preserve the current contract and leave T-002 blocked. | Registry routing remains incomplete. | No caller-visible change. | Confirm no routing change was applied. |
| 2 | Add the smallest adapter that preserves the public contract. | Completes registry routing. | Existing callers retain request and error behavior. | Verify old request and error contract through the adapter. |

## TaskDeclaredExecutionResults
- CommandOrProcedure: Inspect routing and error normalization with contract checks.
- ExpectedRecordedResult: Entry routes through the registry and outward errors
  preserve the existing envelope.

## CompletionCondition
Entry delegates dispatch and preserves caller-visible success and error behavior.
