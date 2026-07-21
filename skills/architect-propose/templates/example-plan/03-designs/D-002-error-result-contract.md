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

## RepositoryEvidence
- The repository already exposes a caller-visible error envelope that existing
  tests and callers depend on.
- Internal refactoring will move dispatch control flow, which creates a real
  risk of drifting status mapping or field placement.
- Current failure handling is distributed enough that one explicit preservation
  rule is needed before the `architect-build` stage starts restructuring internals.

## CompatibilityBoundary
- Preserve the existing external error envelope for all current callers.
- Allow internal normalization and error-routing changes as long as outward
  field names, meaning, and status mapping remain compatible.
- Do not broaden this subdesign into a new exception taxonomy or transport
  redesign.

## PatternDecision
- Decision: Reject GoF for the primary decision and record this subdesign as an
  interface-contract preservation boundary.
- Why: the repository needs an explicit compatibility rule for outward failure
  behavior, not a reusable object-pattern abstraction.
- Rejected neighbors: Proxy was rejected because the problem is not mediated
  access; Template Method was rejected because the contract risk is envelope
  preservation, not fixed step sequencing.

## ExternalEvidenceDecision
- Considered evidence: compatibility-preservation guidance, interface-contract
  examples, and error-normalization patterns from framework practice.
- Accepted evidence: the external guidance that recommends freezing caller
  contracts before internal refactors that move control flow.
- Rejected evidence: generic "collapse all failures" advice was rejected
  because it would weaken current compatibility for existing callers.
- Repository fit reasoning: accepted evidence is used only to preserve the
  current external contract while leaving internal exception structure flexible.

## Rationale
Dispatch refactoring can accidentally change failure shape, message placement,
or status mapping. Recording the contract as a separate approved subdesign
prevents the `architect-build` stage from changing external error behavior while it restructures
internal control flow.

## Alternatives
- Keep error handling implicit in each handler branch: rejected because contract
  drift becomes difficult to detect.
- Collapse all failures into one generic exception output: rejected because it
  weakens compatibility for existing callers.

## FunctionalBoundary
- Target functionality: normalize internal handler failures before returning the
  existing external error envelope.
- Protected related functionality: external field names, meanings, and status
  mappings remain unchanged for current callers.
- Explicit non-goals: a new exception taxonomy, transport redesign, or changed
  public failure semantics.
- Hard-stop condition: stop if one normalization point cannot preserve the
  protected external error behavior.

## CodeImpactScope
- Expected locations: request entry wiring, one error normalization module, and
  contract-focused tests.
- The surface is a reference; build may adapt internal helper placement only
  after assessing and logging the preserved caller-visible behavior.

## VerificationSeams
- Verify that the external error envelope shape remains unchanged for existing
  callers.
- Verify that handler failures pass through one normalization point before
  leaving the dispatch flow.
- Verify that no branch-specific error envelope variations are introduced during
  refactoring.

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
