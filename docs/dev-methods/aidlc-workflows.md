# AI-DLC Workflows — 日本語で試すAI駆動開発ライフサイクル

> **対象ツール**: AI-DLC Workflows（Codex・Claude Code・Kiro・Cursor・GitHub Copilotほか） ｜ **実行環境**: CLI / IDE ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-11

> [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) は、AWS Labsが公開するAI駆動開発ライフサイクルのOSS実装です。AWSのマネージドサービスではありません。

## 30秒で判断する

| 確認したいこと | 回答 |
|----------------|------|
| 自分で試せるか。 | はい。公開されているインストーラーから導入できます。 |
| AWSへデプロイする必要があるか。 | ありません。完成するアプリの実行場所はプロジェクト側で決めます。 |
| Bedrockが必須か。 | 方法論自体はモデル提供元に依存しません。実際の接続先は利用するハーネスの設定に従います。 |
| 日本語で依頼できるか。 | できます。ただし、説明の一部に英語が混ざる不具合報告があります。 |
| Power Platformにも使えるか。 | 開発工程の考え方は適用できますが、専用の公式連携は確認できていません。詳しくは[Plansとの比較](ai-dlc-power-platform.md)を参照してください。 |

## AI-DLC Workflowsが解決すること

AIコーディングエージェントへ短い依頼だけを渡すと、要件を詰める前に実装したり、テスト結果を十分に確認せず完了と判断したりすることがあります。

AI-DLC Workflowsは、要件、設計、実装、テスト、運用を一つの流れとして扱います。作業内容に合わせて必要な工程を選び、成果物と判断を記録し、人が確認する地点を設けます。

> AI-DLCと似た名前の手法は、[AI-DLC・AI-PDLC・AI BPRの用語整理](ai-driven-lifecycle-terms.md)で分けて説明しています。

## 5つのフェーズ

現行のAI-DLC Workflowsは、次の5フェーズで構成されています。すべての作業で全工程を実行するわけではありません。

| フェーズ | 主な役割 |
|----------|----------|
| Initialization | プロジェクトと実行状態を準備する。 |
| Ideation | 意図、対象範囲、実現可能性を整理する。 |
| Inception | 要件、設計、作業単位、実行計画を具体化する。 |
| Construction | 詳細設計、実装、ビルド、テストを行う。 |
| Operation | デプロイ、監視、性能確認、改善を扱う。 |

AWSの方法論や学習コースでは、開発の中心をInception、Construction、Operationの3フェーズで説明しています。現行のOSS実装「AI-DLC Workflows」は、その前段にInitializationとIdeationを置いた5フェーズ、33ステージです。このページで5フェーズと書く場合は、現行のOSS実装を指します。

機能追加、バグ修正、PoC、インフラ変更など、依頼の種類に応じたワークフローがあります。各工程には常に実行するものと、対象範囲に応じて選ばれるものがあります。

## 対応するハーネス

ハーネスは、AI-DLC Workflowsを実際に動かすコーディングエージェントです。現行の公式READMEに掲載されている主な選択肢は次のとおりです。

| ハーネス | `aidlc config`の値 | ワークフローの開始 |
|----------|----------------------|----------------------|
| Claude Code | `claude` | `/aidlc` |
| Kiro CLI | `kiro` | `/aidlc` |
| Kiro IDE | `kiro-ide` | `/aidlc` |
| Codex CLI | `codex` | `$aidlc` |
| Cursor | `cursor` | `/aidlc` |
| OpenCode | `opencode` | `/aidlc` |
| GitHub Copilot | `copilot` | `/aidlc` |

