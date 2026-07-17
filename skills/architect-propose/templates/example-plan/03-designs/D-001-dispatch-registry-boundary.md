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

## Rationale
The current branching flow couples request parsing, dispatch selection, and
handler invocation. A registry isolates the selection decision, removes
duplicated branching rules, and gives later tasks one explicit place to extend
or inspect dispatch behavior.

## Alternatives
- Keep the current conditional chain: rejected because dispatch rules stay
  duplicated and entry logic remains hard to audit.
- Introduce reflection-based auto-discovery: rejected because it adds implicit
  behavior and weakens boundary clarity for Build.

## DesignBoundaries
- The registry owns only handler selection.
- Request parsing and handler business logic stay outside the registry.
- Registry extension is explicit and code-declared, not dynamic.

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
