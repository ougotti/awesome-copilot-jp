# Codex ガイド（Agent Skills）

> **対象ツール**: Codex（OpenAI） ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-01

[openai/skills](https://github.com/openai/skills) は OpenAI が公開している Codex 用の公式スキルカタログです。指示・スクリプト・リソースをフォルダにまとめた「スキル」を追加することで、デプロイ・ブラウザ自動化・外部サービス連携といったワークフローを Codex に持たせられます。

このページは**導入して最初の 1 個を動かすまで**の入口です。全スキルの一覧は [Agent Skills カタログ](catalog.md) にあります。

---

## 1. 準備する

### インストール

```bash
npm install -g @openai/codex
codex
```

### スキルの置き場所

Codex は次の順序でスキルを探します。**リポジトリで共有したいなら `.agents/skills/`、自分専用なら `~/.codex/skills/`** です。

```
カレントディレクトリ
  └── .agents/skills/          # リポジトリ共有（コミットする）
親ディレクトリ（リポジトリルートまで）
  └── .agents/skills/
ユーザーレベル
  └── ~/.codex/skills/          # 個人用（全プロジェクト共通）
システムレベル（自動インストール済み）
  └── ~/.codex/skills/.system/
```

### インストール後の確認

```bash
# curated スキルをスキル名で導入
$skill-installer linear
```

> [!IMPORTANT]
> **インストール後は Codex を完全に終了して再起動してください。**再起動しないとスキルが認識されません。再起動後、`$<スキル名>` で呼び出せれば導入成功です。

---

## 2. 最初に試す 3 〜 5 個

用途別の入口です。まず 1 つ入れて、呼び出せることを確認してから増やしてください。

| 目的 | 最初に試すスキル | 導入コマンド | 追加で必要なもの |
|------|----------------|------------|----------------|
| スキルの仕組みを理解する | `skill-creator` | 不要（System・自動） | — |
| CI の失敗を直させる | `gh-fix-ci` | `$skill-installer gh-fix-ci` | GitHub リポジトリ |
| E2E テストを書かせる | `playwright` | `$skill-installer playwright` | 対象アプリの起動 |
| フロントエンドを公開する | `vercel-deploy` | `$skill-installer vercel-deploy` | Vercel アカウント |
| 仕様や調査を残す | `notion-research-documentation` | `$skill-installer notion-research-documentation` | Notion アカウント・コネクタ |

**→ 全スキルの一覧は [Agent Skills カタログ](catalog.md) を参照**

---

## 3. スキルを呼び出す

呼び出し方は 2 通りだけです。以下はすべてのスキルに共通します。

### 明示的に指定する

スキル名を `$` プレフィックスで指定します。

```
「$linear を使って、バグレポートの Issue を作成してください」
「$playwright で、フォームの送信テストを実行してください」
```

### Codex に選ばせる

タスク内容とスキルの `description` を照合し、Codex が自動的に選択します。

```
「Vercel にデプロイしてください」
→ Codex が自動的に $vercel-deploy を選択
```

> 意図しないスキルが選ばれる場合は、`$` で明示するのが確実です。自作スキルで自動選択が効かないときは、`description` に「いつ使うか」が書けているかを見直してください（[書き方の例](catalog.md#description-の書き方)）。

---

## 4. 3 つの階層の違い

`openai/skills` はスキルを 3 層に分けています。**信頼度と導入方法が違う**ので、この表だけ押さえておけば十分です。

| 階層 | ディレクトリ | 提供元 | 状態 | インストール | 使う前に |
|-----|------------|-------|------|------------|---------|
| **System** | `skills/.system/` | Official | GA | 不要（自動） | そのまま使える |
| **Curated** | `skills/.curated/` | Official | GA | スキル名で指定 | 外部アカウントの要否を確認 |
| **Experimental** | `skills/.experimental/` | Community | Experimental | パス / URL で指定 | **中身とスクリプトを必ず確認** |

Experimental は OpenAI による品質保証がありません。検証環境で試してから使ってください。

---

## 外部アカウントが必要なスキル

以下は Codex 単体では完結せず、**アカウントやコネクタ設定が前提**です。導入前に用意してください。

| 前提 | 該当スキル |
|------|-----------|
| Vercel / Netlify / Render / Cloudflare のアカウント | `vercel-deploy` / `netlify-deploy` / `render-deploy` / `cloudflare-deploy` |
| GitHub リポジトリへのアクセス権 | `gh-fix-ci` / `gh-address-comments` |
| Figma アカウントとファイル権限 | `figma` 系すべて |
| Notion アカウントとコネクタ | `notion-` 系すべて |
| Linear / Sentry のアカウント | `linear` / `sentry` |
| 対象アプリの起動（localhost 等） | `playwright` / `playwright-interactive` / `screenshot` |

> デプロイ系スキルは**本番環境に影響します。**実行前に対象環境と公開範囲を必ず確認してください。

---

## GitHub Copilot Skills との違い

| | **openai/skills** | **GitHub Copilot Skills** |
|--|------------------|--------------------------|
| 対象ツール | OpenAI Codex CLI | GitHub Copilot |
| 形式 | `SKILL.md` + スクリプト | `SKILL.md` + 関連ファイル |
| 用途 | ターミナルエージェント向けワークフロー | Copilot チャットのテンプレート |
| 配置場所 | `.agents/skills/` | `.github/skills/` |

> ツールごとの用語の違い全般は [ツール間の用語対照表](../../README.md#ツール間の用語対照表) を参照してください。

---

## 関連ドキュメント

- [Agent Skills カタログ](catalog.md) — 全スキル一覧（入力・生成物・確認すべき点つき）とカスタムスキルの作り方
- [Skills 最新動向](../trends.md) — `gh skill` など Skill の発見・配布・更新の仕組み
- [GitHub Copilot ガイド](../copilot/README.md) ／ [Claude Code ガイド](../claude-code/README.md) — 他ツールのカスタマイズ

## 参考リンク

- [openai/skills リポジトリ](https://github.com/openai/skills) — 公式スキルカタログ
- [Agent Skills – Codex 公式ドキュメント](https://developers.openai.com/codex/skills) — 公式スキル解説
- [openai/codex リポジトリ](https://github.com/openai/codex) — Codex CLI 本体
- [Codex CLI 公式ドキュメント](https://developers.openai.com/codex/cli) — CLI の使い方

---

> **注意**: Experimental スキルはコミュニティ提供であり、OpenAI による品質保証はありません。本番環境での使用前に十分な検証が必要です。
