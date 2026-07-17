<div align="center">

<h1>
  <img src="../assets/architect-wordmark.svg" alt="Architect" width="520" />
</h1>

**快速寫程式碼不難。難的是讓程式碼庫在接下來上百次變更後依然站得住。**

*建立會隨著規模成長仍保持一致性的程式碼庫，而不是落入巨型模組、預設性抽象或意外破壞性變更。*

[![Architect Workflow](https://img.shields.io/static/v1?label=Architect&message=design%20%E2%86%92%20propose%20%E2%86%92%20build&color=111827&style=flat-square)](../skills/architect-design/)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](../LICENSE)
[![Architect Repo](https://img.shields.io/badge/GitHub-open%20repo-181717?style=flat-square)](..)

<br />

**不要讓架構在偶然中形成。** &nbsp; **不要靠臆測引入抽象。** &nbsp; **不要憑假設維護相容性。**

[Why](#為什麼選擇-architect) &middot; [Install](#安裝) &middot; [Quick start](#外掛快速開始) &middot; [Use it correctly](#正確使用方式) &middot; [Example](#示例體驗) &middot; [Workflow](#工作流) &middot; [Outputs](#產物)

</div>

<h4 align="center">
  <p>
    <a href="../README.md">English</a> |
    <b>&#32321;&#39636;&#20013;&#25991;</b> |
    <a href="README_zh-hans.md">&#31616;&#20307;&#20013;&#25991;</a> |
    <a href="README_ja-jp.md">&#26085;&#26412;&#35486;</a>
  </p>
</h4>

---

## 為什麼選擇 Architect

多數 coding agent 失敗，並不是因為它們不會寫程式碼。

而是因為它們會在寫程式碼的同時，悄悄做出結構性決策。

一個聽起來很普通的請求：

```text
增加第二個支付提供方。
重構這個服務。
讓這個功能可擴展。
```

其實已經強迫你對所有權、邊界、相容性、失敗行為、狀態流、遷移方式和回滾方式做出決策。

當這些決策始終保持隱含狀態時，程式碼庫通常會滑向三種代價高昂的狀態之一：

| Failure | What happens |
| --- | --- |
| **Architecture by neglect** | 功能被塞進最近的檔案裡。所有權開始模糊，規則開始複製，一兩個模組不斷吞掉一切。 |
| **Architecture by speculation** | 還沒有真實變化點時，可能的未來就先被做成介面、工廠、登錄表、事件層或繼承層。 |
| **Compatibility by assumption** | 在未先把預期邊界說清楚之前，既有行為就被預設保留，或者被預設破壞。 |

Architect 的存在，就是為了在程式碼庫為這些決策付出代價之前，先把它們強制暴露出來。

---

## 安裝

### 外掛

#### Codex

```text
codex plugin marketplace add vortezwohl/Architect
codex plugin install architect@architect
```

#### Claude Code

```text
/plugin marketplace add vortezwohl/Architect
/plugin install architect@architect
```

安裝完成後請開啟一個新工作階段，這樣 agent 才能發現該外掛。

### 獨立技能

```text
npx skills add vortezwohl/Architect
```

或者把 `skills/` 複製到你的工具支援的 skills 目錄中，然後手動呼叫各階段：

```text
$architect-design
$architect-propose <plan-name>
$architect-build <plan-name>
```

> [!IMPORTANT]
> 安裝前先閱讀 skill。這些 skill 編碼了執行規則、包合約和階段邊界。

> [!TIP]
> 如果安裝後沒有立刻看到這些命令，先開啟一個新工作階段。

---

## 外掛快速開始

安裝完成後，你應該會看到**三個外掛命令**：

- `design`
- `propose`
- `build`

把它當成精靈來用。只有上一步完成後，再點下一步。

> [!TIP]
> 對大多數人來說，最快的開始方式很簡單：先點 `design`，用一句話描述要做的變更，然後用同一個名稱接著走 `propose` 和 `build`。

### Step 1: Design

先用這個。

告訴 Architect 你想改什麼。

```text
$architect-design Add a second payment provider without breaking checkout.
```

```text
/architect:design Add a second payment provider without breaking checkout.
```

你會得到：

- 一個已批准的設計包；
- 清晰的邊界；
- 此時還不會開始寫程式碼。

### Step 2: Propose

在設計獲批後使用這個。

給這次變更起一個簡短的計畫名：

```text
$architect-propose add-payment-provider
```

```text
/architect:propose add-payment-provider
```

你會得到：

- 一個封存好的 `.architect/add-payment-provider/` 包；
- 任務文件；
- 驗證計畫；
- 執行日誌。

### Step 3: Build

在計畫包已經存在後使用這個。

繼續使用同一個計畫名：

```text
$architect-build add-payment-provider
```

```text
/architect:build add-payment-provider
```

會發生什麼：

- Architect 依序執行已記錄的任務；
- 更新狀態和日誌；
- 把工作限制在已批准邊界內。

### 我該點哪個？

- 新變更：從 `design` 開始
- 設計已批准，但還沒有計畫包：用 `propose`
- 計畫已經建立好：用 `build`

### 一條規則

不要直接跳到 `build`。

Architect 的核心就是：

```text
design -> propose -> build
```

---

## 正確使用方式

依序使用各階段。

1. 只有在你需要一個經過批准的設計包時，才執行 `architect-design`。
2. 只有在該設計包已經獲批後，才執行 `architect-propose`。
3. 只有在生成的執行包已經封存並校驗後，才執行 `architect-build`。

不要從一個大型請求直接跳到 `architect-build`。這個儲存庫是圍繞「已批准設計、封存計畫和有邊界執行的分離」而建立的。

> [!IMPORTANT]
> Architect 故意保持手動三階段流程。它不是用來替你猜下一步該做什麼的。

---

## 示例體驗

```text
User:
在不破壞目前結帳流程的前提下，增加第二個支付提供方。
```

```text
Stage 1: $architect-design
- 先讀取儲存庫。
- 詢問必須保持哪些相容性。
- 把已被證明的變化點和穩定策略分離開。
- 產出已批准的 D-xxx 子設計。
```

```text
Stage 2: $architect-propose add-payment-provider
- 建立 .architect/add-payment-provider/
- 使用儲存庫腳本分配設計文件和任務文件。
- 封存並校驗執行包。
```

```text
Stage 3: $architect-build add-payment-provider
- 載入封存包和目前執行狀態。
- 依序執行記錄在案的 T-xxx 任務。
- 用真實結果更新執行日誌。
```

差異很直接：

- 一般 coding agent 會直接開始寫程式碼，並把架構決策藏進 diff 裡。
- Architect 會讓這些決策變得顯式、可批准、可序列化、可執行。

---

## 工作流

Architect 是一個嚴格的**手動三階段流程**：

```text
architect-design -> architect-propose -> architect-build
```

每個階段都有獨立職責，並且會拒絕自動去做下一個階段的工作。

| Stage | Invoke when | Produces | Refuses to do |
| --- | --- | --- | --- |
| `architect-design` | 你需要為一次重要變更確定一個經過批准的架構方向。 | 一個經過批准的設計包，其中包含一個或多個 `D-xxx` 子設計。 | 計畫編排、檔案寫入或實作。 |
| `architect-propose` | 設計包已經獲批，必須轉成可執行包。 | 一個封存好的 `.architect/<plan-name>/` 包，包含 `D-xxx`、`T-xxx`、狀態檔案和日誌產物。 | 重新設計方案或編輯應用程式碼。 |
| `architect-build` | 封存包已經校驗完畢，準備執行。 | 真實的實作推進、任務狀態更新，以及基於事實的執行日誌。 | 在建置中途重新打開設計，或臨時發明新結構。 |

這就是核心的使用者體驗變化：agent 不再從請求直接跳到程式碼。它必須先把設計批准、計畫封存和有邊界的執行拆開。

---

## 產物

### 1. 已批准的設計包

`architect-design` 會為一個未來計畫包產出一個已批准的設計包。

每個設計包都可以包含多個 `D-xxx` 子設計，並且明確給出意圖、邊界、反例、反模式，以及 `MUST DO` / `MUST NOT DO` 規則。

### 2. 封存的執行包

`architect-propose` 會把該已批准設計包轉換為位於以下目錄中的一個確定性執行包：

```text
.architect/<plan-name>/
```

該執行包包含：

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

這不是一堆筆記，而是建置階段的執行合約。

### 3. 受檢查點控制的建置證據

`architect-build` 會依序執行封存的 `T-xxx` 任務，如實更新任務狀態，追加基於事實的日誌記錄，並把實作嚴格限制在已批准邊界內。

你得到的不只是程式碼。你得到的是程式碼，以及解釋為什麼要改程式碼、實際發生了什麼的決策軌跡、狀態軌跡和執行軌跡。

---

## 儲存庫結構

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

公開產品名稱是 **Architect**。

三個可呼叫階段分別是 `architect-design`、`architect-propose` 和 `architect-build`。

---

## 貢獻

貢獻應該強化這套工作流，而不是增加噪音。

好的貢獻通常會改善以下某一項：

- 設計階段的證據門禁；
- 相容性邊界的清晰度；
- 封存包的確定性；
- 建置階段的執行紀律；
- 回滾、校驗或日誌記錄的準確性。

如果一個改動增加了流程負擔，卻沒有提升上述任一屬性，那它大概率就是錯誤的改動。

---

## 授權

MIT。參見 [LICENSE](../LICENSE)。
