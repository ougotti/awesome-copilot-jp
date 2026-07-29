# Skills (旧 Prompts) 一覧と活用ガイド

> **注意**: upstream の [github/awesome-copilot](https://github.com/github/awesome-copilot) では、Prompts は **[Skills](https://github.com/github/awesome-copilot/tree/main/skills)** に移行されました。各リンクは現在の Skills ディレクトリを指しています。

## Prompts とは

Prompts は、Copilot Chat の `/` コマンドから呼び出せる**再利用可能なタスクテンプレート**です。繰り返し行う定型作業をテンプレート化することで、一貫した品質の出力を得られます。

Instructions が「自動適用されるルール」、Agents が「相談相手の専門家」なら、Prompts は「定型タスクのレシピ」です。

### 設定方法

```
.github/
  prompts/
    create-readme.prompt.md
    generate-jest-tests.prompt.md
```

Copilot Chat で `/create-readme` のように入力すると呼び出せます。

---

## カテゴリ別 Prompts 一覧

### ドキュメント生成

#### README・仕様書

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`create-readme.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-readme) | README.md 作成 | プロジェクトルートの README.md |
| [`create-specification.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-specification) | AI 向け仕様書作成 | `/spec/spec-*.md` |
| [`create-architectural-decision-record.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-architectural-decision-record) | ADR（アーキテクチャ決定記録）作成 | `/docs/adr/adr-NNNN-*.md` |
| [`create-technical-spike.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-technical-spike) | 技術スパイクドキュメント作成 | `/spikes/*-spike.md` |
| [`documentation-writer.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/documentation-writer) | Diataxis フレームワークに基づくドキュメント | チュートリアル、How-to、リファレンス、説明 |
| [`create-tldr-page.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-tldr-page) | TLDR ページ作成 | コマンドの簡潔な説明 |
| [`tldr-prompt.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/tldr-prompt) | TLDR 形式の説明 | 簡潔な概要 |
| [`readme-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/readme-blueprint-generator) | README 設計図生成 | README の構造案 |

**[create-readme.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/create-readme)** の特徴:
- ワークスペース全体をレビューして README を生成
- GitHub Flavored Markdown（GFM）+ admonition 構文
- 過剰な絵文字を避けた簡潔なコンテンツ
- LICENSE/CONTRIBUTING/CHANGELOG は別ファイルに（README には含めない）

**[create-specification.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/create-specification)** の特徴:
- AI 向けに最適化された機械可読な仕様書
- 明確で曖昧さのない言語
- `/spec/` ディレクトリに保存
- 11 セクション構成（Introduction, Requirements, Acceptance Criteria 等）
- YAML フロントマター（title, version, dates, owner, tags）

**[create-architectural-decision-record.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/create-architectural-decision-record)** の特徴:
- `/docs/adr/` に連番で保存（adr-0001-*, adr-0002-* ...）
- ステータス追跡（Proposed/Accepted/Rejected/Superseded/Deprecated）
- Consequences セクション（POS/NEG コーディング）
- 代替案と却下理由の文書化

---

#### 計画・設計

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`create-implementation-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-implementation-plan) | 実装計画作成 | `/plan/[purpose]-[component]-[version].md` |
| [`update-implementation-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/update-implementation-plan) | 実装計画更新 | 既存計画の更新 |
| [`breakdown-epic-pm.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-epic-pm) | Epic PRD 作成（PM 向け） | `/docs/ways-of-work/plan/{epic}/epic.md` |
| [`breakdown-epic-arch.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-epic-arch) | Epic アーキテクチャ仕様（アーキテクト向け） | `/docs/ways-of-work/plan/{epic}/arch.md` |
| [`breakdown-feature-prd.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-feature-prd) | Feature PRD 作成 | `/docs/ways-of-work/plan/{epic}/{feature}/prd.md` |
| [`breakdown-feature-implementation.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-feature-implementation) | Feature 実装計画 | `/docs/ways-of-work/plan/{epic}/{feature}/implementation-plan.md` |
| [`breakdown-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-plan) | GitHub プロジェクト計画 | project-plan.md + issues-checklist.md |
| [`breakdown-test.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-test) | テスト戦略・QA 計画 | テスト戦略、Issue チェックリスト、QA 計画 |
| [`architecture-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/architecture-blueprint-generator) | アーキテクチャ設計図生成 | アーキテクチャ図 |
| [`code-exemplars-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/code-exemplars-blueprint-generator) | コード例設計図生成 | コード例の構造 |
| [`copilot-instructions-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/copilot-instructions-blueprint-generator) | Copilot Instructions 設計図 | Instructions ファイル構造 |
| [`folder-structure-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/folder-structure-blueprint-generator) | フォルダ構造設計図 | ディレクトリ構造 |
| [`project-workflow-analysis-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/project-workflow-analysis-blueprint-generator) | プロジェクトワークフロー分析 | ワークフロー設計 |
| [`technology-stack-blueprint-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/technology-stack-blueprint-generator) | 技術スタック設計図 | 技術選定ガイド |

