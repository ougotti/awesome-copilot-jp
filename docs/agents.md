# Agents 一覧と活用ガイド

> [github/awesome-copilot](https://github.com/github/awesome-copilot) で公開されている **192 個の Agents** を日本語で解説します。

## Agents とは

Agents は、Copilot を特定ドメインの**専門家ペルソナ**として振る舞わせる定義ファイルです。MCP（Model Context Protocol）サーバーと連携させることで、外部ツールやサービスと直接やり取りする能力を持たせることもできます。

Instructions が「コードを書くときのルール」なら、Agents は「誰に相談するか」を選ぶ仕組みです。

### 設定方法

```
.github/
  agents/
    code-reviewer.agent.md
    azure-architect.agent.md
```

Copilot Chat のエージェント選択で、ビルトインエージェントと並んで選択できるようになります。

---

## カテゴリ別 Agents 一覧

### コード品質・開発プロセス

#### レビュー・品質管理

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`se-security-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-security-reviewer.agent.md) | セキュリティレビュー専門家（OWASP Top 10、Zero Trust） | セキュリティ監査、脆弱性チェック |
| [`se-system-architecture-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-system-architecture-reviewer.agent.md) | システムアーキテクチャレビュー専門家 | アーキテクチャ検証、WAF 適用 |
| [`se-technical-writer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-technical-writer.agent.md) | テクニカルライター | ドキュメント作成、ブログ、チュートリアル |
| [`se-ux-ui-designer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-ux-ui-designer.agent.md) | UX リサーチ専門家（JTBD 分析） | ユーザージャーニーマップ、デザインリサーチ |
| [`se-responsible-ai-code.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-responsible-ai-code.agent.md) | 責任ある AI 専門家 | バイアス防止、アクセシビリティ、倫理的 AI |
| [`se-product-manager-advisor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-product-manager-advisor.agent.md) | プロダクトマネージャーアドバイザー | 要件定義、GitHub Issue 作成 |
| [`gilfoyle.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gilfoyle.agent.md) | 辛辣なコードレビュアー（Silicon Valley 風） | 厳格なコードレビュー |
| `gilfoyle-code-review.instructions.md` | Gilfoyle スタイルレビュー（Instructions 版） | 厳格なレビュールール |
| [`critical-thinking.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/critical-thinking.agent.md) | 批判的思考エージェント | 仮定の検証、論理的分析 |
| [`devils-advocate.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/devils-advocate.agent.md) | 悪魔の代弁者 | 反対意見の検討、リスク分析 |
| [`wg-code-alchemist.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/wg-code-alchemist.agent.md) | コード錬金術師 | コード変換、リファクタリング |
| [`wg-code-sentinel.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/wg-code-sentinel.agent.md) | コード番人 | コード品質監視 |
| [`agent-governance-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/agent-governance-reviewer.agent.md) | AI エージェントガバナンスレビュアー | エージェントシステムの安全性・ポリシー審査 |
| [`doublecheck.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/doublecheck.agent.md) | AI 生成物検証エージェント | ファクトチェック・ソース検証 |
| [`gem-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md) | GEM レビュアー（セキュリティゲートキーパー） | OWASP・シークレット検出・PRD 準拠検証 |
| [`gem-critic.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-critic.agent.md) | GEM クリティック（仮定・設計・アプローチへの批判的挑戦） | 仮定の検証・エッジケース発見・過剰設計の指摘 |
| [`gem-designer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-designer.agent.md) | GEM デザイナー（UI/UX スペシャリスト） | レイアウト・テーマ・カラースキーム・デザインシステム・アクセシビリティ検証 |

**[se-security-reviewer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/se-security-reviewer.agent.md) の特徴:
- OWASP Top 10 脆弱性検出
- AI/LLM システムのセキュリティレビュー（プロンプトインジェクション対策含む）
- Zero Trust 原則に基づく認証・認可検証
- `docs/code-review/` に Markdown レポート生成
- **MCP ツール:** `codebase`, `edit/editFiles`, `search`, `problems`

---

