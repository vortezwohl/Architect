---
name: architect-design
description: "Manual-only skill. Use only when the user explicitly invokes the architect-design skill to produce one approved design bundle for one new independent future plan package. A single architect-design run may produce multiple D-xxx subdesigns. Do not auto-trigger from a generic feature, refactor, integration, or implementation request."
---

# Architect Design

Use this skill only as a manually selected architecture decision stage. Its job
is to make the agent learn first, then produce one approved design decision
bundle. It does not plan tasks, modify files, or invoke sibling skills
automatically. It is stage 1 of the one-way flow `architect-design ->
architect-propose -> architect-build`.

## Defined Terms

- `architect-design`: the manual stage that studies the codebase, learns the
  relevant architecture knowledge, asks for the compatibility boundary, and
  produces one approved design bundle.
- `design bundle`: the complete approved output of one `architect-design`
  invocation. One bundle may contain multiple `D-xxx` subdesigns.
- `D-xxx subdesign`: one independently explainable architectural decision
  inside the approved design bundle. One `D-xxx` subdesign is not the same
  thing as the whole `architect-design` stage.
- `independent plan`: one new future `.architect/<plan-name>/` package created
  by one later `architect-propose` invocation from one approved design bundle.

## Manual Invocation Only

- Run this skill only when the user explicitly asks for `architect-design`.
- Do not auto-switch into `architect-propose` or `architect-build`.
- If the user wants to continue after approval, the only forward next stage is
  `architect-propose`, invoked manually by the user.

## Core Outcome

Produce an approved, bounded design bundle that later stages can consume
without guessing:

- establish the minimum required understanding of the current system and
  codebase before abstract design begins;
- learn the required architecture method, source concepts, and supporting best
  practices before deciding;
- clarify the compatibility target with the user before design is locked;
- inspect only the repository evidence needed for the current decision;
- compare the direct design with the best adjacent alternatives;
- choose the best supported design, whether that best design preserves backward
  compatibility or intentionally replaces it;
- define one or more explicit `D-xxx` subdesigns with boundaries, counterexamples,
  anti-patterns, and design rules;
- obtain explicit user approval for the displayed design bundle.

## Strict Boundary

- Design is read-only. Inspect files, ask questions, and reason, but do not
  write, patch, generate, or overwrite repository content.
- Do not create a plan package or implementation task.
- Do not convert an unapproved assumption into a design unit.
- Do not let silence count as approval.
- Do not continue while compatibility intent, design detail, or approval
  coverage remains unresolved.
- Do not default to the smallest design unless evidence shows it is also the
  best design.
- Do not use a pattern because its shape looks familiar.

## Working Sequence

1. Classify the request only far enough to decide whether architecture design
   is needed.
2. Build the minimum required system understanding before deep design work. Do
   not proceed until you can name the relevant entry points, callers, state
   flow, dependencies, tests, ownership boundaries, and operational
   constraints.
3. Read `references/decision-protocol.md` and apply Gate 0 after that basic
   system understanding is established and before design is locked.
4. Read `references/source-article.md` before the first design decision.
5. Continue learning beyond the local references. Before proposing a design,
   gather enough external knowledge to cite concrete supporting evidence from
   primary English-language internet sources first. Use other reliable language
   sources only as a fallback. Prioritize academic material, industry
   references, framework documentation, and broadly accepted best practices
   over generic opinion.
6. Learn the relevant entries in `references/gof-patterns.md` before choosing,
   rejecting, or comparing a GoF pattern. Read neighboring candidates together
   whenever two or more candidate patterns could reasonably fit the same
   problem.
7. Deepen repository understanding only where the design decision needs more
   evidence: lifecycle, failures, transactions, concurrency, framework
   constraints, and operational risk.
8. Ask the user whether backward compatibility is required and what exactly
   must remain compatible: external contracts, stored data, state transitions,
   configuration, extension points, operational behavior, or migration paths.
   Do this before recommending the design.
9. Define the compatibility boundary, evolution horizon, real variation,
   stable core, collaborators, lifecycle, and likely failure mode from
   evidence, not imagination.
10. Compare the direct design with architectural alternatives using
   maintainability, comprehensibility, ownership, dependency direction,
   verifiability, compatibility, operational risk, and complexity.
11. Recommend the globally best design under the current code reality, the
    user-confirmed compatibility boundary, and the strongest supporting
    external evidence. It may be the smallest design if that is truly optimal,
    but do not treat "smallest" as a default victory condition.
12. Split the approved solution into one or more independently understandable
    `D-xxx` subdesigns. One `D-xxx` subdesign owns one architectural decision.
    The full approved design bundle may therefore contain multiple `D-xxx`
    subdesigns.
13. For every `D-xxx` subdesign, record the supporting engineering concept or
    pattern, reliable references, counterexamples, anti-patterns, design
    boundaries, and design-level `MUST DO` / `MUST NOT DO` rules.
14. Present the complete design bundle and obtain explicit user approval for
    the displayed `D-xxx` identifiers.

## Teaching Standard

Before asking for approval, explain for every non-trivial decision:

- what concrete problem the chosen concept solves here;
- what remains stable and what changes independently;
- what outside knowledge, best practice, or accepted reference most strongly
  supports the decision;
- whether backward compatibility was required, and if so, what exact surface
  was preserved;
- which simpler direct design was considered and why it was accepted or
  rejected;
- which adjacent pattern or abstraction was rejected and why;
- which misuse, counterexample, or operational failure would make the concept a
  poor fit;
- which validation boundary Build must later preserve.

Do not cite the references mechanically. Convert them into reasoning that the
later stages can reapply.

## Subdesign Contract

Every `D-xxx` subdesign must contain the following fixed English fields. Explanatory
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

Rules must constrain implementation details, not merely desired outcomes.

## Completion Standard

Finish only when the user can inspect the approved design bundle, understand
what the agent learned, what minimum system understanding the design depends
on, which compatibility boundary was chosen, why the recommended design is the
globally best supported option rather than merely the smallest one, and see
which one or more `D-xxx` subdesigns will later be recorded into one new
independent plan by `architect-propose`.
