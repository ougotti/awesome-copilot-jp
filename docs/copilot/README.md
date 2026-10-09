# GitHub Copilot ガイド

> **対象ツール**: GitHub Copilot ｜ **実行環境**: Chat UI（github.com / Mobile）／ IDE（VS Code 等）／ CLI ／ Cloud（cloud agent） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-10-10

GitHub Copilot は GitHub が提供するコーディングアシスタントで、IDE 内のインライン補完・チャットが中心です。このページでは、Copilot のカスタマイズの種類と設定方法、クイックスタートを解説します。

## このディレクトリのドキュメント

| ドキュメント | 内容 |
|-------------|------|
| **[Instructions 一覧](instructions.md)** | ファイルパターンに応じてコーディング規約を自動適用するルールファイルの詳細解説 |
| **[Agents 一覧](agents.md)** | Copilot を特定ドメインの専門家ペルソナとして振る舞わせるエージェント定義の詳細解説 |
| **[Prompts / Skills 一覧](prompts.md)** | `/` コマンドから呼び出せる再利用可能なタスクテンプレートおよび Skills の詳細解説 |
| **[Plugins](plugins.md)** | Agents / Skills / Hooks / MCP / LSP を 1 つの単位で配布する Plugin と Marketplace の詳細解説 |
| **[VS Code エディタウィンドウでの複数ルート運用](multi-root.md)** | 複数フォルダ（multi-root workspace）を横断するエージェントセッションの設定・hooks の読み込み元・確認手順（Experimental） |

---

## カスタマイズの種類

