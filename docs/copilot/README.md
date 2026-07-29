# GitHub Copilot ガイド

> **対象ツール**: GitHub Copilot ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-29

GitHub Copilot は GitHub が提供するコーディングアシスタントで、IDE 内のインライン補完・チャットが中心です。このページでは、Copilot のカスタマイズの種類と設定方法、クイックスタートを解説します。

## このディレクトリのドキュメント

| ドキュメント | 内容 |
|-------------|------|
| **[Instructions 一覧](instructions.md)** | ファイルパターンに応じてコーディング規約を自動適用するルールファイルの詳細解説 |
| **[Agents 一覧](agents.md)** | Copilot を特定ドメインの専門家ペルソナとして振る舞わせるエージェント定義の詳細解説 |
| **[Prompts / Skills 一覧](prompts.md)** | `/` コマンドから呼び出せる再利用可能なタスクテンプレートおよび Skills の詳細解説 |

---

## カスタマイズの種類

| 種類 | ファイル形式 | 概要 | 適用タイミング |
|------|------------|------|--------------|
| [Instructions](#instructions---コーディング規約の自動適用) | `.instructions.md` | ファイルパターンに応じた規約を自動適用 | コード編集時に自動 |
| [Prompts](#prompts---再利用可能なタスクテンプレート) | `.prompt.md` | VS Code などで `/` コマンドから呼び出すローカルのタスクテンプレート | チャットで手動実行 |
| [Agents](#agents---専門家ペルソナ) | `.agent.md` | 特定ドメインの専門家として振る舞うペルソナ | チャットで手動選択 |
| [Skills](#skills---リソース同梱の複合ツール) | `SKILL.md` + 関連ファイル | upstream の `skills/` で公開される、関連リソース同梱の自己完結型ツール | チャットで手動実行 |
| [Collections](#collections---カスタマイズのセット) | `.collection.yml` | 上記を組み合わせたキュレーション済みセット | プロジェクト単位で適用 |
| [Hooks](#hooks---セッションイベント駆動の自動アクション) | `hooks.json` + スクリプト | Copilot コーディングエージェントのセッションイベントで自動実行 | エージェントセッション中に自動 |
| [Agentic Workflows](#agentic-workflows---ai-駆動のリポジトリ自動化) | `.md`（フロントマター + 自然言語） | GitHub Actions 上で動く AI 自動化ワークフロー | スケジュール・イベントで自動実行 |
| [Cookbook](#cookbook-recipes---実践的なコード例) | コードスニペット集 | Copilot SDK を使ったコピー＆ペーストですぐ使えるコード例 | 実装の参考として随時 |

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

## 参考リンク

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — カスタマイズの公式リポジトリ
- [GitHub Copilot ドキュメント](https://docs.github.com/copilot) — 公式ドキュメント
- [Copilot のカスタマイズ方法](https://docs.github.com/copilot/customizing-copilot) — 公式カスタマイズガイド
- [Agentic Workflows ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.workflows.md) — AI 駆動ワークフローの一覧
- [Hooks ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.hooks.md) — セッションイベント駆動フックの一覧
- [Cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/README.md) — Copilot SDK を活用した実践的コードレシピ集

## 関連ドキュメント

- ツール横断の開発手法: [superpowers](../dev-methods/superpowers.md) / [mattpocock/skills](../dev-methods/mattpocock-skills.md) / [AI-DLC ワークフロー](../dev-methods/aidlc-workflows.md) — GitHub Copilot（CLI・コーディングエージェント）にも対応した開発プロセス改善スキル
- [ツール間の用語対照表](../../README.md#ツール間の用語対照表) — 「Skills」「Agents」がツールごとに何を指すかの整理