#### 計画・設計

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`plan.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/plan.agent.md) | 戦略的計画・アーキテクチャアシスタント | コードベース分析、実装戦略策定 |
| [`planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/planner.agent.md) | 実装計画作成エージェント（コード変更なし） | Markdown 形式の計画書作成 |
| [`prd.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/prd.agent.md) | シニアプロダクトマネージャー | PRD（プロダクト要件定義書）作成 |
| [`specification.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/specification.agent.md) | 仕様書作成エージェント | AI 向け仕様書生成 |
| [`implementation-plan.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/implementation-plan.agent.md) | 実装計画エージェント（AI-to-AI） | 機械可読な実装計画 |
| [`task-planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/task-planner.agent.md) | タスクプランナー | タスク分解、優先順位付け |
| [`task-researcher.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/task-researcher.agent.md) | タスクリサーチャー | 技術調査、情報収集 |
| [`research-technical-spike.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/research-technical-spike.agent.md) | 技術スパイク検証エージェント | 技術検証、POC 調査 |
| [`tech-debt-remediation-plan.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/tech-debt-remediation-plan.agent.md) | 技術的負債解消計画 | 負債の可視化と解消計画 |
| [`blueprint-mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/blueprint-mode.agent.md) | ブループリントモード | 設計図作成 |
| [`blueprint-mode-codex.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/blueprint-mode-codex.agent.md) | ブループリントモード（Codex 版） | 設計図 + コード生成 |
| [`context-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/context-architect.agent.md) | コンテキストアーキテクト | マルチファイル変更計画・依存関係マッピング |
| [`one-shot-feature-issue-planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/one-shot-feature-issue-planner.agent.md) | ワンショット機能計画エージェント | 機能要件を即座に GitHub Issue 化 |
| [`rug-orchestrator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/rug-orchestrator.agent.md) | RUG オーケストレーター（Repeat Until Good） | サブエージェント委任・繰り返し検証 |
| [`gem-orchestrator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-orchestrator.agent.md) | GEM オーケストレーター（チームリード） | マルチエージェントワークフロー指揮 |
| [`gem-planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-planner.agent.md) | GEM プランナー（DAG 設計） | タスク分解・計画 YAML 生成 |
| [`gem-researcher.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-researcher.agent.md) | GEM リサーチャー | コードベース調査・パターン発見 |
| [`gem-implementer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-implementer.agent.md) | GEM 実装エージェント（TDD） | テスト駆動でコード実装 |
| [`gem-designer-mobile.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-designer-mobile.agent.md) | GEM モバイルデザイナー（HIG/Material Design 3 専門） | モバイル UI/UX 設計・プラットフォーム規約準拠 |
| [`gem-implementer-mobile.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-implementer-mobile.agent.md) | GEM モバイル実装エージェント（TDD） | React Native/Expo/Flutter コード実装 |
| [`project-architecture-planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/project-architecture-planner.agent.md) | プロジェクトアーキテクチャプランナー | テックスタック評価・スケーラビリティロードマップ設計・クラウド非依存コスト分析・Mermaid 図生成 |

**[plan.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/plan.agent.md) の特徴:
- 「Think First, Code Later」アプローチ
- コードベース探索とパターン発見
- 複雑な要件を管理可能な単位に分解
- 複数の実装オプションとトレードオフ評価
- **MCP ツール:** `search/codebase`, `vscode/extensions`, `web/fetch`, `web/githubRepo`, `read/problems` 等

**[implementation-plan.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/implementation-plan.agent.md) の特徴:
- AI-to-AI コミュニケーション向けの曖昧さゼロの計画
- `/plan/` ディレクトリに標準命名で保存
- ステータスバッジ（Completed, In progress, Planned 等）
- 標準 ID プレフィックス（REQ-, TASK-, GOAL-）
- **MCP ツール:** 43 種類のツールを使用

---

#### メンタリング・教育

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`mentor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/mentor.agent.md) | メンター（ソクラテス式指導） | 新人指導、学習支援 |
| [`code-tour.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/code-tour.agent.md) | CodeTour 作成専門家 | コードベースウォークスルー作成 |
| [`demonstrate-understanding.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/demonstrate-understanding.agent.md) | 理解度確認エージェント | 学習確認、概念説明 |
| [`microsoft-study-mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/microsoft-study-mode.agent.md) | Microsoft Study モード | Microsoft 技術学習 |
| [`microsoft_learn_contributor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/microsoft_learn_contributor.agent.md) | Microsoft Learn コントリビューター | 学習コンテンツ作成 |
| [`mentoring-juniors.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/mentoring-juniors.agent.md) | ジュニア開発者メンター「先生」（ソクラテス式） | 新人指導・PEAR ループ学習支援 |
| [`gem-documentation-writer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-documentation-writer.agent.md) | GEM ドキュメントライター | 技術ドキュメント作成・コード-ドキュメント整合性維持 |

**[mentor.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/mentor.agent.md) の特徴:
- ソクラテス式メソッドと「5 Whys」技法
- 直接解答せず、問題解決の思考をガイド
- 安全でない実践や短期的解決の長期コストを指摘
- 表、図、GIF を使った視覚的説明
- **MCP ツール:** `codebase`, `web/fetch`, `findTestFiles`, `githubRepo`, `search`, `usages`

---