必要なバージョンや認証方法は変わるため、導入時には[公式Getting Started](https://awslabs.github.io/aidlc-workflows/guide/01-getting-started/)を確認してください。

## Windowsで試す最小手順

以下は公式Getting Startedとリリースページに基づく手順です。このガイドではインストーラーの実行とモデル接続を実機検証していません。

### 1. AI-DLCをインストールする

GitHubの最新リリース情報から、インストーラーと公開されているSHA-256ダイジェストを取得します。インストーラーは、すぐに実行せずファイルとして保存します。

```powershell
$release = Invoke-RestMethod "https://api.github.com/repos/awslabs/aidlc-workflows/releases/latest"
$asset = $release.assets | Where-Object { $_.name -eq "install.ps1" } | Select-Object -First 1
if (-not $asset -or -not $asset.digest) {
    throw "install.ps1またはSHA-256ダイジェストを取得できません。"
}

$installer = Join-Path $PWD "install-aidlc.ps1"
Invoke-WebRequest $asset.browser_download_url -OutFile $installer
Get-Content -LiteralPath $installer

$actualHash = (Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedHash = $asset.digest -replace "^sha256:", ""
if ($actualHash -ne $expectedHash) {
    Remove-Item -LiteralPath $installer
    throw "SHA-256が一致しないため、インストーラーを削除しました。"
}
```

表示されたスクリプトの内容と、[最新リリース](https://github.com/awslabs/aidlc-workflows/releases/latest)の説明を確認してから実行します。

```powershell
$version = $release.tag_name.TrimStart("v")
& $installer -Version $version
Remove-Item -LiteralPath $installer
```

組織でダウンロードしたスクリプトの実行が禁止されている場合は、実行せず管理者へ確認してください。

### 2. 試すプロジェクトを設定する

Codex CLIを使う例です。対象はGitリポジトリである必要があります。

```powershell
Set-Location C:\work\todo-sample
aidlc config --harness codex
aidlc doctor
```

別のハーネスを使う場合は、前の表にある値へ置き換えます。`aidlc config`を引数なしで実行すると、利用できるハーネスを対話形式で選べます。

### 3. 日本語で開始する

Codex CLI内では、次のように入力します。

```text
$aidlc Windowsのローカルで動くToDoアプリを作りたい。
質問、説明、要件定義書、設計書は日本語にする。
データはSQLiteへ保存し、AWSやクラウドへはデプロイしない。
```

ほかの対応ハーネスでは、`$aidlc`の代わりに`/aidlc`を使います。

## 実際のやり取り

質問の内容や順序は、依頼の規模と選ばれたワークフローで変わります。次は実行ログではなく、体験を理解するための例です。

```text
AI: 利用者は一人ですか。期限や優先度は必要ですか。
人: 自分だけで使います。期限は必要ですが、優先度はいりません。

AI: タスクの追加・編集・削除、期限、完了状態、SQLiteへの保存を
    対象にします。ログインと端末間同期は対象外です。
    要件を確認して設計へ進めますか。
人: 期限切れを赤く表示する要件を追加してください。
```

AIは回答を要件と設計へ反映し、実装、ビルド、テストへ進みます。人は、業務上の判断、成果物、テスト結果、外部へ影響する操作を確認します。

## AWSで動くアプリに限定されない理由

AI-DLCを使うときには、次の三つを分けて考えます。

| 選択するもの | 例 |
|--------------|----|
| AI-DLCを動かすハーネス。 | Codex、Claude Code、Kiroなど。 |
| AIモデルの接続先。 | ハーネスが対応するモデル提供元。 |
| 完成したアプリの実行場所。 | ローカルPC、社内サーバー、Power Platform、クラウドなど。 |

AWS Platform Agentやインフラ設計の工程が存在しても、すべてのプロジェクトでAWSリソースを作るわけではありません。ローカルアプリなら、最初の依頼と要件に「クラウドへデプロイしない」と記録し、インフラ構築・デプロイ工程の実行計画を確認します。

## 日本語利用時の注意

日本語の入力と日本語の成果物を指定できます。一方、非英語の会話でも自由記述の説明が英語になる事象が、公式リポジトリのIssueで報告されています。

開始時に次の条件を明示し、生成された要件書と設計書の言語も確認してください。

```text
会話と成果物は日本語にする。
コマンド名、ファイル名、API名など変更できない識別子は原文を維持する。
```

## AI-DLCが向く開発

| 向く状況 | 理由 |
|----------|------|
| 要件と実装の対応を残したい。 | 判断と成果物を工程ごとに記録できる。 |
| 複数の担当領域が関係する。 | 設計、品質、セキュリティ、運用の観点を分けて扱える。 |
| 既存システムを段階的に変更する。 | 既存コードの調査と変更計画を実装前に置ける。 |
| チーム固有の確認事項がある。 | ルールや工程を拡張できる。 |

小さな試作では、全工程を細かく実行すると確認作業のほうが大きくなることがあります。最初は軽量なワークフローを使い、必要な成果物と確認地点を見極めます。

## 公式情報と状態

| リソース | 提供元 | 状態 | 確認できること |
|----------|--------|------|------------------|
| [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) | Official（AWS Labs） | GA（安定版） | 現行README、対応ハーネス、ライセンス、機能。 |
| [Getting Started](https://awslabs.github.io/aidlc-workflows/guide/01-getting-started/) | Official（AWS Labs） | GA（安定版） | インストール、設定、最初の実行。 |
| [Orchestrator Reference](https://awslabs.github.io/aidlc-workflows/reference/03-orchestrator/) | Official（AWS Labs） | GA（安定版） | フェーズ、工程、実行条件。 |
| [日本語コースの案内](https://aws.amazon.com/jp/blogs/news/aidlc-aws-skill-builder/) | Official（AWS） | —（公開コース） | 無料の日本語学習コースと方法論の3フェーズ。 |
| [非英語で説明が混在するIssue](https://github.com/awslabs/aidlc-workflows/issues/780) | Community（公式リポジトリ上の報告） | —（Issue） | 日本語を含む非英語利用時に確認すべき事象。 |

## 関連ドキュメント

- [Power Apps PlansとAI-DLCの比較](ai-dlc-power-platform.md) — Power Platformで使う場合の役割と導入判断。
- [AI-DLC・AI-PDLC・AI BPRの違い](ai-driven-lifecycle-terms.md) — 似た名前の対象と公開形態。
- [仕様駆動開発（SDD）](spec-driven.md#ai-dlc-との関係--どちらを選ぶか) — GitHub Spec Kitとの選び方。

> [!IMPORTANT]
> 生成AIの出力、実行するコマンド、テスト結果、費用、外部システムへの変更は人が確認してください。