**[create-implementation-plan.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/create-implementation-plan)** の特徴:
- AI-to-AI コミュニケーション向けの決定論的言語
- Purpose プレフィックス: `upgrade`, `refactor`, `feature`, `data`, `infrastructure`, `process`, `architecture`, `design`
- 8 セクション構成（Requirements, Implementation Steps, Alternatives, Dependencies, Files, Testing, Risks, Related Specs）
- 標準 ID プレフィックス（REQ-, TASK-, SEC-, CON-）
- 具体的なファイルパスと関数名を含む

**[breakdown-epic-pm.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-epic-pm)** の特徴:
- SaaS プラットフォーム向け Epic PRD
- 8 セクション構成（Epic Name, Goal, User Personas, User Journeys, Business Requirements, Success Metrics, Out of Scope, Business Value）
- 機能要件と非機能要件の分離
- KPI の定義

**[breakdown-test.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/breakdown-test)** の特徴:
- ISTQB / ISO 25010 準拠
- GitHub Issue テンプレート生成（テスト戦略: 2-3 SP、Playwright E2E: 2-5 SP、QA 検証: 3-5 SP）
- 品質目標: > 80% 行カバレッジ、> 90% ブランチカバレッジ（クリティカルパス）

---

### MCP サーバー生成

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`python-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/python-mcp-server-generator) | Python MCP サーバー生成 | 完全な Python プロジェクト |
| [`typescript-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/typescript-mcp-server-generator) | TypeScript MCP サーバー生成 | 完全な Node.js/TypeScript プロジェクト |
| [`csharp-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-mcp-server-generator) | C# MCP サーバー生成 | 完全な C# コンソールアプリ |
| [`go-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/go-mcp-server-generator) | Go MCP サーバー生成 | 完全な Go プロジェクト |
| [`java-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-mcp-server-generator) | Java MCP サーバー生成 | Maven/Gradle プロジェクト |
| [`rust-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/rust-mcp-server-generator) | Rust MCP サーバー生成 | 完全な Rust プロジェクト |
| [`kotlin-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/kotlin-mcp-server-generator) | Kotlin MCP サーバー生成 | Kotlin プロジェクト |
| [`ruby-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/ruby-mcp-server-generator) | Ruby MCP サーバー生成 | 完全な Ruby プロジェクト |
| [`php-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/php-mcp-server-generator) | PHP MCP サーバー生成 | 完全な PHP プロジェクト |
| [`swift-mcp-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/swift-mcp-server-generator) | Swift MCP サーバー生成 | Swift 6.0+ プロジェクト |
| [`mcp-copilot-studio-server-generator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/mcp-copilot-studio-server-generator) | Copilot Studio MCP サーバー | Copilot Studio 連携 |

**MCP サーバー生成プロンプトの共通特徴:**
- 完全なプロジェクト構造（設定ファイル、ディレクトリ構成）
- 公式 MCP SDK の使用
- ツール、リソース、プロンプトの実装例
- エラーハンドリングとロギング
- テストスイート
- Claude Desktop 統合手順

**[python-mcp-server-generator.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/python-mcp-server-generator)** の特徴:
- `uv` パッケージマネージャー使用
- FastMCP サーバー実装
- デコレーター付きツール関数
- 型ヒント、docstring、async サポート
- PEP 8 準拠

**[typescript-mcp-server-generator.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/typescript-mcp-server-generator)** の特徴:
- `@modelcontextprotocol/sdk` + `zod` 依存関係
- ES モジュールサポートの `tsconfig.json`
- McpServer クラス + zod バリデーションスキーマ
- MCP Inspector テスト手順

---

### テスト生成

#### JavaScript/TypeScript

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`javascript-typescript-jest.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/javascript-typescript-jest) | Jest テストガイド | Jest テスト規約 |