#### デバッグ・保守

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`debug.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/debug.agent.md) | システマティックデバッグ専門家 | バグ調査、根本原因分析 |
| [`janitor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/janitor.agent.md) | ユニバーサルジャニター | コードクリーンアップ、技術的負債解消 |
| [`refine-issue.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/refine-issue.agent.md) | Issue 改善エージェント | GitHub Issue の詳細化 |
| [`address-comments.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/address-comments.agent.md) | コメント対応エージェント | PR コメントへの対応 |
| [`swe-subagent.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/swe-subagent.agent.md) | シニアソフトウェアエンジニア（SWE）サブエージェント | 機能開発・デバッグ・リファクタリング |
| [`gem-debugger.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-debugger.agent.md) | GEM デバッガー（根本原因分析・スタックトレース診断） | 根本原因調査・スタックトレース解析・リグレッション特定 |
| [`gem-code-simplifier.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-code-simplifier.agent.md) | GEM コードシンプリファイアー（デッドコード除去・複雑度削減） | リファクタリング・デッドコード削除・重複統合・命名改善 |
| [`devtools-regression-investigator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/devtools-regression-investigator.agent.md) | DevTools リグレッション調査エージェント | ブラウザリグレッションの再現・証拠収集・根本原因特定 |
| [`frontend-performance-investigator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/frontend-performance-investigator.agent.md) | フロントエンドパフォーマンス調査エージェント | Core Web Vitals・Lighthouse リグレッション診断 |

**[debug.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/debug.agent.md) の特徴:
- 4 フェーズの構造化アプローチ（問題評価、調査、解決、品質保証）
- エラー分析とコードベース検査
- 変数状態、データフロー、制御ロジックの追跡
- **MCP ツール:** `edit/editFiles`, `search`, `execute/runInTerminal`, `read/problems`, `execute/runTests` 等 12 種類

**[janitor.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/janitor.agent.md) の特徴:
- 「Less Code = Less Debt」の原則
- 未使用の関数、変数、インポート、デッドコード削除
- 複雑なパターンの簡略化（インライン化、ネスト解消）
- 古いテスト、コメント、ボイラープレート削除
- **MCP ツール:** 30 種類以上

---

### 言語・フレームワーク専門家

#### .NET / C#

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`CSharpExpert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/CSharpExpert.agent.md) | C# エキスパート | C# 開発全般 |
| [`expert-dotnet-software-engineer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/expert-dotnet-software-engineer.agent.md) | .NET ソフトウェアエンジニア | .NET アーキテクチャ、SOLID |
| [`csharp-dotnet-janitor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/csharp-dotnet-janitor.agent.md) | C#/.NET ジャニター | .NET コードクリーンアップ |
| [`dotnet-upgrade.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/dotnet-upgrade.agent.md) | .NET アップグレード専門家 | フレームワーク移行 |
| [`dotnet-maui.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/dotnet-maui.agent.md) | .NET MAUI 専門家 | クロスプラットフォームアプリ |
| [`WinFormsExpert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/WinFormsExpert.agent.md) | WinForms エキスパート | Windows フォームアプリ |
| [`semantic-kernel-dotnet.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/semantic-kernel-dotnet.agent.md) | Semantic Kernel（.NET）専門家 | AI/ML .NET 開発 |
| [`microsoft-agent-framework-dotnet.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/microsoft-agent-framework-dotnet.agent.md) | Microsoft Agent Framework（.NET） | エージェント開発 |
| [`winui3-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/winui3-expert.agent.md) | WinUI 3 専門家 | Windows App SDK デスクトップアプリ開発 |
| [`dotnet-self-learning-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/dotnet-self-learning-architect.agent.md) | .NET 自己学習アーキテクト（並行/オーケストレーション型サブエージェント対応） | エンタープライズ .NET システム設計・実装 |

**[expert-dotnet-software-engineer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/expert-dotnet-software-engineer.agent.md) の特徴:
- Anders Hejlsberg、Robert C. Martin、Kent Beck の教えに基づく
- async/await パターンと依存性注入
- Repository、Unit of Work、CQRS、Event Sourcing パターン
- xUnit, NUnit, MSTest による TDD
- **MCP ツール:** `codebase`, `search`, `edit`, `runTests`, `microsoft.docs.mcp` 等 18 種類

---

#### JavaScript / TypeScript

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`expert-nextjs-developer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/expert-nextjs-developer.agent.md) | Next.js 16 エキスパート | Next.js フルスタック開発 |
| [`expert-react-frontend-engineer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/expert-react-frontend-engineer.agent.md) | React 19.2 フロントエンドエンジニア | React SPA 開発 |
| [`electron-angular-native.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/electron-angular-native.agent.md) | Electron + Angular ネイティブ | デスクトップアプリ |
| [`vuejs-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/vuejs-expert.agent.md) | Vue.js フロントエンドエンジニア | Vue 3 / Composition API 開発 |
| [`nuxt-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/nuxt-expert.agent.md) | Nuxt エキスパート | Nuxt 3 / Nitro / SSR 開発 |

**[expert-nextjs-developer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/expert-nextjs-developer.agent.md) の特徴:
- App Router、Server Components、Cache Components
- Turbopack（デフォルトバンドラー）
- v16 の破壊的変更（async params/searchParams）に対応
- `next/image`, `next/font`, React Compiler でパフォーマンス最適化
- **MCP ツール:** `codebase`, `edit/editFiles`, `runTests`, `figma-dev-mode-mcp-server` 等

**[expert-react-frontend-engineer.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/expert-react-frontend-engineer.agent.md) の特徴:
- React 19.2 の新機能: `<Activity>`, `useEffectEvent()`, `cacheSignal`
- モダン Hooks: `use()`, `useFormStatus`, `useOptimistic`, `useActionState`
- Server Components、Actions、クライアント/サーバー境界
- WCAG 2.1 AA アクセシビリティ準拠
- **MCP ツール:** 18 種類以上

---

