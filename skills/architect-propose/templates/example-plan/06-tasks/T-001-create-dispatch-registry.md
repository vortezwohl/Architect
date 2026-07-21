# Task: T-001-create-dispatch-registry

## Metadata
- DocumentType: Task
- DocumentId: T-001
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## DesignSources
- SubdesignRefs: D-001
- RuleRefs: R-D001-001, R-D001-002, R-D001-N001, R-D001-N002
- ProhibitedNewConcepts: No plugin framework, reflection-based discovery, or
  duplicate branch-owned dispatch table.

## Preconditions
- D-001 is approved and no registry module exists yet.

## FunctionalBoundary
- TargetFunctionality: Create one explicit registry that owns handler selection.
- ProtectedRelatedFunctionality: Request parsing, handler business rules, and
  public request and error behavior remain unchanged.
- ExplicitNonGoals: Request entry rewiring, runtime plugins, and transport
  changes are outside this task.
- CompatibilityObligations: Existing callers observe no public behavior change.
- HardStopCondition: Stop if registry creation requires changing protected
  behavior or adding a prohibited runtime extension mechanism.

## CodeImpactScope
| ExpectedPath | SymbolOrArea | ExpectedChange | EvidenceOrReason |
| --- | --- | --- | --- |
| src/service/dispatch_registry.py | DispatchRegistry | Add registry and lookup | D-001 assigns selection ownership here. |

## ImpactScopeAdaptationRules
- CoverageIntent: Cover the new registry module and likely focused test helpers.
- AdaptiveExpansionRule: Add a necessary helper or fixture only after confirming
  it preserves the functional boundary and is the smallest viable choice.
- AssessmentAndLogRequirement: Record the evidence, alternatives, affected
  locations, and verification for every impact-scope adaptation.

## MUST DO
- M-T001-001: Create one explicit registry module that owns handler selection.
- M-T001-002: Keep the registration surface readable and static in repository code.

## MUST NOT DO
- N-T001-001: Do not add reflection, plugin loading, or import side effects.
- N-T001-002: Do not duplicate registry decisions inside the old entry branch flow.

## AtomicSteps
1. Create the registry data structure and deterministic selection logic.
2. Keep request entry wiring unchanged until T-002.

## FunctionalBoundaryEscalation
- TriggerCondition: No compliant minimal implementation can preserve the stated functional boundary.
- RequiredAnalysis: Show attempted in-boundary designs, protected functionality, code impact scope evidence, and why each rejected alternative fails.
- Recommendation: Select `3` because it is the best supported path for this conflict.
- ApprovalQuestion: Reply with `1` to preserve protected behavior and stop this task, `2` to approve the described behavior change, or `3` to approve the compatibility path.
- DecisionScope: Only the explicitly analyzed functional conflict and its minimum necessary implementation scope.
- RecordRequirement: Record the selected path, rationale, actual affected code, and verification in execution state and log.

### DecisionOptions
| Number | Path | FunctionalImpact | CompatibilityImpact | Verification |
| --- | --- | --- | --- | --- |
| 1 | Preserve protected behavior and leave T-001 blocked. | Target functionality remains incomplete. | No public behavior change. | Confirm no implementation change was applied. |
| 2 | Approve the described protected-behavior change. | Changes the protected request behavior. | Existing callers may observe the new behavior. | Verify the approved new request behavior. |
| 3 | Add the smallest compatibility path that preserves both behaviors. | Completes target functionality without changing the protected behavior. | Existing callers retain the current behavior. | Verify both behavior paths and focused regressions. |

## TaskDeclaredExecutionResults
- CommandOrProcedure: Inspect registry selection and its focused checks.
- ExpectedRecordedResult: Selection is explicit and deterministic without
  reflection-based discovery.

## CompletionCondition
The registry owns handler selection while protected functionality is unchanged.