**[javascript-typescript-jest.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/javascript-typescript-jest)** の特徴:
- テストファイル命名規則（`.test.ts`/`.test.js`）
- 分離テクニック（`jest.mock()`, `jest.spyOn()`）
- async テストパターン
- React Testing Library との組み合わせ
- Jest マッチャーリファレンス

---

#### C# テスト

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`csharp-xunit.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-xunit) | xUnit テストガイド | xUnit テスト規約 |
| [`csharp-nunit.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-nunit) | NUnit テストガイド | NUnit テスト規約 |
| [`csharp-mstest.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-mstest) | MSTest テストガイド | MSTest テスト規約 |
| [`csharp-tunit.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-tunit) | TUnit テストガイド | TUnit テスト規約（.NET 8.0+） |

**[csharp-xunit.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-xunit)** の特徴:
- `[Fact]` と `[Theory]` 属性
- AAA（Arrange-Act-Assert）パターン
- データ駆動テスト（`[InlineData]`, `[MemberData]`, `[ClassData]`）

**[csharp-mstest.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-mstest)** の特徴:
- MSTest 3.x/4.x の最新機能
- `[DataRow]` と `DynamicData`
- `[Retry]`, `[Timeout]` などの高度な機能
- ワークアイテムトレーサビリティ

**[csharp-tunit.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/csharp-tunit)** の特徴:
- .NET 8.0+ 必須
- 非同期 Fluent アサーション（`await Assert.That(value).IsEqualTo(expected)`）
- デフォルトで並列実行
- `[Arguments]`, `[MethodData]`, `[ClassData]` によるデータ駆動

---

#### Java テスト

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`java-junit.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-junit) | JUnit 5 テストガイド | JUnit 5 テスト規約 |
| [`java-docs.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-docs) | Java ドキュメント生成 | Javadoc |

**[java-junit.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/java-junit)** の特徴:
- JUnit 5 ライフサイクル管理（`@BeforeEach`, `@AfterEach`）
- Arrange-Act-Assert パターン
- パラメータ化テスト（`@ParameterizedTest`, `@ValueSource`, `@CsvSource`, `@MethodSource`）
- タグ付け、ネスト、順序付けによるテスト組織化

---

#### Playwright（E2E テスト）

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`playwright-generate-test.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/playwright-generate-test) | Playwright テスト生成 | TypeScript Playwright テスト |
| [`playwright-explore-website.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/playwright-explore-website) | Web サイト探索 | UI 要素ドキュメント、テストケース提案 |
| [`playwright-automation-fill-in-form.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/playwright-automation-fill-in-form) | フォーム自動入力 | フォーム操作自動化 |

**[playwright-generate-test.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/playwright-generate-test)** の特徴:
- 「理解してからコード」の構造化手法
- `@playwright/test` 使用
- `tests/` ディレクトリに保存
- 反復的なテスト検証

**[playwright-explore-website.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/playwright-explore-website)** の特徴:
- 3-5 のコア機能/ユーザーフローを特定
- UI 要素ロケーターとインタラクションパターンの文書化
- テストケース提案

---

#### Python テスト

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`pytest-coverage.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/pytest-coverage) | pytest カバレッジ分析 | 100% カバレッジ達成まで反復 |

**[pytest-coverage.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/pytest-coverage)** の特徴:
- `cov_annotate` ディレクトリにカバレッジレポート生成
- 未カバー行（`!` マーク）の特定
- 反復的なテスト追加で 100% カバレッジ達成

---

