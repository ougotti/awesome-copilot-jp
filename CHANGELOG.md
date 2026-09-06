# 更新履歴

本ガイドの主な更新を時系列で記録します。upstream の新規スキル検出への対応と、ガイド本体の構成変更・解説追加をここにまとめます。

## 2026-09

- **2026-09-06** trends.md に A2A の Agentic AI Foundation 合流（2026-08-17）を反映（#139）
  - **[Skills 最新動向](docs/trends.md) 13 節に「エージェント間プロトコルの統治の集約」を追加** — A2A（Google 開発）が、MCP・goose・AGENTS.md を創設プロジェクトとする AAIF（Agentic AI Foundation、Linux Foundation 傘下、2025-12-09 発足）に hosted project として合流した事実を追加。**MCP はエージェントとツールの接続、A2A はエージェントとエージェントの連携**という役割の違いを、AAIF 自身の整理に沿って書いた
  - **一次情報で裏取り** — issue 作成時点でブロックされていた `linuxfoundation.org`・`aaif.io` が今回は取得できた。AAIF 設立の公式プレスリリース（2025-12-09）と、A2A 合流を発表した AAIF 自身のブログ記事（`aaif.io/blog/a2a-joins-aaif`、2026-08-17 付、AAIF CTO と Google Cloud VP の引用あり）の両方を取得して確認した。二次情報（Forbes・Axios 等）は日付の裏取りにのみ使い、本文の根拠には一次情報を用いた
  - **数字は本文に書いていない**（CONTRIBUTING の「変化しやすい情報」）。「150 組織以上」は書かず、最新状況を確認できる `aaif.io/projects/agent2agent` へのリンクに置き換えた
  - **ロードマップと確定した組織変更を区別した** — 13 節が既に「2026-08-22 の MCP ロードマップは方向性の表明であって確定仕様ではない」と書いている扱いに揃え、A2A の AAIF 合流は**既に起きた組織上の事実**として書いた
  - **読者の判断材料を明記** — 「いま何かを変える必要があるか」に対し、A2A・MCP いずれも API に破壊的変更はなく、A2A を使っていない読者は対応不要である旨を書いた
  - **7-2 節から接続** — Agent Finder / ARD の「Catalog に A2A エージェントも含められる」という既存記述から 13 節へのリンクを追加した

- **2026-09-05** 導入経路の比較に APM（Agent Package Manager）を追加（#144）
  - **[Skills 最新動向](docs/trends.md) 7 節に「7-4. APM — 宣言でチームの環境を再現する」を新設** — `apm.yml` に依存を宣言して `apm install` で各エージェントへ展開する方式。既存 3 つとの決定的な違いを**「命令的か宣言的か」**と定め、比較表を 4 列へ拡張して「方式」「マニフェスト」の 2 行を先頭に置いた。「使い分けの目安」にも「チームの環境を再現可能にする」→ APM の行を追加
  - **提供元ラベルは断定せず、事実を併記した** — issue で最も慎重に決めるべき点とされていた箇所。**Microsoft 側の事実**（`microsoft` org 配下・LICENSE の著作権表記が Microsoft Corporation・SECURITY.md が Microsoft 標準・配布が `aka.ms` と `microsoft/*` チャネル）と、**コミュニティ側の事実**（README 自身が「open-source, community-driven」と名乗る・Maintainer は個人 2 名でうち 1 名は Microsoft 以外の所属）の両方を並べ、Microsoft の製品として提供・サポートされる旨の記述は見当たらなかったことを明記。組織導入時はラベルではなくリポジトリの実態で判断するよう促した
  - **`npx skills` の提供元表記に注記を追加** — CLI の提供元が Vercel であることは変わらないが、`google/skills`・`aws/agent-toolkit-for-aws`・`microsoft/azure-skills` の README がいずれも `npx skills add` を導入手順として案内しており、**発見ポータルであると同時にベンダー公式スキルの導入経路にもなっている**実態を書いた（確認日 2026-09-05）
  - **[skills.sh ガイド](docs/dev-methods/skills-sh.md) の冒頭の位置づけを更新** — 同じ趣旨を 1 段落で追記し、宣言的に再現したい場合の選択肢として APM へリンク
  - **バージョン番号と対応ハーネス数は本文に書いていない**（CONTRIBUTING の「変化しやすい情報」）。対応先はリリースと公式ドキュメントへのリンクに寄せた。`curl | sh` 形式のインストーラーは、パッケージマネージャー経由を選ぶかスクリプトを確認してから実行するよう [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) の観点を添えて紹介した

