# AI-DLC・AI-PDLC・AI BPRは何が違うのか

> **対象ツール**: AI-DLC Workflows・AI-PDLC公開サンプル・AI BPR ｜ **実行環境**: CLI / IDE ｜ **対象読者**: AIエージェントを開発・業務へ導入する担当者 ｜ **最終更新**: 2026-09-11

AWSの公開情報では、AI-DLC、AI-PDLC、AI BPRという似た名前が使われています。このページでは、三つを「何を決めるか」と「現在どのように公開されているか」で分けます。

> 三つを順番に実行する一つの公式製品や、統合された公式パイプラインが発表されているという意味ではありません。それぞれの領域は重なります。

## 30秒で整理する

| 名前 | 主な問い | 対象 | 公開形態 |
|------|----------|------|----------|
| AI BPR | 人とAIの役割をどう組み直すか。 | 業務プロセス、組織、責任分担。 | AWSが顧客向けプログラムとして紹介。 |
| AI-PDLC | 顧客にとって何を作るべきか。 | 顧客理解、製品企画、設計、開発、運用。 | AWS Samplesにハンドブックとエージェントの公開サンプルあり。 |
| AI-DLC | どのように開発し、検証するか。 | ソフトウェア開発ライフサイクル。 | AWS LabsがAI-DLC WorkflowsをOSSとして公開。 |

## AI BPR — 業務と役割を組み直す

AI BPRは、AI-driven Business Process Re-Engineeringの略です。既存業務の一部へAIを追加するだけでなく、AIエージェントが存在する前提で、人が集中する価値とAIへ委ねる仕事を見直します。

AWS公式ブログでは、次の4ステップで説明されています。

| ステップ | 扱う内容 |
|----------|----------|
| Observe | 業務、強み、価値、リスクを把握する。 |
| Shift | 人とAIエージェントの役割を再設計する。 |
| Simulate | 新しい業務の流れを試し、評価する。 |
| Forecast | 導入のロードマップを作る。 |

AWSは顧客やパートナーとの提供事例、アカウントチーム向け研修、ProServeと専用メニューを構築する計画を紹介しています。利用したい場合の案内先はAWSアカウントチームです。

本調査では、AI BPRの公式Skills一式を誰でも取得できる一般公開先は確認できませんでした。これはAWSが「未公開」と宣言したことを意味しません。

## AI-PDLC — 製品として何を作るかを考える

AI-PDLCは、AIを製品開発ライフサイクルへ組み込む考え方です。顧客の声、価値仮説、要件、設計、開発、提供後の改善までを扱います。公開情報では、AI-PDLCとAIPDLCの表記が見られます。

AWS Samplesの`sample-claude-code-agents-for-product-teams`は、ツールに依存しない製品開発ハンドブックと、Claude Code用プラグインを公開しています。製品責任者、ビジネス分析、UX、設計、セキュリティ、開発、QA、運用など、役割別のエージェントと成果物を定義しています。

これは導入可能な公開サンプルです。AWSの独立したマネージドサービスがGAになった、という意味ではありません。

## AI-DLC — 開発を進め、検証する

AI-DLCは、AI-Driven Development Life Cycleの略です。AIコーディングエージェントによる要件整理、設計、実装、テスト、デプロイ、運用を、成果物と人の確認地点を持つ流れとして管理します。

AWS LabsのAI-DLC Workflowsは、複数のコーディングエージェントへ導入できるOSSです。AWSにデプロイするアプリ専用ではなく、方法論自体はモデル提供元に依存しないと説明されています。

実際に試す手順は、[日本語で試すAI-DLC入門](aidlc-workflows.md)を参照してください。

## どこから始めるか

| 現在の状況 | 最初に考える領域 |
|------------|------------------|
| 業務の分担や目的から見直したい。 | AI BPRの問いを使い、人とAIの責任を整理する。 |
| 顧客の要望はあるが、作る製品が決まっていない。 | AI-PDLCの観点で価値仮説と製品判断を整理する。 |
| 作る機能は決まり、開発の進め方を整えたい。 | AI-DLC Workflowsを試す。 |
| Power Appsで業務アプリを作りたい。 | [Power Apps PlansとAI-DLCの比較](ai-dlc-power-platform.md)から選ぶ。 |

この表は、本ガイドが理解のために整理した選び方です。AWSが三つの手法の実行順序として公式に定義したものではありません。

## 公開情報の読み方

| 表示 | 意味 |
|------|------|
| AWS公式ブログ | AWSが公開した解説や事例。製品のサービス仕様書とは限らない。 |
| `awslabs` | AWS Labsが管理するOSS。AWSマネージドサービスとは限らない。 |
| `aws-samples` | AWSが公開するサンプル。サンプルの注意事項とライセンスを確認して利用する。 |
| 本ガイドの整理 | 複数の公開資料を比較した説明。AWSの公式な製品分類ではない。 |

## 公式情報と状態

| リソース | 提供元 | 状態 | 確認できること |
|----------|--------|------|------------------|
| [AI BPRの解説](https://aws.amazon.com/jp/blogs/news/ai-bpr/) | Official（AWS） | —（顧客向けプログラム） | 方法、事例、相談窓口、今後の提供計画。 |
| [AI-PDLC公開サンプル](https://github.com/aws-samples/sample-claude-code-agents-for-product-teams) | Official（AWS Samples） | —（公開サンプル） | 製品開発ハンドブック、役割別エージェント、Claude Codeプラグイン。 |
| [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) | Official（AWS Labs） | GA | OSSの実装、対応ハーネス、導入方法。 |
| [AI-PDLCの紹介](https://builder.aws.com/content/31nH8BYD9j9uCxMMsvSVKP78UDW/ai-driven-product-development-lifecycle-aipdlc-building-what-customers-actually-need) | Official（AWS Builder Center） | —（解説） | 顧客の声から製品判断へ進む方法論。 |

> [!NOTE]
> 提供状況、導入手順、リージョン、対応言語は変わります。導入前にリンク先の最新版を確認してください。
