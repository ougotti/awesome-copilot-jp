# Awesome AI Skills JP

> GitHub・OpenAI・Anthropic が公式に公開している **生成AIツールのスキル／エージェント／カスタマイズ機能**を、日本語で体系的に解説するガイドです。  
> エンジニアだけでなく、**事務・経理・金融・バックオフィス**で生成AIを使いたい方にも役立つ情報を集めています。

---

## 🧭 目的から選ぶ

「何を読めばいいか分からない」方は、目的から入口を選んでください。

### 共通・事務活用

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 💬 まず生成AIを触ってみたい（コードは書かない） | [非エンジニア向けクイックスタート](#-非エンジニア向けクイックスタート) |
| 📋 業務シーン別に「使える例」を見たい | [シナリオ別ユースケース集](docs/business/use-cases.md) |
| 🌐 2026年のSkills・MCP・GUI自動化をまとめて知りたい | [2026年7月版 Skills最新動向](docs/trends.md) |
| 📝 議事録・請求書・資料など事務作業を効率化したい | [事務・バックオフィス活用ガイド](docs/business/office-work.md) |
| 💹 決算・経理・金融業務を効率化したい | [金融サービス向けスキル](docs/business/financial-services.md) |

### GitHub Copilot

| やりたいこと | おすすめの入口 |
|------------|--------------|
| ⌨️ コーディング規約を Copilot に守らせたい | [Instructions 一覧](docs/copilot/instructions.md) |
| 🧑‍💻 Copilot を専門家として使いたい | [Agents 一覧](docs/copilot/agents.md) |
| ⚡ `/` コマンドで定型タスクを実行したい | [Prompts / Skills 一覧](docs/copilot/prompts.md) |

### Claude Code

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🤖 Claude Code をターミナルで使いたい | [Claude Code スキル](docs/claude-code/basics.md) |
| 🧱 開発プロセス（要件整理〜TDD〜設計）を改善したい | [mattpocock/skills](docs/dev-methods/mattpocock-skills.md) |
| 📦 公式スキル（docx/pdf/pptx/xlsx 等）を知りたい | [Anthropic 公式スキル](docs/claude-code/official-skills.md) |

### Codex

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🚀 Codex でデプロイ・ブラウザ自動化を追加したい | [Codex 公式スキル](docs/codex/README.md) |

### AWS AI-DLC

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🏗️ AI エージェントに 3 フェーズの開発ライフサイクルを適用したい | [AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md) |

---

## 🚀 非エンジニア向けクイックスタート

コードを書かない方でも、**3 ステップ**で生成AIを業務に使えます。

1. **[Claude.ai](https://claude.ai) の有料プランに登録** — Word／Excel／PowerPoint／PDF を扱うスキルが最初から使えます。
2. **ファイルを添付して、日本語で頼むだけ** — 例：「この議事録メモを、決定事項と ToDo に分けた Word にして」
3. **出力をダウンロードして確認・微修正** — 数値や固有名詞は必ず自分で確認しましょう。

> 「どんなことを頼めるの？」という方は、まず [シナリオ別ユースケース集](docs/business/use-cases.md) を眺めてみてください。

---

## ドキュメント一覧

### GitHub Copilot

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Instructions 一覧](docs/copilot/instructions.md)** | ファイルパターンに応じてコーディング規約を自動適用するルールファイルの詳細解説 | 197 件 |
| **[Agents 一覧](docs/copilot/agents.md)** | Copilot を特定ドメインの専門家ペルソナとして振る舞わせるエージェント定義の詳細解説 | 240 件 |
| **[Prompts / Skills 一覧](docs/copilot/prompts.md)** | `/` コマンドから呼び出せる再利用可能なタスクテンプレートおよび Skills の詳細解説 | 137 件 |

### Claude Code

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Claude Code スキル](docs/claude-code/basics.md)** | Claude Code 専用のスラッシュコマンド、カスタムコマンド、フック、CLAUDE.md、MCP 連携の解説 | — |
| **[Anthropic 公式スキル](docs/claude-code/official-skills.md)** | [anthropics/skills](https://github.com/anthropics/skills) リポジトリ収録の 17 スキル（docx/pdf/pptx/xlsx 等）の詳細解説 | 17 件 |
| **[mattpocock/skills](docs/dev-methods/mattpocock-skills.md)** | [mattpocock/skills](https://github.com/mattpocock/skills) の実務エンジニア向けスキル集（grill-me / to-prd / tdd 等、開発プロセス改善型） | 21 件 |
| **[superpowers](docs/dev-methods/superpowers.md)** | [obra/superpowers](https://github.com/obra/superpowers) の SDLC スキルフレームワーク（brainstorming / TDD / systematic-debugging 等 14 スキル） ※ Claude Code・Codex・Copilot CLI など複数ツール対応 | 14 件 |

### Codex

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Codex 公式スキル](docs/codex/README.md)** | [openai/skills](https://github.com/openai/skills) リポジトリ収録の Codex Agent Skills（system/curated/experimental の 3 層構成）の詳細解説 | 40+ 件 |

### AWS AI-DLC

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md)** | [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) の AI 駆動開発ライフサイクル（Inception → Construction → Operations の 3 フェーズ）の詳細解説。GitHub Copilot・Claude Code・Amazon Q・Cursor など主要エージェント対応 | — |

### 共通・事務活用

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[シナリオ別ユースケース集](docs/business/use-cases.md)** | 役割・業務シーンから探す生成AIの実例カタログ（プロンプト例つき） | — |
| **[事務・バックオフィス活用ガイド](docs/business/office-work.md)** | 議事録・請求書・レポート・スプレッドシート作成など、日々の事務作業を生成AIで効率化する実践ガイド | — |
| **[金融サービス向けスキル](docs/business/financial-services.md)** | [anthropics/financial-services](https://github.com/anthropics/financial-services) 収録の金融・経理業務向けエージェント／スキル（決算照合・月次決算・KYC 等）の詳細解説 | 10 エージェント + 7 業務プラグイン |
| **[2026年7月版 Skills最新動向](docs/trends.md)** | Matt Pocock、Context7、Firecrawl、Vercel、Record & Replay、Computer Use / Browser Use の比較と使い分け | 6 テーマ |

---

## このガイドについて

生成AIツールは、そのままでも強力なアシスタントですが、**スキル・エージェント・カスタマイズ**を適用することで、用途に特化した使い方ができます。

| ツール | 提供元 | 特徴 |
|-------|-------|------|
| **GitHub Copilot** | GitHub | IDE 内インライン補完・チャット中心。Instructions／Agents／Skills でチームのルールや専門家ペルソナを適用 |
| **Claude Code** | Anthropic | ターミナルベースのコーディングエージェント。スラッシュコマンドやフックで複雑なタスクを自動化 |
| **Codex** | OpenAI | Agent Skills でデプロイ・ブラウザ自動化・外部サービス連携などを追加 |

### ツール間の用語対照表

「Skills」「Agents」などの用語は、**ツールによって指すものが異なります**。本ガイドを読んでいて迷ったら、この表に戻ってください。

| 用語 | GitHub Copilot | Claude Code / Claude | Codex（OpenAI） |
|------|----------------|----------------------|------------------|
| **Skills** | `SKILL.md` + 関連リソース同梱の自己完結型ツール（upstream では旧 Prompts の移行先） | Agent Skills。[anthropics/skills](https://github.com/anthropics/skills) の公式スキル（docx / pdf 等）や [mattpocock/skills](https://github.com/mattpocock/skills) 等の手順スキル | Agent Skills。[openai/skills](https://github.com/openai/skills) の system / curated / experimental 3層カタログ |
| **Agents** | 専門家ペルソナ定義（`.agent.md`） | サブエージェント（メインの会話から分離して動く補助エージェント） | —（相当機能はスキルで代替） |
| **Instructions** | ファイルパターン別にコーディング規約を自動適用（`.instructions.md`） | `CLAUDE.md` がほぼ同じ役割 | `AGENTS.md` がほぼ同じ役割 |
| **Prompts** | `/` コマンドのタスクテンプレート（`.prompt.md`） | カスタムコマンド（`.claude/commands/`） | カスタムプロンプト（`~/.codex/prompts/`） |
| **Hooks** | コーディングエージェントセッションのイベント駆動スクリプト（`hooks.json`） | `PreToolUse` / `PostToolUse` 等のイベント駆動自動化 | — |

> 各ドキュメントの冒頭には「**対象ツール**」ヘッダーを付けています。どのツールの話か迷ったら、ページ先頭とこの表を確認してください。

---

## GitHub Copilot

GitHub Copilot のカスタマイズは、以下の種類があります。

### カスタマイズの種類

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

> **補足**: upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) では、Prompts のカタログは **[skills/](https://github.com/github/awesome-copilot/tree/main/skills)** に移行済みです。ローカルでは `.prompt.md` を使い続けられますが、この README の upstream 参照リンクは `xxx.prompt.md` 表記で skills/ を指しています。

---

### Instructions - コーディング規約の自動適用

#### 概要

Instructions は、特定のファイルパターン（例: `*.py`, `*.tsx`）に対して、Copilot が従うべきコーディング規約やベストプラクティスを定義するものです。一度設定すれば、該当ファイルを編集するたびに自動的に適用されます。

#### こんなときに使える

- **チームのコーディング規約を徹底したい** — レビューで毎回指摘する代わりに、Copilot が最初から規約に沿ったコードを生成する
- **特定フレームワークの推奨パターンを適用したい** — React の関数コンポーネントスタイルや、Python の型ヒント付きコードを標準にする
- **新人のオンボーディングを加速したい** — プロジェクト固有のパターンを Instructions に記述しておけば、初日から規約に沿ったコードが書ける

#### 利用できる主な Instructions

##### プログラミング言語

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**C#**](https://github.com/github/awesome-copilot/blob/main/instructions/csharp.instructions.md) | .NET 規約、null 安全性、LINQ パターン | .NET アプリケーション開発 |
| [**Go**](https://github.com/github/awesome-copilot/blob/main/instructions/go.instructions.md) | エラーハンドリング、goroutine パターン | Go サービス開発 |
| [**Rust**](https://github.com/github/awesome-copilot/blob/main/instructions/rust.instructions.md) | 所有権パターン、Result 型の活用 | Rust プロジェクト |

##### Web フレームワーク

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Next.js**](https://github.com/github/awesome-copilot/blob/main/instructions/nextjs.instructions.md) | App Router、Server Components | Next.js フルスタック開発 |
| [**Svelte**](https://github.com/github/awesome-copilot/blob/main/instructions/svelte.instructions.md) | ストア管理、コンポーネント設計 | Svelte アプリケーション開発 |
| [**Blazor**](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | コンポーネントライフサイクル、状態管理 | .NET Web UI 開発 |

##### インフラ・DevOps

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Terraform**](https://github.com/github/awesome-copilot/blob/main/instructions/terraform.instructions.md) | モジュール構成、状態管理、命名規則 | IaC によるインフラ管理 |
| [**Kubernetes**](https://github.com/github/awesome-copilot/blob/main/instructions/kubernetes-manifests.instructions.md) | マニフェスト構成、リソース制限 | K8s デプロイメント管理 |
| [**GitHub Actions**](https://github.com/github/awesome-copilot/blob/main/instructions/github-actions-ci-cd-best-practices.instructions.md) | ワークフロー構成、セキュリティ設定 | CI/CD パイプライン構築 |
| [**Docker**](https://github.com/github/awesome-copilot/blob/main/instructions/containerization-docker-best-practices.instructions.md) | マルチステージビルド、セキュリティ | コンテナイメージ最適化 |
| [**Azure**](https://github.com/github/awesome-copilot/tree/main/instructions) | リソース命名、セキュリティ設定 | Azure クラウド構築 |

##### テスト

| カテゴリ | 主なルール例 | 活用場面 |
|---------|------------|---------|
| [**Playwright**](https://github.com/github/awesome-copilot/blob/main/instructions/playwright-typescript.instructions.md) | E2E テストパターン、Page Object Model | ブラウザ自動テスト |
| [**Vitest**](https://github.com/github/awesome-copilot/blob/main/instructions/nodejs-javascript-vitest.instructions.md) | ユニットテスト構成、モック戦略 | Vite プロジェクトのテスト |
| [**Pester**](https://github.com/github/awesome-copilot/blob/main/instructions/powershell-pester-5.instructions.md) | PowerShell テストパターン | PowerShell スクリプトのテスト |

#### 設定方法

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

**→ 全 Instructions の詳細は [docs/copilot/instructions.md](docs/copilot/instructions.md) を参照**

---

### Prompts - 再利用可能なタスクテンプレート

#### 概要

Prompts は、Copilot Chat の `/` コマンドから呼び出せる再利用可能なタスクテンプレートです。繰り返し行う定型作業をテンプレート化することで、一貫した品質の出力を得られます。

> **注意**: upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) では、Prompts は **[Skills](https://github.com/github/awesome-copilot/tree/main/skills)** に移行されました。VS Code などのローカル機能では `.prompt.md` を `.github/prompts/` に置く運用が残っていますが、以下のリンクは現在の Skills ディレクトリを参照しています。

#### こんなときに使える

- **README やドキュメントを毎回同じ品質で作りたい** — テンプレート化されたプロンプトで、抜け漏れなくドキュメントを生成
- **コードレビューの観点を統一したい** — セキュリティ、パフォーマンス、保守性など、チーム共通のレビュー基準でチェック
- **テストコードの雛形を素早く作りたい** — フレームワーク固有のテスト構造を一発生成
- **定型的なコード生成を効率化したい** — API エンドポイント、データモデル、コンポーネントなどの雛形生成

#### 利用できる主な Prompts

##### ドキュメント生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**create-readme.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-readme) | README.md の作成 | 新規プロジェクトの初期セットアップ |
| [**create-specification.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-specification) | 技術仕様書の作成 | 機能開発の設計フェーズ |
| [**create-architectural-decision-record.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-architectural-decision-record) | Architecture Decision Record の作成 | アーキテクチャ上の意思決定を記録 |

##### テスト生成

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**javascript-typescript-jest.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/javascript-typescript-jest) | Jest テスト生成 | JavaScript/TypeScript ユニットテスト |
| [**java-junit.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/java-junit) | JUnit テスト生成 | Java ユニットテスト |
| [**playwright-generate-test.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/playwright-generate-test) | Playwright テスト生成 | E2E テストの自動生成 |
| [**csharp-nunit.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/csharp-nunit) | NUnit テスト生成 | .NET ユニットテスト |

##### インフラ・DevOps

| プロンプト名 | 用途 | 活用場面 |
|-------------|------|---------|
| [**multi-stage-dockerfile.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/multi-stage-dockerfile) | Dockerfile 生成 | コンテナ化 |
| [**create-github-action-workflow-specification.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/create-github-action-workflow-specification) | GitHub Actions ワークフロー生成 | CI/CD セットアップ |
| [**sql-optimization.prompt.md**](https://github.com/github/awesome-copilot/tree/main/skills/sql-optimization) | SQL クエリ最適化 | データベースパフォーマンス改善 |

#### 設定方法

VS Code などのローカルカスタマイズでは、Prompt ファイルをリポジトリの `.github/prompts/` ディレクトリに配置します。

```
.github/
  prompts/
    create-readme.prompt.md
    generate-jest-tests.prompt.md
```

Copilot Chat で `/create-readme` のように入力すると呼び出せます。

**→ 全 Prompts / Skills の詳細は [docs/copilot/prompts.md](docs/copilot/prompts.md) を参照**

---

### Agents - 専門家ペルソナ

#### 概要

Agents は、Copilot を特定ドメインの専門家として振る舞わせるペルソナ定義です。MCP（Model Context Protocol）サーバーと連携させることで、外部ツールやサービスと直接やり取りする能力を持たせることもできます。

#### こんなときに使える

- **コードレビューを専門家の視点で行いたい** — セキュリティレビューア、パフォーマンスエキスパートとして分析
- **特定クラウドサービスの構築に詳しいアドバイザーが欲しい** — Azure、AWS などのアーキテクト視点でアドバイス
- **データベース設計の相談相手が欲しい** — PostgreSQL、MongoDB などの DBA として最適化の提案を受ける
- **メンターとして段階的に教えてほしい** — いきなり回答を出さず、考え方をガイドしてくれるメンター

#### 利用できる主な Agents

##### コードの品質と開発プロセス

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| [**code-reviewer**](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md) | コードレビューの専門家 | PR レビュー、コード品質向上 |
| [**security-reviewer**](https://github.com/github/awesome-copilot/blob/main/agents/se-security-reviewer.agent.md) | セキュリティレビューの専門家 | 脆弱性チェック、セキュリティ監査 |
| [**technical-writer**](https://github.com/github/awesome-copilot/blob/main/agents/se-technical-writer.agent.md) | テクニカルライター | API ドキュメント、ユーザーガイド作成 |
| [**mentor**](https://github.com/github/awesome-copilot/blob/main/agents/mentor.agent.md) | メンター・教育者 | 新人指導、学習支援 |

##### インフラ・クラウド

| エージェント名 | 役割 | 活用場面 |
|--------------|------|---------|
| [**azure-architect**](https://github.com/github/awesome-copilot/blob/main/agents/azure-principal-architect.agent.md) | Azure アーキテクト | Azure 環境設計 |
| [**kubernetes-sre**](https://github.com/github/awesome-copilot/blob/main/agents/platform-sre-kubernetes.agent.md) | Kubernetes SRE | K8s 運用・トラブルシュート |
| [**terraform-expert**](https://github.com/github/awesome-copilot/blob/main/agents/terraform.agent.md) | Terraform の専門家 | IaC 設計・最適化 |

#### 設定方法

Agent ファイルをリポジトリの `.github/agents/` ディレクトリに配置します。

```
.github/
  agents/
    code-reviewer.agent.md
    azure-architect.agent.md
```

**→ 全 Agents の詳細は [docs/copilot/agents.md](docs/copilot/agents.md) を参照**

---

### Skills - リソース同梱の複合ツール

#### 概要

Skills は、Instructions だけでは実現できない、関連リソース（テンプレートファイル、設定ファイル、サンプルコードなど）を同梱した自己完結型のツールキットです。

#### こんなときに使える

- **コミットメッセージを規約に沿って自動生成したい** — `git-commit` スキルがリポジトリの変更を分析して適切なメッセージを提案
- **アーキテクチャ図を自動生成したい** — `excalidraw-diagram-generator` や `plantuml-ascii` でコードからダイアグラムを生成
- **PRD（プロダクト要件定義書）を標準フォーマットで作りたい** — `prd` スキルで統一的な要件定義書を作成

#### 利用できる主な Skills

| スキル名 | 機能 | 活用場面 |
|---------|------|---------|
| **git-commit** | コミットメッセージ自動生成 | 日常のコミット作業 |
| **github-issues** | GitHub Issue の作成支援 | バグ報告・機能要求の整理 |
| **prd** | プロダクト要件定義書作成 | 新機能の要件定義 |
| **excalidraw-diagram-generator** | 図表自動生成 | アーキテクチャ図の作成 |
| **azure-deployment-preflight** | Azure デプロイ事前チェック | デプロイ前の検証 |

#### 設定方法

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

### Collections - カスタマイズのセット

#### 概要

Collections は、関連する Instructions、Prompts、Agents、Skills をテーマごとにまとめたキュレーション済みのセットです。

#### こんなときに使える

- **新規プロジェクトのセットアップを効率化したい** — 技術スタックに合った Collection を選ぶだけで必要なカスタマイズ一式が揃う
- **チーム全体の開発環境を統一したい** — Collection を共有すれば全員が同じルールとツールを使える

#### 利用できる主な Collections

| コレクション名 | 含まれるカスタマイズ | 活用場面 |
|--------------|-------------------|---------|
| **java-development** | Java の Instructions + Prompts + Agents | Java プロジェクト全般 |
| **csharp-dotnet-development** | C#/.NET の全カスタマイズ | .NET プロジェクト全般 |
| **python-mcp-development** | Python MCP サーバー開発用一式 | Python で MCP サーバーを構築 |
| **security-best-practices** | セキュリティカスタマイズ | セキュリティ対策の強化 |
| **devops-oncall** | オンコール対応カスタマイズ | 運用・障害対応 |

#### 設定方法

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

### Hooks - セッションイベント駆動の自動アクション

#### 概要

Hooks は、GitHub Copilot コーディングエージェントのセッション中に発生する特定のイベントをトリガーとして自動実行されるスクリプトです。

#### こんなときに使える

- **セッションのログ・監査証跡を残したい** — セッション開始・終了・プロンプトを自動記録
- **危険な操作を事前にブロックしたい** — 破壊的ファイル操作や force push などをエージェントが実行する前に遮断
- **シークレットの漏洩を防ぎたい** — セッション中に変更されたファイルを自動スキャン

#### 利用できる主な Hooks

| フック名 | 概要 | 対応イベント |
|---------|------|------------|
| [**dependency-license-checker**](https://github.com/github/awesome-copilot/tree/main/hooks/dependency-license-checker) | 新規追加依存関係のライセンスコンプライアンスチェック | sessionEnd |
| [**secrets-scanner**](https://github.com/github/awesome-copilot/tree/main/hooks/secrets-scanner) | セッション中に変更されたファイルのシークレット検出 | sessionEnd |
| [**session-auto-commit**](https://github.com/github/awesome-copilot/tree/main/hooks/session-auto-commit) | セッション終了時に変更を自動コミット＆プッシュ | sessionEnd |
| [**tool-guardian**](https://github.com/github/awesome-copilot/tree/main/hooks/tool-guardian) | 危険なツール操作（破壊的ファイル操作、force push）をブロック | preToolUse |

#### 設定方法

```
.github/
  hooks/
    session-auto-commit/
      hooks.json
      auto-commit.sh
```

---

### Agentic Workflows - AI 駆動のリポジトリ自動化

#### 概要

Agentic Workflows は、GitHub Actions 上でコーディングエージェントを実行する AI 駆動のリポジトリ自動化の仕組みです。

#### こんなときに使える

- **Issue のトリアージ・ラベリングを自動化したい** — 新しい Issue を自動で分類し、適切なラベルを付与
- **定期的なステータスレポートを生成したい** — 毎日・毎週の進捗サマリーを自動作成
- **スラッシュコマンドで操作したい** — Issue や PR にコメントするだけでエージェントを呼び出せる

#### 利用できる主な Agentic Workflows

| ワークフロー名 | 概要 | トリガー |
|--------------|------|---------|
| [**daily-issues-report**](https://github.com/github/awesome-copilot/blob/main/workflows/daily-issues-report.md) | 未解決 Issue の日次サマリーを Issue に投稿 | schedule |
| [**ospo-org-health**](https://github.com/github/awesome-copilot/blob/main/workflows/ospo-org-health.md) | ステール Issue/PR・コントリビューターランキングの週次レポート | schedule |
| [**relevance-check**](https://github.com/github/awesome-copilot/blob/main/workflows/relevance-check.md) | Issue や PR がプロジェクトに関連するかをスラッシュコマンドで評価 | slash_command |

#### 設定方法

```bash
# gh aw 拡張機能をインストール
gh extension install github/gh-aw

# ワークフロー定義ファイルをコンパイル
gh aw compile
```

---

### Cookbook Recipes - 実践的なコード例

#### 概要

Cookbook Recipes は、GitHub Copilot SDK を使ったアプリケーション開発のための実践的なコードスニペット集です。

#### 対応言語

| 言語 | 提供される例 |
|------|------------|
| **.NET (C#)** | SDK セットアップ、エラーハンドリング、セッション管理 |
| **Go** | SDK セットアップ、ファイル操作、ベストプラクティス |
| **Node.js (TypeScript)** | SDK セットアップ、非同期処理、ストリーミング |
| **Python** | SDK セットアップ、エラーハンドリング、統合パターン |

---

## Claude Code

Claude Code は Anthropic が提供するターミナルベースのコーディングエージェントです。GitHub Copilot が IDE 内のインライン補完に特化しているのに対し、ファイルシステム全体を横断する複雑なタスクをこなせるエージェントとして設計されています。

### 主な機能

| 機能 | 概要 |
|-----|------|
| **組み込みスラッシュコマンド** | `/init`, `/review`, `/code-review`, `/compact` など |
| **カスタムコマンド** | `.claude/commands/` に Markdown を置いてコマンド化 |
| **フック（Hooks）** | `PreToolUse`, `PostToolUse`, `Stop` などのイベント駆動自動化 |
| **CLAUDE.md** | プロジェクトのコンテキストと規約を記述するファイル |
| **MCP 連携** | GitHub、PostgreSQL、Slack などの外部ツールと統合 |

**→ Claude Code スキルの詳細は [docs/claude-code/basics.md](docs/claude-code/basics.md) を参照**

---

### Anthropic 公式スキル

[anthropics/skills](https://github.com/anthropics/skills) は Anthropic が公開している Claude 用スキルのリポジトリです。Word・PDF・PowerPoint・Excel などのドキュメント処理スキルや、生成アート・MCP サーバービルドなど 17 種類のスキルが収録されています。

#### カテゴリ別スキル一覧

| カテゴリ | スキル | 主な機能 |
|---------|-------|---------|
| **ドキュメント処理** | docx / pdf / pptx / xlsx | Word・PDF・PowerPoint・Excel の自動生成・編集・変換 |
| **クリエイティブ** | algorithmic-art / canvas-design / frontend-design / theme-factory | アート・デザイン・UI の生成 |
| **開発・技術** | claude-api / mcp-builder / webapp-testing / web-artifacts-builder | API 開発・MCP 構築・Web テスト |
| **エンタープライズ** | brand-guidelines / doc-coauthoring / internal-comms / slack-gif-creator / skill-creator | 組織コミュニケーション・カスタムスキル作成 |

#### インストール方法（Claude Code）

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**→ Anthropic 公式スキルの詳細は [docs/claude-code/official-skills.md](docs/claude-code/official-skills.md) を参照**

---

## Codex（OpenAI）

[openai/skills](https://github.com/openai/skills) は OpenAI が公開している Codex 用スキルのカタログリポジトリです。system / curated / experimental の 3 層構造で、デプロイ・Figma・Notion・セキュリティ・ブラウザ自動化など 40 種類以上のスキルが収録されています。

### スキル階層

| 階層 | 説明 | インストール |
|-----|------|------------|
| **System** | Codex に自動インストールされる基盤スキル（skill-installer, skill-creator 等） | 不要 |
| **Curated** | OpenAI が精選した高品質スキル（linear, playwright, vercel-deploy 等） | スキル名で指定 |
| **Experimental** | コミュニティ提供の実験的スキル | パス / URL で指定 |

### インストール方法（Codex CLI）

```bash
# Codex セッション内で $skill-installer を使用
$skill-installer linear
$skill-installer playwright
$skill-installer vercel-deploy
```

### 主なカテゴリ

| カテゴリ | スキル例 |
|---------|---------|
| **デプロイ** | cloudflare-deploy / netlify-deploy / render-deploy / vercel-deploy |
| **GitHub 連携** | gh-address-comments / gh-fix-ci |
| **ブラウザ自動化** | playwright / playwright-interactive / screenshot |
| **Figma** | figma-implement-design / figma-generate-design など 8 種 |
| **Notion** | notion-spec-to-implementation / notion-meeting-intelligence など 4 種 |
| **セキュリティ** | security-best-practices / security-threat-model など 3 種 |

**→ Codex 公式スキルの詳細は [docs/codex/README.md](docs/codex/README.md) を参照**

---

## 事務・ビジネス業務での活用

生成AIはコーディングだけでなく、**事務・経理・総務・営業事務**といったバックオフィス業務の効率化にも役立ちます。Word／Excel／PowerPoint／PDF の自動生成・編集や、金融・経理業務に特化したエージェントを活用できます。

### こんなときに使える

- **議事録・報告書・案内文を素早く作りたい** — 走り書きメモから整った文書を生成
- **バラバラの表を集計・整形したい** — 複数の Excel を共通フォーマットに統合
- **提案資料・報告スライドを量産したい** — 文章メモから構成済みのスライドを作成
- **請求書 PDF から情報を転記したい** — 帳票からの抽出・フォーム入力を自動化
- **月次決算・勘定照合・取引先審査を効率化したい** — 金融・経理向けエージェントでドラフト作成

### 主なドキュメント

| ドキュメント | 内容 |
|-------------|------|
| **[事務・バックオフィス活用ガイド](docs/business/office-work.md)** | 議事録・請求書・集計表・スライド作成など、業種を問わない事務作業の実践レシピ |
| **[金融サービス向けスキル](docs/business/financial-services.md)** | 決算照合・月次決算・KYC・バリュエーションなど金融・経理業務向けエージェント／スキル |

> **ポイント**: 金額・税・日付などの数値や、契約・法的文書は**必ず人（有資格者）が確認**してください。生成AIの出力はドラフトとして扱うのが安全です。

---

## クイックスタートガイド

### GitHub Copilot — 最小構成で始める

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

### GitHub Copilot — チーム向けの推奨構成

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

### Claude Code を導入する

```bash
# Claude Code のインストール
npm install -g @anthropic-ai/claude-code

# プロジェクトに CLAUDE.md を生成
claude
/init
```

---

## よくある質問

### Q: Instructions と Agents の違いは？

**Instructions** はファイルパターンに応じて**自動的に**適用されるルールです。一方、**Agents** はチャットで**明示的に選択**して使う専門家ペルソナです。

### Q: GitHub Copilot と Claude Code の違いは？

**GitHub Copilot** は GitHub が提供するコーディングアシスタントで、IDE 内のインライン補完やチャットが中心です。**Claude Code** は Anthropic が提供するターミナルベースのエージェントで、ファイルシステム全体を横断する複雑なタスクに向いています。

### Q: GitHub Copilot と Codex の違いは？

**GitHub Copilot** は IDE 補完・チャット向けのカスタマイズが中心です。**Codex**（OpenAI）はターミナルベースのエージェントで、Agent Skills によってデプロイ・ブラウザ自動化・外部サービス連携などのワークフローを追加できます。

### Q: 既存のプロジェクトにも適用できる？

はい。`.github/` ディレクトリにファイルを追加するだけで、既存プロジェクトにも適用できます。コードベースへの変更は不要です。

### Q: カスタマイズはどのプランで使える？

Instructions、Prompts、Agents は GitHub Copilot のすべてのプラン（Free、Pro、Pro+、Business、Enterprise）で利用可能です。

---

## 参考リンク

### GitHub Copilot

- [github/awesome-copilot](https://github.com/github/awesome-copilot) — カスタマイズの公式リポジトリ
- [GitHub Copilot ドキュメント](https://docs.github.com/copilot) — 公式ドキュメント
- [Copilot のカスタマイズ方法](https://docs.github.com/copilot/customizing-copilot) — 公式カスタマイズガイド
- [Agentic Workflows ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.workflows.md) — AI 駆動ワークフローの一覧
- [Hooks ドキュメント](https://github.com/github/awesome-copilot/blob/main/docs/README.hooks.md) — セッションイベント駆動フックの一覧
- [Cookbook](https://github.com/github/awesome-copilot/blob/main/cookbook/README.md) — Copilot SDK を活用した実践的コードレシピ集

### Claude Code

- [Claude Code 公式ドキュメント](https://docs.anthropic.com/ja/docs/claude-code/overview) — Claude Code の使い方
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic 公式 Claude スキルリポジトリ

### Codex

- [openai/skills](https://github.com/openai/skills) — Codex 公式スキルカタログ

---

> **注意**: このガイドは [github/awesome-copilot](https://github.com/github/awesome-copilot) リポジトリの内容および公式ドキュメントを元に作成しています。GitHub および Anthropic はこれらのカスタマイズの機能やセキュリティを保証するものではありません。利用前にカスタマイズの内容を確認してください。
