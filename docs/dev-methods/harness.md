# AI エージェントの実行基盤（ハーネス）

> **対象ツール**: ツール横断 ｜ **実行環境**: CLI / Cloud ｜ **対象読者**: エンジニア・プラットフォーム担当 ｜ **最終更新**: 2026-09-09

> エージェントは「モデル」だけでは動きません。ツール呼び出し・状態管理・ループ制御・権限といった裏側の仕組みを **ハーネス（harness）** と呼びます。このページは概念、実装例（Microsoft Copilot Studio / QM / Kiro Crew）、そして「なぜ設計を意識するのか」を 1 か所にまとめた解説です。最近の動きだけを追いたい場合は [Skills 最新動向 10 節](../trends.md#10-aiエージェントの実行基盤ハーネス) を参照してください。

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

## 実装を見る 3 つの入口

ハーネスは概念だけでは掴みにくいため、性格の異なる実装を 3 つ並べます。

| | Microsoft Copilot Studio | QM（Y Combinator） | Kiro Crew（AWS） |
|---|---|---|---|
| 形態 | GUI・ローコードで構成する商用プラットフォーム | ソースを読める OSS（MIT） | ソースを読める OSS（Apache-2.0）＋公式ビルドの配布 |
| 想定利用者 | 業務担当者・開発者 | 組織のプラットフォームエンジニア | 個人・チームの開発者 |
| 見えるもの | 設計の**考え方**を GUI 上で追える | 設計の**実装**をコードで追える | **常駐して動き続ける**前提の設計を実装で追える |
| 重心 | 業務フローの構成 | 組織のスコープと権限 | セッションをまたぐ継続と起動条件 |
| `提供元` / `状態` | Official（Microsoft） / GA | Official（Y Combinator） / **Experimental** | Official（AWS） / GA |

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

### 層の関係 — Kiro CLI を下敷きにする

Kiro Crew は **Agent Client Protocol（ACP）** 経由で `kiro-cli` を駆動します。QM が Claude Code・Codex・OpenCode・Pi を差し替え可能な部品として扱ったのと同じ構図で、こちらは下位に自社の CLI を固定した形です。

| 層 | 担うもの |
|----|---------|
| ハーネス（Kiro Crew） | 永続セッション、メモリ、スケジュール、チャネルへの配送、サンドボックス、監査 |
| コーディングツール（`kiro-cli`） | 実際のエージェントループ |
| モデル | 推論（Kiro アカウントのサインインを使う） |

`.kiro` 配下の steering files・カスタムエージェント・Skill は**そのまま引き継がれます**。すでに Kiro を使っているなら、定義を書き直さずに常駐側へ持ち上げられます。

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

### セキュリティ — 分離の強さを選ぶ

Linux と macOS では `kiro-cli` を **namespace / Seatbelt による分離**の中で動かせます。強さは **standard / strict / off** から選びます。セキュリティイベントとツールの実行履歴は記録され、`kirocrew security events` / `audit` / `verify` で確認できます。

QM が Strict / Auto / Dangerous という**渡す内容の選別**の強さを選ばせるのに対し、Kiro Crew は**プロセス分離**の強さを選ばせます。着眼点は違いますが、どちらも「既定でどこまで許すか」を運用者に決めさせる設計です。無人で回すほどこの既定値が効いてきます（[ループエンジニアリング](loop-engineering.md)）。

### 導入の前提 — OSS だが「自前で完結」ではない

- 本体は Apache-2.0 の OSS で追加の費用はかからないが、**動かすには Kiro のプランが必要**。エージェントの利用は Kiro アカウントの枠を消費する
- Kiro Crew 自体はアカウントの仕組みを持たず、モデルアクセスは `kiro-cli` のサインインに委ねられる
- 公式の記述に Preview / Beta の表記はなく、既定の更新チャネルも安定版のため、本ガイドでは `状態`: GA として扱う（チャネルの構成は変わるため、[公式ドキュメント](https://kiro.dev/docs/crew/)を参照）

QM が「自前のクラウド・Postgres・インフラ担当者」を前提にするのに対し、Kiro Crew は**手元のマシンで動かせる代わりに、モデルの提供をベンダーに依存**します。同じ OSS ハーネスでも、組織へ入れるときに確認する項目はここまで違います。

> 導入手順・対応 OS の細目・コマンドは変わります。導入時は [リポジトリ](https://github.com/kirodotdev/KiroCrew) と [公式ドキュメント](https://kiro.dev/docs/crew/) を一次情報として確認してください。

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

> **対応の深さはツールごとに違い、変化も速い領域です。** 上表は各公式ドキュメントの確認日（2026-09-07）時点のもので、導入時は必ず最新の記述を確認してください。

この「動かした後に何が見えるか」は、[Skill / Plugin のセキュリティ 5 節「統制が効く 3 つの段階」](skill-security.md#5-統制が効く-3-つの段階)の**実行後（監査）**と直結します。あちらが「セッションのトランスクリプトを取得する」という組織向け機能（Compliance API）を扱うのに対し、ここでの OpenTelemetry は**ベンダー中立の計測データ**（メトリクス・ログ・トレース）を自分たちの監視基盤（OTLP 対応バックエンド）へ流す仕組みです。両者は排他ではなく、組織で使える統制の手段が違う層として併存します。

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

## 参考リンク

- [なぜ今、AI に「ハーネス」が必要なのか](https://www.geekfujiwara.com/tech/powerplatform/8591/) — ハーネスの概念と Microsoft Copilot Studio での実装例（ギークフジワラ）
- [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) — Mitchell Hashimoto によるハーネスエンジニアリングの定義（一次情報）
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI の実証報告（公式）
- [yc-software/qm](https://github.com/yc-software/qm) — QM のリポジトリと README（公式）
- [QM の SECURITY.md](https://github.com/yc-software/qm/blob/main/SECURITY.md) — 脅威モデル・運用者の前提・既知の限界（公式）
- [Kiro Crew](https://kiro.dev/crew/) — 製品ページと FAQ（前提となるプラン・対応 OS。公式）
- [Introducing Kiro Crew](https://kiro.dev/blog/introducing-kiro-crew/) — 公開時の発表（公式・2026-08-04）
- [kirodotdev/KiroCrew](https://github.com/kirodotdev/KiroCrew) — リポジトリと README（公式・Apache-2.0）
- [Kiro Crew ドキュメント](https://kiro.dev/docs/crew/) — 機能・設定・セキュリティの一次情報（公式）
- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/) — GenAI semantic conventions の解説（OpenTelemetry 公式）
- [Claude Code Monitoring](https://code.claude.com/docs/en/monitoring-usage) — OTel メトリクス・イベント・トレース（ベータ）の設定（公式）
- [Codex CLI Advanced Configuration — `[otel]`](https://learn.chatgpt.com/docs/config-file/config-advanced) — Codex の OTel 設定（公式）
- [Monitor agent usage with OpenTelemetry](https://code.visualstudio.com/docs/agents/guides/monitoring-agents) — VS Code Copilot Chat の OTel 対応（公式）
- [Manage resources as code with `ant apply`](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/apply) — リソースの種類・`claude-lock.json`・フラグ・CI 運用の一次情報（Anthropic 公式）
- [Claude Platform リリースノート](https://platform.claude.com/docs/en/release-notes/overview) — `ant` CLI 1.30.0 / `ant apply` の公開（2026-09-03、公式）

