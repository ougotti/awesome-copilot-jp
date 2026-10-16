# Codex Agent Skills カタログ

> **対象ツール**: Codex（OpenAI） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-10-16

[openai/skills](https://github.com/openai/skills) 収録スキルの全一覧です。導入手順・最初に試すスキル・3 層の違いは [Codex ガイド](README.md) を参照してください。

> [!WARNING]
> **`openai/skills` は 2026-06-22 に deprecated になりました。** リポジトリの README は、現行の Codex の Skill・Plugin の例として [openai/plugins](https://github.com/openai/plugins) を、自作の Skill を Codex に追加する方法として [Build plugins](https://developers.openai.com/codex/plugins/build)（Skill だけの Plugin の作り方を含む）を案内しています。最後の更新は 2026-06-24 で、以降は追加も削除もありません（2026-10-16 確認）。
>
> 公式の [Build skills](https://learn.chatgpt.com/docs/build-skills) は、`$skill-installer` で `openai/skills` から入れられると引き続き説明しています。一方で、自分の Skill を再利用・配布するなら Plugin を推奨しています。**この下の一覧は、2026-06 時点で更新が止まったカタログ**として読んでください。新しく探すなら、次の「現行の入口」から始めます。

## 現行の入口 — openai/plugins と Plugins Directory

| 入口 | 内容 | 状態 |
|------|------|------|
| [openai/plugins](https://github.com/openai/plugins) | OpenAI が管理する Codex Plugin の例の集まり。`plugins/<名前>/` ごとに `.codex-plugin/plugin.json` と、`skills/`・`.mcp.json`・`.app.json`・`agents/`・`commands/`・`hooks.json` などを同梱する。2026-10-16 時点で 62 件（Figma・Notion・Linear・Sentry・Vercel・Cloudflare・GitHub・Slack・`build-web-apps`・`build-ios-apps`・`codex-security`・`superpowers` など） | Official。**一覧は件数ごと変わるため、本ガイドでは全件を転記しない** |
| ChatGPT / Codex の Plugins Directory | 公開 Plugin は、ChatGPT と Codex で共有されるディレクトリに 1 回登録すれば両方に出る。desktop app の Plugins Directory か [ChatGPT Plugins](https://chatgpt.com/plugins) から入れる | Official |
| `/plugins`（Codex CLI 0.147.0 以降） | ローカル・個人・ワークスペース・リモートのカタログを横断して探す | Official（[導入手順](README.md#5-plugin-でまとめて配る2026-08-の追加)） |

`openai/skills` の Curated にあった Figma・Notion・Linear・Sentry・Vercel・Cloudflare などは、`openai/plugins` では **Skill に MCP や app を組み合わせた Plugin** として置かれています。同じ名前でも構成が違うため、Skill 単体の感覚で入れず、同梱する MCP・接続先・必要なアカウントを導入前に確認してください（[Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#2-導入前に何を確認するか)）。

> **表の読み方**: 「入力」「生成物」「人が確認すべき点」は、各スキルの用途から**本ガイドが整理した目安**です。正確な仕様と最新の収録内容は [openai/skills](https://github.com/openai/skills) の各 `SKILL.md` を確認してください。

---

## System（自動インストール・`Official` / `GA`）

Codex に同梱され、インストール不要で使えます。

| スキル | 呼び出し | 入力 | 生成物 | 人が確認すべき点 |
|-------|---------|------|-------|----------------|
| **skill-installer** | `$skill-installer` | スキル名 / パス / GitHub URL | インストール済みスキル | 導入元の信頼性、`SKILL.md` の中身 |
| **skill-creator** | `$skill-creator` | 作りたい手順の説明 | `SKILL.md` とスクリプト雛形 | `description` が自動選択の判断に足るか |
| **plugin-creator** | `$plugin-creator` | まとめたい機能の説明 | プラグインの雛形 | 同梱する MCP・スクリプトの権限範囲 |
| **imagegen** | `$imagegen` | 画像の指示文 | 生成画像 | 権利・ブランド表現の妥当性 |
| **openai-docs** | `$openai-docs` | 知りたい仕様、モデル選定・移行の相談 | 公式ドキュメントを引用した回答、モデル名の更新方針 | 参照したドキュメントの版、移行対象を広げすぎていないか |
> `skill-installer` でスキルを追加した後は、Codex を完全に終了して再起動しないと新しいスキルが認識されません。

> `openai-docs` は System 層へ追加され、**インストールなしで使えるようになりました**（Curated 層にも同じスキルが残っています）。回答は OpenAI 公式ドキュメントの MCP サーバーを一次情報とし、Codex 自身に関する質問はマニュアル取得用のヘルパーを先に使う作りです。**MCP サーバーが未設定だと公式ドメインの Web 検索にフォールバック**するため、出力された回答の参照元が公式ドキュメントかどうかを利用者側で確認してください。

---

## Curated（`Official` / `GA`）

`$skill-installer <スキル名>` でインストールします。

### 開発・コーディング

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **aspnet-core** | 要件、既存プロジェクト | ASP.NET Core の実装 | 認証・入力検証・エラー処理 |
| **cli-creator** | ツールの仕様 | CLI ツールの実装 | 引数設計、破壊的操作の確認プロンプト |
| **migrate-to-codex** | 既存リポジトリ | `AGENTS.md` 等の Codex 対応設定 | 生成された前提が実態と合っているか |
| **winui-app** | UI 要件 | WinUI アプリの実装 | 対応 OS バージョン |
| **chatgpt-apps** | アプリ要件 | ChatGPT 連携アプリの実装 | API キーの扱い、利用規約 |

### デプロイ・インフラ

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **cloudflare-deploy** | プロジェクト、アカウント | Cloudflare Workers / Pages のデプロイ | 公開範囲、環境変数、課金 |
| **netlify-deploy** | 静的サイト、アカウント | Netlify のデプロイ | 公開範囲、ビルド設定 |
| **render-deploy** | バックエンド、アカウント | Render のデプロイ | 公開範囲、シークレット |
| **vercel-deploy** | フロントエンド、アカウント | Vercel のデプロイ | 公開範囲、環境変数、課金 |

> デプロイ系はいずれも**外部アカウントと認証情報**が必要です。本番環境へ流れないよう、実行前に対象環境を必ず確認してください。

### GitHub 連携

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **gh-address-comments** | PR とレビューコメント | 修正コミット・返信 | 指摘の意図を取り違えていないか |
| **gh-fix-ci** | 失敗している CI | 修正コミット | 根本原因を直したか、テストを緩めていないか |

### ブラウザ自動化・テスト

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **playwright** | 対象 URL、シナリオ | E2E テストコード・実行結果 | 認証情報の扱い、外部サイトへの影響 |
| **playwright-interactive** | 対象 URL | ブラウザ操作の実行結果 | 実データを操作していないか |
| **screenshot** | 対象 URL / 画面 | スクリーンショット画像 | 機密情報の写り込み |

### Figma 連携

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **figma** | Figma ファイル | 各種操作結果 | 対象ファイルの権限 |
| **figma-use** | Figma ファイル | デザイン内容の参照結果 | 参照したバージョン |
| **figma-generate-design** | デザイン要件 | Figma 上のデザイン | ブランドガイドラインとの整合 |
| **figma-implement-design** | Figma デザイン | 実装コード（React 等） | 余白・状態・アクセシビリティの再現度 |
| **figma-create-design-system-rules** | 既存デザイン | デザインシステムのルール | 既存運用との矛盾 |
| **figma-create-new-file** | 構成の指示 | 新規 Figma ファイル | 命名・配置先 |
| **figma-generate-library** | コンポーネント要件 | デザインライブラリ | 重複コンポーネント |
| **figma-code-connect-components** | デザインと実装 | 両者のリンク定義 | 対応付けの正しさ |

> Figma 系は **Figma アカウントと対象ファイルへのアクセス権**が必要です。

### Notion 連携

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **notion-knowledge-capture** | 記録したい内容 | Notion ページ | 書き込み先、公開範囲 |
| **notion-meeting-intelligence** | 会議メモ・記録 | 整理された議事ページ | 決定事項の取り違え |
| **notion-research-documentation** | 調査結果 | 調査レポートページ | 出典の記載 |
| **notion-spec-to-implementation** | Notion の仕様書 | 実装コード | 仕様の解釈違い |

> Notion 系は **Notion アカウントとコネクタ設定**が必要です。

### セキュリティ

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **security-best-practices** | コードベース | 改善提案・修正 | 提案の網羅性を過信しない |
| **security-ownership-map** | 構成情報 | 責任範囲のマップ | 実際の運用体制との一致 |
| **security-threat-model** | 設計・API 仕様 | 脅威モデル | 前提の抜け、対策の実現性 |

> セキュリティ系の出力は**レビューの出発点**です。監査や公式なリスク評価の代替にはなりません。

### ドキュメント・データ処理

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **pdf** | PDF ファイル | 抽出データ・生成 PDF | 数値・表の抽出精度 |
| **jupyter-notebook** | データ、分析方針 | Notebook と分析結果 | 前提条件、統計処理の妥当性 |
| **openai-docs** | 知りたい仕様 | ドキュメントの該当箇所 | 参照バージョン（**System 層にも同梱**。上記参照） |
| **define-goal** | ぼんやりした要望 | 明確化されたゴール定義 | 認識のズレ |

### その他

| スキル | 入力 | 生成物 | 人が確認すべき点 |
|-------|------|-------|----------------|
| **linear** | Issue 内容 | Linear の Issue・更新 | 書き込み先プロジェクト |
| **sentry** | エラー情報 | エラー分析・対応方針 | 個人情報の取り扱い |
| **speech** | テキスト / 音声 | 音声・処理結果 | 用途と権利 |
| **transcribe** | 音声・動画 | 文字起こし | 固有名詞・数値の誤り |
| **hatch-pet** | — | デモ用の成果物 | 実験用（本番利用は想定外） |
| **yeet** | — | 汎用補助タスクの結果 | 実験用（本番利用は想定外） |

> Linear・Sentry 系は**外部アカウントとコネクタ設定**が必要です。

---

## Experimental（現在は存在しない）

以前は `skills/.experimental/` にコミュニティ提供の Skill があり、パスや URL で指定して入れる方式でした。**2026-10-16 時点で、このディレクトリはリポジトリにありません**（README の手順には記載が残っています）。Experimental の Skill を入れる手順は使えないものとして扱い、同等の Skill が必要なら `openai/plugins` や配布元のリポジトリを確認してください。

---

## カスタムスキルを作る

`$skill-creator` で対話的に作成できますが、手で書く場合の最小構成は次のとおりです。

```
my-skill/
├── SKILL.md        # 必須
├── scripts/        # ヘルパースクリプト（任意）
└── resources/      # 参照リソース（任意）
```

### SKILL.md テンプレート

```markdown
---
name: my-skill-name
description: |
  このスキルが何をするか、いつ使用するかの説明。
  Codex がいつ自動選択するかを決定します。
---

# スキル名

[Codex が実行する指示をここに記述]

## 手順
1. ステップ 1
2. ステップ 2

## ガイドライン
- ガイドライン 1
- ガイドライン 2
```

### フロントマターの必須フィールド

| フィールド | 説明 |
|----------|------|
| `name` | スキル識別子（小文字、スペースはハイフンに置換） |
| `description` | 機能と使用タイミングの説明。**Codex が自動選択する際の判断基準**になる |

### `description` の書き方

`description` の具体性が、自動選択の精度をそのまま左右します。

```yaml
# 良い例：いつ使うかが明確
description: |
  Vercel へのデプロイが必要なときに使用する。
  フロントエンドのビルド・設定確認・デプロイを自動化する。

# 悪い例：曖昧すぎる
description: デプロイスキル
```

---

## 関連ドキュメント

- [Codex ガイド](README.md) — インストール、最初に試すスキル、3 層の違い
- [Skills 最新動向](../trends.md) — `gh skill` など Skill の発見・配布・更新の仕組み

## 参考リンク

- [openai/skills リポジトリ](https://github.com/openai/skills) — 公式スキルカタログ（**2026-06-22 に deprecated**）
- [openai/plugins リポジトリ](https://github.com/openai/plugins) — 現行の Codex Plugin の例（公式）
- [Build skills](https://learn.chatgpt.com/docs/build-skills) — Skill の置き場所と作り方（公式。旧 developers.openai.com/codex/skills から転送）
- [Build plugins](https://developers.openai.com/codex/plugins/build) — Skill だけの Plugin の作り方と marketplace（公式）
