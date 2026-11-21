Warning: truncated output (original token count: 47624)
Total output lines: 745

# 更新履歴

本ガイドの主な更新を時系列で記録します。upstream の新規スキル検出への対応と、ガイド本体の構成変更・解説追加をここにまとめます。

## 2026-11

- **2026-11-21** #324 の 11-14〜11-21 の未掲載差分を反映。
  - [Copilot Plugins](docs/copilot/plugins.md)に `strictPluginOnlyCustomization`、Marketplace policy との違い、team customizations の direct member / child team / opt-out / 上位 policy の境界を追加した。
  - [Copilot](docs/copilot/README.md)に code review の Adaptive・cross-repository context・secret detection、Azure Repos review、verified MCP connectors の状態と管理条件を追加した。
  - [Claude Code 2.1.326](docs/claude-code/basics.md)の Agent Teams + Code Mode、managed MCP、settings 保存・解析、background session、Bash / trust / managed hook の修正を整理した。
  - [Codex 0.170 / 0.171](docs/codex/README.md)の同名 MCP server、OAuth credential、permission profile、enterprise sign-in、remote app server の境界を追加した。公式資料は 2026-11-21 に確認し、実機・管理画面・API の検証は行っていない。

- **2026-11-18** [月額プランのAPIクレジット比較](docs/dev-methods/subscription-api-credits.md)を追加。ChatGPT・Claude・Geminiの受取先・有効期限・残高切れの挙動と、ChatGPT Proでの有効化を整理した。

- **2026-11-17** [Instructions](docs/copilot/instructions.md) に Bulma v1 と Godot 4、[Agents](docs/copilot/agents.md) に New Relic、オンデバイス委譲などの8件を追加。追跡一覧と件数を同期した（#320）。

