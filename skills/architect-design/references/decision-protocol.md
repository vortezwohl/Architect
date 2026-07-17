# Binding Design Decision Protocol

## Language Rule

Maintain this protocol and all skill instructions in English. Use the user's current language for user-facing proposals and the semantic body of plan documents unless the user explicitly requests another language. Plan field names, identifiers, timestamps, and status values remain fixed English tokens.

## How to Use This Protocol

1. Read this file first for the gates, approval boundaries, and non-negotiable output requirements.
2. Treat Architect Design as a read-only stage. Inspect repository files and think through the design, but do not edit, create, or overwrite files at this stage.
3. Read `source-article.md` before the first design decision for methodology, pattern framing, and AI-era misuse warnings.
4. Read `gof-patterns.md` for candidate patterns and neighboring comparisons before selecting, rejecting, or reviewing a GoF pattern.
5. Convert what those references teach into explicit reasoning. Do not cite them mechanically or treat a pattern name as sufficient evidence.

## Gate 0: Compatibility Intent

Before repository inspection or design work that can affect behavior, contracts, data, configuration, integrations, or extension points, ask the user to choose:

1. Preserve the affected existing contracts.
2. Allow intentional breaking changes for a better long-term design.
3. Describe a custom compatibility boundary.

Do not infer an answer from repository age, deployment status, silence, or task wording. Restate the answer as preserved behavior, intentionally breakable behavior, consumers, migration obligations, and rollback limits.

## Evidence and Design Units

After Gate 0, inspect only evidence relevant to the change: callers, existing tests, ownership, dependencies, state, lifecycle, error paths, transactions, concurrency, framework rules, and operational constraints.

Design remains read-only while collecting this evidence. You may read, inspect, compare, and reason about repository files, but you must not edit code, tests, configuration, documentation, plans, or generated artifacts in this stage.

Choose the best justified architecture for the stated evolution horizon. Compare the direct alternative, but do not grant it automatic priority merely because it is smaller. Every chosen decision must be one `D-xxx` design unit with:
- A recognized engineering concept or pattern, canonical name, category, and reliable reference.
- The stable core, actual variation, collaborators, ownership, dependency direction, lifecycle, and failure semantics.
- Concrete alternatives and rejected neighboring concepts.
- Explicit design boundaries, counterexamples, and anti-patterns.
- Design-level `MUST DO` and `MUST NOT DO` rules that constrain implementation details rather than merely desired results.

Do not introduce an unnamed abstraction, speculative extension point, hidden global dependency, event without delivery semantics, or inheritance hierarchy without evidence that it improves the stated decision criteria.

## Teaching Output Contract

Before asking for approval, teach the design instead of only presenting a conclusion. For every non-trivial `D-xxx` unit, explain at least:

- The concrete problem this concept solves in the current repository or request.
- The stable core and the real variation that justify the concept.
- The simplest direct design that was considered, and why it was accepted or rejected.
- The nearest neighboring pattern or abstraction that was rejected, and why.
- The likely misuse, counterexample, or operational failure that would make this concept a poor fit.
- The validation boundary that must hold if Build later implements the design.

When possible, map the teaching explanation directly onto the design-unit fields: `Intent`, `StableCoreAndVariation`, `Rationale`, `Alternatives`, `Counterexamples`, `AntiPatterns`, and `Rules`.

## Gate 1: Design Approval

Present the full design bundle and ask the user to approve or request changes. Approval must identify the covered `D-xxx` units directly or unambiguously refer to the displayed bundle. Silence is not approval. If feedback changes one decision, revisit the affected design unit and obtain approval again.

Record approval evidence and a digest of the approved bundle. Architect Propose may copy approved design content into a plan but may not change, add, or infer a design unit.

## Handoff Gate

Do not hand off to Propose when any `D-xxx` unit lacks a concept, rationale, counterexample, anti-pattern, design boundary, MUST rule, teaching explanation, or approval coverage. If Plan or Build discovers a new design decision, it must return here rather than improvise.
