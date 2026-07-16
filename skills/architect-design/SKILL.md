---
name: architect-design
description: "Investigate consequential changes, define explicit design units with recognized engineering concepts, record design-level constraints and anti-patterns, and obtain user approval before a plan is created. Use for features, refactors, integrations, and structural changes that affect boundaries, dependencies, state, lifecycle, compatibility, or future evolution."
---

# Architect Design

Design the most justified architecture for the stated compatibility boundary and
evolution horizon. Do not optimize for the fewest files or abstractions by
default. Complexity remains an explicit cost, but a direct implementation wins
only when it is also the clearest, most maintainable, and best-supported option.

`architect-design` is the decision stage of a strict three-stage workflow:

1. `architect-design` investigates and obtains approval for design units.
2. `architect-propose` records only approved design units as a plan package.
3. `architect-build` executes only the sealed package, one atomic task at a time.

## Strict Boundary

- Do not create a plan package or edit implementation files.
- Do not convert an unapproved assumption into a design unit.
- Do not let silence count as approval.
- Do not continue to Propose after unresolved design detail, missing approval, or
  an unnamed engineering concept.
- Do not use a pattern because its class diagram resembles the problem.

## Required Decision Protocol

1. Apply the compatibility-intent gate before repository inspection when a
   contract, state, configuration, integration, or extension point may change.
2. Inspect repository evidence only after the compatibility boundary is known:
   callers, tests, ownership, dependencies, lifecycle, state, failures,
   transactions, concurrency, framework constraints, and operational risk.
3. Define an explicit evolution horizon. It must name evidence-backed future
   changes or state that no such evidence exists; imagined extensibility is not
   evidence.
4. Compare the direct alternative with architectural alternatives using
   maintainability, comprehensibility, responsibility ownership, dependency
   direction, verifiability, operational risk, compatibility, and complexity.
5. Split the approved solution into independently understandable design units:
   `D-001`, `D-002`, and so on. A design unit owns one architectural decision.
6. For every design unit, name a recognized software engineering concept or
   pattern. Record its canonical name, category, and a reliable reference.
   A justified direct design must name its engineering concept as well.
7. Record concrete counterexamples, anti-patterns, design boundaries, and
   design-level `MUST DO` / `MUST NOT DO` rules for every design unit.
8. Present the complete design bundle and obtain unambiguous user approval for
   the covered `D-xxx` identifiers. A user instruction to proceed is valid only
   when it clearly refers to the displayed bundle; silence is never approval.
9. Produce a design bundle digest and hand off only the approved design text,
   approval evidence, objective, non-goals, compatibility boundary, risks, and
   required validation categories to `architect-propose`.

## Design Unit Contract

Every design unit must contain the following fixed English fields. Explanatory
content uses the user's current language unless the user explicitly requests a
different language.

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

Rules must constrain design details, not merely outcomes. Good rules define
ownership, dependency direction, lifecycle authority, state transitions,
contract mapping, error behavior, transaction boundaries, or framework usage.

## Approval and Handoff Gate

Do not hand off when any design unit is missing approval evidence, a canonical
concept, a counterexample, an anti-pattern, a boundary, or a design rule. A
later implementation detail that requires a new architectural judgment is a
return to Design, not an opportunity for Propose or Build to improvise.

## Completion Standard

Finish only when the user can inspect the approved design bundle, identify why
each concept was selected over its alternatives, see exactly what must and must
not be built, and decide whether to stop or invoke `$architect-propose`.
