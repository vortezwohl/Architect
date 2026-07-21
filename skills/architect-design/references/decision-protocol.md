# Binding Design Decision Protocol

## Language Rule

Maintain this protocol and all skill instructions in English. Use the user's current language for user-facing proposals and the semantic body of plan documents unless the user explicitly requests another language. Plan field names, identifiers, timestamps, and status values remain fixed English tokens.

## How to Use This Protocol

1. Read this file first for the gates, approval boundaries, and non-negotiable output requirements.
2. Treat `architect-design` as a read-only stage. Inspect repository files and think through the architecture, but do not edit, create, or overwrite files at this stage.
3. Perform minimal context extraction before any knowledge injection. Extract only the repository facts needed to identify the system purpose, relevant entry points, affected modules, current behavior owner, caller path, state flow, current tests, and operational constraints for the requested change.
4. Establish basic repository understanding from that extracted context before design is recommended. This gate is satisfied only when you can explicitly state the system purpose, relevant entry points, affected modules, current behavior owner, caller path, state flow, constraints, and current tests for the requested change.
5. Read `source-article.md` only after Step 4 is satisfied and before the first design decision for methodology, pattern framing, and AI-era misuse warnings.
6. Read `gof-patterns.md` immediately after `source-article.md` and before any external architecture learning so the local GoF comparison frame is established first.
7. Convert what those references teach into explicit reasoning. Do not cite them mechanically or treat a pattern name as sufficient evidence.
8. Keep knowledge-source precedence and design-decision authority separate. Learn external supporting theory in this order: `source-article.md`, `gof-patterns.md`, external English-language academic papers, best-practice articles from top-tier engineering organizations, then other reliable supporting sources only if still needed.
9. Do not treat framework documentation as a default theory source, and do not treat a best practice, a famous paper, or a top-tier company example as a design command.
10. Repository facts, the current request, and the user-confirmed compatibility boundary outrank every external source. External knowledge may support a design only after repository-first reasoning proves that it fits this repository better than the available alternatives.

## Defined Terms

- `architect-design`: the manual stage that produces one approved design bundle.
- `minimal context extraction`: the smallest repository-focused evidence pass
  required before any knowledge injection or design reasoning begins.
- `basic repository understanding`: the post-extraction state in which the
  agent can explicitly state the system purpose, relevant entry points,
  affected modules, current behavior owner, caller path, state flow,
  constraints, and current tests for the requested change.
- `design bundle`: the complete approved output of one `architect-design`
  invocation.
- `D-xxx subdesign`: one independently explainable architectural decision inside
  the approved design bundle.
- `pattern decision`: the explicit judgment about whether the best supported
  design uses one GoF pattern, multiple GoF patterns, or no GoF pattern at all.
- `external evidence decision`: the explicit record of which external sources,
  patterns, papers, framework examples, or best-practice claims were accepted
  or rejected and why.
- `verification seam`: the concrete boundary that later `architect-build` work must test or
  preserve, such as an interface, lifecycle transition, error path,
  transaction edge, concurrency contract, ownership rule, or compatibility
  surface.
- `functional boundary`: the approved target functionality, protected related
  functionality, explicit non-goals, compatibility obligations, and hard-stop
  condition that build may not autonomously change.
- `code impact scope`: the known likely paths, symbols, configuration, tests,
  and callers affected by the design. It guides cautious execution but is not a
  hard path-level limit.
- `independent plan`: one new future `.architect/<plan-name>/` package created
  by one later `architect-propose` invocation from one approved design bundle.

## Gate 0: Compatibility and Functional Boundary Intent

After basic repository understanding is established and before any design recommendation that can affect behavior, contracts, data, configuration, integrations, or extension points, ask the user to choose:

1. Preserve the affected existing contracts.
2. Allow intentional breaking changes for a better long-term design.
3. Describe a custom compatibility boundary.

Do not infer an answer from repository age, deployment status, silence, or task wording. Restate the answer as preserved behavior, intentionally breakable behavior, consumers, migration obligations, and rollback limits.

Before recommending the design, confirm the target functionality, protected
related functionality, explicit non-goals, and the hard-stop condition proving
when build cannot meet the target without changing protected functionality or a
non-goal. Record a broad, evidence-based code impact scope, but do not treat
its incompleteness as permission to leave the functional boundary ambiguous.

