# skills.sh — Agent Skills ディスカバリーサイト

> **対象ツール**: ツール横断（Claude Code・Codex・Cursor・OpenCode ほか 70+ エージェント対応） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-22

> [skills.sh](https://skills.sh/) は、Agent Skills を検索・発見・導入するための公開ポータルサイトです。[vercel-labs/skills](https://github.com/vercel-labs/skills) が提供する `npx skills` CLI と連携しており、個人・企業・コミュニティが公開したスキル集を一元的に参照できます。

## skills.sh とは

| 項目 | 内容 |
|------|------|
| **サイト** | [https://skills.sh/](https://skills.sh/) |
| **CLI** | `npx skills` （[vercel-labs/skills](https://github.com/vercel-labs/skills)） |
| **対応エージェント** | Claude Code、Codex、Cursor、OpenCode、Gemini CLI ほか 70 以上 |
| **スキル形式** | `SKILL.md`（YAML フロントマター + Markdown 指示） |
| **ライセンス** | スキルごとに異なる（MIT が多数） |

Agent Skills とは `SKILL.md` ファイルを核とした、エージェントが動的に読み込む指示セットです。特定ツールへの統合手順、コーディング規約、ワークフロー、外部サービス連携など、エージェントの行動をタスク単位で拡張します。

---

## CLI の基本操作

```powershell
# スキルを検索する
npx skills find react

# リポジトリからスキルをインストールする
npx skills add vercel-labs/agent-skills

# 特定のスキルだけを選んでインストールする
npx skills add mattpocock/skills --skill grill-me --skill to-spec

# インストール済みスキルを確認する
npx skills list

# スキルを更新する
npx skills update

# スキルを削除する
npx skills remove web-design-guidelines
```

### エージェントとスコープを指定してインストール

```powershell
# Claude Code と Cursor にのみインストール
npx skills add vercel-labs/agent-skills -a claude-code -a cursor

# グローバル（全プロジェクト共通）にインストール
npx skills add mattpocock/skills -g

# インストールせず一時利用して Claude Code を起動する
npx skills use vercel-labs/agent-skills --skill web-design-guidelines --agent claude-code
```

### インストール先パス（代表例）

| スコープ | Claude Code | Codex |
|----------|------------|-------|
| プロジェクト | `.claude/skills/` | `.codex/skills/` |
| グローバル | `~/.claude/skills/` | `~/.codex/skills/` |

---

## 用途から選ぶ定番スキル

skills.sh のランキングは短期間で入れ替わります。ここでは**順位ではなく用途**で整理しています。掲載順に意味はありません。インストール数・順位・掲載件数といった変動値は本文に書かないため、「いま何が伸びているか」は [skills.sh](https://skills.sh/) で直接確認してください。

> 各スキルの説明は、**提供元リポジトリの README と `SKILL.md`（2026-08-22 確認）**に基づきます。収録スキルは追加・削除されることがあります。

### 開発プロセスを整える

要件整理から実装・レビューまでの進め方を、エージェントに規律として与えるスキルです。**まとめて導入して流れごと変える**使い方が前提になります。

| 目的 | スキル | 提供元 | 導入 |
|------|-------|-------|------|
| 着手前に要件の抜けを潰す | `grill-me` | mattpocock/skills | `npx skills add mattpocock/skills --skill grill-me` |
| 会話を仕様にして Issue へ出す | `to-spec` | mattpocock/skills | `npx skills add mattpocock/skills --skill to-spec` |
| 仕様を依存関係付きのチケットへ分解する | `to-tickets` | mattpocock/skills | `npx skills add mattpocock/skills --skill to-tickets` |
| 仕様どおりに実装させる（TDD とレビューを内包） | `implement` | mattpocock/skills | `npx skills add mattpocock/skills --skill implement` |
| red-green-refactor を徹底する | `tdd` / `test-driven-development` | mattpocock/skills ／ obra/superpowers | `npx skills add mattpocock/skills --skill tdd` |
| 規約と仕様準拠を分けてレビューする | `code-review` | mattpocock/skills | `npx skills add mattpocock/skills --skill code-review` |
| 1 セッションに収まらない作業を地図にする | `wayfinder` | mattpocock/skills | `npx skills add mattpocock/skills --skill wayfinder` |
| 設計を質問で深掘りしてから実装させる | `brainstorming` | obra/superpowers | `npx skills add obra/superpowers` |
| 推測での修正をやめさせる | `systematic-debugging` | obra/superpowers | `npx skills add obra/superpowers` |

**→ 個々の解説は [mattpocock/skills](mattpocock-skills.md) ／ [superpowers](superpowers.md) を参照**

### Web フロントエンドの品質を上げる

Vercel 公式の [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) は、まとめて導入して必要なものだけ残す使い方が向いています。

```powershell
npx skills add vercel-labs/agent-skills
```

| 目的 | スキル | 内容 |
|------|-------|------|
| React / Next.js の性能を直す | `react-best-practices` | ウォーターフォール排除・バンドルサイズ・再レンダリング最適化を 8 カテゴリで指導 |
| UI のアクセシビリティと UX を監査する | `web-design-guidelines` | aria-label・フォームバリデーション・アニメーション・ダークモードなどを点検 |
| デプロイ済みプロジェクトのコストを下げる | `vercel-optimize` | メトリクスを取得してから、指し示されたルートとファイルだけを調査する |
| 文書の書き方を揃える | `writing-guidelines` | Vercel の文書規約（ボイス・構造・コード例・タイポグラフィ） |
| ページ遷移アニメーションを実装する | `react-view-transitions` | `<ViewTransition>` / `addTransitionType` と App Router 統合 |
| boolean prop の増殖を止める | `composition-patterns` | Compound Components / State Lifting / 内部 Composition |

> 上記のほか、upstream の README では `react-native-guidelines`・`vercel-deploy-claimable` も紹介されています。収録は入れ替わるため、導入時は `npx skills add vercel-labs/agent-skills` の選択画面か[リポジトリ](https://github.com/vercel-labs/agent-skills)で最新の一覧を確認してください。

### 文書・データを扱う

| 目的 | スキル | 提供元 | 導入 |
|------|-------|-------|------|
| Word・PDF・PowerPoint・Excel を生成／編集する | `docx` / `pdf` / `pptx` / `xlsx` | anthropics/skills | `/plugin install document-skills@anthropic-agent-skills` |
| Web 検索・スクレイピング・構造化抽出を足す | Firecrawl 公式プラグイン | Firecrawl | `npx -y firecrawl-cli@latest init --all --browser` |

**→ 文書処理スキルの詳細は [Anthropic 公式スキル](../claude-code/official-skills.md) を参照**

### 選ぶときの注意

- **入れるほど良いわけではありません。** カタログが膨らむとコンテキストを圧迫し、意図しないスキルが選ばれることもあります。使う分だけ有効にしてください
- **導入前に中身を読む。** `SKILL.md` はエージェントの振る舞いを書き換える指示です（[Skill / Plugin のセキュリティ](skill-security.md)）

---

## スキル形式（SKILL.md の構造）

```yaml
---
name: my-skill
description: このスキルが何をするか、いつ使うかを記述する
---
# スキルタイトル

エージェントへの指示をここに書く。

## 手順
1. まず〇〇を確認する
2. 次に〇〇を実行する

## 制約
- 〇〇はしない
- 必ず〇〇を確認してから進む
```

YAML フロントマターに `name` と `description` を設定するだけで、`npx skills` で発見・インストール可能なスキルになります。

---

## 自分でスキルを作る

```powershell
# カレントディレクトリに SKILL.md テンプレートを生成する
npx skills init

# サブディレクトリに新しいスキルを作成する
npx skills init my-custom-skill
```

チームのコーディング規約・デプロイ手順・レビュー基準などを `SKILL.md` に書き、リポジトリで管理することで、チーム全員が同じスキルを使えます。

---

## 他のスキル集との比較

| | **skills.sh 掲載スキル全般** | **[mattpocock/skills](mattpocock-skills.md)** | **[obra/superpowers](superpowers.md)** |
|--|--------------------------|-----------------------------------------------|----------------------------------------|
| 主眼 | 用途別に特化した単機能スキル | 開発プロセス全体を小さなSkillで構成 | SDLCの規律を自動強制するフレームワーク |
| 選び方 | 目的に応じて個別インストール | 開発フロー改善にまとめて導入 | 強制的な規律が必要な場合に導入 |
| カスタマイズ | コピーして自由に改変できる | コピーして改変しやすい | Iron Lawで動作を制約する |

---

## 参考リンク

- [skills.sh](https://skills.sh/) — スキルの検索・発見ポータル
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — `npx skills` CLI リポジトリ
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — Vercel 公式スキル集
- [mattpocock/skills 日本語解説](mattpocock-skills.md) — 実務エンジニア向け開発プロセス Skills
- [obra/superpowers 日本語解説](superpowers.md) — SDLC フレームワーク
- [Anthropic 公式スキル](../claude-code/official-skills.md) — docx / pdf / pptx / xlsx 等の文書作成スキル
- [Skill / Plugin のセキュリティ](skill-security.md) — 導入前に何を確認するか
- [Skills 最新動向](../trends.md) — skills.sh を含む Agent Skills エコシステムの概要

---

> **注意**: 本ページに記載のスキルは、各リポジトリのオーナーが提供するものです。Anthropic・Vercel・OpenAI・GitHub がすべてのスキルの動作やセキュリティを保証するものではありません。導入前に各スキルの内容を必ず確認してください。
