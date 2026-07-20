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
- ProhibitedNewConcepts: No plugin framework, no reflection-based discovery, no
  duplicate branch-owned dispatch table.

## Preconditions
- D-001 is approved and recorded in this plan.
- No registry module exists yet.
- The `architect-build` stage has not started modifying request entry wiring.

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedImplementationDetail |
| --- | --- | --- | --- |
| src/service/dispatch_registry.py | DispatchRegistry | create | Define one explicit registry type and its stable registration/lookup API. |
| src/service/dispatch_registry.py | select_handler | create | Implement deterministic lookup without reflection or runtime discovery. |

## ExplicitlyOutOfScope
- Do not modify request entry wiring in this task.
- Do not change handler business logic.
- Do not change the public error envelope.

## MUST DO
- M-T001-001: Create one explicit registry module that owns handler selection.
- M-T001-002: Keep the registration surface readable and static in repository code.

## MUST NOT DO
- N-T001-001: Do not add reflection, plugin loading, or import side effects.
- N-T001-002: Do not duplicate registry decisions inside the old entry branch flow.

## AtomicSteps
1. Create `src/service/dispatch_registry.py`.
2. Define the registry data structure and explicit registration API.
3. Define deterministic selection logic for the existing handler keys.
4. Leave entry wiring unchanged so the next task can switch over cleanly.

## ExecutionBoundaryRules
- BoundaryCompleteness: The exact boundary fully covers the registry module and
  deterministic lookup function required by this task.
- BuildBlockingGapCheck: No unresolved path, symbol, or preserved-surface gap
  remains for this task.
- AdditionalRules: Only create the registry boundary described by D-001. If a
  helper is needed, keep it inside the new registry module. Do not touch
  transport-facing code in this task.

## CrossBoundaryEscalation
- TriggerCondition: A required implementation step would touch request entry
  wiring, handler business logic, transport-facing code, or any path outside
  `src/service/dispatch_registry.py`.
- ApprovalQuestion: The `architect-build` stage discovered work outside the sealed boundary for
  T-001. Reply with `1` to approve only the described temporary
  cross-boundary change, `2` to reject it and stop the `architect-build`
  stage, or `3` to approve all later truly necessary minimal cross-boundary
  changes during the current `architect-build` invocation.
- Option1: Approve only the described temporary cross-boundary change for
  T-001.
- Option2: Reject the temporary cross-boundary change and stop the `architect-build` stage for new
  `architect-design` / `architect-propose` guidance.
- Option3: Approve all later truly necessary minimal cross-boundary changes for
  T-001 and later tasks during the current `architect-build` invocation, with
  each actual overrun still described and logged factually when it occurs.
- TemporaryOverrideScope: The smallest explicitly described path, symbol, and
  operation outside the sealed T-001 boundary.

## TaskDeclaredExecutionResults
- CommandOrProcedure: Inspect the created registry module and confirm that all
  current dispatch keys map through one explicit registry structure.
- ExpectedRecordedResult: The registry module exists, contains deterministic
  lookup logic, and introduces no reflection-based discovery path.

## CompletionCondition
The repository contains one explicit registry boundary for dispatch selection,
and request entry code is still untouched.