## Evidence and Design Units

After Gate 0, inspect and deepen only the evidence relevant to the change: callers, existing tests, ownership, dependencies, state, lifecycle, error paths, transactions, concurrency, framework rules, and operational constraints.

Design remains read-only while collecting this evidence. You may read, inspect, compare, and reason about repository files, but you must not edit code, tests, configuration, documentation, plans, or generated artifacts in this stage.
Do not treat external architecture learning as a substitute for minimal context extraction or for basic repository understanding. The repository gate comes first.
Do not copy an external architecture only because it appears successful, elegant, widely adopted, or endorsed by a top-tier company. First derive the design from the repository facts, the request, the compatibility boundary, the real stable core, the actual variation, and the failure semantics that exist here.

Choose the globally best justified architecture for the stated evolution horizon under the current code reality, the user-approved compatibility boundary, and the strongest supporting external evidence. Compare the direct alternative, but do not grant it automatic priority merely because it is smaller. The approved design bundle may contain multiple `D-xxx` subdesigns. Every chosen `D-xxx` subdesign must include:
- A recognized engineering concept or pattern, canonical name, category, and reliable reference.
- The stable core, actual variation, collaborators, ownership, dependency direction, lifecycle, and failure semantics.
- Repository evidence, compatibility boundary, explicit pattern decision, and explicit external evidence decision.
- Concrete alternatives and rejected neighboring concepts.
- Explicit functional boundaries, code impact scopes, verification seams,
  counterexamples, and anti-patterns.
- Design-level `MUST DO` and `MUST NOT DO` rules that constrain implementation details rather than merely desired results.

Do not introduce an unnamed abstraction, speculative extension point, hidden global dependency, event without delivery semantics, or inheritance hierarchy without evidence that it improves the stated decision criteria.

## Teaching Output Contract

Before asking for approval, teach the design instead of only presenting a conclusion. For every non-trivial `D-xxx` subdesign, explain at least:

- The concrete problem this concept solves in the current repository or request.
- The repository facts, request constraints, and compatibility requirements that make this problem real here.
- The stable core and the real variation that justify the concept.
- Whether the best supported design uses one GoF pattern, multiple GoF patterns, or explicitly rejects GoF patterns.
- How the cited paper, pattern, or best practice was adapted to this repository instead of copied from a foreign context.
- Which outside evidence was considered, which evidence was accepted or rejected, and why those acceptance or rejection decisions follow from repository facts.
- The simplest direct design that was considered, and why it was accepted or rejected.
- The nearest neighboring pattern or abstraction that was rejected, and why.
- The likely misuse, counterexample, or operational failure that would make this concept a poor fit.
- The functional boundary that build must preserve, the expected code impact
  surface it may cautiously adapt, and the verification seam that must hold if
  `architect-build` later implements the design.

When possible, map the teaching explanation directly onto the design-unit fields: `Intent`, `StableCoreAndVariation`, `RepositoryEvidence`, `CompatibilityBoundary`, `PatternDecision`, `ExternalEvidenceDecision`, `Rationale`, `Alternatives`, `VerificationSeams`, `Counterexamples`, `AntiPatterns`, and `Rules`.

## Gate 1: Design Approval

Present the full design bundle. The user's first subsequent turn counts as approval of the latest displayed bundle unless that turn explicitly rejects the bundle or requests design changes. A direct user request to continue into `architect-propose` also counts as approval of the latest displayed bundle. If feedback changes one decision, revisit the affected `D-xxx` subdesign and obtain approval again under the same rule.

Record approval evidence and a digest of the approved bundle. One later `architect-propose` invocation must copy the approved bundle into one new independent plan package. It may record multiple approved `D-xxx` subdesigns and later derive multiple `T-xxx` tasks from them, but it may not change, add, or infer a subdesign.

## Handoff Gate

Do not hand off to `architect-propose` when any `D-xxx` subdesign lacks a concept, repository evidence, compatibility boundary, functional boundary, code impact scope, pattern decision, external evidence decision, rationale, verification seam, counterexample, anti-pattern, MUST rule, teaching explanation, or approval coverage. A later build run may make a cautious local minimal design decision only inside this approved functional boundary; it must record that decision rather than reopen an earlier stage. If the functional boundary cannot be preserved, build must stop and obtain a user decision without returning to `architect-design` or `architect-propose`.
