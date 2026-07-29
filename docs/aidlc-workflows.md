# awslabs/aidlc-workflows — AI 駆動開発ライフサイクル（AI-DLC）ワークフロー

> [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) は AWS が公開した、AI エージェントを**検証可能・自己修正可能なエンジニアリングワークフロー**へと変える OSS プロジェクトです。GitHub Copilot、Claude Code、Amazon Q Developer、Cursor、Cline、Codex など主要なコーディングエージェントに対応しています。

## AI-DLC とは

AI-DLC（AI-Driven Development Life Cycle）は、AIコーディングエージェントが「すぐ実装しようとする」「計画なしに進める」「品質チェックを省略する」といった問題行動を、**ルールファイル（ワークフロー定義）によって構造的に防ぐ**インテリジェントなソフトウェア開発ワークフローです。

チャットで「Using AI-DLC, ...」と書くだけでワークフローが起動し、要件整理から設計・実装・品質確認まで**AIエージェントが段階的に自律実行**します。

| 項目 | 内容 |
|------|------|
| **提供元** | AWS Labs（awslabs） |
| **リポジトリ** | [github.com/awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) |
| **ライセンス** | Apache-2.0 |
| **対応ツール** | GitHub Copilot、Amazon Q Developer、Claude Code、Cursor、Cline、OpenAI Codex、Kiro、その他任意のエージェント |
| **最新版** | v2（AI-DLC Workflows 2.0） |

---

## 3 フェーズの適応型ワークフロー

AI-DLC はプロジェクトの複雑さに応じて自動的に適応する、3 フェーズの構造化ワークフローを採用しています。

### フェーズ 1 — Inception（着想・要件定義）

**「何を作るか」と「なぜ作るか」を決める**

- 要件の分析とバリデーション
- ユーザーストーリーの作成（該当する場合）
- アプリケーション設計と並行開発のための作業単位の作成
- リスク評価と複雑さの評価

### フェーズ 2 — Construction（設計・実装）

**「どのように作るか」を決める**

- 詳細なコンポーネント設計
- コード生成と実装
- ビルド構成とテスト戦略
- 品質保証とバリデーション

### フェーズ 3 — Operations（運用）※将来対応

**デプロイと監視**

- デプロイの自動化とインフラストラクチャ
- モニタリングとオブザーバビリティのセットアップ
- 本番環境への準備検証

---

## 主な特徴

| 特徴 | 説明 |
|------|------|
| **適応的インテリジェンス** | リクエストに応じて価値を追加するステージのみを実行 |
| **コンテキスト認識** | 既存のコードベースと複雑さの要件を分析 |
| **リスクベース** | 複雑な変更には包括的な処理、単純な変更は効率的に処理 |
| **質問駆動** | チャットではなくファイルへの構造化された多肢選択式の質問 |
| **常に制御可能** | 実行計画を確認し、各フェーズを承認できる |
| **拡張可能** | セキュリティ・コンプライアンス・組織固有のルールをコアワークフローに追加可能 |

---

## セットアップ方法

### 1. リリースファイルのダウンロード