#### その他の言語

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`laravel-expert-agent.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/laravel-expert-agent.agent.md) | Laravel 12+ エキスパート | PHP Laravel 開発 |
| [`shopify-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/shopify-expert.agent.md) | Shopify エキスパート | Shopify テーマ/アプリ開発 |
| [`salesforce-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/salesforce-expert.agent.md) | Salesforce テクニカルアーキテクト | Salesforce 開発 |
| [`drupal-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/drupal-expert.agent.md) | Drupal エキスパート | Drupal CMS 開発 |
| [`pimcore-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/pimcore-expert.agent.md) | Pimcore エキスパート | Pimcore PIM/CMS |
| [`expert-cpp-software-engineer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/expert-cpp-software-engineer.agent.md) | C++ ソフトウェアエンジニア | C++ 開発 |
| [`clojure-interactive-programming.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/clojure-interactive-programming.agent.md) | Clojure インタラクティブプログラミング | Clojure REPL 開発 |

---

#### Salesforce

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`salesforce-apex-triggers.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/salesforce-apex-triggers.agent.md) | Salesforce Apex & トリガー開発 | Apex ビジネスロジック・トリガー実装 |
| [`salesforce-aura-lwc.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/salesforce-aura-lwc.agent.md) | Salesforce UI 開発（Aura & LWC） | LWC / Aura コンポーネント開発 |
| [`salesforce-flow.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/salesforce-flow.agent.md) | Salesforce Flow 開発 | 宣言型ビジネス自動化 |
| [`salesforce-visualforce.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/salesforce-visualforce.agent.md) | Salesforce Visualforce 開発 | Visualforce ページ・コントローラー実装 |

---

### MCP サーバー開発専門家

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`python-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/python-mcp-expert.agent.md) | Python MCP エキスパート | Python MCP サーバー構築 |
| [`typescript-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/typescript-mcp-expert.agent.md) | TypeScript MCP エキスパート | TypeScript MCP サーバー構築 |
| [`csharp-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/csharp-mcp-expert.agent.md) | C# MCP エキスパート | C# MCP サーバー構築 |
| [`go-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/go-mcp-expert.agent.md) | Go MCP エキスパート | Go MCP サーバー構築 |
| [`java-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/java-mcp-expert.agent.md) | Java MCP エキスパート | Java MCP サーバー構築 |
| [`rust-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/rust-mcp-expert.agent.md) | Rust MCP エキスパート | Rust MCP サーバー構築 |
| [`kotlin-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/kotlin-mcp-expert.agent.md) | Kotlin MCP エキスパート | Kotlin MCP サーバー構築 |
| [`ruby-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/ruby-mcp-expert.agent.md) | Ruby MCP エキスパート | Ruby MCP サーバー構築 |
| [`php-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/php-mcp-expert.agent.md) | PHP MCP エキスパート | PHP MCP サーバー構築 |
| [`swift-mcp-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/swift-mcp-expert.agent.md) | Swift MCP エキスパート | Swift MCP サーバー構築 |

**MCP エキスパートの共通特徴:**
- 各言語の公式 MCP SDK に精通
- プロジェクト構造の完全なスキャフォールディング
- ツール、リソース、プロンプトの実装ガイダンス
- トランスポート設定（stdio, HTTP/SSE）
- Claude Desktop 統合とテスト方法

---

### インフラ・DevOps

#### CI/CD・DevOps

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`devops-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/devops-expert.agent.md) | DevOps エキスパート | DevOps ライフサイクル全般 |
| [`github-actions-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/github-actions-expert.agent.md) | GitHub Actions エキスパート | GitHub Actions CI/CD |
| [`se-gitops-ci-specialist.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/se-gitops-ci-specialist.agent.md) | GitOps CI スペシャリスト | GitOps ワークフロー |
| [`gem-devops.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-devops.agent.md) | GEM DevOps エージェント | コンテナ・CI/CD・インフラデプロイ |
| [`github-actions-node-upgrade.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/github-actions-node-upgrade.agent.md) | GitHub Actions Node ランタイムアップグレード | Actions の Node.js バージョン更新・メジャーバンプ |

**[devops-expert.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/devops-expert.agent.md) の特徴:
- DevOps ライフサイクル 8 フェーズ（plan, code, build, test, release, deploy, operate, monitor）
- CI/CD パイプライン、IaC、テストフレームワーク自動化
- DORA メトリクス（deployment frequency, lead time, MTTR, failure rate）
- 文化的ガイダンス（サイロ解消、ブレームレス・ポストモーテム）
- **MCP ツール:** `codebase`, `edit/editFiles`, `terminalCommand`, `githubRepo`, `runCommands`, `runTasks`

**[github-actions-expert.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/github-actions-expert.agent.md) の特徴:
- 最小権限と OIDC 認証によるセキュリティ強化
- CodeQL SAST、依存関係レビュー、Trivy コンテナスキャン、SBOM 生成
- キャッシュ戦略と並行制御による最適化
- 15 項目のセキュリティチェックリスト

---

#### Kubernetes・SRE

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`platform-sre-kubernetes.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/platform-sre-kubernetes.agent.md) | Kubernetes SRE | K8s 運用・信頼性 |
| [`arch.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/arch.agent.md) | Arch Linux エキスパート | Arch Linux 環境 |
| [`arch-linux-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/arch-linux-expert.agent.md) | Arch Linux エキスパート（詳細版） | Arch Linux 管理 |
| [`centos-linux-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/centos-linux-expert.agent.md) | CentOS エキスパート | CentOS 環境 |
| [`debian-linux-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/debian-linux-expert.agent.md) | Debian エキスパート | Debian 環境 |
| [`fedora-linux-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/fedora-linux-expert.agent.md) | Fedora エキスパート | Fedora 環境 |

**[platform-sre-kubernetes.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/platform-sre-kubernetes.agent.md) の特徴:
- 5 フェーズのデプロイ方法論（計画、マニフェスト生成、検証、監視付きロールアウト、テスト済みロールバック）
- 必須セキュリティ設定（runAsNonRoot, readOnlyRootFilesystem）
- 高可用性パターン（マルチレプリカ、Pod Disruption Budgets、ゾーン分散）
- kubectl dry-run、kubeconform によるデプロイ前検証

---

