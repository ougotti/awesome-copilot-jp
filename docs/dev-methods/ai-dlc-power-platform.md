# Power Apps PlansがあるのにAI-DLCを使う意味はあるのか

> **対象ツール**: Power Apps Plans・AI-DLC Workflows・Power Platform CLI / Pipelines ｜ **実行環境**: Cloud / CLI / IDE ｜ **対象読者**: Power Platformの業務アプリを作る担当者・開発者 ｜ **最終更新**: 2026-09-11

> AWSまたはMicrosoftが、AI-DLC WorkflowsとPower Apps Plansの併用を公式に推奨している事実は確認できていません。本記事の比較とPower Platformへの適用方法は、両者の公開仕様から考えた案です。AI-DLCからPower Platformへの実装・デプロイは実機検証していません。

## 先に結論

Power AppsとPower Automateで完結する業務アプリなら、まずPlansを検討します。Power Platformの製品内で、業務の説明からデータとアプリの構成へ直接進めるためです。

独自APIや別のシステムも変更する場合、または要件、設計、テストの対応を長く維持する必要がある場合は、AI-DLC Workflowsを開発全体の進行に使う余地があります。

## Plansでできること

Power AppsのPlansは、自然言語で記述した業務上の課題や、既存画面・業務フローの画像を基に、業務ソリューションの計画を作る機能です。

公式資料では、利用者と要件を整理し、Dataverseテーブル、キャンバスアプリ、モデル駆動型アプリ、Power Pages、Power Automateクラウドフロー、Copilot Studioエージェントなどを含む構成を生成すると説明されています。

Plans自体はGAと案内されています。ただし、Code Appの生成など、関連する一部の機能はPreviewです。Dataverseを備えた対象環境、作成権限、地域と言語の提供条件も必要です。

## AI-DLC Workflowsでできること

AI-DLC Workflowsは、特定の業務アプリ製品ではなく、ソフトウェア開発の進め方を制御するOSSです。要件、設計、実装、ビルド、テスト、デプロイ、運用を一つの流れとして扱い、必要な工程と人が確認する地点を選びます。

AI-DLC単体に、Power Appsの画面やPower Automateフローを操作する専用機能が含まれているとは確認できません。Power Platformへ適用するには、AIが編集できるソース、Power Platform CLI、Pipelines、各環境の権限などを別途組み合わせる必要があります。

AI-DLCそのものは、[日本語で試すAI-DLC入門](aidlc-workflows.md)で説明しています。

## 同じ購入申請アプリで比べる

「社員が備品購入を申請し、金額に応じて上長または部門長が承認するアプリ」を例にします。

| 工程 | Plansを起点にする場合 | AI-DLCを起点にする場合 |
|------|----------------------|-------------------------|
| 業務の入力 | 業務上の課題、利用者、既存画面やフローを入力する。 | 作りたい機能、制約、既存システム、完了条件を入力する。 |
| 要件整理 | 利用者、ユーザーストーリー、必要なデータを計画へ反映する。 | 承認条件、例外、非機能要件を成果物として確認する。 |
| 設計 | Dataverse、アプリ、フローなどPower Platformの構成へ進む。 | Power Platformを含むシステム全体の設計と作業単位を決める。 |
| 実装 | Power Apps内の生成・編集機能から実装へ進む。 | 利用ハーネスが扱えるコード、CLI、APIを通じて実装する。 |
| テスト | Power Platformのテスト機能やALMへつなぐ。 | 受け入れ条件との対応、ビルド、テスト結果を工程内で確認する。 |
| リリース | SolutionとPipelinesを使って環境間を移送する。 | Power Platform側のSolution、Pipelines、権限を実行手段として使う。 |

ここで差が出るのは、画面生成の速度だけではありません。次の例外をどこで発見し、誰が判断し、どのテストで保証するかが重要です。

- 承認者が不在の場合。
- 申請後に金額が変更された場合。
- 同じ領収書を使った重複申請。
- 申請者が自分の権限を超えて状態を変更した場合。
- 通知に失敗した場合。

## PlansとAI-DLCの比較

