<div align="center">

<h1>
  <img src="../assets/architect-wordmark.svg" alt="Architect" width="520" />
</h1>

**コードを速く書くことは難しくありません。難しいのは、そのコードベースを次の百回の変更にも耐えさせることです。**

*巨大モジュール、先回りした抽象化、意図しない破壊的変更に陥ることなく、成長しても整合性を保つコードベースを構築します。*

[![Architect Workflow](https://img.shields.io/static/v1?label=Architect&message=design%20%E2%86%92%20propose%20%E2%86%92%20build&color=111827&style=flat-square)](../skills/architect-design/)
[![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](../LICENSE)
[![Architect Repo](https://img.shields.io/badge/GitHub-open%20repo-181717?style=flat-square)](..)

<br />

**偶然に任せてアーキテクチャを作らない。** &nbsp; **推測で抽象化しない。** &nbsp; **互換性を思い込みで扱わない。**

[Why](#なぜ-architect-なのか) &middot; [Install](#インストール) &middot; [Quick start](#プラグインのクイックスタート) &middot; [Use it correctly](#正しい使い方) &middot; [Example](#利用イメージ) &middot; [Workflow](#ワークフロー) &middot; [Outputs](#成果物)

</div>

<h4 align="center">
  <p>
    <a href="../README.md">English</a> |
    <a href="README_zh-hant.md">&#32321;&#39636;&#20013;&#25991;</a> |
    <a href="README_zh-hans.md">&#31616;&#20307;&#20013;&#25991;</a> |
    <b>&#26085;&#26412;&#35486;</b>
  </p>
</h4>

---

## なぜ Architect なのか

多くの coding agent が失敗するのは、コードを書けないからではありません。

コードを書きながら、構造上の意思決定を黙って進めてしまうからです。

一見すると普通の依頼でも、

```text
2 つ目の決済プロバイダを追加する。
このサービスをリファクタリングする。
この機能を拡張可能にする。
```

すでに所有権、境界、互換性、失敗時の挙動、状態遷移、移行、ロールバックに関する判断を迫っています。

こうした判断が暗黙のままだと、コードベースはたいてい次の 3 つの高コストな状態のどれかに流れていきます。

| Failure | What happens |
| --- | --- |
| **Architecture by neglect** | 機能は一番近いファイルに押し込まれます。責務の所在が曖昧になり、ルールが重複し、1 つか 2 つのモジュールがすべてを吸い込みます。 |
| **Architecture by speculation** | 実際の変化点が存在しないうちから、あり得る未来のためにインターフェース、ファクトリ、レジストリ、イベント層、継承層が作られます。 |
| **Compatibility by assumption** | 意図した境界を明示しないまま、既存の挙動が守られることも壊されることも前提扱いされます。 |

Architect は、コードベースがその代償を払う前に、そうした判断を必ず表に出させるために存在します。

---

## インストール

### プラグイン

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

インストール後は新しいセッションを開始してください。そうしないと agent がプラグインを認識できません。

### スタンドアロンスキル

```text
npx skills add vortezwohl/Architect
```

または `skills/` を利用中ツールの対応 skills ディレクトリにコピーし、各段階を手動で呼び出します。

```text
$architect-design
$architect-propose <plan-name>
$architect-build <plan-name>
```

> [!IMPORTANT]
> インストール前に skill を読んでください。これらの skill には、実行ルール、パッケージ契約、段階境界が埋め込まれています。

> [!TIP]
> インストール後にすぐ命令が見えない場合は、まず新しいセッションを開始してください。

---

## プラグインのクイックスタート

インストール後、**3 つのプラグインコマンド**が見えるはずです。

- `design`
- `propose`
- `build`

これをウィザードのように使ってください。前の段階が終わってから次を押します。

> [!TIP]
> ほとんどの人にとって最速の始め方は単純です。まず `design` を押し、やりたい変更を 1 文で書き、その同じ名前で `propose` と `build` まで進めます。

### Step 1: Design

最初に使うのはこれです。

Architect に何を変えたいか伝えてください。

```text
$architect-design Add a second payment provider without breaking checkout.
```

```text
/architect:design Add a second payment provider without breaking checkout.
```

得られるもの：

- 承認済みの設計バンドル 1 つ
- 明確な境界
- まだコーディングは始めないこと

### Step 2: Propose

設計が承認された後に使います。

変更に短いプラン名を付けてください。

```text
$architect-propose add-payment-provider
```

```text
/architect:propose add-payment-provider
```

得られるもの：

- 封印済みの `.architect/add-payment-provider/` パッケージ 1 つ
- タスクファイル
- 検証計画
- 実行ログ

### Step 3: Build

プランパッケージが存在する状態で使います。

同じプラン名をそのまま使ってください。

```text
$architect-build add-payment-provider
```

```text
/architect:build add-payment-provider
```

起きること：

- Architect が記録済みタスクを順番に実行する
- 状態とログを更新する
- 承認済み境界の内側に作業を保つ

### どれを押せばいい？

- 新しい変更: `design`
- 設計は承認済みで、まだプランがない: `propose`
- プラン作成済み: `build`

### 1 つだけ守ること

いきなり `build` に飛ばないでください。

Architect の要点は次の順番です。

```text
design -> propose -> build
```

---

## 正しい使い方

段階を順番に使ってください。

1. `architect-design` は、承認済み設計バンドルが必要なときだけ実行します。
2. `architect-propose` は、そのバンドルが承認された後にだけ実行します。
3. `architect-build` は、生成されたパッケージが封印され、検証された後にだけ実行します。

大きな依頼から直接 `architect-build` へ飛ばないでください。このリポジトリは、承認済み設計、封印済み計画、境界付き実行の分離を前提に構築されています。

> [!IMPORTANT]
> Architect は意図的に手動フローです。次の段階を勝手に推測するためのものではありません。

---

## 利用イメージ

```text
User:
現在のチェックアウトフローを壊さずに、2 つ目の決済プロバイダを追加する。
```

```text
Stage 1: $architect-design
- まずリポジトリを読む。
- どの互換性を維持すべきか確認する。
- 実証済みの変化点と安定した方針を分離する。
- 承認済みの D-xxx サブデザインを作る。
```

```text
Stage 2: $architect-propose add-payment-provider
- .architect/add-payment-provider/ を作成する。
- リポジトリのスクリプトで設計文書とタスク文書を割り当てる。
- パッケージを封印して検証する。
```

```text
Stage 3: $architect-build add-payment-provider
- 封印済みパッケージと現在の実行状態を読み込む。
- 記録された T-xxx タスクを順に実行する。
- 実際の結果で実行ログを更新する。
```

違いは明快です。

- 通常の coding agent はすぐに実装を始め、アーキテクチャ上の判断を diff の中に隠します。
- Architect は、その判断を明示し、承認可能にし、直列化し、実行可能にします。

---

## ワークフロー

Architect は厳格な**手動の 3 段階フロー**です。

```text
architect-design -> architect-propose -> architect-build
```

各段階には独立した責務があり、自動で次の段階の仕事を引き受けることはありません。

| Stage | Invoke when | Produces | Refuses to do |
| --- | --- | --- | --- |
| `architect-design` | 影響の大きい変更に対して、承認済みのアーキテクチャ方針を 1 つ定めたいとき。 | 1 つ以上の `D-xxx` サブデザインを含む、承認済みの設計バンドル。 | 計画化、ファイル書き込み、実装。 |
| `architect-propose` | 設計バンドルがすでに承認され、実行可能なパッケージに変換する必要があるとき。 | `D-xxx`、`T-xxx`、状態、ログ成果物を含む、封印済みの `.architect/<plan-name>/` パッケージ。 | 解決策の再設計やアプリコードの編集。 |
| `architect-build` | 封印済みパッケージが検証を終え、実行準備ができているとき。 | 実際の実装進行、タスク状態更新、事実ベースの実行ログ。 | 設計の再オープンや、ビルド途中での新しい構造の持ち込み。 |

ここがユーザー体験の核心です。agent は依頼から直接コードへ飛びません。まず、設計承認、計画の封印、境界付きの実行を切り分けなければなりません。

---

## 成果物

### 1. 承認済み設計バンドル

`architect-design` は、将来の 1 つの計画パッケージに対して 1 つの承認済みバンドルを生成します。

各バンドルには複数の `D-xxx` サブデザインを含めることができ、意図、境界、反例、アンチパターン、`MUST DO` / `MUST NOT DO` ルールを明示します。

### 2. 封印済み実行パッケージ

`architect-propose` は、その承認済みバンドルを次の場所にある決定的なパッケージへ変換します。

```text
.architect/<plan-name>/
```

パッケージには次が含まれます。

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

これは単なるメモではありません。ビルド段階の実行契約です。

### 3. チェックポイント制御されたビルド証跡

`architect-build` は封印された `T-xxx` タスクを順番に実行し、タスク状態を正直に更新し、事実ベースのログを追記し、実装を承認済み境界の内側に保ちます。

得られるのはコードだけではありません。なぜそのコードが変わったのか、実際に何が起きたのかを説明できる、意思決定の軌跡、状態の軌跡、実行の軌跡も得られます。

---

## リポジトリ構成

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

公開されている製品名は **Architect** です。

呼び出せる 3 つの段階は `architect-design`、`architect-propose`、`architect-build` です。

---

## コントリビュート

コントリビューションは、このワークフローを強くするものであるべきで、ノイズを増やすものであってはいけません。

よい変更は、たいてい次のどれかを改善します。

- 設計段階の証拠ゲート。
- 互換性境界の明確さ。
- 封印済みパッケージの決定性。
- ビルド段階の実行規律。
- ロールバック、検証、ログ記録の正確さ。

これらの性質をどれも改善しないまま手順だけを増やす変更は、おそらく誤った変更です。

---

## ライセンス

MIT。詳細は [LICENSE](../LICENSE) を参照してください。