#### Terraform・IaC

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`terraform.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/terraform.agent.md) | Terraform インフラ専門家 | Terraform IaC 全般 |
| [`terraform-iac-reviewer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/terraform-iac-reviewer.agent.md) | Terraform IaC レビュアー | IaC コードレビュー |
| [`terraform-azure-planning.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/terraform-azure-planning.agent.md) | Terraform Azure 計画 | Azure インフラ計画 |
| [`terraform-azure-implement.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/terraform-azure-implement.agent.md) | Terraform Azure 実装 | Azure インフラ実装 |
| [`terratest-module-testing.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/terratest-module-testing.agent.md) | Terratest モジュールテスト | Terraform モジュールの Go テスト自動化 |

**[terraform.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/terraform.agent.md) の特徴:
- パブリック/プライベート Terraform レジストリ連携
- 厳格なファイル構造（main.tf, variables.tf, outputs.tf, README.md）
- HCP Terraform ワークスペース管理と plan/apply オーケストレーション
- ハードコードシークレット禁止、最小権限 IAM
- **MCP ツール:** Terraform MCP サーバー（プロバイダー/モジュール検出、ワークスペース操作、実行管理）

---

### クラウド・Azure

#### Azure アーキテクチャ

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`azure-principal-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-principal-architect.agent.md) | Azure プリンシパルアーキテクト | Azure アーキテクチャ設計 |
| [`azure-saas-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-saas-architect.agent.md) | Azure SaaS アーキテクト | マルチテナント SaaS 設計 |
| [`azure-iac-generator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-iac-generator.agent.md) | Azure IaC ジェネレーター | Bicep/Terraform/Pulumi 生成 |
| [`azure-iac-exporter.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-iac-exporter.agent.md) | Azure IaC エクスポーター | 既存リソースの IaC 化 |
| [`azure-logic-apps-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-logic-apps-expert.agent.md) | Azure Logic Apps エキスパート | ワークフロー開発 |
| [`azure-verified-modules-bicep.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-verified-modules-bicep.agent.md) | Azure Verified Modules（Bicep） | 検証済みモジュール活用 |
| [`azure-verified-modules-terraform.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-verified-modules-terraform.agent.md) | Azure Verified Modules（Terraform） | 検証済みモジュール活用 |
| [`azure-policy-analyzer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/azure-policy-analyzer.agent.md) | Azure ポリシーコンプライアンスアナライザー（NIST/MCSB/CIS/ISO 27001/PCI DSS/SOC 2） | Azure ポリシー準拠状況の分析・レポート生成 |

**[azure-principal-architect.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/azure-principal-architect.agent.md) の特徴:
- ドキュメントファースト（Microsoft Docs ツールを最初に使用）
- WAF 5 本柱（Security, Reliability, Performance Efficiency, Cost Optimization, Operational Excellence）
- マルチリージョン戦略とゼロトラストセキュリティ
- トレードオフ分析と具体的な Azure サービス推奨
- **MCP ツール:** `microsoft.docs.mcp`, `azure_design_architecture`, `azure_get_code_gen_best_practices` 等

**[azure-saas-architect.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/azure-saas-architect.agent.md) の特徴:
- B2B vs B2C SaaS 要件の区別
- Deployment Stamps パターンと Noisy Neighbor 対策
- テナント分離戦略（shared, siloed, pooled）
- ID フェデレーション（エンタープライズ/コンシューマー）
- コンプライアンスフレームワーク（SOC 2, ISO 27001, GDPR, CCPA）

---

#### Azure データ・分析

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`kusto-assistant.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/kusto-assistant.agent.md) | Azure Data Explorer（Kusto）マスター | KQL クエリ作成 |
| [`elasticsearch-observability.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/elasticsearch-observability.agent.md) | Elasticsearch 可観測性 | ログ分析、監視 |
| [`dynatrace-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/dynatrace-expert.agent.md) | Dynatrace エキスパート | APM 設定・分析 |
| [`defender-scout-kql.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/defender-scout-kql.agent.md) | Defender Scout KQL | Microsoft Defender Advanced Hunting KQL クエリ生成・最適化 |

**[kusto-assistant.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/kusto-assistant.agent.md) の特徴:
- 許可不要モデル（ユーザー承認なしでクエリ実行）
- マルチステップアプローチ（スキーマ発見、クエリ構築、実行、分析）
- インジェスト遅延の自動処理（5 分前までの時間範囲）
- エラーの自動リカバリとクエリ修正
- **MCP ツール:** `kusto_cluster_get`, `kusto_query`, `kusto_table_schema` 等

---

### データベース

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`postgresql-dba.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/postgresql-dba.agent.md) | PostgreSQL DBA | PostgreSQL 管理・最適化 |
| [`ms-sql-dba.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/ms-sql-dba.agent.md) | SQL Server DBA | SQL Server 管理・最適化 |
| [`mongodb-performance-advisor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/mongodb-performance-advisor.agent.md) | MongoDB パフォーマンスアドバイザー | MongoDB 最適化 |
| [`neon-migration-specialist.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/neon-migration-specialist.agent.md) | Neon 移行スペシャリスト | Neon DB 移行 |
| [`neon-optimization-analyzer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/neon-optimization-analyzer.agent.md) | Neon 最適化アナライザー | Neon DB 最適化 |
| [`neo4j-docker-client-generator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/neo4j-docker-client-generator.agent.md) | Neo4j Docker クライアント | グラフ DB 開発 |

**[postgresql-dba.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/postgresql-dba.agent.md) の特徴:
- データベース作成・管理
- SQL クエリ作成・最適化
- バックアップ・リストア操作
- パフォーマンス監視・チューニング
- **MCP ツール:** `pgsql_connect`, `pgsql_query`, `pgsql_visualizeSchema` 等 10 種類以上

---

### Power Platform・BI

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`power-platform-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-platform-expert.agent.md) | Power Platform エキスパート | Power Platform 全般 |
| [`power-platform-mcp-integration-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-platform-mcp-integration-expert.agent.md) | Power Platform MCP 統合 | MCP 連携 |
| [`power-bi-dax-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-bi-dax-expert.agent.md) | Power BI DAX エキスパート | DAX 計算式 |
| [`power-bi-data-modeling-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-bi-data-modeling-expert.agent.md) | Power BI データモデリング | データモデル設計 |
| [`power-bi-performance-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-bi-performance-expert.agent.md) | Power BI パフォーマンス | パフォーマンス最適化 |
| [`power-bi-visualization-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/power-bi-visualization-expert.agent.md) | Power BI ビジュアライゼーション | ビジュアル設計 |

**[power-bi-dax-expert.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/power-bi-dax-expert.agent.md) の特徴:
- 変数を使用したパフォーマンスと可読性の向上
- 完全修飾カラム参照（`Table[Column]`）
- パフォーマンス最適化（COUNTROWS vs COUNT、SELECTEDVALUE vs VALUES）
- DIVIDE 関数（除算演算子の代わり）
- **MCP ツール:** `microsoft.docs.mcp`

---

### Microsoft 365・Copilot

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`declarative-agents-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/declarative-agents-architect.agent.md) | M365 Declarative Agents アーキテクト | M365 Copilot エージェント開発 |
| [`mcp-m365-agent-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/mcp-m365-agent-expert.agent.md) | M365 エージェント MCP エキスパート | M365 MCP 連携 |

**[declarative-agents-architect.agent.md](https://github.com/github/awesome-copilot/blob/main/agents/declarative-agents-architect.agent.md) の特徴:
- JSON スキーマ v1.5 準拠（文字数制限、バリデーション要件）
- TypeSpec による型安全なエージェント定義
- VS Code 拡張による M365 Agents Toolkit 統合
- 11 種類のエージェント機能（WebSearch, GraphConnectors, PowerPlatform, CustomConnectors 等）

---

### AI・機械学習

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`semantic-kernel-python.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/semantic-kernel-python.agent.md) | Semantic Kernel（Python）専門家 | Python AI/ML 開発 |
| [`microsoft-agent-framework-python.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/microsoft-agent-framework-python.agent.md) | Microsoft Agent Framework（Python） | Python エージェント開発 |
| [`comet-opik.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/comet-opik.agent.md) | Comet Opik | ML 実験管理 |
| [`python-notebook-sample-builder.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/python-notebook-sample-builder.agent.md) | Python Notebook サンプルビルダー | Azure・AI 機能の Jupyter Notebook 作成 |
| [`spark-performance.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/spark-performance.agent.md) | PySpark パフォーマンスエキスパート | PySpark ボトルネック診断・分散実行アンチパターン修正 |

