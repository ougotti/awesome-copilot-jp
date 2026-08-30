# Claude Code のカスタマイズ機能

> **対象ツール**: Claude Code ｜ **実行環境**: CLI（ターミナル/デスクトップ） / Chat UI（Web） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-30

Claude Code を「自分たちのやり方」に合わせるための仕組みを解説します。**どの仕組みをいつ使うか**の判断を先に示し、その後で各仕組みの設定方法を説明します。

> 変化の速いコマンド一覧（組み込みスラッシュコマンド、キーボードショートカット）は [コマンド一覧（付録）](commands.md) に分離しています。正確な最新版は必ず [公式リファレンス](https://code.claude.com/docs/en/interactive-mode) を確認してください。

---

## 導入の順番

はじめて導入するなら、**この順に 1 つずつ**進めるのが確実です。いきなり全部を設定する必要はありません。

| 順番 | やること | 効果 | 目安 |
|-----|---------|------|------|
| **1** | `CLAUDE.md` を置く | プロジェクトの前提・規約・コマンドを毎回説明しなくてよくなる | 数分（`/init` で雛形生成） |
| **2** | Skill を 1 つ作る | 繰り返す作業手順を、必要なときに自動で適用させる | 30 分程度 |
| **3** | Plugin にまとめる | チーム・他プロジェクトへ配布し、更新を追える形にする | 標準化したくなってから |

まず `CLAUDE.md` だけでも、毎回の説明コストは大きく減ります。Skill・Plugin は「同じ指示を 3 回書いた」と感じてから着手すれば十分です。

---

## どの仕組みを使うか

Claude Code には目的の近い仕組みが複数あります。**やりたいことから逆引き**してください。

| やりたいこと | 選ぶ仕組み | 起動のしかた |
|------------|-----------|------------|
| プロジェクトの前提を常に効かせたい | [CLAUDE.md](#claudemd) | 常時（自動で読まれる） |
| 作業知識・手順を、必要なときに自動適用したい | [Agent Skills](#agent-skills) | 自動（内容に応じて選択）／ `/skill-name` で手動も可 |
| 手動で呼ぶ定型処理を用意したい | [カスタムスラッシュコマンド](#カスタムスラッシュコマンド) | `/コマンド名` |
| 役割を分離して並行作業させたい | [サブエージェント](#サブエージェント) | メインの会話から委譲 |
| 複数の機能をまとめて配布したい | [プラグイン](#プラグイン) | インストール後は常時有効 |
| 特定イベントで必ず処理を挟みたい | [フック](#フック) | イベント発火時に自動 |
| 外部サービス・DB へ接続したい | [MCP](#mcpmodel-context-protocol統合) | ツールとして随時 |

> **Skill と Custom Command の関係**: `.claude/commands/` のカスタムコマンドは引き続き動作し、同じフロントマターに対応しています。ただし公式は、補助ファイルを同梱できるなど機能が多い **Skill を推奨**しています。新しく作るなら Skill から検討してください。

---

## CLAUDE.md

`CLAUDE.md` は Claude Code がプロジェクトを読み込むときに自動的に参照するコンテキストファイルです。チームのルール、コマンド、アーキテクチャ上の制約を記述しておきます。

### 配置場所

| パス | スコープ |
|-----|---------|
| `CLAUDE.md`（リポジトリルート） | プロジェクト全員に適用 |
| `~/.claude/CLAUDE.md` | 個人設定（全プロジェクト共通） |
| サブディレクトリの `CLAUDE.md` | そのディレクトリ配下に適用 |

### 記述例

```markdown
# プロジェクト: MyApp

## 技術スタック
- バックエンド: Node.js + TypeScript + Express
- データベース: PostgreSQL（ORM は Prisma）
- テスト: Vitest + Playwright

## よく使うコマンド
- `npm run dev` — 開発サーバー起動
- `npm test` — ユニットテスト実行
- `npm run db:migrate` — DB マイグレーション

## コーディング規約
- 関数コンポーネントのみ使用（クラスコンポーネント禁止）
- エラーハンドリングは必ず `Result` 型で包む
- コミットメッセージは Conventional Commits 形式

## 注意事項
- `src/legacy/` は触らない（移行対象外）
- 環境変数は `.env.example` に追加すること
```

既存のコードベースから雛形を生成するには、Claude Code 内で `/init` を実行します。

---

## Agent Skills

Agent Skills は、タスク内容に応じて**必要なときに読み込まれる**再利用可能な能力パッケージです。手順・判断基準・補助ファイルをひとまとめにできます。

### 配置場所

```
.claude/
  skills/
    my-skill/
      SKILL.md        # エントリーポイント
      reference.md    # 補助ファイル（任意）
      scripts/        # 実行スクリプト（任意）
```

| パス | スコープ |
|-----|---------|
| `.claude/skills/` | プロジェクト共有（リポジトリにコミット） |
| `~/.claude/skills/` | 個人用（ローカルの全プロジェクト） |

### 呼び出しの制御

フロントマターで、自動適用するか手動専用にするかを指定できます。

| フロントマター | 効果 |
|--------------|------|
| `description` | この記述をもとに、Claude が使うべき場面を判断する（自動選択の根拠） |
| `disable-model-invocation: true` | 自動起動を止め、`/skill-name` の手動呼び出し専用にする |
| `context: fork` | そのスキルを独立したサブエージェントのコンテキストで実行する |

### 実行環境による違い

| 環境 | `.claude/skills/`（プロジェクト） | `~/.claude/skills/`（個人） |
|------|--------------------------------|---------------------------|
| ローカルの CLI・デスクトップ | 読み込まれる | 読み込まれる |
| クラウドセッション | 読み込まれる（クローンしたリポジトリのもの） | **読み込まれない** |
| Cowork セッション | — | **読み込まれない**（claude.ai アカウントで有効化したスキルを使う） |

> 個人用ディレクトリにだけ置いたスキルは、クラウド／Cowork セッションでは「見つからない」と報告されます。これらの環境でも使いたい場合は、リポジトリの `.claude/skills/` にコミットするか、Plugin として配布してください。

---

## カスタムスラッシュコマンド

`.claude/commands/` に Markdown ファイルを置くと、独自のスラッシュコマンドになります。手動で呼ぶ定型処理に向いています。

```
.claude/
  commands/
    generate-tests.md       # /generate-tests になる
    create-pr.md            # /create-pr になる
```

プロジェクトルートの `.claude/commands/` はリポジトリ全員で共有され、`~/.claude/commands/` は個人専用です。

### 記述例

```markdown
---
description: 現在のブランチのテストを生成して実行する
---

以下の手順でテストを生成・実行してください：

1. `$ARGUMENTS` に指定されたファイルを確認する
2. 既存のテストパターンに従ってユニットテストを生成する
3. `npm test` でテストを実行して結果を報告する
```

`/generate-tests src/utils.ts` のように引数を渡して呼び出します。

| 記法 | 意味 |
|-----|------|
| `$ARGUMENTS` | コマンド呼び出し時に渡した引数が展開される |
| `!コマンド` | シェルコマンドを実行してその結果を使用する（例: `!git status`） |

---

## サブエージェント

サブエージェントは、特定役割に特化したエージェント定義です。メインの会話から切り離して動かすため、役割ごとに観点を分けたいときに使います。

```
.claude/
  agents/
    reviewer.md
    migration-helper.md
```

| パス | スコープ |
|-----|---------|
| `.claude/agents/` | プロジェクト共有 |
| `~/.claude/agents/` | 個人用 |

レビュー専用・ドキュメント更新専用のように役割を分けると、大きなタスクを担当ごとの観点で進められます。

> **2026-08 の変更**: サブエージェントの **fork が既定で有効**になりました（2.1.232）。`subagent_type: "fork"` のサブエージェントは親の会話とプロンプトキャッシュをそのまま引き継ぎ、対話セッションでのエージェント起動は既定でバックグラウンド実行になります。会話の続きを別観点で走らせたいときは、役割定義を書き起こすより fork のほうが速いことがあります。

---

## プラグイン

Skill・コマンド・サブエージェント・フック・MCP 設定をまとめて配布・更新する単位です。マーケットプレイス（配布元の Git リポジトリ）を追加してインストールします。

| コマンド | 概要 |
|---------|------|
| `/plugin marketplace add <source>` | 配布元マーケットプレイスを追加 |
| `/plugin install <plugin>@<marketplace>` | プラグインをインストール |
| `/plugin` | インストール済みプラグインの確認・管理 |

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

> GitHub Copilot 側の Plugin との違い（含められる要素、Marketplace の扱い、組織での強制方法）は [GitHub Copilot Plugins](../copilot/plugins.md#claude-code-の-plugin-marketplace-との比較) の比較表を参照してください。

### 配布元と検証（2026-08 時点）

| 項目 | 内容 |
|------|------|
| **GitLab の Marketplace** | `gitlab.com` のリポジトリ URL（nested subgroup を含む）を GitHub と同じように clone できる（2.1.232）。clone の認証に失敗したときのヒントも、実際の git ホスト名で表示される |
| **`claude plugin validate`** | `.claude/skills` だけを持つプラグインも検査対象になり、frontmatter の解析に失敗する `SKILL.md` を報告する（2.1.233）。公開前の自己点検に使える |
| **`headersHelper`** | url 形式の Marketplace やカタログエントリが、短命トークンなどの HTTP ヘッダーを生成するコマンドを実行できる（2.1.238）。実行前にコマンドが表示されて `[y/N]` の確認が入り、フォルダ信頼の受諾が必須で、資格情報の環境変数は継承されない |

> バージョン番号は 2026-08 時点のスナップショットです。最新は [Claude Code の CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) を確認してください。

### Agent Plugins 1.0.0 との関係

2026 年 8 月に、Amazon・Anysphere（Cursor）・Microsoft・OpenAI・Vercel によるマルチベンダー共通仕様 **Agent Plugins 1.0.0** が公開され、GitHub Copilot・Cursor・Codex などが対応しました。一方 **Claude Code は現時点で対応を表明しておらず**、上記の `/plugin` はこれまでどおり Claude Code 独自形式のままです。共通仕様側が標準化しているのは Skills と MCP サーバーの 2 つだけなので、可搬性が要るなら **プラグイン単位ではなく `SKILL.md` 単位で共有する**ほうが現実的です。

**→ 仕様の中身と各ツールの対応状況は [Skills 最新動向 8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準) を参照**

---

## フック

Hooks は、Claude Code の特定イベントで自動実行されるシェルコマンドです。Skill と違って **Claude の判断を挟まず必ず実行される**ため、ガードレールや記録に向いています。

### 利用可能なイベント

| イベント | タイミング | 活用例 |
|---------|-----------|-------|
| `PreToolUse` | ツール実行前 | 危険なコマンドのブロック、ログ記録 |
| `PostToolUse` | ツール実行後 | テスト自動実行、フォーマット適用 |
| `PostToolUseBackground` | ツール実行後（非同期） | 重い分析処理、通知送信 |
| `Notification` | Claude からの通知時 | デスクトップ通知、Slack 通知 |
| `Stop` | セッション終了時 | 作業ログの記録、自動コミット |
| `PreCompact` | コンテキスト圧縮前 | 重要な情報の保存 |

### 設定方法

`.claude/settings.json`（プロジェクト）または `~/.claude/settings.json`（ユーザー）に記述します。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "scripts/check-dangerous-command.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "scripts/auto-commit.sh" }
        ]
      }
    ]
  }
}
```

### 例: 危険なコマンドをブロックする（PreToolUse）

```bash
#!/bin/bash
# scripts/check-dangerous-command.sh

COMMAND=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+-rf|git\s+push\s+--force|DROP\s+TABLE'; then
  echo "危険なコマンドが検出されました: $COMMAND" >&2
  exit 2  # exit 2 でブロック
fi
```

### 例: セッション終了時に自動コミットする（Stop）

```bash
#!/bin/bash
# scripts/auto-commit.sh

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chore: auto-commit by Claude Code session"
fi
```

---

## 組織での統制 — 導入前・推論前・実行後

Claude Enterprise では、Skill や Plugin の「入れる前の確認」に加えて、**推論の直前**と**実行の後**にも統制をかけられます。3 つの段階の考え方は [Skill / Plugin のセキュリティ 5 節](../dev-methods/skill-security.md#5-統制が効く-3-つの段階) にまとめています。ここでは Claude 側の設定と利用条件を扱います。

| 段階 | 機能 | 状態 | 何ができるか |
|------|------|------|-------------|
| 導入前 | Skill / Plugin のセキュリティスキャン | Beta（Enterprise プラン、2026-08-06） | 第三者製の Skill・Plugin を、**アップロードまたは編集された時点**で悪意ある内容がないか自動検査する |
| 推論前 | Inference hooks | Beta（Claude Enterprise、2026-08-05） | 組織の AI セキュリティサーバーを指定すると、**claude.ai・Cowork・Claude Code の対象プロンプトが、サーバーの allow / deny 判定が返るまで推論に進まない**。リクエストは署名され、失敗時の挙動は設定可能。**拒否はすべて Activity Feed に記録される** |
| 実行後 | Compliance API のセッション取得 | 利用者のマシン上のセッション取得は 2026-08-26 に**ベータを終了**（Cowork / Claude Code） | 組織横断でセッションを一覧し、個別セッションのメタデータとトランスクリプトを取得する。既存の Compliance Access Key と `read:compliance_user_data` スコープを使う |

### 導入時に確認すること

- **いずれも Enterprise 向け**です。個人・チームプランでは使えません
- **Inference hooks は自組織でセキュリティサーバーを用意する前提**です。判定サーバーが落ちたときの挙動（通すのか止めるのか）を設定で決めておく必要があります
- Compliance API で取得できるのは**利用者のマシン上で動いたセッションを含みます**。監査の範囲と、従業員への周知の要否を法務・人事と確認してください

> 3 つとも「入れてよい Skill か」を人が読む作業を置き換えるものではありません。**スキャンは既知の悪意を検出する仕組み**であり、[導入前に中身を読む](../dev-methods/skill-security.md#2-導入前に何を確認するか)必要は変わりません。

---

## 設定ファイル（settings.json）

`.claude/settings.json`（プロジェクト）または `~/.claude/settings.json`（ユーザー）で動作を制御します。

```json
{
  "model": "opus",
  "permissions": {
    "allow": ["Bash(npm run *)", "Bash(git *)", "Edit", "Read"],
    "deny": ["Bash(rm -rf *)", "Bash(git push --force)"]
  },
  "hooks": { "PreToolUse": [], "Stop": [] },
  "env": { "NODE_ENV": "development" }
}
```

### パーミッションの書き方

`allow` / `deny` にツール名やコマンドパターンを指定すると、確認プロンプトなしに実行を許可・拒否できます。

| 書き方 | 意味 |
|-------|------|
| `"Bash"` | すべての Bash コマンドを許可 |
| `"Bash(npm run *)"` | `npm run` で始まるコマンドのみ許可 |
| `"Edit"` | ファイル編集を許可 |
| `"Read"` | ファイル読み取りを許可 |
| `"mcp__github__*"` | GitHub MCP ツールをすべて許可 |

---

## MCP（Model Context Protocol）統合

MCP サーバーを設定すると、ブラウザ操作・データベース接続・外部 API 連携などの能力を追加できます。

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    }
  }
}
```

### よく使われる MCP サーバー

| サーバー | 機能 | 用途 |
|---------|------|------|
| `server-github` | GitHub API 操作 | Issue/PR 管理、リポジトリ操作 |
| `server-filesystem` | ファイルシステム操作 | 制限付きでファイルアクセス |
| `server-postgres` | PostgreSQL 接続 | DB 直接操作・クエリ実行 |
| `server-puppeteer` | ブラウザ自動化 | Web スクレイピング、E2E テスト |
| `server-slack` | Slack API | メッセージ送受信、チャンネル操作 |

> MCP サーバーは外部へ接続し、認証情報を扱います。導入前に接続先と権限範囲を確認してください。

---

## セットアップ

```bash
# インストール
npm install -g @anthropic-ai/claude-code

# 起動して CLAUDE.md を生成
claude
/init
```

チームで共有する構成の例です。

```
.claude/
  skills/
    release-checklist/
      SKILL.md         # 必要なときに自動適用される手順
  commands/
    create-pr.md       # /create-pr（手動で呼ぶ定型処理）
  settings.json        # パーミッション・フック
CLAUDE.md              # プロジェクトの前提・規約
```

---

## 関連ドキュメント

- [コマンド一覧（付録）](commands.md) — 組み込みスラッシュコマンドとキーボードショートカットのスナップショット
- [Anthropic 公式スキル](official-skills.md) — docx / pdf / pptx / xlsx などの公式スキル
- [GitHub Copilot Plugins](../copilot/plugins.md) — Copilot 側の Plugin との比較
- [mattpocock/skills](../dev-methods/mattpocock-skills.md) ／ [superpowers](../dev-methods/superpowers.md) — 開発プロセス改善スキル

## 参考リンク

- [Claude Code 公式ドキュメント](https://code.claude.com/docs/) — 機能説明・セットアップガイド（**一次情報**）
- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands) — Agent Skills の作成と運用
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode) — キーボードショートカット・対話機能のリファレンス
- [CLI reference](https://code.claude.com/docs/en/cli-reference) — CLI の起動オプション
- [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks) — 推論前の allow / deny 判定（公式）
- [Compliance API — Retrieve session transcripts](https://platform.claude.com/docs/en/manage-claude/compliance-sessions) — セッションのトランスクリプト取得（公式）
- [Claude apps release notes](https://support.claude.com/en/articles/12138966-release-notes) — Skill / Plugin セキュリティスキャンの提供状況（公式）
- [MCP 公式サイト](https://modelcontextprotocol.io/) — Model Context Protocol の仕様
- [MCP サーバー一覧](https://github.com/modelcontextprotocol/servers) — 公式・コミュニティ MCP サーバー
