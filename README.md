# Awesome AI Skills JP

> GitHub・OpenAI・Anthropic が公式に公開している **生成AIツールのスキル／エージェント／カスタマイズ機能**を、日本語で体系的に解説するガイドです。  
> エンジニアだけでなく、**事務・経理・金融・バックオフィス**で生成AIを使いたい方にも役立つ情報を集めています。

---

## 🚪 ツール別ガイド

各ツールの詳細解説は、ツール別の入口ページから読み進めてください。

| ガイド | 内容 |
|-------|------|
| **[GitHub Copilot ガイド](docs/copilot/README.md)** | Instructions / Prompts / Agents / Skills など8種のカスタマイズの解説とクイックスタート |
| **[Claude Code ガイド](docs/claude-code/README.md)** | 基本機能（コマンド・フック・MCP）と Anthropic 公式スキル |
| **[Codex ガイド](docs/codex/README.md)** | OpenAI Codex の Agent Skills（system / curated / experimental） |
| **[ツール横断の開発手法](#ツール横断の開発手法)** | superpowers / mattpocock/skills / AI-DLC などツールを問わない開発プロセス改善。skills.sh での Agent Skills 発見・導入も含む |
| **[事務・ビジネス活用ガイド](docs/business/README.md)** | 非エンジニア向けの業務活用（議事録・帳票・金融・経理） |

---

## 🧭 目的から選ぶ

「何を読めばいいか分からない」方は、目的から入口を選んでください。

### 共通・事務活用

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 💬 まず生成AIを触ってみたい（コードは書かない） | [非エンジニア向けクイックスタート](#-非エンジニア向けクイックスタート) |
| 📋 業務シーン別に「使える例」を見たい | [シナリオ別ユースケース集](docs/business/use-cases.md) |
| 🌐 Skills・MCP・GUI自動化の最新動向をまとめて知りたい | [Skills 最新動向](docs/trends.md) |
| 🔎 Skill の探し方・バージョン固定・組織配布を知りたい | [Skills 最新動向](docs/trends.md#7-skill-の発見配布更新)（「Skill の発見・配布・更新」） |
| 🆕 このガイドの最近の更新を知りたい | [更新履歴（CHANGELOG）](CHANGELOG.md) |
| 📝 議事録・請求書・資料など事務作業を効率化したい | [事務・バックオフィス活用ガイド](docs/business/office-work.md) |
| 💹 決算・経理・金融業務を効率化したい | [金融サービス向けスキル](docs/business/financial-services.md) |

### GitHub Copilot

| やりたいこと | おすすめの入口 |
|------------|--------------|
| ⌨️ コーディング規約を Copilot に守らせたい | [Instructions 一覧](docs/copilot/instructions.md) |
| 🧑‍💻 Copilot を専門家として使いたい | [Agents 一覧](docs/copilot/agents.md) |
| ⚡ `/` コマンドで定型タスクを実行したい | [Prompts / Skills 一覧](docs/copilot/prompts.md) |
| 📦 チームへ拡張一式をまとめて配布したい | [Plugins](docs/copilot/plugins.md) |

### Claude Code

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🤖 Claude Code をターミナルで使いたい | [Claude Code スキル](docs/claude-code/basics.md) |
| 🧱 開発プロセス（要件整理〜TDD〜設計）を改善したい | [mattpocock/skills](docs/dev-methods/mattpocock-skills.md) |
| 📦 公式スキル（docx/pdf/pptx/xlsx 等）を知りたい | [Anthropic 公式スキル](docs/claude-code/official-skills.md) |

### Codex

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🚀 Codex でデプロイ・ブラウザ自動化を追加したい | [Codex 公式スキル](docs/codex/README.md) |

### AWS AI-DLC

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🏗️ AI エージェントに 3 フェーズの開発ライフサイクルを適用したい | [AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md) |

### skills.sh

| やりたいこと | おすすめの入口 |
|------------|--------------|
| 🔍 skills.sh で人気スキルを検索・導入したい | [skills.sh ガイド](docs/dev-methods/skills-sh.md) |
| ⭐ 注目の Agent Skills Top 20 を知りたい | [skills.sh ガイド](docs/dev-methods/skills-sh.md) |

---

## 🚀 非エンジニア向けクイックスタート

コードを書かない方でも、**3 ステップ**で生成AIを業務に使えます。

1. **[Claude.ai](https://claude.ai) の有料プランに登録** — Word／Excel／PowerPoint／PDF を扱うスキルが最初から使えます。
2. **ファイルを添付して、日本語で頼むだけ** — 例：「この議事録メモを、決定事項と ToDo に分けた Word にして」
3. **出力をダウンロードして確認・微修正** — 数値や固有名詞は必ず自分で確認しましょう。

> 「どんなことを頼めるの？」という方は、まず [シナリオ別ユースケース集](docs/business/use-cases.md) を眺めてみてください。

---

## ドキュメント一覧

### GitHub Copilot

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Instructions 一覧](docs/copilot/instructions.md)** | ファイルパターンに応じてコーディング規約を自動適用するルールファイルの詳細解説 | 197 件 |
| **[Agents 一覧](docs/copilot/agents.md)** | Copilot を特定ドメインの専門家ペルソナとして振る舞わせるエージェント定義の詳細解説 | 240 件 |
| **[Prompts / Skills 一覧](docs/copilot/prompts.md)** | `/` コマンドから呼び出せる再利用可能なタスクテンプレートおよび Skills の詳細解説 | 137 件 |
| **[Plugins](docs/copilot/plugins.md)** | Agents / Skills / Hooks / MCP / LSP を 1 つの単位で配布する Plugin、Marketplace、`enabledPlugins` の詳細解説 | — |

### Claude Code

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Claude Code スキル](docs/claude-code/basics.md)** | Claude Code 専用のスラッシュコマンド、カスタムコマンド、フック、CLAUDE.md、MCP 連携の解説 | — |
| **[Anthropic 公式スキル](docs/claude-code/official-skills.md)** | [anthropics/skills](https://github.com/anthropics/skills) リポジトリ収録の 17 スキル（docx/pdf/pptx/xlsx 等）の詳細解説 | 17 件 |

### Codex

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[Codex 公式スキル](docs/codex/README.md)** | [openai/skills](https://github.com/openai/skills) リポジトリ収録の Codex Agent Skills（system/curated/experimental の 3 層構成）の詳細解説 | 40+ 件 |

### ツール横断の開発手法

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[skills.sh ガイド](docs/dev-methods/skills-sh.md)** | [skills.sh](https://skills.sh/) の Agent Skills 発見・導入ポータルの解説。`npx skills` CLI の使い方と注目 Top 20 スキルの紹介 | 20 件 |
| **[mattpocock/skills](docs/dev-methods/mattpocock-skills.md)** | [mattpocock/skills](https://github.com/mattpocock/skills) の実務エンジニア向けスキル集（grill-me / to-prd / tdd 等、開発プロセス改善型） | 21 件 |
| **[superpowers](docs/dev-methods/superpowers.md)** | [obra/superpowers](https://github.com/obra/superpowers) の SDLC スキルフレームワーク（brainstorming / TDD / systematic-debugging 等 14 スキル） ※ Claude Code・Codex・Copilot CLI など複数ツール対応 | 14 件 |
| **[AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md)** | [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) の AI 駆動開発ライフサイクル（Inception → Construction → Operations の 3 フェーズ）の詳細解説。GitHub Copilot・Claude Code・Amazon Q・Cursor など主要エージェント対応 | — |

### 共通・事務活用

| ドキュメント | 内容 | 件数 |
|-------------|------|------|
| **[シナリオ別ユースケース集](docs/business/use-cases.md)** | 役割・業務シーンから探す生成AIの実例カタログ（プロンプト例つき） | — |
| **[事務・バックオフィス活用ガイド](docs/business/office-work.md)** | 議事録・請求書・レポート・スプレッドシート作成など、日々の事務作業を生成AIで効率化する実践ガイド | — |
| **[金融サービス向けスキル](docs/business/financial-services.md)** | [anthropics/financial-services](https://github.com/anthropics/financial-services) 収録の金融・経理業務向けエージェント／スキル（決算照合・月次決算・KYC 等）の詳細解説 | 10 エージェント + 7 業務プラグイン |
| **[Skills 最新動向](docs/trends.md)** | Matt Pocock、Context7、Firecrawl、Vercel、Record & Replay、Computer Use / Browser Use、Skill の発見・配布・更新（`gh skill` / Agent Finder・ARD / Copilot Plugins）の比較と使い分け（常設・随時更新） | 7 テーマ |
| **[更新履歴（CHANGELOG）](CHANGELOG.md)** | 本ガイドの構成変更・解説追加・upstream 対応の時系列記録 | — |

---

## このガイドについて

生成AIツールは、そのままでも強力なアシスタントですが、**スキル・エージェント・カスタマイズ**を適用することで、用途に特化した使い方ができます。

| ツール | 提供元 | 特徴 |
|-------|-------|------|
| **GitHub Copilot** | GitHub | IDE 内インライン補完・チャット中心。Instructions／Agents／Skills でチームのルールや専門家ペルソナを適用 |
| **Claude Code** | Anthropic | ターミナルベースのコーディングエージェント。スラッシュコマンドやフックで複雑なタスクを自動化 |
| **Codex** | OpenAI | Agent Skills でデプロイ・ブラウザ自動化・外部サービス連携などを追加 |

### ツール間の用語対照表

「Skills」「Agents」などの用語は、**ツールによって指すものが異なります**。本ガイドを読んでいて迷ったら、この表に戻ってください。

| 用語 | GitHub Copilot | Claude Code / Claude | Codex（OpenAI） |
|------|----------------|----------------------|------------------|
| **Skills** | `SKILL.md` + 関連リソース同梱の自己完結型ツール（upstream では旧 Prompts の移行先） | Agent Skills。[anthropics/skills](https://github.com/anthropics/skills) の公式スキル（docx / pdf 等）や [mattpocock/skills](https://github.com/mattpocock/skills) 等の手順スキル | Agent Skills。[openai/skills](https://github.com/openai/skills) の system / curated / experimental 3層カタログ |
| **Agents** | 専門家ペルソナ定義（`.agent.md`） | サブエージェント（メインの会話から分離して動く補助エージェント） | —（相当機能はスキルで代替） |
| **Instructions** | ファイルパターン別にコーディング規約を自動適用（`.instructions.md`） | `CLAUDE.md` がほぼ同じ役割 | `AGENTS.md` がほぼ同じ役割 |
| **Prompts** | `/` コマンドのタスクテンプレート（`.prompt.md`） | カスタムコマンド（`.claude/commands/`） | カスタムプロンプト（`~/.codex/prompts/`） |
| **Hooks** | コーディングエージェントセッションのイベント駆動スクリプト（`hooks.json`） | `PreToolUse` / `PostToolUse` 等のイベント駆動自動化 | — |
| **Plugins** | Agents / Skills / Hooks / MCP / LSP をまとめた配布単位（`plugin.json`）。Marketplace から導入（[解説](docs/copilot/plugins.md)） | Skills / Commands / Subagents / Hooks / MCP をまとめた配布単位。`/plugin marketplace add` で導入 | Skill・MCP・コネクタ等をまとめた配布単位（例: firecrawl-codex-plugin） |

> 各ドキュメントの冒頭には「**対象ツール**」ヘッダーを付けています。どのツールの話か迷ったら、ページ先頭とこの表を確認してください。

---

## よくある質問

### Q: GitHub Copilot と Claude Code の違いは？

**GitHub Copilot** は GitHub が提供するコーディングアシスタントで、IDE 内のインライン補完やチャットが中心です。**Claude Code** は Anthropic が提供するターミナルベースのエージェントで、ファイルシステム全体を横断する複雑なタスクに向いています。

### Q: GitHub Copilot と Codex の違いは？

**GitHub Copilot** は IDE 補完・チャット向けのカスタマイズが中心です。**Codex**（OpenAI）はターミナルベースのエージェントで、Agent Skills によってデプロイ・ブラウザ自動化・外部サービス連携などのワークフローを追加できます。

> ツール固有の FAQ（設定方法・対応プランなど）は [GitHub Copilot ガイドのよくある質問](docs/copilot/README.md#よくある質問)を参照してください。

---

> **注意**: このガイドは [github/awesome-copilot](https://github.com/github/awesome-copilot) リポジトリの内容および公式ドキュメントを元に作成しています。GitHub および Anthropic はこれらのカスタマイズの機能やセキュリティを保証するものではありません。利用前にカスタマイズの内容を確認してください。
