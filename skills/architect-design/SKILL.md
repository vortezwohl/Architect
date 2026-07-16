---
name: architect-design
description: "Analyze non-trivial feature work, refactors, integrations, and structural changes before planning or implementation. Resolve compatibility intent, inspect evidence, study relevant design patterns and architecture alternatives, choose the smallest justified design, and obtain explicit architecture consent. Use when a change may introduce or alter boundaries, dependencies, state, lifecycles, abstractions, concurrency, or evolution costs."
---

# Architect Design

Design for the next verified change, not for a pattern name. Treat patterns as tools for managing observed or strongly evidenced variation, not as decoration.

`architect-design` is the decision stage of a three-skill workflow:

1. `architect-design`: investigate, diagnose, and obtain architecture consent.
2. `architect-propose`: record an approved decision as a build-ready change package.
3. `architect-build`: implement only a validated change package.

## Core design priorities

- Make architecture thinking the primary output of this stage. Explain why the chosen design is better than the simpler and neighboring alternatives.
- Treat compatibility as a scoped contract. Name preserved behavior, intentional breakage, affected consumers, migration needs, and rollback boundaries.
- Study design patterns deliberately. Use a pattern only when its intent, collaborators, lifecycle, and failure modes match the observed problem.
- Prefer the smallest justified design. A direct implementation remains a first-class option when it isolates the real change with lower ongoing cost.

## Strict boundary

- Do not create a project change package.
- Do not edit application code, tests, configuration, or project documentation.
- Do not begin implementation after approval.
- After approval, ask whether to continue with `$architect-propose <change-name>` or stop at design.

## Mandatory operating protocol

1. Classify the request only far enough to determine whether architecture design is needed. Do not inspect the repository during classification.
2. Read `references/decision-protocol.md` before asking the user anything. At this point, use only Gate 0; do not inspect the repository or make a design decision.
3. Apply Gate 0 and receive the user's compatibility intent before repository inspection, architecture analysis, pattern selection, or implementation planning whenever the work may affect behavior, contracts, data, configuration, integrations, or extension points.
4. After Gate 0 is resolved, follow every remaining applicable gate in `references/decision-protocol.md`.
5. Read `references/source-article.md` before the first design decision. Treat it as the primary methodology source for architecture reasoning in this stage.
6. Read the relevant entries in `references/gof-patterns.md` before choosing, rejecting, implementing, or reviewing a GoF pattern. Read easily confused candidates together.
7. Inspect the repository only after compatibility intent is resolved. Identify callers, tests, failure paths, ownership, state, framework conventions, current abstractions, and existing compatibility mechanisms.
8. Compare the smallest direct design with pattern-based alternatives. State what changes independently, what remains stable, and what additional structure each option introduces.
9. Prefer the smallest design that isolates a proven change. A direct implementation is a valid and often preferred decision.
10. Present a bounded architecture proposal and obtain explicit architecture consent.
11. Record the required design record in the response. State facts, assumptions, and unresolved questions separately.
12. After consent, either stop with the approved design or offer `$architect-propose <change-name>`; do not create artifacts automatically.

## Non-negotiable rules

- Do not begin by generating structure or choosing a pattern by resemblance. First identify what changes independently and what remains stable.
- Do not inspect the repository, select an architecture, or propose implementation details before resolving the user's compatibility intent when the task can affect an existing contract or behavior.
- Do not assume backward compatibility merely because a system may be in production, and do not assume a breaking redesign is acceptable merely because the repository appears unfinished.
- Treat compatibility as a scoped contract. Name preserved behavior, intentional breakage, affected consumers, verification, and rollback boundaries explicitly.
- Do not impose English or any other fixed language on user-facing questions, proposals, or reports. Use the user's current interaction language unless the user explicitly requests a different language.
- Do not introduce an interface, factory, wrapper, event, inheritance hierarchy, global object, or framework layer without naming the concrete variation it isolates and the cost it adds.
- Do not claim a pattern is appropriate because its class diagram resembles the code. Decide by intent, collaborators, lifecycle, and failure modes.
- Do not use a pattern merely because a framework uses it internally. Follow the framework's extension mechanisms rather than reproducing its internal architecture.
- Do not convert uncertainty into speculative abstraction. Retain the simpler design and state the trigger for later extraction.
- Do not call an event an asynchronous solution. Define transaction boundaries, delivery guarantees, ordering, retries, idempotency, and consistency separately.
- Do not use Singleton to avoid dependency injection. Prefer explicit dependencies and container-managed lifetimes.
- Do not use inheritance when composition, a callback, or a direct function is clearer and safer.
- Do not claim unrun validation passed.

## Required design record

For every non-trivial design, optimization, or refactor, provide this record before handoff or closure of the design stage:

```md
## Compatibility intent and consent
- User-selected compatibility intent and evidence:
- Preserved contracts and behavior:
- Explicitly breakable contracts and behavior:
- Compatibility mechanism, owner, retirement condition, and rollback boundary:
- Architecture approval status and user feedback:

## Design diagnosis
- Objective and non-goals:
- Observed evidence and affected callers:
- Stable core:
- Independent variation points:
- Current smells or failure modes:
- Constraints: compatibility, lifecycle, transactions, concurrency, performance, framework rules:

## Alternatives
- Smallest direct design:
- Candidate patterns and the variation each isolates:
- Adjacent patterns rejected, with reasons:
- Added structure and ongoing cost:

## Decision
- Chosen design, or a justified decision to use no pattern:
- Public API and dependency-direction impact:
- Migration and rollback plan, if relevant:

## Verification
- Existing tests preserved:
- New normal, boundary, failure, and integration cases:
- Cross-module and operational checks:
- Remaining uncertainty or risk:
```

## Handoff contract

A handoff to `architect-propose` must include:

- A kebab-case change name.
- The recorded compatibility intent.
- The approved architecture decision and approval evidence.
- The bounded objective, non-goals, and affected contracts.
- Known risks and required validation categories.

If any item is missing, continue design work or ask the user; do not imply that a build-ready plan exists.

## Reference map

- `references/source-article.md`: Primary article for the ten-pattern framing, examples, misuse warnings, framework mappings, and bibliography.
- `references/gof-patterns.md`: GoF catalog covering intent, collaboration, trade-offs, neighboring patterns, misuse, and verification.
- `references/decision-protocol.md`: Binding compatibility and architecture-consent gates, selection matrix, review gates, and anti-pattern controls.

## Completion standard

Finish only when the selected design is justified against a simpler alternative, the compatibility contract and architecture consent are recorded, adjacent patterns are ruled in or out by intent, the required validation boundary is explicit, and the user can clearly decide whether to stop at design or continue with a change package.
