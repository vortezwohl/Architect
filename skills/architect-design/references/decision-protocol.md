# Binding Design Decision Protocol

## Language Rule

Maintain this protocol and all skill instructions in English. Use the user's
current language for user-facing proposals and the semantic body of plan
documents unless the user explicitly requests another language. Plan field
names, identifiers, timestamps, and status values remain fixed English tokens.

## Gate 0: Compatibility Intent

Before repository inspection or design work that can affect behavior, contracts,
data, configuration, integrations, or extension points, ask the user to choose:

1. Preserve the affected existing contracts.
2. Allow intentional breaking changes for a better long-term design.
3. Describe a custom compatibility boundary.

Do not infer an answer from repository age, deployment status, silence, or task
wording. Restate the answer as preserved behavior, intentionally breakable
behavior, consumers, migration obligations, and rollback limits.

## Evidence and Design Units

After Gate 0, inspect only evidence relevant to the change: callers, existing
tests, ownership, dependencies, state, lifecycle, error paths, transactions,
concurrency, framework rules, and operational constraints.

Choose the best justified architecture for the stated evolution horizon. Compare
the direct alternative, but do not grant it automatic priority merely because it
is smaller. Every chosen decision must be one `D-xxx` design unit with:

- A recognized engineering concept or pattern, canonical name, category, and
  reliable reference.
- The stable core, actual variation, collaborators, ownership, dependency
  direction, lifecycle, and failure semantics.
- Concrete alternatives and rejected neighboring concepts.
- Explicit design boundaries, counterexamples, and anti-patterns.
- Design-level `MUST DO` and `MUST NOT DO` rules that constrain implementation
  details rather than merely desired results.

Do not introduce an unnamed abstraction, speculative extension point, hidden
global dependency, event without delivery semantics, or inheritance hierarchy
without evidence that it improves the stated decision criteria.

## Gate 1: Design Approval

Present the full design bundle and ask the user to approve or request changes.
Approval must identify the covered `D-xxx` units directly or unambiguously refer
to the displayed bundle. Silence is not approval. If feedback changes one
decision, revisit the affected design unit and obtain approval again.

Record approval evidence and a digest of the approved bundle. Architect Propose
may copy approved design content into a plan but may not change, add, or infer a
design unit.

## Handoff Gate

Do not hand off to Propose when any `D-xxx` unit lacks a concept, rationale,
counterexample, anti-pattern, design boundary, MUST rule, or approval coverage.
If Plan or Build discovers a new design decision, it must return here rather
than improvise.
