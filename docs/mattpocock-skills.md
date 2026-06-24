# mattpocock/skills - 実務エンジニア向け Claude Code スキル集

> [mattpocock/skills](https://github.com/mattpocock/skills) は、TypeScript 教育者として知られる **Matt Pocock** 氏が公開している、コーディングエージェント向けのスキル集です。「実際のエンジニアリング現場で AI エージェントを使うと起きる失敗」を防ぐことを目的に、**小さく・適応しやすく・組み合わせ可能**なスキルとして設計されています。

## このリポジトリの特徴

- **Claude Code をはじめとするコーディングエージェント**（Claude Agent SDK 互換）向け
- 「AI 支援開発でよく起きる 4 つの失敗モード」を解決するという明確な設計思想
- `skills` CLI（`npx skills`）でインストールでき、対象エージェントを選んで導入
- **ユーザーが `/` で呼び出すスキル**と、**モデルが必要に応じて自動で呼び出すスキル**を区別

> [!NOTE]
> [anthropics/skills](anthropics-skills.md) が「ドキュメント生成・デザインなど汎用タスク」中心なのに対し、こちらは **SDLC（開発プロセス）そのものを改善する**ワークフロー型スキルが中心です。

---

## 設計思想：4 つの失敗モード

Matt 氏は、AI エージェントによる開発で起きがちな問題を 4 つに整理し、それぞれに対応するスキルを用意しています。

| 失敗モード | 内容 | 対応スキル |
|-----------|------|-----------|
| **Misalignment（認識のズレ）** | 開発者の意図とエージェントの理解が食い違う | `/grill-me`・`/grill-with-docs` で着手前に認識を揃える |
| **Excessive Verbosity（冗長さ）** | やり取りが長くなり非効率 | 共通ドメイン言語（`CONTEXT.md`）でトークン効率・一貫性を改善 |
| **Broken Code（壊れたコード）** | 動かない・質の低いコードを生む | 静的型・ブラウザ・自動テストによるフィードバックループ（red-green-refactor） |
| **Architectural Decay（設計の劣化）** | 場当たり的な変更で設計が崩れる | `/to-prd`・`/improve-codebase-architecture` で日々設計に投資 |

---

## インストール方法

```bash
npx skills@latest add mattpocock/skills
```

セットアップ手順：

1. 導入したいスキルと対象エージェントを選択（`setup-matt-pocock-skills` を必ず含める）
2. `/setup-matt-pocock-skills` を実行し、以下を設定：
   - **イシュートラッカー**（GitHub / Linear / ローカルファイル）
   - チケットの **トリアージ用ラベル**
   - **ドキュメントの保存先**

---

## スキル一覧

### 🛠 エンジニアリング

#### ユーザー呼び出し（`/` コマンド）

| スキル | 用途 |
|-------|------|
| **ask-matt** | 状況に応じて最適なスキルへ案内する入口 |
| **grill-with-docs** | 詳細なヒアリングでドメインモデルを構築し、プロジェクト文書を更新 |
| **triage** | イシューをステートマシンで管理するトリアージ |
| **improve-codebase-architecture** | アーキテクチャ改善点を洗い出し HTML レポートで提示 |
| **setup-matt-pocock-skills** | リポジトリ向けにスキル群を初期設定 |
| **to-issues** | 計画を縦割り（vertical slice）の独立したイシューに分解 |
| **to-prd** | 議論を正式な PRD（要件定義書）に整理 |
| **prototype** | 設計検証用の使い捨てプロトタイプを作成 |

#### モデル呼び出し（自動）

| スキル | 用途 |
|-------|------|
| **diagnosing-bugs** | 構造化されたデバッグループで原因を切り分け |
| **tdd** | red-green-refactor のテスト駆動開発 |
| **domain-modeling** | プロジェクトのドメインモデルを構築・洗練 |
| **codebase-design** | 保守しやすいモジュール設計の原則を確立 |

### ⚡ 生産性（Productivity）

#### ユーザー呼び出し

| スキル | 用途 |
|-------|------|
| **grill-me** | 計画や設計について徹底的にヒアリング（認識合わせ） |
| **handoff** | エージェント間の引き継ぎ用にコンパクトな handoff 文書を作成 |
| **teach** | 複数セッションにまたがって新しい概念を教える |
| **writing-great-skills** | 質の高いスキルを書くためのリファレンス |

#### モデル呼び出し

| スキル | 用途 |
|-------|------|
| **grilling** | （自動）深掘りヒアリングのプロセス |

### 🧩 その他（Misc）

| スキル | 用途 |
|-------|------|
| **git-guardrails-claude-code** | 危険な git コマンドをブロックするガードレール |
| **migrate-to-shoehorn** | テストアサーションを TypeScript 向けツール（shoehorn）へ移行 |
| **scaffold-exercises** | 構造化された演習ディレクトリを作成 |
| **setup-pre-commit** | lint・テスト付きの pre-commit フックを設定 |

---

## 注目スキルの使いどころ

- **着手前の認識合わせ** — `/grill-me` や `/grill-with-docs` で、実装に入る前にエージェントへ要件を深掘りさせる。手戻りを大きく減らせます。
- **計画 → PRD → イシュー化** — `/to-prd` で要件をまとめ、`/to-issues` で縦割りの独立タスクに分解。エージェントが拾いやすい単位になります。
- **品質を保つ開発ループ** — `tdd` と `diagnosing-bugs` で red-green-refactor を徹底し、壊れたコードを早期に検出。
- **設計の劣化を防ぐ** — `/improve-codebase-architecture` で定期的にアーキテクチャを点検し、HTML レポートで可視化。
- **安全な git 運用** — `git-guardrails-claude-code` で `push --force` などの危険操作をブロック。

---

## 他のスキル集との違い

| | **mattpocock/skills** | **[anthropics/skills](anthropics-skills.md)** | **[superpowers](superpowers.md)** |
|--|----------------------|---------------------|-----------------------|
| 主眼 | 開発プロセス（SDLC）の改善 | 汎用タスク（文書生成・デザイン等） | SDLC スキルフレームワーク |
| 代表スキル | grill-me / to-prd / tdd | docx / pdf / pptx / xlsx | brainstorming / TDD / systematic-debugging |
| インストール | `npx skills add` | `/plugin install` | `/plugin marketplace add` |
| 設計思想 | 4 つの失敗モードへの対処 | 自己完結型ツールキット | 体系的な開発ワークフロー |

> いずれも Claude Code で利用できます。プロセス改善目的なら mattpocock/skills や superpowers、ファイル生成・事務作業なら anthropics/skills が向いています。

---

## 参考リンク

- [mattpocock/skills](https://github.com/mattpocock/skills) — 公式リポジトリ
- [Matt Pocock](https://www.mattpocock.com/) — 著者（Total TypeScript 等で知られる）
- [Claude Code スキル](claude-code-skills.md) — スキルの実行環境
- [Anthropic 公式スキル](anthropics-skills.md) / [superpowers](superpowers.md) — 他のスキル集

---

> **注意**: 本ドキュメントは [mattpocock/skills](https://github.com/mattpocock/skills) の公開情報を元にした日本語解説です。収録スキルや使い方は更新されることがあるため、最新情報は公式リポジトリを確認してください。