- **2026-09-05** クラウド 3 社のベンダー公式スキルと Anthropic の公式ディレクトリを扱う（#142・#141）
  - **[Claude Code のカスタマイズ機能](docs/claude-code/basics.md) に公式ディレクトリ `claude-plugins-official` を追加** — 配置先は `official-skills.md`（`anthropics/skills` というスキル集の解説）ではなく `basics.md` のプラグイン節にした。両者は「スキル集」と「プラグインのディレクトリ」で役割が違うため。**初回に対話モードで起動したときに自動追加される**挙動は Claude Code 公式ドキュメントで確認した。**「公式ディレクトリにある = Anthropic 製・検証済み」ではない**点は、リポジトリ README の「Anthropic は同梱される MCP サーバー・ファイル・ソフトウェアを管理しておらず、意図どおり動くことも変わらないことも保証できない」という記述を根拠に明記。判断材料として、公式名が第三者マーケットプレイスに予約されていることと、**自動更新が既定で有効**（第三者・ローカルは既定でオフ）で再現性を優先するなら切る必要があることを添えた。エントリ総数は本文に書いていない
  - **[Skills 最新動向](docs/trends.md) 8 節に「ベンダー公式スキルの登場」を新設** — AWS・Microsoft・Google の公式リポジトリを提供元・ライセンス・状態で整理。**状態は提供元ごとに違う**（`aws/agent-toolkit-for-aws` は GA と明記、`google/skills` は「under active development」、Microsoft はプラグインごとに異なるためリポジトリ参照）。「標準ができたこと」より「標準を使う側が動き出したこと」を軸にし、読者の行動は `plugin.json` を見ることに集約した
  - **[プラグインの可搬性](docs/dev-methods/plugin-portability.md) の実例表を 3 列へ拡張** — `microsoft/azure-skills` の `azure` を追加。この `plugin.json` は `skills` / `mcpServers` / `hooks` を持ち、**仕様が「構成要素を指すフィールドは存在しない」と定めているもの**の実例になる。あわせて `google/skills` が `plugin.json` を持たず `SKILL.md` を直接配る形であること（＝この判定表の対象外）を注記
  - **[Copilot Instructions](docs/copilot/instructions.md) ／ [Copilot Prompts](docs/copilot/prompts.md) の Power Platform 節から 1 行リンク（#141）** — #142 のコメントの方針どおり、#141 は網羅解説ではなくリンク追加へ縮小した
  - **8 節の「Claude Code は静観」を再確認** — Claude Code のプラグイン公式ドキュメントに Agent Plugins 1.0.0 への言及はなく、記載されるプラグイン構成も `.claude-plugin/plugin.json` のままだったため、記述を維持した。公式ディレクトリが `$schema` 付きのプラグイン（`aws-core`）をホストしていることとは別の話である点を書き分けた
  - 一次情報の確認（2026-09-05）: 4 リポジトリすべての `plugin.json` を取得し、`$schema` があるのは `aws-core` のみであることを確認。`claude-plugins-official` は `.claude-plugin/marketplace.json` と README、自動追加・自動更新・予約名は Claude Code 公式ドキュメントで確認した

- **2026-09-03** プラグインの可搬性（`$schema` による判定）を独立ページへ切り出し（#143）
  - **[プラグインの可搬性](docs/dev-methods/plugin-portability.md) を新設** — 仕様の解説ではなく「**インストールしようとしている Plugin は他のエージェントへ持っていけるか**」を主題にした。`plugin.json` の場所 → `$schema` → 最上位フィールド → MCP 設定のパス → `agents/` などの有無、という 5 段階の判定手順を表にし、**1 と 2 で決まり 3〜5 は裏づけ**である点を明示。可搬形式が課す 3 つの制約（構成要素は Skills と MCP の 2 種類・マニフェストは 10 フィールドで閉じている・マニフェストはプラグインルート固定）と、標準が用意した逃げ道（`extensions` と逆ドメイン名の名前空間ディレクトリ）を [仕様 1.0.0 の原文](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md)で検証して整理した
  - **ベンダー公式プラグインでの実物の対比を追加** — `aws/agent-toolkit-for-aws` の `aws-core` は `$schema` を持ち、Claude Code 固有の Hooks を `extensions` の `com.anthropic.claude-code` へ逃がすことで**マニフェスト本体を 10 フィールドに収めている**。一方 `microsoft/power-platform-skills` の `power-pages` は `.claude-plugin/plugin.json` と `.mcp.json` で、ルートに `plugin.json` がない。**どちらも「複数エージェント向け」と案内しているのに結果が割れる**ことを、優劣ではなく判定の実例として示した（確認日 2026-09-03）
  - **[Skills 最新動向](docs/trends.md) 8 節を要約 + リンクへ縮小** — ハーネス・セキュリティ・オントロジーで採った型に揃えた。**対応状況表は 8 節に据え置き**（陳腐化の速さが可搬性の仕組みとは違うため）
  - **[Copilot Plugins](docs/copilot/plugins.md) の冒頭 2 節を Copilot 固有の話へ絞った** — 8 節とほぼ同じだった 2 形式の比較表とガバナンス表を、選び分けの判断表 1 つ + リンクへ置き換え。「オープン標準が保証しないこと」の表も [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) と重複していたため要約 + リンクにした
  - **[コーディングエージェントの選び方](docs/dev-methods/coding-agents.md) の「定義の可搬性」から新ページへ接続** — 乗り換えの軸から、そのまま判定手順へ進める導線にした

- **2026-09-03** 手動追従 upstream の新規追加 4 件を反映（#133）
  - **[Codex Agent Skills カタログ](docs/codex/catalog.md) の System 層に `openai-docs` を追加** — Curated 層と同じスキルが System 層（同梱・インストール不要）にも収録された。公式ドキュメントの MCP サーバーを一次情報とし、Codex 自身に関する質問はマニュアル取得用ヘルパーを先に使う作りである点、**MCP サーバーが未設定だと公式ドメインの Web 検索にフォールバックする**ため参照元の確認が要る点を添えた。Curated 層の行にも同梱済みである旨を明記
  - **[skills.sh ガイド](docs/dev-methods/skills-sh.md) の Vercel 公式スキル集に 3 件追加** — `react-native-skills`（React Native / Expo の性能規約）・`deploy-to-vercel`（状態を判定してデプロイ経路を選ぶ）・`vercel-cli-with-tokens`（トークン認証での CLI 運用）。**デプロイ系 2 件は認証情報が必要で既定はプレビュー配信**である点を注記に分け、節の見出しを「Web・モバイルの品質を上げ、デプロイまでつなぐ」へ変更
  - **旧名の注記を更新** — upstream の README が `react-native-guidelines`・`vercel-deploy-claimable` の旧名で紹介している状態に合わせ、ディレクトリ名との対応が分かるよう書き換えた
  - `scripts/known-files.json` の `openai_skills` / `vercel_agent_skills` を更新

## 2026-08

