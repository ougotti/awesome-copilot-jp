# Codex ガイド（Agent Skills）

> **対象ツール**: Codex（OpenAI） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-30

[openai/skills](https://github.com/openai/skills) は OpenAI が公開している Codex 用の公式スキルカタログです。指示・スクリプト・リソースをフォルダにまとめた「スキル」を追加することで、デプロイ・ブラウザ自動化・外部サービス連携といったワークフローを Codex に持たせられます。

このページは**導入して最初の 1 個を動かすまで**の入口です。全スキルの一覧は [Agent Skills カタログ](catalog.md) にあります。

---

## 1. 準備する

### インストール

```bash
npm install -g @openai/codex
codex
```

### スキルの置き場所

Codex は次の順序でスキルを探します。**リポジトリで共有したいなら `.agents/skills/`、自分専用なら `~/.codex/skills/`** です。

```
カレントディレクトリ
  └── .agents/skills/          # リポジトリ共有（コミットする）
親ディレクトリ（リポジトリルートまで）
  └── .agents/skills/
ユーザーレベル
  └── ~/.codex/skills/          # 個人用（全プロジェクト共通）
システムレベル（自動インストール済み）
  └── ~/.codex/skills/.system/
```

### インストール後の確認

```bash
# curated スキルをスキル名で導入
$skill-installer linear
```

> [!IMPORTANT]
> **インストール後は Codex を完全に終了して再起動してください。**再起動しないとスキルが認識されません。再起動後、`$<スキル名>` で呼び出せれば導入成功です。

---

## 2. 最初に試す 3 〜 5 個

用途別の入口です。まず 1 つ入れて、呼び出せることを確認してから増やしてください。

| 目的 | 最初に試すスキル | 導入コマンド | 追加で必要なもの |
|------|----------------|------------|----------------|
| スキルの仕組みを理解する | `skill-creator` | 不要（System・自動） | — |
| CI の失敗を直させる | `gh-fix-ci` | `$skill-installer gh-fix-ci` | GitHub リポジトリ |
| E2E テストを書かせる | `playwright` | `$skill-installer playwright` | 対象アプリの起動 |
| フロントエンドを公開する | `vercel-deploy` | `$skill-installer vercel-deploy` | Vercel アカウント |
| 仕様や調査を残す | `notion-research-documentation` | `$skill-installer notion-research-documentation` | Notion アカウント・コネクタ |

**→ 全スキルの一覧は [Agent Skills カタログ](catalog.md) を参照**

---

## 3. スキルを呼び出す

呼び出し方は 2 通りだけです。以下はすべてのスキルに共通します。

### 明示的に指定する

スキル名を `$` プレフィックスで指定します。

```
「$linear を使って、バグレポートの Issue を作成してください」
「$playwright で、フォームの送信テストを実行してください」
```

### Codex に選ばせる

タスク内容とスキルの `description` を照合し、Codex が自動的に選択します。

```
「Vercel にデプロイしてください」
→ Codex が自動的に $vercel-deploy を選択
```

> 意図しないスキルが選ばれる場合は、`$` で明示するのが確実です。自作スキルで自動選択が効かないときは、`description` に「いつ使うか」が書けているかを見直してください（[書き方の例](catalog.md#description-の書き方)）。

---

## 4. 3 つの階層の違い

`openai/skills` はスキルを 3 層に分けています。**信頼度と導入方法が違う**ので、この表だけ押さえておけば十分です。

| 階層 | ディレクトリ | 提供元 | 状態 | インストール | 使う前に |
|-----|------------|-------|------|------------|---------|
| **System** | `skills/.system/` | Official | GA | 不要（自動） | そのまま使える |
| **Curated** | `skills/.curated/` | Official | GA | スキル名で指定 | 外部アカウントの要否を確認 |
| **Experimental** | `skills/.experimental/` | Community | Experimental | パス / URL で指定 | **中身とスクリプトを必ず確認** |

Experimental は OpenAI による品質保証がありません。検証環境で試してから使ってください。

---

## 5. Plugin でまとめて配る（2026-08 の追加）

スキルを 1 つずつ入れるほかに、スキル・コネクタ・MCP サーバー・フックなどを束ねた **Plugin** を導入できます。Codex CLI 0.147.0（2026-08-07）で、可搬形式の Agent Plugin のインストールと、**ローカル / 個人 / ワークスペース / リモート**のカタログを横断した検索に対応しました。

```text
codex
/plugins
```

CLI のプラグインブラウザは Marketplace ごとにタブが分かれ、詳細の確認・インストール・アンインストールと、インストール済みプラグインの有効・無効の切り替え（<kbd>Space</kbd>）ができます。

| 項目 | 内容 |
|------|------|
| 使える場所 | Codex CLI（`/plugins`）と ChatGPT デスクトップアプリの Codex。**IDE 拡張は非対応** |
| 同梱できる要素 | Skills / コネクタ / MCP サーバー / ブラウザ拡張 / フック / 定期タスクのテンプレート |
| 導入後 | スキル導入時と同じく、**新しいセッションを開始してから**使う |
| Cursor からの移行 | Cursor が管理している Skill をインポートできる（0.147.0） |
| 注意 | フックは設定した時点で自動実行される。**有効化する前に中身を確認する** |

> **入れすぎに注意**: Codex はコンテキストが逼迫すると Skill カタログを切り詰め、その旨を警告します。**使う分だけ有効にする**ほうが安定します（プラグインブラウザの <kbd>Space</kbd> で個別に無効化できます）。

**→ 可搬形式（Agent Plugins 1.0.0）の仕様と他ツールの対応状況は [Skills 最新動向 8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準) を参照**

---

## 6. 定期・イベントで動かす（Scheduled tasks）

スキルとプラグインを「呼ぶたびに人が起動する」段階から先へ進めるのが **Scheduled tasks** です。時刻ベースの繰り返しに加えて、外部サービスのイベントを起点にできます。

| 起動のしかた | 内容 |
|-------------|------|
| 時刻ベース | 毎日・毎週・任意の間隔（RFC 5545 の繰り返し規則） |
| イベントベース | **Gmail**（新着メール。送信者・件名で絞り込み）／**Slack**（チャンネルの新規メッセージ。投稿者・スレッド有無で絞り込み）／**GitHub**（PR の活動。レビュー・コメント・コミット・マージ、PR / 作成者 / タイトル / ラベルで絞り込み） |

**1 つのタスクで複数のイベントトリガーは使えますが、イベントトリガーと時刻ベースのスケジュールは併用できません。** Scheduled tasks からは Skills を利用でき、ChatGPT Work で作成したものは Plugins も使えます。

ローカルプロジェクトでは、実行先を**作業中のチェックアウト**にするか、**隔離した Git worktree** にするかを選べます。worktree を選ぶと、タスクの変更が手元の未完了の作業と混ざりません。

### 使う前に確認すること

| 確認すること | 内容 |
|-------------|------|
| プランと権限 | イベントトリガーは対象プランとワークスペースでの有効化が前提。管理者が「Allow event-triggered scheduled tasks」で制御する |
| 対応する面 | **イベントトリガーはデスクトップアプリと CLI では使えない** |
| 実行の前提 | デスクトップアプリのタスクは、**マシンとアプリが起動したまま**である必要がある |

役割で整理すると、**Skill = 手順の定義**、**Plugin = 外部接続**、**Scheduled task = 起動条件**、**worktree / サンドボックス = 実行境界**です。保守・共有したい処理は Skill 側に置き、タスク側には起動条件と対象だけを持たせると、後から読み解けます。

**→ ループとして設計する考え方は [ループエンジニアリング](../dev-methods/loop-engineering.md) を参照**

---

## 7. 他のエージェントから設定と作業を引き継ぐ

Codex は、Claude Code・Cursor などから設定と直近の作業を取り込めます。

| 面 | 取り込み元 | 方法 |
|----|-----------|------|
| ChatGPT デスクトップアプリ | Claude Code / Claude Cowork / Cursor | 設定画面の Import。**自動更新**を有効にすると元の環境と同期を続けられる |
| Codex CLI | Claude Code / Cursor | `/import`。**直近 30 日・最大 50 chat**が対象 |

取り込める対象は、Instructions（`AGENTS.md` / `settings.json` / `config.toml`）、Skills / Plugins、プロジェクトフォルダ、project memories、chat、**MCP サーバー設定・Hooks・スラッシュコマンド・サブエージェント**です。**元の環境は変更も削除もされません。**

> **取り込んだ後に点検すること**: 公式ドキュメントは、ツール制限・MCP の認証設定・Hooks・Plugins・プロンプトテンプレートが**手動のフォローを要する場合がある**と明記しています。特に Hooks は設定された時点で自動実行されるため、[中身を確認してから](../dev-methods/skill-security.md)有効にしてください。

> `/import` は、実行中のタスク・リモートセッション・ローカルの app-server デーモンに接続中は使えません。

---

## 外部アカウントが必要なスキル

以下は Codex 単体では完結せず、**アカウントやコネクタ設定が前提**です。導入前に用意してください。

| 前提 | 該当スキル |
|------|-----------|
| Vercel / Netlify / Render / Cloudflare のアカウント | `vercel-deploy` / `netlify-deploy` / `render-deploy` / `cloudflare-deploy` |
| GitHub リポジトリへのアクセス権 | `gh-fix-ci` / `gh-address-comments` |
| Figma アカウントとファイル権限 | `figma` 系すべて |
| Notion アカウントとコネクタ | `notion-` 系すべて |
| Linear / Sentry のアカウント | `linear` / `sentry` |
| 対象アプリの起動（localhost 等） | `playwright` / `playwright-interactive` / `screenshot` |

> デプロイ系スキルは**本番環境に影響します。**実行前に対象環境と公開範囲を必ず確認してください。

---

## GitHub Copilot Skills との違い

| | **openai/skills** | **GitHub Copilot Skills** |
|--|------------------|--------------------------|
| 対象ツール | OpenAI Codex CLI | GitHub Copilot |
| 形式 | `SKILL.md` + スクリプト | `SKILL.md` + 関連ファイル |
| 用途 | ターミナルエージェント向けワークフロー | Copilot チャットのテンプレート |
| 配置場所 | `.agents/skills/` | `.github/skills/` |

> ツールごとの用語の違い全般は [ツール間の用語対照表](../../README.md#ツール間の用語対照表) を参照してください。

---

## 関連ドキュメント

- [Agent Skills カタログ](catalog.md) — 全スキル一覧（入力・生成物・確認すべき点つき）とカスタムスキルの作り方
- [Skills 最新動向](../trends.md) — `gh skill` など Skill の発見・配布・更新の仕組み
- [GitHub Copilot ガイド](../copilot/README.md) ／ [Claude Code ガイド](../claude-code/README.md) — 他ツールのカスタマイズ

## 参考リンク

- [openai/skills リポジトリ](https://github.com/openai/skills) — 公式スキルカタログ
- [Agent Skills – Codex 公式ドキュメント](https://developers.openai.com/codex/skills) — 公式スキル解説
- [Plugins – Codex 公式ドキュメント](https://developers.openai.com/codex/plugins) — Plugin の導入・権限・Marketplace（公式）
- [openai/codex リポジトリ](https://github.com/openai/codex) — Codex CLI 本体
- [Codex CLI 公式ドキュメント](https://developers.openai.com/codex/cli) — CLI の使い方
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations) — 時刻・イベントでの起動、worktree、プラン要件（公式）
- [Import from another agent](https://learn.chatgpt.com/docs/import) — 取り込み対象・制限・取り込み後の点検項目（公式）

---

> **注意**: Experimental スキルはコミュニティ提供であり、OpenAI による品質保証はありません。本番環境での使用前に十分な検証が必要です。
