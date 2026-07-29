# コントリビューションガイド

このリポジトリへの貢献を歓迎します。

## このリポジトリについて

このリポジトリは **Awesome AI Skills JP** として、GitHub Copilot / Claude Code / Codex / 事務・金融活用を横断して、生成 AI のスキル・エージェント・カスタマイズ機能を日本語で解説するガイドです。

主な対象 upstream:

- [github/awesome-copilot](https://github.com/github/awesome-copilot)
- [anthropics/skills](https://github.com/anthropics/skills)
- [openai/skills](https://github.com/openai/skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [obra/superpowers](https://github.com/obra/superpowers)
- [anthropics/financial-services](https://github.com/anthropics/financial-services)
- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)

新しいスキルやエージェントそのものの追加提案は、対象となる upstream リポジトリへ行ってください。このリポジトリでは、日本語解説・比較・活用ガイドの改善を受け付けます。

## 貢献できること

- 日本語訳・解説の誤りの修正
- 説明が不足しているエントリへの補足
- 新しい使用例・活用シーンの追加
- リンク切れの報告・修正

## Pull Request の手順

1. このリポジトリをフォーク
2. 作業ブランチを作成: `git checkout -b fix/description`
3. 変更をコミット: `git commit -m "fix: 説明の修正内容"`
4. プッシュ: `git push origin fix/description`
5. Pull Request を作成

## 編集ルール

- 説明文は日本語で書く
- `docs/` はテーブル形式（`| 列 | 列 |`）を基本とし、既存ドキュメントの見出し構成に合わせる
- エントリ名のリンク表記は、対象ドキュメントの既存スタイル（例: `**[エントリ名](URL)**` または ``[`ファイル名`](URL)``）に合わせる
- 同じセクション内では表記ゆれを避ける（用語、記号、全角/半角）
- 句点（。）で終わる

## 新規ファイルの追跡

自動検知の対象 upstream で新規追加があった場合は、該当ワークフローの通知 Issue を起点に、`scripts/known-files.json` と対応する `docs/` を更新してください。

| 対象 upstream | 更新チェック workflow | スクリプト | `scripts/known-files.json` の更新キー | 主な更新先ドキュメント |
|---|---|---|---|---|
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | `.github/workflows/check-upstream-updates.yml` | `scripts/check_upstream_updates.py` | `instructions` / `agents` / `prompts` | `docs/instructions.md` / `docs/agents.md` / `docs/prompts.md` |
| [anthropics/skills](https://github.com/anthropics/skills) | `.github/workflows/check-anthropics-skills-updates.yml` | `scripts/check_anthropics_skills_updates.py` | `anthropics_skills` | `docs/anthropics-skills.md` |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | `.github/workflows/check-financial-services-updates.yml` | `scripts/check_financial_services_updates.py` | `financial_services_agents` / `financial_services_vertical` / `financial_services_partner` | `docs/financial-services.md` |

> 補足: `openai/skills`、`mattpocock/skills`、`obra/superpowers`、`awslabs/aidlc-workflows` は現時点で専用の自動更新チェック workflow がないため、必要に応じて手動で差分確認して更新してください。

## 行動規範

建設的なフィードバックを心がけ、誰もが貢献しやすい環境を維持してください。
