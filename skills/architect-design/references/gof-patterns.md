# Complete GoF Design Pattern Catalog

## Coverage Contract

This catalog teaches all 23 Gang of Four patterns: 5 creational, 7 structural, and 11 behavioral. "All design patterns" is not a finite category; treat GoF as the canonical catalog and evaluate architectural styles and framework idioms separately. For every candidate, identify a proven variation, choose by intent rather than shape, state the cost, compare neighbors, and test the seam.

## How to Use This Catalog

- Read this file after `source-article.md` has already framed the design problem.
- Read neighboring candidates together whenever their structure is visually similar or their responsibilities are often confused.
- Extract teaching material, not just labels: stable core, true variation, cost, rejected neighbors, misuse risk, and required task-declared checks.
- Treat this file as a routing and comparison reference; do not force every task into a GoF pattern when a direct design remains better justified.

## Quick Routing by Design Question

| If the design question is about... | Start with | Compare with |
| --- | --- | --- |
| One goal, many algorithms | Strategy | State, Template Method |
| One lifecycle, many valid states | State | Strategy, Template Method |
| One fixed process, varying local steps | Template Method | Strategy, Facade |
| One object versus one compatible family | Factory Method | Abstract Factory, Builder, Prototype |
| Legacy translation versus layered control or enhancement | Adapter | Decorator, Proxy |
| Responsibility enhancement versus access control | Decorator | Proxy, Facade |
| Many consumers reacting to one fact | Observer | Chain of Responsibility, Command |
| Orchestration entry point versus peer coordination | Facade | Mediator |
| Ordered optional handling | Chain of Responsibility | Observer, Command |
| Semantic uniqueness scope | Singleton | Factory Method, container lifetime |

## Design Unit Mapping

When a GoF pattern is selected or rejected, map what you learned into the design-unit fields:

- `Concept`: canonical pattern name, category, and reference.
- `Intent`: the problem the pattern solves in the current task.
- `StableCoreAndVariation`: what stays fixed and what changes independently.
- `Rationale`: why the pattern beats the direct design here.
- `Alternatives`: the neighboring patterns or simpler structures that were rejected.
- `Counterexamples` and `AntiPatterns`: what would make the pattern a bad fit.
- `Rules`: lifecycle, dependency, ownership, transaction, error, and task-declared implementation/check constraints that Build must obey.

## Creational Patterns

| Pattern | Intent and use | Cost, boundary, task-declared checks |
| --- | --- | --- |
| Abstract Factory | Create compatible product families when platform, theme, or vendor families switch together. | More types; adding a product kind changes every factory. Factory Method creates one product, Builder assembles one complex product. Test every family combination and forbid mixed families. |
| Builder | Assemble a complex object through ordered or optional steps while preserving construction invariants. | Ceremony is wasteful for small values. Unlike Abstract Factory, it constructs one object step by step. Test incomplete sequences, defaults, and final immutability. |
| Factory Method | Defer one concrete product choice from users to a creator or injected creation seam. | Factory growth can be unnecessary; a constructor function may be clearer. Unlike Abstract Factory, it does not select a family. Test selection and lifecycle failures. |
| Prototype | Create a configured object by copying a prototype. | Deep and shallow copy, identity, resources, and mutable nested state are dangerous. Unlike Builder, it copies rather than assembles. Test independent mutation and resource handling. |
| Singleton | Enforce a declared semantic uniqueness scope; prefer a dependency-injection container lifetime. | Hidden dependencies, test contamination, global mutation, and concurrency ambiguity. Never use it to avoid dependency injection. |

## Structural Patterns

