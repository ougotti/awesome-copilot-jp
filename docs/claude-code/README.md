# Claude Code ガイド

> **対象ツール**: Claude Code ｜ **実行環境**: CLI（ターミナル） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-01

[Claude Code](https://docs.anthropic.com/ja/docs/claude-code/overview) は Anthropic が提供するターミナルベースのコーディングエージェントです。GitHub Copilot が IDE 内のインライン補完に特化しているのに対し、ファイルシステム全体を横断する複雑なタスクをこなせるエージェントとして設計されています。

## このディレクトリのドキュメント

| ドキュメント | 内容 |
|-------------|------|
| **[Claude Code の基本](basics.md)** | スラッシュコマンド、カスタムコマンド、フック、CLAUDE.md、MCP 連携の解説 |
| **[Anthropic 公式スキル](official-skills.md)** | [anthropics/skills](https://github.com/anthropics/skills) 収録の 17 スキル（docx / pdf / pptx / xlsx 等）の詳細解説 |

---

## 主な機能

| 機能 | 概要 |
|-----|------|
| **組み込みスラッシュコマンド** | `/init`, `/review`, `/code-review`, `/compact` など |
| **カスタムコマンド** | `.claude/commands/` に Markdown を置いてコマンド化 |
| **フック（Hooks）** | `PreToolUse`, `PostToolUse`, `Stop` などのイベント駆動自動化 |
| **CLAUDE.md** | プロジェクトのコンテキストと規約を記述するファイル |
| **MCP 連携** | GitHub、PostgreSQL、Slack などの外部ツールと統合 |

**→ 各機能の詳細は [basics.md](basics.md) を参照**

---

## Anthropic 公式スキル

[anthropics/skills](https://github.com/anthropics/skills) は Anthropic が公開している Claude 用スキルのリポジトリです。Word・PDF・PowerPoint・Excel などのドキュメント処理スキルや、生成アート・MCP サーバービルドなど 17 種類のスキルが収録されています。

### カテゴリ別スキル一覧

| カテゴリ | スキル | 主な機能 |
|---------|-------|---------|
| **ドキュメント処理** | docx / pdf / pptx / xlsx | Word・PDF・PowerPoint・Excel の自動生成・編集・変換 |
| **クリエイティブ** | algorithmic-art / canvas-design / frontend-design / theme-factory | アート・デザイン・UI の生成 |
| **開発・技術** | claude-api / mcp-builder / webapp-testing / web-artifacts-builder | API 開発・MCP 構築・Web テスト |
| **エンタープライズ** | brand-guidelines / doc-coauthoring / internal-comms / slack-gif-creator / skill-creator | 組織コミュニケーション・カスタムスキル作成 |

### インストール方法（Claude Code）

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**→ 全スキルの詳細は [official-skills.md](official-skills.md) を参照**

---

## クイックスタート

```bash
# Claude Code のインストール
npm install -g @anthropic-ai/claude-code

# プロジェクトに CLAUDE.md を生成
claude
/init
```

---

## 参考リンク

- [Claude Code 公式ドキュメント](https://docs.anthropic.com/ja/docs/claude-code/overview) — Claude Code の使い方
- [anthropics/skills](https://github.com/anthropics/skills) — Anthropic 公式 Claude スキルリポジトリ

## 関連ドキュメント

- [mattpocock/skills](../dev-methods/mattpocock-skills.md) / [superpowers](../dev-methods/superpowers.md) — Claude Code で使える開発プロセス改善スキル（ツール横断）
- [金融サービス向けスキル](../business/financial-services.md) — Claude 系ツールで使える金融・経理業務向けエージェント
- [ツール間の用語対照表](../../README.md#ツール間の用語対照表) — 「Skills」「Agents」がツールごとに何を指すかの整理
