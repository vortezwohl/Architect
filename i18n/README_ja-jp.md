# Architect

Architect ?????????????????????????????????????????????

## ??????

## 三段階の流れ

```text
architect-design
-> architect-propose
-> architect-build
```

### Architect Design

Design は互換性の境界を確認してから、リポジトリの証拠に基づく `D-xxx` 設計単位を定義し、利用者の承認を得ます。各設計単位には、標準的な設計概念またはパターン、根拠、代替案、反例、アンチパターン、設計レベルの `MUST DO` / `MUST NOT DO`、承認証拠が必要です。

目的は最小の抽象化を機械的に選ぶことではありません。互換性と明示された進化範囲の中で、最も理解しやすく、保守・検証しやすく、根拠のある構造を選びます。

### Architect Propose

Propose は承認済み設計だけを `.architect/<plan-name>/` に記録します。設計とタスクは責務が一つずつの Markdown ファイルに分割されます。固定の英語フィールド、識別子、タイムスタンプ、ディレクトリはプログラムが作成・検証し、本文は既定で利用者の質問言語を使います。

静的な設計・タスク Markdown が唯一の契約です。可変のタスク状態は `.state/execution-state.json` のみに保存します。

### Architect Build

Build は一度に一つの `T-xxx` 原子的タスクだけを実行します。タスクは承認済み `D-xxx`、正確なパスとシンボル境界、設計ルール、`MUST DO`、`MUST NOT DO`、範囲外の変更、完了条件を参照しなければなりません。

原子的な編集ごとに範囲を確認します。境界違反または中断時は、必ずタスクのチェックポイントへ完全にロールバックします。記憶を持たない新しい agent は、まず進行中のタスクを回復してから、検証済みの状態から再開します。

## 使用方法

```text
Use $architect-design to define and approve D-xxx design units.
Use $architect-propose <plan-name> to create and seal the Markdown-first plan.
Use $architect-build <plan-name> to execute one task with scope checks and rollback.
```

計画ファイルは UTF-8 without BOM でなければなりません。検証は不正な UTF-8、BOM、replacement character、連続した異常な疑問符、既知の文字化けマーカーを拒否します。
