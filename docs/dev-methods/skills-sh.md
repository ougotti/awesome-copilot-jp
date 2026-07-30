# skills.sh — Agent Skills ディスカバリーサイト

> **対象ツール**: ツール横断（Claude Code・Codex・Cursor・OpenCode ほか 70+ エージェント対応） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-30

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

## 注目のスキル集（Top 20）

以下は、[skills.sh](https://skills.sh/) で特に参照数が多く、実務での採用実績も豊富なスキルを 20 個まとめたものです。

### 開発プロセス系

#### 1. grill-me（mattpocock/skills）

計画や設計の意思決定を、分岐が解決するまで質問で詰める。着手前に要件の抜けを防ぐ問答ループ。

```powershell
npx skills add mattpocock/skills --skill grill-me
```

#### 2. to-spec（mattpocock/skills）

現在の会話を仕様書としてまとめ、Issue tracker へ公開する。「話した内容」を「合意した仕様」に変換する。

```powershell
npx skills add mattpocock/skills --skill to-spec
```

#### 3. to-tickets（mattpocock/skills）

仕様を依存関係付きの tracer-bullet 型チケットへ分解する。実装順序と依存グラフを自動生成する。

```powershell
npx skills add mattpocock/skills --skill to-tickets
```

#### 4. implement（mattpocock/skills）

仕様やチケットを実装し、合意した境界で TDD とコードレビューを回す。`tdd` / `code-review` と組み合わせる。

```powershell
npx skills add mattpocock/skills --skill implement
```

#### 5. tdd（mattpocock/skills）

red-green-refactor を垂直スライス単位で進める。TDD サイクルを強制するプロセス規律スキル。

```powershell
npx skills add mattpocock/skills --skill tdd
```

#### 6. code-review（mattpocock/skills）

Standards（コーディング規約）と Spec（仕様準拠）の 2 軸を別々にレビューする。

```powershell
npx skills add mattpocock/skills --skill code-review
```

#### 7. wayfinder（mattpocock/skills）

1 セッションでは収まらない大規模作業を、調査チケットの地図に整理する。長期タスクの羅針盤として機能する。

```powershell
npx skills add mattpocock/skills --skill wayfinder
```

#### 8. brainstorming（obra/superpowers）

設計をソクラテス式の質問で深掘りし、承認なしに実装へ進ませない。superpowers フレームワークのエントリーポイント。

```powershell
npx skills add obra/superpowers
```

#### 9. test-driven-development（obra/superpowers）

RED-GREEN-REFACTOR サイクルを Iron Law（鉄の掟）として強制する。テストなしのコードを書かせない。

#### 10. systematic-debugging（obra/superpowers）

再現→仮説→検証→修正の 4 フェーズでデバッグする。推測での修正を防ぐ体系的アプローチ。

---

### Web 開発系（vercel-labs/agent-skills）

```powershell
# まとめてインストール
npx skills add vercel-labs/agent-skills
```

#### 11. react-best-practices

React / Next.js の性能最適化ルールを 40 以上収録。ウォーターフォール排除・バンドルサイズ削減・再レンダリング最適化を 8 カテゴリで網羅。

#### 12. web-design-guidelines

UI コードのアクセシビリティ・性能・UX を 100 以上のルールで監査。aria-label・フォームバリデーション・アニメーション・ダークモードなど幅広く対応。

#### 13. vercel-optimize

デプロイ済み Vercel プロジェクトのコスト・性能・キャッシュ・Functions 使用状況を監査し、問題箇所をランキング形式でレポートする。

#### 14. writing-guidelines

Vercel の文書作成規約（ボイス・構造・コードサンプル・タイポグラフィ）を 80 以上のルールでレビューする。ドキュメント品質の底上げに使う。

#### 15. react-native-guidelines

React Native / Expo 向けの性能・アーキテクチャ・プラットフォーム別パターンを 16 ルールで解説。FlashList・Reanimated・モノレポ構成に対応。

#### 16. react-view-transitions

React の View Transition API（`<ViewTransition>` / `addTransitionType`）を実装する。ページ遷移・共有要素アニメーション・Next.js App Router 統合まで対応。

#### 17. composition-patterns

boolean prop の増殖を避けるコンポーネント設計（Compound Components / State Lifting / 内部 Composition）を指導する。

#### 18. vercel-deploy-claimable

プロジェクトを Vercel へワンショットでデプロイし、プレビュー URL とクレーム URL を返す。claude.ai や Claude Desktop からの会話デプロイに使う。

---

### ドキュメント作成系（anthropics/skills）

```powershell
# Claude Code プラグイン経由でインストール
/plugin install document-skills@anthropic-agent-skills
```

#### 19. docx / pdf / pptx / xlsx（Anthropic 公式）

Word・PDF・PowerPoint・Excel の生成・編集スキル。Claude.ai の有料プランで提供される文書作成機能のバックエンドとして実用されている。

詳細は [Anthropic 公式スキル](../claude-code/official-skills.md) を参照してください。

---

### Web データ取得系

#### 20. firecrawl-claude-plugin

Web 検索・スクレイピング・クロール・構造化データ抽出を Claude Code へ追加する Firecrawl 公式プラグイン。

```powershell
# Firecrawl CLIでまとめて導入
npx -y firecrawl-cli@latest init --all --browser
```

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
- [Skills 最新動向](../trends.md) — skills.sh を含む Agent Skills エコシステムの概要

---

> **注意**: 本ページに記載のスキルは、各リポジトリのオーナーが提供するものです。Anthropic・Vercel・OpenAI・GitHub がすべてのスキルの動作やセキュリティを保証するものではありません。導入前に各スキルの内容を必ず確認してください。
