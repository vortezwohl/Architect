# Agent Architect

Agent Architect 為編碼 agent 提供嚴格的三階段架構工作流程：先批准設計，再產生可執行計畫，最後在受控邊界內實作。

## 三階段流程

```text
architect-design
-> architect-propose
-> architect-build
```

### Architect Design

Design 階段先確認相容性邊界，再根據儲存庫證據拆分並批准 `D-xxx` 設計單元。每個設計單元必須記錄規範工程概念或模式、選擇依據、替代方案、反例、反模式、設計級 `MUST DO` / `MUST NOT DO` 以及使用者批准證據。

目標不是機械地追求最少抽象，而是在相容性和明確演進範圍內，選擇最容易理解、維護、驗證且有充分依據的結構。

### Architect Propose

Propose 只會把已批准設計寫入 `.architect/<plan-name>/`。設計和任務以多份職責單一的 Markdown 文件保存；固定英文欄位、識別碼、時間戳與目錄由程式產生並驗證，正文預設使用使用者提問語言。

靜態設計與任務 Markdown 是唯一合同；可變任務狀態只保存在 `.state/execution-state.json`，避免狀態分散。

### Architect Build

Build 每次只執行一個 `T-xxx` 原子任務。每個任務必須引用已批准的 `D-xxx`、精確路徑與符號邊界、設計級規則、`MUST DO`、`MUST NOT DO`、範圍外行為與完成條件。

每次原子編輯後都要檢查範圍。越界或中斷時必須完整回退到任務檢查點；新的無記憶 agent 先恢復活躍任務，再從已驗證完成的狀態繼續。

## 使用方式

```text
Use $architect-design to define and approve D-xxx design units.
Use $architect-propose <plan-name> to create and seal the Markdown-first plan.
Use $architect-build <plan-name> to execute one task with scope checks and rollback.
```

計畫文件必須使用 UTF-8 without BOM。驗證流程拒絕無效 UTF-8、BOM、replacement character、連續異常問號和已知亂碼標記。
