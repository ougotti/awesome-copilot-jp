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

## ディレクトリ構成

`docs/` はツール別のディレクトリ構成になっています。新しいドキュメントを追加するときは、対象ツールに合ったディレクトリへ配置してください。

```
docs/
  copilot/       # GitHub Copilot 専用（instructions / agents / prompts / plugins）
  claude-code/   # Claude Code 専用（基本ガイド・Anthropic 公式スキル）
  codex/         # Codex（OpenAI）専用
  dev-methods/   # ツール横断の開発手法（mattpocock/skills・superpowers・AI-DLC）
  business/      # 非エンジニア・業務活用（ユースケース・事務・金融）
  trends.md      # ツール横断の最新動向
```

- 特定ツール専用の内容 → 該当ツールのディレクトリへ
- 複数ツールに対応する開発手法・フレームワーク → `dev-methods/` へ（特定ツール配下に置かない）
- 職種・業務起点の活用ガイド → `business/` へ
- 各ドキュメントの冒頭には `> **対象ツール**: … ｜ **実行環境**: … ｜ **対象読者**: … ｜ **最終更新**: …` のヘッダーを付ける
  - **実行環境** は `Chat UI` / `IDE` / `CLI` / `Cloud` から選ぶ（複数可）。読者が「どこで実行するのか」を先頭で判断できるようにする
  - 外部リソースを紹介する一覧表には、`提供元`（`Official` / `Community`）と `状態`（`GA` / `Preview` / `Experimental`）のラベルを付ける
  - ラベルの定義は [README の「情報ラベルの読み方」](README.md#情報ラベルの読み方) に集約する。各ページで再定義しない

## 編集ルール

- 説明文は日本語で書く
- `docs/` はテーブル形式（`| 列 | 列 |`）を基本とし、既存ドキュメントの見出し構成に合わせる
- エントリ名のリンク表記は、対象ドキュメントの既存スタイル（例: `**[エントリ名](URL)**` または ``[`ファイル名`](URL)``）に合わせる
- 同じセクション内では表記ゆれを避ける（用語、記号、全角/半角）
- 句点（。）で終わる

## 新規ファイルの追跡

自動検知の対象 upstream で新規追加があった場合は、該当ワークフローの通知 Issue を起点に、`scripts/known-files.json` と対応する `docs/` を更新してください。更新したら [CHANGELOG.md](CHANGELOG.md) にも1行追記してください。

| 対象 upstream | 更新チェック workflow | スクリプト | `scripts/known-files.json` の更新キー | 主な更新先ドキュメント |
|---|---|---|---|---|
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | `.github/workflows/check-upstream-updates.yml` | `scripts/check_upstream_updates.py` | `instructions` / `agents` / `prompts` | `docs/copilot/instructions.md` / `docs/copilot/agents.md` / `docs/copilot/prompts.md` |
| [anthropics/skills](https://github.com/anthropics/skills) | `.github/workflows/check-anthropics-skills-updates.yml` | `scripts/check_anthropics_skills_updates.py` | `anthropics_skills` | `docs/claude-code/official-skills.md` |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | `.github/workflows/check-financial-services-updates.yml` | `scripts/check_financial_services_updates.py` | `financial_services_agents` / `financial_services_vertical` / `financial_services_partner` | `docs/business/financial-services.md` |

> 補足: `openai/skills`、`mattpocock/skills`、`obra/superpowers`、`awslabs/aidlc-workflows` は現時点で専用の自動更新チェック workflow がないため、必要に応じて手動で差分確認して更新してください。

## 行動規範

建設的なフィードバックを心がけ、誰もが貢献しやすい環境を維持してください。
