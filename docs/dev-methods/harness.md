# AI エージェントの実行基盤（ハーネス）

> **対象ツール**: ツール横断 ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: エンジニア・プラットフォーム担当 ｜ **最終更新**: 2026-09-23

> エージェントは「モデル」だけでは動きません。ツール呼び出し・状態管理・ループ制御・権限といった裏側の仕組みを **ハーネス（harness）** と呼びます。このページは概念、実装例（Microsoft Copilot Studio / QM / Kiro Crew / OpenAI Agents API）、そして「なぜ設計を意識するのか」を 1 か所にまとめた解説です。最近の動きだけを追いたい場合は [Skills 最新動向 10 節](../trends.md#10-aiエージェントの実行基盤ハーネス) を参照してください。

---

ChatGPT の「チャットに答える」段階から、タスクを自律的に実行する「エージェント時代」への移行に伴い、エージェントの裏側で動く**実行基盤（ハーネス）**への注目が高まっています。

「ハーネス（harness）」とは、AIモデルが外部ツールを呼び出したり、複数のステップを連鎖させたりするための仕組み全体を指す概念です。モデル本体とは別に、次の役割を担います。

| 役割 | 内容 |
|------|------|
| ツール呼び出し | 検索、データ取得、API 実行などをモデルの指示で動かす |
| 状態管理 | 会話履歴・タスク進捗・メモリを保持する |
| ループ制御 | 「計画 → 実行 → 評価」のサイクルを繰り返す |
| エラー処理 | ツール失敗・タイムアウトに対応し、再試行や代替ルートへ切り替える |
| 出力整形 | モデルの生成結果を次のツールや人間が扱いやすい形式に変換する |

## ハーネスエンジニアリングという実践

この領域には **ハーネスエンジニアリング（harness engineering）** という呼び名が付き、2026 年 2 月に相次いで公開された 2 本の記事を機に急速に広まりました。

1 本目は Mitchell Hashimoto（Terraform / Ghostty の作者）の [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) です。実践の定義がシンプルです。

> Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

エージェントの失敗をやり直しで済ませず、**同じ失敗が二度と起きないように環境の側を作り替える** — ルール、チェック、ガードレールを足していく営みをハーネスエンジニアリングと呼んでいます。

2 本目は OpenAI の [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) です。OpenAI 自身の報告では、3 人のチームが**コードを 1 行も手書きせず**、環境の設計 — ルール、フィードバックループ、文書構造、依存の順序 — に回ることで、約 5 か月（2025-08〜2026-01）で約 100 万行・1,500 件のマージ済み PR を出荷したとされています。

> エンジニアの仕事が「コードを書くこと」から「エージェントが確実に働ける環境を設計すること」へ移る、という主張の実証として引かれる事例です。数値は OpenAI の自己報告であり、そのまま一般化できる保証はありません。

## 実装を見る 4 つの入口

ハーネスは概念だけでは掴みにくいため、性格の異なる実装を 4 つ並べます。

| 実装 | 形態 | 想定利用者 | 重心 | `提供元` / `状態` |
|------|------|-----------|------|--------------------|
| Microsoft Copilot Studio | GUI・ローコードで構成する商用プラットフォーム | 業務担当者・開発者 | 業務フローの構成 | Official（Microsoft） / GA |
| QM（Y Combinator） | ソースを読める OSS（MIT） | 組織のプラットフォームエンジニア | 組織のスコープと権限 | Official（Y Combinator） / **Experimental** |
| Kiro Crew（AWS） | OSS（Apache-2.0）＋公式ビルド | 個人・チームの開発者 | セッションをまたぐ継続と起動条件 | Official（AWS） / GA |
| OpenAI Agents API | OpenAI管理のCodexハーネスを呼ぶAPI | エージェントを自社サービスへ組み込む開発者 | durable session、orchestration、context compaction、recovery | Official（OpenAI） / **Public Beta** |

## Microsoft Copilot Studio での実装例

Microsoft Copilot Studio は、ハーネスの概念を GUI で構成できるプラットフォームです。トピック（会話フロー）とアクション（ツール呼び出し）を組み合わせることで、エージェントがどのように計画を立て、ツールを順番に呼び出し、結果をユーザーへ返すかを定義できます。

| 役割 | Copilot Studio での対応 |
|------|------------------------|
| ツール呼び出し | コネクタ / Power Automate フロー / カスタム API |
| 状態管理 | 会話変数・グローバル変数 |
| ループ制御 | トピック内の条件分岐とリダイレクト |
| エラー処理 | エスカレーション・フォールバック トピック |
| 出力整形 | 応答メッセージのテンプレートと変数展開 |

## QM — ソースを読めるハーネス実装

[QM](https://github.com/yc-software/qm)（Quartermaster）は、Y Combinator が 2026 年 7 月末に MIT ライセンスで公開したハーネスです。同社が会計・法務・イベント・エンジニアリングの業務で内部利用してきたものを、そのまま OSS にしたと説明されています。

README の一文が性格をよく表しています。

> A multiplayer agent harness for work. In Slack and on the web.

**個人アシスタントではなく、会社単位で使うこと**を前提にしている点が特徴です。従業員はそれぞれ隔離されたワークスペースを持って独立して作業し、同時に Slack のチャンネル・グループ・プロジェクトで同じエージェントと協働できます。

| 分離の単位 | 何が分かれるか |
|-----------|---------------|
| 人ごと・部屋ごとのスコープ | メモリ、ファイル、キーチェーンの見え方、権限、cron、Web アプリ、**永続サンドボックス** |

### ハーネスとコーディングツールの関係

QM でいちばん参考になるのは、**Pi・OpenCode・Codex・Claude Code が同じコアを駆動する**という設計です。ハーネスを差し替えても中心の仕組みは変わりません。

つまり本ガイドがツール別に解説している Claude Code や Codex は、**ハーネスから見れば差し替え可能な部品**にあたります。ハーネスはその上位にあり、認証・スコープ・権限・スケジュール・監査を引き受けます。

| 層 | 担うもの |
|----|---------|
| ハーネス（QM のコア） | 認証、スコープ、権限、配送、cron、監査、永続化 |
| コーディングツール（Claude Code / Codex / OpenCode / Pi） | 実際のエージェントループ |
| モデル | 推論 |

構成は、ヘッドレスなコアに Postgres（セッション・メモリ・キュー）とスコープ別サンドボックスを組み合わせた形です。Web UI・管理画面・公開ポータルはコアの HTTP API 上のプラグイン、Slack もオプションのプラグインとして扱われます。**ツールの面は小さく固定**されており、そのうちの `execute` がスコープ専用サンドボックス（インストールしたものが残る「永続的なコンピューター」）でコマンドを実行します。

> ハーネス・セッションストア・サンドボックス・メモリといった基盤はすべてインターフェースの背後にあり、実装は 1 つの結線ファイルで差し替えられます。「ハーネスとは何を抽象化する層なのか」を読み取る教材として有用です。

### Skill の扱い — 4 つ目の配布モデル

QM の Skills は**スコープが所有し、付与（grant）によって共有**されます。管理者の承認で組織全体へ昇格させることができ、**git リポジトリから skill pack としてインポート**することもできます。

[Skills 最新動向 7 節](../trends.md#7-skill-の発見配布更新)で扱った `npx skills`・`gh skill`・Agent Plugins が「配る」仕組みだとすれば、QM のそれは**組織の中で誰に見せるかを制御する**仕組みです。配布と権限を同じ軸で扱っている点が異なります。

### セキュリティポスチャ — 標準が空けた穴の埋め方

[Skill / Plugin のセキュリティ](skill-security.md)で述べるとおり、Agent Plugins 1.0.0 は信頼モデル・権限・サンドボックスを定義せず、**安全性の担保は各クライアントに委ねられています**。QM はその負担を実際に引き受けた実装例として読めます。

組織は次の 3 つから 1 つを選び、より狭いスコープはそれを**強める方向にのみ**変更できます。

| ポスチャ | 挙動 |
|---------|------|
| **Strict** | すべてのツール呼び出しで人間の承認を待つ（副作用のないターン終了 2 つを除く） |
| **Auto**（既定） | **出所ラベルの付いた外部データ**とツール結果を、モデルへ渡す前に分類器で選別する。選別を自前のプロキシへ向けることもできる |
| **Dangerous** | 内容の選別もツール呼び出し間の停止もしない |

注目すべきは、**再帰的削除や破壊的な SQL などに対する事前宣言のコマンドポリシーが、Dangerous を含むすべてのポスチャで適用される**点です。「最も緩い設定でも外せない下限」を持たせる設計は、Skill や Plugin を組織へ入れる際の考え方としても参考になります。

### 導入の前提と、成熟度についての但し書き

QM は**組織向けソフトであり、デスクトップアプリではありません**。運用者自身のクラウドアカウント、Postgres、そしてインフラを扱える担当者が前提になります。個人で試す類のものではない点に注意してください。

`SECURITY.md` は限界を率直に書いており、導入判断ではこちらのほうが重要です。

> It is early, experimental software: that design goal is not a promise that data cannot leak, a certification, or a substitute for a deployment-specific security review.

- **公開・マルチテナント向けの堅牢な境界ではない**と明記されている
- **悪意ある、または侵害された運用者からはデプロイを守らない**
- **組織管理者は権限を持つコンテンツ読み取り者**であり、単なるポリシー管理者ではない。管理者の閲覧はスコープに従い監査されるが、利用者の追加承認は要らない

最後の 1 点は、社内へ展開する際に事前に合意しておくべき性質です。

> 初期段階の OSS のため、構成・コマンド・要件は変わります。導入時は必ず [リポジトリ](https://github.com/yc-software/qm) の最新の記述を確認してください。

## Kiro Crew — 常駐して動き続けるハーネス

[Kiro Crew](https://kiro.dev/crew/) は、AWS が 2026-08-04 に Apache-2.0 で公開したハーネスです。Amazon 社内で使われていた仕組み（MeshClaw）を OSS として出したもので、製品ページの説明は次のとおりです。

> Kiro Crew is the persistent, open source development workspace that remembers your context, learns how you work, and coordinates across your unique tools and workflows.

QM が**組織のスコープと権限**を中心に据えるのに対し、Kiro Crew の軸は**対話が終わっても作業が終わらないこと**です。同じ「ソースを読める OSS ハーネス」でも、設計の出発点が違います。

### 層の関係 — セッションごとに Agent Backend を選ぶ

公開時の Kiro Crew は **Agent Client Protocol（ACP）** 経由で Kiro CLI を駆動する構成で、現在の製品 FAQ もこの経路を基本として説明しています。一方、Kiro Crew 0.6.0（2026-09-05）は **Agent Backend** の選択を Preview として追加しました。Developer Mode を有効にすると、Settings → Developer → Agent Backend で **Kiro CLI、Claude Code、Codex、KAS** から選べます。選択は新しいセッションにだけ適用され、既存セッションは開始時のバックエンドを保ちます。

| 層 | 担うもの |
|----|---------|
| ハーネス（Kiro Crew） | 永続セッション、メモリ、スケジュール、チャネルへの配送、セッション制御、監査 |
| Agent Backend | 実際のエージェントループ。Kiro CLI が基本経路で、Claude Code / Codex / KAS への切り替えは **Preview** |
| モデル・認証・利用枠 | 選択したバックエンド側の条件に従う。Kiro CLI 経路は Kiro アカウントとプランを使うが、代替バックエンドの認証・課金対応は Agent Backend ページに記載がないため、各バックエンドの現行情報を確認する |

Preview でも共通すると公式に明記されているのは、monitor loop、project change、follow-up card、conversation reset です。Kiro CLI 経路では既存の `.kiro` 設定（steering files・Skill・custom agent）を引き継げますが、**代替バックエンドが同じ設定を同じ意味で解釈するとは公式ページに書かれていません。** バックエンドを切り替える場合は、設定の継承を推測せず、小さなセッションで確認してください。

### 人がいない時間に動かすための部品

| 部品 | 内容 |
|------|------|
| 永続セッション | 並行する独立したセッションを持ち、常駐プロセスの再起動後も再開できる。過去のセッションを検索して文脈を引き継ぐ |
| スケジュール実行 | タイムゾーンを解釈する定期ジョブを、指定した面へ届ける |
| ハートビート監視 | 作業が終わるまで見張る。メッセージイベントや**認証済み webhook** にも反応する |
| 長時間タスク | タスク仕様を渡すと、手順の計画・実行・結果の検証・失敗時の再試行まで行う |
| メモリ | 好み・進行中の文脈・要約された履歴・持続的な教訓を保持し、**訂正や失敗が以降の挙動を変える** |

入口はデスクトップアプリ・Web ダッシュボード・CLI（`kirocrew`）に加えて、Slack・Discord・Teams などのチャネルがあります。**同じ実行環境へ別の面から入る**設計で、QM が Slack をプラグインとして扱うのと同じ考え方です。

**→ 「いつ起動するか」の設計は [ループエンジニアリング](loop-engineering.md#oss-側の起動条件--kiro-crew) を参照**

### セキュリティ — バックエンドごとの境界も確認する

Kiro CLI 経路では、Linux と macOS で `kiro-cli` を **namespace / Seatbelt による分離**の中で動かせます。強さは **standard / strict / off** から選びます。セキュリティイベントとツールの実行履歴は記録され、`kirocrew security events` / `audit` / `verify` で確認できます。

Agent Backend を変えると承認境界も変わります。公式の Preview ページは、Claude 側の設定ですでに事前承認されたツールは Crew の承認を迂回し、Codex にはサンドボックスが必要だと注意しています。無人実行へ使う前に、Crew 側とバックエンド側の両方で、ファイル書き込み・コマンド・ネットワークアクセスがどこで止まるかを確認してください。

QM が Strict / Auto / Dangerous という**渡す内容の選別**の強さを選ばせるのに対し、Kiro Crew は**プロセス分離**の強さを選ばせます。着眼点は違いますが、どちらも「既定でどこまで許すか」を運用者に決めさせる設計です。無人で回すほどこの既定値が効いてきます（[ループエンジニアリング](loop-engineering.md)）。

### 導入の前提 — OSS だが「自前で完結」ではない

- 本体は Apache-2.0 の OSS で、Crew 自体に別料金はない。**Kiro CLI 経路**では Kiro プランが必要で、エージェントの利用は Kiro アカウントの枠を消費する
- Kiro Crew 全体と個別機能の状態を分ける。本ガイドでは通常配布される Crew 本体を GA として扱うが、Kiro CLI 以外も選べる **Agent Backend は Preview**（2026-09-15 確認）
- 代替バックエンドの認証・利用枠を Kiro CLI 経路から推測しない。導入時は選択したバックエンドと Crew の両方の公式情報を確認する

QM が「自前のクラウド・Postgres・インフラ担当者」を前提にするのに対し、Kiro Crew は**手元のマシンで動かせる代わりに、選択したバックエンドのモデル提供・認証・利用枠に依存**します。同じ OSS ハーネスでも、組織へ入れるときに確認する項目はここまで違います。

> 導入手順・対応 OS の細目・コマンドは変わります。導入時は [リポジトリ](https://github.com/kirodotdev/KiroCrew) と [公式ドキュメント](https://kiro.dev/docs/crew/) を一次情報として確認してください。

## OpenAI Agents API — CodexハーネスをマネージドAPIで使う

[OpenAI Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview) は、Codexと同系統のハーネスを、自社アプリケーションからOpenAI管理のAPIとして利用する入口です。2026-09-10に **Public Beta** として公開されました。OpenAIがsession、orchestration、context compaction、recoveryを管理し、利用側はagentの構成、tools、実行環境、業務上の認可と承認を設計します。

### ハーネスと実行環境を分ける

Agents APIを使うことと、OpenAIのsandboxを使うことは同じではありません。ハーネスはOpenAIが管理しますが、コマンドやファイルを扱う**実行環境は別に選びます**。

| 層 | 担当 | 主な役割 |
|----|------|---------|
| **Harness** | OpenAI | model / tool loop、durable session、orchestration、context compaction、recovery、subagentの調整 |
| **Application server** | 利用側 | taskの投入、stream / webhookの受信、function toolの実行、利用者認可、業務上の承認 |
| **Environment** | 選択による | shell、コード実行、ファイル編集、artifact作成、network access |

Environmentは次の3通りです。

| `environment.type` | 実行場所 | 利用側の責任 |
|--------------------|---------|---------------|
| `none` | shellやworkspaceを持たない。remote MCPやfunction toolは利用できる | function toolの実行と結果返却。組み込みBash / apply patch、workspace file、executor MCPは使えない |
| `openai_hosted` | session用にOpenAIがsandboxを作成・管理する | packages、files、network access、secret、tool権限を設定し、出力を検証する |
| `self_hosted` | 自社環境、private network、独自softwareを使う | provisioning、接続、再接続、停止、永続化、実行中workの終了確認を管理する |

**環境を選べることは、sandboxや権限設計が不要という意味ではありません。** `self_hosted` では実行基盤のlife cycleを自分で持ち、`openai_hosted` でもnetwork、secret、files、toolの露出範囲を自分で決めます。

### Codex、Agents API、Agents SDKを混同しない

| 入口 | 何を提供するか | 選ぶ場面 |
|------|---------------|---------|
| **CodexのCLI / IDE / Desktop / Cloud** | 開発者が直接使うCodex製品と作業UI | 人がrepositoryやtaskを対話的・非同期に進める |
| **Agents API** | OpenAI管理のCodexハーネス、durable session、event、artifact、選択可能なenvironment | 自社サービスへ長時間agentをAPIとして組み込む |
| **Agents SDK** | agent、tool、handoff、guardrail、trace等をコードで組み立てるライブラリ | orchestrationをアプリケーションコード側で設計する |
| **Codex SDK / app server** | Codexプロセスをプログラムやクライアントから制御する入口 | ローカルまたは自社管理のCodexを組み込む。app serverはAgents API互換ではない |

Agents APIは、Agents SDKのホスティング版という単純な関係ではありません。APIはOpenAI管理のCodexハーネスとdurable sessionを提供し、SDKはアプリケーション内でagent workflowを構成するための部品です。

### tools、multi-agent、artifact

Agentにはfunction、remote MCP、Plugin等のtoolsを設定できます。多数のtoolsを常時contextへ入れないためのtool searchや、tool呼び出しをコード側でまとめるprogrammatic tool callingも利用できます。multi-agentを有効にするとsubagentを作成・待機できますが、**複数化するだけで速く、安く、正確になるわけではありません**。分割と統合の責任は[マルチエージェントを使う境界線](multi-agent.md)に従って設計します。

hosted sessionの完了turnから公開したfileはartifactとして取得できます。途中のworkspace fileと、完了後に配布するimmutable artifactを区別し、必要な成果物が公開されたことを終了条件として検証します。

### 費用と導入前の確認

Agents API自体を「定額のCodex利用枠」と見なさないでください。公式ドキュメントでは、選択したmodelのAPI料金、OpenAI toolの料金、OpenAI-hosted sandboxのcontainer料金がそれぞれ発生すると説明されています。価格を本文へ固定せず、導入時に[公式Pricing](https://developers.openai.com/api/docs/pricing)を確認します。

- Public BetaのAPI変更と、利用可能なmodel / tool / environmentを再確認する。
- sessionの保存対象、retention、削除、trace / artifactに含まれる情報を確認する。
- network egress、MCP、function tool、secret、workspace fileの最小権限を決める。
- irreversibleな操作はtool側で止め、利用者の承認とaudit logを用意する。
- self-hosted environmentではreconnection、shutdown、重複実行、途中成果物の回収をテストする。

## 定義の可搬性と実行コンテキストを分ける

VS Code 1.138 の Agent Host は、Agent Host Protocol（AHP）を基盤に agent harness を専用 process で動かし、同じ session へ複数 window から接続できるようにしました。対応する Dev Container 構成と Docker があれば、ローカル machine ではなく container の toolchain / dependencies で session を動かせます（段階的ロールアウト）。

同じ session を ChatGPT app から VS Code へ継続できても、移動先では VS Code built-in / extension / MCP tools が使えるようになります。また Automations の `.automation.md` が運ぶのは name / prompt / schedule などの portable definition だけで、workspace、provider、model、permissions、enabled state、run history は運びません。

つまり、**定義が可搬であること、会話が継続すること、同じ実行環境・権限で動くことは別**です。handoff / import / Dev Container 化のたびに、tool surface、workspace、secret、network、permission を実行先で再評価します。

## ハーネスを意識する理由

- **ループの土台になる**: 無人で回すループは、ハーネスが用意した権限・サンドボックス・観測の範囲でしか安全にならない（[ループエンジニアリング](loop-engineering.md)）。
- **モデルの性能だけでは不十分**: 同じモデルでも、ハーネス設計の差が出力品質・コスト・レイテンシを大きく左右する。
- **障害点の特定**: 問題が「モデルの判断ミス」か「ツール呼び出しの失敗」かを切り分けるには、ハーネスの構造を理解する必要がある。
- **再利用と標準化**: スキルや MCP サーバーも、ハーネスに組み込まれる部品として設計すると再利用しやすい。
- **安全性の実装先**: 標準が定めていない権限・承認・サンドボックスは、結局ハーネス側で決まる（[Skill / Plugin のセキュリティ](skill-security.md)）。組織へ展開するなら、モデルやツールの選定と同じ比重でハーネスの既定値を確認する。

> 詳しくは [なぜ今、AI に「ハーネス」が必要なのか（ギークフジワラ）](https://www.geekfujiwara.com/tech/powerplatform/8591/) を参照してください。

## 動かした後に何が見えるか — OpenTelemetry GenAI Semantic Conventions

ハーネスがツール呼び出し・ループ・エラー処理を引き受けるとして、**動かした後に何が起きたかを外から見る**仕組みも必要になります。ここでベンダー横断の共通スキーマとして広がっているのが OpenTelemetry の **GenAI semantic conventions** です。モデル呼び出し・ツール呼び出し・トークン交換を標準化された属性（`gen_ai.request.model`・`gen_ai.usage.input_tokens` / `output_tokens`・`gen_ai.response.finish_reasons` など）で記録し、既定ではメタデータのみを出力して機微な内容（プロンプト本文やツール引数）を含めません。トレースは `invoke_agent`（エージェント全体）を親に、モデル呼び出しが `chat`、ツール実行が `execute_tool` の子スパンになる階層構造を取ります。

主要なコーディングツールの対応状況は次のとおりです（いずれもオプトインで、既定は無効）。

| ツール | 対応シグナル | GenAI semantic conventions |
|-------|-------------|---------------------------|
| Claude Code | メトリクス・イベント（ログ）が正式対応、トレースはベータ（`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`） | 明記あり（`gen_ai.*` 属性を `claude_code.llm_request` 等のスパンに付与） |
| Codex CLI | メトリクス・ログ（イベント）。`config.toml` の `[otel]` で設定 | 公式ドキュメントに明記なし |
| VS Code Copilot Chat | トレース・メトリクス・イベント | 明記あり（`gen_ai.*` に加え `github.copilot.*` の拡張名前空間） |
| GitHub Copilot app | エージェント session のトレース、モデル・tool 呼び出し、メトリクス・イベント。Enterprise managed settings の `telemetry` で有効化 | app 向け発表は属性名まで明記していない。導入時に実際の span を確認 |

> **対応の深さはツールごとに違い、変化も速い領域です。** 上表は各公式ドキュメントの確認日（既存3ツール: 2026-09-12、Copilot app: 2026-09-23）時点のもので、導入時は必ず最新の記述を確認してください。

GitHub は 2026-09-22 に [Copilot app の OTel 対応](https://github.blog/changelog/2026-09-22-opentelemetry-in-the-github-copilot-app/)を発表しました。Enterprise 管理者が `managed-settings.json` の `telemetry` で export を有効にして OTLP endpoint を指定します。[GitHub の OTel 概念文書](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry)では、session のモデル・tool 呼び出しをつなぐ trace、token 等の metric、個別 action の event を区別しています。prompt・response・tool 引数の本文は既定で除外されます。`captureContent` を有効にする場合は、コードやファイル内容が監視基盤へ送られるため、送信先と保存範囲を確認します。

**文書の対象表記に差があります（2026-09-23 確認）。** 9 月 22 日の発表は Copilot app 対応を明記しますが、[enterprise-managed settings の `telemetry` リファレンス](https://docs.github.com/en/copilot/reference/enterprise-administrators/enterprise-managed-settings#telemetry)は対応先をまだ Copilot CLI / VS Code と記載しています。app へ展開する前に対象バージョンと有効な設定を確認し、collector に実際の trace が届くことを試してください。

Claude Code 2.1.274 では `claude_code.managed_settings_resolved` OTel event が追加されました。managed-settings の source と policy helper の状態を確認でき、`OTEL_LOG_MANAGED_SETTINGS=1` を設定すると**値を redaction した設定と digest**も記録します。設定値そのものを露出させず、「どの管理設定が解決されたか」を監査するための event です。

この「動かした後に何が見えるか」は、[Skill / Plugin のセキュリティ 5 節「統制が効く 3 つの段階」](skill-security.md#5-統制が効く-3-つの段階)の**実行後（監査）**と直結します。あちらが「セッションのトランスクリプトを取得する」という組織向け機能（Compliance API）を扱うのに対し、ここでの OpenTelemetry は**ベンダー中立の計測データ**（メトリクス・ログ・トレース）を自分たちの監視基盤（OTLP 対応バックエンド）へ流す仕組みです。両者は排他ではなく、組織で使える統制の手段が違う層として併存します。

### OTLP とデータの意味を分ける

**OpenTelemetryは観測のためのAPI・SDK・データモデルを含む仕組みで、OTLPはそのデータを運ぶプロトコルです。** OTLPを使っているだけでは、データがGenAI semantic conventionsに従う実行トレースなのか、ベンダー独自の日次集計なのかは決まりません。名前空間、signal（trace / metric / log）、集計粒度を確認してください。

2026-09-01、Kiroは利用者別のusage metricsをOpenTelemetry互換のcollectorへ送るaccount-level exportを追加しました。これは `invoke_agent` や `execute_tool` のspanではなく、`kiro.daily.*` 名前空間の**単調増加するOTLP Sumメトリクス**です。既存のCSV reportと同じ日次集計を別経路で送り、両方を独立して有効化できます。

| 観測対象 | 転送・取得方式 | データ粒度 | 答える問い | 頻度・権限 |
|---------|---------------|-----------|-----------|-----------|
| **GenAI実行トレース / semantic conventions** | 各ツールのOTel exporterからcollectorへ送る。OTLP対応は実装ごとに確認 | 1回のagent・model・tool実行のspan / event / metric、token、latency | どのmodel・toolが動き、どこで失敗・遅延したか | 送信頻度・設定権限はツールごとに異なる |
| **Copilot app の実行トレース** | Enterprise managed settings の `telemetry` で collector へ送る | session と model / tool 呼び出しの trace、metrics、events。本文は既定で除外 | どの操作・model callで失敗や遅延が起きたか | Enterprise 管理者が設定。app での有効な設定と到着を確認 |
| **Kiro user activity export** | Kiroのserverから `OTLP/gRPC` または `OTLP/HTTP`（protobuf）でcollectorへ送る | 利用者・client type・model別の日次集計。credits、overage credits、messages、conversations、model別message数 | 誰がどのclient / modelを使い、adoption・engagement・credit consumptionがどう変わったか | 毎日02:00 UTC。account administratorがKiro consoleで設定し、Secrets Managerのsecret、KMS key、公開到達可能なOTLP endpointが必要 |
| **Copilot usage metrics API** | GitHubのREST API / NDJSON reportから取得（OTLPではない） | Enterprise / Organization / 利用者別の1日・28日集計。専用VS Code Agents windowのuser、session、message数 | 組織内で専用Agents windowを何人が、何session / message使ったか | report単位。owner / billing managerまたは `View Copilot Metrics` 権限と、Copilot usage metrics policyの有効化が必要 |

Kiroの機能は**提供元: Official / Kiro、状態: GA、確認日: 2026-09-16**です。公式ドキュメントでは、個人の開発環境ではなくadministratorがaccount単位で設定し、`kiro.daily.credits`などを1日1回送る機能として説明されています。送信要求がcollectorに受理されても後段でdatapointが拒否される可能性があるため、宛先で到着を確認します。

Copilotの専用VS Code Agents指標は2026-09-11に一般提供され、`daily_active_vscode_agent_users`、`totals_by_vscode_agent`、利用者別の `used_vscode_agent` を1日 / 28日のreportへ追加します。データがない場合は省略または `null` になり得ます。対象は**専用のVS Code Agents windowだけ**で、editor-window Agent Modeや汎用の集計へ足し合わせません。

## 宣言でリモートのエージェントを管理する — `ant apply`

ここまでは「ハーネスをどう作るか・どう動かすか」でした。**動かすエージェントそのものの構成を、コードとしてレビュー・CI に乗せる**仕組みも登場しています。Anthropic の `ant apply`（`ant` CLI 1.30.0 以降、2026-09-03 のリリースノートで案内）は、Claude API 上の Agent・Environment・Skill・Memory Store・Deployment を、リポジトリ内のファイルから作成・更新します。

> **層を取り違えないでください。** これは Claude Code へ Plugin を入れる機能ではなく、**Claude Platform / Managed Agents 側のリモートリソース**を管理する仕組みです。Agent Plugin（クライアントへの配布）・APM（ローカル依存の管理）との違いは [Skills 最新動向 7-5 節](../trends.md#7-5-ant-apply--api-上のリソースを宣言で管理する) に整理しています。

### 何が「リソースのグラフ」になるか

リソースは**相対パスで互いを参照**します。API が他リソースの ID を期待する箇所に、そのリソースのファイルへの相対パスを書くと、`ant apply` が依存順に作成して実際の ID を埋めます。エージェントが Skill を参照し、コーディネーターが配下のエージェントを参照し、Deployment が agent / environment / memory store を参照する、という構成をファイルだけで表現できます。

GitHub URL（`https://github.com/<owner>/<repo>/tree/<branch>/<dir>`）で参照した Skill は、**解決済みのコミットに固定**されます。`--upgrade` を渡したときだけ再解決されます。

### plan と承認

対話的なターミナルでは、`ant apply` は**適用前に plan を表示して承認を求めます**。`d`（details）で、新規リソースのフィールドや更新の差分をフィールド単位で確認できます。

### `claude-lock.json` は生成物ではない

`claude-lock.json` を「ビルド成果物」と捉えると運用を誤ります。これは**どのファイルがどのリモートリソースなのか**（resource identity）と、**外部で変更されていないか**（drift）を管理する記録です。

| 記録される内容 | 用途 |
|---------------|------|
| `origin`（base URL・組織 ID・ワークスペース ID） | 認証情報が別の組織／ワークスペースに解決される場合、`ant apply` は**拒否**する |
| リソース ID | 次回の実行が、新規作成ではなく同じリソースの更新になる |
| `hash` / `remote_hash` | 最後に送った内容と API が返した内容の指紋。ファイルの編集と、**これらのファイルの外で加えられた変更**の両方を検出する |

**コミットしてください。** 手元と CI の後続実行が同じリソースを指すための唯一の手がかりです。

### drift と破壊的な操作

Console などファイルの外側でリソースが編集・アーカイブ・削除されていた場合、plan は `This plan cannot be applied:` と理由を表示し、**`refusing to apply` で終了します**。これが既定の安全側の挙動です。

| フラグ | 用途 | 注意 |
|-------|------|------|
| `--dry-run` | plan を表示して終了。lockfile も書かない | plan がブロックされていても**終了コードは 0** |
| `--yes` | 確認なしで適用。ターミナルがない環境では必須 | — |
| `--force` | 外部で変更・アーカイブ・削除されたリソースにも適用する | **外部の変更を上書きする**、または置き換えを作成する |
| `--prune` | lockfile にあるが、もうファイルで宣言されていないリソースを削除する | アーカイブ（Skill は削除）。**ファイル名の変更は「新規宣言 + 旧リソースの残存」**になるため、prune するまで両方残る |
| `--upgrade` | GitHub URL 参照の Skill を再解決する | 固定していたコミットが動く |

`--force` と `--prune` は破壊的になり得ます。通常のフローとは分けて扱ってください。

なお `ant apply` は、Console や `ant beta:agents create` で作成した既存リソースを**引き取れません**（lockfile にあるものだけが管理対象で、既存エージェントと同じ内容のファイルを適用すると 2 つ目が作られます）。Console の **Export as code** でダウンロードした場合は `claude-lock.json` が同梱されるため、そちらは更新になります。

### CI に載せるときの注意点

ターミナルがない環境では、plan を表示して停止します。公式ドキュメントが示す運用は次のとおりです。

- **PR では `ant apply --dry-run .`** を実行し、レビュアーに plan を見せる（情報提供のみ。plan がブロックされていても終了コードは 0）
- **既定ブランチへの merge 後に `ant apply --yes .`** を実行する。ディレクトリを指定すること — 引数なしの `ant apply --yes` は lockfile が既に追跡しているファイルだけを対象にし、**新規追加ファイルを取りこぼす**
- **途中で失敗した場合も、ジョブの最後に `claude-lock.json` をコミットする**。部分適用でも、作成済みのリソースは記録されているため
- **同時に 1 つだけ実行する**。lockfile はロックされない
- 認証は保存した API キーではなく [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) を使う

**人間の責任境界**: plan の承認（対話時）とレビュー（`--dry-run` の出力）が、変更を止められる唯一の地点です。`--yes` で自動適用する経路には、その前段に PR レビューを置いてください。

## 実行中の権限判定と介入 — Claude Managed Agents

`ant apply` が「どの構成をデプロイするか」を止める仕組みなら、Claude Platform の **Managed Agents permission policies**（Beta）は、デプロイしたエージェントが**実行中に個々のツールを呼べるか**を判定する仕組みです。Managed Agents API では `anthropic-beta: managed-agents-2026-04-01` ヘッダーが必要です。

| ポリシー | 動作 | 運用上の意味 |
|---------|------|-------------|
| `always_allow` | ツール呼び出しを許可する | 低リスクで自動実行してよいツールに限定する |
| `always_ask` | 呼び出しを保留し、応答を待つ | 人の確認が必須の操作に使う |
| `auto` | ツール、入力、セッションの文脈から allow / deny / ask を判定する | 自律性を上げられるが、人の確認を保証しない |

`auto` が deny と判定した呼び出しは上書きできません。ask になった呼び出しはセッションを一時停止し、応答を待ちます。判断の根拠はイベントの `evaluated_permission` と通常そこに含まれる `evaluation` で監査できます。必要なら `ant beta:sessions connect` で進行中のセッションを追跡し、指示を追加し、承認要求へ応答できます。

適用範囲にも境界があります。ポリシーが扱うのは Managed Agents が提供するツールと MCP ツールです。API 利用者が定義した **custom tools には適用されない**ため、認可、確認画面、監査ログをアプリ側で用意します。また、これはサーバー上の Managed Agents の機能で、Claude Code のローカル権限モードではありません。

**→ GitHub Copilot の組織ポリシーとの比較と、導入前から実行後までの統制は [Skill / Plugin のセキュリティ](skill-security.md#managed-agents-はツール呼び出しごとに判定する) を参照**

## ループとの関係

ハーネスの 1 つ上の階には、エージェントを目標へ向けて何度も回す **ループ** の設計があります。ハーネスが「エージェントが動く環境」を決めるのに対し、ループは「その環境で何を、いつまで繰り返すか」を決めます。両者は独立ではありません。**ループはハーネスの上で回るため、ハーネスが弱ければループはその弱点を繰り返し踏み、誤りを増幅します**。無人で回す前に、権限・サンドボックス・観測がハーネス側で揃っているかを先に確認してください。

**→ ループの構成要素・停止条件の作り方・落とし穴は [ループエンジニアリング](loop-engineering.md) を参照**

---

## 関連ドキュメント

- [ループエンジニアリング](loop-engineering.md) — ハーネスの 1 つ上の階。エージェントを目標へ向けて回す反復サイクルの設計
- [Skills 最新動向](../trends.md) — 本ページの要約と、その他のテーマの動向
- [オントロジー](ontology.md) — ハーネス越しにエージェントへ渡す「業務の意味」の定義
- [Skill / Plugin のセキュリティ](skill-security.md) — 標準が定義していない権限・承認・サンドボックスをどう埋めるか
- [Skill / エージェントの評価（evals）](evals.md) — 同じ「ハーネス」という語で呼ばれる**評価用ハーネス**（実行結果を採点する測定用の足場）との違いを整理
- [エージェントに外部操作を与える手段の選び方](tool-selection.md) — ハーネスが管理するツール呼び出しを、API・connector・MCP・CLI・Computer Use のどれで実装するかの判断基準
- [MCP と A2A — 役割の違いと併用方法](agent-protocols.md) — ハーネスの上位にある「エージェントとツール」（MCP）・「エージェントとエージェント」（A2A）の層の違い
- [AIエージェントのID・認可・委任権限](agent-identity.md) — ハーネスが引き受ける「認証・スコープ・権限」を、エージェント固有 ID・委任・control plane の観点で詳しく扱う
- [マルチエージェントを使う境界線](multi-agent.md) — 複数のエージェントを組織で運用する前に、そもそも複数体にすべきかを判断する
- [Claude Code のカスタマイズ機能](../claude-code/basics.md) ／ [Codex ガイド](../codex/README.md) — ハーネスから見れば差し替え可能な「コーディングツール」層の解説
- [コーディングエージェントの選び方](coding-agents.md) — その「コーディングツール」層に何があるかの比較（Claude Code / Codex / Qwen Code / OpenCode / Bionic）
- [長時間タスクの信頼性設計](agent-reliability.md) — ハーネスが引き受ける状態管理・エラー処理を、checkpoint・再開・冪等性の観点で詳しく扱う
- [Codex ガイド](../codex/README.md#codexを製品へ組み込む入口を分ける) — Codex製品、Agents API、Codex SDK / app serverの入口をCodex利用者向けに整理

## 参考リンク

- [なぜ今、AI に「ハーネス」が必要なのか](https://www.geekfujiwara.com/tech/powerplatform/8591/) — ハーネスの概念と Microsoft Copilot Studio での実装例（ギークフジワラ）
- [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) — Mitchell Hashimoto によるハーネスエンジニアリングの定義（一次情報）
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI の実証報告（公式）
- [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview) — managed Codex harness、durable session、料金の考え方（OpenAI公式・Public Beta）
- [Agents API architecture](https://developers.openai.com/api/docs/guides/agents-api/architecture) — harness、application server、environmentの責任分界（OpenAI公式）
- [OpenAI API changelog](https://developers.openai.com/api/docs/changelog) — 2026-09-10のPublic Beta公開（OpenAI公式）
- [Agents SDK overview](https://developers.openai.com/api/docs/guides/agents) — agent workflowをコードで構成するSDK（OpenAI公式）
- [yc-software/qm](https://github.com/yc-software/qm) — QM のリポジトリと README（公式）
- [QM の SECURITY.md](https://github.com/yc-software/qm/blob/main/SECURITY.md) — 脅威モデル・運用者の前提・既知の限界（公式）
- [Kiro Crew](https://kiro.dev/crew/) — 製品ページと FAQ（前提となるプラン・対応 OS。公式）
- [Introducing Kiro Crew](https://kiro.dev/blog/introducing-kiro-crew/) — 公開時の発表（公式・2026-08-04）
- [kirodotdev/KiroCrew](https://github.com/kirodotdev/KiroCrew) — リポジトリと README（公式・Apache-2.0）
- [Kiro Crew ドキュメント](https://kiro.dev/docs/crew/) — 機能・設定・セキュリティの一次情報（公式）
- [Kiro Crew 0.6.0 changelog](https://kiro.dev/changelog/crew/0-6/) — Agent Backend 選択の追加（`提供元`: Official / Kiro ｜ `状態`: —、2026-09-05）
- [Agent backends](https://kiro.dev/docs/crew/features/agent-backends/) — Kiro CLI / Claude Code / Codex / KAS、セッションへの適用範囲、セキュリティ上の注意（`提供元`: Official / Kiro ｜ `状態`: Preview）
- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/) — GenAI semantic conventions の解説（OpenTelemetry 公式）
- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage) — OTel メトリクス・イベント・トレース（ベータ）の設定（公式）
- [Codex CLI Advanced Configuration — `[otel]`](https://learn.chatgpt.com/docs/config-file/config-advanced) — Codex の OTel 設定（公式）
- [Monitor agent usage with OpenTelemetry](https://code.visualstudio.com/docs/agents/guides/monitoring-agents) — VS Code Copilot Chat の OTel 対応（公式）
- [VS Code 1.138 release notes](https://code.visualstudio.com/updates/v1_138) — Agent Host、Dev Container、Codex session handoff と tool surface（Microsoft 公式・2026-09-16）
- [Claude Code v2.1.274](https://github.com/anthropics/claude-code/releases/tag/v2.1.274) — managed settings OTel event と MCP startup wait（Anthropic 公式・2026-09-17）
- [Export user activity with OpenTelemetry](https://kiro.dev/docs/enterprise/monitor-and-track/user-activity/opentelemetry/) — account-levelの日次usage metrics、OTLP、設定権限、export時刻、metric定義（`提供元`: Official / Kiro ｜ `状態`: GA、2026-09-16確認）
- [Kiro changelog — Export Kiro usage metrics to OpenTelemetry](https://kiro.dev/changelog/) — 機能公開の一次情報（`提供元`: Official / Kiro ｜ `状態`: GA、2026-09-01）
- [Add VS Code Agents to Copilot usage metrics](https://github.blog/changelog/2026-09-11-add-vs-code-agents-to-copilot-usage-metrics/) — 専用 Agents ウィンドウの利用指標（GitHub 公式・GA）
- [Copilot usage metrics reference](https://docs.github.com/en/copilot/reference/copilot-usage-metrics/copilot-usage-metrics) — report の種類、field、権限（GitHub 公式）
- [OpenTelemetry in the GitHub Copilot app](https://github.blog/changelog/2026-09-22-opentelemetry-in-the-github-copilot-app/) — app への管理設定からのOTel対応（GitHub公式・2026-09-22）
- [OpenTelemetry for agent monitoring](https://docs.github.com/en/copilot/concepts/enterprise/opentelemetry) — trace / metric / eventと本文の既定除外（GitHub公式）
- [Manage resources as code with `ant apply`](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply) — リソースの種類・`claude-lock.json`・フラグ・CI 運用の一次情報（Anthropic 公式）
- [Claude Platform リリースノート](https://platform.claude.com/docs/en/release-notes/overview) — `ant` CLI 1.30.0 / `ant apply` の公開（2026-09-03、公式）
- [Managed Agents permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies) — `always_allow` / `always_ask` / `auto` とイベント形式（Anthropic 公式・Beta）
- [Connect to a running session](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/sessions-connect) — `ant beta:sessions connect` による追跡・介入（Anthropic 公式）
