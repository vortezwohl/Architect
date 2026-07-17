---
name: architect-design
description: "Investigate consequential changes, study the relevant architecture references, define explicit design units with recognized engineering concepts, record design-level constraints and anti-patterns, and obtain user approval before a plan is created. Use for features, refactors, integrations, and structural changes that affect boundaries, dependencies, state, lifecycle, compatibility, or future evolution."
---

# Architect Design

Teach the agent before constraining the agent. Use this skill as both a learning guide and a decision protocol: study the relevant references first, then produce bounded design units that later stages can execute safely.

Design the most justified architecture for the stated compatibility boundary and evolution horizon. Do not optimize for the fewest files or abstractions by default. Complexity remains an explicit cost, but a direct implementation wins only when it is also the clearest, most maintainable, and best-supported option.

`architect-design` is the decision stage of a strict three-stage workflow:

1. `architect-design` investigates, learns, and obtains approval for design units.
2. `architect-propose` records only approved design units as a plan package.
3. `architect-build` executes only the sealed package, one atomic task at a time.

## Core Responsibilities

- Learn the architecture method before proposing structure or naming a pattern.
- Learn the intent, collaborators, lifecycle, and failure modes of relevant concepts before turning them into design rules.
- Teach the user and the next agent why the chosen concept fits better than the direct and adjacent alternatives.
- Constrain later stages with approved design units, boundaries, anti-patterns, and design-level rules while remaining read-only in Design.

## Strict Boundary

- Design is a read-only stage. Inspect files, ask questions, and reason, but do not write, patch, generate, or overwrite repository content.
- Do not create a plan package or edit any file, including implementation, tests, configuration, documentation, skill artifacts, or generated files.
- Do not convert an unapproved assumption into a design unit.
- Do not let silence count as approval.
- Do not continue to Propose after unresolved design detail, missing approval, or an unnamed engineering concept.
- Do not use a pattern because its class diagram resembles the problem.
- Do not skip the reference-reading and teaching steps because a pattern name feels familiar.

## Learning-First Protocol

1. Classify the request only far enough to determine whether architecture design is needed. Do not inspect the repository during classification.
2. Read `references/decision-protocol.md` before asking the user anything. At this point, use only Gate 0; do not inspect the repository or make a design decision.
3. Apply the compatibility-intent gate before repository inspection when a contract, state, configuration, integration, or extension point may change.
4. Read `references/source-article.md` before the first design decision. Treat it as the primary teaching source for methodology, examples, misuse warnings, and pattern framing.
5. Read the relevant entries in `references/gof-patterns.md` before choosing, rejecting, comparing, or reviewing a GoF pattern. Read adjacent candidates together when confusion is plausible.
6. Carry forward what the references teach. Before locking a design unit, explain the stable core, the real variation, the lifecycle or collaboration model, the expected failure mode, and why the concept fits better than the direct or adjacent alternatives.
7. Inspect repository evidence only after the compatibility boundary is known: callers, tests, ownership, dependencies, lifecycle, state, failures, transactions, concurrency, framework constraints, and operational risk.
8. Define an explicit evolution horizon. It must name evidence-backed future changes or state that no such evidence exists; imagined extensibility is not evidence.
9. Compare the direct alternative with architectural alternatives using maintainability, comprehensibility, responsibility ownership, dependency direction, verifiability, operational risk, compatibility, and complexity.
10. Split the approved solution into independently understandable design units: `D-001`, `D-002`, and so on. A design unit owns one architectural decision.
11. For every design unit, name a recognized software engineering concept or pattern. Record its canonical name, category, and a reliable reference. A justified direct design must name its engineering concept as well.
12. Record concrete counterexamples, anti-patterns, design boundaries, and design-level `MUST DO` / `MUST NOT DO` rules for every design unit.
13. Present the complete design bundle and obtain unambiguous user approval for the covered `D-xxx` identifiers. A user instruction to proceed is valid only when it clearly refers to the displayed bundle; silence is never approval.
14. Produce a design bundle digest and hand off only the approved design text, approval evidence, objective, non-goals, compatibility boundary, risks, and required validation categories to `architect-propose`.

## Teaching Standard

Before approval, make the design response teach at least these points for each non-trivial decision:

- What problem the chosen concept solves in this specific context.
- What remains stable and what changes independently.
- Which simpler direct design was considered and why it was accepted or rejected.
- Which adjacent pattern, abstraction, or workflow was rejected and why.
- Which counterexample or misuse would signal that the concept is a poor fit.

Do not treat the references as citation cargo. Convert them into concrete reasoning that another agent can follow and reapply.

## Design Unit Contract

Every design unit must contain the following fixed English fields. Explanatory content uses the user's current language unless the user explicitly requests a different language.

```md
# Design: D-001-<slug>

## Concept
- CanonicalName:
- Category:
- Reference:

## Intent
## StableCoreAndVariation
## Rationale
## Alternatives
## DesignBoundaries
## Counterexamples
## AntiPatterns
## Rules
### MUST DO
### MUST NOT DO
```

Rules must constrain design details, not merely outcomes. Good rules define ownership, dependency direction, lifecycle authority, state transitions, contract mapping, error behavior, transaction boundaries, or framework usage.

## Approval and Handoff Gate

Do not hand off when any design unit is missing approval evidence, a canonical concept, a counterexample, an anti-pattern, a boundary, or a design rule. A later implementation detail that requires a new architectural judgment is a return to Design, not an opportunity for Propose or Build to improvise.

## Reference Map

- `references/decision-protocol.md`: Binding compatibility-intent and approval gates, diagnostic questions, selection matrix, and anti-pattern controls.
- `references/source-article.md`: Primary teaching article for methodology, examples, misuse warnings, framework mappings, and bibliography.
- `references/gof-patterns.md`: GoF catalog covering intent, collaboration, trade-offs, neighboring patterns, misuse, and verification.

## Completion Standard

Finish only when the user can inspect the approved design bundle, understand what the agent learned from the references, identify why each concept was selected over its alternatives, see exactly what must and must not be built, and decide whether to stop or invoke `$architect-propose`.
