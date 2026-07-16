# Agent Architect

Agent Architect 为编码 agent 提供严格的三阶段架构工作流：先批准设计，再生成可执行计划，最后在受控边界内实施。

## 三阶段流程

```text
architect-design
-> architect-propose
-> architect-build
```

### Architect Design

Design 阶段先确认兼容性边界，再基于仓库证据拆分并批准 `D-xxx` 设计单元。每个设计单元必须说明：

- 规范的软件工程概念或设计模式及参考来源；
- 选择依据、替代方案、职责边界和依赖方向；
- 具体反例和反模式；
- 针对设计细节的 `MUST DO` 与 `MUST NOT DO`；
- 覆盖该设计的用户批准证据。

设计的目标不是机械追求最少抽象，而是在兼容性和明确演进范围内，选择最易于理解、维护、验证且有充分依据的结构。

### Architect Propose

Propose 阶段只能把已批准的设计写入 `.architect/<plan-name>/`。计划主体由多个职责单一的 Markdown 文件组成：

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

所有字段、标识、时间戳和目录由程序生成并校验。字段名使用固定英文，正文默认使用用户提问语言。设计和任务 Markdown 是唯一的静态合同；状态只保存在 `.state/execution-state.json`。

### Architect Build

Build 每次只执行一个 `T-xxx` 原子任务。任务必须引用已批准的 `D-xxx` 和设计规则，并明确允许路径、符号、操作、范围外行为、`MUST DO`、`MUST NOT DO`、局部验证和完成条件。

每次原子编辑后都要检查范围。越界或中断时必须回退到任务检查点，不能修补后继续推测。新的无记忆 agent 会先恢复活跃任务，再从已完成状态继续。

## 使用方式

```text
Use $architect-design to define and approve D-xxx design units.

Use $architect-propose <plan-name> to create and seal the Markdown-first plan.

Use $architect-build <plan-name> to execute one task with scope checks and rollback.
```

## 编码约束

计划文档必须使用 UTF-8 without BOM。创建、封存和验证流程会拒绝无效 UTF-8、BOM、replacement character、连续异常问号以及已知乱码标记。遇到编码问题必须停止、修正文本并重新校验。