[Releases ページ](https://github.com/awslabs/aidlc-workflows/releases/latest)から最新の `ai-dlc-rules-v<バージョン>.zip` をダウンロードし、プロジェクトディレクトリ**外**（例：`~/Downloads`）に展開します。

展開後のフォルダ構成：

```
aidlc-rules/
├── aws-aidlc-rules/        # コアワークフロールール
└── aws-aidlc-rule-details/ # コアルールから参照される詳細ルール
```

### 2. 使用するコーディングエージェントに応じてセットアップ

---

#### GitHub Copilot

AI-DLC は `.github/copilot-instructions.md` を使用してワークフローを実装します。

**macOS/Linux:**

```bash
mkdir -p .github
cp ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md .github/copilot-instructions.md
mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "$env:USERPROFILE\Downloads\aidlc-rules\aws-aidlc-rules\core-workflow.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".aidlc-rule-details"
Copy-Item "$env:USERPROFILE\Downloads\aidlc-rules\aws-aidlc-rule-details\*" ".aidlc-rule-details\" -Recurse
```

**確認方法：**

1. VS Code でプロジェクトフォルダを開く
2. Copilot Chat パネル（Cmd/Ctrl+Shift+I）を開く
3. **Configure Chat**（歯車アイコン）> **Chat Instructions** で `copilot-instructions` が一覧にあることを確認

**ディレクトリ構成：**

```
<プロジェクトルート>/
├── .github/
│   └── copilot-instructions.md
└── .aidlc-rule-details/
    ├── common/
    ├── inception/
    ├── construction/
    ├── extensions/
    └── operations/
```

---

#### Amazon Q Developer

AI-DLC は `.amazonq/rules/` を使用してワークフローを実装します。

**macOS/Linux:**

```bash
mkdir -p .amazonq/rules
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rules .amazonq/rules/
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details .amazonq/
```

**確認方法：**

Amazon Q Chat ウィンドウで `Rules` ボタン（右下）をクリックし、`.amazonq/rules/aws-aidlc-rules` のエントリがあることを確認します。

---

#### Claude Code

AI-DLC は `CLAUDE.md`（プロジェクトメモリファイル）を使用してワークフローを実装します。

**macOS/Linux（プロジェクトルートに配置）：**

```bash
cp ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md ./CLAUDE.md
mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

**確認方法：**

1. プロジェクトディレクトリで Claude Code を起動
2. `/config` コマンドで現在の設定を確認
3. Claude に「このプロジェクトで現在有効なインストラクションは？」と確認

---

#### Cursor

**Option 1: Project Rules（推奨）**

```bash
mkdir -p .cursor/rules

cat > .cursor/rules/ai-dlc-workflow.mdc << 'EOF'
---
description: "AI-DLC (AI-Driven Development Life Cycle) adaptive workflow for software development"
alwaysApply: true
---
EOF
cat ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md >> .cursor/rules/ai-dlc-workflow.mdc

mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

**Option 2: AGENTS.md（シンプルな代替手段）**

```bash
cp ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md ./AGENTS.md
mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

---

#### Cline

**Option 1: .clinerules ディレクトリ（推奨）**

```bash
mkdir -p .clinerules
cp ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md .clinerules/
mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

---

#### OpenAI Codex

Codex はプロジェクトルートの `AGENTS.md` を自動検出して読み込みます。

```bash
cp ~/Downloads/aidlc-rules/aws-aidlc-rules/core-workflow.md ./AGENTS.md
mkdir -p .aidlc-rule-details
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details/* .aidlc-rule-details/
```

---

#### Kiro

AI-DLC は [Kiro Steering Files](https://kiro.dev/docs/cli/steering/) を使用してワークフローを実装します。

```bash
mkdir -p .kiro/steering
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rules .kiro/steering/
cp -R ~/Downloads/aidlc-rules/aws-aidlc-rule-details .kiro/
```

> [!NOTE]
> Kiro IDE では Vibe モードで AI-DLC ワークフローを実行します。Kiro が Spec モードへの切り替えを促した場合は `No` を選択して Vibe モードを維持してください。

---

## 使い方

セットアップ後は、チャットで以下のように入力するだけでワークフローが起動します。

```
Using AI-DLC, [作りたいものの説明]
```

**例：**

- `Using AI-DLC, ユーザー認証機能を追加したい`
- `Using AI-DLC, 既存のプロジェクトを分析してほしい`

**ワークフローの流れ：**

1. `Using AI-DLC, ...` でチャットを開始
2. AI-DLC ワークフローが自動的に起動し、対話形式で導いてくれる
3. AI-DLC が提示する構造化された質問に回答
4. AI が生成するすべての計画を慎重にレビューし、フィードバックを提供
5. 実行計画を確認して、どのステージが実行されるかを把握
6. 各ステージの成果物を慎重にレビューして承認し、制御を維持
7. すべての成果物は `aidlc-docs/` ディレクトリに生成される

---

## 拡張機能（Extensions）システム

AI-DLC はコアワークフローの上に追加ルールを重ねる拡張システムをサポートしています。拡張機能は `aws-aidlc-rule-details/extensions/` 配下のカテゴリ別マークダウンファイルとして構成されています。

### 組み込み拡張機能

| 拡張機能 | 説明 |
|---------|------|
| **security/baseline** | セキュリティのベースラインルール（組織固有にカスタマイズ推奨） |
| **testing/property-based** | プロパティベーステストのルール |
| **resiliency/baseline** | 耐障害性のベースラインルール |

### 拡張機能の仕組み

各拡張機能は 2 つのファイルで構成されます：

- **ルールファイル**（例：`security-baseline.md`）— 拡張ルールの定義
- **オプトインファイル**（例：`security-baseline.opt-in.md`）— 要件分析時にユーザーへ提示する多肢選択式の質問

ワークフロー開始時に `*.opt-in.md` ファイルをスキャンし、要件分析フェーズで各オプトインを提示します。ユーザーがオプトインすると対応するルールファイルがロードされます。

### 独自の拡張機能を追加する方法

1. `extensions/` 配下にディレクトリを作成（例：`security/compliance/`）
2. ルールファイルを追加。各ルールは `## Rule <PREFIX-NN>: <タイトル>` 形式の見出し（例：`COMPLIANCE-01`）で定義
3. オプトインファイルを追加（省略した場合、拡張は常に適用される）

---

## ツール・エバリュエーター

`scripts/aidlc-evaluator/` ディレクトリには AI-DLC ワークフローの変更を検証するための自動テスト・レポートフレームワークが含まれています。

| 機能 | 説明 |
|------|------|
| **ゴールデンテストケース** | 検証用のベースラインテストケース |
| **セマンティック評価** | 出力の正確性と完全性を AI ベースで評価 |
| **コード評価** | 静的解析（リンティング、セキュリティスキャン、重複検出） |
| **NFR 評価** | 非機能要件のテスト（トークン使用量、実行時間、クロスモデル一貫性） |
| **CI/CD 統合** | PR バリデーション用の自動パイプライン |

**クイックスタート：**

```bash
cd scripts/aidlc-evaluator
uv sync
uv run python run.py test
```

---

## 関連リソース

| リソース | URL |
|---------|-----|
| リポジトリ | [github.com/awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) |
| AI-DLC 2.0 仕様書 | [PDF（英語）](https://github.com/awslabs/aidlc-workflows/blob/v2/assets/AI-DLC-Workflows-2.0-Specification.pdf) |
| AWS DevOps ブログ | [AI-Driven Development Life Cycle（英語）](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/) |
| メソッド定義ペーパー | [prod.d13rzhkk8cj2z0.amplifyapp.com（英語）](https://prod.d13rzhkk8cj2z0.amplifyapp.com/) |
| デザインレビューツール | [aws-samples/sample-aidlc-design-reviewer（実験的）](https://github.com/aws-samples/sample-aidlc-design-reviewer) |
| AWS 責任ある AI ポリシー | [aws.amazon.com/ai/responsible-ai/policy/（英語）](https://aws.amazon.com/ai/responsible-ai/policy/) |

> [!IMPORTANT]
> 生成 AI は誤りを犯すことがあります。AI モデルとエージェントコーディングアシスタントが生成するすべての出力とコストを必ずレビューすることを検討してください。
