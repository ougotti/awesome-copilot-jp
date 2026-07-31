# OpenAI Codex 公式スキル（Agent Skills）

> **対象ツール**: Codex（OpenAI） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-01

> [openai/skills](https://github.com/openai/skills) は OpenAI が公開している Codex 用の公式スキルカタログです。エージェントがタスクを確実に実行できるよう、指示・スクリプト・リソースをフォルダにまとめた「スキル」が収録されています。

## スキルとは

Agent Skills は、AI エージェントが特定のタスクを確実に遂行するための**自己完結型ツールキット**です。指示・スクリプト・リソースをフォルダにまとめることで、Codex が適切なワークフローを再現可能な形で実行できるようになります。

```
my-skill/
├── SKILL.md        # スキルの指示書（必須）
├── scripts/        # ヘルパースクリプト（任意）
└── resources/      # 参照リソース（任意）
```

### GitHub Copilot Skills との違い

| | **openai/skills** | **GitHub Copilot Skills** |
|--|------------------|--------------------------|
| 対象ツール | OpenAI Codex CLI | GitHub Copilot |
| 形式 | `SKILL.md` + スクリプト | `SKILL.md` + 関連ファイル |
| 用途 | ターミナルエージェント向けワークフロー | Copilot チャットのテンプレート |
| 発見場所 | `.agents/skills/` ディレクトリ | `.github/skills/` に配置 |

---

## スキルの階層構造

`openai/skills` リポジトリはスキルを 3 層に分類しています。

| 階層 | ディレクトリ | 提供元 | 状態 | 説明 | インストール |
|-----|------------|-------|------|------|------------|
| **System** | `skills/.system/` | Official | GA | Codex に自動インストールされる基盤スキル | 不要（自動） |
| **Curated** | `skills/.curated/` | Official | GA | OpenAI が精選した高品質スキル | スキル名で指定 |
| **Experimental** | `skills/.experimental/` | Community | Experimental | コミュニティ提供の実験的スキル。仕様・品質は保証されない | パス / URL で指定 |

---

## System スキル（自動インストール）

Codex の最新バージョンに同梱され、手動インストール不要で利用できます。

### skill-installer

| 項目 | 内容 |
|-----|------|
| **機能** | Codex セッション内から他のスキルをインストール |
| **呼び出し** | `$skill-installer` |

**インストール方法 3 種：**

| 方法 | 説明 | 例 |
|-----|------|----|
| スキル名 | curated スキルを名前で指定 | `$skill-installer linear` |
| パス | experimental スキルをパスで指定 | `$skill-installer skills/.experimental/create-plan` |
| URL | GitHub URL で任意のスキルを指定 | `$skill-installer https://github.com/user/repo/tree/main/my-skill` |

> **注意:** インストール後は Codex を完全に終了して再起動しないとスキルが認識されません。

---

### skill-creator

| 項目 | 内容 |
|-----|------|
| **機能** | 新しいスキルの作成・修正を対話的に支援 |
| **呼び出し** | `$skill-creator` |

スキルの設計、`SKILL.md` の生成、テスト、最適化を一貫してサポートします。

---

### imagegen

| 項目 | 内容 |
|-----|------|
| **機能** | 画像生成 |
| **呼び出し** | `$imagegen` |

---

### openai-docs

| 項目 | 内容 |
|-----|------|
| **機能** | OpenAI ドキュメントの参照・検索 |
| **呼び出し** | `$openai-docs` |

---

### plugin-creator

| 項目 | 内容 |
|-----|------|
| **機能** | Codex プラグインの作成支援 |
| **呼び出し** | `$plugin-creator` |

---

## Curated スキル一覧

`$skill-installer <スキル名>` でインストールできます。

### 開発・コーディング

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **aspnet-core** | ASP.NET Core アプリケーションの開発 | .NET Web API 構築 |
| **cli-creator** | コマンドラインツールの作成 | CLI ユーティリティ開発 |
| **migrate-to-codex** | 既存プロジェクトを Codex 対応に移行 | Codex 導入時のセットアップ |
| **winui-app** | WinUI アプリケーション開発 | Windows デスクトップアプリ |
| **chatgpt-apps** | ChatGPT を使ったアプリ開発 | ChatGPT API 統合 |

**使用例：**
```
「aspnet-core スキルを使って、RESTful API を作成してください」
```

---

### デプロイ・インフラ

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **cloudflare-deploy** | Cloudflare Workers / Pages へのデプロイ | エッジコンピューティング |
| **netlify-deploy** | Netlify へのデプロイ | 静的サイト・JAMStack |
| **render-deploy** | Render へのデプロイ | バックエンドサービス |
| **vercel-deploy** | Vercel へのデプロイ | Next.js・フロントエンド |

**使用例：**
```
「vercel-deploy スキルを使って、このアプリを Vercel にデプロイしてください」
```

---

### GitHub 連携

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **gh-address-comments** | GitHub PR のコメントに対応 | コードレビュー対応 |
| **gh-fix-ci** | CI/CD パイプラインの修正 | ビルド失敗・テスト失敗の解消 |

**使用例：**
```
「gh-fix-ci スキルを使って、失敗している CI を修正してください」
```

---

### ブラウザ自動化・テスト

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **playwright** | Playwright を使ったブラウザ自動化 | E2E テスト・スクレイピング |
| **playwright-interactive** | Playwright のインタラクティブ操作 | リアルタイムブラウザ操作 |
| **screenshot** | スクリーンショット取得 | UI 確認・ビジュアルテスト |

**使用例：**
```
「playwright スキルを使って、localhost:3000 のログインフローをテストしてください」
```

---

### Figma 連携

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **figma** | Figma 基本操作 | デザインファイルの操作全般 |
| **figma-use** | Figma の活用 | デザイン参照・確認 |
| **figma-generate-design** | デザインの自動生成 | UI デザイン作成 |
| **figma-implement-design** | Figma デザインをコードに実装 | デザインのコード化 |
| **figma-create-design-system-rules** | デザインシステムルールの作成 | ブランドガイドライン整備 |
| **figma-create-new-file** | Figma ファイルの新規作成 | プロジェクト立ち上げ |
| **figma-generate-library** | デザインライブラリ生成 | コンポーネントライブラリ構築 |
| **figma-code-connect-components** | Figma と実装コードのリンク | デザインとコードの同期 |

**使用例：**
```
「figma-implement-design スキルを使って、このデザインを React コンポーネントに実装してください」
```

---

### Notion 連携

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **notion-knowledge-capture** | Notion への知識蓄積 | ドキュメント・メモの保存 |
| **notion-meeting-intelligence** | 会議情報の Notion 管理 | ミーティングメモの整理 |
| **notion-research-documentation** | 研究・調査の記録 | 技術調査レポートの作成 |
| **notion-spec-to-implementation** | Notion 仕様から実装へ | 仕様書に基づいたコード生成 |

**使用例：**
```
「notion-spec-to-implementation スキルを使って、Notion の仕様書をもとに実装してください」
```

---

### セキュリティ

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **security-best-practices** | セキュリティベストプラクティスの適用 | コードセキュリティ改善 |
| **security-ownership-map** | セキュリティ責任範囲のマッピング | セキュリティ体制の整理 |
| **security-threat-model** | 脅威モデルの作成 | セキュリティ設計・レビュー |

**使用例：**
```
「security-threat-model スキルを使って、この API の脅威モデルを作成してください」
```

---

### ドキュメント・データ処理

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **pdf** | PDF の処理・操作 | PDF からのデータ抽出・生成 |
| **jupyter-notebook** | Jupyter Notebook の操作 | データ分析・実験ノートブック |
| **openai-docs** | OpenAI ドキュメントの参照 | API 仕様確認 |
| **define-goal** | タスクゴールの定義 | プロジェクト要件の明確化 |

---

### その他

| スキル名 | 機能 | 使用場面 |
|---------|------|---------|
| **linear** | Linear でのプロジェクト管理 | Issue・プロジェクトの操作 |
| **sentry** | Sentry でのエラー監視 | エラー追跡・デバッグ |
| **speech** | 音声処理 | テキスト読み上げ・音声認識 |
| **transcribe** | 音声のテキスト化 | 会議録・動画の文字起こし |
| **hatch-pet** | ペットハッチングプロジェクト | デモ・実験用 |
| **yeet** | ユーティリティ機能 | 汎用補助タスク |

---

## スキルの呼び出し方

### 明示的な呼び出し

スキル名を `$` プレフィックスで指定します。

```
「$linear を使って、バグレポートの Issue を作成してください」
「$playwright で、フォームの送信テストを実行してください」
```

### 暗黙的な選択

タスクの内容からスキルの `description` と照合し、Codex が自動的に最適なスキルを選択します。

```
「Vercel にデプロイしてください」
→ Codex が自動的に $vercel-deploy を選択
```

---

## スキルの発見パス

Codex は以下の順序でスキルを探索します。

```
カレントディレクトリ
  └── .agents/skills/
親ディレクトリ（リポジトリルートまで）
  └── .agents/skills/
ユーザーレベル
  └── ~/.codex/skills/
システムレベル（自動インストール済み）
  └── ~/.codex/skills/.system/
```

---

## カスタムスキルの作成方法

### 基本構成

```
my-skill/
└── SKILL.md
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
| `description` | スキルの機能と使用タイミングの説明（Codex が自動選択の判断基準に使用） |

### 良い `description` の書き方

```yaml
# 良い例：いつ使うかが明確
description: |
  Vercel へのデプロイが必要なときに使用する。
  フロントエンドのビルド・設定確認・デプロイを自動化する。

# 悪い例：曖昧すぎる
description: デプロイスキル
```

### スクリプトの追加

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── deploy.sh     # デプロイスクリプト
│   └── validate.py   # バリデーション
└── resources/
    └── template.yaml
```

---

## インストール方法まとめ

### Codex CLI から

```bash
# curated スキルをスキル名で
$skill-installer linear

# experimental スキルをパスで
$skill-installer skills/.experimental/create-plan

# GitHub URL で任意のスキルを
$skill-installer https://github.com/user/repo/tree/main/my-skill
```

インストール後は **Codex を再起動** してスキルを認識させます。

### 手動インストール

```bash
# curated スキルを手動でコピー
cp -r skills/.curated/playwright ~/.codex/skills/

# リポジトリ共有スキルとして配置
mkdir -p .agents/skills/
cp -r my-skill .agents/skills/
```

---

## スキルのカテゴリまとめ

| カテゴリ | スキル |
|---------|-------|
| **システム（自動）** | skill-installer, skill-creator, imagegen, openai-docs, plugin-creator |
| **開発・コーディング** | aspnet-core, cli-creator, chatgpt-apps, winui-app, migrate-to-codex |
| **デプロイ** | cloudflare-deploy, netlify-deploy, render-deploy, vercel-deploy |
| **GitHub 連携** | gh-address-comments, gh-fix-ci |
| **ブラウザ自動化** | playwright, playwright-interactive, screenshot |
| **Figma** | figma, figma-use, figma-generate-design, figma-implement-design, figma-create-design-system-rules, figma-create-new-file, figma-generate-library, figma-code-connect-components |
| **Notion** | notion-knowledge-capture, notion-meeting-intelligence, notion-research-documentation, notion-spec-to-implementation |
| **セキュリティ** | security-best-practices, security-ownership-map, security-threat-model |
| **ドキュメント・データ** | pdf, jupyter-notebook, openai-docs, define-goal |
| **その他** | linear, sentry, speech, transcribe, hatch-pet, yeet |

---

## 参考リンク

- [openai/skills リポジトリ](https://github.com/openai/skills) — 公式スキルカタログ
- [Agent Skills – Codex 公式ドキュメント](https://developers.openai.com/codex/skills) — 公式スキル解説
- [openai/codex リポジトリ](https://github.com/openai/codex) — Codex CLI 本体
- [Codex CLI 公式ドキュメント](https://developers.openai.com/codex/cli) — CLI の使い方

---

> **注意**: Experimental スキルはコミュニティ提供であり、OpenAI による品質保証はありません。本番環境での使用前に十分な検証が必要です。
