# Claude Code スキル一覧と活用ガイド

> **対象ツール**: Claude Code ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-29

> [Claude Code](https://docs.anthropic.com/ja/docs/claude-code/overview) は Anthropic が提供するコーディング支援 CLI ツールです。スラッシュコマンド、カスタムコマンド、フック、MCP 連携などの仕組みで作業を自動化・効率化できます。

## Claude Code とは

Claude Code は、ターミナルから直接使えるコーディングエージェントです。コードの読み取り・編集・実行はもちろん、Git 操作や GitHub との連携も行えます。GitHub Copilot が IDE 内のインライン補完に特化しているのに対し、Claude Code はファイルシステム全体を横断する複雑なタスクをこなせるエージェントとして設計されています。

---

## スラッシュコマンド（組み込み）

Claude Code には最初から使えるスラッシュコマンドが組み込まれています。チャット入力欄で `/` に続けてコマンド名を入力するだけで呼び出せます。

### プロジェクト初期化・設定

| コマンド | 概要 | 活用場面 |
|---------|------|---------|
| `/init` | `CLAUDE.md` を自動生成してプロジェクトの構成を記録 | 新規リポジトリへの Claude Code 導入時 |
| `/config` | モデル、テーマ、言語などの設定を変更 | 初期セットアップ、好みのカスタマイズ |
| `/model` | 使用する Claude モデルを切り替え | タスクに応じてモデルを使い分け |
| `/settings` | 設定ファイルの内容を確認・編集 | パーミッションやフックの調整 |
| `/permissions` | ツールの許可・拒否設定を管理 | 自動実行を許可するコマンドを制御 |

### レビュー・品質管理

| コマンド | 概要 | 活用場面 |
|---------|------|---------|
| `/review` | 現在のブランチの PR をレビュー | コードレビューの効率化 |
| `/pr-comments` | PR に付いたコメントを取得して対応 | レビュー指摘への返答・修正 |

### メモリ・コンテキスト管理

| コマンド | 概要 | 活用場面 |
|---------|------|---------|
| `/memory` | プロジェクトや個人レベルのメモリを確認・追加 | セッションをまたいだ情報の保持 |
| `/compact` | 会話履歴を要約してコンテキストを節約 | 長いセッションでの速度改善 |

### 診断・ユーティリティ

| コマンド | 概要 | 活用場面 |
|---------|------|---------|
| `/doctor` | Claude Code の環境・設定を診断 | インストール後のセットアップ確認 |
| `/cost` | 現在のセッションの API 使用コストを表示 | 費用の確認・管理 |
| `/status` | ツールの接続状態とモデル情報を表示 | MCP サーバーの疎通確認 |
| `/mcp` | MCP サーバーの一覧・管理 | 外部ツール連携の確認 |
| `/help` | コマンド一覧とヘルプを表示 | 使い方がわからないとき |
| `/clear` | 会話履歴をリセット | 新しいタスクに切り替えるとき |

### エディタ連携

| コマンド | 概要 | 活用場面 |
|---------|------|---------|
| `/vim` | Vim キーバインドの有効化・無効化 | Vim ユーザーの操作性改善 |
| `/terminal-setup` | ターミナルへの Shift+Enter キーバインド設定 | 複数行入力の利便性向上 |
| `/release-notes` | Claude Code の最新リリースノートを表示 | アップデート内容の確認 |

---

## クラウドスキル（`/` コマンド）

Claude Code on the Web（ブラウザ版・モバイル版）では、以下の組み込みスキルをスラッシュコマンドで呼び出せます。これらはシングルコマンドで複雑な処理を自動実行するエージェント型のスキルです。

### 開発ワークフロー

| スキル | コマンド例 | 概要 |
|-------|-----------|------|
| **init** | `/init` | `CLAUDE.md` をコードベースのドキュメントとして自動生成 |
| **run** | `/run` | プロジェクトのアプリを起動して実際の動作を確認 |
| **verify** | `/verify` | コード変更が意図通りに動作するかアプリを実行して検証 |

### コードレビュー・品質

| スキル | コマンド例 | 概要 |
|-------|-----------|------|
| **code-review** | `/code-review` | 現在の差分を正確性・効率性の観点でレビュー |
| **code-review (high)** | `/code-review high` | より広い範囲をカバーする詳細レビュー |
| **code-review (ultra)** | `/code-review ultra` | クラウドで複数エージェントが並行実行するディープレビュー |
| **code-review (--comment)** | `/code-review --comment` | レビュー結果を PR のインラインコメントとして投稿 |
| **code-review (--fix)** | `/code-review --fix` | レビュー結果を自動で修正として適用 |
| **simplify** | `/simplify` | 差分を確認して簡潔化・クリーンアップを自動適用 |
| **review** | `/review` | プルリクエスト全体をレビュー |
| **security-review** | `/security-review` | セキュリティの観点で差分を詳細レビュー |

### 設定・パーミッション

| スキル | コマンド例 | 概要 |
|-------|-----------|------|
| **update-config** | `/update-config` | `settings.json` でハーネスの設定を更新 |
| **fewer-permission-prompts** | `/fewer-permission-prompts` | 許可リストを追加して権限確認のプロンプトを減らす |
| **keybindings-help** | `/keybindings-help` | キーボードショートカットのカスタマイズ支援 |
| **session-start-hook** | `/session-start-hook` | セッション開始時のフック（SessionStart hook）を設定 |

### API 開発・自動化

| スキル | コマンド例 | 概要 |
|-------|-----------|------|
| **claude-api** | `/claude-api` | Claude API / Anthropic SDK を使ったアプリの構築・デバッグ |
| **loop** | `/loop 5m /code-review` | 指定間隔でコマンドを繰り返し実行（例: 5 分ごと） |

---

## Agent Skills（`.claude/skills`）

Agent Skills は、Claude Code がタスク内容に応じて自動的に読み込む再利用可能なスキル定義です。カスタムスラッシュコマンドが「手動で呼び出すコマンド」なのに対し、Agent Skills は「必要なときに自動適用される能力パッケージ」として使えます。

### 配置場所と構成

```
.claude/
  skills/
    my-skill/
      SKILL.md
```

- プロジェクト共有: `.claude/skills/`
- 個人用（全プロジェクト共通）: `~/.claude/skills/`
- 各スキルは `SKILL.md` をエントリーポイントとして持ちます

### 使いどころ

- 繰り返し発生する実装・レビュー手順の標準化
- チーム固有のルールやチェック観点の再利用
- 特定ドメイン（例: テスト生成、移行作業、ドキュメント更新）の作業品質の平準化

---

## プラグインとマーケットプレイス

Claude Code では、コミュニティや公式が公開しているスキル群・拡張をプラグインとして導入できます。`anthropics/skills` や `mattpocock/skills` のような配布元を追加して、必要な機能をインストールする流れです。

### よく使うコマンド

| コマンド | 概要 |
|---------|------|
| `/plugin marketplace add <source>` | マーケットプレイスの配布元を追加 |
| `/plugin install <plugin>` | プラグインをインストール |
| `/plugin` | インストール済みプラグインの確認・管理 |

### 例

```text
/plugin marketplace add anthropics/skills
/plugin install anthropics/skills
```

---

## サブエージェント（`.claude/agents`）

サブエージェントは、特定役割に特化したカスタムエージェント定義です。Copilot 側の Agents と同様に、役割を分けて複雑な作業を進めたいときに有効です。

### 配置場所

```
.claude/
  agents/
    reviewer.md
    migration-helper.md
```

- プロジェクト共有: `.claude/agents/`
- 個人用（全プロジェクト共通）: `~/.claude/agents/`

### 使いどころ

- レビュー専用、ドキュメント更新専用などの役割分離
- 大きなタスクを分割し、担当ごとの観点で品質を担保
- チーム内で「この役割はこのエージェントを使う」という運用の定着

---

## カスタムスラッシュコマンド

`.claude/commands/` ディレクトリに Markdown ファイルを置くことで、独自のスラッシュコマンドを作成できます。チームで共有する定型タスクをコマンド化するのに最適です。

### ディレクトリ構成

```
.claude/
  commands/
    generate-tests.md       # /generate-tests コマンドになる
    create-pr.md            # /create-pr コマンドになる
    deploy-checklist.md     # /deploy-checklist コマンドになる
```

プロジェクトルートの `.claude/commands/` はリポジトリ全員で共有されます。個人専用のコマンドは `~/.claude/commands/` に配置します。

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

Claude Code で `/generate-tests src/utils.ts` のように引数を渡して呼び出します。

### 特殊記法

| 記法 | 意味 |
|-----|------|
| `$ARGUMENTS` | コマンド呼び出し時に渡した引数が展開される |
| `!コマンド` | シェルコマンドを実行してその結果を使用する（例: `!git status`） |

---

## フック（Hooks）

Hooks は、Claude Code の特定イベントをトリガーとして自動実行されるシェルコマンドです。GitHub Copilot の Hooks と同様の概念ですが、Claude Code 固有のイベントに対応しています。

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

`.claude/settings.json` または `~/.claude/settings.json` でフックを設定します。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "scripts/check-dangerous-command.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "scripts/auto-commit.sh"
          }
        ]
      }
    ]
  }
}
```

### フックの活用例

#### 危険なコマンドのブロック（PreToolUse）

`rm -rf` や `git push --force` などのコマンドを実行前にインターセプトして確認します。

```bash
#!/bin/bash
# scripts/check-dangerous-command.sh