---

### テスト

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`playwright-tester.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/playwright-tester.agent.md) | Playwright テスター | E2E テスト自動化 |
| [`tdd-red.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/tdd-red.agent.md) | TDD Red フェーズ | 失敗テスト作成 |
| [`tdd-green.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/tdd-green.agent.md) | TDD Green フェーズ | テスト合格コード実装 |
| [`tdd-refactor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/tdd-refactor.agent.md) | TDD Refactor フェーズ | テスト維持リファクタリング |
| [`diffblue-cover.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/diffblue-cover.agent.md) | Diffblue Cover | Java テスト自動生成 |
| [`gem-browser-tester.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-browser-tester.agent.md) | GEM ブラウザテスター | E2E ブラウザテスト（Playwright/Chrome DevTools） |
| [`polyglot-test-generator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-generator.agent.md) | ポリグロットテスト生成オーケストレーター | 多言語テスト生成（RPI パイプライン） |
| [`polyglot-test-researcher.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-researcher.agent.md) | ポリグロットテストリサーチャー | コードベース構造・テストフレームワーク調査 |
| [`polyglot-test-planner.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-planner.agent.md) | ポリグロットテストプランナー | テスト実装計画策定（フェーズ分割） |
| [`polyglot-test-implementer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-implementer.agent.md) | ポリグロットテスト実装エージェント | テストファイル作成・ビルド・実行検証 |
| [`polyglot-test-builder.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-builder.agent.md) | ポリグロットテストビルダー | ビルド・コンパイル実行・エラー報告 |
| [`polyglot-test-tester.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-tester.agent.md) | ポリグロットテストランナー | テスト実行・合否レポート |
| [`polyglot-test-fixer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-fixer.agent.md) | ポリグロットテストフィクサー | コンパイルエラー修正 |
| [`polyglot-test-linter.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/polyglot-test-linter.agent.md) | ポリグロットテストリンター | コードフォーマット・スタイル修正 |
| [`qa-subagent.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/qa-subagent.agent.md) | QA サブエージェント | テスト計画・バグハント・品質検証 |
| [`accessibility-runtime-tester.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/accessibility-runtime-tester.agent.md) | アクセシビリティランタイムテスター | キーボードフロー・フォーカス管理・WCAG ランタイム検証 |
| [`gem-mobile-tester.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gem-mobile-tester.agent.md) | GEM モバイルテスター（E2E） | iOS/Android シミュレーターでの E2E テスト実行 |

---

### 移行・モダナイゼーション

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`modernization.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/modernization.agent.md) | モダナイゼーション専門家 | レガシーシステム刷新 |
| [`arm-migration.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/arm-migration.agent.md) | ARM 移行専門家 | ARM テンプレート移行 |
| [`oracle-to-postgres-migration-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/oracle-to-postgres-migration-expert.agent.md) | Oracle → PostgreSQL 移行エキスパート | Oracle から PostgreSQL へのアプリ移行 |
| [`react18-commander.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-commander.agent.md) | React 18 移行オーケストレーター | React 16/17 → 18.3.1 移行パイプライン統括 |
| [`react18-auditor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-auditor.agent.md) | React 18 監査エージェント | React 18 非互換パターンのコードベース全量スキャン |
| [`react18-dep-surgeon.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-dep-surgeon.agent.md) | React 18 依存関係外科医 | React 18.3.1 へのパッケージ正確ピン留めとアップグレード |
| [`react18-class-surgeon.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-class-surgeon.agent.md) | React 18 クラスコンポーネント外科医 | 旧ライフサイクル・Legacy Context・String Ref の移行 |
| [`react18-batching-fixer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-batching-fixer.agent.md) | React 18 自動バッチング修正エージェント | 自動バッチングによるステート回帰の特定と `flushSync` 適用 |
| [`react18-test-guardian.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react18-test-guardian.agent.md) | React 18 テストガーディアン | React 18 移行後のテストスイート修正・ゼロ失敗維持 |
| [`react19-commander.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react19-commander.agent.md) | React 19 移行オーケストレーター | React 18 → 19 移行パイプライン統括 |
| [`react19-auditor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react19-auditor.agent.md) | React 19 監査エージェント | React 19 破壊的変更パターンのコードベース全量スキャン |
| [`react19-dep-surgeon.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react19-dep-surgeon.agent.md) | React 19 依存関係外科医 | React 19 対応依存関係のアップグレードと競合解消 |
| [`react19-migrator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react19-migrator.agent.md) | React 19 マイグレーター | 非推奨 React API の React 19 準拠への一括書き換え |
| [`react19-test-guardian.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/react19-test-guardian.agent.md) | React 19 テストガーディアン | React 19 移行後のテストスイート修正・ゼロ失敗維持 |

---

### 外部サービス連携

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`octopus-deploy-release-notes-mcp.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/octopus-deploy-release-notes-mcp.agent.md) | Octopus Deploy リリースノート | デプロイ自動化 |
| [`launchdarkly-flag-cleanup.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/launchdarkly-flag-cleanup.agent.md) | LaunchDarkly フラグクリーンアップ | フィーチャーフラグ管理 |
| [`pagerduty-incident-responder.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/pagerduty-incident-responder.agent.md) | PagerDuty インシデント対応 | 障害対応 |
| [`jfrog-sec.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/jfrog-sec.agent.md) | JFrog セキュリティ | 依存関係セキュリティ |
| [`stackhawk-security-onboarding.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/stackhawk-security-onboarding.agent.md) | StackHawk セキュリティオンボーディング | セキュリティテスト |
| [`apify-integration-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/apify-integration-expert.agent.md) | Apify 統合エキスパート | Web スクレイピング |
| [`amplitude-experiment-implementation.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/amplitude-experiment-implementation.agent.md) | Amplitude 実験実装 | A/B テスト |
| [`monday-bug-fixer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/monday-bug-fixer.agent.md) | Monday.com バグ修正 | タスク管理連携 |
| [`lingodotdev-i18n.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/lingodotdev-i18n.agent.md) | Lingo.dev i18n | 国際化 |
| [`atlassian-requirements-to-jira.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/atlassian-requirements-to-jira.agent.md) | Atlassian 要件 → Jira | Jira 連携 |
| [`context7.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/context7.agent.md) | Context7 | コンテキスト管理 |
| [`reepl-linkedin.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/reepl-linkedin.agent.md) | Reepl LinkedIn コンテンツエージェント | LinkedIn 投稿作成・スケジュール管理 |
| [`linkedin-post-writer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/linkedin-post-writer.agent.md) | LinkedIn 投稿ライター | Unicode 書式付き LinkedIn 投稿の下書き・フォーマット |
| [`scientific-paper-research.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/scientific-paper-research.agent.md) | 科学論文リサーチエージェント | BGPT MCP を使った科学文献検索・分析 |

---

### 高度なモード

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`4.1-Beast.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/4.1-Beast.agent.md) | Beast モード（GPT-4.1 風） | 高性能推論 |
| [`Thinking-Beast-Mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/Thinking-Beast-Mode.agent.md) | Thinking Beast モード | 段階的思考 |
| [`Ultimate-Transparent-Thinking-Beast-Mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/Ultimate-Transparent-Thinking-Beast-Mode.agent.md) | 究極透明思考 Beast モード | 思考プロセス可視化 |
| [`gpt-5-beast-mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/gpt-5-beast-mode.agent.md) | GPT-5 Beast モード | 最高性能モード |
| [`rust-gpt-4.1-beast-mode.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/rust-gpt-4.1-beast-mode.agent.md) | Rust GPT-4.1 Beast モード | Rust 高性能開発 |
| [`voidbeast-gpt41enhanced.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/voidbeast-gpt41enhanced.agent.md) | VoidBeast GPT-4.1 Enhanced | 拡張推論 |
| [`hlbpa.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/hlbpa.agent.md) | HLBPA | 高レベル計画 |
| [`droid.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/droid.agent.md) | Droid | 汎用エージェント |

---

### その他の専門エージェント

| ファイル名 | ペルソナ | 活用場面 |
|-----------|---------|---------|
| [`principal-software-engineer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/principal-software-engineer.agent.md) | プリンシパルソフトウェアエンジニア | 上級エンジニアリング指導 |
| [`software-engineer-agent-v1.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/software-engineer-agent-v1.agent.md) | ソフトウェアエンジニアエージェント v1 | 汎用開発支援 |
| [`custom-agent-foundry.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/custom-agent-foundry.agent.md) | カスタムエージェントファウンドリ | エージェント作成支援 |
| [`meta-agentic-project-scaffold.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/meta-agentic-project-scaffold.agent.md) | メタエージェントプロジェクトスキャフォールド | エージェントプロジェクト雛形 |
| [`adr-generator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/adr-generator.agent.md) | ADR ジェネレーター | Architecture Decision Record 生成 |
| [`api-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/api-architect.agent.md) | API アーキテクト | API 設計 |
| [`openapi-to-application.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/openapi-to-application.agent.md) | OpenAPI → アプリケーション | OpenAPI からコード生成 |
| [`prompt-builder.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/prompt-builder.agent.md) | プロンプトビルダー | プロンプト作成支援 |
| [`prompt-engineer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/prompt-engineer.agent.md) | プロンプトエンジニア | プロンプト最適化 |
| [`technical-content-evaluator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/technical-content-evaluator.agent.md) | 技術コンテンツ評価者 | コンテンツ品質評価 |
| [`search-ai-optimization-expert.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/search-ai-optimization-expert.agent.md) | 検索 AI 最適化エキスパート | 検索最適化 |
| [`accessibility.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/accessibility.agent.md) | アクセシビリティ専門家 | a11y 対応 |
| [`insiders-a11y-tracker.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/insiders-a11y-tracker.agent.md) | VS Code Insiders アクセシビリティトラッカー | VS Code Insiders の a11y 改善追跡 |
| [`markdown-accessibility-assistant.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/markdown-accessibility-assistant.agent.md) | Markdown アクセシビリティアシスタント | Markdown ドキュメントの a11y 改善 |
| [`simple-app-idea-generator.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/simple-app-idea-generator.agent.md) | シンプルアプリアイデアジェネレーター | アイデア出し |
| [`repo-architect.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/repo-architect.agent.md) | リポジトリアーキテクト | プロジェクト構造設計 |
| [`bicep-plan.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/bicep-plan.agent.md) | Bicep 計画 | Bicep IaC 計画 |
| [`bicep-implement.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/bicep-implement.agent.md) | Bicep 実装 | Bicep IaC 実装 |
| [`aem-frontend-specialist.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/aem-frontend-specialist.agent.md) | AEM フロントエンド専門家 | Adobe Experience Manager |
| [`cast-imaging-impact-analysis.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/cast-imaging-impact-analysis.agent.md) | CAST Imaging 影響分析 | アプリケーション分析 |
| [`cast-imaging-software-discovery.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/cast-imaging-software-discovery.agent.md) | CAST Imaging ソフトウェア発見 | ソフトウェア可視化 |
| [`cast-imaging-structural-quality-advisor.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/cast-imaging-structural-quality-advisor.agent.md) | CAST Imaging 構造品質アドバイザー | コード品質分析 |
| [`taxcore-technical-writer.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/taxcore-technical-writer.agent.md) | TaxCore テクニカルライター（電子財政請求エコシステム専門） | TaxCore / Secure Element Reader のドキュメント作成 |
| [`ember.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/ember.agent.md) | Ember（AI パートナーペルソナ） | AI パートナーシップ体験の共有・人々への火の伝達 |

---

## まとめ

Agents は **213 ファイル** あり、以下のカテゴリに分類されます：

| カテゴリ | ファイル数 | 主な用途 |
|---------|----------|---------|
| コード品質・レビュー | 約 18 | セキュリティ、アーキテクチャレビュー、ガバナンス |
| 計画・設計 | 約 25 | PRD、仕様書、実装計画、マルチエージェント調整 |
| メンタリング・教育 | 約 7 | 新人指導、学習支援、ドキュメント作成 |
| デバッグ・保守 | 約 8 | バグ調査、コードクリーンアップ、パフォーマンス診断 |
| 言語・フレームワーク専門家 | 約 29 | .NET, React, Vue, Nuxt, Salesforce, WinUI 3 等 |
| MCP サーバー開発 | 約 10 | 各言語の MCP SDK |
| インフラ・DevOps | 約 19 | CI/CD, Kubernetes, Terraform, Terratest |
| Azure・クラウド | 約 13 | Azure アーキテクチャ、IaC、ポリシー分析、セキュリティ |
| データベース | 約 10 | PostgreSQL, SQL Server, MongoDB |
| Power Platform・BI | 約 10 | Power BI, Power Platform |
| Microsoft 365 | 約 5 | M365 Copilot エージェント |
| テスト | 約 18 | TDD, Playwright, Polyglot テスト自動化、モバイル E2E |
| AI・機械学習 | 約 6 | Python AI/ML, Notebook サンプル, PySpark |
| 移行・モダナイゼーション | 約 14 | レガシー刷新、React 18/19 移行、Oracle→PostgreSQL |
| 外部サービス連携 | 約 14 | 各種 SaaS 連携、科学論文検索 |
| 高度なモード | 約 8 | Beast モード、高性能推論 |
| その他 | 約 15 | 専門エージェント、a11y、LinkedIn、TaxCore |

プロジェクトの課題に応じて、最適な専門家エージェントを選んで相談しましょう。
