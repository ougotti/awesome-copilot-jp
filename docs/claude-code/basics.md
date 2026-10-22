# Claude Code のカスタマイズ機能

> **対象ツール**: Claude Code ｜ **実行環境**: CLI（ターミナル/デスクトップ） / Chat UI（Web） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-10-22

Claude Code を「自分たちのやり方」に合わせるための仕組みを解説します。**どの仕組みをいつ使うか**の判断を先に示し、その後で各仕組みの設定方法を説明します。

> **モデル選択（2026-09-23確認）**: Claude Opus 5.5 は Claude Code と Claude Platform で利用できます。Anthropic はコードベース全体の移行・監査など長時間の作業を用途に挙げ、Claude Code と Claude Platform で Fast mode も提供しています。Fast mode は速度と料金の条件が通常モードと異なるため、選択時は[公式発表](https://www.anthropic.com/claude-opus-5-5)と最新料金を確認してください。GitHub Copilot 経由の提供プラン・管理者設定は[Copilot ガイド](../copilot/README.md#2026-09-22-の新モデル--copilot-経由の利用条件)で別に扱います。

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

### `AGENTS.md` は `CLAUDE.md` の代替で、追加読み込みではない

Claude Code 2.1.277（2026-09-18）から、プロジェクトに `CLAUDE.md` がない場合は `AGENTS.md` を Project instructions として読めます。**両方があるときに内容をマージする機能ではなく、`CLAUDE.md` があればそちらが優先**されます。切り替えは `/config` の Project instructions で確認します。

リリース時点では Amazon Bedrock、Google Vertex AI、Microsoft Foundry 経由の Claude Code には未提供です。共通の `AGENTS.md` を置いても、これらの経路まで同じ挙動になるとは限りません。

### モデルを更新したら `/doctor prompt-audit` で点検する

`CLAUDE.md` や Skill には、古いモデルの癖に合わせて足した強い言葉や細かい手順が残りがちです。Claude Code 2.1.283（2026-09-25）で加わった `/doctor prompt-audit`（別名 `/checkup prompt-audit`）は、`CLAUDE.md`・Skill・agent・command を読み、古いモデル向けの書き方、古いパス、使えなくなった command、矛盾する指示ファイルを報告します。

点検結果は**削除の候補**であって、そのまま適用する結論ではありません。作成者しか知らない文脈は残し、採用した変更は eval で確かめます。**→ 点検の原則、残すべき記述、eval との組み合わせ方は [Skill / エージェントの評価](../dev-methods/evals.md#モデルの更新も変更として扱う--prompt-audit-で点検してから測る) を参照**

### PR のレビューでは、どの版の `CLAUDE.md` が読まれるか

マネージドの **Code Review**（GitHub の PR に Claude がコメントする機能。research preview、Team・Enterprise）は、PR が `CLAUDE.md` を編集するとき、その **base branch（マージ先）の版**を使います（v2.1.292 の修正。それ以前は編集された `CLAUDE.md` の規則が無視されていました）。そのため、**同じ PR で書き換えた規則は、その PR のレビューには効きません**。一方、ローカルの `/code-review` は通常のセッションと同じく作業ツリーの `CLAUDE.md` に従い、Code Review 向けの `REVIEW.md` は読みません。

Copilot code review は `CLAUDE.md` も custom instructions として、こちらは **head（変更後）の版**から読みます。両方のレビューを使うリポジトリでは、指摘が食い違う原因になり得ます。**→ 参照元の比較、基準を変えるときの手順と検証例は [AI コードレビューはどの指示を読むか](../dev-methods/review-instructions.md) を参照**

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

Claude Code 2.1.275 以降は、同じ claude.ai アカウントで有効にした Skills と Plugins が、サインイン済みのターミナルセッションへ同期されます。端末側を固定構成にしたい場合は `syncClaudeAiSkills: false`、`syncClaudeAiPlugins: false` で個別に止めます。**リポジトリ・ローカル・Plugin・アカウント同期・組織ポリシーの各層を合成したものが、実際に使える拡張セット**です。

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

> **2026-08 の変更**: 対話セッションでは **fork モードが既定で有効**になりました（2.1.232）。`subagent_type: "fork"` は起動時点の親の会話履歴、system prompt / tools、model、prompt cache を引き継ぎます。定義ファイルから起動する通常のサブエージェントは、引き続き新しいコンテキストで開始します。会話の続きを別観点で走らせるなら fork、役割・tool・modelを個別に定義して文脈を隔離するなら非 fork 型を選びます。詳しい比較は[マルチエージェントを使う境界線](../dev-methods/multi-agent.md#3-agent-as-tool-専門作業を隔離して呼び出す)を参照してください。
>
> **2026-10 の変更**: 2.1.302 から、fork モードは `claude -p`・Agent SDK・desktop app・VS Code でも既定で有効です（`CLAUDE_CODE_FORK_SUBAGENT=0` で無効、`claude mcp serve` は対象外）。desktop app と VS Code では main conversation の subagent が常に background で動きます。起動経路ごとの既定は [2.1.302 の変更点](#21302--無人実行の開始モードと-subagent-の実行方式)を参照してください。

2.1.271 以降は、カスタム / Plugin サブエージェントの frontmatter（または `--agents` JSON）に `omitClaudeMd` を指定できます。これは user / project / local の `CLAUDE.md` をサブエージェントへ渡さない隔離であり、**組織が強制する managed policy は引き続き読み込まれます**。プロジェクト指示を隠す設定を、管理ポリシーの回避に使うことはできません。

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

> **2.1.287 以降のプラグインは「mod」を含められます。** mod は Claude Code の内部で動く関数で、画面の描画やツール呼び出しまで書き換えられます。フック・Skill・MCP と違って利用者の権限で、sandbox の外で動くため、入れる前の確認と組織での制御が別に要ります。→ [Mods](mods.md)

> GitHub Copilot 側の Plugin との違い（含められる要素、Marketplace の扱い、組織での強制方法）は [GitHub Copilot Plugins](../copilot/plugins.md#claude-code-の-plugin-marketplace-との比較) の比較表を参照してください。

### 公式ディレクトリ `claude-plugins-official`

Anthropic が管理する公式のプラグインディレクトリです。**初回に対話モードで起動したときに自動で追加される**ため、多くの場合は登録操作なしで `/plugin` の Discover から探せます。ネットワークやポリシーで追加されなかった場合は、自分で登録します。

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install <plugin-name>@claude-plugins-official
```

**「公式ディレクトリにある」＝「Anthropic 製」ではありません。** リポジトリは Anthropic 内製のプラグインと、パートナー・コミュニティ製のプラグインを別のディレクトリに分けて収録しており、実際に AWS・Microsoft・Google などのエントリが並んでいます。README も「**Anthropic は同梱される MCP サーバー・ファイル・ソフトウェアを管理しておらず、意図どおり動くことも、変わらないことも保証できない**」と明記しています。導入前に配布元を確認する必要は、ここでも変わりません。

判断材料になる性質を 2 つ挙げます。

| 性質 | 内容 |
|------|------|
| **名前が予約されている** | `claude-plugins-official` をはじめとする公式マーケットプレイス名は、第三者のマーケットプレイスが名乗れません。公式を騙る配布元を防ぐ仕組みで、予約名で登録済みだったものは読み込まれなくなります |
| **自動更新が既定で有効** | 公式マーケットプレイスは自動更新が既定でオンです（第三者・ローカル開発の配布元は既定でオフ）。エントリ側はコミット SHA で固定されていますが、**ディレクトリが更新されれば追従します**。再現性を優先するなら `/plugin` の Marketplaces から自動更新を切ってください |

> [anthropics/skills](official-skills.md) はスキル集そのもの、`claude-plugins-official` は**プラグインを集めたディレクトリ**で、役割が違います。前者を使うには `/plugin marketplace add anthropics/skills` の登録が要ります。

### 配布元と検証（2026-09 時点）

| 項目 | 内容 |
|------|------|
| **GitLab の Marketplace** | `gitlab.com` のリポジトリ URL（nested subgroup を含む）を GitHub と同じように clone できる（2.1.232）。clone の認証に失敗したときのヒントも、実際の git ホスト名で表示される |
| **`claude plugin validate`** | `.claude/skills` だけを持つプラグインも検査対象になり、frontmatter の解析に失敗する `SKILL.md` を報告する（2.1.233）。公開前の自己点検に使える |
| **`headersHelper`** | url 形式の Marketplace やカタログエントリが、短命トークンなどの HTTP ヘッダーを生成するコマンドを実行できる（2.1.238）。実行前にコマンドが表示されて `[y/N]` の確認が入り、フォルダ信頼の受諾が必須で、資格情報の環境変数は継承されない |

Claude Code 2.1.268 では `claude plugin install` / `uninstall` / `update` / `enable` / `disable` に `--json` が加わり、`claude plugin list --json` の各行に `errorDetails` / `noteDetails` が追加されました。CI や管理スクリプトでは、人向けの表示を解析せず、この機械可読な出力を使えます。

2.1.271 以降は、install / update の `--json` が表示したコマンドを、その SHA-256 に限って `--accept-command <sha256>` で承認できます。これは包括的な `-y` ではなく、**直前にレビューした 1 コマンドだけを一致確認して受け入れる**ための境界です。コマンドや引数が変われば同じハッシュでは通りません。

### `plugin validate` と `plugin eval` を分ける

Claude Code 2.1.269 以降には、Plugin の eval suite を実行する `claude plugin eval` があります。2 つのコマンドは検査する対象が違います。

| コマンド | 確認すること | 主な出力 |
|---------|-------------|---------|
| `claude plugin validate <path>` | manifest、ディレクトリ構造、frontmatter などが読み込めるか | 構造・スキーマのエラー |
| `claude plugin eval <path>` | 実際の prompt で Skill が発火し、期待した結果・ツール順・ファイルを作るか | score、Plugin なしの baseline との差、JSON、HTML report |

2.1.281（2026-09-23）からは、`claude plugin validate` が Plugin の MCP 設定も検査します。load 時に**黙って捨てられる** `.mcp.json` の entry、宣言されていない `${user_config.*}` の参照、insecure な URL を報告します。shell 形式の hook で `${CLAUDE_PLUGIN_ROOT}` を quote していない場合の警告も加わりました。2.1.283（2026-09-25）では、Claude Code が install できない Plugin 名・marketplace 名を `marketplace.json` に書いた場合と、`outputStyles`・`themes`・`monitors`・`lspServers` のパスが存在しない、または Plugin のディレクトリ外を指す場合も失敗になりました。いずれも「読み込める構成か」の検査で、Skill が期待どおり動くかは引き続き `plugin eval` で確認します。

`claude plugin eval init` で `evals/` に case と grader の草案を作れます。各 case は既定で Plugin あり / なしをそれぞれ 3 回実行し、`regex`、`tool_used`、`tool_order`、`file_exists`、LLM judge などで採点します。実際のモデル呼び出しとして利用枠または API 料金を消費します。

> eval はセキュリティ検査ではありません。対象 Plugin の hooks と、明示的に起動した実 MCP server は agent の sandbox 外で動き得ます。信頼できる Plugin だけを評価し、CI では必要な tool だけを `--allow-tools` で許可してください。公式ドキュメントは server-side で command が利用不可になる場合も案内しているため、2.1.269 以上でも現在の利用可否を実行環境で確認します。

**→ case の作り方、baseline、grader、既存の community harness との違いは [Skill / エージェントの評価](../dev-methods/evals.md#claude-code-組み込みの-plugin-eval) を参照**

> バージョン番号は 2026-09 時点のスナップショットです。最新は [Claude Code の CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) を確認してください。

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

### フックの種類 — 誰が判定するか

> **確認日: 2026-10-08**。公式の [Hooks reference](https://code.claude.com/docs/en/hooks) に基づきます。

上の例はすべて `type: "command"`（シェルコマンド）ですが、フックには 5 種類あり、**判定する主体**が違います。

| 種類 | 判定する主体 | 結果の決まり方 | 向く用途 |
|------|-------------|---------------|---------|
| `command` | 自分で書いたスクリプト | 終了コード（`exit 2` でブロック）や JSON 出力 | 必ず同じ判定にしたい制御 |
| `http` | 自分のサーバー | HTTP の応答 | 組織の判定サーバーへの問い合わせ |
| `mcp_tool` | MCP サーバーのツール | ツールの結果 | 既存の MCP サーバーで判定する |
| `prompt` | **Claude のモデル**（1 回の判定） | モデルが返す JSON（`ok` / `reason`） | 文脈を読まないと判断できない条件 |
| `agent` | **ツールを使えるサブエージェント**（Experimental） | 同上。Read / Grep / Glob などで調べてから判定（最大 50 ターン） | ファイルやテスト結果を実際に確かめたい条件 |

`prompt` と `agent` は**自然言語で条件を書くフック**です。`$ARGUMENTS` にフックの入力 JSON が入り、モデルは次の形で答えます。

```json
{ "ok": true | false, "reason": "判断の理由", "impossible": true | false }
```

- 既定のタイムアウトは `prompt` が 30 秒、`agent` が 60 秒です。既定のモデルは、Claude Code が背景処理に使うモデルです（`model` で変更可）。
- 使えるイベントは限られます。`PreToolUse`・`PostToolUse`・`Stop`・`SubagentStop`・`UserPromptSubmit` などは両方に対応しますが、`SessionStart`・`Notification`・`PreCompact` などは `prompt` / `agent` に対応しません。`PermissionRequest` は `prompt` だけ対応し、しかも `ok: false` は**効果がありません**（承認を拒否するには `command` フックを使う）。
- **`ok: false` の意味はイベントで変わります。** `PreToolUse` ではツール呼び出しを拒否し、既定ではターンが終わります（`continueOnBlock: true` で理由を Claude に返して続行）。`Stop` / `SubagentStop` では理由が Claude の次の指示になり、**作業が続きます**（`impossible: true` なら終了を許可）。
- `agent` フックは公式が「Experimental。本番のワークフローには `command` フックを推奨」と明記しています。
- `/goal` は、セッション単位の `prompt` 型 `Stop` フックの組み込みショートカットです（[作業中のエージェントへの指示の出し分け](../dev-methods/agent-commands.md)）。

### 自然言語のフックは「書き方」で結果が変わる — 2.1.294 の修正

2.1.294（2026-10-08）の変更ログには、自然言語のフックについて 2 つの変更があります。**別々の変更**として読んでください。

| 種類 | 変更ログの記載 | 意味 |
|------|---------------|------|
| 修正 | Fixed `prompt` and `agent` hooks written as instructions (such as "Block commands that...") allowing what they should block | 「〜するコマンドをブロックせよ」のような**命令文**で書いたフックが、**本来ブロックすべき操作を通していた**。2.1.293 以前を使っている場合は、命令文のフックが効いていなかった可能性がある |
| 改善 | Improved how `prompt` hooks on Stop and SubagentStop written as instructions (such as "Carry on if the build is broken") are judged, so Claude is less likely to stop early | 「ビルドが壊れていたら続けよ」のような命令文の `Stop` / `SubagentStop` フックで、**早く止まりすぎる**ことが減った |

ここから言えるのは、**自然言語のフックは、書いた意図どおりに判定される保証がない**ということです。モデルが条件を解釈するため、言い回しや版によって結果が変わり得ます。「禁止」と書いただけで禁止が保証されるわけではありません。

#### 使う前に、期待する結果を決めて確かめる

無害な架空の入力で、**許可・拒否・継続・終了**のそれぞれが期待どおりになるかを確認します。以下は、`echo` だけを使う検証用の例です（実際の危険な操作は再現しません）。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Does the command in this input contain the string HOOK-TEST-DENY? If it does, respond ok:false with a reason. Otherwise respond ok:true. Input: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

| 試す入力（Claude に実行を頼む） | 期待する結果 | 確認する場所 |
|-------------------------------|-------------|-------------|
| `echo hello` | 許可（実行される） | トランスクリプト |
| `echo HOOK-TEST-DENY` | 拒否（実行されず、ターンが終わる） | 警告行に `reason` が出る |
| 同じ条件を命令文（"Block commands that contain HOOK-TEST-DENY"）で書いた版 | 上と同じ結果になること | 2.1.293 以前と 2.1.294 以降で比べると差が見える |

`Stop` も同じ考え方で確かめます。`Stop` フックには Claude の最後の応答が `last_assistant_message` として渡されるので、「最後の応答に `VERIFY-DONE` という文字列がなければ ok:false」のような条件にすると、**継続する場合と終了する場合**の両方を無害に試せます。

- 継続が止まらない事故に備えて、Claude Code は**連続 8 回**で `Stop` フックによる継続を打ち切ります（`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` で変更可）。
- `Stop` の入力の `stop_hook_active` が `true` のときは、すでにフックによって継続中です。満たせない条件で回り続けないよう、条件に含めるか、`prompt` フックでは `impossible: true` を返せるようにします。

#### 自然言語フックについて、確認できていないこと

- `prompt` / `agent` フックの**出力が JSON として壊れていた場合、タイムアウトした場合、モデルがエラーを返した場合**に、許可側・拒否側のどちらに倒れるか（fail open / fail closed）は、公式リファレンスで確認できませんでした。**ブロックしたい操作は、この挙動に依存させない**のが安全です。
- （参考）2.1.288 では、`PreToolUse` / `PermissionRequest` のフックが、マッチングの失敗やツール入力の JSON 化の失敗で**スキップされていた**問題が修正され、その場合は呼び出しがブロックされるようになりました。これは「フックが起動したか」の問題で、2.1.294 の「自然言語の判定」の問題とは別です。

#### 強制したい制御は、自然言語に任せない

| 制御 | 主体 | 性質 |
|------|------|------|
| `prompt` / `agent` フック | モデルの判断 | 柔軟だが、言い回し・版・入力で結果が変わり得る |
| `command` フック | 自分のスクリプト | 同じ入力なら同じ結果。テストできる |
| permission ルール（`deny` / `ask` / `allow`） | Claude Code | 宣言的で、モデルの解釈を挟まない |
| managed settings | 組織 | 利用者が弱められない |
| sandbox（OS の隔離） | OS | ツールが何に触れられるかを物理的に制限する |

**「必ず止めたいもの」は permission ルールや `command` フック、sandbox で止め、`prompt` / `agent` フックは「文脈を読まないと判断できない補助的なチェック」に使う**、という分担が安全です。フックの変更時の評価の組み方は [Skill / エージェントの評価](../dev-methods/evals.md#フックを変更したら許可拒否継続終了を測る) を参照してください。

---

### フックの実行失敗も止める — 2.1.295〜2.1.296

**提供元: Official / 状態: GA（CLI の正式リリース）**。2.1.295（2026-10-08）で `command` / `http` フックに `onFailure: "block"` が追加されました。従来の既定値 `continue` では、フックが壊れると対象操作が進む場合があります。拒否すべき条件の判定と、判定プログラム自体の失敗を分けて設定します（2026-10-13 再確認、公開日は公式 release の UTC 日付）。

| 失敗・イベント | `onFailure: "block"` の範囲 |
|---|---|
| 起動できない、タイムアウト、終了コードが 0 / 2 以外 | 対象イベントの exit 2 相当の制御。`PreToolUse` ならツール呼び出しを止める |
| HTTP 接続失敗・非 2xx 応答、不正な JSON / schema 違反 | 失敗として扱う。command の単なるテキスト出力は不正 JSON と同じ扱いではない |
| `PermissionRequest` | リクエストを拒否する |
| `Stop` / `SubagentStop` / `TaskCompleted` / `TeammateIdle` | この設定は効かない |
| `async` / `asyncRewake` の background command hook | この設定は効かない |
| `prompt` / `agent` フック | このフィールドの対象外。上の自然言語フックの未確認範囲を引き続き区別する |

検証用プロジェクトの `.claude/settings.json` で、同期の `PreToolUse` command hook に `"onFailure": "block"` を付け、スクリプトの正常終了・起動失敗・タイムアウト・不正出力をそれぞれ試してください。実行対象は `echo` など副作用のないコマンドとし、正常系は進み、失敗系は実行されないことを確認します。これは検証手順で、本ガイドでの実測結果ではありません。

2.1.296（2026-10-09）は **managed `PreToolUse` の拒否と turn 終了**、managed `PostToolUse` の `updatedMCPToolOutput` 適用、`UserPromptSubmit` / mod の `prompt.submit` 中断時に未検査の prompt が通る問題を修正しました。拒否・turn 終了・出力の置き換えは別々に確認してください。2.1.295 の深い mod hook 入力の切り詰め・managed plugin 判定、2.1.296 の `BASH_ARGV0` を使う shell の承認と secret redaction の修正も、組織で導入版を決める材料です。**これらを使う環境では 2.1.296 以上を検証する下限候補**とします。公式 LTS や、以後の版が不要という意味ではありません。

出典: [Hooks reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails)、[2.1.295](https://github.com/anthropics/claude-code/releases/tag/v2.1.295)、[2.1.296](https://github.com/anthropics/claude-code/releases/tag/v2.1.296)。

## 組織での統制 — 導入前・推論前・実行後

Claude Enterprise では、Skill や Plugin の「入れる前の確認」に加えて、**推論の直前**と**実行の後**にも統制をかけられます。3 つの段階の考え方は [Skill / Plugin のセキュリティ 5 節](../dev-methods/skill-security.md#5-統制が効く-3-つの段階) にまとめています。ここでは Claude 側の設定と利用条件を扱います。

| 段階 | 機能 | 状態 | 何ができるか |
|------|------|------|-------------|
| 導入前 | Skill / Plugin のセキュリティスキャン | Beta（Enterprise プラン、2026-08-06） | 第三者製の Skill・Plugin を、**アップロードまたは編集された時点**で悪意ある内容がないか自動検査する |
| 推論前 | Inference hooks | Claude Enterprise 向けに 2026-08-05 から Beta、**2026-10-20 に Beta を終了** | 組織の AI セキュリティサーバーを指定すると、**claude.ai・Cowork・Claude Code・Claude for Microsoft 365・Claude Tag・Claude in Chrome などの対象プロンプトが、サーバーの allow / deny 判定が返るまで推論に進まない**。**Validate tool calls** を有効にすると、tool の実行前にも判定する（`tool_call` event）。リクエストは署名され、判定の待ち時間（既定 5 秒）と失敗時の挙動は設定可能。**拒否はすべて Activity Feed に記録される** |
| 実行後 | Compliance API のセッション取得 | 利用者のマシン上のセッション取得は 2026-08-26 に**ベータを終了**（Cowork / Claude Code）。Claude for Microsoft 365 のセッションは 2026-09-24 に**ベータを終了**、Claude in Chrome のセッションは 2026-09-18 から **Beta** | 組織横断でセッションを一覧し、個別セッションのメタデータとトランスクリプトを取得する。既存の Compliance Access Key と `read:compliance_user_data` スコープを使う |

### 導入時に確認すること

- **いずれも Enterprise 向け**です。個人・チームプランでは使えません
- **Inference hooks は自組織でセキュリティサーバーを用意する前提**です。判定サーバーが落ちたときの挙動（通すのか止めるのか）を設定で決めておく必要があります。障害が続くと circuit breaker が働き、その間はすべての request にこの設定が適用されます
- **Inference hooks を通らない呼び出しがあります**（2026-10-22 確認）。Anthropic が組織のために動かす **Code Review（GitHub の PR のレビュー）・Claude Security のスキャン・smart reports** のモデル呼び出しは対象外です（利用者が Claude Code で実行する `/code-review` は対象）。Amazon Bedrock・Google Cloud、Claude Platform の API 組織も対象外で、音声モードでは一部の tool call が送られません。判定は allow / deny だけで、prompt の書き換え・伏せ字はできず、画像だけの内容は検査されません。**Inference hooks を唯一の DLP にしない**でください（[Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks)）
- 拒否された内容は会話に残るため、続けると同じ理由で拒否され続けます。Claude Code では `/rewind` で該当の prompt まで戻すか `/clear` で始め直す、と公式が案内しています
- Compliance API で取得できるのは**利用者のマシン上で動いたセッションを含みます**。監査の範囲と、従業員への周知の要否を法務・人事と確認してください
- 取得できる面は増えています。Claude for Microsoft 365（Excel・PowerPoint・Word・Outlook）は `product_surface` が `office_agents` で始まる値、Claude in Chrome は `claude_in_chrome` で区別します。監査対象の一覧に、これらの面を加えるかを決めてください

> **Activity Feed の変更（2026-09-24）**: Compliance API の Activity Feed は、ファイル名・プロジェクト文書名・artifact のタイトルを返さなくなりました。`filename` と `title` は常に空か省略され、**過去の activity にも遡って適用**されます。名前が必要な場合は、`read:compliance_user_data` スコープを持つ Compliance Access Key で ID から引き直します。Activity Feed の名前をそのまま集計・検索していた監査手順は見直しが必要です。

> 3 つとも「入れてよい Skill か」を人が読む作業を置き換えるものではありません。**スキャンは既知の悪意を検出する仕組み**であり、[導入前に中身を読む](../dev-methods/skill-security.md#2-導入前に何を確認するか)必要は変わりません。

### managed settings を下位の設定で弱められない変更

2026-09-22〜25 の Claude Code 2.1.280〜2.1.283 では、**repository・user・Plugin 側の設定から managed の制限を弱められない**方向の修正と追加が続きました。

| 版 | 変更 | 意味 |
|----|------|------|
| 2.1.280 | symlink 経由の書き込みを、repository 内での見かけのパスではなく**実際に書き込まれる先**で判定する | `acceptEdits`、allow rule、auto mode が repository 外への書き込みを承認しなくなった。UI 変更ではなく write boundary の訂正 |
| 2.1.281 | `--setting-sources`（SDK の `settingSources`）を teammates、`/bg`、`claude agents` の session、`--worktree --tmux` へ引き継ぐ | 親 session で読み込み元を絞っても、起動した別 session では絞られていなかった問題の修正。subagent への policy 継承として確認する |
| 2.1.282 | `allowClaudeInChromeWithManagedMcp` を追加 | exclusive な `managed-mcp.json` の下でも `claude --chrome` を使えるようにする managed 専用の許可。Chrome がブロックされたときのエラーがこのキーを示す |
| 2.1.282 | `allowManagedPermissionRulesOnly` の下では、repository・user・`--add-dir` の Skill / command と skills-directory Plugin の manifest が、`allowed-tools` で自らの tool を事前承認できない | 配布物の metadata が managed の permission rule を迂回しない |
| 2.1.282 | managed の boolean lock key を誤った型で書いても lock が適用され、startup で key 名を示す。`permissions` / `autoMode` / `worktree` / `attribution` は一部の値が無効でも残りを適用する | 設定ミスで policy 全体が黙って無効化される状態を減らす |
| 2.1.282 | managed settings または `--settings` で `allowUnsandboxedCommands: false`、あるいは managed で `allowManagedDomainsOnly: true` のとき、project / local の `sandbox.excludedCommands` を無視する | repository 側の設定で sandbox の例外を追加できない |
| 2.1.282 | project / local settings から、OpenTelemetry の export 有効化・endpoint・本文取得に関わる変数（`CLAUDE_CODE_ENABLE_TELEMETRY`、`OTEL_LOG_*` など）を設定できない | clone した repository がテレメトリの送信先を変えられない |
| 2.1.282 | Windows / WSL で、admin policy（HKLM、`managed-settings.json`）が存在するが無効・読めない場合、利用者が書き込める HKCU と WSL の `/etc/claude-code` を適用しない | fail-open を防ぐ |
| 2.1.283 | managed の `sandbox` で入れ子の値が 1 つ無効でも、その値だけを fail-closed にし、残りは適用する | 以前は無効な値が 1 つあると **`sandbox` ブロック全体が無視**されていた |
| 2.1.283 | `Skill(anthropic-skills:<name>)` の deny rule が、Claude Desktop が Plugin として配信した同じ Skill にも効く。`Skill(skill:<name>)` の deny は Skill の alias と表示名にも一致する | 配信経路や呼び名が変わっても deny を回避できない |
| 2.1.283 | `availableModelsMatch` と `deniedModels` を追加（managed 専用） | 新しいモデルを、検証が済むまで使わせない。[下記](#新しいモデルを検証前に使わせない--availablemodelsmatch-と-deniedmodels) を参照 |

同じ 2.1.283 では、Windows の PowerShell tool で `cmd /c rd`・`rmdir`・`del`・`erase` を使うと、`Remove-Item` なら拒否されるドライブのルートやホームフォルダーを削除できた問題も修正されています。Windows で Claude Code を使う端末は、この版以降へ更新してください。

運用確認では、managed file を置いたことではなく、**startup の警告、実際に解決された設定、subagent や別 session での挙動**まで確かめます。managed settings の解決結果は [`claude_code.managed_settings_resolved` OTel event](../dev-methods/harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions) で監査できます。

### auto mode が既定の開始モードになる範囲 — 2.1.283

Claude Code 2.1.283（2026-09-25）から、**どの設定ファイルも開始モードを指定していなければ、対話型のターミナルと VS Code 拡張のセッションは auto mode で始まります**。2.1.282 までは、Pro / Max / Team プランで feature flag を取得するセッションに限られていました。今回から **Enterprise プラン、Claude API、Amazon Bedrock、Google Cloud、Microsoft Foundry、Claude apps gateway** の対話セッションも対象です。

auto mode は、承認プロンプトの代わりに**別のモデル（classifier）が操作を判定する**モードです。承認なしで何でも実行するモードではありませんが、判定するのは人ではなくなります。sandbox やコンテナは、引き続き別の防御層として必要です。なお、`claude -p` と Agent SDK は従来どおり Manual（`default`）で始まるため、非対話の自動化はこの変更の対象外です。third-party provider で telemetry が off、または新規インストール直後の条件でも `default` で始まるよう揃えたのは 2.1.302 です（[変更点](#21302--無人実行の開始モードと-subagent-の実行方式)）。無人実行では開始モードを明示してください。

| 決めたいこと | 設定 | 注意点 |
|------------|------|--------|
| auto mode 自体を使わせない | managed settings の `permissions.disableAutoMode: "disable"` | `Shift+Tab` の選択肢から消え、`--permission-mode auto` で起動しても Manual（`default`）で始まる。**組織として確実に止められるのはこのキー** |
| 組織の既定の開始モードを決める | managed settings の `permissions.defaultMode` | ターミナルのセッションはそのモードで始まる。VS Code 拡張では、利用者の `claudeCode.initialPermissionMode` と、利用者が直前に選んだモードが優先される。どちらでも、実行中に auto mode へ切り替えられる |
| 自分のセッションの開始モードを決める | `~/.claude/settings.json` の `permissions.defaultMode`、または起動時の `--permission-mode` | project の `.claude/settings.json` に書いた `auto` / `bypassPermissions` は、開始モードとしては効かない |
| VS Code 拡張の開始モードを固定する | VS Code のユーザー設定 `claudeCode.initialPermissionMode` | `auto` は指定できない。VS Code 拡張は project の `.claude/settings.json` を開始モードの判定に読まない |

Enterprise と API 利用の組織は、**更新だけで開始モードが変わる**点に注意してください。社内で「承認プロンプトが出る」前提の手順書や研修資料がある場合は、2.1.283 を配布する前に `permissions.defaultMode` か `disableAutoMode` を決めます。

- Enterprise プラン、Claude API、Claude Platform on AWS、Bedrock、Google Cloud、Foundry では、**classifier の呼び出しがトークン使用量に計上**されます。読み取りと、保護されたパス以外の作業ディレクトリ内の編集は classifier を通らないため、増えるのは主にシェルコマンドとネットワーク操作の分です
- インストール・更新の直後の最初のセッションは、feature flag の取得前に開始モードを決めることがあり、表と違うモードで始まる場合があります。次のセッションからは表どおりになります
- auto mode が選ばれても、そのセッションで使えない場合（設定で無効にされている、対応していないモデルを使っている、Anthropic がサーバー側で一時的に止めている、など）は Manual で始まります
- Pro / Max / Team で `~/.claude/settings.json` に auto 以外の `defaultMode` を書いている場合は、その設定が維持され、auto mode へ変えるかを 1 度だけ確認されます

**→ 承認・sandbox・managed rule の関係は [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#claude-code-の-1-コマンド限定許可と-managed-mcp) を参照**

### 新しいモデルを検証前に使わせない — `availableModelsMatch` と `deniedModels`

組織で使えるモデルを絞る `availableModels` は、既定では**前方一致**です。`claude-opus-5` と書くと、Claude Code が対応した時点で Opus 5.5 のような後続版も許可されます。`opus` や `sonnet` のような family alias も、新しい版へ追従します。

2.1.283 で、後続版を自動で許可しないための managed 専用のキーが 2 つ加わりました。

| キー | 効果 | 使いどころ |
|------|------|----------|
| `availableModelsMatch: "exact"` | `availableModels` に**モデル ID で書いた項目**は、その版だけを許可する。新しい版は、一覧に追加するまで使えない | 「検証した版だけを使う」運用 |
| `deniedModels` | 列挙したモデルを拒否する。`availableModels` が許可していても拒否が優先され、許可リストがなくても使える | 特定の版だけを保留する運用 |

公式ドキュメントの例は、Opus と Sonnet を許可したうえで、Opus 5.5 を日付付き・プロバイダ固有の ID も含めて拒否するものです。

```json
{
  "availableModels": ["opus", "sonnet"],
  "deniedModels": ["claude-opus-5-5"]
}
```

拒否されたモデルは `/model` の一覧に表示されず、`/model <名前>` でも選べません。`--model`、`ANTHROPIC_MODEL`、`model` 設定で指定しても、起動時に外されて Default が選ばれます。hook やバックグラウンドの要求が拒否されたモデルを指定した場合は、セッションのモデルで実行されます。`enforceAvailableModels` を設定していない場合、Default が拒否されたモデルに解決されるときは、同じ family の許可された最新版、より低コストの family（Sonnet、Haiku の順）、`availableModels` のうち許可されたモデルを指す最初の項目、の順に下がります。どれも許可されなければ、Default で始まるセッションは起動しません。

導入時は次の 3 点を確認してください。

- **2 つのキーは managed settings からしか読まれません**。user / project / local の設定や `--settings` に書いても、警告とともに無視されます
- **2.1.282 以前はこの 2 つのキーを無視します**。古い版での起動を防ぐため、`requiredMinimumVersion` も併せて設定します
- **配布経路によって届く面が違います**。cloud session には端末に置いた managed settings file が届かないため、claude.ai の管理画面から配る server-managed settings を使います。逆に Bedrock・Google Cloud・Foundry・Claude Platform on AWS のセッションには server-managed settings が届かないため、MDM か managed settings file で配ります

Claude Enterprise では、claude.ai の管理画面でモデルを個別に無効にする方法もあります（2.1.187 以降、サーバー側でも強制）。この制限は、メンバーがサインインした場合と自分の API キーを使った場合に適用されますが、組織のサービスキーのように利用者に紐づかない資格情報には適用されません。そうした資格情報で動かす自動化には、`availableModels` 側の設定が必要です。GitHub Copilot 経由で Claude を使う場合のモデル単位の policy は、[Copilot ガイド](../copilot/README.md#2026-09-22-の新モデル--copilot-経由の利用条件)で扱います。

---

### 2.1.285〜2.1.288 の統制に関わる変更

> **確認日: 2026-10-08**。[Claude Code changelog](https://code.claude.com/docs/en/changelog) に基づきます。

**2.1.288（2026-10-02）— 実行結果と統制に直結する修正**

| 修正 | 運用上の意味 |
|------|-------------|
| リモート MCP server の結果が 16 MB を超える・解析できない場合に、**MCP の tool 呼び出しが 2 回実行されることがあった** | 外部に副作用がある tool（送信・作成など）は重複し得た。冪等性の考え方は [長時間タスクの信頼性設計](../dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い) |
| `bash -c` / `sh -c` の中の危険な `rm`（`/` やホームディレクトリ）が、bypassPermissions モードや shell の allow ルールの下で確認なしに実行され得た | allow ルールを広く書いている場合に影響 |
| `PreToolUse` / `PermissionRequest` のフックが、マッチングの失敗やツール入力の JSON 化の失敗で**スキップされていた** | 修正後はその呼び出しが**ブロックされる**（fail closed） |
| agent team で名前指定で起動した plugin 定義の agent が、自分の prompt・tools・`disallowedTools`・effort ではなく既定値で動いていた | plugin の agent で `disallowedTools` を使っている場合に影響 |
| 再起動した cloud session が、組織が強制するモデル一覧で拒否されるモデルを復元していた | `availableModels` などのモデル制限を使っている場合に影響 |
| path を限定した `.claude/rules` とネストした `CLAUDE.md` が、Write / Edit でファイルを作成・変更したときに読み込まれていなかった（Read のときだけ読まれていた） | ルールを path 単位で分けている場合に影響 |
| （変更）バックグラウンドのコマンドの時間制限は、無人のセッション（`-p`・Agent SDK・CI・cloud）だけに適用される。端末・デスクトップ・VS Code では制限なし | 対話で使う場合、長時間のコマンドが打ち切られなくなる |

remote MCP・危険な shell・権限フックを使う組織では、**2.1.288 以上を推奨下限の候補**として扱えます。ただし公式の LTS 宣言ではなく、その後の版にも統制の修正が続いています。本ページの [2.1.295〜2.1.296 の変更](#フックの実行失敗も止める--2129521296)も合わせて確認してください。導入時はその時点の最新版を選んでください。

**2.1.285〜2.1.287 — plugin・managed settings・MCP**

| 版 | 変更 | 確認すること |
|----|------|-------------|
| 2.1.285（09-29） | `claude plugin configure <plugin>`（`--values-stdin` で値を保存）。`claude plugin install --config` に `<server>.<key>=<value>` を追加し、同梱の `.mcpb` MCP server の設定をインストール時に渡せる | plugin の設定を CI などで自動化する場合の手順 |
| 2.1.285 | managed setting の **`allowedProviders`** で、端末が使える API provider（Anthropic API・独自 endpoint・Bedrock・Mantle・Vertex AI・Foundry・Claude Platform on AWS・Cloud gateway）を限定できる | 組織で接続先を限定する場合 |
| 2.1.285 | OS が managed settings file の読み取りを拒否した場合、起動を拒否せず**警告して、そのファイルの policy なしで起動する**ようになった。**それ以外の読み取りエラーや解析できないファイルでは、すべてのセッションが止まる** | 「警告で起動」と「停止」の境界を一般化しない。配布後に警告が出ていないか確認する |
| 2.1.285 | `@` を含む URL のパスワードの一部が、redact したログやトランスクリプトに出ていた問題を修正 | ログを外部へ送っている場合 |
| 2.1.287（10-01） | **Mods** を追加（[Mods](mods.md)） | — |
| 2.1.287 | OpenTelemetry の `user_prompt` event に **`prompt_text`**（`prompt` の写し）を追加 | **`prompt` を削除・マスクしている箇所では `prompt_text` も同じように扱う** |
| 2.1.287 | 2025-11-25 版 protocol の MCP server からの URL prompt（サインインなど）に対応。更新後に接続できなくなった server は、MCP の設定に `"bareElicitationCapability": true` を加える | 古い MCP server の接続 |
| 2.1.287 | `__proto__` という名前の MCP tool で、組織の tool ごとの権限の上限が黙って外れていた問題を修正 | 組織で tool 単位の上限を使っている場合 |

### 共有フォルダと Windows のパスを扱う前に — 2.1.292 の修正

> **確認日: 2026-10-08**。Claude Code v2.1.292 の [release](https://github.com/anthropics/claude-code/releases/tag/v2.1.292)（2026-10-06 公開）と、公式の [Permissions](https://code.claude.com/docs/en/permissions)・[Sandboxing](https://code.claude.com/docs/en/sandboxing) に基づきます。2.1.292 は「次の修正が入った版」であり、公式の LTS や安全性の保証を意味するものではありません。導入時は、その時点の最新版を選んでください。

2.1.292 では、**許可した範囲と、実際にアクセスする範囲がずれる**問題がいくつか修正されました。

| 修正（release の記載） | 何がずれていたか | 影響を受けやすい使い方 |
|----------------------|----------------|---------------------|
| PreToolUse hook approvals and auto mode bypassing the permission prompt for file reads from network (UNC) paths | ネットワーク（UNC）パスのファイル読み取りで、`PreToolUse` フックの承認や auto mode が**承認の確認を飛ばしていた** | 社内の共有フォルダ（`\\server\share\…`）を読ませる |
| `rm -rf` on the 8.3 short name or another alternate Windows spelling of the home folder or a drive not being treated as removing it | Windows の 8.3 短縮名（例: `C:\Users\TARO~1`）などの**別表記**で指定したホームフォルダやドライブの削除が、その削除として認識されていなかった | Windows で Bash / PowerShell を使う |
| a notebook or PDF read on macOS and Windows being able to return a file outside what was approved, through a link swapped in mid-read | 読み取り中に**リンクを差し替える**と、承認した範囲の外の notebook / PDF が返り得た | リンクを含むフォルダの PDF・notebook を読ませる |
| a managed sandbox read-deny path ... that appears or re-points mid-session not dropping project grants inside it or ending credential injection from files it covers | セッション途中に**現れた・付け替えられた** sandbox の読み取り拒否パスで、許可や credential の注入が止まっていなかった | 組織の managed settings で sandbox の `denyRead` を使う |

#### パスの種類を区別する

| パスの種類 | 例 | Claude Code の扱い（公式ドキュメントより） |
|-----------|----|-----------------------------------------|
| ローカルのパス | `C:\work\project`、`~/work` | permission ルール（`Read(...)` / `Edit(...)`）で判定する |
| **ネットワーク（UNC）パス** | `\\server\share\file` | Bash / PowerShell の引数に含むと**確認が出る**。アクセスすると、その名前のホストへ **Windows の credential が送られ得る**ため。UNC の共有は、ほとんどの場合 working directory に追加できない |
| ドライブに割り当てた共有 | `Z:\` | 公式は、共有をドライブ文字に割り当て、起動時に `--add-dir` で渡す方法を案内している |
| シンボリックリンク・ジャンクション | `./project/link` → `~/.ssh/...` | 要求したパスと解決先の**両方**で判定する。allow は両方が一致したときだけ、deny は**どちらかが一致すれば**効く。開くときにも解決先が承認時と同じかを確かめる |
| Windows の別表記 | 8.3 短縮名など | 2.1.292 で、ホームフォルダ・ドライブの削除として認識されるよう修正 |

#### 共有フォルダを使う前に確認すること

1. **Claude Code を 2.1.292 以降にする**（`claude --version`）。上の修正が入っていない版では、UNC パスの読み取りで確認が出ないことがあります。
2. **共有は UNC のまま渡さず、ドライブに割り当てて必要なサブフォルダだけ** `--add-dir` で渡す。共有全体を渡さない。
3. **機密を含むパスは `Read` の deny ルールで止める**。Windows のドライブや共有を指すパスの書き方は、公式の [Permissions](https://code.claude.com/docs/en/permissions) のパスの書式で確認し、下の「ダミー文書で確かめる」で実際に拒否されるかを確かめる。
4. **層を混同しない。** Claude Code の permission ルール、フック・auto mode の判断、sandbox の `denyRead`、**共有フォルダ側・OS 側のアクセス権**は、それぞれ別の制御です。たとえば sandbox の `denyRead` は Read ツールを止めません（Read は permission ルールに従う）。Claude Code の設定で許可しても、共有側のアクセス権が上限になります。

#### ダミー文書で確かめる

本物の業務データを使わず、**検証専用の共有フォルダにダミー文書だけを置いて**確かめます。

| 試すこと | 期待する結果 |
|---------|-------------|
| 許可したサブフォルダのダミー文書を読ませる | 読める |
| `Read` の deny ルールで止めたダミー文書を読ませる | 拒否される |
| auto mode で UNC パスのダミー文書を読ませる | 2.1.292 以降では確認が出る |
| 許可したフォルダ内のリンクから、範囲外のダミー文書を読ませる | 拒否される（allow は解決先も一致する必要がある） |

削除操作の実演や、共有・OS・managed settings の設定変更は、この確認に含めません。

> **非エンジニアの方へ**: 業務の共有フォルダを AI に読ませる前の考え方は、[生成AIを業務で安全に使う](../business/safety.md#情報の取り扱い) にまとめています。

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
| `"mcp__github__*"` | GitHub MCP ツールをすべて許可。2.1.299 から、書いたサーバー名にだけ一致する（[変更点](#2129921301--mcp-の許可ルールの完全一致化と-hook-の-fail-closed-化)） |

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

### 2026-09 の MCP 関連の変更

| 版・日付 | 変更 | 注意点 |
|---------|------|--------|
| Claude Code 2.1.280（2026-09-22） | `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` で、MCP tool description と server instruction の 2,048 文字上限を変更できる | session 内のすべての MCP server に効く。上限を上げるとコンテキストを消費するため、必要な server があるときだけ変える |
| Claude Code 2.1.281（2026-09-23） | 2026-07-28 版 protocol の接続で **URL-mode elicitation** に対応。server が browser での操作（認証など）を開くよう依頼できる | browser flow を開く経路であり、tool 実行や権限を自動承認する仕組みではない。tool permission・managed policy は別の層で判定される |
| Claude Platform（2026-09-22、Beta） | 会話途中の system message で tool 定義を追加できる **inline tools**（`inline-tools-2026-09-15` beta header） | Claude Code ではなく Messages API の機能。下記を参照 |

**inline tools** は、`tool_addition` block に完全な tool 定義を載せ、会話の途中で tool を追加する・schema を変える・server tool を新しい版へ移すための Beta 機能です。top-level の `tools` を変えないため、prompt cache を無効にしにくい設計です。同じ header で、参照による tool の追加・削除も扱えます。

MCP connector の `mcp-client-2026-09-15` beta header と組み合わせると、定義に MCP toolset を指定でき、response の `mcp_tool_listing` block に各 server から取得した tool list が記録されます。**この block を次の request に返すと tool list が固定されます**。

動的に tool を追加するアプリでは、次の 3 点を実行記録に残してください。

1. 使った beta header
2. 追加した tool 定義の出所（どの server・どの版から来たか）
3. 固定した `mcp_tool_listing`

動的な発見は、そのままでは同じ tool 一覧で再実行できることを意味しません。一覧を固定せずに再実行すると、server 側の変更で使える tool が変わる可能性があります。**→ 可搬性との関係は [プラグインの可搬性](../dev-methods/plugin-portability.md#tool-一覧の固定と構成の検証はクライアントごとに違う) を参照**

---

### 2.1.295〜2.1.296 の MCP・workflow の変更

| 項目 | 変更と確認点 |
|---|---|
| remote MCP | 2.1.295 で headless / SDK の長い切断からの再接続、直後に切れる接続への backoff、同じ pagination cursor の反復を修正 |
| protocol negotiation | 2.1.295 で、feature flag を取得しないインストールの claude.ai connector は MCP `2026-07-28` を既定にする。すべての MCP 接続に一律適用される変更ではない |
| 無効化した server | 2.1.296 で、ディレクトリ変更・plugin reload 後に headless session がフォルダで無効化済みの `.mcp.json` / plugin MCP server を起動する問題を修正 |
| tool description / server instruction | 2.1.296 で先行送信する説明の既定上限が 2,048 → 4,096 文字。全 tool を無制限に preload する保証ではない |
| subagent の文脈 | 2.1.296 の `autoCompactWindow` を frontmatter / `--agents` 定義に指定すると、親より早い compaction を設定できる |
| workflow のモデル | 2.1.296 の `CLAUDE_CODE_WORKFLOW_SUBAGENT_MODEL` は workflow agent に共通モデルを指定し、他の subagent のモデルは維持する |
| Skill と再開 | 2.1.295 は `skills` から最大 32 Skill を各 1 回 preload（Skill tool があれば残りも呼べる）。forked Skill の結果を呼び出した workflow subagent に返す修正も含む。2.1.296 は完了済み MCP result で終了した turn の再実行を修正 |

出典: [2.1.295](https://github.com/anthropics/claude-code/releases/tag/v2.1.295)、[2.1.296](https://github.com/anthropics/claude-code/releases/tag/v2.1.296)（2026-10-13 確認）。再接続・再開の検証は [エージェントの信頼性](../dev-methods/agent-reliability.md#workflow-と-mcp-の再開を検証する)へ。

### 2.1.299〜2.1.301 — MCP の許可ルールの完全一致化と hook の fail-closed 化

> **確認日: 2026-10-16**。**提供元: Official / 状態: GA（CLI の正式リリース）**。[2.1.299](https://github.com/anthropics/claude-code/releases/tag/v2.1.299)（2026-10-14）、[2.1.300](https://github.com/anthropics/claude-code/releases/tag/v2.1.300)（2026-10-14）、[2.1.301](https://github.com/anthropics/claude-code/releases/tag/v2.1.301)（2026-10-15）の release に基づきます（日付は公式 release の UTC 日付。2.1.297〜2.1.298 の release はありません）。本ガイドでは実機で再現していません。

この 3 版は、**既存の設定の効き方が変わる変更**を含みます。更新前に、次の表の「見直すこと」を確認してください。

**既存の設定の効き方が変わるもの**

| 版 | 変更 | 見直すこと |
|----|------|-----------|
| 2.1.299 | **MCP の allow rule が、書いたサーバー名にだけ一致する**。`mcp__a` は `a__b` や `a_` という別のサーバーを許可しなくなった | サーバー全体を許可するときは `mcp__<正規化したサーバー名>__*` と書く。前方一致で別サーバーまで許可していなかったかも確認する |
| 2.1.299 | **agent の `tools:` も、指定したサーバーの tool だけを取る**。名前に `__` を含むサーバーは `mcp__<名前全体>__*` と書く | custom agent・subagent の定義で MCP tool を列挙している場合 |
| 2.1.299 | 名前に `__` を含むサーバーへの `mcp__<server>` 形式の **deny / ask rule が効いていなかった**問題を修正 | deny で止めたつもりのサーバーが、更新前に動いていなかったか |
| 2.1.299 | **`UserPromptSubmit` hook が、Skill・カスタムスラッシュコマンドの展開より前に動く**。hook が prompt を止めると、埋め込みの shell 行も実行されない。Skill の frontmatter に書いた `UserPromptSubmit` は、その Skill を呼び出した次の prompt から動く | prompt の検査 hook で、展開後の内容を前提に判定していた場合 |
| 2.1.300 | PreToolUse / PermissionRequest hook が返す **`updatedInput` を、Claude 自身の入力と同じく検証する**。未知のキーは捨て、tool が受け付けない入力は deny になる | 入力を書き換える hook。独自のキーを足していた場合は効かなくなる |
| 2.1.300 | `claude remote-control` の `--sandbox` / `--no-sandbox` を削除。**この flag は以前から効果がなく**、指定するとエラー終了する | flag で sandbox 化していたつもりの起動スクリプトは、実際には sandbox なしだった。settings の `sandbox.enabled` へ移す |

**hook と sandbox が止める側に寄ったもの（2.1.299）**

| 変更 | 運用上の意味 |
|------|-------------|
| plugin hook が止められる操作は、hook が受け取れない・答えを返せないとき**拒否**する | 以前は通していた。hook の起動失敗で作業が止まり得るため、配布前に動作を確かめる |
| Windows で shell を指定していない PreToolUse / PermissionRequest hook が、Git for Windows がないと **fail-open** していた問題を修正（失敗時は block） | Windows 端末で bash 前提の hook を配っている組織は影響を受けていた可能性がある |
| plan mode で、PreToolUse hook や mod の `tool.check` が allow した**書き込み（MCP・ファイル・shell）が実行されていた**問題を修正 | plan mode を「書き込まない」前提で使う場合 |
| sandbox: macOS で symlink 経由の denied path へのアクセス、`--plugin-dir` への書き込み（sandbox の外で再読み込みされる）、glob の解釈の差を修正 | sandbox を書き込み境界として使う場合 |
| claude.ai の connector proxy と Anthropic がホストする MCP server、cloud / self-hosted runner の MCP proxy は **HTTP redirect を追わない** | redirect 先へ接続していた構成は動かなくなる。connector 自身のサーバーによる redirect は対象外 |
| 実行中の headless / SDK session に追加した MCP server を、**接続前に policy で確認**する。`claude mcp list` / `get` と subagent の MCP server も、policy で拒否されたものを起動しない | managed の MCP 制限が、動的な追加や subagent にも効く |
| ファイル名・フォルダ名に不可視文字・方向制御文字・空白に似た文字・`<` `>` を含む Skill / コマンドは、名前を変えるまで読み込まない | 見た目が同じ別の Skill を紛れ込ませる手口への対策 |

**cloud session と監査（2.1.299〜2.1.301）**

- Cowork の cloud session の auto mode では、PermissionRequest hook が **shell コマンドと subagent を承認できない**（2.1.299）。hook の allow に含めた `setMode` も無視される（2.1.300）。hook で権限モードを切り替える運用は使えません。
- agent hook が自分の `model` 指定に従うようになった（2.1.300）。subagent のモデルで上書きされず、使えないモデルは呼び出し元のモデルに戻ります。
- OpenTelemetry の `tool_decision` event に `classifier_verdict`・`permission_mode`・`classifier_category` が追加された（2.1.301）。auto mode の classifier による判定と permission rule による判定を区別できます。→ [ハーネスの OTel](../dev-methods/harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions)
- workflow agent が「task text には利用者の権限がない」という注記を読んで手順を飛ばし、run は成功と報告される問題が修正された（2.1.301）。workflow の成功表示だけで、全手順の実行を確認したとみなさないでください。

**更新時の確認手順（検証用プロジェクトで行う設計例。本ガイドでの実測ではありません）**

1. `settings.json` と managed settings の `mcp__` で始まる rule を一覧にし、サーバー全体を対象にする rule を `mcp__<server>__*` に揃える。
2. 名前に `__` を含む MCP server があれば、deny / ask が更新後に効くことを、副作用のない tool で確かめる。
3. 入力を書き換える hook は、`updatedInput` に tool の schema にないキーを入れていないかを確認する。
4. Windows 端末では、hook を起動できない状態（shell がない）で対象の操作が止まることを確かめる。

**→ 組織での見直しの観点は [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#2026-10-1410-16-の権限境界の更新) を参照**

### 2.1.302 — 無人実行の開始モードと subagent の実行方式

> **確認日: 2026-10-17**。**提供元: Official / 状態: GA（CLI の正式リリース）**。[2.1.302](https://github.com/anthropics/claude-code/releases/tag/v2.1.302)（2026-10-16 UTC、日本時間 10-17）の release に基づきます。本ガイドでは実機で再現していません。

この版は、**terminal 以外の起動経路（`claude -p`・Agent SDK・desktop app・VS Code）の既定値**を terminal に揃える変更を含みます。無人実行や、subagent をさらに入れ子で起動する構成では、更新前に次を確認してください。

**permission mode を指定しなかったときの開始モード**

| 起動経路 | 2.1.302 の挙動 | 見直すこと |
|---------|---------------|-----------|
| `claude -p` / Agent SDK で、third-party provider を使い、telemetry が off、または新規インストール直後 | permission mode を指定しなければ **`default`（Manual）で始まる** | この条件で別のモードで始まっていた環境がないか。release note はこの条件で「`default` で始まるよう変更した」と書いている |
| 上と同じ条件で `--permission-mode auto` を明示 | **auto のまま** | auto をやめる変更ではない。auto を使う無人実行は flag を明示する |
| 対話型の terminal / VS Code 拡張 | 変更なし（[2.1.283 の既定](#auto-mode-が既定の開始モードになる範囲--21283)のまま） | — |

無人実行の開始モードを、版や provider・telemetry の条件に任せないでください。起動スクリプト・CI では `--permission-mode` を、SDK では permission mode を**明示**し、組織として止めたいものは managed settings（`permissions.disableAutoMode` など）で決めます。

**fork subagent と background 実行の既定**

| 起動経路 | fork subagent（`subagent_type: "fork"`） | main conversation が起動する subagent | subagent 自身が起動する Agent call |
|---------|------------------------------------------|---------------------------------------|----------------------------------|
| terminal | 既定で有効（2.1.232 から） | background | （release note に変更の記載なし） |
| `claude -p` / Agent SDK | **既定で有効**（2.1.302 から） | （release note に変更の記載なし） | **既定で foreground** |
| desktop app / VS Code | **既定で有効**（2.1.302 から） | **常に background**（Claude が選ばなくなった） | **既定で foreground** |
| `claude mcp serve` | **提供しない** | — | — |

- fork subagent は `CLAUDE_CODE_FORK_SUBAGENT=0` で無効にできます。
- **fork かどうか（会話の文脈を引き継ぐか）と、background / foreground（親が待つか）は別の設定**です。background で動くことは、親の権限・sandbox・provider をそのまま受け継ぐことを意味しません。文脈と実行境界の違いは [マルチエージェントを使う境界線](../dev-methods/multi-agent.md#3-agent-as-tool-専門作業を隔離して呼び出す) を参照してください。
- 親（main conversation）と、その subagent が起動する子とでは既定が違います。入れ子の構成では、どの階層が background で動き、どの階層の完了を待つのかを確認してください。

**hook・auto mode・cloud の routine**

| 変更 | 運用上の意味 |
|------|-------------|
| `prompt` / `agent` hook は、**同じイベントについて同時に 12 個まで**実行し、残りは順番を待つ | session 全体や subagent の同時実行数の上限ではない（subagent の上限は [8 節](../dev-methods/multi-agent.md#8-通信コンテキストコスト権限停止条件)）。並列で動く前提になっていない hook は、順序・timeout・外部への副作用を点検する |
| `CLAUDE_CODE_AUTO_MODE_MODEL` を追加。**client 側**の auto mode classifier が使うモデルを選ぶ | **server 側**の auto mode のモデルは変わらない。どちらの classifier が判定しているかを分けて確認する |
| server 側 classifier の auto mode で、会話が長すぎて安全性の確認ができない場合、すべての tool call を拒否する代わりに compaction する | 判定が緩むのではなく、判定できる長さに縮めてから確認する |
| OpenTelemetry の `tool_decision` で、auto mode classifier の拒否の大半に `classifier_category` が付いていなかった問題、`OTEL_LOGRECORD_ATTRIBUTE_COUNT_LIMIT` が低いと `tool_use_id` などが押し出される問題を修正 | [2.1.301 で追加した属性](#2129921301--mcp-の許可ルールの完全一致化と-hook-の-fail-closed-化)で集計している場合は、2.1.302 以降のデータで見直す |
| cloud session の scheduled routine が途中で失敗した後、**1 時間以上後に最初から再実行**され、同じ報告の投稿などを繰り返し得た問題を修正 | 修正後も外部への書き込みは冪等にする（[ループエンジニアリング](../dev-methods/loop-engineering.md#定期実行の再実行と外部副作用--claude-code-21302)） |
| routine の run が、session の異常終了後に Completed、開始前の archive で Cancelled と表示されていた問題を修正（failed と表示する）。開始できなかった理由（組織の concurrent cloud session の上限など）を routine のページに表示 | Completed の表示だけで成功とみなしていなかったか、過去の run を確認する |

**MCP・Plugin・worktree の互換性の修正**

| 変更 | 影響を受けていた構成 |
|------|-------------------|
| MCP protocol `2026-07-28` を negotiate した server が `resultType`・`ttlMs`・`cacheScope` を省略すると、tool が出てこない・すべての呼び出しが失敗する問題を修正 | 2026-07-28 仕様へ移行した MCP server。省略は server 側の誤りとしてではなく、client 側の修正として扱われている |
| `claude plugin` などの subcommand が、設定の書き込みの完了前に終了し、変更が失われる・`.tmp` が残る問題を修正 | スクリプトから plugin の導入・設定を行う環境 |
| git の既定が reftable のとき、marketplace が毎回 clone され、git plugin の version が unknown になる問題を修正。self-hosted runner の reftable checkout の fetch 失敗も修正 | git の既定の ref format を reftable にしている端末・runner |
| git 2.56 以降で、存在しないディレクトリを指す `.git` file があると worktree isolation が worktree を作成・再開できない問題を修正 | worktree isolation を使う subagent / session |
| Windows の exFAT / FAT32 の drive 上の project で、すべてのファイル書き込みが拒否・確認になる問題を修正（`--plugin-dir` の session を含む） | 外付け drive・USB メモリで作業する端末 |
| Read tool が、画像ファイルをサイズに関係なく、また画像の名前を持つ pipe / device を丸ごとメモリへ読み込んでいた問題を修正。**128 MB を超える画像は拒否** | 巨大ファイルや special file によるメモリ枯渇の境界 |

これらの不具合に対して設定の回避策を入れていた場合は、恒久的な運用にせず、2.1.302 へ更新したうえで副作用のない操作で再検証してから回避策を外してください。**MCP・Plugin・worktree をこの構成で使う環境では 2.1.302 以上を検証する下限候補**とします。公式 LTS や、以後の版が不要という意味ではありません。

**→ 組織での見直しの観点は [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#2026-10-1510-17-の権限境界の更新) を参照**

### 2.1.304〜2.1.307 — 統制が緩む変更と、締まる・見える変更

> **確認日: 2026-10-22**。**提供元: Official / 状態: GA（CLI の正式リリース）**。[2.1.304](https://github.com/anthropics/claude-code/releases/tag/v2.1.304)（2026-10-19）、[2.1.305](https://github.com/anthropics/claude-code/releases/tag/v2.1.305)（2026-10-20）、[2.1.306](https://github.com/anthropics/claude-code/releases/tag/v2.1.306)（2026-10-21）、[2.1.307](https://github.com/anthropics/claude-code/releases/tag/v2.1.307)（2026-10-21）の release に基づきます（日付は公式 release の UTC 日付。2.1.303 と 2.1.308 は不具合修正のみ）。本ガイドでは実機で再現していません。

この期間は、**更新するだけで今までより通るようになる変更**が 2 つあります。先にこれを確認してください。

**統制が緩む方向の変更（更新前に確認する）**

| 版 | 変更 | 見直すこと |
|----|------|-----------|
| 2.1.305 | **`allowedMcpServers` が、`managed-mcp.json` の stdio server のうち `${VAR}` を `env` にだけ使うものを絞り込まなくなった**。allowlist から外していたそうした server は、**更新すると読み込まれる** | 止めたい server は `deniedMcpServers` に書く。allowlist だけで止めていた構成を洗い出す |
| 2.1.305 | `sandbox.allowNestedUserNamespaces` を追加。Linux の sandbox 内で user namespace を作れるようにする（Chromium・rootless podman 向け）。**公式は「sandbox のファイル保護を迂回できる」と明記** | 有効にするなら、その端末の sandbox は書き込み境界として扱わない。managed settings で禁止するかを決める |
| 2.1.304 | tool search を、独自の `ANTHROPIC_BASE_URL` の背後でも既定で有効にした（gateway が 400 / 422 を返したら外して再送） | LLM gateway で tool 定義を検査・記録している場合、送られる tool の形が変わる |

**統制が締まる・見える方向の変更**

| 版 | 変更 | 運用上の意味 |
|----|------|-------------|
| 2.1.304 | [Mods](mods.md) の `tool.check` に **`decider: "person"`**。その確認は承認画面か host の callback でしか承認できず、誰にも聞けない場面では mod の理由を添えて拒否される | auto mode や classifier に委ねたくない確認を、人の判断に固定できる |
| 2.1.304 | Mods の `settings.read` hook が**設定の層ごと**に受け取り、統合後の設定を書き換えられる。managed mod が組織の設定を**上限**にでき、保存期間の掃除に使う `cleanupPeriodDays` も対象 | 利用者の設定で組織の値を緩められない形を、mod で作れる |
| 2.1.304 | plugin の hook だけを許すポリシーで、main conversation で使う Skill の hook が外される場合、その Skill の **`allowed-tools` も付与しない** | hook を止めた Skill が、許可だけ持ち込む抜け道を塞ぐ |
| 2.1.304 | 1 つの取得元（リポジトリ・自分のフォルダ・plugin）の Skill が登録できる hook を、session あたり 1,024 個・matcher 16,384 文字までに制限 | 大量の hook を登録する Skill は動かなくなる |
| 2.1.305 | `allowManagedPermissionRulesOnly` を設定した組織では、Claude Desktop がパス指定で読み込む plugin の `allowed-tools` を付与しない | managed の許可だけを効かせる設定が、desktop の plugin にも及ぶ |
| 2.1.307 | OpenTelemetry に **`claude_code.safety_event`**。permission rule・auto mode・安全チェック・hook・sandbox が止めた、確認を求めた、差し戻した tool 呼び出しごとに出る | 「何が止められたか」を集計できる。→ [ハーネスの OTel](../dev-methods/harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions) |
| 2.1.307 | `/permissions` の Recently denied に拒否した shell コマンドそのものを表示し、承認すると説明ではなくコマンドを名指しする | 何を承認したかが曖昧なまま許可しない |

**無人実行・再開の修正**

| 版 | 変更 | 影響を受けていた構成 |
|----|------|-------------------|
| 2.1.307 | HTTP MCP の tool 呼び出しが、**呼び出し中に接続が切れると 2 回送られていた**。read-only か idempotent の tool だけを再試行するよう修正 | 書き込みをする remote MCP tool。過去に二重の作成・送信がなかったか確認する（[信頼性設計](../dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い)） |
| 2.1.304 | `claude --worktree` が、HEAD が detached か別のブランチのとき、終了時に確認なしで worktree とブランチを削除し、**コミットを失い得た** | `--worktree` で作業した端末。失ったコミットは `git reflog` で探す |
| 2.1.304 | plugin が subagent を起動・再実行して、headless 実行を `--max-turns`・Stop・入力の終了を越えて続けていた | 回数や時間の上限を `--max-turns` で決めていた無人実行 |
| 2.1.305 | Workflow の再開で、完了済みの `pipeline()` / `parallel()` の agent を記録から返さず再実行していた | workflow を途中から再開する運用（[ループエンジニアリング](../dev-methods/loop-engineering.md#定期実行の再実行と外部副作用--claude-code-21302)） |
| 2.1.305 | cloud session や SDK の `setMcpServers` で渡した MCP server が、後から利用者の設定にある同名の server に置き換えられていた | 呼び出し側が接続先を固定していたつもりの構成 |

**運用の新機能**

- `/auto-mode-setup`（2.1.304）— プロジェクトと最近の session を読み、auto mode に環境を教える対話型の設定。Bedrock・Vertex・Foundry・telemetry off の session でも使えます。
- `/claude-api managed-agents-secure`（2.1.304）— Managed Agents の agent の設定を、Anthropic の公開しているセキュリティガイドと比べます。設定は変えません。
- Code Review（2.1.304〜2.1.307）— Owner が組織に **Quick / Standard（既定）/ Deep** のレビュー段階を選び、リポジトリごとに変えられます。組織のすべてのリポジトリ（後から追加したものを含む）を対象にする設定と、`@claude review always` の購読をやめる `@claude review stop`（`off` / `pause`）も追加されました。→ [AI コードレビューはどの指示を読むか](../dev-methods/review-instructions.md)

**更新時の確認手順（検証用プロジェクトで行う設計例。本ガイドでの実測ではありません）**

1. `managed-mcp.json` の stdio server で `${VAR}` を `env` に使うものを一覧にし、allowlist から外していたものを `deniedMcpServers` に移す。更新後に `claude mcp list` で読み込まれないことを確かめる。
2. `sandbox.allowNestedUserNamespaces` を誰かが有効にしていないか、managed settings と配布している settings を確認する。
3. 書き込みをする remote MCP tool があれば、2.1.307 より前に二重の作成・送信が起きていなかったかを、相手側の記録で確認する。

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
- [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) — Claude Code / Platform と Fast mode の提供範囲（Anthropic 公式・2026-09-22）
- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands) — Agent Skills の作成と運用
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode) — キーボードショートカット・対話機能のリファレンス
- [CLI reference](https://code.claude.com/docs/en/cli-reference) — CLI の起動オプション
- [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) — `claude plugin eval` の suite、grader、baseline、分離、CI（公式）
- [Claude Code v2.1.268](https://github.com/anthropics/claude-code/releases/tag/v2.1.268) — Plugin 管理コマンドの JSON 出力（公式・2026-09-10）
- [Claude Code v2.1.269](https://github.com/anthropics/claude-code/releases/tag/v2.1.269) — `claude plugin eval` の追加（公式・2026-09-11）
- [Claude Code v2.1.271](https://github.com/anthropics/claude-code/releases/tag/v2.1.271) — `omitClaudeMd`、コマンド単位のドメイン許可、Plugin コマンドのハッシュ承認（公式・2026-09-14）
- [Claude Code v2.1.275](https://github.com/anthropics/claude-code/releases/tag/v2.1.275) — claude.ai の Skills / Plugins 同期と opt-out（公式・2026-09-17）
- [Claude Code v2.1.277](https://github.com/anthropics/claude-code/releases/tag/v2.1.277) — `AGENTS.md` fallback と提供経路の制限（公式・2026-09-18）
- [Claude Code v2.1.280](https://github.com/anthropics/claude-code/releases/tag/v2.1.280) ／ [v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) ／ [v2.1.282](https://github.com/anthropics/claude-code/releases/tag/v2.1.282) — MCP description 上限、URL-mode elicitation、`plugin validate` の MCP 検査、setting source の伝播、managed settings の優先（公式・2026-09-22〜24）
- [Claude Code v2.1.283](https://github.com/anthropics/claude-code/releases/tag/v2.1.283) — auto mode の開始モードの拡大、`availableModelsMatch` / `deniedModels`、`/doctor prompt-audit`、managed `sandbox` の fail-closed、`plugin validate` の厳格化（公式・2026-09-25）
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) — 開始モードの決まり方、`disableAutoMode`、VS Code 拡張の判定順、classifier の利用量（公式）
- [Model configuration — Restrict model selection](https://code.claude.com/docs/en/model-config#restrict-model-selection) — `availableModels` の前方一致、`availableModelsMatch`、`deniedModels`、配布経路ごとの適用範囲（公式）
- [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview) — inline tools（2026-09-22、Beta）と `mcp_tool_listing`、cache diagnostics の GA（2026-09-23）、Compliance API の Claude in Chrome（2026-09-18、Beta）・Microsoft 365（2026-09-24）・Activity Feed の変更（2026-09-24）（公式）
- [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks) — 推論前の allow / deny 判定（公式）
- [Compliance API — Retrieve session transcripts](https://platform.claude.com/docs/en/manage-claude/compliance-sessions) — セッションのトランスクリプト取得（公式）
- [Claude apps release notes](https://support.claude.com/en/articles/12138966-release-notes) — Skill / Plugin セキュリティスキャンの提供状況（公式）
- [MCP 公式サイト](https://modelcontextprotocol.io/) — Model Context Protocol の仕様
- [MCP サーバー一覧](https://github.com/modelcontextprotocol/servers) — 公式・コミュニティ MCP サーバー
