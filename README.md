# GitHub Copilot カスタマイズ活用ガイド（日本語版）

> [github/awesome-copilot](https://github.com/github/awesome-copilot) リポジトリで公開されている GitHub Copilot のカスタマイズ機能を、日本語で体系的に解説するガイドです。

## 詳細ドキュメント

各カスタマイズの全ファイルを網羅した詳細ガイドはこちら：

| ドキュメント | 内容 |
|-------------|------|
| **[Instructions 一覧](docs/instructions.md)** | 168 個の Instructions ファイルの詳細解説 |
| **[Agents 一覧](docs/agents.md)** | 145 個の Agents ファイルの詳細解説 |
| **[Prompts 一覧](docs/prompts.md)** | 138 個の Prompts ファイルの詳細解説 |

## このガイドについて

GitHub Copilot はそのままでも強力なコーディングアシスタントですが、**カスタマイズ**を適用することで、チームのコーディング規約に合ったコードを生成させたり、特定のフレームワークに精通した専門家として振る舞わせたりできます。

このガイドでは、awesome-copilot リポジトリで提供されている 5 つのカスタマイズ手法について、**どのような場面で使えるか**を中心に解説します。

## カスタマイズの種類

| 種類 | ファイル形式 | 概要 | 適用タイミング |
|------|------------|------|--------------|
| [Instructions](#instructions---コーディング規約の自動適用) | `.instructions.md` | ファイルパターンに応じた規約を自動適用 | コード編集時に自動 |
| [Prompts](#prompts---再利用可能なタスクテンプレート) | `.prompt.md` | `/` コマンドで呼び出せるタスクテンプレート | チャットで手動実行 |
| [Agents](#agents---専門家ペルソナ) | `.agent.md` | 特定ドメインの専門家として振る舞うペルソナ | チャットで手動選択 |
| [Skills](#skills---リソース同梱の複合ツール) | `SKILL.md` + 関連ファイル | 関連リソースを同梱した自己完結型ツール | チャットで手動実行 |
| [Collections](#collections---カスタマイズのセット) | `.collection.yml` | 上記を組み合わせたキュレーション済みセット | プロジェクト単位で適用 |
| [Agentic Workflows](#agentic-workflows---ai-駆動のリポジトリ自動化) | `.md`（フロントマター + 自然言語） | GitHub Actions 上で動く AI 自動化ワークフロー | スケジュール・イベントで自動実行 |
| [Cookbook](#cookbook-recipes---実践的なコード例) | コードスニペット集 | Copilot SDK を使ったコピー＆ペーストですぐ使えるコード例 | 実装の参考として随時 |

---

## Instructions - コーディング規約の自動適用

### 概要

Instructions は、特定のファイルパターン（例: `*.py`, `*.tsx`）に対して、Copilot が従うべきコーディング規約やベストプラクティスを定義するものです。一度設定すれば、該当ファイルを編集するたびに自動的に適用されます。

### こんなときに使える

- **チームのコーディング規約を徹底したい** — レビューで毎回指摘する代わりに、Copilot が最初から規約に沿ったコードを生成する
- **特定フレームワークの推奨パターンを適用したい** — React の関数コンポーネントスタイルや、Python の型ヒント付きコードを標準にする
- **新人のオンボーディングを加速したい** — プロジェクト固有のパターンを Instructions に記述しておけば、初日から規約に沿ったコードが書ける

### 利用できる主な Instructions

#### プログラミング言語

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| **Python** | 型ヒント必須、docstring 形式、async/await パターン | Python プロジェクトの品質統一 |
| **TypeScript** | strict モード、import 整理、エラーハンドリング | フロントエンド/バックエンド TypeScript 開発 |
| **Java** | バージョン移行ガイド（11→17, 17→21, 21→25） | Java バージョンアップ対応 |
| **C#** | .NET 規約、null 安全性、LINQ パターン | .NET アプリケーション開発 |
| **Go** | エラーハンドリング、goroutine パターン | Go サービス開発 |
| **Rust** | 所有権パターン、Result 型の活用 | Rust プロジェクト |

#### Web フレームワーク

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| **React** | 関数コンポーネント、Hooks ベスト・プラクティス | React SPA 開発 |
| **Vue.js** | Composition API、リアクティビティパターン | Vue アプリケーション開発 |
| **Angular** | モジュール構成、RxJS パターン | Angular エンタープライズ開発 |
| **Next.js** | App Router、Server Components | Next.js フルスタック開発 |
| **Svelte** | ストア管理、コンポーネント設計 | Svelte アプリケーション開発 |
| **Blazor** | コンポーネントライフサイクル、状態管理 | .NET Web UI 開発 |

#### インフラ・DevOps

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| **Terraform** | モジュール構成、状態管理、命名規則 | IaC によるインフラ管理 |
| **Kubernetes** | マニフェスト構成、リソース制限 | K8s デプロイメント管理 |
| **GitHub Actions** | ワークフロー構成、セキュリティ設定 | CI/CD パイプライン構築 |
| **Docker** | マルチステージビルド、セキュリティ | コンテナイメージ最適化 |
| **Azure** | リソース命名、セキュリティ設定 | Azure クラウド構築 |

#### テスト

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| **Playwright** | E2E テストパターン、Page Object Model | ブラウザ自動テスト |
| **Vitest** | ユニットテスト構成、モック戦略 | Vite プロジェクトのテスト |
| **Pester** | PowerShell テストパターン | PowerShell スクリプトのテスト |

### 設定方法

Instructions ファイルをリポジトリの `.github/instructions/` ディレクトリに配置します。

```
.github/
  instructions/
    python.instructions.md      # *.py に自動適用
    react.instructions.md       # *.tsx, *.jsx に自動適用
    terraform.instructions.md   # *.tf に自動適用
```

ファイル先頭の YAML フロントマターで適用対象を指定します。

```yaml
---
applyTo: "**/*.py"
---
```

---

## Prompts - 再利用可能なタスクテンプレート

### 概要

Prompts は、Copilot Chat の `/` コマンドから呼び出せる再利用可能なタスクテンプレートです。繰り返し行う定型作業をテンプレート化することで、一貫した品質の出力を得られます。

### こんなときに使える

- **README やドキュメントを毎回同じ品質で作りたい** — テンプレート化されたプロンプトで、抜け漏れなくドキュメントを生成
- **コードレビューの観点を統一したい** — セキュリティ、パフォーマンス、保守性など、チーム共通のレビュー基準でチェック
- **テストコードの雛形を素早く作りたい** — フレームワーク固有のテスト構造を一発生成
- **定型的なコード生成を効率化したい** — API エンドポイント、データモデル、コンポーネントなどの雛形生成

### 利用できる主な Prompts

#### ドキュメント生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| **create-readme** | README.md の作成 | 新規プロジェクトの初期セットアップ |
| **create-spec** | 技術仕様書の作成 | 機能開発の設計フェーズ |
| **create-adr** | Architecture Decision Record の作成 | アーキテクチャ上の意思決定を記録 |
| **component-docs** | コンポーネントドキュメント | ライブラリ・UI コンポーネントの文書化 |

#### コード生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| **generate-springboot** | Spring Boot アプリ雛形生成 | Java バックエンド新規構築 |
| **generate-aspnet** | ASP.NET アプリ雛形生成 | .NET バックエンド新規構築 |
| **generate-nextjs** | Next.js アプリ雛形生成 | フルスタック Web アプリ構築 |
| **generate-python / go / rust / ...** | 言語別コード生成 | 各言語でのプロジェクト作成 |

#### テスト生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| **generate-jest-tests** | Jest テスト生成 | JavaScript/TypeScript ユニットテスト |
| **generate-junit-tests** | JUnit テスト生成 | Java ユニットテスト |
| **generate-playwright-tests** | Playwright テスト生成 | E2E テストの自動生成 |
| **generate-nunit-tests** | NUnit テスト生成 | .NET ユニットテスト |

#### インフラ・DevOps

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| **create-dockerfile** | Dockerfile 生成 | コンテナ化 |
| **create-github-actions** | GitHub Actions ワークフロー生成 | CI/CD セットアップ |
| **optimize-sql** | SQL クエリ最適化 | データベースパフォーマンス改善 |

#### 計画・設計

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| **create-epic-breakdown** | エピックの分解 | アジャイル開発の計画 |
| **create-implementation-plan** | 実装計画の作成 | 機能開発の計画フェーズ |
| **create-architecture-blueprint** | アーキテクチャ設計図 | システム設計 |

### 設定方法

Prompt ファイルをリポジトリの `.github/prompts/` ディレクトリに配置します。

```
.github/
  prompts/
    create-readme.prompt.md
    generate-jest-tests.prompt.md
```

Copilot Chat で `/create-readme` のように入力すると呼び出せます。

---

## Agents - 専門家ペルソナ

### 概要

Agents は、Copilot を特定ドメインの専門家として振る舞わせるペルソナ定義です。MCP（Model Context Protocol）サーバーと連携させることで、外部ツールやサービスと直接やり取りする能力を持たせることもできます。

### こんなときに使える

- **コードレビューを専門家の視点で行いたい** — セキュリティレビューア、パフォーマンスエキスパートとして分析
- **特定クラウドサービスの構築に詳しいアドバイザーが欲しい** — Azure、AWS などのアーキテクト視点でアドバイス
- **データベース設計の相談相手が欲しい** — PostgreSQL、MongoDB などの DBA として最適化の提案を受ける
- **メンターとして段階的に教えてほしい** — いきなり回答を出さず、考え方をガイドしてくれるメンター

### 利用できる主な Agents

#### コードの品質と開発プロセス

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| **code-reviewer** | コードレビューの専門家 | PR レビュー、コード品質向上 |
| **security-reviewer** | セキュリティレビューの専門家 | 脆弱性チェック、セキュリティ監査 |
| **technical-writer** | テクニカルライター | API ドキュメント、ユーザーガイド作成 |
| **mentor** | メンター・教育者 | 新人指導、学習支援 |
| **implementation-plan** | 実装計画策定者 | 機能設計、タスク分解 |

#### 言語・フレームワーク専門家

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| **python-expert** | Python 開発の専門家 | Python アプリ設計・最適化 |
| **csharp-expert / dotnet-expert** | C#/.NET の専門家 | .NET アプリ設計・最適化 |
| **java-expert** | Java 開発の専門家 | Java エンタープライズ開発 |
| **react-expert / nextjs-expert** | React/Next.js の専門家 | フロントエンド設計 |
| **rust-expert** | Rust 開発の専門家 | Rust システム開発 |

#### インフラ・クラウド

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| **azure-architect** | Azure アーキテクト | Azure 環境設計 |
| **kubernetes-sre** | Kubernetes SRE | K8s 運用・トラブルシュート |
| **terraform-expert** | Terraform の専門家 | IaC 設計・最適化 |

#### データベース

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| **postgresql-dba** | PostgreSQL DBA | DB 設計、クエリ最適化 |
| **mongodb-expert** | MongoDB の専門家 | NoSQL データモデリング |
| **mssql-dba** | SQL Server DBA | SQL Server 管理・最適化 |

#### パートナー提供エージェント

GitHub パートナー企業が提供する専門エージェントも利用可能です。

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| **Octopus Deploy** | デプロイ自動化 | CD パイプラインの最適化 |
| **LaunchDarkly** | フィーチャーフラグ管理 | 段階的リリース |
| **PagerDuty** | インシデント対応 | 障害対応の効率化 |
| **Dynatrace** | パフォーマンス監視 | APM 設定・分析 |
| **JFrog** | セキュリティスキャン | 依存関係の脆弱性管理 |

### 設定方法

Agent ファイルをリポジトリの `.github/agents/` ディレクトリに配置します。

```
.github/
  agents/
    code-reviewer.agent.md
    azure-architect.agent.md
```

Copilot Chat のエージェント選択で、ビルトインエージェントと並んで選択できるようになります。

---

## Skills - リソース同梱の複合ツール

### 概要

Skills は、Instructions だけでは実現できない、関連リソース（テンプレートファイル、設定ファイル、サンプルコードなど）を同梱した自己完結型のツールキットです。単一の `SKILL.md` ファイルに加えて、必要なファイル群をフォルダにまとめます。

### こんなときに使える

- **コミットメッセージを規約に沿って自動生成したい** — `git-commit` スキルがリポジトリの変更を分析して適切なメッセージを提案
- **GitHub Issues の作成を定型化したい** — `github-issues` スキルでテンプレートに沿った Issue を素早く作成
- **アーキテクチャ図を自動生成したい** — `excalidraw-diagram-generator` や `plantuml-ascii` でコードからダイアグラムを生成
- **PRD（プロダクト要件定義書）を標準フォーマットで作りたい** — `prd` スキルで統一的な要件定義書を作成
- **コードリファクタリングの手順を体系化したい** — `refactor` スキルでリファクタリングのベストプラクティスを適用

### 利用できる主な Skills

#### 開発ワークフロー

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **git-commit** | コミットメッセージ自動生成 | 日常のコミット作業 |
| **github-issues** | GitHub Issue の作成支援 | バグ報告・機能要求の整理 |
| **gh-cli** | GitHub CLI 操作支援 | GitHub リポジトリ操作 |
| **make-repo-contribution** | リポジトリ貢献ワークフロー | OSS コントリビューション |
| **refactor** | コードリファクタリング支援 | コード品質改善 |

#### ドキュメント・設計

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **prd** | プロダクト要件定義書作成 | 新機能の要件定義 |
| **meeting-minutes** | 議事録作成支援 | ミーティングの記録 |
| **excalidraw-diagram-generator** | 図表自動生成 | アーキテクチャ図の作成 |
| **plantuml-ascii** | PlantUML ダイアグラム生成 | シーケンス図・クラス図の作成 |
| **markdown-to-html** | Markdown から HTML への変換 | ドキュメント公開 |

#### クラウド・インフラ

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **azure-deployment-preflight** | Azure デプロイ事前チェック | デプロイ前の検証 |
| **azure-resource-visualizer** | Azure リソース可視化 | インフラ構成の把握 |
| **azure-role-selector** | Azure ロール選択支援 | RBAC 設定 |
| **azure-static-web-apps** | Azure Static Web Apps 構成 | 静的サイトのデプロイ |
| **terraform-azurerm-set-diff-analyzer** | Terraform 差分分析 | IaC 変更の影響確認 |

#### テスト・品質

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **webapp-testing** | Web アプリテスト支援 | E2E テスト・統合テスト |
| **agentic-eval** | エージェント評価 | AI エージェントの品質検証 |
| **web-design-reviewer** | Web デザインレビュー | UI/UX の品質チェック |
| **scoutqa-test** | QA テスト支援 | 品質保証テスト |

#### ツール連携

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **chrome-devtools** | Chrome DevTools 連携 | フロントエンドデバッグ |
| **image-manipulation-image-magick** | 画像処理 | 画像の変換・加工 |
| **vscode-ext-commands** | VS Code 拡張コマンド | エディタ操作の自動化 |
| **nuget-manager** | NuGet パッケージ管理 | .NET 依存関係管理 |

### 設定方法

Skills はフォルダ単位で `.github/skills/` ディレクトリに配置します。

```
.github/
  skills/
    git-commit/
      SKILL.md           # スキルの定義
      commit-template.md # 同梱テンプレート
    prd/
      SKILL.md
      template.md
```

---

## Collections - カスタマイズのセット

### 概要

Collections は、関連する Instructions、Prompts、Agents、Skills をテーマごとにまとめたキュレーション済みのセットです。特定の技術スタックやワークフロー向けに最適化された組み合わせを一括で導入できます。

### こんなときに使える

- **新規プロジェクトのセットアップを効率化したい** — 技術スタックに合った Collection を選ぶだけで、必要なカスタマイズ一式が揃う
- **チーム全体の開発環境を統一したい** — Collection を共有すれば、全員が同じルールとツールを使える
- **特定ドメインのベストプラクティスを一括導入したい** — セキュリティ、DevOps、テストなど、分野ごとの知見を網羅的に適用

### 利用できる主な Collections

#### 言語・フレームワーク別

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **java-development** | Java の Instructions + Prompts + Agents | Java プロジェクト全般 |
| **csharp-dotnet-development** | C#/.NET の全カスタマイズ | .NET プロジェクト全般 |
| **frontend-web-dev** | フロントエンド開発の全カスタマイズ | Web フロントエンド開発 |

#### MCP 開発

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **python-mcp-development** | Python MCP サーバー開発用一式 | Python で MCP サーバーを構築 |
| **typescript-mcp-development** | TypeScript MCP サーバー開発用一式 | TypeScript で MCP サーバーを構築 |
| **go-mcp-development** | Go MCP サーバー開発用一式 | Go で MCP サーバーを構築 |
| **csharp-mcp-development** | C# MCP サーバー開発用一式 | C# で MCP サーバーを構築 |

#### 業務プロセス

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **project-planning** | 計画・設計用カスタマイズ | プロジェクト計画フェーズ |
| **testing-automation** | テスト自動化カスタマイズ | テスト戦略の導入 |
| **security-best-practices** | セキュリティカスタマイズ | セキュリティ対策の強化 |
| **devops-oncall** | オンコール対応カスタマイズ | 運用・障害対応 |
| **software-engineering-team** | チーム開発カスタマイズ | 開発チーム全体の標準化 |

#### データ・クラウド

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **database-data-management** | DB 管理カスタマイズ | データベース設計・運用 |
| **azure-cloud-development** | Azure 開発カスタマイズ | Azure クラウド開発 |
| **power-bi-development** | Power BI カスタマイズ | BI レポート開発 |

### 設定方法

Collection ファイルをリポジトリの `.github/collections/` ディレクトリに配置します。

```yaml
# .github/collections/java-development.collection.yml
name: Java Development
description: Java 開発に必要なカスタマイズ一式
items:
  - instructions/java.instructions.md
  - prompts/generate-java.prompt.md
  - agents/java-expert.agent.md
```

---

## Agentic Workflows - AI 駆動のリポジトリ自動化

### 概要

Agentic Workflows は、GitHub Actions 上でコーディングエージェントを実行する AI 駆動のリポジトリ自動化の仕組みです。自然言語の指示をフロントマター付きの Markdown ファイルで定義し、スケジュールやイベントを起点に自動実行できます。セキュリティファーストな設計とガードレールを備えています。

### こんなときに使える

- **Issue のトリアージ・ラベリングを自動化したい** — 新しい Issue を自動で分類し、適切なラベルを付与
- **定期的なステータスレポートを生成したい** — 毎日・毎週の進捗サマリーを自動作成して Issue に投稿
- **ドキュメントを常に最新に保ちたい** — コード変更に合わせて自動でドキュメントを更新
- **スラッシュコマンドで操作したい** — Issue や PR にコメントするだけでエージェントを呼び出せる
- **コード品質チェックを定期実行したい** — スケジュールに従って自動でコードレビューや品質検証を実施

### 利用できる主な Agentic Workflows

| ワークフロー名 | 概要 | トリガー |
|--------------|------|---------|
| **daily-issues-report** | 未解決 Issue と最近のアクティビティの日次サマリーを Issue として投稿 | schedule |
| **ospo-contributors-report** | 組織全体のコントリビューター活動状況の月次レポート | schedule, workflow_dispatch |
| **ospo-org-health** | ステール Issue/PR・マージ時間・コントリビューターランキングなどを含む週次ヘルスレポート | schedule, workflow_dispatch |
| **ospo-stale-repos** | 非アクティブなリポジトリを特定しアーカイブ候補レポートを生成 | schedule, workflow_dispatch |
| **ospo-release-compliance-checker** | OSS リリース要件に対するコンプライアンスチェックをレポートとして Issue に投稿 | issues, workflow_dispatch |
| **relevance-check** | Issue や PR がプロジェクトに関連するかをスラッシュコマンドで評価 | slash_command |
| **relevance-summary** | `/relevance-check` 回答済みの未解決 Issue/PR を1つの Issue にまとめてレポート | workflow_dispatch |

### 設定方法

`gh aw` CLI 拡張機能を使って導入します。

```bash
# gh aw 拡張機能をインストール
gh extension install github/gh-aw

# ワークフロー .md ファイルをリポジトリの .github/workflows/ に配置後、
# .lock.yml ファイルにコンパイル
gh aw compile

# 手動実行
gh aw run <workflow-name>
```

```
.github/
  workflows/
    daily-issues-report.md       # ワークフロー定義（自然言語 + フロントマター）
    daily-issues-report.lock.yml # コンパイル済み GitHub Actions ファイル
```

---

## Cookbook Recipes - 実践的なコード例

### 概要

Cookbook Recipes は、GitHub Copilot SDK を使ったアプリケーション開発のための実践的なコードスニペット集です。コピー＆ペーストですぐに動作する、現実のユースケースに基づいたコード例が提供されています。

### こんなときに使える

- **Copilot SDK を使ったアプリケーションを初めて作る** — 言語別のスターターコードで素早く開始
- **エラーハンドリングのパターンを知りたい** — 実践的なエラー処理の例を参照
- **セッション管理の実装方法を知りたい** — ユーザーセッションの管理パターンを学べる

### 対応言語

| 言語 | 提供される例 |
|------|------------|
| **.NET (C#)** | SDK セットアップ、エラーハンドリング、セッション管理 |
| **Go** | SDK セットアップ、ファイル操作、ベストプラクティス |
| **Node.js (TypeScript)** | SDK セットアップ、非同期処理、ストリーミング |
| **Python** | SDK セットアップ、エラーハンドリング、統合パターン |

---

## クイックスタートガイド

### 1. 最小構成で始める

まずは Instructions から始めるのが最もシンプルです。

```
.github/
  instructions/
    python.instructions.md
```

```markdown
---
applyTo: "**/*.py"
---

# Python コーディング規約

- すべての関数に型ヒントを付与すること
- docstring は Google スタイルで記述すること
- テストは pytest を使用すること
- import は isort で整理すること
```

### 2. チーム向けの推奨構成

チーム開発では、Instructions + Prompts + Agents の組み合わせが効果的です。

```
.github/
  instructions/
    python.instructions.md        # コーディング規約
    typescript.instructions.md     # フロントエンド規約
    terraform.instructions.md      # IaC 規約
  prompts/
    create-readme.prompt.md        # README 生成
    generate-tests.prompt.md       # テスト生成
    create-github-actions.prompt.md # CI/CD セットアップ
  agents/
    code-reviewer.agent.md         # コードレビュー
    security-reviewer.agent.md     # セキュリティレビュー
```

### 3. awesome-copilot から導入する

awesome-copilot リポジトリの MCP サーバーを使うと、カスタマイズの検索・インストールを VS Code から直接行えます。

1. VS Code で MCP サーバーを設定
2. Copilot Chat で `@awesome-copilot` に利用したいカスタマイズを相談
3. 選んだカスタマイズをワンクリックでインストール

---

## よくある質問

### Q: Instructions と Agents の違いは？

**Instructions** はファイルパターンに応じて**自動的に**適用されるルールです。コードを書いているだけで効果を発揮します。一方、**Agents** はチャットで**明示的に選択**して使う専門家ペルソナです。対話的に質問や相談をしたいときに使います。

### Q: 既存のプロジェクトにも適用できる？

はい。`.github/` ディレクトリにファイルを追加するだけで、既存プロジェクトにも適用できます。コードベースへの変更は不要です。

### Q: カスタマイズは Copilot のどのプランで使える？

Instructions、Prompts、Agents は GitHub Copilot のすべてのプラン（Individual、Business、Enterprise）で利用可能です。ただし、MCP サーバー連携などの一部機能は対応するエディタバージョンが必要です。

### Q: 自分でカスタマイズを作るには？

awesome-copilot リポジトリの [CONTRIBUTING.md](https://github.com/github/awesome-copilot/blob/main/CONTRIBUTING.md) に詳しいガイドラインがあります。基本的には、規定のファイル形式（`.instructions.md`、`.prompt.md`、`.agent.md`）に従ってマークダウンファイルを作成します。

### Q: チームで共有するには？

カスタマイズファイルをリポジトリの `.github/` ディレクトリにコミットするだけで、リポジトリにアクセスできるチームメンバー全員に自動的に適用されます。

---

## 参考リンク

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — カスタマイズの公式リポジトリ
- [GitHub Copilot ドキュメント](https://docs.github.com/copilot) — 公式ドキュメント
- [Copilot のカスタマイズ方法](https://docs.github.com/copilot/customizing-copilot) — 公式カスタマイズガイド
- [Agentic Workflows ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.workflows.md) — AI 駆動ワークフローの一覧と使い方
- [Cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/README.md) — Copilot SDK を活用した実践的コードレシピ集

---

> **注意**: このガイドは [github/awesome-copilot](https://github.com/github/awesome-copilot) リポジトリの内容を元に作成しています。GitHub はこれらのカスタマイズの機能やセキュリティを保証するものではありません。利用前にカスタマイズの内容を確認してください。
