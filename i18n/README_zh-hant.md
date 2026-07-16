<div align="center">

<h1>
  <img src="../assets/agent-architect-wordmark.svg" alt="Agent Architect" width="560" />
</h1>

**快速寫程式碼很容易。真正更難的，是建出一個能撐過下一百次變更的程式碼庫。**

*讓程式碼庫在持續成長時依然保持一致性，不再被巨型模組、預支未來的抽象，或意外引入的破壞性變更拖垮。*

[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-agent--architect-111827?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/tree/main/skills/agent-architect)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](https://github.com/vortezwohl/Agent-Architect/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars)](https://github.com/vortezwohl/Agent-Architect/stargazers)

<br />

**不要讓架構靠偶然形成。** &nbsp; **不要讓抽象靠猜測生長。** &nbsp; **不要讓相容性靠想當然決定。**

[安裝](#安裝) &middot; [前後對比](#前後對比) &middot; [它如何構建更好的架構](#它如何構建更好的架構) &middot; [適用場景](#適用場景)

</div>

<h4 align="center">
  <p>
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/README.md">English</a> |
    <b>繁體中文</b> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_zh-hans.md">简体中文</a> |
    <a href="https://github.com/vortezwohl/Agent-Architect/blob/main/i18n/README_ja-jp.md">日本語</a>
  </p>
</h4>

---

## 你的智能體會寫程式碼。它也會設計系統嗎？

大多數人不會明確要求編碼智能體去做架構決策。

他們要求的，通常只是一般開發工作：

```text
新增一個發票下載端點。
接入第二個支付服務商。
重構這個服務。
讓這個功能更易擴展。
```

但在第一行程式碼落下之前，智能體其實已經在做架構選擇：

- 哪個模組擁有這段行為和狀態。
- 哪些依賴會跨越邊界。
- 哪些錯誤會變成對外可見的行為。
- 哪些行為必須保持相容，哪些可以被有意修改。
- 直接實作、抽象層，還是框架擴充，哪一種才有真實依據。

如果沒有架構判斷力，智能體往往會朝兩個代價都很高的方向之一失控。

| 失敗方式 | 程式碼庫會變成什麼樣 |
| --- | --- |
| **疏於架構** | 功能被塞進最近的檔案。職責邊界越來越模糊，規則開始重複，分支不斷增殖，少數服務或套件逐漸膨脹到沒人願意再碰。 |
| **猜測式架構** | 在真實變化出現之前，一個「可能的未來」就先變成了介面、工廠、註冊表、事件、包裝器，甚至繼承層次。 |

而在這兩種失敗裡，還藏著第三種常被忽視的問題：

> **想當然的相容性。** 智能體不是預設把過時行為全部保留下來，就是在沒有先講清邊界的情況下，直接改寫本來運作正常的行為。

結果也許能編譯，也許甚至能演示成功。

但它仍會在之後的每一次變更裡，變得更難理解、更難測試、更難擴展，也更難信任。

**Agent Architect 給編碼智能體一套有紀律的結構判斷方式，讓複雜度在擴散之前先被看見。**

---

## 前後對比

### 沒有 Agent Architect

```text
使用者：「接入第二個支付服務商。」

智能體：往 CheckoutService 裡繼續加服務商分支，
複製一套 Webhook 處理邏輯，在處理器裡直接存取持久層，
為了「未來可能還會有更多服務商」提前造一個 PaymentProviderFactory，
並悄悄改掉了現有整合正在依賴的重試行為。
```

### 有 Agent Architect

```text
使用者：「接入第二個支付服務商。」

智能體：
1. 梳理現有支付生命週期、呼叫方、重試歸屬、
   Webhook、持久化、錯誤路徑和測試。
2. 不再預設舊契約必須保留，或者可以隨便打破，
   而是先把相容性意圖說清楚。
3. 把已被證明會變化的部分（服務商執行）與穩定策略
   （結算、鑑權、重試歸屬）拆開。
4. 比較最小直接方案和引入服務商邊界的方案。
5. 只引入那些足以隔離已證實變化點的結構。
6. 在約定好的相容性邊界內，驗證成功、拒絕、逾時、
   Webhook、重試、遷移和回滾路徑。
```

結果不是多了一層儀式感。

而是 **更小的影響半徑、更耐用的設計，以及在程式碼庫為這個決定付出代價之前，就能被檢查的解釋路徑。**

---

## Agent Architect 改變了什麼

Agent Architect **不會** 把架構變成使用者必須參與的委員會流程。

它做的是：把一個高速程式碼生成器，變成一個更負責任的軟體設計者；當判斷會影響行為、結構或相容性時，讓它的推理過程變得可見。

| 不再是 | Agent Architect 會幫助智能體 |
| --- | --- |
| 在最近的檔案裡直接寫程式碼 | 找出真正的歸屬者、邊界、呼叫方、依賴關係和失敗路徑。 |
| 為每一種可能的未來都提前抽象 | 在獨立變化被明確命名並被證據證明之前，保持直接設計。 |
| 想當然地預設向後相容，或預設可以直接重寫 | 在設計前先明確真正想維持的相容性邊界。 |
| 把一次重構簡單稱作「更乾淨了」 | 明確替代方案、結構成本、已完成驗證和剩餘風險。 |

> 相容性意圖不是官僚流程。它防止兩種同樣昂貴的錯誤：保留沒人需要的遺留行為，或者打破有人依賴的行為。

---

## 它如何構建更好的架構

### 1. 先讀現實，再做設計

智能體在提出結構前，會先檢查倉庫裡的實際證據：受影響的呼叫方、歸屬關係、依賴、狀態、失敗路徑、生命週期、交易、並行、框架約束以及現有測試。

### 2. 讓相容性變成有意選擇

當變更可能影響契約、資料、設定、外部整合或擴充點時，智能體會先追問：哪些必須相容，哪些可以有意修改。然後把實際邊界、遷移或回滾影響、以及尚未解決的風險記錄下來。

它不會偷偷選擇「全部保留」或「直接重寫更乾淨」。

### 3. 選擇最小但耐用的結構

直接方案永遠都是一個真實候選項。介面、適配器、策略、事件、工廠、包裝器或框架擴充，只有在它們確實能隔離某個具體且獨立的變化點時，才配得上自己的複雜度成本。

### 4. 解釋並驗證這個決策

智能體會產出一份可審計的架構記錄，並在受影響的邊界上驗證行為。它會說明跑了什麼、哪些地方仍不確定、以及為什麼被否決的替代方案不值得承擔那筆結構成本。

---

## 智能體會交付什麼

對於每一個非平凡的功能、整合、設計、重構或評審，Agent Architect 都會生成一份架構記錄：

```text
01. 設計診斷
    目標、非目標、倉庫證據、呼叫方、穩定核心、
    變化點、失敗模式與約束。

02. 相容性意圖
    需要保留與有意修改的契約、使用方、
    遷移或回滾邊界，以及未解決風險。

03. 備選方案與決策
    最小直接設計、被論證成立的結構、被拒絕的選項、
    API 影響、依賴方向與持續成本。

04. 驗證
    正常路徑、邊界路徑、失敗路徑、整合、並行與維運檢查，
    實際執行過的驗證，以及剩餘不確定性。
```

這樣，架構決策就不再只是「一堆今天碰巧能跑的生成檔案」，而是可以被解釋、被審查的工程判斷。

---

## 安裝

### 外掛

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

安裝後請開啟新的工作階段，讓智能體偵測此插件。

### 獨立 Skill

使用 Skills CLI 直接安裝此 skill：

```text
npx skills add vortezwohl/Agent-Architect
```

或者將 `skills/agent-architect/` 複製到智能體支援的 skills 目錄，然後呼叫：

```text
agent-architect
```

> [!IMPORTANT]
> 安裝前請先閱讀 skill。Skill 是可執行的智能體指引：請檢查其說明、附帶的參考資料、腳本以及信任邊界。

---

## 使用方式

你可以這樣對編碼智能體下達指令：

```text
在實作或評審這項非平凡變更之前，先使用 $agent-architect。
檢查倉庫，在必要處明確相容性意圖，
選擇最小但耐用的架構，然後再實作並驗證。
```

範例：

```text
在接入這個支付服務商之前，先使用 $agent-architect。

用 $agent-architect 評審這個功能，
找出偶然形成的架構、猜測式抽象，以及不清晰的相容性邊界。

在重構這個服務邊界之前，先使用 $agent-architect。
只有在契約被明確之後，才允許保留或有意改變行為。

用 $agent-architect 判斷這項整合到底需要適配器、
直接依賴，還是框架擴充。
```

---

## 適用場景

當一次變更可能重塑程式碼庫時，就該使用 Agent Architect：

- 一個功能跨越多個模組、層、服務、資料庫或第三方服務商。
- 你正準備「重構」「擴展」「抽象」「解耦」「泛化」或「為未來做準備」。
- 智能體開始提議介面、工廠、事件、註冊表、包裝器、繼承體系或全域狀態。
- 你不確定現有行為是否必須保持相容。
- 你已經看到巨型服務、巨型套件、重複規則、跨層依賴，或沒人能自信解釋的分支邏輯。
- 一個 PR 看起來能工作，但其中的結構性決策仍然是隱含的。

> [!TIP]
> 把 Agent Architect 放進處理功能開發和結構性變更的工作流程裡。不要等偶發複雜度已經擴散之後再補救。

---

## 模式是最後一步，不是起點

Agent Architect 覆蓋全部 23 個 GoF 設計模式。

但它更重要的能力，是知道 **什麼時候不該使用某個模式**。

它從證據出發：**什麼在變化，誰擁有它，什麼會失敗，什麼必須保持穩定，以及直接方案已經解決了什麼。**

<details>
<summary><b>建立型決策</b></summary>

- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton scope

</details>

<details>
<summary><b>結構型決策</b></summary>

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

</details>

<details>
<summary><b>行為型決策</b></summary>

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
<summary><b>關鍵模式邊界</b></summary>

| 不要混淆 | 應區分於 |
| --- | --- |
| Decorator | Proxy 或 Adapter |
| Facade | Mediator |
| Factory Method | Abstract Factory、Builder 或 Prototype |
| Strategy | State 或 Template Method |
| Observer | Chain of Responsibility 或 Command |
| Composite | Decorator |

模式應根據 **意圖、協作者、生命週期、變化方式和失敗行為** 來選擇，而不是只看類別圖。

</details>

---

## 這個 skill 不是什麼

| 不是這個 | 而是這個 |
| --- | --- |
| 設計模式百科 | 面向編碼智能體的架構判斷系統 |
| 儀式生成器 | 一種把恰當程度的結構變得顯式且可驗證的方法 |
| 預設套用「整潔架構」 | 基於證據分析邊界、歸屬、依賴和生命週期 |
| 增加更多層級的理由 | 當沒有證據時，允許保留直接設計 |
| 卡住人工審批的瓶頸 | 當相容性或架構變得重要時，讓人類保持知情的方法 |
| 工程責任的替代品 | 讓智能體產出的結構更負責任、可審計、可維護的方法 |

---

## 倉庫結構

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

- `SKILL.md` -- 執行規則與必需的架構記錄
- `decision-protocol.md` -- 相容性意圖、架構共識、診斷、選擇、重構與評審關卡
- `gof-patterns.md` -- 模式意圖、權衡、誤用案例與驗證指引
- `source-article.md` -- AI 編碼時代的架構原則

---

## 貢獻

貢獻應當提升 **架構判斷力**，而不是增加儀式。

有價值的貢獻包括：

- 面向真實功能和架構決策的證據關卡。
- 更清晰的相容性邊界、遷移指引和回滾標準。
- 更清晰的模式邊界與拒絕條件。
- 可重現的偶然架構與猜測式抽象案例。
- 面向生命週期、並行、交易、遷移和回滾的驗證指引。
- 讓智能體更不容易擴散結構複雜度的修正。

在發起變更前，先問自己：

```text
這是否提升了智能體在程式碼擴散之前能做出的判斷？
這項改進能被驗證嗎？
它是否在不增加猜測式流程的前提下提供了指導？
```

---

## 授權

MIT。詳見 [LICENSE](../LICENSE)。

---

<div align="center">

### 給你的編碼智能體補上架構判斷力。

<strong>讓它在變化中持續建出一致的程式碼庫。</strong>

</div>
