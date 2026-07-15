<div align="center">

<h1>
  <img src="../assets/agent-architect-wordmark.svg" alt="Agent Architect" width="560" />
</h1>

**给你的编码智能体补上架构判断力。**

*让代码库在持续增长时依然保持一致性，不再被巨型模块、预支未来的抽象、或意外引入的破坏性变更拖垮。*

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-agent--architect-111827?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars)](https://github.com/vortezwohl/Agent-Architect/stargazers)

<br />

**不要让架构靠偶然形成。** &nbsp; **不要让抽象靠猜测生长。** &nbsp; **不要让兼容性靠想当然决定。**

[安装](#安装) &middot; [前后对比](#前后对比) &middot; [它如何构建更好的架构](#它如何构建更好的架构) &middot; [适用场景](#适用场景)

</div>

<h4 align="center">
  <p>
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/README.md">English</a> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_zh-hant.md">繁體中文</a> |
    <b>简体中文</b> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_ja-jp.md">日本語</a>
  </p>
</h4>

---

## 你的智能体会写代码。它也会设计系统吗？

大多数人不会明确要求编码智能体去做架构决策。

他们要求的，通常只是普通开发工作：

```text
新增一个发票下载端点。
接入第二个支付服务商。
重构这个服务。
让这个功能更易扩展。
```

但在第一行代码落下之前，智能体其实已经在做架构选择：

- 哪个模块拥有这段行为和状态。
- 哪些依赖会跨越边界。
- 哪些错误会变成对外可见的行为。
- 哪些行为必须保持兼容，哪些可以被有意修改。
- 直接实现、抽象层、还是框架扩展，哪一种才有真实依据。

如果没有架构判断力，智能体往往会朝两个代价都很高的方向之一失控。

| 失败方式 | 代码库会变成什么样 |
| --- | --- |
| **疏于架构** | 功能被塞进最近的文件。职责边界越来越模糊，规则开始重复，分支不断增殖，少数服务或包逐渐膨胀到没人愿意再碰。 |
| **猜测式架构** | 在真实变化出现之前，一个“可能的未来”就先变成了接口、工厂、注册表、事件、包装器，甚至继承层次。 |

而在这两种失败里，还藏着第三种常被忽视的问题：

> **想当然的兼容性。** 智能体不是默认把过时行为全部保留下来，就是在没有先讲清边界的情况下，直接改写本来运行正常的行为。

结果也许能编译，也许甚至能演示成功。

但它仍会在之后的每一次变更里，变得更难理解、更难测试、更难扩展，也更难信任。

**Agent Architect 给编码智能体一套有纪律的结构判断方式，让复杂度在扩散之前先被看见。**

---

## 前后对比

### 没有 Agent Architect

```text
用户：“接入第二个支付服务商。”

智能体：往 CheckoutService 里继续加服务商分支，
复制一套 Webhook 处理逻辑，在处理器里直接访问持久层，
为了“未来可能还会有更多服务商”提前造一个 PaymentProviderFactory，
并悄悄改掉了现有集成正在依赖的重试行为。
```

### 有 Agent Architect

```text
用户：“接入第二个支付服务商。”

智能体：
1. 梳理现有支付生命周期、调用方、重试归属、
   Webhook、持久化、错误路径和测试。
2. 不再默认旧契约必须保留，或者可以随便打破，
   而是先把兼容性意图说清楚。
3. 把已被证明会变化的部分（服务商执行）与稳定策略
   （结算、鉴权、重试归属）拆开。
4. 比较最小直接方案和引入服务商边界的方案。
5. 只引入那些足以隔离已证实变化点的结构。
6. 在约定好的兼容性边界内，验证成功、拒绝、超时、
   Webhook、重试、迁移和回滚路径。
```

结果不是多了一层仪式感。

而是 **更小的影响半径、更耐用的设计，以及在代码库为这个决定付出代价之前，就能被检查的解释路径。**

---

## Agent Architect 改变了什么

Agent Architect **不会** 把架构变成用户必须参与的委员会流程。

它做的是：把一个高速代码生成器，变成一个更负责任的软件设计者；当判断会影响行为、结构或兼容性时，让它的推理过程变得可见。

| 不再是 | Agent Architect 会帮助智能体 |
| --- | --- |
| 在最近的文件里直接写代码 | 找出真正的归属者、边界、调用方、依赖关系和失败路径。 |
| 为每一种可能的未来都提前抽象 | 在独立变化被明确命名并被证据证明之前，保持直接设计。 |
| 想当然地默认向后兼容，或默认可以直接重写 | 在设计前先明确真正想维持的兼容性边界。 |
| 把一次重构简单称作“更干净了” | 明确替代方案、结构成本、已完成验证和剩余风险。 |

> 兼容性意图不是官僚流程。它防止两种同样昂贵的错误：保留没人需要的遗留行为，或者打破有人依赖的行为。

---

## 它如何构建更好的架构

### 1. 先读现实，再做设计

智能体在提出结构前，会先检查仓库里的实际证据：受影响的调用方、归属关系、依赖、状态、失败路径、生命周期、事务、并发、框架约束以及现有测试。

### 2. 让兼容性变成有意选择

当变更可能影响契约、数据、配置、外部集成或扩展点时，智能体会先追问：哪些必须兼容，哪些可以有意修改。然后把实际边界、迁移或回滚影响、以及尚未解决的风险记录下来。

它不会偷偷选择“全部保留”或“直接重写更干净”。

### 3. 选择最小但耐用的结构

直接方案永远都是一个真实候选项。接口、适配器、策略、事件、工厂、包装器或框架扩展，只有在它们确实能隔离某个具体且独立的变化点时，才配得上自己的复杂度成本。

### 4. 解释并验证这个决策

智能体会产出一份可审计的架构记录，并在受影响的边界上验证行为。它会说明跑了什么、哪些地方仍不确定、以及为什么被否决的替代方案不值得承担那笔结构成本。

---

## 智能体会交付什么

对于每一个非平凡的功能、集成、设计、重构或评审，Agent Architect 都会生成一份架构记录：

```text
01. 设计诊断
    目标、非目标、仓库证据、调用方、稳定核心、
    变化点、失败模式与约束。

02. 兼容性意图
    需要保留与有意修改的契约、使用方、
    迁移或回滚边界，以及未解决风险。

03. 备选方案与决策
    最小直接设计、被论证成立的结构、被拒绝的选项、
    API 影响、依赖方向与持续成本。

04. 验证
    正常路径、边界路径、失败路径、集成、并发与运维检查，
    实际执行过的验证，以及剩余不确定性。
```

这样，架构决策就不再只是“一堆今天碰巧能跑的生成文件”，而是可以被解释、被审查的工程判断。

---

## 安装

### Codex

```text
$skill-installer install https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect
```

安装后请重启 Codex。

### 其他兼容 Agent Skills 的工具

把 `skills/agent-architect/` 复制到工具支持的 skills 目录中，然后执行：

```text
agent-architect
```

> [!IMPORTANT]
> 安装前请先阅读 skill。Skill 本质上是可执行的智能体指令：你需要检查它的说明、附带参考资料、脚本，以及信任边界。

---

## 使用方式

你可以这样对编码智能体下达指令：

```text
在实现或评审这项非平凡变更之前，先使用 $agent-architect。
检查仓库，在必要处明确兼容性意图，
选择最小但耐用的架构，然后再实现并验证。
```

示例：

```text
在接入这个支付服务商之前，先使用 $agent-architect。

用 $agent-architect 评审这个功能，
找出偶然形成的架构、猜测式抽象，以及不清晰的兼容性边界。

在重构这个服务边界之前，先使用 $agent-architect。
只有在契约被明确之后，才允许保留或有意改变行为。

用 $agent-architect 判断这项集成到底需要适配器、
直接依赖，还是框架扩展。
```

---

## 适用场景

当一次变更可能重塑代码库时，就该使用 Agent Architect：

- 一个功能跨越多个模块、层、服务、数据库或第三方服务商。
- 你正准备“重构”“扩展”“抽象”“解耦”“泛化”或“为未来做准备”。
- 智能体开始提议接口、工厂、事件、注册表、包装器、继承体系或全局状态。
- 你不确定现有行为是否必须保持兼容。
- 你已经看到巨型服务、巨型包、重复规则、跨层依赖，或没人能自信解释的分支逻辑。
- 一个 PR 看起来能工作，但其中的结构性决策仍然是隐含的。

> [!TIP]
> 把 Agent Architect 放进处理功能开发和结构性变更的工作流里。不要等偶发复杂度已经扩散之后再补救。

---

## 模式是最后一步，不是起点

Agent Architect 覆盖全部 23 个 GoF 设计模式。

但它更重要的能力，是知道 **什么时候不该使用某个模式**。

它从证据出发：**什么在变化，谁拥有它，什么会失败，什么必须保持稳定，以及直接方案已经解决了什么。**

<details>
<summary><b>创建型决策</b></summary>

- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton scope

</details>

<details>
<summary><b>结构型决策</b></summary>

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

</details>

<details>
<summary><b>行为型决策</b></summary>

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
<summary><b>关键模式边界</b></summary>

| 不要混淆 | 应区分于 |
| --- | --- |
| Decorator | Proxy 或 Adapter |
| Facade | Mediator |
| Factory Method | Abstract Factory、Builder 或 Prototype |
| Strategy | State 或 Template Method |
| Observer | Chain of Responsibility 或 Command |
| Composite | Decorator |

模式应根据 **意图、协作者、生命周期、变化方式和失败行为** 来选择，而不是只看类图。

</details>

---

## 这个 skill 不是什么

| 不是这个 | 而是这个 |
| --- | --- |
| 设计模式百科 | 面向编码智能体的架构判断系统 |
| 仪式生成器 | 一种把恰当程度的结构变得显式且可验证的方法 |
| 默认套用“整洁架构” | 基于证据分析边界、归属、依赖和生命周期 |
| 增加更多层级的理由 | 当没有证据时，允许保留直接设计 |
| 卡住人工审批的瓶颈 | 当兼容性或架构变得重要时，让人类保持知情的方法 |
| 工程责任的替代品 | 让智能体产出的结构更负责任、可审计、可维护的方法 |

---

## 仓库结构

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

- `SKILL.md` -- 运行规则与必需的架构记录
- `decision-protocol.md` -- 兼容性意图、架构共识、诊断、选择、重构与评审关卡
- `gof-patterns.md` -- 模式意图、权衡、误用案例与验证指引
- `source-article.md` -- AI 编码时代的架构原则

---

## 贡献

贡献应当提升 **架构判断力**，而不是增加仪式。

有价值的贡献包括：

- 面向真实功能和架构决策的证据关卡。
- 更清晰的兼容性边界、迁移指引和回滚标准。
- 更清晰的模式边界与拒绝条件。
- 可复现的偶然架构与猜测式抽象案例。
- 面向生命周期、并发、事务、迁移和回滚的验证指引。
- 让智能体更不容易扩散结构复杂度的修正。

在发起变更前，先问自己：

```text
这是否提升了智能体在代码扩散之前能做出的判断？
这项改进能被验证吗？
它是否在不增加猜测式流程的前提下提供了指导？
```

---

## 许可证

MIT。详见 [LICENSE](../LICENSE)。

---

<div align="center">

### 快速写代码很容易。真正更难的，是构建一个能撑过下一百次变更的代码库。

<strong>把这种判断力，交给你的编码智能体。</strong>

</div>
