---
name: architect-design
description: "Manual-only skill. Use only when the user explicitly invokes the architect-design skill to produce one approved design bundle for one new independent future plan package. A single architect-design run may produce multiple D-xxx subdesigns. Do not auto-trigger from a generic feature, refactor, integration, or implementation request."
---

# Architect Design

Use this skill only as a manually selected architecture decision stage. Its job
is to extract the minimum required repository context first, then learn the
required architecture knowledge, then produce one approved design decision
bundle. It does not plan tasks, modify files, or invoke sibling skills
automatically. It is stage 1 of the one-way flow `architect-design ->
architect-propose -> architect-build`.

## Defined Terms

- `architect-design`: the manual stage that studies the codebase, learns the
  relevant architecture knowledge, asks for the compatibility boundary, and
  produces one approved design bundle.
- `minimal context extraction`: the smallest repository-focused evidence pass
  required before any knowledge injection or design reasoning begins. It
  extracts only the facts needed to identify what the system is, where the
  requested change lands, what currently owns the behavior, which callers and
  tests matter, and which constraints already exist.
- `basic repository understanding`: the post-extraction state in which the
  agent can state the system purpose, relevant entry points, affected modules,
  current behavior owner, caller path, state flow, constraints, and current
  tests for the requested change. This is a required gate, not a vague
  impression.
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
  codebase before knowledge injection or abstract design begins;
- perform minimal context extraction before any architecture learning starts;
- learn the required architecture method, source concepts, and supporting best
  practices before deciding;
- clarify the compatibility target with the user before design is locked;
- inspect only the repository evidence needed for the current decision;
- compare the direct design with the best adjacent alternatives;
- choose the best supported design, whether that best design preserves backward
  compatibility or intentionally replaces it;
- define one or more explicit `D-xxx` subdesigns with boundaries, counterexamples,
  anti-patterns, and design rules;
- obtain approval for the displayed design bundle under the default
  non-rejection rule defined by this skill.

## Strict Boundary

- Design is read-only. Inspect files, ask questions, and reason, but do not
  write, patch, generate, or overwrite repository content.
- Do not create a plan package or implementation task.
- Do not convert an unapproved assumption into a design unit.
- No approval exists before the user's first turn after the latest displayed
  design bundle.
- Do not continue while compatibility intent, design detail, or approval
  coverage remains unresolved.
- Do not begin `source-article.md`, external architecture learning, or pattern
  comparison before minimal context extraction is complete.
- Do not treat a vague feeling of familiarity with the repository as basic
  repository understanding.
- Do not default to the smallest design unless evidence shows it is also the
  best design.
- Do not use a pattern because its shape looks familiar.

## Working Sequence

1. Classify the request only far enough to decide whether architecture design
   is needed.
2. Perform minimal context extraction before any knowledge injection. Extract
   only the repository facts needed to identify the system purpose, relevant
   entry points, affected modules, current behavior owner, caller path, state
   flow, existing tests, and operational constraints for the requested change.
3. Establish basic repository understanding from that extracted context. Do not
   proceed until you can explicitly state the system purpose, relevant entry
   points, affected modules, current behavior owner, caller path, state flow,
   constraints, and current tests for the requested change.
4. Read `references/decision-protocol.md` after basic repository understanding
   is established and use it as the binding rule set for the remaining Design
   stage.
5. Read `references/source-article.md` only after Steps 2 through 4 are
   complete and before the first design decision.
6. Continue learning beyond the local references. Before proposing a design,
   gather enough external knowledge to cite concrete supporting evidence from
   primary English-language internet sources first. Use other reliable language
   sources only as a fallback. Prioritize English-language academic papers
   first, best-practice articles from top-tier engineering organizations
   second, and other reliable supporting sources third. Do not treat framework
   documentation as a default theory source.
7. Learn the relevant entries in `references/gof-patterns.md` before choosing,
   rejecting, or comparing a GoF pattern. Read neighboring candidates together
   whenever two or more candidate patterns could reasonably fit the same
   problem.
8. Deepen repository understanding only where the design decision needs more
   evidence: lifecycle, failures, transactions, concurrency, framework
   constraints, and operational risk.
9. Ask the user whether backward compatibility is required and what exactly
   must remain compatible: external contracts, stored data, state transitions,
   configuration, extension points, operational behavior, or migration paths.
   Do this before recommending the design.
10. Define the compatibility boundary, evolution horizon, real variation,
   stable core, collaborators, lifecycle, and likely failure mode from
   evidence, not imagination.
11. Compare the direct design with architectural alternatives using
   maintainability, comprehensibility, ownership, dependency direction,
   verifiability, compatibility, operational risk, and complexity.
12. Recommend the globally best design under the current code reality, the
    user-confirmed compatibility boundary, and the strongest supporting
    external evidence. It may be the smallest design if that is truly optimal,
    but do not treat "smallest" as a default victory condition.
13. Split the approved solution into one or more independently understandable
    `D-xxx` subdesigns. One `D-xxx` subdesign owns one architectural decision.
    The full approved design bundle may therefore contain multiple `D-xxx`
    subdesigns.
14. For every `D-xxx` subdesign, record the supporting engineering concept or
    pattern, reliable references, counterexamples, anti-patterns, design
    boundaries, and design-level `MUST DO` / `MUST NOT DO` rules.
15. Present the complete design bundle. The user's first subsequent turn counts
    as approval of the latest displayed bundle unless that turn explicitly
    rejects the bundle or requests design changes. A direct user request to
    continue into `architect-propose` also counts as approval.

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

## Approval Rule

Apply this exact approval rule after the complete design bundle is displayed:

- The user's first subsequent turn counts as approval of the latest displayed
  bundle unless that turn explicitly rejects the bundle or requests design
  changes.
- A direct user request to continue into `architect-propose` counts as
  approval of the latest displayed bundle.
- An explicit rejection or requested design change reopens the affected
  `D-xxx` subdesigns and cancels the prior approval state for those affected
  parts.
- No approval exists before the user's first turn after the latest displayed
  design bundle.

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
what repository context was minimally extracted before learning began, what
basic repository understanding the design depends on, what the agent learned
after that gate, which compatibility boundary was chosen, why the recommended
design is the globally best supported option rather than merely the smallest
one, and see which one or more `D-xxx` subdesigns will later be recorded into
one new independent plan by `architect-propose`.