| 種類 | ファイル形式 | 実行環境 | 状態 | 概要 | 適用タイミング |
|------|------------|---------|------|------|--------------|
| [Instructions](#instructions---コーディング規約の自動適用) | `.instructions.md` | IDE | GA | ファイルパターンに応じた規約を自動適用 | コード編集時に自動 |
| [Prompts](#prompts---再利用可能なタスクテンプレート) | `.prompt.md` | IDE | GA | VS Code などで `/` コマンドから呼び出すローカルのタスクテンプレート | チャットで手動実行 |
| [Agents](#agents---専門家ペルソナ) | `.agent.md` | IDE / CLI | GA | 特定ドメインの専門家として振る舞うペルソナ | チャットで手動選択 |
| [Skills](#skills---リソース同梱の複合ツール) | `SKILL.md` + 関連ファイル | IDE / CLI | GA | upstream の `skills/` で公開される、関連リソース同梱の自己完結型ツール | チャットで手動実行 |
| [Collections](#collections---カスタマイズのセット) | `.collection.yml` | IDE | GA | 上記を組み合わせたキュレーション済みセット | プロジェクト単位で適用 |
| [Plugins](#plugins---拡張をまとめた配布単位) | `plugin.json` + 各要素 | CLI / IDE | GA | Agents / Skills / Hooks / MCP / LSP をまとめて配布・更新する単位 | インストール後は常時有効 |
| [Hooks](#hooks---セッションイベント駆動の自動アクション) | `hooks.json` + スクリプト | Cloud（コーディングエージェント） | GA | Copilot コーディングエージェントのセッションイベントで自動実行 | エージェントセッション中に自動 |
| [Agentic Workflows](#agentic-workflows---ai-駆動のリポジトリ自動化) | `.md`（フロントマター + 自然言語） | Cloud（GitHub Actions） | GA | GitHub Actions 上で動く AI 自動化ワークフロー | スケジュール・イベントで自動実行 |
| [Cookbook](#cookbook-recipes---実践的なコード例) | コードスニペット集 | — | GA | Copilot SDK を使ったコピー＆ペーストですぐ使えるコード例 | 実装の参考として随時 |

> 表記の意味は [情報ラベルの読み方](../../README.md#情報ラベルの読み方) を参照してください。upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) が配布するカスタマイズはすべて `Official`（GitHub 公式）です。

> **補足**: upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) では、Prompts のカタログは **[skills/](https://github.com/github/awesome-copilot/tree/main/skills)** に移行済みです。ローカルでは `.prompt.md` を使い続けられますが、このページの upstream 参照リンクは `xxx.prompt.md` 表記で skills/ を指しています。

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
| [**C#**](https://github.com/github/awesome-copilot/blob/main/instructions/csharp.instructions.md) | .NET 規約、null 安全性、LINQ パターン | .NET アプリケーション開発 |
| [**Go**](https://github.com/github/awesome-copilot/blob/main/instructions/go.instructions.md) | エラーハンドリング、goroutine パターン | Go サービス開発 |
| [**Rust**](https://github.com/github/awesome-copilot/blob/main/instructions/rust.instructions.md) | 所有権パターン、Result 型の活用 | Rust プロジェクト |

#### Web フレームワーク

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Next.js**](https://github.com/github/awesome-copilot/blob/main/instructions/nextjs.instructions.md) | App Router、Server Components | Next.js フルスタック開発 |
| [**Svelte**](https://github.com/github/awesome-copilot/blob/main/instructions/svelte.instructions.md) | ストア管理、コンポーネント設計 | Svelte アプリケーション開発 |
| [**Blazor**](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | コンポーネントライフサイクル、状態管理 | .NET Web UI 開発 |

#### インフラ・DevOps

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Terraform**](https://github.com/github/awesome-copilot/blob/main/instructions/terraform.instructions.md) | モジュール構成、状態管理、命名規則 | IaC によるインフラ管理 |
| [**Kubernetes**](https://github.com/github/awesome-copilot/blob/main/instructions/kubernetes-manifests.instructions.md) | マニフェスト構成、リソース制限 | K8s デプロイメント管理 |
| [**GitHub Actions**](https://github.com/github/awesome-copilot/blob/main/instructions/github-actions-ci-cd-best-practices.instructions.md) | ワークフロー構成、セキュリティ設定 | CI/CD パイプライン構築 |
| [**Docker**](https://github.com/github/awesome-copilot/blob/main/instructions/containerization-docker-best-practices.instructions.md) | マルチステージビルド、セキュリティ | コンテナイメージ最適化 |
| [**Azure**](https://github.com/github/awesome-copilot/tree/main/instructions) | リソース命名、セキュリティ設定 | Azure クラウド構築 |

#### テスト

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Playwright**](https://github.com/github/awesome-copilot/blob/main/instructions/playwright-typescript.instructions.md) | E2E テストパターン、Page Object Model | ブラウザ自動テスト |
| [**Vitest**](https://github.com/github/awesome-copilot/blob/main/instructions/nodejs-javascript-vitest.instructions.md) | ユニットテスト構成、モック戦略 | Vite プロジェクトのテスト |
| [**Pester**](https://github.com/github/awesome-copilot/blob/main/instructions/powershell-pester-5.instructions.md) | PowerShell テストパターン | PowerShell スクリプトのテスト |

### 設定方法

Instructions ファイルをリポジトリの `.github/instructions/` ディレクトリに配置します。

```
.github/
  instructions/
    go.instructions.md          # *.go に自動適用
    nextjs.instructions.md      # *.tsx, *.jsx に自動適用
    terraform.instructions.md   # *.tf に自動適用
```

ファイル先頭の YAML フロントマターで適用対象を指定します。

```yaml
---
applyTo: "**/*.py"
---
```

**→ 全 Instructions の詳細は [instructions.md](instructions.md) を参照**

---

## Prompts - 再利用可能なタスクテンプレート

### 概要

Prompts は、Copilot Chat の `/` コマンドから呼び出せる再利用可能なタスクテンプレートです。繰り返し行う定型作業をテンプレート化することで、一貫した品質の出力を得られます。

> **注意**: upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) では、Prompts は **[Skills](https://github.com/github/awesome-copilot/tree/main/skills)** に移行されました。VS Code などのローカル機能では `.prompt.md` を `.github/prompts/` に置く運用が残っていますが、以下のリンクは現在の Skills ディレクトリを参照しています。

### こんなときに使える

- **README やドキュメントを毎回同じ品質で作りたい** — テンプレート化されたプロンプトで、抜け漏れなくドキュメントを生成
- **コードレビューの観点を統一したい** — セキュリティ、パフォーマンス、保守性など、チーム共通のレビュー基準でチェック
- **テストコードの雛形を素早く作りたい** — フレームワーク固有のテスト構造を一発生成
- **定型的なコード生成を効率化したい** — API エンドポイント、データモデル、コンポーネントなどの雛形生成

### 利用できる主な Prompts

#### ドキュメント生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**create-readme.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-readme) | README.md の作成 | 新規プロジェクトの初期セットアップ |
| [**create-specification.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-specification) | 技術仕様書の作成 | 機能開発の設計フェーズ |
| [**create-architectural-decision-record.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-architectural-decision-record) | Architecture Decision Record の作成 | アーキテクチャ上の意思決定を記録 |

#### テスト生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**javascript-typescript-jest.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/javascript-typescript-jest) | Jest テスト生成 | JavaScript/TypeScript ユニットテスト |
| [**java-junit.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/java-junit) | JUnit テスト生成 | Java ユニットテスト |
| [**playwright-generate-test.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/playwright-generate-test) | Playwright テスト生成 | E2E テストの自動生成 |
| [**csharp-nunit.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/csharp-nunit) | NUnit テスト生成 | .NET ユニットテスト |

#### インフラ・DevOps

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**multi-stage-dockerfile.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/multi-stage-dockerfile) | Dockerfile 生成 | コンテナ化 |
| [**create-github-action-workflow-specification.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-github-action-workflow-specification) | GitHub Actions ワークフロー生成 | CI/CD セットアップ |
| [**sql-optimization.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/sql-optimization) | SQL クエリ最適化 | データベースパフォーマンス改善 |

### 設定方法

VS Code などのローカルカスタマイズでは、Prompt ファイルをリポジトリの `.github/prompts/` ディレクトリに配置します。

```
.github/
  prompts/
    create-readme.prompt.md
    generate-jest-tests.prompt.md
```

Copilot Chat で `/create-readme` のように入力すると呼び出せます。

**→ 全 Prompts / Skills の詳細は [prompts.md](prompts.md) を参照**

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
| [**code-reviewer**](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md) | コードレビューの専門家 | PR レビュー、コード品質向上 |
| [**security-reviewer**](https://github.com/github/awesome-copilot/blob/main/agents/se-security-reviewer.agent.md) | セキュリティレビューの専門家 | 脆弱性チェック、セキュリティ監査 |
| [**technical-writer**](https://github.com/github/awesome-copilot/blob/main/agents/se-technical-writer.agent.md) | テクニカルライター | API ドキュメント、ユーザーガイド作成 |
| [**mentor**](https://github.com/github/awesome-copilot/blob/main/agents/mentor.agent.md) | メンター・教育者 | 新人指導、学習支援 |

#### インフラ・クラウド

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| [**azure-architect**](https://github.com/github/awesome-copilot/blob/main/agents/azure-principal-architect.agent.md) | Azure アーキテクト | Azure 環境設計 |
| [**kubernetes-sre**](https://github.com/github/awesome-copilot/blob/main/agents/platform-sre-kubernetes.agent.md) | Kubernetes SRE | K8s 運用・トラブルシュート |
| [**terraform-expert**](https://github.com/github/awesome-copilot/blob/main/agents/terraform.agent.md) | Terraform の専門家 | IaC 設計・最適化 |

### 設定方法

Agent ファイルをリポジトリの `.github/agents/` ディレクトリに配置します。

```
.github/
  agents/
    code-reviewer.agent.md
    azure-architect.agent.md
```

**→ 全 Agents の詳細は [agents.md](agents.md) を参照**

---

## Skills - リソース同梱の複合ツール

### 概要

Skills は、Instructions だけでは実現できない、関連リソース（テンプレートファイル、設定ファイル、サンプルコードなど）を同梱した自己完結型のツールキットです。

### こんなときに使える

- **コミットメッセージを規約に沿って自動生成したい** — `git-commit` スキルがリポジトリの変更を分析して適切なメッセージを提案
- **アーキテクチャ図を自動生成したい** — `excalidraw-diagram-generator` や `plantuml-ascii` でコードからダイアグラムを生成
- **PRD（プロダクト要件定義書）を標準フォーマットで作りたい** — `prd` スキルで統一的な要件定義書を作成

### 利用できる主な Skills

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **git-commit** | コミットメッセージ自動生成 | 日常のコミット作業 |
| **github-issues** | GitHub Issue の作成支援 | バグ報告・機能要求の整理 |
| **prd** | プロダクト要件定義書作成 | 新機能の要件定義 |
| **excalidraw-diagram-generator** | 図表自動生成 | アーキテクチャ図の作成 |
| **azure-deployment-preflight** | Azure デプロイ事前チェック | デプロイ前の検証 |

### 設定方法

```
.github/
  skills/
    git-commit/
      SKILL.md
    prd/
      SKILL.md
      template.md
```

---

## Collections - カスタマイズのセット

### 概要

Collections は、関連する Instructions、Prompts、Agents、Skills をテーマごとにまとめたキュレーション済みのセットです。

### こんなときに使える

- **新規プロジェクトのセットアップを効率化したい** — 技術スタックに合った Collection を選ぶだけで必要なカスタマイズ一式が揃う
- **チーム全体の開発環境を統一したい** — Collection を共有すれば全員が同じルールとツールを使える

### 利用できる主な Collections

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **java-development** | Java の Instructions + Prompts + Agents | Java プロジェクト全般 |
| **csharp-dotnet-development** | C#/.NET の全カスタマイズ | .NET プロジェクト全般 |
| **python-mcp-development** | Python MCP サーバー開発用一式 | Python で MCP サーバーを構築 |
| **security-best-practices** | セキュリティカスタマイズ | セキュリティ対策の強化 |
| **devops-oncall** | オンコール対応カスタマイズ | 運用・障害対応 |

### 設定方法

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

## Plugins - 拡張をまとめた配布単位

### 概要

Plugins は、Custom Agents・Skills・Hooks・MCP サーバー設定・LSP サーバー設定を `plugin.json` で 1 つにまとめ、Marketplace 経由で配布・更新する仕組みです。Collections が「カスタマイズの推奨セット」を示すのに対し、Plugins は **インストールと更新の単位そのもの** です。

### こんなときに使える

- **チーム標準の拡張一式を配りたい** — Skill だけでなく、Hooks や MCP 接続設定まで含めて 1 コマンドで揃える
- **リポジトリごとに必要な拡張を固定したい** — `.github/copilot/settings.json` の `enabledPlugins` に書けば、クローンした開発者全員に同じ構成が適用される
- **組織で使える拡張を制限したい** — Enterprise の managed settings で、許可する Plugin を統制する

### 導入方法

```powershell
copilot plugin marketplace list
copilot plugin marketplace browse awesome-copilot
copilot plugin install database-data-management@awesome-copilot
copilot plugin update database-data-management
```

Copilot CLI には `copilot-plugins`（GitHub 公式コレクション）と `awesome-copilot` の 2 つの Marketplace が既定で登録されています。VS Code の **Agent plugins** は 2026-08-12 に一般提供となり、Copilot CLI・Copilot SDK・Copilot アプリと合わせて全 Copilot プランで使えます。

同じ発表で、マルチベンダー共通の **Agent Plugins 1.0.0** への対応も一般提供となりました。ただし Copilot Plugin を書けば自動的に他エージェントへ持ち出せるわけではなく、`plugin.json` に `$schema` を書いて可搬形式へオプトインしたものだけが対象です。

**→ 構成・Marketplace の作り方・Claude Code Plugin との比較は [plugins.md](plugins.md) を参照**
**→ 可搬形式と Copilot 独自形式の選び分けは [plugins.md の「2 つの形式」](plugins.md#2-つの形式可搬形式とツール独自形式)、インストール前に可搬かを判定する手順は [プラグインの可搬性](../dev-methods/plugin-portability.md) を参照**

---

## Hooks - セッションイベント駆動の自動アクション

### 概要

Hooks は、GitHub Copilot コーディングエージェントのセッション中に発生する特定のイベントをトリガーとして自動実行されるスクリプトです。

### こんなときに使える

- **セッションのログ・監査証跡を残したい** — セッション開始・終了・プロンプトを自動記録
- **危険な操作を事前にブロックしたい** — 破壊的ファイル操作や force push などをエージェントが実行する前に遮断
- **シークレットの漏洩を防ぎたい** — セッション中に変更されたファイルを自動スキャン

### 利用できる主な Hooks

| フック名 | 概要 | 対応イベント |
|---------|------|------------|
| [**dependency-license-checker**](https://github.com/github/awesome-copilot/tree/main/hooks/dependency-license-checker) | 新規追加依存関係のライセンスコンプライアンスチェック | sessionEnd |
| [**secrets-scanner**](https://github.com/github/awesome-copilot/tree/main/hooks/secrets-scanner) | セッション中に変更されたファイルのシークレット検出 | sessionEnd |
| [**session-auto-commit**](https://github.com/github/awesome-copilot/tree/main/hooks/session-auto-commit) | セッション終了時に変更を自動コミット＆プッシュ | sessionEnd |
| [**tool-guardian**](https://github.com/github/awesome-copilot/tree/main/hooks/tool-guardian) | 危険なツール操作（破壊的ファイル操作、force push）をブロック | preToolUse |

### 設定方法

```
.github/
  hooks/
    session-auto-commit/
      hooks.json
      auto-commit.sh
```

---

## Agentic Workflows - AI 駆動のリポジトリ自動化

### 概要

Agentic Workflows は、GitHub Actions 上でコーディングエージェントを実行する AI 駆動のリポジトリ自動化の仕組みです。

### こんなときに使える

- **Issue のトリアージ・ラベリングを自動化したい** — 新しい Issue を自動で分類し、適切なラベルを付与
- **定期的なステータスレポートを生成したい** — 毎日・毎週の進捗サマリーを自動作成
- **スラッシュコマンドで操作したい** — Issue や PR にコメントするだけでエージェントを呼び出せる

### 利用できる主な Agentic Workflows

| ワークフロー名 | 概要 | トリガー |
|--------------|------|---------|
| [**daily-issues-report**](https://github.com/github/awesome-copilot/blob/main/workflows/daily-issues-report.md) | 未解決 Issue の日次サマリーを Issue に投稿 | schedule |
| [**ospo-org-health**](https://github.com/github/awesome-copilot/blob/main/workflows/ospo-org-health.md) | ステール Issue/PR・コントリビューターランキングの週次レポート | schedule |
| [**relevance-check**](https://github.com/github/awesome-copilot/blob/main/workflows/relevance-check.md) | Issue や PR がプロジェクトに関連するかをスラッシュコマンドで評価 | slash_command |

### 設定方法

```bash
# gh aw 拡張機能をインストール
gh extension install github/gh-aw

# ワークフロー定義ファイルをコンパイル
gh aw compile
```

---

## Cookbook Recipes - 実践的なコード例

### 概要

Cookbook Recipes は、GitHub Copilot SDK を使ったアプリケーション開発のための実践的なコードスニペット集です。

### 対応言語

| 言語 | 提供される例 |
|------|------------|
| **.NET (C#)** | SDK セットアップ、エラーハンドリング、セッション管理 |
| **Go** | SDK セットアップ、ファイル操作、ベストプラクティス |
| **Node.js (TypeScript)** | SDK セットアップ、非同期処理、ストリーミング |
| **Python** | SDK セットアップ、エラーハンドリング、統合パターン |

---

## Automations — エージェントタスクを定期実行する

VS Code 1.137（2026-09-09）で追加された **Automations** は、1.138（2026-09-16）で共有用ファイルの export / import に対応しました。保存した prompt、workspace、agent / model / permission options、schedule を使い、Agents ウィンドウから同じタスクを繰り返し実行します。

> **状態は Preview です。** 1.138 release notes は「既定で有効」と案内していますが、現行の Automations ドキュメントは段階的ロールアウト中で、Stable は既定オフ、Insiders は既定オンとしています。利用面・ロールアウト時点で差があるため、GA と扱わず `chat.automations.enabled` と表示有無を確認してください。

1. Settings で `chat.automations.enabled` を有効にする
2. Agents ウィンドウ → Automations → Create Automation を開く
3. prompt、workspace、agent、model、permission options を指定する
4. Git workspace で agent が対応していれば New Worktree と基準ブランチを選ぶ
5. 最初は **Manual** で保存し、`Run now` の結果と承認要求を History で確認する
6. 確認後に Hourly / Daily / Weekly を選び、Enabled にする

Automation はローカルで動きます。Agent Host を使う schedule は Agent Host process、それ以外は VS Code window が起動している必要があり、マシンもスリープさせないようにします。中断後に catch-up run が起きる場合はありますが、逃した回がすべて再実行される保証はありません。同じ Automation は一度に 1 セッションだけ動きます。

共有時は `.automation.md` を使います。これは実行環境を丸ごと移すファイルではなく、**移植可能な定義だけ**を渡します。

| 含む | 含まない |
|------|----------|
| name、prompt、Manual / Hourly / Daily / Weekly の schedule、file format version、portable identifier | workspace、provider、model、permissions、enabled state、run history |

import した側が workspace、agent、model、permissions、isolation をローカルで選び直し、Enabled はオフの状態から始まります。定義の共有を、実行権限の共有とみなさないでください。

> 保存した permission options は組織ポリシーを迂回しません。将来の run で承認待ちになる可能性があるため、無人化する前に Manual run で確認してください。Automation を無効にしても、すでに実行中のセッションは止まりません。History から Stop を選びます。

**→ Codex Scheduled tasks、Claude Code `/loop`、Kiro Crew との比較は [ループエンジニアリング](../dev-methods/loop-engineering.md#定期実行を選ぶときの比較) を参照**

### VS Code 1.138 の Agent Host と Codex 継続

Agent Host は Agent Host Protocol（AHP）を基盤に、agent harness を **VS Code 本体とは別の専用 process** で動かします。同じ session に複数の VS Code window から接続でき、ローカル folder の対応する Dev Container へ session を移して、プロジェクト側の toolchain / dependencies で動かせます。Dev Container 経路には Docker と対応構成が必要で、1.138 時点は段階的ロールアウトです。

Codex session は ChatGPT app と VS Code の間で同じ会話を継続できます。ただし移動後の tool surface は VS Code 側の built-in / extension / MCP tools へ広がります。**会話が同じでも、使える tool と実行境界が同じとは限らない**ため、handoff 後に権限と接続先を再確認します。

### VS Code 1.139 — Dev Container を remote host へ広げる

VS Code 1.139（2026-09-23、Stable）では、Agent Host の Dev Container session が local folder だけでなく **SSH・Tunnel・WSL 上の project** でも使えるようになりました。1.138 の local 対応を置き換えるものではなく、**実行 host の範囲を広げる追加**です。

| 前提 | 内容 |
|------|------|
| 設定 | `chat.agentHost.devContainer.enabled`。段階的ロールアウト中のため、既定で有効になっていない場合は手動で有効にする |
| 操作 | Agents Window の folder menu から Use Dev Container を選ぶ |
| remote 側 | remote folder に対応する Dev Container configuration があり、**remote host 上で Docker** が使えること |

toolchain / dependencies を remote project 側で揃えたまま agent に build / test させられますが、container の中で動くことは、network・secret・tool 権限の設計が不要になることを意味しません。

同じ release では、組織の account policy で Agent mode を無効にしている場合に、Welcome 画面や `code --agents` などの別経路から Agents Window を開けてしまう問題が修正されました。**起動経路の違いは policy の回避手段ではありません**。

### VS Code 1.140 — Copilot harness・複数フォルダの session・remote host への委任

> **確認日: 2026-10-08**。[VS Code 1.140 release notes](https://code.visualstudio.com/updates/v1_140)（2026-09-30、Stable）に基づきます。個別の機能には Experimental が含まれます。

| 機能 | 状態 | 内容 | 注意点 |
|------|------|------|-------|
| **Copilot harness** | 記載なし | Copilot SDK を使う harness が、Agent Host Protocol（AHP）ベースの専用の agent host process で動く。chat 入力の harness picker で選び、環境によっては既定になっている | Copilot app / CLI と挙動を揃える目的の変更。従来の **Local harness** とは別の選択肢 |
| **Agents window の複数フォルダの session** | **Experimental**（既定は無効） | session ごとに別のリポジトリ・フォルダ・worktree を開ける。`chat.agentHost.copilotAgent.multiRootEnabled`（Claude / Codex は同名の `claudeAgent` / `codexAgent`）をユーザーの `settings.json` で `true` にする | 設定画面には出ない。エディタウィンドウの multi-root とは別機能（[複数ルート運用](multi-root.md#agents-window-の複数フォルダの-session-は別機能vs-code-1140)） |
| **remote host への委任** | **Experimental**（既定は無効） | `chat.remoteAgentHostsEnabled` と `chat.remoteSessions.tools.enabled`（Agents window のみ）で、`list_agent_hosts`・`create_remote_session`・`get_remote_session`・`send_remote_message` の tool が使える | **元の workspace は clone もコピーもされない**。remote 側でも通常の承認が適用される。remote の**最終回答は自動では転送されない**ので明示的に取得する。調整役の Agents window を開いたまま接続しておく必要がある |
| MCP の設定の保存先 | 記載なし | global は `$COPILOT_HOME/mcp-config.json`（未設定なら `~/.copilot/mcp-config.json`）、workspace は `.mcp.json` | `.vscode/mcp.json` は workspace の保存先として **deprecated** |
| OpenTelemetry の identity capture | 記載なし | `github.copilot.chat.otel.captureIdentity` で、`user.name` などを span に加える | **既定はオフ**で、本文の capture とは独立。現時点では **Local harness のみ**に適用（agent host 側は未対応） |

### Copilot CLI 1.0.89〜1.0.91 — instruction の互換・MCP 認証・sandbox

[Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) から、可搬性と安全な運用に関わる変更を抜き出します。

| 版（日付） | 変更 | 確認すること |
|-----------|------|-------------|
| 1.0.89（09-28） | **Claude Code の `.claude/rules` のルールファイルを custom instructions として読む**ようになった | Claude Code 向けに書いたルールが Copilot CLI にも効く。意図しないルールが効いていないか、両方のエージェントで確かめる（[プラグインの可搬性](../dev-methods/plugin-portability.md#instruction-ファイルは別のエージェントにも読まれる)） |
| 1.0.89 | 事前登録した MCP の OAuth client が、設定した `oauthScopes` に従う。managed の MCP policy の適用中に extension が読み込みに失敗する問題を修正。直接インストールした plugin を `copilot plugin enable` / `disable` できる | scope を絞った設定が効いているか |
| 1.0.90（09-30） | **`--mcp-github-auth`** で、GitHub アカウントの認証を**承認した MCP server の origin にだけ**渡せる | GitHub の認証を、承認していない MCP server へ渡していないか |
| 1.0.90 | パスへのアクセス確認に、**session 限定の read-only のディレクトリ承認**を追加。MCP の tool が一時的な discovery の失敗から再起動なしで回復する | 読み取りだけを許すべき場所を read-only で承認しているか |
| 1.0.91（10-01） | **`copilot sandbox ca`** で、proxy の CA の信頼を check / create / trust / rotate / remove できる（`/sandbox ca install` は `create` と `trust` に分かれた） | CA の作成・信頼・破棄の手順を、運用手順に含める |
| 1.0.91 | 静的に完全に解析できる**読み取り専用の shell pipeline** は execution-evidence review に入り、不完全・未束縛の pipeline は**明示的な承認**が必要 | 解析できないコマンドが自動で通っていないか |
| 1.0.91 | Windows で filesystem の列挙に対応しない版でも sandbox 内でコマンドが動くが、PowerShell の現在位置が誤り得る警告が出る | Windows では警告の有無を確認する |

### Copilot の local sandbox（GA）

> **確認日: 2026-10-08**。2026-09-23 に Copilot app で Public Preview になった local sandboxing は、**2026-10-07 に一般提供（GA）**になりました（[公式の変更ログ](https://github.blog/changelog/2026-10-07-local-sandboxing-for-github-copilot-now-generally-available/)）。追加料金はかかりません。

Copilot が起動するツールとコマンドを、**filesystem・network・credential などへのアクセスを制限した状態**で動かす仕組みです。共通の sandbox policy を、**Microsoft eXecution Container（MXC）** が Windows・macOS・Linux それぞれの OS の制御へ変換します。公式は、**モデルの実行とツールの隔離は別**であり、どのモデルを使っていても sandbox の policy はツールの実行に適用されると説明しています。

| 項目 | 内容 |
|------|------|
| 対象 | Copilot CLI、Copilot app、**Agent Host を使う VS Code の session**（変更ログより。公式の概念ページは CLI と app のみを記載） |
| 既定 | **オフ** |
| 有効化（CLI） | `/sandbox enable`。以降のセッションにも保存され、`/sandbox disable` で解除する |
| 有効化（app） | project の設定が、新しい local repository / working tree session の既定になる。実行中の session だけ切り替えることもでき、その場合は project の既定は変わらない |
| CLI と app の関係 | **設定は別々**。片方で有効にしても、もう片方には効かない |

#### 制限できるもの — CLI と app で範囲が違う

| 対象 | Copilot CLI | Copilot app |
|------|------------|-------------|
| Filesystem | 特定パスの read-only / read-write、拒否するパス | 同じ種類の制御の一部 |
| Network | internet と local network、**ホスト単位の allow / deny** | internet と local network の許可・遮断 |
| Credential | Git と `gh` の認証、**追加の環境変数のマスク** | Git と `gh` の認証 |
| その他 | macOS の keychain へのアクセス、コマンド単位で sandbox の外で実行する例外 | 個別のコマンドを sandbox の外で実行するよう承認を求められることがある（project の設定では、この要求を許すかどうかを制御できない） |

credential は、sandbox 内のツールには**プレースホルダー**が渡され、ローカルのプロキシが**承認済みの HTTPS 送信先にだけ**本物の credential を付けます。

#### MCP サーバーと language server

- **ローカルの MCP サーバーと LSP サーバーは、既定で sandbox に含まれます。** sandbox 内で動かすかどうかは選べます。
- **リモートの MCP サーバーは sandbox の対象になりません。** 接続先側で動くためです。
- 組み込みのファイル操作ツールは Copilot のプロセス内で動くため、OS の sandbox からは見えません。公式は、これらは policy を「**ベストエフォート**」で確認すると説明しています。

#### OS が sandbox を強制できないとき

| 面 | 挙動 |
|----|------|
| CLI | 保存した設定はそのセッションだけ無効になり、通知が出る（保存値の `sandbox.enabled` は変わらない）。`/sandbox enable` は拒否される |
| app | セッションは始まり得るが、sandbox 化したプロセスは起動時に失敗する。保存した設定は残る |
| 拒否パスを強制できない場合（app） | 弱い制限で動かさず、そのコマンドを失敗させる |
| enterprise の managed settings | `sandbox.enabled` と `sandbox.failIfUnavailable` がともに `true` なら、CLI は**モデルへのリクエストとツールの実行を止める** |

#### 組織で必須にする

- enterprise の managed settings（server-managed・MDM・ファイル）で `sandbox.enabled` と `sandbox.failIfUnavailable` を設定できます。
- **組織が sandbox を必須にした場合、通常の設定や起動オプションでは無効にできません。** policy が回避を許していれば、現在のセッションだけ無効にでき、保存された policy は変わりません。
- 端末管理の設定は、未対応のホストでも sandbox を必須にできます。この場合、コマンドは sandbox なしで動かず、失敗します。
- project・ユーザー・enterprise の設定の優先順位の全体像は、公式の概念ページに記載がありません。確実なのは「app では project の設定が既定になる」「enterprise の要件が通常の設定より優先される」の 2 点です。

#### OS の要件と限界

| OS | 要件 |
|----|------|
| macOS | Seatbelt を使用。macOS 15（Sequoia）以降（それより古い版は禁止されないが未検証） |
| Linux | bubblewrap 0.5.0 以降（`bwrap` が `PATH` にあること）。外向き通信の制御には `slirp4netns`、util-linux 2.35 以降の `unshare` / `nsenter`、iptables / ip6tables の restore（nf_tables 推奨）、`/dev/net/tun` も必要 |
| Windows | sandbox に対応した最近の Windows 11。一部の機能は Windows の版に依存する |

- **軽量な隔離です。** OS レベルの封じ込めであり、VM やコンテナではありません。
- Linux では、起動したプロセスの local network へのアクセスを個別に制御できません（Copilot のプロセス内の操作には local network の設定が効きます）。
- Windows のプロキシ制御は、プログラムがプロキシ設定に従うことが前提です。macOS / Linux のように直接接続まで遮断するわけではありません。

#### 実行後に確認すること

- CLI では `/sandbox` の状態と、組織の managed settings が要求しているかを確認する。app では project の既定と、実行中の session の設定を分けて確認する。
- 許可したホストや書き込み可能なパスに、意図しないものが入っていないかを見る。
- リモートの MCP サーバーや、sandbox の外で実行する例外を承認したコマンドは、sandbox の対象外として別に管理する。

> **別の sandbox 設定と混同しないでください。** local sandbox は利用者のマシン上で動くツールを制限するものです。GitHub がホストする **cloud sandbox**（Public Preview、組織の「Cloud Sandbox access」ポリシーで有効化、既定は無効、利用量に応じて課金）とは別物です。公式の概念ページは、local sandbox が cloud agent・remote host・Dev Container に適用されるかを記載していません。JetBrains の managed sandbox（Public Preview）も別機能で、今回の GA の対象ではありません。実行場所ごとの比較は [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#実行場所ごとの隔離境界を分ける) を参照してください。

### Agentic CLI の customization 利用指標

2026-09-17、Copilot usage metrics API に CLI の Skill / custom agent / MCP / slash command / Plugin 指標が加わりました。

| 問い | フィールド |
|------|-----------|
| よく使われるもの（上位 5 件、各 `interaction_count`） | `totals_by_skill` / `totals_by_custom_agent` / `totals_by_mcp` / `totals_by_slash_cmd` / `totals_by_plugin` |
| 使われた種類数（上位 5 件以外も含む） | `distinct_skill_use_count` / `distinct_custom_agent_use_count` / `distinct_mcp_use_count` / `distinct_slash_cmd_use_count` / `distinct_plugin_use_count` |

顧客定義名は privacy のため Skill / custom agent / MCP / Plugin では `other`、custom slash command では `custom` にまとめられます。MCP の `interaction_count` は**接続 / 再接続の試行回数**で、tool call 数ではありません（成功・失敗の両方を数える）。Plugin は Plugin に属する Skill invocation の subset で、同じ activity が Skill totals にも入るため、両者を加算しません。

この指標が示すのは adoption、利用の偏り、enablement gap です。生産性、成果物の品質、MCP 接続の成功率を直接示す評価指標ではありません。

2026-09-25 には repository 単位の `repos-1-day` report に `pull_request_review_times` が加わり、ready for review → 初回 review、初回 → 最終 review、最終 review → merge の各段階の median / p90 を取得できるようになりました。人が開き、別の人が review した PR だけが対象で、Copilot code review・bot・author 自身の review は計時しません。**→ 測定対象・欠測・読み方は [Skill / エージェントの評価](../dev-methods/evals.md#pr-のレビュー待ち時間を品質スコアと混同しない) を参照**

### Copilot app の OpenTelemetry 実行トレース

2026-09-22、GitHub は Copilot app のエージェント session を OpenTelemetry で観測できるようになったと発表しました。Enterprise 管理者が `managed-settings.json` の `telemetry` で export と OTLP endpoint を設定します。session 内の model / tool 呼び出しを追う trace、token 等の metric、個別 action の event が対象です。**prompt・response・tool 引数の本文は既定で除外**され、`captureContent` を有効にすると機密情報を含み得るため、監視基盤への送信前に確認が必要です。

上の usage metrics API は 1 日・28 日の**利用集計**、この OTel は個々の session の**実行経路**です。[管理設定リファレンス](https://docs.github.com/en/copilot/reference/enterprise-administrators/enterprise-managed-settings#telemetry)にはまだ対応クライアントとして CLI / VS Code だけが列記されています（2026-09-23 確認）。app 向けの新しい発表と記述が揃うまで、対象バージョン・設定値・collector への到着を確認してください。製品横断の観測データ比較は[ハーネス解説](../dev-methods/harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions)にまとめています。

---

## カスタマイズが効く場所 — レビューとエージェント

カスタマイズは IDE のチャットの中だけのものではありません。同じ `SKILL.md` と MCP 設定を、**プルリクエストのレビュー**にも効かせられます（2026-07-29 一般提供）。

| 項目 | 内容 |
|------|------|
| Skill の置き場所 | リポジトリの `.github/skills/<スキル名>/SKILL.md`（**コミットが必要**） |
| MCP の設定 | リポジトリ設定 → Copilot → MCP servers |
| 資格情報 | リポジトリ設定 → Secrets and variables → **Agents** |
| 制約 | code review からの MCP ツール呼び出しは **read-only に限定**される |
| 対象プラン | Pro / Pro+ / Business / Enterprise |

> **置き場所を間違えやすい点**: ここで使う `.github/skills/` は、`copilot plugin install` や `gh skill install` が Skill を置く先とは**別系統**です。レビューに効かせたい Skill はリポジトリへコミットしてください。

**指示と skills は PR の head branch から読まれます。** Copilot code review は、custom instructions（`.github/copilot-instructions.md`・`AGENTS.md`・`.github/instructions/` に加え、`CLAUDE.md`・`GEMINI.md`・`REVIEW.md`）、agent instructions、agent skills を、マージ先ではなく**変更を含むブランチ**から読みます。PR 内で変えた基準をマージ前に試せる一方、レビュー基準の変更とコードの変更が同じ PR に入ると、どちらが結果に効いたのか分けにくくなります。Claude Code の Code Review は、PR で編集された `CLAUDE.md` の **base 版**を使うため、同じファイルでも読む版が異なります。**→ 参照元の比較、基準を変えるときの手順と検証例、CODEOWNERS での承認は [AI コードレビューはどの指示を読むか](../dev-methods/review-instructions.md) を参照**

レビューの深さ（**effort levels**）も選べます（2026-08-07 一般提供）。`Lite` は単純な変更向け、`Balanced` はより高い推論能力が要る変更向けで、組織管理者が既定値を設定できます（組織設定 → Copilot → Copilot code review）。使用されたレベルはタイムラインと PR の概要コメントに表示されます。

### 2026-09-28 から `Default` は `Balanced` を使う

[2026-10-02の公式変更ログ](https://github.blog/changelog/2026-10-02-copilot-code-review-api-support-and-new-default-effort-level/)は、**2026-09-28から**、review effortが `Default` の組織・リポジトリで `Balanced` が使われると記載しています（"the Default review effort level now uses Balanced for new and existing repositories"）。[2026-08-28の告知](https://github.blog/changelog/2026-08-28-upcoming-changes-to-github-copilot-policies-and-billing/#copilot-code-review-default-is-changing-to-balanced-effort-level)にあった**予定が実施された**ものです。

- `Default` のままの既存・新規の組織とリポジトリは、`Balanced` で review されます。
- 明示的に `Lite` を選んでいた設定は、そのまま尊重されます。`Default` のまま `Lite` 相当を期待していた場合は、**組織またはリポジトリの設定で `Lite` を明示**してください。
- 設定は Enterprise・Organization・Repository・個人の各層で変えられます。組織の既定値は、独自の値を選んでいない配下リポジトリへ適用されます。リポジトリの既定値は自動リクエストされたreviewへ適用され、手動リクエストではPRのReviewers欄からeffort levelを選べます。
- **review の深さが変わると、所要時間と指摘の量も変わり得ます。** 既存のリポジトリで指摘数や待ち時間が変わっていないか、PRのタイムラインと概要コメントに表示されるeffort levelと合わせて確認してください。

### API から review を依頼する（2026-10-02）

同じ変更ログで、**REST / GraphQL API から Copilot に review を依頼**できるようになりました（"You can now request a review from Copilot using the supported REST and GraphQL APIs"）。各リクエストで review effort level を指定することもできます（任意）。対象プランは Copilot Pro・Pro+・Max・Business・Enterprise で、公式の記載は一般提供です。

CI・社内ツール・bot から review を起動する場合は、次の点を分けて設計します。

| 観点 | 確認すること |
|------|-------------|
| 誰の権限で依頼するか | API を呼ぶトークンの持ち主と、その権限（PR への書き込み権限を持つ主体を、必要最小限にする） |
| effort をどう決めるか | 呼び出し側で指定するか、リポジトリの既定に任せるか。指定しない呼び出しは、`Default` の解決先（現在は `Balanced`）に従う |
| approval との関係 | review の依頼と、Copilot approval（[下の節](#プルリクエストの承認をどこまで-ai-に任せるか)）を required approvals に数える設定は**別**。API で review を起動しても、approval が merge 要件を満たすわけではない |
| 起動の頻度 | push のたびに依頼する運用は、review の回数と待ち時間を増やす。対象パスや PR の状態で絞る |

> **確認できていない点**: 具体的なエンドポイント名・リクエストのフィールド名・レート制限は、公式の変更ログ本文からは確認できていません。実装前に[公式ドキュメント](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review)で確認してください。

**→ 経緯と他ツールの対応状況は [Skills 最新動向 9 節](../trends.md#9-skill-が動く場所の広がり) を参照**

---

## プルリクエストの承認をどこまで AI に任せるか

Copilot code review が **approving review を提出できる**ようになりました（2026-09-01、**Public Preview**。Pro / Pro+ / Max / Business / Enterprise）。ここは用語を混同しやすいので、3 つを分けて理解してください。

| 用語 | 意味 | merge 要件を満たすか |
|------|------|-------------------|
| **approval assessment** | PR が承認に値するかという Copilot の判定。すべての Copilot review に表示される | **満たさない。** 公式の変更ログは "An approval assessment alone does not count toward merge requirements." と明記している |
| **Copilot approval** | Copilot が GitHub 上で `APPROVED` のレビューを提出すること | 管理者が明示的に許可した場合のみ提出される（**既定は無効**） |
| **required approvals へのカウント** | その approval をブランチ保護の必須承認数に数えるか | **さらに別の設定**（"Allow Copilot approvals to count toward merge requirements"） |

### 設定階層とパス限定

| 層 | 設定できること |
|----|--------------|
| Enterprise | ポリシーの選択（組織に委ねる / 特定組織で有効 / 全体で無効） |
| Organization | 組織全体の既定。リポジトリへ決定権を委譲することもできる |
| Repository | 個別の有効化と、**パスによる限定** |

リポジトリでは、**変更ファイルがすべて指定した glob に一致する PR だけ**をカウント対象に絞れます（**最大 15 個の glob**）。

### 承認後の挙動と、残る人間の責任

approval 後に新しいコミットが push されると、**人間のレビュアーと同じように approval は dismiss** され、再レビューが必要になります。

> **Public Preview である点と、既定が無効である点を前提に設計してください。** 高リスク領域は CODEOWNERS と必須の human reviewer を維持し、status checks を外さないでください。AI の approval を required approvals に数えるかどうかは、**責任分界を変える設定**です。段階的に導入し、まずはカウントさせない状態で assessment の精度を観察するのが安全です。

なお、PR を merge 可能な状態へ持っていく**修復ループ**（VS Code 1.136 の **Agent Merge**、Preview）は、これとは別の機能です。merge の実行でも approval でもありません（[Skills 最新動向 9-3 節](../trends.md#9-3-pr-を-merge-ready-にするまで--修復ループと-ai-の-approval)）。

---

## 組織の統制 — 実行操作を `deny` / `ask` / `allow` に分ける

GitHub Copilot の **enterprise managed permissions** が 2026-09-09 に一般提供されました。Enterprise owner は、エージェントが行う操作を `permissions.deny`、`permissions.ask`、`permissions.allow` に分類できます。

対象は shell command、file read / edit、network domain です。複数の規則が一致する場合は **`deny` → `ask` → `allow`** の順で優先され、組織の `ask` には毎回新しい承認が必要です。一般提供の対象として発表された面は、**Copilot app、Copilot CLI、VS Code Agent Host のセッション**です。

### JetBrains は managed sandbox の Public Preview

GitHub Copilot for JetBrains では、2026-09-08 に **enterprise managed sandbox** が Public Preview になりました。これは JetBrains の実行環境を中央設定する機能で、上記の操作単位の managed permissions が JetBrains でも一般提供された、という発表ではありません。

**→ セレクター、承認を省略できない条件、JetBrains sandbox、Claude Managed Agents との比較は [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#実行する操作を-deny--ask--allow-に分ける) を参照**

### managed settings を validator で確認する

2026-09-25、enterprise managed settings の **in-product validator** が加わりました。JSON の書式誤り、未対応の構成、無効な team mapping など、**policy が意図どおり適用されない原因**を、enterprise の AI controls ページにある「Copilot settings validation」に表示します。各 issue には対象 file と JSON path が示されます。

| 検証対象 | 内容 |
|---------|------|
| `copilot/managed-settings.json` | enterprise 全体の managed settings |
| `copilot/team-mappings.json` | team mapping と、そこから参照される team settings file |

修正は `.github-private` repository の **default branch へ commit** し、Agents ページを再読み込みしてから validator の結果を再確認します。「file を置いた」ことではなく「validator がエラーを出さない」ことを適用確認の最低ラインにしてください。

### Copilot CLI の別経路にも managed settings が効く — 1.0.87 / 1.0.88

Copilot CLI は、ターミナルで対話する使い方のほかに、エディタや別のアプリから**プロトコル経由で起動される**ことがあります。1.0.88（2026-09-22）の changelog は、次の経路で起動したセッションにも enterprise managed settings が適用されるようになったと記載しています。**それより前の版では、これらのセッションは managed の MCP・permission・plugin の policy なしで動いていました**。

| 起動のしかた | 使われ方 |
|------------|---------|
| `copilot --acp` | Agent Client Protocol（ACP）サーバーとして起動し、ACP に対応したエディタや自動化ツールから操作される（ACP 対応は Public Preview） |
| `copilot --ahp-host` | Agent Host Protocol（AHP）の host として起動する |
| `--server` で公開したセッション | サーバーとして公開した Copilot CLI のセッション |

管理者は次を確認してください。

- 組織の端末の Copilot CLI を **1.0.88 以降**にそろえる。そろえられない間は、上の 3 経路を「統制が効かない経路」として扱い、利用を止めるかどうかを決める
- エディタ連携などで Copilot CLI が**裏側で起動されている使い方**を棚卸しする。利用者がターミナルを開いていなくても、CLI は動いている場合がある
- validator がエラーを出さないことに加えて、それぞれの経路で MCP の一覧と承認の挙動を実際に確かめる

1.0.87（2026-09-21）には、統制に関わる次の変更もあります。

- 空の `strictKnownMarketplaces` allowlist を置くと、CLI に組み込まれた plugin marketplace も表示されなくなり、ブロックされる。組み込みのものも含めて Plugin の導入元を閉じられる
- Auto routing tier の起動時の既定を、利用者の設定と managed settings で指定できる。managed 側では、厳格に固定するか、利用者の上書きを許すかを選べる

同じ「統制が効いていない経路がないか」という観点は、Claude Code の [auto mode の開始モードの拡大](../claude-code/basics.md#auto-mode-が既定の開始モードになる範囲--21283)にも当てはまります。どちらも、**配った設定ファイルではなく、実際に動いているセッションで確かめる**ことが確認の基本です。

### JetBrains 1.18.0 — エージェントの承認・共有設定・MCP

2026-09-22 の [GitHub 公式発表](https://github.blog/changelog/2026-09-22-new-features-and-improvements-in-copilot-for-jetbrains/)で、GitHub Copilot for JetBrains 1.18.0 に次の変更が加わりました。

| 変更 | 利用時の注意 |
|------|--------------|
| **assisted approvals**（Public Preview） | Copilot agent セッションの低リスクなツール呼び出しを自動承認し、高リスクな操作は利用者へ確認する。上記の enterprise managed permissions や managed sandbox と同一機能ではない |
| 共有 Skill・instructions | organization / enterprise の Skill と organization-managed custom instructions を、local session と Copilot agent session の両方で利用できる |
| MCP ツール制御 | 組み込み GitHub MCP Server は既定で有効。手動構成した MCP Server は変えずに組み込み分だけ切り替えられ、Copilot agent session ではツールごとの設定を永続化できる |
| Codex agent の plan mode | 実装前に計画を確認・修正・承認できる |
| 以前のメッセージの再編集 | Copilot agent session で過去のユーザーメッセージを再編集できる。置き換えを送信する前に、会話とファイル変更がその地点まで巻き戻されるため、残したい変更は事前に確認する |

JetBrains Gateway / リモート開発環境では、inline chat とその入口が非表示になりました。通常の JetBrains IDE の説明をリモート環境にそのまま当てはめないでください。

---

## 新機能の既定ポリシー — 2026-10-22 から適用

2026-09-24、Copilot Business / Enterprise の enterprise / organization 設定に、**一般提供（GA）された eligible な機能と client capability の global default policy** が追加されました。設定は今すぐできますが、利用者の機能アクセスに影響し始めるのは **2026-10-22** からです。

> **確認日: 2026-09-27 / 状態: 設定受付中（2026-10-22 適用開始）**。適用後は公式文書と管理画面で実際の挙動を再確認してください。

| 項目 | 内容 |
|------|------|
| 設定場所 | AI Controls → Copilot → **Default policy for new features** |
| 対象 | Features & clients ページで管理される eligible な機能、Agents ページの **Copilot Code Review** policy、**MCP servers in Copilot** policy。eligibility と例外は公式の default availability 文書で確認する |
| 選択肢 | **Enabled**（現在と将来の eligible 機能を既定で利用可能）／ **Disabled**（現在の eligible 機能は使えないまま、将来の機能は管理者の承認が必要）／ **Let organizations decide** |

2026-10-22 以降の扱いは次のとおりです。

- **Unconfigured のまま**の eligible な GA 機能は、選んだ global default に従います
- **明示的に enable / disable した設定は保持**されます
- **Preview は引き続き opt-in** です。Preview で選んだ設定は、その機能が後に GA になっても保持されます

「全機能が自動で有効になる」わけではありません。一方、何も選ばなければ未設定の policy が新しい既定に従うため、管理者は期限前に次を確認します。

1. Features & clients、Copilot Code Review、MCP servers in Copilot のうち、**Unconfigured のまま**の項目を洗い出す
2. MCP server の利用可否は、[MCP allowlists](../dev-methods/skill-security.md#4-組織で許可範囲を絞る) と合わせて意図した状態にする
3. 組織ごとに判断させる場合は、organization 管理者へ期限と判断基準を伝える

---

## Upcoming — github.com・Mobile・cloud agentのポリシー統合

[GitHubの2026-08-28の公式告知](https://github.blog/changelog/2026-08-28-upcoming-changes-to-github-copilot-policies-and-billing/#copilot-cloud-agent-copilot-chat-on-githubcom-and-copilot-chat-in-github-mobile-are-converging-to-a-single-experience-and-policy)では、**2026-09-28より前には開始しない**（no earlier than September 28th, 2026）条件で、Copilot Chat on github.com、GitHub MobileのCopilot Chat、Copilot cloud agentを単一の体験とポリシーへ統合する予定です。

> **確認日: 2026-09-16 / 状態: Upcoming（予定）**。以下は現在の挙動ではありません。ロールアウト後に公式変更ログ、管理画面、データ保持の公式文書を再確認し、この節を更新してください。

| 変更予定 | 管理・利用への影響 |
|---------|------------------|
| 3つの体験の個別ポリシーを単一ポリシーへ統合 | 統合後は既定で有効になる予定。現在の個別設定がそのまま同じ意味で残るとは限らない |
| Copilot on github.comをagent sessionsの体験へ移行 | github.comのチャットデータ保持期間を**28日からアカウントの存続期間へ変更**する予定 |
| cloud agentでSandboxを利用 | GitHubは、より高速なcloud体験を目的としていると説明している |
| 統合後にopt outする | github.comとGitHub MobileのCopilotへアクセスできなくなる予定 |

### Business / Enterprise管理者が事前に確認すること

1. **2026-09-28より前に**、github.comのCopilot設定を開きます。
2. 公式告知で追加予定とされる `Copilot cloud agent` ポリシーを確認します。
3. github.com / Mobile / cloud agentをチームに許可するか、統合後の既定有効化を受け入れるかを決めます。
4. チャットデータをアカウント存続期間まで保持する変更が、社内のデータ保持・監査方針と合うかを確認します。

利用を継続するだけなら、GitHubは追加操作を不要としています。ただし管理者は、既定有効化とデータ保持期間の変更を理解したうえで期限前にポリシーを確認する必要があります。

---

## 組織の統制 — content exclusion

機密ファイルを Copilot のコンテキストから除外する **content exclusion** が、**Copilot app と Copilot CLI で一般提供（GA）** になりました（2026-09-02）。対象は **Copilot Business / Copilot Enterprise** です。

除外したファイルは、インラインの提案に使われず、他ファイルへの提案にも影響せず、Copilot の応答にも Copilot code review にも使われません。

### 対応している面・していない面

**「app・CLI・主要 IDE で GA」であって「全ての面で GA」ではありません。** GitHub Web / Mobile は Public Preview に留まり、VS Code の Edit mode / Agent mode は非対応です。ここを取り違えると、保護されていない経路が残ります。

> 上記のポリシー統合予定は、content exclusionの対応範囲が同じ日付に自動で変わることを意味しません。ロールアウト後も、content exclusionの公式文書で対応面を別に確認してください。

| 面 | 対応 |
|----|------|
| Copilot app / Copilot CLI | **GA**（2026-09-02） |
| Visual Studio / VS Code / JetBrains（インライン提案・チャット・エージェント） | **GA** |
| Vim・Neovim / Xcode / Eclipse | **GA**（インライン提案のみ） |
| GitHub Web / GitHub Mobile | **Public Preview**（チャット・エージェントのみ） |
| **VS Code の Copilot Chat の Edit mode / Agent mode** | **非対応** |
| Azure Data Studio、Xcode / Eclipse のチャット・エージェント | 非対応 |

設定は、リポジトリ管理者・組織オーナー・Enterprise オーナーが行います。

### 併せて確認すること

- **semantic information** — IDE が型情報やシンボル定義として間接的に提供する内容は、除外ファイル由来でも使われる可能性があります
- **symlink と、リモートファイルシステム上のリポジトリ** — 現時点では適用されません
- **MCP / Skill は別経路** — content exclusion は Copilot のコンテキスト取り込みに対する制御です。MCP サーバーや Skill が別の経路でファイルを読む場合の防御は別途必要です（[Skill / Plugin のセキュリティ](../dev-methods/skill-security.md)）

> **content exclusion だけを秘密情報の防御線にしないでください。** OS の権限、サンドボックス、secret scanning、MCP / Skill の allowlist と組み合わせた多層防御が前提です（[生成AIを業務で安全に使う](../business/safety.md)）。

---

## クイックスタート

### 最小構成で始める

まずは Instructions から始めるのが最もシンプルです。

```
.github/
  instructions/
    go.instructions.md
```

```markdown
---
applyTo: "**/*.go"
---

# Go コーディング規約

- Effective Go に準拠すること
- エラーは即座にチェックし `fmt.Errorf` でラップすること
```

### チーム向けの推奨構成

```
.github/
  instructions/
    go.instructions.md             # コーディング規約
    terraform.instructions.md      # IaC 規約
  prompts/
    create-readme.prompt.md        # README 生成
    generate-tests.prompt.md       # テスト生成
  agents/
    code-reviewer.agent.md         # コードレビュー
    security-reviewer.agent.md     # セキュリティレビュー
```

---

## よくある質問

### Q: Instructions と Agents の違いは？

**Instructions** はファイルパターンに応じて**自動的に**適用されるルールです。一方、**Agents** はチャットで**明示的に選択**して使う専門家ペルソナです。

### Q: 既存のプロジェクトにも適用できる？

はい。`.github/` ディレクトリにファイルを追加するだけで、既存プロジェクトにも適用できます。コードベースへの変更は不要です。

### Q: カスタマイズはどのプランで使える？

Instructions、Prompts、Agents は GitHub Copilot のすべてのプラン（Free、Pro、Pro+、Business、Enterprise）で利用可能です。

---

## 2026-09-22 の新モデル — Copilot 経由の利用条件

GitHub Copilot でも **Claude Opus 5.5** と **GPT-6 Sol / Luna** が段階的に展開されています。これは Anthropic / OpenAI の直接提供とは別のモデルピッカー・プラン・課金条件です。

| モデル | Copilot の対象プラン | 選ぶ目安 |
|--------|----------------------|----------|
| Claude Opus 5.5 | Pro+ / Max / Business / Enterprise | 長時間の agentic coding や知識作業 |
| GPT-6 Sol | Pro+ / Max / Business / Enterprise | 複数手順の検証を伴う開発作業 |
| GPT-6 Luna | Pro / Pro+ / Max / Business / Enterprise | 小さめ・高速な作業 |

VS Code、Copilot CLI、Copilot app、cloud / coding agent、JetBrains などのモデルピッカーで提供されますが、展開は段階的です。Business / Enterprise 管理者は Copilot settings の model policy を確認してください。Copilot 側は usage-based billing が適用されるため、固定単価は記載せず[公式料金案内](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)を参照します。年払いの一部個人プランに残る旧 premium request 課金とは区別してください。**→ OpenAI 側の Codex / Work での提供条件は [Codex ガイド](../codex/README.md#gpt-6-sol--luna-と-codex-cli-0156-系)を参照。**

Copilot の model policy は Copilot 経由の利用にだけ効きます。同じ組織で Claude Code を直接使っている場合、新しいモデルを検証が済むまで使わせない設定は Claude Code 側の managed settings で別に行います（2.1.283 の `availableModelsMatch` / `deniedModels`）。**→ [Claude Code のカスタマイズ機能](../claude-code/basics.md#新しいモデルを検証前に使わせない--availablemodelsmatch-と-deniedmodels)を参照。**

## ローカルモデルを使う — Ollama の発見と offline mode（CLI 1.0.94-0〜）

> **確認日: 2026-10-08**。対象は Copilot CLI 1.0.94-0 以降の `/model` です（[公式の変更ログ](https://github.blog/changelog/2026-10-07-discover-local-models-in-github-copilot-cli/)、2026-10-07）。

Copilot CLI 1.0.94-0 から、`/model` が**起動中のローカル Ollama から対応モデルを見つけて**、設定済みのモデルや Copilot のクラウドモデルと並べて表示するようになりました。

### 最小の手順

| 手順 | 内容 |
|------|------|
| 1. 事前準備 | **Ollama とモデルを先に入れて、Ollama を起動しておく。** この操作は runtime のインストールやモデルのダウンロードを行わない |
| 2. 探す | CLI で `/model` を開く。起動中の Ollama にある対応モデルが一覧に出る |
| 3. 確かめる | 選んだモデルの **provider と endpoint** を確認する（ローカルの Ollama を指しているか） |
| 4. 追加する | 「**Add and use for this session**」（追加して今のセッションで使う）か「**Add without switching**」（追加だけして切り替えない）を選ぶ。CLI の再起動は不要 |

- **見つかったモデルは自動では追加されません。** 選んで追加したものだけが使われます。
- モデルは **tool calling と streaming に対応**している必要があります。対応しないモデルでは CLI がエラーを返します。BYOK の公式ドキュメントは、**128k トークン以上のコンテキスト**を推奨しています。
- provider への接続に失敗した場合は、モデルピッカーに理由が表示されます。

### 「ローカルモデル」「offline」「telemetry」は別々の設定

ここが最も誤解しやすい点です。公式の変更ログは次の 2 点を明記しています。

- **ローカルモデルを選んでも、offline mode にはならない。** CLI の offline mode は `COPILOT_OFFLINE=true` で**明示的に**有効にする。
- **ローカルモデルを選んでも、GitHub の telemetry は止まらない。**

| 設定 | 決めるもの | 設定方法 |
|------|-----------|---------|
| どのモデルを使うか | 推論に使うモデル | `/model`、`COPILOT_MODEL` / `--model` |
| どこへ送るか（provider） | プロンプトとコード文脈の送信先 | `/model` で追加したモデルの endpoint、または `COPILOT_PROVIDER_BASE_URL` など |
| offline mode | Copilot CLI が **GitHub のサーバーへ接続しない**ようにする | `COPILOT_OFFLINE=true` |
| telemetry | GitHub への利用データの送信 | ローカルモデルの選択では変わらない（止め方は公式ドキュメントで確認） |

組み合わせごとの送信先を整理すると、次のとおりです。

| 構成 | プロンプト・コード文脈の送信先 | GitHub への通信 |
|------|-----------------------------|----------------|
| Copilot のクラウドモデル | GitHub / モデル提供元 | あり |
| ローカル Ollama（offline mode なし） | 手元の Ollama | **あり**（telemetry を含む） |
| ローカル Ollama ＋ `COPILOT_OFFLINE=true` | 手元の Ollama | 止める設定 |
| リモートの provider ＋ `COPILOT_OFFLINE=true` | **そのリモート provider へネットワーク経由で送られる** | 止める設定 |

公式ドキュメントは、**完全なネットワーク隔離には provider もローカル（または同じ隔離環境）にある必要がある**と明記しています。offline mode でも、base URL がリモートなら「プロンプトとコード文脈はその provider へ送られる」ためです。

### 使い終わった後・使う前に確認すること

- `/model` で、**今のセッションがどのモデルを使っているか**と、その endpoint を確認する。「Add without switching」を選んだ場合、セッションは切り替わっていません。
- コードを社外へ出せない作業では、**モデルの選択だけで判断しない**。endpoint がローカルか、`COPILOT_OFFLINE=true` が設定されているかを別々に確かめる。
- MCP サーバーや Web 取得など、モデル以外の外部接続も別に存在します。offline mode がそれらをどこまで止めるかは、公式ドキュメントに記載が見当たりませんでした。

### まだ確認できていないこと

- この機能の**対象プランや組織ポリシー**は、変更ログに記載がありません。組織で BYOK・ローカルモデルを制御する設定は、別の公式文書（enterprise 向けのカスタムモデル設定）を確認してください。
- BYOK 利用時に GitHub 認証が必要かどうかも、BYOK のページには記載がありませんでした。
- 変更ログが触れている**ローカルモデルとの intelligent routing は「今後提供」**の発表段階です。現時点で使える機能として扱いません。
- Copilot app にも独自の BYOK 設定があります（[公式ドキュメント](https://docs.github.com/copilot/how-tos/github-copilot-app/use-byok-models)）。CLI の `/model` の発見機能とは別の手順です。

## 複数のモデル・エージェントを組み合わせる — HydraFusion と Dynamic workflows

2026-09-30〜10-01 に、Copilot で「複数を組み合わせる」機能が 2 つ広がりました。名前は似た印象ですが、**組み合わせるもの・誰が手順を決めるか**が違います。

| | HydraFusion | Dynamic workflows |
|--|-------------|-------------------|
| 組み合わせるもの | **複数のモデル**（1 ターンの中で） | 自動化した手順と**複数のエージェント** |
| 手順を決めるのは | HydraFusion（プロンプトごとに実行パターンを選ぶ） | **ワークフローの作者**（コードで定義） |
| 使い方 | モデルピッカーで選ぶ | 名前を指定して実行（`copilot workflow run` も可） |
| 状態 | **Research preview**（本番利用向けではなく、SLA なし） | **Public preview** |
| 対象 | VS Code（1.140 以降 / Insiders）、Copilot app、Copilot CLI | Copilot CLI（`--experimental`）、Copilot app、Copilot SDK |

### HydraFusion — モデルピッカーに出る「調整役」

[HydraFusion](https://github.blog/changelog/2026-09-30-hydrafusion-in-vs-code-and-the-github-copilot-app/) は、モデルピッカーに表示されますが、**単一のモデルではなく、複数のモデルを調整する仕組み**です。2026-09-30 に、Copilot CLI に加えて VS Code と Copilot app でも使えるようになりました。プロンプトごとに、次の 3 つの実行パターンから 1 つを選びます。

| パターン | 動き |
|---------|------|
| **Single** | 1 つのモデルがそのまま解く |
| **Cascade** | 効率のよいモデルが下書きし、品質ゲートが採用するか、より強いモデルへ引き上げるかを決める |
| **Critique** | 1 つのモデルが下書きし、**別系統のモデルが読み取り専用で批評**し、最初のモデルが 1 回だけ直す（CLI の Rubber Duck と同じレビューの型） |

| 項目 | 内容 |
|------|------|
| 有効化 | VS Code: モデルピッカーで HydraFusion を選ぶ。出てこなければ `chat.copilot.hydraFusion.enabled` を有効化／app: Settings で「HydraFusion」を検索してオンにし、モデルピッカーで選ぶ |
| 対象プラン | Copilot Pro・Pro+・Business・Enterprise |
| 組織の制御 | プレビュー機能のポリシーに従う。Business / Enterprise は管理者がプレビュー機能を許可する必要がある。**組織の model policy で許可されたモデルだけ**を使い、使えるモデルがなければピッカーに出ない |
| 課金 | 使った各モデルが通常単価で課金される（HydraFusion 自体の追加料金はない）。**Auto の割引は適用されず、単一モデルより多くの AI credits を使うことがある** |
| どのパターンが動いたか | CLI: 進捗表示と会話の要約／VS Code: 完了した応答のフッターにホバー／app: 応答にホバー／詳細: `/collect-debug-logs` |

**Auto との違い**: Auto はリクエストごとに**1 つのモデルを選びます**。HydraFusion は**実行パターンを選び、1 ターンの中で複数のモデルを協調させます**。

運用上の注意（公式ドキュメントより）:

- **途中の下書きは表示されず、破棄されることがあります。破棄された下書きが行ったファイル編集は自動では元に戻りません。** コミット前に差分を確認してください。
- サブエージェントとは別の仕組みで、サブエージェントを起動しません。
- 使うモデルの一覧は固定されておらず、利用者は選べません。プレビュー中にパターンやモデルが変わることがあります。
- 補助するモデル（批評役など）には「必要な文脈だけ」が渡されると説明されていますが、保持期間や学習への利用は公式ページに記載がありません。**扱う情報の範囲は、Copilot 全体のデータ取り扱いの文書で確認**してください。

### Dynamic workflows — 手順をコードで決めて、判断だけエージェントに任せる

[Dynamic workflows](https://github.blog/changelog/2026-10-01-dynamic-workflows-in-copilot-cli-and-the-copilot-app/) は、**タスクの進め方をコードで定義したプログラム**です。自動化した手順とエージェントの作業を組み合わせ、順番に・並列に・その両方で実行できます。手順・いつエージェントを使うか・結果をどう使うかはコードが決め、エージェントは分析や判断が要る部分を担います。

できること（公式の説明）:

- コマンドの実行、ツールの利用、他サービスの呼び出し
- 目標をタスクに分け、独立したものを並列に実行する
- 段階から段階へ、構造化した結果を渡す
- サブエージェント同士に検証させる
- 利用者に入力を求める（クライアントが対応する場合）
- 途中で一時停止して確認し、再開する

**autopilot・`/fleet` との違い**（公式ドキュメントの比較表より）:

| | autopilot | `/fleet` | Dynamic workflow |
|--|-----------|----------|------------------|
| 目的 | 入力を待たずに自律的に進める | 並列のサブエージェントへ仕事を任せる | コードで定義した手順を実行する |
| 手順を決めるのは | Copilot | Copilot（毎回） | ワークフローの作者 |
| 再現性 | Copilot の判断で変わる | Copilot の判断で変わる | 毎回同じ手順とルール。ただし経路とエージェントの出力は変わり得る |

#### 作る・置く・実行する

| やること | 方法 |
|---------|------|
| CLI で使えるようにする | `copilot --experimental`、または対話中に `/experimental on`（app は設定不要） |
| 作る | 目的・手順の順番・エージェントに任せる部分・上限を説明して Copilot に作らせる。自分で書く場合は `Show me the guidance for writing dynamic workflows.` と頼むと組み込みのガイドが出る |
| 実体 | **Copilot extension**（例: `extensions/java-security-checks/extension.mjs`） |
| 置き場所 | 既定はセッション内。個人は `~/.copilot/extensions/`、リポジトリは `.github/extensions/`、配布は plugin |
| 実行（対話） | 名前と入力を書いて頼み、承認で **Yes** を選ぶ |
| 実行（コマンド） | `copilot workflow run <名前> --args @input.json --allow-tool=read`（`--result-file` で結果を JSON 保存） |
| 一時停止・再開・中止 | CLI: `/workflows` で P（一時停止）・R（再開）・X（中止）／app: **Workflows** パネル。**中止した実行は再開できない** |

#### 上限を必ず決める

公式は、上限の設定を任意としつつ、AI credits の管理のために**推奨**しています。

- 設定できる上限: 同時に動くエージェント数（超えた分は待ち行列に入る）、1 回の実行で起動するエージェントの総数、実行時間（一時停止中は数えない）、**おおよその AI credits**
- 指定する場所と優先順位: **プロンプト → ワークフローのコード → 個人の `/settings`（`workflows.defaultLimits.*`）**
- **credits の上限は「おおよそ」です。** 使用量は事後に報告されるため、厳密な上限にはなりません。大きな実行の前に小さく試して使用量を測るよう、公式も勧めています。
- 上限で止まった実行を再開するときの新しい上限は、**実行全体の合計**です（新たな枠が追加されるわけではありません）。

#### 権限と信頼の境界

- サブエージェントは **CLI の権限の仕組みを使い、セッションで既に与えた許可を引き継ぎます。** セッションで一度許可した操作は、それを必要とするすべてのサブエージェントに効きます。
- 対話中は、未承認の操作で通常どおり確認が出ます。**`copilot workflow run` は確認を表示しません。** 事前に `--allow-tool` / `--allow-url` で許可し、それ以外の要求は拒否されます。
- **extension は自分のコードを直接実行でき、これは上記の権限の確認の外側で動きます**（"An extension can also run its own code directly, outside these permission prompts."）。共有された workflow を使う前に、`extension.mjs` の中身を確認してください。考え方は Claude Code の [Mods](../claude-code/mods.md#3-入れる前に--信頼の境界を理解する) と同じで、**実行コードを持つ拡張**として扱います。
- CI では `COPILOT_GITHUB_TOKEN` などで認証します。未信頼のディレクトリでプロジェクトの extension を読ませる `GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS=true` は、公式も「**信頼できるコードにだけ**」使うよう警告しています。
- 公式ドキュメントには、組織の管理者が Dynamic workflows を制御する設定や、workflow のコードの隔離（sandbox）についての記載が見当たりませんでした。

> **対象プランの表記に差があります**: 変更ログは「すべての Copilot プラン」としていますが、概念ページは「旧来のリクエスト課金に残る Copilot Pro / Pro+ の年払いプランを除く」としています。導入前に、自分のプランで使えるかを確認してください。

**→ 複数エージェントにすべきかどうかの判断基準は [マルチエージェントを使う境界線](../dev-methods/multi-agent.md#copilot-の-hydrafusion-と-dynamic-workflows2026-09-3010-01) を参照**

## Computer Use — デスクトップアプリを操作する（Public Preview）

2026-10-01 から、**Copilot CLI と GitHub Copilot app** で、Copilot が macOS / Windows のデスクトップアプリを操作できるようになりました（[公式の変更ログ](https://github.blog/changelog/2026-10-01-github-copilot-can-now-interact-with-desktop-apps/)、**Public Preview**）。アクセシビリティ情報と、必要に応じたスクリーンショットで画面を読み、クリック・テキスト入力・キー操作・スクロール・ドラッグ・アプリ間の移動を行います。

| 項目 | 内容 |
|------|------|
| 状態 | Public Preview（2026-10-01） |
| 対象 | Copilot CLI と GitHub Copilot app。**macOS / Windows のローカルセッションのみ** |
| 既定 | **無効**。使う前に明示的に有効化する |
| 有効化 | CLI: `/computer on`（状態確認は `/computer show`、無効化は `/computer off`）／ app: Settings → Computer Use → Enable Computer Use |
| 画面の読み方 | OS のアクセシビリティツリー。視覚的な文脈が要る場面ではスクリーンショット |
| macOS の権限 | Accessibility（コントロールの操作）と Screen Recording（ウィンドウの確認） |
| 組織の制御 | Enterprise 管理者は managed settings で無効化できる。ローカルで `/computer on` にしても、組織のポリシーは上書きできない |

### 承認の流れ — 「Always allow」の範囲に注意する

Computer Use は、CLI の**現在の permission mode** に従って承認を求めるかどうかが決まります（`/permissions show` で確認）。承認を求められたときの選択肢は次のとおりです。

| 選択 | 効く範囲 |
|------|---------|
| **Allow** | 現在の Computer Use セッションのみ |
| **Always allow** | 以降のセッションにも保存される。**同じコンピューターの Copilot app にも適用される** |
| 拒否・キャンセル | そのリクエストを実行しない |

- **`deny` ルールは、自動承認や保存済みの承認より優先されます。** 操作させたくないアプリは、承認の記憶に頼らず `deny` で止めます。
- 公式は、**機密情報を含むアプリや、影響の大きい操作ができるアプリに「Always allow」を選ばない**よう勧めています。メール・会計・社内管理画面などは、毎回確認する運用が安全です。
- 「Always allow」の一覧は見直し・リセットできると公式は説明しています（具体的な操作手順は[公式ドキュメント](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/computer-use)で確認してください）。
- 実行中の操作は **Esc を 2 回**押すと中断できます。
- 承認は「そのアプリを操作してよい」という範囲の許可です。アプリ内で何を送信・削除するかまで個別に確認されるとは限りません。承認の重さの考え方は[エージェントに外部操作を与える手段の選び方](../dev-methods/tool-selection.md#8-承認境界--読み取り入力送信購入削除で分ける)を参照してください。

### いつ使うか — API・MCP・CLI が先

公式ドキュメントは、**API・MCP サーバー・ターミナルコマンド・ファイル操作ツール・専用のブラウザツールで直接できる作業なら、そちらの方が構造化された情報と予測しやすい結果を返す**としています。Computer Use が向くのは、API や CLI、MCP 連携のないレガシーソフトや、GUI でしか操作できないアプリです。

| 向く作業 | 向かない作業 |
|---------|-------------|
| API のない社内ツールの画面から状態を読み取る | GitHub の Issue や PR の操作（`gh` や GitHub MCP で足りる） |
| GUI 専用アプリでの E2E 確認・画面の最終確認 | 大量データの反復処理（API・CLI の方が速く確実） |
| 複数アプリにまたがる手作業の手順を、読み取り中心で自動化する | 取り消せない送信・購入・削除を無人で行う |

指示は、**目的・対象アプリ・してはいけないこと**を含めて書きます。公式の例は次のとおりです。

```text
Open APP_NAME and summarize the status information shown in the main window. Do not change any values or submit any forms.
```

### 公式が挙げる限界とリスク

- 間違ったコントロールを選ぶ、違う場所に入力する、非標準・動的なコントロールや複雑な手順で失敗することがある。
- 指示が曖昧だったり、**画面上に予期しない内容があったりすると、意図しない操作**がデバイス・データ・接続アカウントに及ぶことがある。画面に表示された文字列は「データ」であって「指示」ではありません（[プロンプトインジェクションの扱い](../dev-methods/tool-selection.md#8-承認境界--読み取り入力送信購入削除で分ける)）。
- アプリのウィンドウには機密情報が表示され得る。公式ドキュメントは、どのデータがモデルへ送られるかを詳しく述べていないため、**コンテキストとして共有される内容を利用者が確認する**前提で使います。
- 公式は「Computer Use は人の判断の代わりにはならない」と明記しています。

> **他社の Computer Use との違い**: Codex / ChatGPT Work の Computer Use、OpenAI Agents API の Computer Use（OpenAI-hosted ブラウザ）とは、実行場所・承認の単位・管理方法が異なります。比較は [Skills 最新動向 6 節](../trends.md#6-computer-use--browser-use)を参照してください。

## モデルの廃止 — 2026-10-02 実施分と 2026-10-19 予定分

Copilot では、モデルピッカーのモデルが短い間隔で入れ替わります。**自分のワークフロー・組織のポリシー・社内手順書が、廃止されるモデル名を固定していないか**を確認してください。

### 2026-10-02 に廃止された（実施済み）

[公式の変更ログ](https://github.blog/changelog/2026-10-02-selected-models-in-github-copilot-deprecated/)によると、2026-10-02 付けで次のモデルが廃止されました。

| 廃止されたモデル | 移行先 |
|-----------------|--------|
| Gemini 3.5 Flash / Gemini 3.6 Flash | Gemini 3.8 Flash |
| Kimi K2.7 Code | Kimi K3 |
| Claude Opus 4.7 | Claude Opus 5.5 |

廃止モデルを削除する作業は不要ですが、**ワークフローや連携は対応モデルへ更新**する必要があります。Copilot Enterprise の管理者は、代替モデルを使えるようにするため、Copilot 設定の model policy で有効化が必要な場合があります。

### 2026-10-19 に廃止される（予定）

[2026-09-18 の告知](https://github.blog/changelog/2026-09-18-upcoming-deprecation-of-selected-github-copilot-models-in-mid-october/)によると、**2026-10-19** に次のモデルが廃止されます。対象は Copilot Chat・インライン編集・ask / agent モード・コード補完を含むCopilotの各体験です。

| 廃止されるモデル | 推奨される代替 |
|-----------------|---------------|
| Gemini 3.7 Flash | Gemini 3.8 Flash |
| GPT-5.5 | GPT-5.6 Sol |
| GPT-5.4 | GPT-5.6 Sol |
| GPT-5.4 mini | GPT-5.6 Luna |
| GPT-5 mini | GPT-5.6 Luna |
| Grok 4.5 | Grok 4.6 |

### 管理者が確認すること

公式は、Copilot Enterprise と Business では、**global default の model enablement が有効で、管理者が当該モデルを明示的に無効にしていない限り**、推奨される代替モデルが自動で有効になると説明しています。つまり、次の 2 つの層で挙動が分かれます。

| 組織の状態 | 廃止後の代替モデル |
|-----------|-------------------|
| global default を有効のまま、廃止モデルも明示的に無効にしていない | 自動で有効になる |
| global default を無効にしている、または廃止モデルを明示的に無効にしている | **自動では有効にならない**。model policy で代替モデルへのアクセスを有効にする |

- **モデルを個別に絞っている組織**は、廃止日の前に model policy を見直し、代替モデルを検証して有効にするか決めます。
- 代替モデルは**世代と挙動が違います**（たとえば、廃止対象のGPT-5.5・GPT-5.4と、代替のGPT-5.6 Sol）。プロンプトや Skill・Instructions の評価を、モデルを固定して行っている場合は、代替モデルで再評価します（[Skill / エージェントの評価](../dev-methods/evals.md)）。
- 同じモデル名を **Claude Code や Codex の側**で固定している場合、Copilot の廃止は影響しません。Copilot 経由の利用にだけ効く変更です（Claude Code 側は 2.1.283 の `availableModelsMatch` / `deniedModels` を参照）。
- 日付と対象は変更され得ます。**廃止日の前に、公式変更ログと組織のモデルピッカーを再確認**してください。

## 参考リンク

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — カスタマイズの公式リポジトリ
- [Claude Opus 5.5 is now available in GitHub Copilot](https://github.blog/changelog/2026-09-22-claude-opus-5-5-is-now-available-in-github-copilot/) ／ [GPT-6 Sol and Luna now available](https://github.blog/changelog/2026-09-22-openais-gpt-6-sol-and-gpt-6-luna-now-available/) — Copilot 側のプラン、対象面、段階展開（GitHub 公式）
- [GitHub Copilot ドキュメント](https://docs.github.com/copilot) — 公式ドキュメント
- [Copilot のカスタマイズ方法](https://docs.github.com/copilot/customizing-copilot) — 公式カスタマイズガイド
- [Agentic Workflows ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.workflows.md) — AI 駆動ワークフローの一覧
- [Hooks ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.hooks.md) — セッションイベント駆動フックの一覧
- [VS Code 1.137 release notes](https://code.visualstudio.com/updates/v1_137) — Automations の公開（Microsoft 公式・2026-09-09、Preview）
- [VS Code 1.138 release notes](https://code.visualstudio.com/updates/v1_138) — Agent Host、Dev Container、Codex session 継続、Automation 共有（Microsoft 公式・2026-09-16）
- [Create and manage agent automations](https://code.visualstudio.com/docs/agents/run/automations) — Preview / rollout、`.automation.md` の portable boundary（Microsoft 公式）
- [Agentic CLI customizations in the usage metrics API](https://github.blog/changelog/2026-09-17-agentic-cli-customizations-now-in-the-usage-metrics-api/) — 上位 5 件、distinct count、privacy と集計上の注意（GitHub 公式）
- [OpenTelemetry in the GitHub Copilot app](https://github.blog/changelog/2026-09-22-opentelemetry-in-the-github-copilot-app/) — appからのOTel exportと本文の既定除外（GitHub公式・2026-09-22）
- [VS Code 1.139 release notes](https://code.visualstudio.com/updates/v1_139) — SSH / Tunnel / WSL 上の Dev Container session と Agent mode policy の修正（Microsoft 公式・2026-09-23）
- [Local sandboxing for GitHub Copilot now generally available](https://github.blog/changelog/2026-10-07-local-sandboxing-for-github-copilot-now-generally-available/) ／ [About cloud and local sandboxes](https://docs.github.com/copilot/concepts/security-governance-and-network-settings/about-cloud-and-local-sandboxes) — local sandbox の GA、MXC、制御項目、managed settings、OS 要件（GitHub 公式・2026-10-07）
- [Local sandboxing in the GitHub Copilot app](https://github.blog/changelog/2026-09-23-local-sandboxing-in-the-github-copilot-app/) — project 単位の file / network / credential 制限（GitHub 公式・2026-09-23、Public Preview）
- [Default enablement of Copilot features for Copilot Business and Enterprise](https://github.blog/changelog/2026-09-24-default-enablement-of-copilot-features-for-copilot-business-and-enterprise/) — 新機能の global default policy と 2026-10-22 の適用開始（GitHub 公式・2026-09-24）
- [Enterprise managed settings in-product validator](https://github.blog/changelog/2026-09-25-enterprise-managed-settings-in-product-validator/) — managed settings / team mappings の検証（GitHub 公式・2026-09-25）
- [VS Code 1.140 release notes](https://code.visualstudio.com/updates/v1_140) — Copilot harness、Agents window の複数フォルダの session と remote host への委任（Experimental）、MCP の保存先、OTel の identity capture（Microsoft 公式・2026-09-30）
- [Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) — 1.0.89〜1.0.91 の `.claude/rules` 互換・`--mcp-github-auth`・`copilot sandbox ca`、1.0.87（2026-09-21）の `strictKnownMarketplaces` と Auto routing tier、1.0.88（2026-09-22）の ACP / AHP / `--server` への managed settings 適用（GitHub 公式）
- [Copilot CLI ACP server](https://docs.github.com/en/copilot/reference/copilot-cli-reference/acp-server) — `copilot --acp` の起動方法と ACP の役割（GitHub 公式）
- [Usage metrics API adds pull request review stages](https://github.blog/changelog/2026-09-25-usage-metrics-api-adds-pull-request-review-stages/) — `pull_request_review_times` の段階別 median / p90（GitHub 公式・2026-09-25）
- [GitHub Copilot weekly releases: September 21](https://github.blog/changelog/2026-09-25-github-copilot-weekly-releases-september-21/) — 同週の Copilot app・VS Code・JetBrains 等の更新一覧（GitHub 公式・2026-09-25）
- [Cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/README.md) — Copilot SDK を活用した実践的コードレシピ集
- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — Plugin の概念と構成（公式）
- [Manage agent skills with GitHub CLI](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) — `gh skill` による Skill 管理（公式）
- [Discover local models in GitHub Copilot CLI](https://github.blog/changelog/2026-10-07-discover-local-models-in-github-copilot-cli/) — `/model` による Ollama の発見と、offline mode・telemetry との違い（GitHub 公式・2026-10-07、CLI 1.0.94-0〜）
- [Using your own LLM models in GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli/customize-copilot/use-byok-models) — provider の種類、`COPILOT_PROVIDER_*`・`COPILOT_OFFLINE`、モデルの要件（GitHub 公式）
- [HydraFusion in VS Code and the GitHub Copilot app](https://github.blog/changelog/2026-09-30-hydrafusion-in-vs-code-and-the-github-copilot-app/) ／ [HydraFusion（docs）](https://docs.github.com/early-access/copilot/hydrafusion) — 実行パターン、課金、組織の制御、注意点（GitHub 公式・2026-09-30、Research preview）
- [Dynamic workflows in Copilot CLI and the Copilot app](https://github.blog/changelog/2026-10-01-dynamic-workflows-in-copilot-cli-and-the-copilot-app/) ／ [About dynamic workflows](https://docs.github.com/en/copilot/concepts/agents/dynamic-workflows) ／ [Use dynamic workflows](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-dynamic-workflows) — autopilot・`/fleet` との違い、上限、権限、CI（GitHub 公式・2026-10-01、Public preview）
- [GitHub Copilot can now interact with desktop apps with computer use](https://github.blog/changelog/2026-10-01-github-copilot-can-now-interact-with-desktop-apps/) — Copilot CLI / app の Computer Use（GitHub 公式・2026-10-01、Public Preview）
- [About computer use in GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/computer-use) ／ [Using GitHub Copilot CLI to interact with desktop applications](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/computer-use) — 使いどころ・限界・承認の流れ（GitHub 公式）
- [Copilot code review: API support and new default effort level](https://github.blog/changelog/2026-10-02-copilot-code-review-api-support-and-new-default-effort-level/) — REST / GraphQL API からの review 依頼と、`Default` が `Balanced` を使う変更（GitHub 公式・2026-10-02）
- [Selected models in GitHub Copilot deprecated](https://github.blog/changelog/2026-10-02-selected-models-in-github-copilot-deprecated/) — 2026-10-02 に廃止されたモデルと移行先（GitHub 公式）
- [Upcoming deprecation of selected GitHub Copilot models in mid-October](https://github.blog/changelog/2026-09-18-upcoming-deprecation-of-selected-github-copilot-models-in-mid-october/) — 2026-10-19 に廃止予定のモデル、代替、管理者向けの扱い（GitHub 公式・2026-09-18）
- [Copilot code review can now approve pull requests](https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/) — approval assessment と approval の区別（公式・2026-09-01、Public Preview）
- [Configuring code review by GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/set-up-copilot/configure-code-review) — 設定階層・パス限定（最大 15 glob）の一次情報（公式）
- [Enterprise managed permissions for GitHub Copilot agent operations](https://github.blog/changelog/2026-09-09-enterprise-managed-permissions-for-github-copilot-agent-operations/) — 操作単位の managed permissions 一般提供（公式・2026-09-09）
- [Enterprise managed settings reference](https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/enterprise-administrators/enterprise-managed-settings) — 規則の優先順位、対象面、サンドボックス設定（公式）
- [Enterprise managed sandbox in Copilot for JetBrains](https://github.blog/changelog/2026-09-08-enterprise-managed-sandbox-in-copilot-for-jetbrains/) — JetBrains の managed sandbox Public Preview（公式・2026-09-08）
- [New features and improvements in Copilot for JetBrains](https://github.blog/changelog/2026-09-22-new-features-and-improvements-in-copilot-for-jetbrains/) — JetBrains 1.18.0 の assisted approvals・共有 Skill・MCP 制御（公式・2026-09-22）
- [Content exclusions generally available in Copilot app and CLI](https://github.blog/changelog/2026-09-02-content-exclusions-generally-available-in-copilot-app-and-cli/) — app / CLI での GA（公式・2026-09-02）
- [Content exclusion for GitHub Copilot](https://docs.github.com/en/copilot/concepts/context/content-exclusion) — 対応面・非対応面と制限の一次情報（公式）

## 関連ドキュメント

- [VS Code エディタウィンドウでの複数ルート運用](multi-root.md) — 複数フォルダを横断するエージェントセッションの設定と制約（Experimental）
- ツール横断の開発手法: [superpowers](../dev-methods/superpowers.md) / [mattpocock/skills](../dev-methods/mattpocock-skills.md) / [AI-DLC ワークフロー](../dev-methods/aidlc-workflows.md) — GitHub Copilot（CLI・コーディングエージェント）にも対応した開発プロセス改善スキル
- [ツール間の用語対照表](../../README.md#ツール間の用語対照表) — 「Skills」「Agents」がツールごとに何を指すかの整理