### SQL・データベース

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`sql-optimization.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/sql-optimization) | SQL 最適化 | 最適化された SQL クエリ |
| [`sql-code-review.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/sql-code-review) | SQL コードレビュー | セキュリティ・パフォーマンスレビュー |
| [`postgresql-optimization.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-optimization) | PostgreSQL 最適化 | PostgreSQL 固有の最適化 |
| [`postgresql-code-review.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-code-review) | PostgreSQL コードレビュー | PostgreSQL 固有のレビュー |
| [`cosmosdb-datamodeling.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/cosmosdb-datamodeling) | Cosmos DB データモデリング | データモデル設計 |

**[sql-optimization.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/sql-optimization)** の特徴:
- MySQL, PostgreSQL, SQL Server, Oracle 対応
- クエリチューニング、インデックス戦略
- アンチパターン特定（相関サブクエリ → ウィンドウ関数）
- DB 固有の最適化戦略

**[sql-code-review.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/sql-code-review)** の特徴:
- 優先度レベルとリスク評価
- セキュリティ問題（SQL インジェクション、アクセス制御）
- Before/After コード例
- セキュリティ、パフォーマンス、保守性、スキーマ品質のスコア

**[postgresql-optimization.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/postgresql-optimization)** の特徴:
- PostgreSQL 固有機能（JSONB, 配列, ウィンドウ関数, 全文検索）
- インデックス戦略（GIN, 複合, 部分, 式インデックス）
- 拡張機能推奨（uuid-ossp, pgcrypto）

**[cosmosdb-datamodeling.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/cosmosdb-datamodeling)** の特徴:
- ペアプログラミング形式でインタラクティブに要件収集
- 集約指向設計原則
- パーティションキー戦略
- マルチエンティティドキュメントパターン（30-70% アクセス相関時）
- RU コスト計算

---

### コンテナ・Docker

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`multi-stage-dockerfile.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/multi-stage-dockerfile) | マルチステージ Dockerfile 生成 | 最適化された Dockerfile |
| [`containerize-aspnetcore.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnetcore) | ASP.NET Core コンテナ化 | Linux Docker 環境向け Dockerfile |
| [`containerize-aspnet-framework.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnet-framework) | ASP.NET Framework コンテナ化 | Windows Docker 環境向け Dockerfile |

**[multi-stage-dockerfile.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/multi-stage-dockerfile)** の特徴:
- 言語/フレームワークを問わず適用可能
- ビルダーステージとランタイムステージの分離
- レイヤー最適化とキャッシュ活用
- セキュリティベストプラクティス（non-root ユーザー）
- ヘルスチェック設定

**[containerize-aspnetcore.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnetcore)** の特徴:
- .NET バージョン検出と SDK/ランタイムイメージ選択
- Linux ディストリビューション選択（Alpine, Ubuntu, Chiseled, Azure Linux）
- `.dockerignore` 生成
- non-root ユーザー実行設定

**[containerize-aspnet-framework.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnet-framework)** の特徴:
- Windows Server Core ベースイメージ
- IIS 設定、GAC アセンブリ、COM コンポーネント対応
- LogMonitor 設定
- ServiceMonitor 統合

---

### GitHub・CI/CD

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`create-github-action-workflow-specification.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-github-action-workflow-specification) | GitHub Actions ワークフロー仕様 | `/spec/spec-process-cicd-*.md` |
| [`create-github-issue-feature-from-specification.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issue-feature-from-specification) | 仕様から GitHub Issue 作成 | 単一の GitHub Issue |
| [`create-github-issues-feature-from-implementation-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issues-feature-from-implementation-plan) | 実装計画から GitHub Issues 作成 | フェーズごとの Issue |
| [`create-github-issues-for-unmet-specification-requirements.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-github-issues-for-unmet-specification-requirements) | 未達成要件の Issue 作成 | 要件ギャップの Issue |
| [`conventional-commit.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/conventional-commit) | Conventional Commits 形式 | `type(scope): description` 形式のコミット |
| [`git-flow-branch-creator.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/git-flow-branch-creator) | Git Flow ブランチ作成 | feature/release/hotfix ブランチ |

