# Binding Design Decision Protocol

## Language Rule

Maintain this protocol and all skill instructions in English. Use the user's current language for user-facing proposals and the semantic body of plan documents unless the user explicitly requests another language. Plan field names, identifiers, timestamps, and status values remain fixed English tokens.

## How to Use This Protocol

1. Read this file first for the gates, approval boundaries, and non-negotiable output requirements.
2. Treat Architect Design as a read-only stage. Inspect repository files and think through the design, but do not edit, create, or overwrite files at this stage.
3. Perform minimal context extraction before any knowledge injection. Extract only the repository facts needed to identify the system purpose, relevant entry points, affected modules, current behavior owner, caller path, state flow, current tests, and operational constraints for the requested change.
4. Establish basic repository understanding from that extracted context before design is recommended. This gate is satisfied only when you can explicitly state the system purpose, relevant entry points, affected modules, current behavior owner, caller path, state flow, constraints, and current tests for the requested change.
5. Read `source-article.md` only after Step 4 is satisfied and before the first design decision for methodology, pattern framing, and AI-era misuse warnings.
6. Read `gof-patterns.md` for candidate patterns and neighboring comparisons before selecting, rejecting, or reviewing a GoF pattern.
7. Convert what those references teach into explicit reasoning. Do not cite them mechanically or treat a pattern name as sufficient evidence.
8. When gathering external evidence beyond the local references, prioritize English-language academic papers first, best-practice articles from top-tier engineering organizations second, and other reliable supporting sources third. Do not treat framework documentation as a default theory source.

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
- `independent plan`: one new future `.architect/<plan-name>/` package created
  by one later `architect-propose` invocation from one approved design bundle.

## Gate 0: Compatibility Intent

After basic repository understanding is established and before any design recommendation that can affect behavior, contracts, data, configuration, integrations, or extension points, ask the user to choose:

1. Preserve the affected existing contracts.
2. Allow intentional breaking changes for a better long-term design.
3. Describe a custom compatibility boundary.

Do not infer an answer from repository age, deployment status, silence, or task wording. Restate the answer as preserved behavior, intentionally breakable behavior, consumers, migration obligations, and rollback limits. Do not recommend the design before this boundary is explicit.

## Evidence and Design Units

After Gate 0, inspect and deepen only the evidence relevant to the change: callers, existing tests, ownership, dependencies, state, lifecycle, error paths, transactions, concurrency, framework rules, and operational constraints.

Design remains read-only while collecting this evidence. You may read, inspect, compare, and reason about repository files, but you must not edit code, tests, configuration, documentation, plans, or generated artifacts in this stage.
Do not treat external architecture learning as a substitute for minimal context extraction or for basic repository understanding. The repository gate comes first.

Choose the globally best justified architecture for the stated evolution horizon under the current code reality, the user-approved compatibility boundary, and the strongest supporting external evidence. Compare the direct alternative, but do not grant it automatic priority merely because it is smaller. The approved design bundle may contain multiple `D-xxx` subdesigns. Every chosen `D-xxx` subdesign must include:
- A recognized engineering concept or pattern, canonical name, category, and reliable reference.
- The stable core, actual variation, collaborators, ownership, dependency direction, lifecycle, and failure semantics.
- Concrete alternatives and rejected neighboring concepts.
- Explicit design boundaries, counterexamples, and anti-patterns.
- Design-level `MUST DO` and `MUST NOT DO` rules that constrain implementation details rather than merely desired results.

Do not introduce an unnamed abstraction, speculative extension point, hidden global dependency, event without delivery semantics, or inheritance hierarchy without evidence that it improves the stated decision criteria.

## Teaching Output Contract

Before asking for approval, teach the design instead of only presenting a conclusion. For every non-trivial `D-xxx` subdesign, explain at least:

- The concrete problem this concept solves in the current repository or request.
- The stable core and the real variation that justify the concept.
- The simplest direct design that was considered, and why it was accepted or rejected.
- The nearest neighboring pattern or abstraction that was rejected, and why.
- The likely misuse, counterexample, or operational failure that would make this concept a poor fit.
- The validation boundary that must hold if Build later implements the design.

When possible, map the teaching explanation directly onto the design-unit fields: `Intent`, `StableCoreAndVariation`, `Rationale`, `Alternatives`, `Counterexamples`, `AntiPatterns`, and `Rules`.

## Gate 1: Design Approval

Present the full design bundle. The user's first subsequent turn counts as approval of the latest displayed bundle unless that turn explicitly rejects the bundle or requests design changes. A direct user request to continue into `architect-propose` also counts as approval of the latest displayed bundle. If feedback changes one decision, revisit the affected `D-xxx` subdesign and obtain approval again under the same rule.

Record approval evidence and a digest of the approved bundle. One later `architect-propose` invocation must copy the approved bundle into one new independent plan package. It may record multiple approved `D-xxx` subdesigns and later derive multiple `T-xxx` tasks from them, but it may not change, add, or infer a subdesign.

## Handoff Gate

Do not hand off to Propose when any `D-xxx` subdesign lacks a concept, rationale, counterexample, anti-pattern, design boundary, MUST rule, teaching explanation, or approval coverage. If a later independent cycle needs a new design decision, that new decision belongs to a new Architect Design stage and a new independent plan cycle, not to improvisation inside the current Propose or Build run.