- **2026-08-31** [Kiro Crew](https://kiro.dev/crew/)（AWS が 2026-08-04 に Apache-2.0 で公開した常駐型のハーネス）への言及を 4 ページに追加（#134）
  - **[ハーネス](docs/dev-methods/harness.md) に実装例として追加** — 実装を見る入口を 2 つから 3 つへ。Agent Client Protocol 経由で `kiro-cli` を駆動する層関係、`.kiro` 配下の steering files・カスタムエージェント・Skill をそのまま引き継ぐ点、永続セッション／定期ジョブ／ハートビート／長時間タスク／メモリという部品、namespace / Seatbelt による分離（standard / strict / off）と監査コマンドを整理
  - **QM との違いを軸にした** — QM が「組織のスコープと権限」を中心に据え、自前のクラウド・Postgres・インフラ担当者を前提にするのに対し、Kiro Crew は「セッションをまたぐ継続」が軸で手元のマシンで動く。**本体は無償の OSS でも動かすには Kiro のプランが必要**で、モデルの提供はベンダーに依存する点を導入判断として明記
  - **[ループエンジニアリング](docs/dev-methods/loop-engineering.md) に「OSS 側の起動条件」を追加** — Codex の Scheduled tasks との違いは、起動条件の実装を読めることと、常駐したセッションが起動条件を受け取る（エージェントの側が終わらない）こと。長時間タスクを任せるほど停止条件を渡す側で決める必要が増す点を添えた
  - **[コーディングエージェントの選び方](docs/dev-methods/coding-agents.md) は比較表に足さず**、「エージェントとハーネスの関係」で層が違うことを明示。Kiro Crew は 6 つ目のコーディングエージェントではない
  - [Skills 最新動向](docs/trends.md) 10 節に要約を追加し、8 節に Kiro の製品構成（IDE / `kiro-cli` / Crew）の補足を追記

- **2026-08-30** 2026-08 後半の動向のうち **P1（Copilot のカスタマイズ運用・Claude の統制範囲）**を反映（#128）
  - **[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) に「5. 統制が効く 3 つの段階」を新設** — 導入前（スキャン）・推論前（allow / deny 判定）・実行後（セッションの監査）。**中身が安全な Skill でも、渡される入力や実行される文脈まではスキャンできない**ため導入前だけでは埋まらない、という論点を軸にした。いずれも組織向けプラン前提で、個人利用では導入前チェックが主役である点も明記。既存の「同名の別パッケージ」は 6 節へ繰り下げ
  - **[Claude Code のカスタマイズ機能](docs/claude-code/basics.md) に Claude 固有の設定と条件** — Skill / Plugin セキュリティスキャン（Enterprise・Beta・2026-08-06）、Inference hooks（Claude Enterprise・Beta・2026-08-05。claude.ai / Cowork / Claude Code の対象プロンプトが判定を待つ。リクエストは署名され、拒否は Activity Feed に記録）、Compliance API（利用者のマシン上のセッション取得が 2026-08-26 に**ベータ終了**）。判定サーバーが落ちたときの挙動を決めておく必要と、監査範囲の周知の要否も添えた
  - **[GitHub Copilot Plugins](docs/copilot/plugins.md) に Customize タブ（GA）と marketplace の自動更新** — `extraKnownMarketplaces` の marketplace ごとに `autoUpdate: true`（2026-08-26、Copilot Business / Enterprise）。**自動更新の対象でも `strictKnownMarketplaces` の allowlist で許可されている必要がある**点と、**自動更新とコミット SHA 固定は目的が違う**（継続更新か再現性か）点を判断材料として整理
  - [Skills 最新動向](docs/trends.md) 12 節に統制の 3 段階の要約を追記
  - **訂正**: Issue #128 は Compliance API のセッション取得を新機能としていたが、一次情報では 2026-08-03 にベータ提供され **2026-08-26 にベータ終了**したもの。日付と状態をそれに合わせた
- **2026-08-30** 2026-08 後半の動向のうち **P0（Codex の自動化・エージェント間移行・MCP ロードマップ）**を反映（#128）
  - **[Codex ガイド](docs/codex/README.md) に 2 節追加** — Scheduled tasks（時刻ベースと、Gmail / Slack / GitHub のイベントベース）と、他エージェントからの取り込み。**1 タスクで複数のイベントトリガーは使えるが、イベントトリガーと時刻ベースのスケジュールは併用できない**点、イベントトリガーがデスクトップアプリと CLI では使えない点、対象プランとワークスペースでの有効化が前提である点を明記
  - **取り込み後の点検を手順として記載** — 公式ドキュメントがツール制限・MCP 認証・Hooks・Plugins・プロンプトテンプレートは手動フォローを要する場合があると明記しているため。CLI `/import` の取り込み元は Claude Code と Cursor（Cowork はデスクトップのみ）、直近 30 日・最大 50 chat
  - **[コーディングエージェントの選び方](docs/dev-methods/coding-agents.md) に「乗り換えるときに見る軸」を新設** — 定義の可搬性・作業の継続性・同期方式・再認証の要否・対応する面の 5 軸。乗り換えコストが下がるほど、取り込みが運ぶ Hooks や MCP 設定の確認が重要になる点を添えた
  - **[ループエンジニアリング](docs/dev-methods/loop-engineering.md) に実例 2 件** — Codex の Scheduled tasks（起動条件の製品実装）と、OpenAI が公開した Runme + WebMCP の事例。後者は**無人実行より「実行で得た知識を次回へ戻すこと」に価値を置いた**ループで、計画の承認は人が持つ。WebMCP により専用 MCP サーバーなしでブラウザ側の限定ツールを公開できる
  - **[Skills 最新動向](docs/trends.md) 13 節に MCP ロードマップ（2026-08-22）** — 5 つの重点領域を、2026-07-28 の確定仕様と**区別して**追加。progressive discovery が 7-2 節の Agent Finder / ARD と同じ方向である点を横断的に説明し、ロードマップは方向性の表明で確定仕様ではないと明記
  - 一次情報での確認結果は #128 のコメントに記録。Runme + WebMCP の記事はページ上に公開日の表示がないため**日付を書かない**方針とし、Codex CLI 0.147.0（2026-08-03〜07）とデスクトップの Import（08-11）は Issue が想定した日付範囲より前だった
- **2026-08-29** [GBrain](https://github.com/garrytan/gbrain) への言及を 3 ページに追加（#126）。Y Combinator の CEO である Garry Tan が 2026 年 4 月に MIT で公開した、エージェント向けの知識・記憶層
  - **位置づけ**: [オントロジー](docs/dev-methods/ontology.md) の実装例を 2 件から 3 件へ。AWS Context Ontology Accelerator と Palantir Foundry Ontology が「組織で形式的な定義を作る側」なのに対し、GBrain は **OWL / RDF で語彙を定義する手前で止める**側として対比した。判断表にも「`SKILL.md` では足りないが形式的な定義を組むほどでもない」中間の行を追加
  - **中身**: Markdown の git リポジトリが正で、PGLite / Postgres へ同期する。エンティティ抽出に**書き込みごとの LLM 呼び出しがない**。`gbrain search`（上位ページ）と `gbrain think`（根拠付きの統合回答と、まだ分かっていないことの指摘）の 2 つの問い方。接続は MCP（stdio / HTTP）と CLI
  - **限界も明記**: 単一の担当者が自分の知識を管理する前提のため、組織の共通語彙を権限つきで運用したい場合は前の 2 件が対象になる
  - [ループエンジニアリング](docs/dev-methods/loop-engineering.md) の構成要素「外部状態」に実装例として追加し、外部状態が無人ループで効く理由を 1 段落補った
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) に「5. 同名の別パッケージという入口」を新設。GBrain は npm で配布されておらず、npm 上の同名パッケージを入れると PATH 上の正規バイナリを隠す。配布元の確認・`which` での実体確認・`doctor` 相当の実行を導入前チェックに追加した。**エージェントに導入を任せると、公式が配布していない場所から同名の別物を入れがち**という点も明記
  - 独立ページは作らず既存 3 ページへの追記に留めた（オントロジーのページと説明が重複するため）。star 数・伸び率は本文に書かず、公開日は一次情報で日付単位まで確認できなかったため 2026-04 の粒度に留めた
- **2026-08-29** [Skills 最新動向](docs/trends.md) に「11. エージェントに渡す知識（オントロジー）」を新設（#127）。[オントロジー](docs/dev-methods/ontology.md) を、[ハーネス](docs/dev-methods/harness.md) や [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) と同じ「動向ページに要約 + 独立ページへ誘導」の扱いに揃えた
  - **配置の判断**: 節の並び（発見・配布 → 実行基盤 → 安全 → プロトコル）に対し、オントロジーは「エージェントに何を渡すか」で実行基盤の隣に来るため 10 節（ハーネス）の直後へ挿入。従来の 11・12 節は 12・13 節へ繰り下げた。他ページからのアンカー参照は 7〜10 節のみで、繰り下げによる参照切れはない（`scripts/check_links.py` がアンカーまで検証）
  - 「全体像」と「使い分け」の表にも 1 行ずつ追加し、`ontology.md` 冒頭から動向ページ 11 節への参照を追加（`harness.md` と同じ形）
- **2026-08-28** [オントロジー](docs/dev-methods/ontology.md) を新設（#118）。業務の意味（語彙・関係・規則）を機械が読める形で定義し、AI エージェントへ渡す方法を整理した
  - **スコープを限定**: 哲学・情報科学一般としてのオントロジー論ではなく「AI エージェントに業務知識を渡す手段」に絞った。README の「扱わない = 生成AIの一般論」との整合を取るため
  - **用語の切り分け**: 二次情報で混同が多いため、オントロジー（語彙と規則の**定義**）／ナレッジグラフ（実体と関係の**データ**）／RAG（引いて渡す）／GraphRAG（たどって渡す）を表で先に分けた。標準は W3C の [RDF](https://www.w3.org/TR/rdf11-concepts/) と [OWL 2](https://www.w3.org/TR/owl2-overview/)
  - **実装例 2 件**: [AWS Context Ontology Accelerator](https://github.com/aws/context-ontology-accelerator)（Apache-2.0、2026-07-31 公開。Scan → Model → Serve、MCP / REST で提供）と [Palantir Foundry Ontology](https://www.palantir.com/docs/foundry/ontology/overview)（意味的要素と動的要素を含む運用レイヤー）。**AI が草案を作り人が承認する**、**エージェントは統制された層の上で動く**という共通点を軸に整理
  - 「いつ不要か」を判断表に含め、維持担当を置けない場合はやめる、狭い範囲なら `SKILL.md` で足りる、と明記した
  - 不採用としたもの: Microsoft の企業向けオントロジー基盤・NTT データ LITRON / GRAG AI は日本語の二次情報にのみ現れ一次情報を特定できなかったため書かない（Microsoft からは GraphRAG のみ扱う）。導入企業数・市場規模・製品順位も本文に書かない
- **2026-08-28** [ループエンジニアリング](docs/dev-methods/loop-engineering.md) を新設（#117）。人がプロンプトを打ち続けるのをやめ、エージェントを回すループの側を設計する実践を、一次情報をもとに整理した
  - **用語の位置づけ**: Addy Osmani（Google Chrome）が [Loop Engineering](https://addyosmani.com/blog/loop-engineering/)（2026-06-07）で命名。ハーネスエンジニアリングの「1 つ上の階」にあたるとされ、プロンプト → コンテキスト → ハーネス → ループの 4 層として整理した
  - **命名の経緯を原典で確認**: 二次情報では「きっかけは Boris Cherny の発言」「Peter Steinberger の発言」で記述が割れていたが、原典には**両方が引用**されている。本文でも両方を併記した
  - 構成要素（自動実行・ワークツリー・スキル・コネクタ・サブエージェント・外部状態）、ループの 4 つの型、機械が判定できる停止条件の作り方、落とし穴（無人の誤り・理解の負債・思考の放棄）を記載。内側のループはエージェント、外側のループは人という分担は [Own the Outer Loop](https://addyosmani.com/blog/own-the-outer-loop/)（2026-07-15）に基づく
  - [ハーネス](docs/dev-methods/harness.md) に「ループとの関係」を追加し、[Skills 最新動向](docs/trends.md) 10 節へ要約と誘導を追記して相互リンクした
  - 不採用としたもの: ReAct（2022）との対比は二次情報にのみ現れ原典に記述がないため書かない。`/schedule` は[公式コマンドリファレンス](https://code.claude.com/docs/en/commands)に掲載がないためコマンド名としては書かない（`/goal` と `/loop` は掲載を確認）
- **2026-08-25** [コーディングエージェントの選び方](docs/dev-methods/coding-agents.md) を新設（#113）。Claude Code・Codex・Qwen Code・OpenCode・Bionic の 5 つを比較し、選定軸を整理した
  - **「◯◯中心」という分類の訂正**: 各公式リポジトリ／ドキュメントで確認したところ、モデル系列による分類は既定値と開発元の立ち位置を指すもので、使えるモデルの制約とは限らない。[Qwen Code](https://github.com/QwenLM/qwen-code) は Qwen 専用ではなく OpenAI・Anthropic・Gemini・ローカルモデルに対応するマルチプロトコル構成（Gemini CLI v0.8.2 が出発点、Apache-2.0）、[OpenCode](https://github.com/anomalyco/opencode) は AI SDK / Models.dev 経由で 75+ プロバイダーとローカル実行に対応（MIT）。実務で効く差は「エージェント本体が OSS か」「推論がどこで走るか」「モデルの選択肢」の 3 点として整理した
  - **Bionic は種類が違う点を明示**: [LM Studio の発表（2026-07-16）](https://lmstudio.ai/blog/introducing-lm-studio-bionic)で確認したとおり、他の 4 つがターミナル中心なのに対し Bionic は**デスクトップアプリ**。ローカル / LM Link / Secure Cloud の 3 つの実行先と Zero Data Retention を記載
  - 共通化しつつある部分（`SKILL.md` / `AGENTS.md` / MCP / Agent Plugins 1.0.0）と、[ハーネス](docs/dev-methods/harness.md)との層の違いを整理し、相互リンクを追加
  - 一次情報で確認できなかったもの: Bionic の **MCP / Skill 対応可否**と **macOS 以外のプラットフォーム対応**は公式発表に記載がないため、本文では「未確認」と明示して断定を避けた
- **2026-08-25** upstream 追加スキル 2 件に追従（#114）。[Anthropic 公式スキル](docs/claude-code/official-skills.md) に「学習支援・応答の質」カテゴリを新設して解説を追加し、`scripts/known-files.json` の `anthropics_skills` を 17 → 19 件へ更新
  - `academy-guide` — 回答に [Claude Academy](https://academy.claude.com) の該当コースを最大 2 件添える。**まず質問に答える**こと、URL は取得したカタログの実データのみ使うこと、一致が弱ければ推奨しないこと（誤った推奨の損失を重く見る設計）を明記
  - `discernment-nudge` — 実行に移せる回答の後に、確認すべき点を突く質問を 2〜3 個添える。1 会話につき 1 回のみ発動し、単純な調べもの・創作・雑談・コード作成、ユーザーが既に裏取りを依頼済みの場合は発動しない
  - この 2 件は成果物を作らず**応答の作法そのものを定義する**タイプで、既存 4 カテゴリのいずれにも収まらないため新カテゴリを立てた。内容は各 `SKILL.md` のフロントマターと本文で確認
- **2026-08-22** dev-methods の upstream 点検で未反映だった 2 件を追補（#104 の残件）
  - [obra/superpowers](docs/dev-methods/superpowers.md) — 「対応ツール」に **Devin CLI・Hermes Agent** を追加（[v6.3.0](https://github.com/obra/superpowers/releases) で対応。本文の導入手順一覧には既出だったが概要表に反映されていなかった）。スキル一覧に 2026-08 の変更を追記 — v6.2.0 で `testing-anti-patterns` が **`writing-good-tests` へ改名**（「やってはいけない例」から「良い例を先に示す 6 つのルール」へ）、v6.3.0 で依頼を **spike / bounded / architectural** に分類して手続きの重さを変える動作を追加
  - [skills.sh ガイド](docs/dev-methods/skills-sh.md) — CLI（`npx skills`）の 2026-08 の変更を追記。一括選択の追加、`--skill '*'` からの内部スキル除外、パック導入時の事前選択、`update` での新規スキル提示、**Posit Assistant・MiniMax Code** 対応、プライベートリポジトリ認証の強化
  - 二次情報にあった superpowers の「brainstorming three-path router」はリリースノートに該当記述がなく**不採用**とし、確認できた ceremony のスケーリングのみ記載
- **2026-08-22** 非エンジニア向け（business/）ページを点検し、ユースケースを追補（#109）
  - **手順の訂正**: Claude.ai のファイル作成（.docx / .xlsx / .pptx / .pdf）は[全プランで利用可能](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)（**無料プランを含む**）で、設定 → Capabilities の「コード実行とファイル作成」をオンにして使う、というのが現在の実態。「有料プランに標準搭載」としていた [README のクイックスタート](README.md#非エンジニア向けクイックスタート)・[事務・ビジネス活用ガイド](docs/business/README.md)・[事務・バックオフィス活用ガイド](docs/business/office-work.md) の記述を修正し、出力の受け取り方（ダウンロード／Google Drive 保存）も追記
  - **シナリオ 3 件追加**（[シナリオ別ユースケース集](docs/business/use-cases.md)。既存の「用意するもの／頼みかた／受け取るもの／確認する項目」書式に準拠）— 「複数ファイルをまとめて要約し、比較表にする」「会議メモから議事録とタスク一覧まで一気に作る」（3 ステップの連続フロー）「PDF 帳票と転記済みデータを突き合わせる」（転記の検算）
  - [生成AIを業務で安全に使う](docs/business/safety.md) から、エンジニア向けの [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) への「もっと詳しく」リンクを追加（#106 と対）
  - プロンプトテンプレートは出力形式の実現可能性（ファイル作成が対応する形式か）と制約文の妥当性を机上で点検。Claude.ai 上での実行確認は行っていない
- **2026-08-22** [skills.sh ガイド](docs/dev-methods/skills-sh.md) の「注目のスキル集（Top 20）」をランキング非依存の構成へ再編（#108）。順位付けの見出しをやめ、**用途別（開発プロセス／Web フロントエンド／文書・データ）の表**へ組み替えた。インストール数・順位・掲載件数といった変動値は本文に書かず、確認日（2026-08-22）と出典リポジトリを明記する形に統一。CONTRIBUTING の「変化しやすい情報の扱い」にランキングの行を追加
- **2026-08-22** upstream 監視の対象を拡張し、ページ鮮度の自動レポートを追加（#107）
  - `scripts/check_dev_methods_updates.py` を新設し、手動追従だった 5 リポジトリ（openai/skills・mattpocock/skills・obra/superpowers・vercel-labs/agent-skills・awslabs/aidlc-workflows）の新規追加を 1 スクリプトで検出。`.github/workflows/check-dev-methods-updates.yml` が毎週チェックし、対応 docs ページと `known-files.json` の更新キーを明記した Issue を起票する
  - `scripts/known-files.json` に 5 リポジトリの現在の一覧（計 91 件）を登録
  - `scripts/check_page_freshness.py` と `.github/workflows/check-page-freshness.yml` を新設。毎月 1 日に「最終更新」が **45 日超**のページを一覧化した Issue を起票する（ヘッダーが無いページも報告）
  - 監視対象一覧と鮮度チェックの対応フローを [CONTRIBUTING](CONTRIBUTING.md#新規ファイルの追跡) に追記
- **2026-08-22** [Skills 最新動向](docs/trends.md) を再構成（#106）。12 節・約 810 行まで肥大化していたため、恒常的な解説だった 2 節を独立ページへ分離した
  - [AI エージェントの実行基盤（ハーネス）](docs/dev-methods/harness.md) を新設（旧 9 節）。概念・ハーネスエンジニアリング・Microsoft Copilot Studio / QM の実装・セキュリティポスチャを集約
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md) を新設（旧 10 節）。標準が未定義の領域・導入前の確認手順・Snyk の監査データ・組織での許可範囲の限定に加え、「導入の最低ライン」表を追加
  - エンジニア向けの上記ページと、非エンジニア向けの [生成AIを業務で安全に使う](docs/business/safety.md) を相互リンク。[Agents 一覧](docs/copilot/agents.md) の `trojan-skill-hunter` からもセキュリティページへ導線を張った
  - trends.md は要約＋リンクを残し、7 節以降をテーマ順（発見・配布 → 実行基盤 → 安全 → プロトコル）へ並べ替え。約 810 行 → 約 640 行
- **2026-08-22** README に「🆕 最近の更新」欄と CI バッジを常設（#105）。冒頭 1 スクロール以内で直近の更新が分かるようにし、`ci.yml` に `main` への push トリガーを追加してバッジが既定ブランチの状態を示すようにした。運用ルール（CHANGELOG 追記時に README のハイライトも更新・上限 5 行）を [CHANGELOG の記録のルール](CHANGELOG.md#記録のルール) と [CONTRIBUTING の編集チェックリスト](CONTRIBUTING.md#編集チェックリスト) に明記
- **2026-08-22** ツール別入口ページへ 2026-08 の動向を反映（#104）。trends.md にしか書かれていなかった GA 情報を、各ツールの手順・判断表へ落とし込んだ
  - [GitHub Copilot ガイド](docs/copilot/README.md) — Plugins の状態を `GA`（VS Code の Agent plugins が [2026-08-12 に一般提供](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/)）へ更新し、「カスタマイズが効く場所 — レビューとエージェント」を新設（code review の Skill / MCP 活用と `.github/skills/` の配置、effort levels）。`plugins.md` への導線を追加
  - [Claude Code のカスタマイズ機能](docs/claude-code/basics.md) — プラグイン節に「配布元と検証」（GitLab Marketplace 対応、`claude plugin validate` の frontmatter 検査、`headersHelper` の確認・フォルダ信頼・資格情報分離）と「Agent Plugins 1.0.0 との関係」を追加。サブエージェントの fork が既定で有効になった点を追記
  - [コマンド一覧（付録）](docs/claude-code/commands.md) — [公式リファレンス](https://code.claude.com/docs/en/commands)でスナップショットを取り直し。削除・変更されたコマンド（`/settings` は存在しない、`/vim` は v2.1.92 で削除、`/pr-comments` は v2.1.91 で削除、`/cost` は `/usage` の別名、`/agents` は案内表示のみ）を明示し、`/context`・`/effort`・`/rewind`・`/fork`・`/plugin`・`/skills` 等を追加
  - [Codex ガイド](docs/codex/README.md) — 「Plugin でまとめて配る」を新設（CLI 0.147.0 の `/plugins` ブラウザ、ローカル / 個人 / ワークスペース / リモートのカタログ横断、Cursor 管理 Skill のインポート、IDE 拡張は非対応、コンテキスト逼迫時のカタログ切り詰め）。[Agent Skills カタログ](docs/codex/catalog.md) に CLI 側の入手経路への導線を追加
  - [mattpocock/skills](docs/dev-methods/mattpocock-skills.md) — upstream 差分に追従。Claude Code 公式マーケットプレイス収録により `marketplace add` が不要になった点、追加された Skill（`wizard` / `to-questionnaire` / `wait-what` / `writing-for-agents`）を反映
  - [superpowers](docs/dev-methods/superpowers.md) / [AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md) — 差分点検。superpowers は対応ハーネスの拡大（Antigravity・Devin CLI ほか）を注記、AI-DLC は補助ツール 2 件（Traceability / Code Reviewer）をリソース表へ追加
  - 反映前に各公式 changelog の 2026-08-18 以降の差分を再点検（GitHub Copilot は Slack / Teams 連携と JetBrains の managed settings、Claude Code は 2.1.239、Codex CLI は 0.149.0 まで）。カスタマイズ機能に影響するものは上記に含めた
- **2026-08-21** [Skills 最新動向](docs/trends.md) の 10 節に Snyk「ToxicSkills」調査の定量データを追加（#100 で保留していた項目）。前回調査時に 403 で到達できなかった[一次記事](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)を取得して検証 — 公開日 2026-02-05、監査対象 3,984 Skill（ClawHub / skills.sh）、36.82%（1,467 件）に問題・13.4%（534 件）が critical、悪性ペイロード 76 件（うち 8 件が調査時点で公開中）。二次情報で流通していた「30 件以上の悪性 Skill」「記事公開日 2026-04」は一次記事と食い違うため不採用。あわせて 10-3 の managed settings 適用対象に [JetBrains 対応（2026-08-18 発表）](https://github.blog/changelog/2026-08-18-enterprise-managed-settings-in-github-copilot-for-jetbrains/)を追記
  - 一次情報を確認できなかったもの: CSA research note（SKILL.md agent context poisoning）は本文・公開日とも取得できず（403）、検索経由の数値（1,184 件など）は不掲載のまま。Claude の「組織向け Skill 管理／パートナー Skill ディレクトリ」は公開日が 2025-12-18 と確認できたため、2026-08 の新規動向としては対象外
  - 各公式 changelog の 2026-08-18 以降の差分も点検（#104 の着手前確認）: GitHub は上記 JetBrains 対応のみ、Claude Code は 2.1.236〜2.1.238（2026-08-19〜2026-08-20。plugin marketplace / MCP の `headersHelper` に実行前確認とフォルダ信頼の必須化、資格情報の分離）、Codex CLI は 0.148.0〜0.149.0（2026-08-18〜2026-08-20。plugin マニフェスト処理の堅牢化、plugin の home スコープへの移動禁止、サンドボックスの fail-closed 化）。いずれもツール別ページへの反映は #104 で実施
- **2026-08-21** [Skills 最新動向](docs/trends.md) の 9 節に「ハーネスエンジニアリングという実践」を追加。Mitchell Hashimoto の [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) の定義と、OpenAI の [Harness engineering](https://openai.com/index/harness-engineering/) の実証（数値は OpenAI の自己報告である旨を明記）を紹介
  - 一次記事の URL・タイトルは各公式ドメインで確認。数値は複数の独立ソースが同一値を引用するもののみ採用し、それらと矛盾する「90% を AI が記述」という流通値は不採用。「Hashimoto が命名した」という断定も避け、「2 本の記事を機に広まった」とした
- **2026-08-18** [Skills 最新動向](docs/trends.md) の 9 節（ハーネス）に **QM**（Y Combinator が MIT ライセンスで公開した OSS のハーネス）を追加。Copilot Studio（GUI・商用）との対比、ハーネスとコーディングツール（Pi / OpenCode / Codex / Claude Code）の層関係、スコープ所有＋付与による Skill 共有、3 つのセキュリティポスチャ（Strict / Auto / Dangerous と、全ポスチャに適用される事前宣言コマンドポリシー）を整理し、10 節「標準が定義していない領域」への橋渡しとした
  - 参照した公式情報: [yc-software/qm](https://github.com/yc-software/qm)（README / [SECURITY.md](https://github.com/yc-software/qm/blob/main/SECURITY.md) / LICENSE）
  - 二次情報で流通している「ハーネスエンジニアリングの命名者」「OpenAI の生産性実績」の 2 点は一次情報を確認できなかったため本文に記載していない。組織向けソフトであることと `状態: Experimental` を明示し、SECURITY.md が挙げる限界（公開・マルチテナント向けの堅牢な境界ではない／悪意ある運用者からは守らない／組織管理者は権限を持つコンテンツ読み取り者）も併記した
- **2026-08-18** upstream 追加 Instructions 2 件に追従（#99）。`azure-apim-ai-gateway`（API Management を生成 AI ゲートウェイとして構成。トークン単位のレート制限・マネージド ID の audience 対応・呼び出し元ごとのセマンティックキャッシュ分割）と `powershell-pester-6`（Pester v6 の規約。v5 以前からの移行で効く変更点を併記）。件数を 198 → 200 へ更新
- **2026-08-17** [Skills 最新動向](docs/trends.md) に「10. Skill / Plugin のセキュリティ」「11. Skill が動く場所の広がり」「12. MCP の次期仕様」を新設し、「8. Agent Plugins 1.0.0」を仕様原文で検証して訂正（#100）。訂正点は 4 つ — `plugin.json` の例（マニフェストのスキーマは閉じており `skills` / `mcpServers` は許可されない。`$schema` は必須）、MCP 設定の固定位置（`.mcp.json` ではなく `mcp.json`）、Copilot Plugin の可搬性（`$schema` を書いて初めて可搬形式にオプトインする）、仕様公開日
  - 参照した公式情報: [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec)（[仕様 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) / [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) / [Technical Charter](https://github.com/agentplugins/agent-plugins-spec/blob/main/GOVERNANCE.md) / [MAINTAINERS](https://github.com/agentplugins/agent-plugins-spec/blob/main/MAINTAINERS.md)） / [Agent Plugins 1.0 in VS Code, Copilot CLI, and the Copilot app](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/) / [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) / [Copilot code review: Agent skills and MCP now generally available](https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available/) / [Copilot code review effort levels are generally available](https://github.blog/changelog/2026-08-07-copilot-code-review-effort-levels-are-generally-available/) / [GitHub MCP Server supports the next MCP specification](https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification/) / [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
  - セキュリティ節は仕様の Future Considerations（信頼モデル・権限・サンドボックス・出自の検証・シークレット・組織ポリシー・監査ログが v1.0.0 で未定義）を根拠にした。第三者調査の具体的な件数は一次情報へ到達できなかったため本文に記載していない
- **2026-08-17** [GitHub Copilot Plugins](docs/copilot/plugins.md) に「可搬形式（Agent Plugins 1.0.0）」と「Copilot 独自形式」の対比表を追加し、既存の構成説明を独自形式として明示（#100）。VS Code の Agent plugins を Preview から一般提供へ更新し、「オープン標準が保証しないこと」「MCP サーバーを組織で限定する」を追加
- **2026-08-17** `trojan-skill-hunter` の解説を詳細化し、レビュー・品質管理へ再配置（#91）。`gitmoji-setup` も CI/CD・DevOps へ再配置。件数表記の不整合（README の Agents 240 件・Instructions 197 件、`docs/copilot/agents.md` の 240）を `known-files.json` の実態（agents 243 / instructions 198）へ修正
- **2026-08-13** [Skills 最新動向](docs/trends.md) に「Agent Plugins 1.0.0」を追加（マルチベンダー共通エージェント設定標準 / AWS・Microsoft・OpenAI・Anysphere・Vercel による共同発表。GitHub Copilot・VS Code・Cursor・ChatGPT・AWS Kiro が対応済み）（#94）
- **2026-08-13** upstream 追加 2件（`cloud-saas-outage-triage.agent.md` / `microsoft-foundry.instructions.md`）に追従し、`docs/copilot/agents.md`・`docs/copilot/instructions.md` の解説と `scripts/known-files.json` を更新（#93）
- **2026-08-03** upstream 追加 Agent 2件（`gitmoji-setup.agent.md` / `trojan-skill-hunter.agent.md`）に追従し、`docs/copilot/agents.md` の解説と `scripts/known-files.json` を更新（#91）
- **2026-08-01** README「30 秒で選ぶ」表から消えていた非エンジニア向け 3 行を復旧（#85 P0 の退行修正）。再削除を防ぐため、意図を README 内のコメントと CONTRIBUTING のチェックリストに明記
- **2026-08-01** ユースケースの実用性を向上（#85 P2）。[生成AIを業務で安全に使う](docs/business/safety.md) を新設して business 各ページの共通注意事項を集約し、[シナリオ別ユースケース集](docs/business/use-cases.md) の全シナリオに「用意するもの／頼みかた（テンプレート）／受け取るもの／確認する項目」を追加。CONTRIBUTING に読者中心の編集チェックリストと、変化しやすい情報（件数・価格・コマンド一覧）の更新ルールを追加
- **2026-08-01** 長すぎるページを再編集（#85 P1）。`docs/claude-code/basics.md` から変わりやすいコマンド一覧を [コマンド一覧（付録）](docs/claude-code/commands.md) へ分離し、拡張機能の使い分け判断表と導入順を追加。`docs/codex/README.md` を入口ページへ戻し、全スキル一覧を [Agent Skills カタログ](docs/codex/catalog.md) へ分離（入力・生成物・人が確認すべき点を追加）
- **2026-08-01** 読者導線を基準に入口ページを再編集（#85 P0）。README の「ツール別ガイド」「目的から選ぶ」を「30 秒で選ぶ」へ統合し、重複していた製品紹介・FAQ を削除。`提供元` / `状態` / `実行環境` の情報ラベルを導入し、非エンジニア向け（Chat UI）と CLI 向けの導線を分離
- **2026-08-01** [Skills 最新動向](docs/trends.md) に「Skill の発見・配布・更新」を追加し、[GitHub Copilot Plugins](docs/copilot/plugins.md) を新設（#84）。公開後に一次情報（`cli.github.com`・`docs.github.com` 原文）で内容を検証し、`gh skill install` の `--agent` 指定例の誤り（`copilot` → 正しくは `github-copilot`）等を修正
  - 参照した公式情報: [Manage agent skills with GitHub CLI](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) / [gh skill マニュアル](https://cli.github.com/manual/gh_skill)（install/update/publish/preview/search 各サブコマンドページ含む） / [Agent finder for GitHub Copilot now available](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/) / [ARD Specification](https://agenticresourcediscovery.org/spec/) / [AI Catalog Standard](https://agenticresourcediscovery.org/ai_catalog_spec/) / [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) / [Finding and installing plugins for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) / [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

## 2026-07

- **2026-07-30** skills.sh ガイドページを新設し、注目スキル Top 20 の解説を追加（#82）
- **2026-07-29** 「Skills 最新動向」を常設ページ化し、更新履歴（本ページ）を新設（#77）
- **2026-07-29** README をハブ化し、ツール別入口ページへ詳細解説を移設（#76）
- **2026-07-29** docs/ をツール別ディレクトリ構成（copilot / claude-code / codex / dev-methods / business）に再編（#75）
- **2026-07-29** 全ドキュメントに「対象ツール」ヘッダーを追加し、ツール間の用語対照表を新設（#74）
- **2026-07-22** [Skills 最新動向](docs/trends.md) の初版を公開（6テーマ）

## 2026-06 以前（主なもの）

- **2026-06-20** Awesome AI Skills JP へ刷新し、事務・ビジネス活用コンテンツを追加
- **2026-06-08** superpowers のスキル解説を追加
- **2026-05-28** Codex 公式スキル解説、Claude Code スキルページ、Anthropic 公式スキル解説、upstream 自動更新チェックを追加
- **2026-02-07** Instructions / Agents / Prompts の詳細ガイドを追加

---

## 記録のルール

- upstream 更新チェック（check-upstream-updates / check-anthropics-skills-updates / check-financial-services-updates）の通知 Issue に対応して docs を更新したら、ここに1行追記します。
- ページの新設・構成変更も1行で記録します。書式は `**YYYY-MM-DD** 変更内容（関連 Issue/PR）` です。
- **ここに追記したら、[README の「🆕 最近の更新」](README.md#-最近の更新) にも 1 行追加してください。**上限は 5 行で、古い行から落とします。README しか見ない読者にも、直近 1〜2 週間で何が変わったかが伝わる状態を保つのが目的です。