| Pattern | Intent and use | Cost, boundary, task-declared checks |
| --- | --- | --- |
| Adapter | Translate an incompatible legacy or third-party interface into the target interface. | It can conceal a wrong model. Facade simplifies, Decorator enhances, and Proxy controls. Contract-test data, error, and version translation. |
| Bridge | Split two independent axes of variation to avoid a subclass cross-product. | Indirection is unjustified if axes do not vary independently. Strategy swaps one algorithm; Bridge separates durable abstraction and implementation axes. |
| Composite | Treat leaf and part-whole tree elements uniformly through one component contract. | A shared contract can become dishonest. Test empty and deep trees, cycles, and leaf restrictions. |
| Decorator | Stack optional responsibilities such as cache, retry, or logging without subclass combinations. | Wrapper order, debugging, and identity matter. Proxy controls access; Adapter translates. Test stacked, order-sensitive behavior and failures. |
| Facade | Give callers one high-level interface over repeated complex subsystem orchestration. | It can become a god object or hide transaction policy. Test order, compensations, failures, and decoupled callers. |
| Flyweight | Share intrinsic immutable state when measured object-count pressure exists. | Cache lifecycle, identity, and thread safety make premature use harmful. Benchmark memory and test immutability. |
| Proxy | Preserve a subject interface while controlling authorization, lazy load, remote access, cache, or transactions. | Hidden latency, failures, and policy bypasses require allowed, denied, invalidation, and remote-failure tests. |

## Behavioral Patterns

| Pattern | Intent and use | Cost, boundary, task-declared checks |
| --- | --- | --- |
| Chain of Responsibility | Pass a request through ordered optional handlers until handled or exhausted. | Requests may vanish and ordering is policy. Test no-handler, order, short-circuit, errors, and cycles. |
| Command | Represent an operation for queueing, audit, retry, scheduling, remote dispatch, or undo. | Many small types and idempotency ambiguity; a callable may suffice. Test serialization, retry, authorization, and compensation. |
| Interpreter | Represent and evaluate a small stable DSL grammar through expression objects. | Grammar growth becomes class explosion; use a parser engine for serious languages. Test syntax, precedence, limits, and diagnostics. |
| Iterator | Traverse an aggregate without exposing representation. | Mutation invalidation, resource lifetime, and hidden I/O matter. Test empty, deep, paginated, mutating, and cancelled traversal. |
| Mediator | Centralize complex peer coordination so peers do not form a coupling mesh. | The mediator can become a god object. Test rules, transitions, and prohibited direct coupling. |
| Memento | Capture and restore state without exposing internals for undo or checkpoints. | Memory, sensitive retention, versioning, and shallow copies are risks. Test restoration, branching, redaction, and versions. |
| Observer | Broadcast a fact to independent subscribers without making the publisher know consumers. | Ordering, handler failure, delivery, transactions, retries, idempotency, and consistency require separate design. |
| State | Change context behavior according to explicit lifecycle state and transitions. | Too many classes are wasteful for trivial conditionals; hidden transitions are dangerous. Test transition tables, illegal states, concurrency, and recovery. |
| Strategy | Swap a family of algorithms serving one stable goal. | It is unnecessary for a few stable branches. Test each algorithm, selection, fallback, and edge cases. |
| Template Method | Fix algorithm order and invariants while deferring local steps to subclasses. | Fragile base classes and inheritance hierarchies are risks; prefer composition for independently combinable changes. |
| Visitor | Add operations across a stable heterogeneous element structure through double dispatch. | New element types force every visitor change. Test every visitor-element pair and missing operations. |

## Teaching Checklist

For each candidate, explain the changing thing, stable core, collaborators and dependency direction, lifecycle and ownership, direct alternative, nearest patterns rejected, failure semantics, and normal, boundary, failure, integration, concurrency, and performance tests where relevant.

## Non-Negotiable Distinctions

- Decorator / Proxy / Adapter: enhancement / control / translation.
- Factory Method / Abstract Factory / Builder / Prototype: one product choice / family choice / staged assembly / copying.
- Strategy / State / Template Method: selected algorithm / lifecycle behavior / fixed skeleton.
- Observer / Chain / Command: broadcast fact / ordered propagation / represented operation.
- Facade / Mediator: simplify subsystem access / coordinate peers.