COMMAND=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.command // ""')

if echo "$COMMAND" | grep -qE 'rm\s+-rf|git\s+push\s+--force|DROP\s+TABLE'; then
  echo "危険なコマンドが検出されました: $COMMAND" >&2
  exit 2  # exit 2 でブロック
fi
```

#### セッション終了時に自動コミット（Stop）

```bash
#!/bin/bash
# scripts/auto-commit.sh

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "chore: auto-commit by Claude Code session"
fi
```

#### ツール実行後にテストを自動実行（PostToolUse）

```bash
#!/bin/bash
# scripts/run-tests-after-edit.sh

TOOL_NAME=$(echo "$CLAUDE_TOOL_NAME")

if [ "$TOOL_NAME" = "Edit" ] || [ "$TOOL_NAME" = "Write" ]; then
  npm test --passWithNoTests 2>&1 | tail -5
fi
```

---

## CLAUDE.md

`CLAUDE.md` は Claude Code がプロジェクトを読み込むときに自動的に参照するコンテキストファイルです。チームのルール、コマンド、アーキテクチャ上の制約などを記述しておくことで、毎回説明しなくてもよくなります。

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

### /init で自動生成する

`/init` コマンドを使うと、既存のコードベースを分析して `CLAUDE.md` の雛形を自動生成します。

---

## 設定ファイル（settings.json）

`.claude/settings.json`（プロジェクト）または `~/.claude/settings.json`（ユーザー）で Claude Code の動作を細かく制御できます。

### 主な設定項目

```json
{
  "model": "opus",
  "theme": "dark",
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git *)",
      "Edit",
      "Read"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force)"
    ]
  },
  "hooks": {
    "PreToolUse": [...],
    "Stop": [...]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

### パーミッション設定

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

MCP サーバーを設定することで、Claude Code にブラウザ操作、データベース接続、外部 API 連携などの能力を追加できます。

### 設定方法

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
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

---

## キーボードショートカット

Claude Code CLI でよく使うキーバインドです。

| ショートカット | 動作 |
|--------------|------|
| `Ctrl+C` | 実行中の処理をキャンセル |
| `Ctrl+D` | セッションを終了 |
| `↑` / `↓` | 入力履歴を遡る |
| `Tab` | スラッシュコマンドの補完 |
| `Shift+Enter` | 改行（`/terminal-setup` で設定後） |
| `Esc` | 入力をキャンセル |

---

## クイックスタート

### 1. プロジェクトに Claude Code を導入する

```bash
# インストール
npm install -g @anthropic-ai/claude-code

# プロジェクトに CLAUDE.md を生成
claude
/init
```

### 2. チーム共有のカスタムコマンドを追加する

```
.claude/
  commands/
    create-pr.md       # /create-pr コマンド
    run-checks.md      # /run-checks コマンド
  settings.json        # パーミッション設定
CLAUDE.md              # プロジェクトの説明
```

### 3. 危険な操作を防ぐフックを設定する

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/guard.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 参考リンク

- [Claude Code 公式ドキュメント](https://docs.anthropic.com/ja/docs/claude-code/overview) — 機能説明・セットアップガイド
- [Claude Code Agent Skills](https://docs.anthropic.com/ja/docs/claude-code/skills) — Agent Skills（`.claude/skills`）の作成と運用
- [Claude Code Plugins](https://docs.anthropic.com/ja/docs/claude-code/plugins) — プラグインとマーケットプレイスの使い方
- [Claude Code Subagents](https://docs.anthropic.com/ja/docs/claude-code/sub-agents) — サブエージェント（`.claude/agents`）の定義
- [Claude Code フック](https://docs.anthropic.com/ja/docs/claude-code/hooks) — フックの詳細仕様
- [Claude Code 設定](https://docs.anthropic.com/ja/docs/claude-code/settings) — settings.json リファレンス
- [MCP 公式サイト](https://modelcontextprotocol.io/) — Model Context Protocol の仕様
- [MCP サーバー一覧](https://github.com/modelcontextprotocol/servers) — 公式・コミュニティ MCP サーバー

---

> **注意**: Claude Code は Anthropic が開発・提供するツールであり、GitHub Copilot とは別製品です。このページは Claude Code 固有の機能を解説しています。GitHub Copilot のカスタマイズについては [トップページ](../../README.md) を参照してください。
