# 更新履歴

本ガイドの主な更新を時系列で記録します。upstream の新規スキル検出への対応と、ガイド本体の構成変更・解説追加をここにまとめます。

## 2026-08

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