| 観点 | Power Apps Plans | AI-DLC Workflows |
|------|------------------|------------------|
| 製品上の位置づけ | Power Appsに組み込まれた機能。 | AWS Labsが公開するOSS。 |
| 主な対象 | Power Platformの業務ソリューション。 | 技術構成を限定しないソフトウェア開発。 |
| 実装への距離 | Power Platformの構成と作成へ直接つながる。 | 対象環境を操作するツールとの接続が必要。 |
| 開発工程 | Plansで要件と構成を反復し、Power Platformの開発・ALM機能と組み合わせる。 | 要件から運用までの工程、成果物、確認地点を管理する。 |
| カスタマイズ | Microsoftが提供するPlansの操作と機能を使う。 | 工程、エージェント、ルールを変更できる。 |
| 前提 | Dataverse環境、権限、地域・言語条件。 | 対応ハーネス、AIモデル、対象プロジェクト。 |
| 日本語 | 地域・言語別の提供状況を確認する。一部のVibe機能は英語のみ。 | 日本語を指定できるが、説明に英語が混ざる報告がある。 |

## 公平に比較するならALMまで含める

Plansだけを取り出して、テストやリリースの機能が不足していると判断するのは適切ではありません。Power PlatformにはSolution、Pipelines、CLIなどのALM機能があります。

Pipelinesは、開発環境から対象環境へのSolutionの展開、接続参照と環境変数の事前確認、承認に基づくデプロイ、実行履歴などを提供します。CLIを使えば、Solutionの展開やソース管理に必要な操作の一部をコマンドから実行できます。

比較する単位は次の二つです。

- Plansと、Power Platformの開発・テスト・ALM機能。
- AI-DLC Workflowsと、対象システムの実装・テスト・デプロイ用ツール。

AI-DLC上の承認だけで、Power Platformのテナント権限や本番環境の制御を代替することはできません。

## どちらを選ぶか

| 開発の状況 | 最初に選ぶもの | 理由 |
|------------|----------------|------|
| Power Appsとフローで完結する小規模な業務アプリ。 | Plans。 | 製品内で業務の説明から実装へ進める。 |
| Power Platformの経験が少ない担当者が試作する。 | Plans。 | 必要な製品とデータ構成を対話で確認できる。 |
| 独自APIや複数システムを同時に変更する。 | AI-DLCを開発全体の進行に使うことを検討する。 | 異なる実装先をまたいで要件・設計・検証を扱える。 |
| 規制、監査、複雑な権限がある。 | 現行のALM・統制を基礎にAI-DLCの確認工程を評価する。 | AIの成果物だけではプラットフォームの権限を強制できない。 |
| 業務分担自体が決まっていない。 | アプリ生成前に業務を整理する。 | 何を自動化し、何を人が判断するかを先に決める必要がある。 |

最初からPlansとAI-DLCの両方で要件書を作ると、二重管理になる可能性があります。Plansで小さく作り、変更時の追跡、複数システムの調整、テストの証拠など、実際に不足した工程を確認してからAI-DLCを追加する方法が現実的です。

## 導入前に行う小さな比較

同じ購入申請の要件を使い、次の項目を比較します。

| 比較項目 | 確認すること |
|----------|--------------|
| 要件の確認 | 承認者不在、差し戻し、重複申請などを発見できるか。 |
| 作成の負担 | 人が入力、設定、修正する時間はどれくらいか。 |
| 実装の正しさ | 権限、状態遷移、通知、エラー処理が受け入れ条件を満たすか。 |
| 変更への対応 | 承認条件の変更を画面、フロー、テストへ反映できるか。 |
| 引き継ぎ | 別の担当者が設計理由と変更方法を理解できるか。 |

これは検証計画です。本ガイドでは速度や品質の比較結果を測定していません。

## 公式情報と状態

| リソース | 提供元 | 状態 | 本記事で確認した内容 |
|----------|--------|------|----------------------|
| [Plansの概要](https://learn.microsoft.com/en-us/power-apps/maker/plan-designer/plan-designer) | Official（Microsoft） | GA | 生成するPower Platform構成、環境と権限の前提。 |
| [Plans FAQ](https://learn.microsoft.com/en-us/power-apps/maker/common/faq-plan-designer) | Official（Microsoft） | GA / Previewを含む | 入力制限、Code App生成、言語上の制約。 |
| [Power Platform Pipelines](https://learn.microsoft.com/en-us/power-platform/alm/pipelines) | Official（Microsoft） | GA | 環境間の展開、承認、接続と環境変数の確認。 |
| [Power Platform CLI Solution](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution) | Official（Microsoft） | GA / Previewを含む | Solutionのpack、unpack、環境への操作。 |
| [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows) | Official（AWS Labs） | GA | AI-DLCの工程、対応ハーネス、拡張方法。 |

> [!IMPORTANT]
> PlansまたはAI-DLCが生成した内容は、権限、個人情報、接続先、業務ルール、テスト結果を確認してから対象環境へ展開してください。
