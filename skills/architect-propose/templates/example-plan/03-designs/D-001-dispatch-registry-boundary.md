# Subdesign: D-001-dispatch-registry-boundary

## Metadata
- Document Type: Design
- Document ID: D-001
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Concept
- Canonical Name: Registry
- Category: Behavioral Coordination Boundary
- Reference: A registry centralizes stable lookup rules while keeping concrete
  handler implementations independent from entry wiring.

## Intent
Create one stable dispatch-selection boundary so request entry code stops owning
handler routing policy directly.

## Stable Core and Variation
- Stable core: the request entry path delegates handler selection to one
  registry interface.
- Variation: new handlers may be added by extending the registry mapping
  without rewriting the entry branch structure.

## Repository Evidence
- Current request entry logic owns both request parsing and dispatch selection.
- Existing branching rules are duplicated in the entry path rather than
  isolated behind one inspectable boundary.
- The current repository already treats handlers as separate business units, so
  the missing seam is selection ownership rather than handler implementation.

## Compatibility Boundary
- Preserve the current external request contract and the currently supported
  dispatch outcomes.
- Allow internal routing structure to change as long as caller-visible request
  semantics remain stable.
- Do not add a runtime plugin mechanism or any new public extension surface in
  this plan.

## Pattern Decision
- Decision: Reject GoF for the primary decision and record this subdesign as a
  direct architectural boundary.
- Why: the repository needs one explicit ownership boundary for handler
  selection, but not a full GoF pattern hierarchy.
- Rejected neighbors: Strategy was rejected because no stable algorithm family
  is selected at runtime by a caller-owned slot; Facade was rejected because
  the issue is not repeated subsystem choreography.

## External Evidence Decision
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

## Functional Boundary
- Target functionality: move handler selection out of request entry code.
- Protected related functionality: request parsing, handler business rules, and
  caller-visible request and error behavior remain unchanged.
- Explicit non-goals: runtime plugins, reflection, and a public extension model.
- Hard-stop condition: stop if explicit registry selection requires changing a
  protected caller-visible behavior or non-goal.

## Code Impact Scope
- Expected locations: the new registry module, request entry wiring, and
  focused dispatch tests.
- The surface is a reference; build may add a helper or fixture only after an
  impact assessment confirms the functional boundary remains intact.

## Verification Seams
- Verify that request entry delegates selection through one registry boundary.
- Verify that no duplicate branch-owned routing logic remains after the
  refactor.
- Verify that extending the registry mapping does not require changing the
  caller-visible request contract.

## Counterexamples
- A single fixed handler with no branching need does not justify a registry.
- Highly dynamic runtime plugin discovery would require a different design.

## Anti-Patterns
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
