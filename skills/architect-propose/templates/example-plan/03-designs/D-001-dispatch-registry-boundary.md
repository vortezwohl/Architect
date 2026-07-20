# Subdesign: D-001-dispatch-registry-boundary

## Metadata
- DocumentType: Design
- DocumentId: D-001
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## Concept
- CanonicalName: Registry
- Category: Behavioral Coordination Boundary
- Reference: A registry centralizes stable lookup rules while keeping concrete
  handler implementations independent from entry wiring.

## Intent
Create one stable dispatch-selection boundary so request entry code stops owning
handler routing policy directly.

## StableCoreAndVariation
- Stable core: the request entry path delegates handler selection to one
  registry interface.
- Variation: new handlers may be added by extending the registry mapping
  without rewriting the entry branch structure.

## RepositoryEvidence
- Current request entry logic owns both request parsing and dispatch selection.
- Existing branching rules are duplicated in the entry path rather than
  isolated behind one inspectable boundary.
- The current repository already treats handlers as separate business units, so
  the missing seam is selection ownership rather than handler implementation.

## CompatibilityBoundary
- Preserve the current external request contract and the currently supported
  dispatch outcomes.
- Allow internal routing structure to change as long as caller-visible request
  semantics remain stable.
- Do not add a runtime plugin mechanism or any new public extension surface in
  this plan.

## PatternDecision
- Decision: Reject GoF for the primary decision and record this subdesign as a
  direct architectural boundary.
- Why: the repository needs one explicit ownership boundary for handler
  selection, but not a full GoF pattern hierarchy.
- Rejected neighbors: Strategy was rejected because no stable algorithm family
  is selected at runtime by a caller-owned slot; Facade was rejected because
  the issue is not repeated subsystem choreography.

## ExternalEvidenceDecision
- Considered evidence: registry-style coordination guidance, GoF comparison
  material, and framework examples that centralize dispatch ownership.
- Accepted evidence: the external guidance that recommends one explicit lookup
  seam when routing rules would otherwise scatter horizontally.
- Rejected evidence: dynamic auto-discovery and plugin-oriented examples were
  rejected because the repository does not show a real need for runtime
  extension or reflective loading.
- Repository fit reasoning: the accepted evidence strengthens a direct,
  code-declared registry boundary without adding speculative indirection.

## Rationale
The current branching flow couples request parsing, dispatch selection, and
handler invocation. A registry isolates the selection decision, removes
duplicated branching rules, and gives later tasks one explicit place to extend
or inspect dispatch behavior.

## Alternatives
- Keep the current conditional chain: rejected because dispatch rules stay
  duplicated and entry logic remains hard to audit.
- Introduce reflection-based auto-discovery: rejected because it adds implicit
  behavior and weakens boundary clarity for the `architect-build` stage.

## DesignBoundaries
- The registry owns only handler selection.
- Request parsing and handler business logic stay outside the registry.
- Registry extension is explicit and code-declared, not dynamic.

## VerificationSeams
- Verify that request entry delegates selection through one registry boundary.
- Verify that no duplicate branch-owned routing logic remains after the
  refactor.
- Verify that extending the registry mapping does not require changing the
  caller-visible request contract.

## Counterexamples
- A single fixed handler with no branching need does not justify a registry.
- Highly dynamic runtime plugin discovery would require a different design.

## AntiPatterns
- Rebuilding conditional dispatch logic beside the registry.
- Making the registry responsible for request mutation or business execution.
- Hiding dispatch entries behind reflection or import side effects.

## Rules

### MUST DO
- R-D001-001: Route handler selection through one explicit registry boundary.
- R-D001-002: Keep registry entries declarative and readable from repository code.

### MUST NOT DO
- R-D001-N001: Do not leave duplicate dispatch rules in the entry flow after registry wiring
  is complete.
- R-D001-N002: Do not introduce reflection-based auto-discovery or plugin loading.