- **2026-11-17** [AI-DLC の実行報告書](docs/dev-methods/aidlc-workflows.md#失敗した実行の報告書を作る)の作成手順と共有前の確認を追加し、`aidlc-issue-report` を追跡対象に登録した（#321）。

- **2026-11-14** #318 の 11-07〜11-14 の未掲載差分を反映。
  - [Claude Code 2.1.321 / 2.1.323](docs/claude-code/basics.md)の Code Mode、Plugin の version range・hook 検証・heartbeat、MCP OAuth、Bash・background session の permission / identity 修正を整理した。
  - [Codex 0.168 / 0.169](docs/codex/README.md)の未信頼 directory における project config / MCP、明示的な `--trust`、plan handoff、MCP wait・interrupt / approval cancellation の修正を追加した。
  - [MCP Skills 拡張](docs/dev-methods/skills-over-mcp.md)に C# SDK 2.4.0 の Experimental 実装を、[Copilot](docs/copilot/README.md)に GHES 対応の GA と Enterprise GitHub App の seat management permission を追加した。公式資料は 2026-11-14 に確認し、実機・管理画面・API の検証は行っていない。

- **2026-11-11** [共有したダッシュボードは誰のアクセスで動くか](docs/business/shared-data-access.md)を追加。
  - 2026-11-10 の Claude Data（旧 Claude Dashboards）の GA と、Claude Sheets・Claude Whiteboards のベータを受けて、Team と Enterprise の既定の設定を表にした。Enterprise では Claude Data が 2026-11-19 に既定でオンになり、オーナーが先に設定を保存していればそれが残ることを記した。
  - ベータの live sharing は、見る人ではなく作った人のアクセスで問い合わせが動き、データソースの権限がない人にも結果が見えることを、使わない場合と並べて整理した。行レベルのアクセス制御・組織外の人への動作・キャッシュの置き場所は、公式の資料から確かめられなかった点として分けた。
  - certified queries の印を付けられる人と印が外れる条件、利用量の負担先、Compliance API に残るイベント、導入の順番を書いた。Hacker News の議論は「コミュニティの見方」として分けた。
  - 同じ日に報じられた Claude Meetings は、Anthropic の公式の資料で確かめられなかったため扱っていない。
  - [事務・ビジネス活用ガイド](docs/business/README.md)・[生成AIを業務で安全に使う](docs/business/safety.md#関連ドキュメント)・[AIエージェントのID・認可・委任権限](docs/dev-methods/agent-identity.md#関連ドキュメント)から誘導した。Anthropic の発表とヘルプセンターは 2026-11-11 に確認した。実機・管理画面での検証は行っていない。

- **2026-11-09** [エージェントの周辺ツールが終わるとき](docs/dev-methods/tool-exit-plan.md)を追加。
  - 2026-11-04 の Conductor の Meta への合流の発表を受けて、Conductor Cloud の 11-13 の読み取り専用化・11-20 の終了とデータ削除、ローカルの Mac アプリの 2027 年初めの終了を表にした。発表が日付だけで時刻とタイムゾーンを書いていないことも記した。
  - 利用者が期限までにやること（Export data の中身の確認、Transfer to local で移らないかもしれない branch・未 push の commit を Git で持ち出す、渡した OAuth・API key を片づける）をまとめた。
  - 周辺ツールに預けているものを、コード・会話・手順と設定・認証・実行環境・契約の層に分け、各製品の並列機能で足りるかの確認と、次のツールを選ぶときの「退出のしやすさ」の条件を書いた。Hacker News の議論は「コミュニティの見方」として分けた。
  - [マルチエージェントを使う境界線](docs/dev-methods/multi-agent.md#関連ドキュメント)から誘導した。Conductor の公式の発表と changelog は 2026-11-09 に確認した。実機での検証は行っていない。

- **2026-11-07** #311 の 11-05〜11-07 の未掲載差分を反映。
  - [Claude Code 2.1.319](docs/claude-code/basics.md)の prompt 待ち拒否、auto mode の check path、MCP task と resume / 保存境界を追加した。
  - [Codex 0.167](docs/codex/README.md)の managed network / fresh checkpoint の文書化と、収録 PR の MCP lease・Plugin override・approval metadata・diagnostics の対象範囲、draft / transcript の継続を整理した。
  - [Copilot](docs/copilot/README.md)の telemetry / version gap と engagement、[code review の addressed rate](docs/dev-methods/evals.md#copilot-code-review-の-addressed-rate)、設定・local automation・Slack / Teams GA を追加した。実機試験は未実施で、確認手順と資料上の事実を区別した。

- **2026-11-07** #309 の 10-27〜10-30 の未掲載差分を反映。
  - [Claude Code](docs/claude-code/basics.md)の write block・policy・指示ファイル保護・Gateway、[Codex](docs/codex/README.md)の Marketplace と approval / resume、[Copilot](docs/copilot/README.md)の組織認証・Projects・connectors・AHP を追加した。
  - [Copilot Plugins](docs/copilot/plugins.md)の repository defaults を強制設定と読める説明を修正し、enterprise controls との違いを明記した。運用ガイドへ設定の適用・再開・失効を確認する手順を追加した。
  - 公式 release / 発表を 2026-11-07 に再確認。製品・API・管理画面の実機試験は未実施で、導入時の試験手順として記載した。

- **2026-11-04** [今週のエージェント動向](docs/dev-methods/agent-updates-2026-11-04.md)を追加。
  - 10-29〜11-04の APM / Dependabot、Claude Message threads（Beta）、Codex CLI 0.166.0・Claude Code 2.1.318、Copilot in JetBrains Air・BYOK 利用指標、WorkSpaces の対応 OS を、更新・再開・実行場所と費用の管理につなげた。
  - 10-28の自己改善する Automations は背景として扱い、既存の「チームで常設するエージェント」へ誘導した。公式の変更と記事の提案を区別し、資料確認日と未実施の実機検証を明記した。
  - README と[最新動向](docs/trends.md)から誘導した。

## 2026-10

- **2026-10-30** [チームで常設するエージェント](docs/dev-methods/team-automations.md)を追加。
  - 2026-10-28 の GitHub Universe で出た Shared Copilot Automations、trigger・tool・費用の上限の追加、自己改善する Automations、Agent Merge、Agentic Workflows の GA を、「誰の名義で動き、誰が払い、何をきっかけに動き、誰が改善を判断するか」の軸で整理した。
  - Automations（Git に入らない）と Agentic Workflows（PR でレビューする）の選び方、personal と shared の違い（型は後から変えられない、shared の PR には追加の承認）、write 権限のない人のイベントを無視する既定、連鎖での自己再発火、run ごとの上限と日・週・月の上限の止まり方の違い、Agent Merge の課金先とテストの弱化の点検を書いた。
  - VS Code のローカルの Automations とは別物であることを [GitHub Copilot ガイド](docs/copilot/README.md#automations--エージェントタスクを定期実行する)に明記し、[ループエンジニアリング](docs/dev-methods/loop-engineering.md)・[費用管理](docs/dev-methods/agent-costs.md)・[ID・認可](docs/dev-methods/agent-identity.md)から誘導した。
  - 公式の changelog と docs は 2026-10-30 に確認した。実機・管理画面での検証は行っていない。Hacker News では中身のある議論がまだないことも記した。

- **2026-10-28** Meta の Muse（2026-10-23 に日本で提供開始）を追加。
  - [Hermes Agent](docs/dev-methods/hermes-agent.md#11-事業者が運営する選択肢--claude-duetchatgpt-の-dotsmeta-の-muse)の 11 節を「事業者が運営する選択肢 — Claude Duet・ChatGPT の dots・Meta の Muse」に改め、比較表に Muse の列と「日本から」の行を加えた。Muse は利用者ごとに隔離された仮想マシン（Muse Secure VM）で動き、インターネットへのアクセスを独立した Sentinel エージェントが管理し、メール送信や購入の前に確認すること、多くの基本機能が無料であること、高度な音声モード・独自のメールアドレスなどは日本での提供が別途案内であること、仮想マシン全体を暗号化する Muse Confidential VM は未提供であることを明記した。
  - [Skills 最新動向](docs/trends.md#10-aiエージェントの実行基盤ハーネス)の 10 節と「2026-10-23〜10-24 の更新」に要約を、[生成AIを業務で安全に使う](docs/business/safety.md#ノーコードで自分専用のエージェントを動かす前に)に Muse を追加した。
  - 一次資料（Meta の発表記事と日本語のニュースルーム、OpenAI の dots のドキュメント）は 2026-10-28 に確認した。実機では確認していない。

- **2026-10-28** 2026-10-23〜10-24 の更新を製品別ページへ反映（#297）。[週次記事](docs/dev-methods/agent-updates-2026-10-27.md)の補足で触れた項目を、手順と境界つきで詳しくした。
  - [Claude Code のカスタマイズ機能](docs/claude-code/basics.md#21310--windows-の-hooksymlink-の行き先sandbox-が動かない理由)に 2.1.310 の節を新設した。Windows で Git Bash がなく hook の command が引用符の文字列だけのときに hook が通していた問題（この条件の修正であり、すべての hook が fail-closed になったわけではない）、読み取りの確認での symlink の行き先、auto mode の外部読み取りの確認、Ubuntu の AppArmor による sandbox の制限の診断、Monitor と長い foreground の sleep、非対話の MCP elicitation の timeout、Enterprise role の cloud session と Remote Control を整理した。
  - [MCP ツールの契約設計](docs/dev-methods/mcp-tool-contracts.md#答える人がいないときの問い合わせelicitation)に「答える人がいないときの問い合わせ（elicitation）」を新設し、問い合わせの前に副作用を起こさない、答えがないことを業務エラーとして返す、という契約を加えた。[信頼性設計](docs/dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い)・[ハーネス](docs/dev-methods/harness.md#同じハーネスでも起動経路で既定が違う--claude-code-21302)にも反映した。
  - [GitHub Copilot ガイド](docs/copilot/README.md#agentic-cli-の-customization-利用指標)に `totals_by_client`（ツールごとのモデルの呼び出し・session・token。prompt や task の数ではなく、client の分類は best-effort）を、[Teams の通知から修正・PR まで](docs/copilot/README.md#teams-の通知から修正pr-まで進める2026-10-23と旧-app-の廃止11-16)と旧 app の 2026-11-16 の廃止・移行手順を追加した。[evals](docs/dev-methods/evals.md) にも利用指標の読み方を追記した。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-2310-24-の権限境界の更新)に「2026-10-23〜10-24 の権限境界の更新」を、[Skills 最新動向](docs/trends.md#2026-10-2310-24-の更新--条件つきの-fail-open-と通知からの書き込み)の冒頭に期間の一覧を追加した。
  - release note と公式 changelog は 2026-10-28 に確認した。実機・管理画面・API での検証は行っていない。

- **2026-10-28** awesome-copilot に追加された Instructions を反映（#304）。
  - [Instructions 一覧](docs/copilot/instructions.md#データベース)の「データベース」に `sql-server-safe-tsql.instructions.md`（本番に近い SQL Server で安全に動く T-SQL の書き方。既定は dry run、`XACT_ABORT` と `THROW`、小分けの更新、読み取り専用の診断、破壊的な操作の前の確認）を追加し、件数を 192 件 → 193 件にした。`scripts/known-files.json` に登録した。

- **2026-10-27** [今週のエージェント動向](docs/dev-methods/agent-updates-2026-10-27.md)を追加。
  - 10-26〜10-27の Copilot assisted permissions の GA・CLI 1.0.104、Claude Code 2.1.311、Work / Codex の GPT-6.1 Terra を、承認・再開・画面操作の軸で整理した。
  - 前週10-23の Teams 統合・利用指標の `totals_by_client`・Claude Code 2.1.310 は補足として区別した。製品の変更と記事の解釈、UTC の公開日と日本時間、資料確認と実機検証を分けて記載した。
  - [最新動向](docs/trends.md)と README から誘導した。公式資料は10-27に確認し、実機検証は行っていない。

- **2026-10-24** エージェント活用とこれからのソフトウェア開発を扱う 5 ページを追加（#298〜#302）。どのページも数値は一次資料（報告書・論文・公式ドキュメント）で確認できたものだけを書き、Hacker News の議論は「コミュニティの見方」として区別して併記した。
  - [AI 導入の効果をどう測るか](docs/dev-methods/ai-adoption-metrics.md)（#298）— 採用・活動・成果の 3 層、DORA の「増幅器」という位置づけ、METR の 2025-07 の研究（体感と実測のずれ）と 2026-02 の更新（選択効果で測れなくなった理由）、指標の落とし穴、導入の効果を測る手順、製品の指標が測るもの・測らないもの。
  - [エージェントが働きやすいリポジトリ](docs/dev-methods/agent-ready-repo.md)（#299）— 指示ファイルの効果を調べた研究（成功率は上がらず費用は 20% 以上増えた）と Vercel の評価、各ツールが読む指示ファイル、何を指示ファイルに書き何を Skill・テスト・CI に移すか、エージェントが自分で確かめる仕組み、保守の方法。
  - [エージェントの費用管理](docs/dev-methods/agent-costs.md)（#300）— 費用が膨らむ仕組み、Copilot の AI Credits と予算の階層（organization 以上は既定で止まらない）、Claude Code の上限と `/usage`・`modelPricing`・`--max-budget-usd`、Codex の利用枠、チームでの配分。
  - [人の仕事はどこに移るか](docs/dev-methods/human-role.md)（#301）— GitHub での採用とエージェントの PR の大きさ・マージ後の変化を調べた研究、雇用の統計（いずれも限界つき）、律速がレビューに移る理由と対策、人が持ち続ける仕事、経験の浅い開発者の育成。提案時に挙げた working paper のうち原典を確認できなかったものは使っていない。
  - [レガシーのモダナイゼーション](docs/dev-methods/legacy-modernization.md)（#302）— 理解 → 振る舞いの固定 → 分割 → 変換 → 検証の段階、Microsoft・GitHub・AWS Transform（富士通 GS21 にも対応）・Anthropic の手順の比較、失敗しやすい点、進め方の設計例。
  - [evals](docs/dev-methods/evals.md)・[AI コードレビュー](docs/dev-methods/ai-code-review.md)・[ループエンジニアリング](docs/dev-methods/loop-engineering.md)・[マルチエージェント](docs/dev-methods/multi-agent.md)・[仕様駆動開発](docs/dev-methods/spec-driven.md)・[Claude Code](docs/claude-code/basics.md) の関連ドキュメントから誘導した。

- **2026-10-23** GitHub の 2026-10-22 の更新と Copilot CLI 1.0.103 を反映（#295）。
  - [新機能の既定ポリシー](docs/copilot/README.md#新機能の既定ポリシー--2026-10-22-から適用)の状態を GA に更新し、10-22〜10-26 の順次適用と、Unconfigured の項目には適用時に**一度だけ**効き、後から global default を変えても変わらない点を追記した。[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#4-組織で許可範囲を絞る)の記述も合わせた。
  - [Agentic CLI の customization 利用指標](docs/copilot/README.md#agentic-cli-の-customization-利用指標)に、自作の Skill・agent・MCP server・slash command・Plugin を名前で集計する変更（最大 25 件、対象の面、過去の日付は変わらない）と、名前が組織外へ出る情報になり得る注意を追加した。
  - [Copilot CLI 1.0.100〜1.0.102 の節](docs/copilot/README.md#cli-1010010102-と-vs-code-1143--sandbox-の既定とskillplugin指示の入り方)に、1.0.103 で ACP の session が sandbox の設定に従うようになった変更を追記した。
  - 一次資料は 2026-10-23 に確認した。管理画面・API での検証は行っていない。

- **2026-10-23** Codex CLI 0.164.0 を反映（#294）。
  - [Codex ガイド](docs/codex/README.md#codex-cli-01640--presetsenterprise-mcp-の認証資格情報のマスク)に節を新設した。`/presets`、`/model`・`/permissions` への引数の直接指定、enterprise MCP の認証を Codex のアカウントの権限や専用サインインで行う変更、リモートの Bash と Zsh snapshot での資格情報のマスク、macOS の sandbox の検査の強化、Windows の proxy 認証、Bedrock の設定ウィザード、再開時に thread の設定を保つ修正を整理した。
  - [作業中のエージェントへの指示](docs/dev-methods/agent-commands.md#ツールごとのキーとコマンド)に `/presets` と `/rewind` の範囲の追記を、[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1810-22-の権限境界の更新)の更新表に 1 行を追加した。
  - release note は 2026-10-23 に確認した。実機での検証は行っていない。

- **2026-10-23** Claude Code 2.1.309 を反映（#293）。
  - [Claude Code のカスタマイズ機能](docs/claude-code/basics.md#21309--sandbox-と権限の境界の修正rewind-で戻らない操作)に節を新設した。sandbox の Bash がシェルの起動ファイルを sandbox の外で実行していた問題、`--mcp-config` の設定ファイルの書き換え、`Edit(path)` の deny のリダイレクトによる回避、worktree isolation の guard、Windows の PowerShell hook の fail-open など境界を抜け得た不具合の修正と、`sed -i` が `/rewind` で戻らなくなった変更、`claude ultrareview` のワークスペースの信頼、bypass モードでの危険な `rm` の即時拒否、sandbox なしへの fallback の拒否を整理した。
  - [長時間タスクの信頼性設計](docs/dev-methods/agent-reliability.md#ツールの巻き戻しが戻す範囲を確かめる)に「ツールの巻き戻しが戻す範囲を確かめる」を、[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1810-22-の権限境界の更新)の更新表に 1 行を追加した。
  - release note は 2026-10-23 に確認した。実機での検証は行っていない。

- **2026-10-23** リンク検査が、GitHub で飛ばないアンカーを見逃す問題を修正（#292）。
  - `scripts/check_links.py` は、リンク側のフラグメントも見出しと同じ規則で slug に変換してから比べていたため、`〜` や全角かっこを含むアンカーを通していた。フラグメントは URL デコードだけを行い、そのまま見出しの ID と比べるようにした。同名の見出しに GitHub が付ける `-1`・`-2` にも対応した。
  - 修正後の検査で見つかった `#codex-cli-01600（2026-10-01）`（2 か所）を直し、[CONTRIBUTING](CONTRIBUTING.md#編集ルール)にアンカーは記号を除いた形で書く旨を追加した。

- **2026-10-22** Claude Duet（Anthropic、2026-10-21、Research Preview）を追加（#286）。
  - [Hermes Agent](docs/dev-methods/hermes-agent.md#11-事業者が運営する選択肢--claude-duetchatgpt-の-dotsmeta-の-muse)に「11. 事業者が運営する選択肢 — Claude Duet・ChatGPT の dots」を新設し、運営者・動く場所・モデル・接続先・確認の頻度・承認・費用を 3 つで比べた。米国の Pro / Max 向けのウェイトリスト制で日本からは使えないこと、承認があっても証券取引と口座間の送金は行わないこと、背景での確認も利用上限を消費すること、外から届く文面の指示への注意を明記した。「30 秒で判断する」からも誘導した。
  - [Skills 最新動向](docs/trends.md#10-aiエージェントの実行基盤ハーネス) 10 節に要約を、[生成AIを業務で安全に使う](docs/business/safety.md#ノーコードで自分専用のエージェントを動かす前に)に事業者が運営する製品でも変わらない確認を追加した。
  - 一次資料（発表記事・製品ページ・ヘルプ記事）は 2026-10-22 に確認した。日本からは利用できないため実機では確認していない。
- **2026-10-22** Claude Code 2.1.304〜2.1.307 の統制に関わる変更を反映（#287）。
  - [Claude Code のカスタマイズ機能](docs/claude-code/basics.md#2130421307--統制が緩む変更と締まる見える変更)に節を新設した。**更新で今までより通るようになる変更**（`allowedMcpServers` が `managed-mcp.json` の一部の stdio server を絞り込まなくなり `deniedMcpServers` が必要に、`sandbox.allowNestedUserNamespaces` は sandbox のファイル保護を迂回できる、gateway の背後での tool search）と、締まる・見える変更（Mods の `decider: "person"` と `settings.read` による上限、hook を止めた Skill の `allowed-tools`、`claude_code.safety_event`）、無人実行の修正（HTTP MCP の二重送信、`--worktree` のコミット消失、`--max-turns` 超過、Workflow の再開）を分け、更新時の確認手順をまとめた。
  - [Mods](docs/claude-code/mods.md#2130421305-で統制に使える部品が増えた)・[ハーネスの OTel](docs/dev-methods/harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions)・[信頼性設計](docs/dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い)・[AI コードレビュー](docs/dev-methods/review-instructions.md#レビューの深さも基準と同じく変更として扱う)（Quick / Standard / Deep と `@claude review stop`）へ反映し、[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1810-22-の権限境界の更新)に「2026-10-18〜10-22 の権限境界の更新」を新設した。
  - release note は 2026-10-22 に確認した。実機での検証は行っていない。
- **2026-10-22** Copilot CLI 1.0.100〜1.0.102 と VS Code 1.143 を反映（#288）。
  - [GitHub Copilot ガイド](docs/copilot/README.md#cli-1010010102-と-vs-code-1143--sandbox-の既定とskillplugin指示の入り方)に節を新設した。sandbox が localhost・private network へのアクセスを既定で許可する変更と proxy の継承、GitHub のインストールリンクからの「verified」な Skill / Plugin の導入（基準は非公開）、信頼済みリポジトリの Plugin の自動導入、Team の marketplace、`.github/instructions` のパス別の指示の自動適用、Skill の `allowed-tools` の解釈の修正、`assistedApprovalInstructions`・subagent への承認の引き継ぎ・`--trust-folder`、VS Code 1.143 の必須 agent plugin の自動導入・session ごとの sandbox 切り替え・`telemetry.headersProvider` を整理した。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1810-22-の権限境界の更新)に、sandbox の通信・信頼と導入の結びつき・「verified」の意味の 3 行を追加した。
  - release note は 2026-10-22 に確認した。実機での検証は行っていない。
- **2026-10-22** Claude API version `2026-10-21` と SDK / `ant` CLI 2.0 を反映（#289）。
  - [Skills 最新動向](docs/trends.md#api-version-2026-10-21-と-ant-cli-202026-10-21) 7-5 節に、`ant apply` を CI で回すリポジトリが CLI を上げる時点で確認する変更の表を追加した（`--api-key` / `--auth-token` の削除、`Authorization: Bearer`、sampling パラメータの 400、`document` / `citations` の制約、Admin API の旧フィールド名、Text Completions とクライアント側 compaction の削除、MIT → Apache 2.0、Go の module path）。Claude Code 2.1.307 の `/claude-api api-version` は挙動の変わる変更を出力で確かめる前提で紹介した。
  - [ハーネスの `ant apply`](docs/dev-methods/harness.md#ci-に載せるときの注意点) の CI の注意点に flag の削除を追加した。
  - 移行ガイドは 2026-10-22 に確認した。SDK・CLI での実機の検証は行っていない。
- **2026-10-22** 組織統制の更新を反映（#290）。
  - Inference hooks の Beta 終了（2026-10-20）を [Claude Code の組織での統制](docs/claude-code/basics.md#導入時に確認すること)・[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#5-統制が効く-3-つの段階)・[Skills 最新動向](docs/trends.md#12-skill--plugin-のセキュリティ) 12 節に反映し、対象の製品面、`tool_call` event、circuit breaker に加えて、**判定を通らない経路**（Anthropic が組織のために動かす Code Review・Claude Security のスキャン・smart reports、Bedrock / Google Cloud、API 組織、音声モードの一部）と、拒否後に会話を続ける方法を追記した。
  - [Web ツールの URL 制限](docs/dev-methods/skill-security.md#web-ツールが取得できる-url-を絞る2026-10-07)に、組織単位の Web fetch の無効化・ドメイン制限と、Managed Agents の `web_fetch` / `web_search` が組織と agent の両方の設定を満たす必要がある点を追加した。
  - [AIエージェントのID・認可・委任権限](docs/dev-methods/agent-identity.md#誰のための-request-かをモデル提供者に伝える--claude-api-の-user-profiles2026-10-20)に Claude API の user profiles（最終顧客ごとの識別、`enforcement_status`、organization webhooks）を、[GitHub Copilot ガイド](docs/copilot/README.md#モデルの方針を-api-で管理する--copilot-model-policy-api2026-10-19)に Copilot model policy API と 10-19 のモデル廃止の実施を追加した。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1810-22-の権限境界の更新)の更新表に、推論前の判定・組織単位の Web 取得・最終顧客ごとの識別・GitHub package firewall（Public Preview、npm のみ）・モデルの方針の行を追加した。
  - 一次資料は 2026-10-22 に確認した。管理画面・API での検証は行っていない。

- **2026-10-21** Hermes Agent（Nous Research の OSS の常駐型エージェント）の解説を追加（#282）。
  - [Hermes Agent — 常駐して自分から連絡してくる OSS エージェント](docs/dev-methods/hermes-agent.md)を新設した。動画「Build Your First AI Agent in 20 Minutes (No Coding)」（Metics Media、2026-10-19）が紹介する VPS + Telegram + 安価なモデル + 価格の監視という構成を、公式ドキュメントで裏を取りながら整理した。チャットボット・コーディングエージェント・常駐エージェントの違い、gateway・エージェント本体・terminal backend・モデルの 4 層、置き場所の選び方、最小の手順、モデルの接続先（Claude Code のログインを借りる経路は Pro では使えず extra usage を消費する点を含む）、cron の `[SILENT]` / `wakeAgent` / `no_agent` による「変化があったときだけ知らせる」組み方と cron の性質、費用の 4 分類、公開前の最低ライン（allowlist・承認モード・コンテナ backend・ダッシュボードの bind・v0.21.6 のセキュリティ修正）、Kiro Crew・QM・Letta Code との違いをまとめた。
  - [ハーネス](docs/dev-methods/harness.md#hermes-agent--個人が自分の置き場所に住まわせるエージェント)の実装一覧を 5 つにして Hermes の節を追加し、[Skills 最新動向](docs/trends.md#10-aiエージェントの実行基盤ハーネス) 10 節に要約を追加した。
  - 一次資料（README・releases・公式ドキュメント・Nous Portal）は 2026-10-21 に確認した。実機での検証は行っていない。動画の字幕は取得できず、概要欄とチャプターで内容を確認した。
- **2026-10-21** エージェントが自分で書く Skill の統制と、Hub からの導入時のスキャンを追記（#283）。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#エージェントが自分で書く-skill)に「エージェントが自分で書く Skill」を新設した。導入前の確認が届かない理由、`skills.write_approval` による保留と差分の確認、背景レビューの停止、`external_dirs` が書き込み保護の境界ではない点、リンターと注入検査が意図を判定しない点を整理し、Hermes の Hub のスキャンと信頼レベルを 2・3 節（ToxicSkills の監査対象だった ClawHub・skills.sh）と対応づけた。まとめの表に 1 行足した。
  - [Skills 最新動向](docs/trends.md#7-skill-の発見配布更新) 7 節の冒頭に誘導を、[Skill の公開・共有](docs/dev-methods/skill-publishing.md)に `~/.agents/skills/` のような共通の置き場所を書き換えるエージェントと共有する場合の注意を追加した。
- **2026-10-21** ループエンジニアリング・記憶基盤・業務の安全に Hermes Agent の cron と組み込みの記憶を反映（#284）。
  - [ループエンジニアリング](docs/dev-methods/loop-engineering.md#何もなかった回を黙らせる--hermes-agent-の-cron)に「何もなかった回を黙らせる — Hermes Agent の cron」を新設し、`[SILENT]`・`wakeAgent` ゲート・`no_agent` ジョブで「変化があったか」の判定を LLM の外へ移す考え方と、gateway 依存・新規セッション・cron での承認拒否などの性質を整理した。「定期実行を選ぶときの比較」に Hermes Agent の列と「何もなかった回」の行を加えた。
  - [エージェントの記憶基盤](docs/dev-methods/agent-memory.md#本体に組み込まれた記憶--hermes-agent-の例)に、上限つきの `MEMORY.md` / `USER.md` と全文検索の履歴という 2 層の組み込み記憶、外部プロバイダのプラグイン化（v0.22.0）、書き込みの承認を追加し、用途別の選び方に 1 行足した。[長時間タスクの信頼性設計](docs/dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い)に、自動では再実行しない設計と取りこぼしの確認を追加した。
  - [生成AIを業務で安全に使う](docs/business/safety.md#ノーコードで自分専用のエージェントを動かす前に)に、コードを書かない方が VPS とメッセージアプリでエージェントを動かす前の確認（データの置き場所・話しかけられる人・実行の承認・費用の上限・止め方・紹介記事の利害）を追加した。

- **2026-10-19** MCP の Skills 拡張（`io.modelcontextprotocol/skills`、SEP-2640）の解説を追加（#280）。
  - [MCP Skills 拡張 — Skill を MCP server から配る](docs/dev-methods/skills-over-mcp.md)を新設した。ファイルの Skill・Plugin・server instructions との違い、`skill://` URI と `skills/list` / `skills/get` / `resources/directory/read`、digest つきの目録と上限（512 ファイル・16 MiB）、対応状況（ChatGPT の申請時の取り込み・MCP Inspector など。Claude Code・Copilot・Codex は未対応）、ホストに課された要件（出所の表示・暗黙の実行の禁止・`allowed-tools` の無視・内容に結びついた承認・キャッシュの扱い）、Inspector CLI での検証をまとめた。
  - [Skills 最新動向](docs/trends.md#skill-を-mcp-server-から配る--skills-拡張sep-2640) 13 節に要約を、7 節の冒頭に誘導を追加した。[Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#承認の記憶がどこまで及ぶか)に pnpm の承認との対比を、[MCP と A2A](docs/dev-methods/agent-protocols.md)に Resources を Skill の配布に使う例を追加した。
  - 一次資料は 2026-10-19 に確認した。SDK・ホストでの実機の検証は行っていない。

- **2026-10-18** pnpm 12.11.0（2026-10-09）の agent skills を反映（#279）。
  - [Skills 最新動向](docs/trends.md#7-6-pnpm--依存パッケージに同梱された-skill-をつなぐ) 7 節に「7-6. pnpm — 依存パッケージに同梱された Skill をつなぐ」を新設した。配る側の `skills/<name>/SKILL.md`、`pnpm approve` と `pnpm-workspace.yaml` の `permissions`、リンク先の決まり方（既存ディレクトリ・環境変数による検出・`skills.dirs`）、直接依存だけが対象で global / `dlx` / `deploy` は対象外という制約をまとめた。
  - 比較表を「[5 つの仕組みの比較](docs/trends.md#5-つの仕組みの比較)」へ拡張して pnpm の列を加え、「使い分けの目安」に依存ライブラリの使い方を届ける行を足した。[skills.sh ガイド](docs/dev-methods/skills-sh.md)と過去の履歴の見出しリンクも合わせた。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#承認の記憶がどこまで及ぶか)に、承認がパッケージ単位で以降のバージョンにも及び、pnpm は Skill の中身を検査しない点と、止め方を追加した。
  - 一次資料は 2026-10-18 に確認した。pnpm での実機の検証は行っていない。

- **2026-10-17** 2026-10-15〜10-17 のエージェント関連の更新を反映（#277）。
  - [Claude Code 2.1.302](docs/claude-code/basics.md#21302--無人実行の開始モードと-subagent-の実行方式)の、`claude -p` / Agent SDK の開始モード、fork subagent と background / foreground の起動経路ごとの既定、`prompt` / `agent` hook の同一イベント 12 並列、`CLAUDE_CODE_AUTO_MODE_MODEL`、scheduled routine の再実行と状態表示、MCP・Plugin・worktree の互換性の修正を追加した。
  - [マルチエージェント](docs/dev-methods/multi-agent.md#3-agent-as-tool-専門作業を隔離して呼び出す)・[ハーネス](docs/dev-methods/harness.md#同じハーネスでも起動経路で既定が違う--claude-code-21302)に起動経路ごとの既定を、[ループエンジニアリング](docs/dev-methods/loop-engineering.md#定期実行の再実行と外部副作用--claude-code-21302)・[信頼性設計](docs/dev-methods/agent-reliability.md#workflow-と-mcp-の再開を検証する)に retry / rerun / 外部の再送の区別と検証項目を、[Plugin の可搬性](docs/dev-methods/plugin-portability.md#claude-code-21302--mcp-の省略可能な-field-と-plugin-の設定書き込み)に MCP と設定書き込みの修正を追加した。
  - [GitHub Copilot ガイド](docs/copilot/README.md#slack--teams-から複数の-repository-を扱う2026-10-15)に GitHub in Slack / Teams の複数 repository 対応と、会話の範囲と repository の権限を分ける運用を追加した。
  - [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md#2026-10-1510-17-の権限境界の更新)に Compliance API の `user_preferences`（Beta）を、[業務で安全に使う](docs/business/safety.md#外部への送信とファイルの保持)に保存済みの指示も組織の管理対象になり得る点を追加した。[最新動向](docs/trends.md#2026-10-1510-17-の更新--無人実行の既定値と会話から届く範囲)に一覧を追加した。
  - 一次資料は 2026-10-17 に確認した。実機・管理画面・API での検証は行っていない。

- **2026-10-16** upstream の削除も検知するようにし、Instructions を同期した（#275）。
  - 週次の更新チェック 4 本（awesome-copilot・手動追従 upstream・anthropics/skills・financial-services）が、`scripts/known-files.json` にあって upstream から消えたものも「削除」として通知 Issue に載せるようにした。取得が 404 になったパスは削除と判定しない。旧 Prompts は `skills/<名前>/` の有無で照合する。
  - [Instructions 一覧](docs/copilot/instructions.md)を upstream に合わせ、`powershell-pester-5`（→ `-6`）と Java の移行 3 件（→ `java-upgrade`）を差し替え、漏れていた `ansible` を追加して 202 件 → 192 件にした。
  - 削除検知を試したところ、mattpocock/skills の `resolving-merge-conflicts`（2026-09-24 削除）と、AI-DLC の v2 で旧 `extensions` が廃止され追跡が止まっていたことが分かった。[mattpocock/skills の解説](docs/dev-methods/mattpocock-skills.md)に削除を明記し、AI-DLC の監視先を `core/skills` に替えた。
  - 4 本のスクリプトをローカルで実行し、修正後に追加 0・削除 0 になることを確認した。通知 Issue の本文は模擬データで生成を確認した。

- **2026-10-16** 10-20〜10-26 に「最終更新」から 45 日を超える 6 ページを先に点検（#273）。
  - [Agents 一覧](docs/copilot/agents.md)から、upstream で 2026-03〜08 に削除された 22 件（`polyglot-test-*`・Beast モード系・`semantic-kernel-*`・`microsoft-agent-framework-*`・`winui3-expert` など）を外し、244 件 → 222 件にした。[Skills（旧 Prompts）一覧](docs/copilot/prompts.md)は、deprecated になった `csharp-mcp-server-generator` の行を外して後継の `dotnet-mcp-builder` を注記し、137 件 → 128 件にした。`scripts/known-files.json` と README の件数も合わせた。
  - [AI-DLC Workflows](docs/dev-methods/aidlc-workflows.md)を 2.11.0 に合わせ、公式 README のハーネスごとの最小版（Kiro CLI の v3 / V2 の設定値の違いを含む）、preview channel、2.9.0〜2.11.0 の運用に関わる変更、更新手順を追加した。
  - [MCP と A2A](docs/dev-methods/agent-protocols.md)・[AI-DLC・AI-PDLC・AI BPR の違い](docs/dev-methods/ai-driven-lifecycle-terms.md)は差分なし、[Power Apps Plans との比較](docs/dev-methods/ai-dlc-power-platform.md)は Plans が既定で有効な点を補足した。
  - upstream の更新チェックは追加だけを検知するため、削除が反映されていなかった。Instructions にも同じずれ（削除 11・追加 1）があり、別途扱う。一次資料は 2026-10-16 に確認した。

- **2026-10-16** `openai/skills` の追跡と Codex の入口を `openai/plugins` へ移した（#271）。
  - 手動追従 upstream の週次チェック（`scripts/check_dev_methods_updates.py`）の監視対象を、2026-06-22 に deprecated になった `openai/skills` から後継の `openai/plugins` の `plugins/` へ替え、`scripts/known-files.json` に現在の 62 件を登録した。CONTRIBUTING の upstream 一覧・追跡表と README のカタログ紹介も更新した。
  - [Codex ガイド](docs/codex/README.md)の 1〜4 節を、Skill と Plugin の関係・Plugin から試す流れに組み替え、Skill の置き場所を現行の公式ガイドに合わせた（管理者レベルの `/etc/codex/skills` を追加）。`$skill-installer` と 3 層の説明は「従来の方法」として残した。
  - 一次資料は 2026-10-16 に確認した。スクリプトは対象を絞ってローカルで実行し、新規 0 件を確認した。Codex での Plugin の導入は試していない。

- **2026-10-16** 「最終更新」が 10-18 に 45 日を超える 2 ページを先に点検（#269）。
  - [Codex Agent Skills カタログ](docs/codex/catalog.md)で、`openai/skills` が 2026-06-22 に deprecated になったこと、`skills/.experimental/` が存在しないことを反映し、一覧を 2026-06 時点で更新が止まったカタログとして位置づけ直した。現行の入口として [openai/plugins](https://github.com/openai/plugins)（62 件）と Plugins Directory を追加し、[Codex ガイド](docs/codex/README.md)の冒頭と 3 層の説明にも注記した。System 5 件・Curated 40 件の一覧は upstream と一致した。
  - [GitHub Copilot Plugins](docs/copilot/plugins.md)を CLI plugin reference と changelog に合わせ、可搬形式でも `com.github.copilot/` に Agents・Hooks などを置けること、`$schema` 1.0.0 / 1.1.0 の認識と非対応版の拒否、マニフェストの探索順、`copilot-plugins` が既定かどうか公式文書で記載が分かれる点、install の指定形式、managed settings のエントリ単位の優先、repository の `autoUpdate` が無視される点を反映した。Claude Code との比較表の既定 Marketplace の誤りも直し、Copilot ガイドと trends の記述を揃えた。
  - 一次資料は 2026-10-16 に確認した。CLI での実機確認は行っていない。

- **2026-10-16** 2026-10-14〜10-16 のエージェント関連の更新を反映（#263〜#267）。
  - [Claude Code 2.1.299〜2.1.301](docs/claude-code/basics.md#2129921301--mcp-の許可ルールの完全一致化と-hook-の-fail-closed-化)の、MCP の allow rule と agent の `tools:` の完全一致化、`UserPromptSubmit` の実行順、`updatedInput` の検証、plugin hook の fail-closed 化、sandbox の修正、`tool_decision` の classifier 属性を追加し、更新前の棚卸し手順を示した（#263）。
  - [VS Code 1.142](docs/copilot/README.md#vs-code-1142--統制を入れると-copilot-harness-へ移るpermission-mode-を絞る)で managed の `permissions` / `sandbox` が Copilot harness を必須にし Claude・Codex・terminal chat が使えなくなる点、`temporaryDefaultToLocalHarness` が統制も外す点、permission mode の個別制御と Assisted Permissions の非互換を追加した。Copilot CLI 1.0.98 と HydraFusion の更新（Max を含む）も反映した（#264）。
  - [Claude Managed Agents の OpenTelemetry export](docs/dev-methods/harness.md#claude-apimanaged-agents-の-trace-を自分の監視基盤へ送る2026-10-14beta)（beta）の設定・span・本文・配送の限界と、[`web_fetch` の既出 URL 制限と `allowed_hosts`](docs/dev-methods/skill-security.md#web-ツールが取得できる-url-を絞る2026-10-07)を追加した（#265）。
  - [agentic autofix と AI Scan for pull requests](docs/copilot/README.md#セキュリティ-alert-を直すエージェントとpr-の脆弱性検出--agentic-autofix-と-ai-scan) の GA を、入口・有効化・課金・merge を止めない点で比較し、[検査の通過と修正の正しさ](docs/dev-methods/evals.md#検査ツールが通ったことを修正の正しさと混同しない)を区別した（#266）。
  - [Codex CLI 0.163.0](docs/codex/README.md#codex-cli-01630--再開時の権限復元network-proxy-の強化応答中の-steer) の再開時の権限復元、network proxy の強化、応答中の steer と、GPT-5.5 廃止に伴うモデル設定の棚卸しを追加した（#267）。
  - 一次資料は 2026-10-16 に確認した。release note と公式 docs の照合のみで、実機での拒否・移行・送信の検証は未実施と各節に明記した。

- **2026-10-15** [AI 時代のコードレビュー](docs/dev-methods/ai-code-review.md)を追加（#254）。
  - GitHub の Copilot ランタイム Rust 移行事例（SDK コールバックの移植漏れと E2E テストの削除）を基に、実装の差分とテストの差分を分けて見る手順、テスト変更のチェックリスト、不当な更新と妥当な更新の対の例を整理した。
  - ReviewBench（research preview）の golden set・LLM による照合・重大度別の層別、grounded / augmented の分母の違いと、augmented recall を単独で順位付けに使わない理由、golden set の不完全さなどの限界をまとめた。
  - 前提から人の照合までの小さな検証計画と記録の様式を追加した。本ガイドでは実行しておらず、成績は載せていない。[evals](docs/dev-methods/evals.md#ai-レビュアー自体の誤検知と見逃しを測る)・[レビュー指示の参照元](docs/dev-methods/review-instructions.md)・README から案内した。

- **2026-10-14** 2026-10-10〜10-14 の最新動向を反映（#260）。
  - [GitHub Copilot ガイド](docs/copilot/README.md#managed-settings-の強制更新と最小-client-version2026-10-13)に、managed settings の `forceRemoteSettingsRefresh`（fail-closed）と `sandbox` キーの最小 client version、telemetry の identity と 5 種類の capture class を追加した。
  - VS Code 1.141 の sandbox 必須化（Preview）・旧 policy の移行・`send_message`・Worktree cleanup・Codex の引き継ぎ、Copilot CLI 1.0.96〜1.0.97 の agent 単位の hook と Autopilot での `ask` の扱い、JetBrains の MCP 自動起動の無効化を製品ページと横断ページへ追加した。
  - Claude Code・Claude Platform・Codex・MCP は期間中に新しい正式 release がないことを確認した。release note と docs の照合のみで、実機での拒否・引き継ぎの検証は未実施と明記した。

- **2026-10-13** 2026-10-03〜10-10 の最新動向を反映（#253）。
  - [Claude Managed Agents Dynamic Workflows](docs/dev-methods/harness.md#claude-managed-agents-の-dynamic-workflows)を Copilot / Claude Code と比較し、event stream、停止・予算・参照版の固定、再開時の検証を整理した。
  - Claude Code 2.1.295〜2.1.296、Copilot CLI 1.0.92〜1.0.95、Codex 0.160.1〜0.162.1 の hook・権限・MCP・sandbox の変更を製品ページへ追加した。ChatGPT Plugin RBAC と追加指示の更新も反映した。
  - 一次資料の確認日と公開日を分け、機能の前提・対象外・実機未検証の範囲を明記した。

- **2026-10-11** [Skill の公開・共有](docs/dev-methods/skill-publishing.md)を追加（#257）。
  - フォルダ共有・Git 管理・Plugin 配布・組織内公開・公式掲載の選び方と、リポジトリ／Marketplace／Plugin／Skill の関係を整理した。
  - Portable 形式の最小例、PowerShell での登録・導入・更新、公開条件、README 記載項目を追加した。Windows の Codex CLI 0.153.4 でローカル登録・導入・更新ファイルの反映を確認し、GitHub 取得・アプリ操作・チャット実行の未検証範囲を明記した。
  - README、Codex ガイド、可搬性ガイドから導線を追加し、Codex のローカル Skill 配置・再読み込みの説明を現行公式情報に合わせた。

- **2026-10-10** [dots と定期作業の選び方](docs/codex/README.md#個人の定期作業dotsteam-tasksを選ぶ)を公式資料に基づき更新（#255）。
  - dots の継続的な進捗確認・フォローと Codex の実装・デバッグ・テスト・レビューの役割、Work / Codex への委譲を整理した。クラウドコンピューター／ブラウザー、対応アプリ、許可したローカルPC、自動承認チェックの境界を追加した。
  - 10-09 の公式更新に合わせてモバイルアプリからの作成を反映し、mobile web 非対応を明記した。提供条件は確認日と公式 Access へのリンクで案内し、既存の停止操作の区別を維持した。
  - README の「30 秒で選ぶ」、[コーディングエージェントの選び方](docs/dev-methods/coding-agents.md)、[事務・ビジネス活用ガイド](docs/business/README.md)から導線を追加した。一次資料は2026-10-10に確認した。

- **2026-10-10** 「最終更新」が 45 日を超えた 2 ページを点検（#251）。
  - [Claude Code コマンド一覧](docs/claude-code/commands.md)を公式の Commands・Interactive mode と照合した。「作業の進め方・並行作業」（`/plan`・`/goal`・`/btw`・`/subtask`・`/background`）を新設し、`/import`・`/ultrareview`・`/skill-doctor`・`/reload-skills`・`/batch`・`/deep-research` を追加した。`/code-review` の努力度と `ultra`、`/doctor prompt-audit`、`/simplify` がバグを探さないこと、`/stats` の別名、`/ultraplan` の削除と `/fork` の意味の変化を反映し、キーボードショートカット（`Esc`・`Esc` 2 回・`Shift+Tab`・`Ctrl+B`・`Ctrl+O`）を公式の説明に合わせた。
  - [事務・バックオフィス活用ガイド](docs/business/office-work.md)で、「コード実行とファイル作成」が Free・Pro・Max・Team と新しい Enterprise の組織で既定でオンになった点、Team / Enterprise のネットワーク接続が既定で無効な点を反映し、Excel 監査スキル（`/debug-model`）と Microsoft 365 アドインの準備ツールへの記述を #225 の更新に合わせた。同じ記述のある README と[業務活用ガイド](docs/business/README.md)も直した。

- **2026-10-10** AI コードレビューが読む指示の参照元とレビュー基準の更新手順を追加（#249）。
  - [AI コードレビューはどの指示を読むか](docs/dev-methods/review-instructions.md)を新設し、head / base の区別、Copilot code review が custom instructions・agent instructions・agent skills を head から読むこと、Claude Code の Code Review が PR で編集された `CLAUDE.md` の base 版を使うこと（v2.1.292）、Copilot も `CLAUDE.md`・`REVIEW.md` を読むため同じファイルが製品ごとに別の版で読まれ得ること、実行場所（IDE・ローカルの `/code-review`・自前の Actions）による違いを整理した。
  - 基準を更新するときの手順、正常例・違反例・同時変更の検証例（実測ではない設計例と明記）、記録項目、base 側の CODEOWNERS と code owner の承認の組み合わせを追加した。`REVIEW.md` の参照元は出典で確定できないため断定しなかった。
  - [GitHub Copilot ガイド](docs/copilot/README.md#カスタマイズが効く場所--レビューとエージェント)・[Claude Code のカスタマイズ機能](docs/claude-code/basics.md#pr-のレビューではどの版の-claudemd-が読まれるか)・[Skill / エージェントの評価](docs/dev-methods/evals.md#レビュー基準を変えたら新旧の版で同じ差分を比べる)から導線を追加した。各一次資料を2026-10-10に確認した。

- **2026-10-09** PR #231 の固有の内容を MCP Events・MCP Apps・Codex ガイドへ移植（#228 の補足）。
  - [MCP Events](docs/dev-methods/mcp-events.md#購読から解除までの流れ)に、発見から解除までのサーバー側の流れ、署名ヘッダーと同一バイト列の送信、secret の更新、callback の宛先検証、大きな記録の扱い、`cursor: null`、自己再発火の防ぎ方を追加した。公式ドキュメントで再確認し、公式にない対策は実装例と明記した。
  - [MCP Apps](docs/dev-methods/mcp-apps.md#chatgpt-固有の拡張--plugin-extensions)に Plugin Extensions の残りの種類（設定・表示モード・ディープリンク・Model-App Context・オンボーディング）と説明用の構成例を、[Codex ガイド](docs/codex/README.md#外部の変化をきっかけに動かす--mcp-events)に Scheduled tasks のイベントトリガーと MCP Events の対応面の違いを追加した。

- **2026-10-09** 金融サービス向けスキルのページを upstream と照合して更新（#225）。
  - [金融サービス向けスキル](docs/business/financial-services.md)を anthropics/financial-services の README と marketplace の定義（2026-10-09 時点）と照合した。垂直プラグインを 6 種＋パートナー 2 種に改め、marketplace から外れた `wealth-management` とそのコマンド（`/client-review`・`/tlh`）を削除し、`/debug-model`・`/returns` を追加した。
  - Managed Agents のサブエージェント委任（`callable_agents`）が Research Preview である点、Microsoft 365 アドインを自社クラウド向けに準備する管理者用の Claude Code plugin、Egnyte と Box を別々に掲載していることを反映した。upstream の README にある `claude-for-financial-advisors` は marketplace とパスを確認できなかったため掲載しなかった。
  - `scripts/known-files.json` の `financial_services_vertical` から `wealth-management` を外した。

- **2026-10-08** ChatGPT の Plugin Extensions と MCP Events の対応範囲を追加（#228）。
  - [MCP Events](docs/dev-methods/mcp-events.md)を新設し、通常の tool・MCP Apps・Plugin Extensions・Events の役割の違い、前提（MCP 2.0 / `2026-07-28`、webhook と callback の検証のみ）、使える場所、利用者が決めること（購読条件・やること・終了条件）、サーバー開発者の責任、配信・重複・期限・再起動の扱い、失敗の観点ごとのテスト表を整理した。draft を GA や標準化完了とは書かず、ChatGPT の対応を他のクライアントへ一般化しなかった。
  - [MCP Apps](docs/dev-methods/mcp-apps.md#chatgpt-固有の拡張--plugin-extensions)に ChatGPT 固有の Plugin Extensions（サイドバー・会話横のパネル・ファイルビューア・フォーム・composer のメンション）と可搬性の注意を、[プラグインの可搬性](docs/dev-methods/plugin-portability.md#標準が用意した逃げ道)に manifest の `extensions` との区別を追加した。
  - [Codex ガイド](docs/codex/README.md#外部の変化をきっかけに動かす--mcp-events)・[最新動向 13 節](docs/trends.md#外部の変化で起動する--chatgpt-の-mcp-eventsdraft)・README から導線を追加した。公式の Plugin Extensions・MCP Events を2026-10-08に確認した。

- **2026-10-08** 2026-09-26〜10-03 の最新動向の残りを反映（#232）。Computer Use・Dynamic workflows・Code Review API は 10-05〜06 の更新で対応済み。
  - [GitHub Copilot ガイド](docs/copilot/README.md#vs-code-1140--copilot-harness複数フォルダの-sessionremote-host-への委任)に VS Code 1.140（Copilot harness と Local harness の区別、Agents window の複数フォルダの session と remote host への委任＝Experimental、MCP の保存先と `.vscode/mcp.json` の deprecated、OTel の identity capture は既定オフで Local harness のみ）と、Copilot CLI 1.0.89〜1.0.91（`.claude/rules` 互換、`oauthScopes`、`--mcp-github-auth`、read-only のディレクトリ承認、`copilot sandbox ca`、読み取り専用 pipeline の review）を追加した。
  - [複数ルート運用](docs/copilot/multi-root.md#agents-window-の複数フォルダの-session-は別機能vs-code-1140)の「Agents window は対象外」を保ったまま、1.140 の Agents window の機能を別機能として比較表で区別した。
  - [Claude Code のカスタマイズ機能](docs/claude-code/basics.md#2128521288-の統制に関わる変更)に 2.1.288 の修正（remote MCP の二重実行、`bash -c` 内の危険な `rm`、フックのスキップ、plugin agent の設定、cloud session のモデル、path 限定ルール、バックグラウンドの時間制限）と、2.1.285〜2.1.287（`plugin configure`、`.mcpb`、`allowedProviders`、managed settings の読み取りエラーの境界、`prompt_text`、`bareElicitationCapability`、`__proto__`）を追加し、2.1.288 以上を推奨下限の候補として示した（LTS とは書かない）。
  - [Codex ガイド](docs/codex/README.md#codex-cli-016002026-10-01)に 0.160.0 を追加し、[信頼性設計](docs/dev-methods/agent-reliability.md#5-冪等性重複実行外部副作用の扱い)・[プラグインの可搬性](docs/dev-methods/plugin-portability.md#instruction-ファイルは別のエージェントにも読まれる)・[ハーネス](docs/dev-methods/harness.md)・[最新動向](docs/trends.md)に要約を追加した。各一次情報を2026-10-08に確認した。

- **2026-10-08** mattpocock/skills の新規 Skill 3 件を反映（#233）。
  - [mattpocock/skills 解説](docs/dev-methods/mattpocock-skills.md#新規-skill-の使い分け2026-10-05-追加分)に、`implement-spec`（仕様全体を統合ブランチへ、タスクグラフの frontier ごとにサブエージェントで並列実装）・`retro`（セッション後の環境改善）をユーザー呼び出しへ、`pr`（Summary / Evidence / Merge Danger の PR 本文の型）をモデル呼び出しへ追加した。
  - 推奨ワークフローに `implement-spec`・`pr`・`retro` を加え、`implement` との使い分けと注意点の表を追加した。
  - `scripts/known-files.json` の `mattpocock_skills` に 3 件を追加した。upstream の SKILL.md と README を2026-10-08に確認した。

- **2026-10-08** Claude Code 2.1.292 の Windows・UNC パスの権限修正と共有フォルダの運用を追加（#239）。
  - [Claude Code のカスタ…17624 tokens truncated…cs/copilot/agents.md)** の「AI・機械学習」に `research-harness-engineer.agent.md`（リサーチ評価ハーネスエンジニア）を追加
  - `scripts/known-files.json` の `instructions` / `agents` を更新（201 / 244 件に）

- **2026-09-07** 既存ページの拡張候補 2 件（可観測性 / 非同期クラウド型エージェント）に対応（#140）
  - **[AI エージェントの実行基盤（ハーネス）](docs/dev-methods/harness.md) に「動かした後に何が見えるか — OpenTelemetry GenAI Semantic Conventions」を新設** — issue の提案どおり、新規ページではなく既存ページへ節を追加した（差分を小さく保つため）。OpenTelemetry 公式ブログを一次情報として取得し（issue 作成時点では egress ポリシーでブロックされていたが、今回のセッションでは取得できた）、Claude Code・Codex CLI・VS Code Copilot Chat それぞれの公式ドキュメントを直接確認して対応状況（メトリクス／ログ／トレース、`gen_ai.*` 属性への準拠）を比較表にした
  - **`skill-security.md` 5 節（統制が効く 3 段階）と接続** — OpenTelemetry（ベンダー中立の計測データを自分の監視基盤へ流す）と Compliance API（組織向けプランでのセッション監査）が排他ではなく別の層であることを明記した
  - **[コーディングエージェントの選び方](docs/dev-methods/coding-agents.md) に「対話しながら回すか、投げて PR をレビューするか」を新設** — issue の提案どおり、Jules・Antigravity を既存の比較表へ行として追加せず、**同期/非同期という軸**を立てて既存の「エージェントとハーネスの関係」「乗り換えるときに見る軸」の後に配置した。Jules（Google Labs、公式サイトを一次情報として確認、2026-05-19 GA）と Antigravity（Google、公式発表記事を確認、2025-11-20 Preview 公開）の一次情報を取得し、優劣やスコアではなく「主な使い方・実行場所・承認ゲート」の 3 点で整理した（CONTRIBUTING の「変化しやすい情報」を踏まえ、比較は事実の分類に留めた）
  - **一次情報の確認（2026-09-07）**: OpenTelemetry 公式ブログ、Claude Code 公式ドキュメント（`code.claude.com/docs/en/monitoring-usage`）、Codex CLI 公式ドキュメント（`learn.chatgpt.com/docs/config-file/config-advanced`）、VS Code 公式ドキュメント（`code.visualstudio.com/docs/agents/guides/monitoring-agents`）、Jules 公式サイト（`jules.google/`）、Antigravity 公式発表記事（`developers.googleblog.com`）をそれぞれ直接取得して確認した
  - **CHANGELOG.md と README の「🆕 最近の更新」・「ツール横断の開発手法」表に追記**
  - これで issue #137〜#144 の一連の対応が完了

- **2026-09-07** Skill / エージェントの評価（evals）の解説ページを新設（#138）
  - **[Skill / エージェントの評価（evals）](docs/dev-methods/evals.md) を新設** — [Skill / Plugin のセキュリティ](docs/dev-methods/skill-security.md)が扱う「**導入前**に入れてよいか」に対して、「**導入後**に実際に効いているか」を測る話として位置づけた。退行の典型パターン（①発火しない ②過剰に発火する ③手順を飛ばす ④余計なファイルを残す）、測り方の最小手順（成功の定義 → タスク集合の作成 → あり/なし比較 → 決定論的採点 → 変更のたびに回す）、道具（Codex の `codex exec --json` / `--output-schema`、`adewale/skill-eval-harness`）を整理した
  - **issue が「egress ポリシーでブロックされ未取得」としていた一次情報を取得** — OpenAI「Testing Agent Skills Systematically with Evals」、LangChain「Evaluating Skills」（Robert Xu、2026-03-05）の両方を今回のセッションでは取得でき、正確な引用（`description` が呼び出し精度を決める、という主張の原文）を根拠にした
  - **SkillsBench は arXiv アブストラクトを直接取得して確認** — 検索結果の要約に出た数値は一次情報と食い違ったため使わず、`arxiv.org/abs/2602.12670` のアブストラクト本文を直接取得して確認できた事実（平均では改善するが、ドメイン・構成により効果の大きさは大きくばらつく）だけを書いた。CONTRIBUTING の「変化しやすい情報」に沿い、タスク数・ドメイン数・スコアの具体値は本文に固定せず、確認先へのリンクに委ねた
  - **`harness.md` との用語の衝突を明示的に整理** — 「実行基盤としてのハーネス」（エージェントを動かす裏側の仕組み）と「評価用ハーネス」（実行結果を採点する測定用の足場）が同じ語を指すことを明記し、両ページから相互リンクした
  - **`skill-security.md` と「導入前 / 導入後」の役割分担を相互リンク** — 双方の「関連ドキュメント」に追加
  - **[Skills 最新動向](docs/trends.md) に「15. Skill / エージェントの評価（evals）」を新設** — 既存の「要約 + 独立ページ」の型に揃え、全体像・使い分け・参考リンクの各表にも反映
  - **CHANGELOG.md と README の「🆕 最近の更新」に追記**（5 行を維持）

- **2026-09-06** 仕様駆動開発（SDD）の解説ページを新設（#137）
  - **[仕様駆動開発（SDD）](docs/dev-methods/spec-driven.md) を新設** — SDD とは何か（仕様がコードに従うのではなくコードが仕様に従う、という上下関係の反転）から、[github/spec-kit](https://github.com/github/spec-kit) のコアワークフロー（`/speckit.constitution` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` → `/speckit.converge`）、`.specify/` のテンプレート優先順位（プロジェクトローカル > プリセット > Extension > コア）まで整理した
  - **EARS（Easy Approach to Requirements Syntax）を一次情報で裏取り** — issue が「二次情報でしか確認できていない」としていた出典を、提唱者 Alistair Mavin 本人による公式解説ページ（2009 年発表）を取得して確認した。5 つのパターン（Ubiquitous / Event-driven / State-driven / Optional feature / Unwanted behaviour）を整理し、**spec-kit 自体には EARS への直接の言及がない**こともあわせて明記した
  - **AI-DLC との関係を「SDD の実装の 1 つ」として整理** — [aidlc-workflows.md](docs/dev-methods/aidlc-workflows.md) から新ページへ相互リンクし、「機能単位で明示的な収束確認をしたいか」「プロジェクト全体を 3 フェーズで管理したいか」という選び方の軸を立てた。片方の焼き直しにしないよう、提供元・単位・起動方法・拡張性・収束の確認方法を表で対比した
  - **`AGENTS.md` との関係は断定しなかった** — 公式ドキュメントに明示的な記述が見当たらなかったため、「別のファイルとして併存する」という確認できた事実だけを書いた
  - **[Skills 最新動向](docs/trends.md) に「14. 仕様駆動開発（SDD）」を新設** — ハーネス・オントロジー・セキュリティと同じ「要約 + 独立ページ」の型に揃えた。全体像の表にも 1 行追加
  - **対応エージェント数は本文に固定で書いていない**（CONTRIBUTING の「変化しやすい情報」）。「30 以上」という数値表記をレビューで指摘され、`specify integration list` または公式の対応表へのリンクに置き換えた。spec-kit 自体のバージョン（v1.0.0）や前提ソフトウェアのバージョン（Python 3.11+）は、変動する収録件数とは別の安定した事実として残している

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
