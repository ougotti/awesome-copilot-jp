# 更新履歴

本ガイドの主な更新を時系列で記録します。upstream の新規スキル検出への対応と、ガイド本体の構成変更・解説追加をここにまとめます。

## 2026-08

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
