# Subdesign: D-002-error-result-contract

## Metadata
- DocumentType: Design
- DocumentId: D-002
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## Concept
- CanonicalName: Error Contract
- Category: Interface Contract
- Reference: Stable error contracts preserve caller expectations when internal
  execution boundaries are refactored.

## Intent
Freeze one explicit error-result contract so internal dispatch refactoring does
not silently change caller-visible failure behavior.

## StableCoreAndVariation
- Stable core: the externally visible error envelope and meaning stay fixed.
- Variation: internal code may normalize errors before returning the stable
  contract.

## Rationale
Dispatch refactoring can accidentally change failure shape, message placement,
or status mapping. Recording the contract as a separate approved subdesign
prevents Build from changing external error behavior while it restructures
internal control flow.

## Alternatives
- Keep error handling implicit in each handler branch: rejected because contract
  drift becomes difficult to detect.
- Collapse all failures into one generic exception output: rejected because it
  weakens compatibility for existing callers.

## DesignBoundaries
- This design controls the external error envelope only.
- It does not prescribe internal exception class hierarchy.
- It does require one consistent normalization point before returning to
  callers.

## Counterexamples
- A brand-new internal-only API with no compatibility requirement may not need a
  frozen error contract.
- Pure batch tooling with no stable caller-facing protocol may choose simpler
  failure reporting.

## AntiPatterns
- Returning branch-specific error shapes from different handlers.
- Allowing raw internal exceptions to leak through the external contract.
- Changing field names or status mapping during the refactor.

## Rules

### MUST DO
- R-D002-001: Preserve the current external error envelope shape for all existing callers.
- R-D002-002: Normalize handler failures before they leave the dispatch flow.

### MUST NOT DO
- R-D002-N001: Do not let raw internal exceptions escape to the external contract.
- R-D002-N002: Do not introduce per-handler error envelope variations.