**[create-github-action-workflow-specification.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/create-github-action-workflow-specification)** の特徴:
- AI 最適化された CI/CD 仕様書
- Mermaid 実行フロー図
- Jobs/Dependencies マトリクス
- 要件マトリクス（機能、セキュリティ、パフォーマンス）
- 入出力契約とシークレット管理

**[conventional-commit.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/conventional-commit)** の特徴:
- `git status` と `git diff` で変更を分析
- 標準フォーマット: `type(scope): description`
- タイプ: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
- Breaking Changes とIssue 参照のフッター

---

### Azure

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`az-cost-optimize.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/az-cost-optimize) | Azure コスト最適化 | 最適化推奨 + GitHub Issues |
| [`azure-resource-health-diagnose.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/azure-resource-health-diagnose) | Azure リソースヘルス診断 | 7 ステップの診断レポート |
| [`update-avm-modules-in-bicep.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/update-avm-modules-in-bicep) | AVM モジュール更新 | 更新された Bicep ファイル |

**[az-cost-optimize.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/az-cost-optimize)** の特徴:
- Azure IaC ファイル（Bicep, Terraform, ARM）を分析
- 個別の最適化ごとに GitHub Issue 作成
- マスター EPIC Issue（アーキテクチャ図、優先度順推奨）
- 優先度スコア: (Value Score × Monthly Savings) / (Risk Score × Implementation Days)

**[azure-resource-health-diagnose.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/azure-resource-health-diagnose)** の特徴:
- 7 ステップのワークフロー
- Log Analytics / Application Insights（KQL クエリ）
- 重大度分類（critical, high, medium, low）
- 根本原因分析（設定、リソース制約、ネットワーク、アプリケーション、依存関係、セキュリティ）
- Azure CLI コマンド付きの段階的修復手順

---

### コードレビュー・リファクタリング

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`review-and-refactor.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/review-and-refactor) | コードレビュー＆リファクタリング | リファクタリング済みコード |
| [`ai-prompt-engineering-safety-review.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/ai-prompt-engineering-safety-review) | プロンプトエンジニアリング安全レビュー | 安全性評価 |

**[review-and-refactor.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/review-and-refactor)** の特徴:
- `.github/instructions/*.md` のプロジェクトルールに従う
- `.github/copilot-instructions.md` も参照
- ファイル構造を維持（断片化なし）
- 既存テストをパス

---

### Spring Boot / Java

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`create-spring-boot-java-project.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-spring-boot-java-project) | Spring Boot（Java）プロジェクト作成 | Spring Boot プロジェクト |
| [`create-spring-boot-kotlin-project.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-spring-boot-kotlin-project) | Spring Boot（Kotlin）プロジェクト作成 | Spring Boot Kotlin プロジェクト |
| [`java-springboot.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-springboot) | Spring Boot ガイド | Spring Boot 規約 |
| [`kotlin-springboot.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/kotlin-springboot) | Kotlin Spring Boot ガイド | Kotlin Spring Boot 規約 |
| [`java-refactoring-extract-method.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-refactoring-extract-method) | Java メソッド抽出リファクタリング | リファクタリング済みコード |
| [`java-refactoring-remove-parameter.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-refactoring-remove-parameter) | Java パラメーター削除リファクタリング | リファクタリング済みコード |
| [`java-add-graalvm-native-image-support.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/java-add-graalvm-native-image-support) | GraalVM Native Image サポート追加 | Native Image 設定 |

---

### .NET

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`dotnet-upgrade.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-upgrade) | .NET アップグレード | アップグレードされたプロジェクト |
| [`dotnet-best-practices.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-best-practices) | .NET ベストプラクティス | 規約ガイド |
| [`dotnet-design-pattern-review.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dotnet-design-pattern-review) | .NET デザインパターンレビュー | パターン適用レビュー |
| [`csharp-docs.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-docs) | C# ドキュメント生成 | XML ドキュメント |
| [`csharp-async.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/csharp-async) | C# 非同期パターン | async/await ガイド |
| [`ef-core.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/ef-core) | Entity Framework Core | EF Core ガイド |
| [`aspnet-minimal-api-openapi.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/aspnet-minimal-api-openapi) | ASP.NET Minimal API + OpenAPI | Minimal API 設定 |

---

### Power Platform

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`power-bi-dax-optimization.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-dax-optimization) | Power BI DAX 最適化 | 最適化された DAX |
| [`power-bi-model-design-review.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-model-design-review) | Power BI モデルデザインレビュー | モデルレビュー |
| [`power-bi-performance-troubleshooting.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-performance-troubleshooting) | Power BI パフォーマンストラブルシューティング | パフォーマンス改善 |
| [`power-bi-report-design-consultation.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-bi-report-design-consultation) | Power BI レポートデザイン相談 | デザイン推奨 |
| [`power-apps-code-app-scaffold.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-apps-code-app-scaffold) | Power Apps Code App スキャフォールド | Code App 雛形 |
| [`power-platform-mcp-connector-suite.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/power-platform-mcp-connector-suite) | Power Platform MCP コネクタスイート | MCP コネクタ |

---

### M365 Copilot / Agents

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`declarative-agents.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/declarative-agents) | Declarative Agents 作成 | エージェント定義 |
| [`mcp-create-declarative-agent.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/mcp-create-declarative-agent) | MCP Declarative Agent 作成 | MCP エージェント |
| [`mcp-create-adaptive-cards.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/mcp-create-adaptive-cards) | MCP Adaptive Cards 作成 | Adaptive Cards |
| [`mcp-deploy-manage-agents.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/mcp-deploy-manage-agents) | MCP エージェントのデプロイ・管理 | デプロイ手順 |
| [`typespec-create-agent.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-agent) | TypeSpec でエージェント作成 | TypeSpec 定義 |
| [`typespec-create-api-plugin.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/typespec-create-api-plugin) | TypeSpec で API プラグイン作成 | API プラグイン |
| [`typespec-api-operations.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/typespec-api-operations) | TypeSpec API オペレーション | API 操作定義 |
| [`create-agentsmd.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-agentsmd) | agents.md ファイル作成 | エージェント定義ファイル |
| [`finalize-agent-prompt.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/finalize-agent-prompt) | エージェントプロンプト最終化 | 最終調整されたプロンプト |

---

### Dataverse / Python

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`dataverse-python-quickstart.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-quickstart) | Dataverse Python クイックスタート | 入門コード |
| [`dataverse-python-production-code.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-production-code) | Dataverse Python 本番コード | 本番向けコード |
| [`dataverse-python-advanced-patterns.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-advanced-patterns) | Dataverse Python 高度なパターン | 上級パターン |
| [`dataverse-python-usecase-builder.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/dataverse-python-usecase-builder) | Dataverse Python ユースケースビルダー | ユースケース実装 |

---

### ユーティリティ・その他

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`remember.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/remember) | 記憶プロンプト | セッション間の記憶 |
| [`remember-interactive-programming.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/remember-interactive-programming) | インタラクティブプログラミング記憶 | REPL セッション記憶 |
| [`memory-merger.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/memory-merger) | メモリマージャー | 複数記憶の統合 |
| [`repo-story-time.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/repo-story-time) | リポジトリストーリータイム | リポジトリの歴史説明 |
| [`shuffle-json-data.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/shuffle-json-data) | JSON データシャッフル | ランダム化された JSON |
| [`convert-plaintext-to-md.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/convert-plaintext-to-md) | プレーンテキスト → Markdown 変換 | Markdown ファイル |
| [`update-markdown-file-index.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/update-markdown-file-index) | Markdown ファイルインデックス更新 | 目次更新 |
| [`mkdocs-translations.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/mkdocs-translations) | MkDocs 翻訳 | 多言語ドキュメント |
| [`next-intl-add-language.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/next-intl-add-language) | next-intl 言語追加 | 新言語サポート |
| [`editorconfig.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/editorconfig) | .editorconfig 生成 | エディター設定 |
| [`boost-prompt.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/boost-prompt) | プロンプトブースト | プロンプト改善 |
| [`first-ask.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/first-ask) | 最初の質問 | 要件明確化の質問 |
| [`gen-specs-as-issues.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/gen-specs-as-issues) | 仕様を Issue として生成 | GitHub Issues |
| [`openapi-to-application-code.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/openapi-to-application-code) | OpenAPI → アプリケーションコード | コード生成 |
| [`devops-rollout-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/devops-rollout-plan) | DevOps ロールアウト計画 | デプロイ計画 |

---

### Copilot カスタマイズ

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`generate-custom-instructions-from-codebase.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/generate-custom-instructions-from-codebase) | コードベースからカスタム Instructions 生成 | Instructions ファイル |
| [`write-coding-standards-from-file.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/write-coding-standards-from-file) | ファイルからコーディング規約生成 | コーディング規約 |
| [`add-educational-comments.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/add-educational-comments) | 教育的コメント追加 | コメント付きコード |
| [`comment-code-generate-a-tutorial.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/comment-code-generate-a-tutorial) | コードコメント → チュートリアル生成 | チュートリアル |
| [`suggest-awesome-github-copilot-agents.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-agents) | おすすめ Agents 提案 | エージェント推奨 |
| [`suggest-awesome-github-copilot-instructions.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-instructions) | おすすめ Instructions 提案 | Instructions 推奨 |
| [`github-copilot-starter.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/github-copilot-starter) | GitHub Copilot スターター | 入門ガイド |

**[generate-custom-instructions-from-codebase.prompt.md](https://github.com/github/awesome-copilot/tree/main/skills/generate-custom-instructions-from-codebase)** の特徴:
- 既存コードベースを分析
- プロジェクト固有のパターンを抽出
- チーム向けカスタム Instructions を自動生成

---

### Structured Autonomy

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`structured-autonomy-generate.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-generate) | 構造化自律生成 | 生成されたコード |
| [`structured-autonomy-implement.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-implement) | 構造化自律実装 | 実装されたコード |
| [`structured-autonomy-plan.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/structured-autonomy-plan) | 構造化自律計画 | 計画ドキュメント |

---

### Linux トリアージ

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`arch-linux-triage.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/arch-linux-triage) | Arch Linux トリアージ | 問題診断 |
| [`centos-linux-triage.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/centos-linux-triage) | CentOS トリアージ | 問題診断 |
| [`debian-linux-triage.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/debian-linux-triage) | Debian トリアージ | 問題診断 |
| [`fedora-linux-triage.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/fedora-linux-triage) | Fedora トリアージ | 問題診断 |

---

### LLM 設定

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`create-llms.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/create-llms) | LLM 設定作成 | LLM 設定ファイル |
| [`update-llms.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/update-llms) | LLM 設定更新 | 更新された設定 |

---

### コンポーネントドキュメント

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`update-specification.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/update-specification) | 仕様更新 | 更新された仕様 |

---

### アプリレビュー

| ファイル名 | 用途 | 出力 |
|-----------|------|------|
| [`apple-appstore-reviewer.prompt.md`](https://github.com/github/awesome-copilot/tree/main/skills/apple-appstore-reviewer) | Apple App Store レビュー対応 | レビュー準備チェックリスト |

---

## まとめ

Prompts は **138 ファイル** あり、以下のカテゴリに分類されます：

| カテゴリ | ファイル数 | 主な用途 |
|---------|----------|---------|
| ドキュメント生成 | 約 15 | README, 仕様書, ADR |
| 計画・設計 | 約 15 | 実装計画, PRD, アーキテクチャ |
| MCP サーバー生成 | 約 12 | 各言語の MCP サーバー |
| テスト生成 | 約 15 | Jest, xUnit, NUnit, Playwright |
| SQL・データベース | 約 5 | SQL 最適化, PostgreSQL |
| コンテナ・Docker | 約 5 | Dockerfile 生成 |
| GitHub・CI/CD | 約 10 | Actions, Issues, PR |
| Azure | 約 5 | コスト最適化, 診断 |
| Spring Boot / Java | 約 10 | プロジェクト作成, リファクタリング |
| .NET | 約 10 | アップグレード, ベストプラクティス |
| Power Platform | 約 8 | Power BI, Power Apps |
| M365 Copilot | 約 10 | Declarative Agents |
| ユーティリティ | 約 20 | 変換, 記憶, 設定 |

プロジェクトの定型タスクに合わせて、必要な Prompts を `.github/prompts/` ディレクトリにコピーして活用してください。
