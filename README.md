<div align="center">

<h1>
  <img src="assets/agent-architect-wordmark.svg" alt="Agent Architect" width="560" />
</h1>

**Fast code is easy. A codebase that survives its next hundred changes is harder.**

*Build codebases that stay coherent as they grow -- without giant modules, speculative abstractions, or accidental breaking changes.*

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-agent--architect-111827?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars)](https://github.com/vortezwohl/Agent-Architect/stargazers)

<br />

**No architecture by accident.** &nbsp; **No abstraction by speculation.** &nbsp; **No compatibility by assumption.**

[Install](#install) &middot; [See the difference](#before-and-after) &middot; [How it works](#how-it-builds-better-architecture) &middot; [Use cases](#when-to-use-it)

</div>

<h4 align="center">
  <p>
    <b>English</b> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_zh-hant.md">&#32321;&#39636;&#20013;&#25991;</a> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_zh-hans.md">&#31616;&#20307;&#20013;&#25991;</a> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_ja-jp.md">&#26085;&#26412;&#35486;</a>
  </p>
</h4>

---

## Your agent can write code. Can it design a system?

Most people do not ask a coding agent to make an architecture decision.

They ask it to ship ordinary work:

```text
Add an invoice-download endpoint.
Connect a second payment provider.
Refactor this service.
Make this feature extensible.
```

But before the first line is written, the agent has already made architectural choices:

- Which module owns the behavior and state.
- Which dependencies cross a boundary.
- Which errors become public behavior.
- What should remain compatible and what may intentionally change.
- Whether a direct implementation, an abstraction, or a framework extension is justified.

Without architectural judgment, an agent tends to fail in one of two expensive directions.

| Failure | What your codebase becomes |
| --- | --- |
| **Architecture by neglect** | Features land in the nearest file. Ownership blurs, rules duplicate, branches multiply, and a few services or packages grow until nobody wants to change them. |
| **Architecture by speculation** | A possible future becomes an interface, factory, registry, event, wrapper, or inheritance hierarchy before a real variation exists. |

There is a third failure that hides inside both:

> **Compatibility by assumption.** The agent either preserves obsolete behavior by default or rewrites working behavior without first making the boundary explicit.

The result may compile. It may even demo well.

It will still become harder to understand, test, extend, and trust with every next change.

**Agent Architect gives coding agents a disciplined way to reason about structure before complexity spreads.**

---

## Before and after

### Without Agent Architect

```text
User: "Add a second payment provider."

Agent: adds provider-specific conditionals to CheckoutService,
duplicates webhook handling, reaches into persistence from a handler,
creates a PaymentProviderFactory "for future providers,"
and quietly changes retry behavior used by an existing integration.
```

### With Agent Architect

```text
User: "Add a second payment provider."

Agent:
1. Maps the existing payment lifecycle, callers, retry ownership,
   webhooks, persistence, error paths, and tests.
2. Makes compatibility intent explicit instead of assuming that the old
   contract must be preserved -- or may be broken.
3. Separates proven variation (provider execution) from stable policy
   (checkout, authorization, retry ownership).
4. Compares the smallest direct design with a provider seam.
5. Introduces only the structure that isolates the evidenced variation.
6. Verifies success, decline, timeout, webhook, retry, migration, and
   rollback paths within the agreed compatibility boundary.
```

The result is not more ceremony.

It is **a smaller blast radius, a more durable design, and an explanation you can inspect before the codebase pays for the decision.**

---

## What Agent Architect changes

Agent Architect does **not** turn architecture into a committee exercise for users.

It turns a fast code generator into a more responsible software designer -- and makes its reasoning visible when a decision affects behavior, structure, or compatibility.

| Instead of | Agent Architect helps the agent |
| --- | --- |
| Coding in the nearest file | Find the real owner, boundary, callers, dependencies, and failure paths. |
| Abstracting for every possible future | Keep a direct design until independent variation is named and evidenced. |
| Assuming backward compatibility or a clean rewrite | Make the intended compatibility boundary explicit before design. |
| Calling a refactor "clean" | State the alternatives, structural cost, validation performed, and remaining risk. |

> Compatibility intent is not bureaucracy. It prevents two equally expensive mistakes: preserving legacy behavior nobody needs, and breaking behavior somebody depends on.

---

## How it builds better architecture

### 1. Read reality before designing

The agent inspects repository evidence before proposing structure: affected callers, ownership, dependencies, state, failure paths, lifecycle, transactions, concurrency, framework rules, and current tests.

### 2. Make compatibility intentional

When a change may affect contracts, data, configuration, integrations, or extension points, the agent asks what must remain compatible and what may intentionally change. It then records the actual boundary, migration or rollback implications, and unresolved risks.

It does not silently choose "always preserve everything" or "rewrite it cleanly."

### 3. Choose the smallest durable structure

The direct solution is always a real alternative. An interface, adapter, strategy, event, factory, wrapper, or framework extension must earn its cost by isolating a concrete independent variation.

### 4. Explain and verify the decision

The agent produces an auditable architecture record and verifies behavior at the affected boundary. It reports what it ran, what remains uncertain, and why rejected alternatives were not worth their cost.

---

## What the agent delivers

For each non-trivial feature, integration, design, refactor, or review, Agent Architect produces an architecture record:

```text
01. Design diagnosis
    Objective, non-goals, repository evidence, callers, stable core,
    variation points, failure modes, and constraints.

02. Compatibility intent
    Preserved and intentionally changed contracts, consumers,
    migration or rollback boundaries, and unresolved risk.

03. Alternatives and decision
    The smallest direct design, justified structure, rejected options,
    API impact, dependency direction, and ongoing cost.

04. Verification
    Normal, boundary, failure, integration, concurrency, and operational
    checks; validation actually run; and remaining uncertainty.
```

This is how an architectural decision becomes explainable -- not just a pile of generated files that happens to work today.

---

## Install

### Codex

```text
$skill-installer install https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect
```

Restart Codex after installation.

### Other Agent Skills-compatible tools

Copy `skills/agent-architect/` into the tool's supported skills location, then invoke:

```text
agent-architect
```

> [!IMPORTANT]
> Read a skill before installing it. A skill is executable agent guidance: inspect its instructions, bundled references, scripts, and trust boundary.

---

## Use it

Ask your coding agent:

```text
Use $agent-architect before implementing or reviewing this non-trivial change.
Inspect the repository, make compatibility intent explicit where it matters,
choose the smallest durable architecture, then implement and verify it.
```

Examples:

```text
Use $agent-architect before adding this payment provider.

Use $agent-architect to review this feature for accidental architecture,
speculative abstractions, and an unclear compatibility boundary.

Use $agent-architect before refactoring this service boundary.
Preserve or intentionally change behavior only after the contract is explicit.

Use $agent-architect to decide whether this integration needs an adapter,
a direct dependency, or a framework extension.
```

---

## When to use it

Use Agent Architect when the change can reshape the codebase:

- A feature crosses modules, layers, services, databases, or third-party providers.
- You are about to "refactor," "extend," "abstract," "decouple," "generalize," or make something "future-proof."
- An agent proposes an interface, factory, event, registry, wrapper, inheritance hierarchy, or global state.
- You do not know whether existing behavior must remain compatible.
- You see giant services, giant packages, duplicated rules, cross-layer dependencies, or branch logic that nobody can confidently explain.
- A PR appears to work, but the structural decision is still implicit.

> [!TIP]
> Add Agent Architect to the workflow that handles feature work and structural changes. Do not wait until accidental complexity has already spread.

---

## Patterns are a last step, not a starting point

Agent Architect covers all 23 Gang of Four patterns.

Its more important skill is knowing when **not** to use one.

It begins with evidence: **what varies, who owns it, what fails, what must remain stable, and what the direct alternative already solves.**

<details>
<summary><b>Creational decisions</b></summary>

- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton scope

</details>

<details>
<summary><b>Structural decisions</b></summary>

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

</details>

<details>
<summary><b>Behavioral decisions</b></summary>

- Chain of Responsibility
- Command
- Interpreter
- Iterator
- Mediator
- Memento
- Observer
- State
- Strategy
- Template Method
- Visitor

</details>

<details>
<summary><b>Critical pattern boundaries</b></summary>

| Do not confuse | With |
| --- | --- |
| Decorator | Proxy or Adapter |
| Facade | Mediator |
| Factory Method | Abstract Factory, Builder, or Prototype |
| Strategy | State or Template Method |
| Observer | Chain of Responsibility or Command |
| Composite | Decorator |

Patterns are selected by **intent, collaborators, lifecycle, variation, and failure behavior** -- never by a class diagram alone.

</details>

---

## What this skill is not

| Not this | But this |
| --- | --- |
| A pattern encyclopedia | An architectural-judgment system for coding agents |
| A ceremony generator | A way to make the right amount of structure explicit and verifiable |
| "Clean architecture" by default | Evidence-based analysis of boundaries, ownership, dependencies, and lifecycle |
| A reason to add layers | Permission to keep the direct design when evidence is absent |
| A user approval bottleneck | A way to keep the human informed when compatibility or architecture becomes consequential |
| A substitute for engineering ownership | A way to make agent-produced structure more responsible, auditable, and maintainable |

---

## Repository structure

```text
assets/
`-- agent-architect-wordmark.svg

skills/
`-- agent-architect/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    `-- references/
        |-- decision-protocol.md
        |-- gof-patterns.md
        `-- source-article.md
```

- `SKILL.md` -- operating rules and the required architecture record
- `decision-protocol.md` -- compatibility intent, architecture consent, diagnostic, selection, refactoring, and review gates
- `gof-patterns.md` -- pattern intent, trade-offs, misuse cases, and verification guidance
- `source-article.md` -- architecture principles for the AI coding era

---

## Contributing

Contributions should improve **architectural judgment**, not add ceremony.

Useful contributions include:

- Evidence gates for real feature and architecture decisions.
- Clearer compatibility boundaries, migration guidance, and rollback criteria.
- Clearer pattern boundaries and rejection criteria.
- Reproducible examples of accidental architecture and speculative abstraction.
- Verification guidance for lifecycle, concurrency, transactions, migration, and rollback.
- Corrections that make agents less likely to spread structural complexity.

Before opening a change, ask:

```text
Does this improve a decision an agent can make before code spreads?
Can the improvement be verified?
Does it add guidance without adding speculative process?
```

---

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">

### Give your coding agent architectural judgment.

<strong>Build code that stays coherent through change.</strong>

</div>
