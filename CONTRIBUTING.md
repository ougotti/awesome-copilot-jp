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
  claude-code/   # Claude Code 専用（カスタマイズ機能・コマンド一覧・Anthropic 公式スキル）
  codex/         # Codex（OpenAI）専用（入口ページ・スキルカタログ）
  dev-methods/   # ツール横断の開発手法・標準（mattpocock/skills・superpowers・AI-DLC・プラグインの可搬性）
  business/      # 非エンジニア・業務活用（ユースケース・事務・金融）
  trends.md      # ツール横断の最新動向
```

- 入口ページ（各ディレクトリの `README.md`）は「選び方」と「最小の手順」を中心にし、**網羅的な一覧は別ファイルへ分離する**（例: `codex/catalog.md`）
- バージョンで変わりやすいコマンド一覧は付録ファイルへ分け、**公式リファレンスへのリンクを主とする**（例: `claude-code/commands.md`）

- 特定ツール専用の内容 → 該当ツールのディレクトリへ
- 複数ツールに対応する開発手法・フレームワーク → `dev-methods/` へ（特定ツール配下に置かない）
- 職種・業務起点の活用ガイド → `business/` へ
- 各ドキュメントの冒頭には `> **対象ツール**: … ｜ **実行環境**: … ｜ **対象読者**: … ｜ **最終更新**: …` のヘッダーを付ける
  - **実行環境** は `Chat UI` / `IDE` / `CLI` / `Cloud` / `—` から選ぶ（複数可）。必要に応じて括弧で補足を付けてもよい（例: `CLI（ターミナル）`, `IDE（VS Code 等）`）。
  - 外部リソースを紹介する一覧表には、`提供元`（`Official` / `Community`）と `状態`（`GA` / `Preview` / `Experimental`）のラベルを付ける
  - ラベルの定義は [README の「情報ラベルの読み方」](README.md#情報ラベルの読み方) に集約する。各ページで再定義しない

## 編集チェックリスト

ページを追加・更新したら、**読者の立場で**次を確認してください。

- [ ] **この説明は他ページと重複していないか** — 詳しい説明は 1 か所に置き、他ページからは短い要約とリンクにする
- [ ] **読者は実行場所と前提条件を判断できるか** — Chat UI / IDE / CLI / Cloud のどれか、必要なプラン・OS・アカウント・権限が分かるか
- [ ] **公式／コミュニティ、GA／Preview を区別できるか** — 外部リソースには `提供元` と `状態` のラベルが付いているか
- [ ] **一覧の前に選び方があるか** — 網羅的なカタログより先に「自分はどれを選べばよいか」が示されているか
- [ ] **最小手順をそのまま実行できるか** — コマンド例に、どこで実行するか（PowerShell / ツール内スラッシュコマンド / チャット入力）が書かれているか
- [ ] **出力後に人が確認する項目が分かるか** — 生成物をそのまま使ってよいのか、何を検算・確認すべきかが書かれているか
- [ ] **時間経過で壊れやすい記述になっていないか** — 下記の更新ルールに従っているか
- [ ] **更新を README から見つけられるか** — `CHANGELOG.md` に追記したら、README の「🆕 最近の更新」にも 1 行足し、5 行を超えたら古い行を落としたか
- [ ] **非エンジニア向けの導線を消していないか** — README の「30 秒で選ぶ」表から Chat UI 行を削らない。表を短くする場合も、Chat UI 行と CLI 行の双方を残す

## 変化しやすい情報の扱い

件数・モデル名・価格・コマンド一覧・プラン名は陳腐化しやすいため、次のルールで扱います。

| 情報 | 扱い |
|------|------|
| **収録件数** | 自動検証できるものだけ本文に書く。`scripts/check_catalog_counts.py` が `known-files.json` と照合している Instructions / Agents / Prompts の 3 つが該当。**それ以外の件数は本文に書かない** |
| **コマンド一覧** | 付録ファイルへ分け、冒頭でスナップショットである旨と公式リファレンスを明示する（例: `docs/claude-code/commands.md`） |
| **価格・プラン名・モデル名** | 本文に固定で書かず、公式ページへのリンクにする。書く場合はページ冒頭の「最終更新」日と併せて読める形にする |
| **ランキング・人気順** | 本文に順位や参照数を書かない。順位で並べず**用途・カテゴリで整理**し、変動値が必要な場合のみ「取得日: YYYY-MM-DD」を明記して出典サイトへリンクする（例: `docs/dev-methods/skills-sh.md`） |
| **提供状況** | `GA` / `Preview` / `Experimental` のラベルで示す。提供地域・OS の限定がある場合は本文冒頭か表に明記する |

> 件数表記を変更するときは `python3 scripts/check_catalog_counts.py` が通ることを確認してください。CI でも検証されます。

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
| [openai/skills](https://github.com/openai/skills) | `.github/workflows/check-dev-methods-updates.yml` | `scripts/check_dev_methods_updates.py` | `openai_skills` | `docs/codex/catalog.md` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 同上 | 同上 | `mattpocock_skills` | `docs/dev-methods/mattpocock-skills.md` |
| [obra/superpowers](https://github.com/obra/superpowers) | 同上 | 同上 | `superpowers_skills` | `docs/dev-methods/superpowers.md` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | 同上 | 同上 | `vercel_agent_skills` | `docs/dev-methods/skills-sh.md` |
| [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) | 同上 | 同上 | `aidlc_extensions` | `docs/dev-methods/aidlc-workflows.md` |

監視対象を増やすときは、`scripts/check_dev_methods_updates.py` の `TARGETS` に 1 エントリ（リポジトリ・監視パス・対応 docs・`known-files.json` のキー）を追加し、`scripts/known-files.json` に現在の一覧を登録してください。新しいスクリプトやワークフローを作る必要はありません。

> 補足: [vercel-labs/skills](https://github.com/vercel-labs/skills)（`skills.sh` の CLI 本体）は「新規ファイルの追加」で変化を捉えられないため、監視対象は Vercel 公式 Skill 集の [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) にしています。CLI 側の変更は下記の鮮度チェックを起点に、リリースノートを確認して追従してください。

### ページ鮮度の月次チェック

`.github/workflows/check-page-freshness.yml` が毎月 1 日に `scripts/check_page_freshness.py` を実行し、**「最終更新」が 45 日を超えた `docs/` 配下のページ**を一覧にした Issue を起票します。

- 内容が実態と合っているかを点検し、**差分がなければ「最終更新」の日付だけを更新**してください（点検した記録になります）
- 内容を変更した場合は `CHANGELOG.md` と README の「🆕 最近の更新」にも追記します
- しきい値を変えて試すときは、ワークフローの手動実行（`workflow_dispatch`）で `threshold_days` を指定できます

## 行動規範

建設的なフィードバックを心がけ、誰もが貢献しやすい環境を維持してください。
