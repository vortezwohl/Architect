<div align="center">

# Agent Architect

**The architecture guardrail for coding agents.**

*Your agent is already making architecture decisions.<br />
Do not let it make them silently.*

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-agent--architect-111827?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars)](https://github.com/vortezwohl/Agent-Architect/stargazers)

<br />

> <strong>No architecture by accident.</strong><br />
> <strong>No abstraction by speculation.</strong>

[Install](#install) &middot; [The Problem](#the-problem) &middot; [See The Difference](#see-the-difference) &middot; [Protocol](#the-decision-protocol)

</div>

---

## The problem

Most users do not ask an agent to make an architecture decision.

They ask it to do ordinary work:

```text
Add an invoice-download endpoint.
Build a settings page.
Connect this service to a new provider.
Refactor this module.
Make this feature extensible.
```

Before the agent writes its first line, it has already started deciding:

- Which module owns the behavior and state.
- Which dependencies cross a boundary.
- Which failure paths become public behavior.
- Whether a direct implementation, an abstraction, or a framework extension is justified.
- How the change will evolve, migrate, roll back, and be verified.

Those are architecture decisions.

Without an explicit protocol, agents usually fail in one of three ways:

<table>
<tr>
<th align="left">Failure</th>
<th align="left">What happens</th>
</tr>
<tr>
<td><strong>Architecture by accident</strong></td>
<td>The agent writes the feature directly into the nearest file. Dependencies, state, and error paths spread before anyone has named the boundary.</td>
</tr>
<tr>
<td><strong>Abstraction by speculation</strong></td>
<td>The agent sees a possible future and creates interfaces, factories, registries, events, or inheritance before a real variation exists.</td>
</tr>
<tr>
<td><strong>Verification by assertion</strong></td>
<td>The agent calls the refactor clean or complete without proving behavior, compatibility, failure handling, or remaining risk.</td>
</tr>
</table>

**Agent Architect** is the guardrail between a non-trivial coding request and structural complexity.

It makes the agent inspect reality, choose the smallest justified design, and report the evidence before complexity spreads.

---

## See the difference

### Before Agent Architect

```text
User: "Add an invoice-download endpoint."

Agent: writes a handler, reaches into persistence, calls storage,
adds authorization inline, creates an ExportFactory "for future formats,"
and reports that the endpoint is complete.
```

### With Agent Architect

```text
User: "Add an invoice-download endpoint."

Agent:
1. Inspects existing invoice ownership, authorization, storage, callers,
   error handling, and tests.
2. Names the actual change: one new HTTP entry point for one existing
   invoice artifact.
3. Compares the direct application-service call with a new export layer.
4. Keeps the direct design when there is one format and one storage path.
5. Records the extraction trigger: multiple independently changing export
   formats or storage providers behind the same application operation.
6. Verifies authorization, missing invoices, storage failure, and the
   existing invoice flow.
```

The result is not less engineering.

It is **engineering with an explicit decision, a smaller blast radius, and a verification path**.

---

## The decision protocol

```text
Receive a non-trivial coding request
      |
      v
Inspect the repository and current behavior
      |
      v
Name the proven change, stable core, constraints, and failure paths
      |
      +-- No independent variation is evidenced?
      |     `-- Keep the direct design. Record the extraction trigger.
      |
      v
Compare the smallest direct solution with candidate structures
      |
      v
Reject unnecessary interfaces, factories, wrappers, events, and inheritance
      |
      v
Check ownership, lifecycle, API direction, transactions, concurrency,
rollback, observability, and framework conventions
      |
      v
Implement one smallest verified slice
      |
      v
Report evidence, decision, validation performed, and remaining risk
```

### Non-negotiable rules

- Do not generate structure before naming what changes independently and what remains stable.
- Do not introduce an interface, factory, wrapper, event, inheritance hierarchy, global object, or framework layer without naming the concrete variation it isolates and the cost it adds.
- Do not turn uncertainty into speculative abstraction.
- Do not call an event an async design without delivery semantics.
- Do not use Singleton to avoid dependency injection.
- Do not use inheritance when composition, callbacks, or direct functions are clearer.
- Do not call an unverified implementation or refactor complete.

---

## What the agent produces

For every non-trivial feature, integration, design, or refactor, Agent Architect produces an auditable record:

```text
01. Design diagnosis
    Objective, non-goals, repository evidence, callers, stable core,
    variation points, smells, and constraints.

02. Alternatives
    The smallest direct design, candidate structures,
    rejected alternatives, and ongoing structural cost.

03. Decision
    Chosen design, public API and dependency impact,
    migration and rollback implications, or a justified decision to use no pattern.

04. Verification
    Normal, boundary, failure, integration, and operational checks;
    validation actually run; and remaining uncertainty or risk.
```

---

## When to use it

Use Agent Architect **before implementing or reviewing any non-trivial change**, including:

- New features that cross modules, layers, or services.
- Refactors that alter dependencies, ownership, state, or lifecycle.
- Third-party integrations and legacy adaptation.
- Async, event, transaction, retry, cache, or authorization work.
- Requests to make a system "clean," "extensible," "scalable," or "future-proof."
- PR reviews where code looks reasonable but its structural decision is implicit.

> [!TIP]
> Do not wait for a user to ask an architecture question. Add this skill to the agent workflow that handles feature work and structural changes.

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
Inspect the repository, choose the smallest justified design,
then implement and verify it.
```

Examples:

```text
Use $agent-architect before adding this payment provider.

Use $agent-architect to review this feature for accidental architecture
and speculative abstractions.

Use $agent-architect before refactoring this service boundary.
Preserve behavior and report the migration and rollback implications.

Use $agent-architect to determine whether this integration needs an adapter,
a direct dependency, or a framework extension.
```

---

## Patterns are tools, not the product

Agent Architect covers all 23 GoF patterns, but it does not begin with a pattern catalog.

It begins with evidence: **what varies, who owns it, what fails, and what must remain stable.**

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

Patterns are selected by **intent, collaborators, lifecycle, variation, and failure behavior** - never by a class diagram alone.

</details>

---

## What this skill is not

| Not this | But this |
| --- | --- |
| A pattern encyclopedia | An architecture decision protocol for coding agents |
| A ceremony generator | A guardrail against accidental complexity |
| "Clean architecture" by default | Explicit analysis of boundaries, dependencies, and lifecycle |
| A reason to add layers | Permission to keep the direct design when evidence is absent |
| A substitute for engineering ownership | A way to make agent-produced structure auditable and verifiable |

---

## Repository structure

```text
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

- `SKILL.md` - operating rules and the required design record
- `decision-protocol.md` - binding diagnostic, selection, refactoring, and review gates
- `gof-patterns.md` - pattern intent, trade-offs, misuse cases, and verification guidance
- `source-article.md` - architecture principles for the AI coding era

---

## The standard

A feature is not complete because it compiles.

A refactor is not complete because the code looks cleaner.

An architecture decision is complete only when it can answer:

```text
What evidence justified this structure?
Why is the direct alternative insufficient?
What changes independently?
What did we reject, and why?
How was behavior verified?
What risk remains?
```

> **Design for the next verified change - not for a pattern name.**

---

## Contributing

Contributions should improve **judgment**, not add ceremony.

Useful contributions include:

- Evidence gates for real feature and architecture decisions.
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

### Do not let your coding agent silently design your system.

<strong>Star it. Fork it. Add it before your next non-trivial change.</strong>

</div>
