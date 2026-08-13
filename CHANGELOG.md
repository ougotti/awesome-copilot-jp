# 更新履歴

本ガイドの主な更新を時系列で記録します。upstream の新規スキル検出への対応と、ガイド本体の構成変更・解説追加をここにまとめます。

## 2026-08

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
