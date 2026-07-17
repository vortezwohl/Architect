<div align="center">

<h1>
  <img src="assets/architect-wordmark.svg" alt="Architect" width="520" />
</h1>

**Fast code is easy. A codebase that survives its next hundred changes is harder.**

*Build codebases that stay coherent as they grow -- without giant modules, speculative abstractions, or accidental breaking changes.*

[![Architect Workflow](https://img.shields.io/badge/Architect-design%20-%20propose%20-%20build-111827?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/tree/main/skills/architect-design)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars)](https://github.com/vortezwohl/Agent-Architect/stargazers)

<br />

**No architecture by accident.** &nbsp; **No abstraction by speculation.** &nbsp; **No compatibility by assumption.**

[Why](#why-architect) &middot; [Workflow](#workflow) &middot; [Outputs](#outputs) &middot; [Example](#example-experience) &middot; [Install](#install)

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

## Why Architect

Most coding agents do not fail because they cannot write code.

They fail because they make structural decisions silently while writing it.

A request that sounds ordinary:

```text
Add a second payment provider.
Refactor this service.
Make this feature extensible.
```

already forces decisions about ownership, boundaries, compatibility, failure behavior, state flow, migration, and rollback.

When those decisions stay implicit, the codebase usually drifts into one of three expensive states:

| Failure | What happens |
| --- | --- |
| **Architecture by neglect** | The feature lands in the nearest file. Ownership blurs, rules duplicate, and one or two modules absorb everything. |
| **Architecture by speculation** | A possible future becomes an interface, factory, registry, event, or inheritance layer before a real variation exists. |
| **Compatibility by assumption** | Existing behavior is preserved or broken without first making the intended boundary explicit. |

Architect exists to force those decisions into the open before the codebase pays for them.

---

## Workflow

Architect is a strict **manual three-stage flow**:

```text
architect-design -> architect-propose -> architect-build
```

Each stage has a separate responsibility and refuses to do the next stage's work automatically.

| Stage | Invoke when | Produces | Refuses to do |
| --- | --- | --- | --- |
| `architect-design` | You need one approved architectural direction for one consequential change. | One approved design bundle containing one or more `D-xxx` subdesigns. | Planning, file writes, or implementation. |
| `architect-propose` | The design bundle is already approved and must become an executable package. | One sealed `.architect/<plan-name>/` package with `D-xxx`, `T-xxx`, state, and log artifacts. | Redesigning the solution or editing app code. |
| `architect-build` | The sealed package is validated and ready to execute. | Real implementation progress, task-state updates, and factual execution logs. | Reopening design or inventing new structure mid-build. |

This is the core user experience change: the agent no longer jumps from request to code. It must first separate design approval, plan sealing, and bounded execution.

---

## Outputs

### 1. Approved design bundle

`architect-design` produces one approved bundle for one future plan package.

Each bundle may contain multiple `D-xxx` subdesigns with explicit intent, boundaries, counterexamples, anti-patterns, and `MUST DO` / `MUST NOT DO` rules.

### 2. Sealed execution package

`architect-propose` converts that approved bundle into one deterministic package under:

```text
.architect/<plan-name>/
```

The package includes:

```text
00-plan-manifest.md
01-context-and-contract.md
02-design-catalog.md
03-designs/D-xxx-<slug>.md
04-impact-and-boundaries.md
05-task-catalog.md
06-tasks/T-xxx-<slug>.md
07-verification-plan.md
08-execution-log.md
.state/execution-state.json
```

This package is not notes. It is the execution contract for the build stage.

### 3. Checkpoint-controlled build evidence

`architect-build` executes the sealed `T-xxx` tasks in order, updates task state truthfully, appends factual log entries, and keeps implementation inside the approved boundary.

What you get is not just code. You get code plus the decision trail, state trail, and execution trail that explain why the code was changed and what actually happened.

---

## Example experience

```text
User:
Add a second payment provider without breaking the current checkout flow.
```

```text
Stage 1: $architect-design
- Reads the repository first.
- Asks what compatibility must hold.
- Separates proven variation from stable policy.
- Produces approved D-xxx subdesigns.
```

```text
Stage 2: $architect-propose add-payment-provider
- Creates .architect/add-payment-provider/
- Allocates design and task documents with repository scripts.
- Seals and validates the package.
```

```text
Stage 3: $architect-build add-payment-provider
- Loads the sealed package and current execution state.
- Executes the recorded T-xxx tasks in order.
- Updates the execution log with actual results.
```

The difference is straightforward:

- A normal coding agent starts coding and hides architectural decisions inside diffs.
- Architect makes those decisions explicit, approved, serialized, and executable.

---

## Install

### Plugin

#### Codex

```text
codex plugin marketplace add vortezwohl/Agent-Architect
codex plugin install architect@architect
```

#### Claude Code

```text
/plugin marketplace add vortezwohl/Agent-Architect
/plugin install architect@architect
```

Start a new session after installation so the agent can discover the plugin.

### Standalone skills

```text
npx skills add vortezwohl/Agent-Architect
```

Or copy `skills/` into your tool's supported skills directory and invoke the stage manually:

```text
$architect-design
$architect-propose <plan-name>
$architect-build <plan-name>
```

> [!IMPORTANT]
> Read a skill before installing it. These skills encode execution rules, package contracts, and stage boundaries.

---

## Using it correctly

Use the stages in order.

1. Run `architect-design` only when you want one approved design bundle.
2. Run `architect-propose` only after that bundle is approved.
3. Run `architect-build` only after the generated package is sealed and validated.

Do not skip directly from a large request to `architect-build`. The repository is built around the separation of approved design, sealed plan, and bounded execution.

---

## Repository shape

```text
assets/
`-- architect-wordmark.svg

skills/
|-- architect-design/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/
|       |-- decision-protocol.md
|       |-- gof-patterns.md
|       `-- source-article.md
|-- architect-propose/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   |-- scripts/
|   `-- templates/
`-- architect-build/
    |-- SKILL.md
    `-- agents/openai.yaml
```

The public product is **Architect**.

The three callable stages are `architect-design`, `architect-propose`, and `architect-build`.

---

## Contributing

Contributions should strengthen the workflow, not add noise.

Good contributions usually improve one of these:

- design-stage evidence gates;
- compatibility-boundary clarity;
- sealed package determinism;
- build-stage execution discipline;
- rollback, validation, or logging accuracy.

If a change adds ceremony without improving one of those properties, it is probably the wrong change.

---

## License

MIT. See [LICENSE](LICENSE).
