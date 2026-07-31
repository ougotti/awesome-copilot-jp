# Awesome AI Skills JP

> GitHub Copilot・Claude Code・Codex の **スキル／エージェント／カスタマイズ機能**を、日本語で体系的に解説するガイドです。
> GitHub・OpenAI・Anthropic・AWS の公式リポジトリに加えて、mattpocock/skills・superpowers・skills.sh といった**コミュニティ資源**も対象にしています。
> コードを書かない**事務・経理・金融・バックオフィス**向けの活用ガイドも収録しています。

---

## 30 秒で選ぶ

「何を読めばいいか分からない」方は、この表から入口を決めてください。

| やりたいこと | 使う環境 | 最初に読むページ |
|------------|---------|----------------|
| コードを書かずに文書・表・スライドを作る | Chat UI | [事務・ビジネス活用ガイド](docs/business/README.md) |
| 業務シーン別に「使える例」を眺める | Chat UI | [シナリオ別ユースケース集](docs/business/use-cases.md) |
| 決算・経理・金融業務を効率化する | Chat UI | [金融サービス向けスキル](docs/business/financial-services.md) |
| IDE でのコーディングを支援する | IDE | [GitHub Copilot ガイド](docs/copilot/README.md) |
| ターミナルから開発作業を任せる | CLI | [Claude Code ガイド](docs/claude-code/README.md) ／ [Codex ガイド](docs/codex/README.md) |
| Skill を探して導入・更新する | CLI | [skills.sh ガイド](docs/dev-methods/skills-sh.md) ／ [Skills 最新動向](docs/trends.md) |
| 開発プロセス（要件整理〜TDD〜レビュー）を改善する | CLI | [ツール横断の開発手法](#ツール横断の開発手法) |
| チーム・組織の標準を作る | Repository / Enterprise | [Instructions 一覧](docs/copilot/instructions.md) ／ [Plugins](docs/copilot/plugins.md) |

> **はじめての方へ**: コードを書かない方は [非エンジニア向けクイックスタート](#非エンジニア向けクイックスタート)（ターミナル不要）から始めてください。

> **用語で迷ったら**: 「Skills」「Agents」はツールごとに指すものが違います。[ツール間の用語対照表](#ツール間の用語対照表) を確認してください。

---

## このガイドで扱う範囲

| | 内容 |
|---|---|
| **扱う** | 公式・コミュニティのスキル／エージェント／カスタマイズ機能の日本語解説、比較と選び方、業務での活用例 |
| **扱わない** | スキル本体の配布（各 upstream リポジトリを参照）、契約・課金手続きの案内、生成AIの一般論やモデル性能比較 |

新しいスキルそのものの追加提案は、対象となる upstream リポジトリへお願いします。本リポジトリでは日本語解説の改善を受け付けています（[CONTRIBUTING.md](CONTRIBUTING.md)）。

---

## 情報ラベルの読み方

一覧表には、判断に必要な次のラベルを付けています。

| ラベル | 値と意味 |
|-------|---------|
| **提供元** | `Official` = GitHub / OpenAI / Anthropic / AWS などベンダー公式 ｜ `Community` = 有志・企業ラボによる公開物 ｜ `本ガイド` = 本リポジトリで書き起こした解説 |
| **状態** | `GA` = 一般提供 ｜ `Preview` = 公開プレビュー ｜ `Experimental` = 実験的（仕様変更あり） ｜ `—` = 該当なし（ページ自体の状態を持たない／複数状態が混在） |
| **環境** | `Chat UI` = ブラウザ／アプリのチャット ｜ `IDE` = VS Code などエディタ内 ｜ `CLI` = ターミナル ｜ `Cloud` = クラウド上のエージェント ｜ `—` = 該当なし（索引ページなど） |

> ラベルは各ページ冒頭の「最終更新」日時点の情報です。`Preview` / `Experimental` の機能は、名称・コマンド・提供条件が変わることがあります。導入前に各公式リンクを確認してください。

---

## 非エンジニア向けクイックスタート

**コードを書かない方向けの入口です。ターミナルやコマンドの知識は必要ありません。**

1. **[Claude.ai](https://claude.ai) の有料プランに登録** — Word／Excel／PowerPoint／PDF を扱うスキルが最初から使えます。
2. **ファイルを添付して、日本語で頼むだけ** — 例：「この議事録メモを、決定事項と ToDo に分けた Word にして」
3. **出力をダウンロードして確認・微修正** — 数値や固有名詞は必ず自分で確認しましょう。

> 次に読むなら [シナリオ別ユースケース集](docs/business/use-cases.md) です。ターミナルを使う自動化まで進みたくなったら、[Claude Code ガイド](docs/claude-code/README.md)（CLI）へ移ってください。

---

## ドキュメント一覧

本ガイドの全ページの索引です。各ページの詳しい導入は、上の [30 秒で選ぶ](#30-秒で選ぶ) から辿ってください。

### GitHub Copilot

| ドキュメント | 提供元 | 状態 | 環境 | 内容 | 件数 |
|-------------|-------|------|------|------|------|
| **[Instructions 一覧](docs/copilot/instructions.md)** | Official | GA | IDE | ファイルパターン別に規約を自動適用するルール | 197 件 |
| **[Agents 一覧](docs/copilot/agents.md)** | Official | GA | IDE | 特定ドメインの専門家ペルソナ定義 | 240 件 |
| **[Prompts / Skills 一覧](docs/copilot/prompts.md)** | Official | GA | IDE / CLI | `/` から呼ぶタスクテンプレートと Skills | 137 件 |
| **[Plugins](docs/copilot/plugins.md)** | Official | GA（CLI）／Preview（VS Code） | CLI / IDE | 拡張一式をまとめて配布する単位と Marketplace | — |

### Claude Code

| ドキュメント | 提供元 | 状態 | 環境 | 内容 |
|-------------|-------|------|------|------|
| **[Claude Code の基本](docs/claude-code/basics.md)** | Official | GA | CLI | スラッシュコマンド、フック、CLAUDE.md、MCP 連携 |
| **[Anthropic 公式スキル](docs/claude-code/official-skills.md)** | Official | GA | Chat UI / CLI | [anthropics/skills](https://github.com/anthropics/skills) のドキュメント処理スキル等 |

### Codex

| ドキュメント | 提供元 | 状態 | 環境 | 内容 |
|-------------|-------|------|------|------|
| **[Codex 公式スキル](docs/codex/README.md)** | Official | GA（System / Curated）／Experimental | CLI | [openai/skills](https://github.com/openai/skills) の 3 層カタログ |

### ツール横断の開発手法

| ドキュメント | 提供元 | 状態 | 環境 | 内容 |
|-------------|-------|------|------|------|
| **[skills.sh ガイド](docs/dev-methods/skills-sh.md)** | Community | GA | CLI | Agent Skills の検索・導入ポータルと注目スキル |
| **[mattpocock/skills](docs/dev-methods/mattpocock-skills.md)** | Community | GA | CLI | 要件整理〜仕様化〜TDD〜レビューの手順スキル |
| **[superpowers](docs/dev-methods/superpowers.md)** | Community | GA | CLI | SDLC スキルフレームワーク（複数ツール対応） |
| **[AI-DLC ワークフロー](docs/dev-methods/aidlc-workflows.md)** | Official（AWS） | GA | CLI / IDE | 3 フェーズの AI 駆動開発ライフサイクル |

### 共通・事務活用

| ドキュメント | 提供元 | 状態 | 環境 | 内容 |
|-------------|-------|------|------|------|
| **[シナリオ別ユースケース集](docs/business/use-cases.md)** | 本ガイド | — | Chat UI | 役割・業務シーン別の実例カタログ |
| **[事務・バックオフィス活用ガイド](docs/business/office-work.md)** | 本ガイド | — | Chat UI | 議事録・帳票・集計・スライド作成の実践 |
| **[金融サービス向けスキル](docs/business/financial-services.md)** | Official | GA | Chat UI / CLI | 決算照合・月次決算・KYC 等の業務エージェント |
| **[Skills 最新動向](docs/trends.md)** | Official / Community / 本ガイド | GA / Preview / Experimental | Chat UI / IDE / CLI / Cloud | Skill・MCP・GUI 自動化の動向と使い分け（随時更新） |
| **[更新履歴（CHANGELOG）](CHANGELOG.md)** | 本ガイド | — | — | 本ガイドの構成変更・解説追加の時系列記録 |

---

## ツール間の用語対照表

「Skills」「Agents」などの用語は、**ツールによって指すものが異なります**。本ガイドを読んでいて迷ったら、この表に戻ってください。

| 用語 | GitHub Copilot | Claude Code / Claude | Codex（OpenAI） |
|------|----------------|----------------------|------------------|
| **Skills** | `SKILL.md` + 関連リソース同梱の自己完結型ツール（upstream では旧 Prompts の移行先） | Agent Skills。[anthropics/skills](https://github.com/anthropics/skills) の公式スキル（docx / pdf 等）や [mattpocock/skills](https://github.com/mattpocock/skills) 等の手順スキル | Agent Skills。[openai/skills](https://github.com/openai/skills) の system / curated / experimental 3層カタログ |
| **Agents** | 専門家ペルソナ定義（`.agent.md`） | サブエージェント（メインの会話から分離して動く補助エージェント） | —（相当機能はスキルで代替） |
| **Instructions** | ファイルパターン別にコーディング規約を自動適用（`.instructions.md`） | `CLAUDE.md` がほぼ同じ役割 | `AGENTS.md` がほぼ同じ役割 |
| **Prompts** | `/` コマンドのタスクテンプレート（`.prompt.md`） | カスタムコマンド（`.claude/commands/`） | カスタムプロンプト（`~/.codex/prompts/`） |
| **Hooks** | コーディングエージェントセッションのイベント駆動スクリプト（`hooks.json`） | `PreToolUse` / `PostToolUse` 等のイベント駆動自動化 | — |
| **Plugins** | Agents / Skills / Hooks / MCP / LSP をまとめた配布単位（`plugin.json`）。Marketplace から導入（[解説](docs/copilot/plugins.md)） | Skills / Commands / Subagents / Hooks / MCP をまとめた配布単位。`/plugin marketplace add` で導入 | Skill・MCP・コネクタ等をまとめた配布単位（例: firecrawl-codex-plugin） |

3 ツールの位置づけは、**Copilot = IDE 内の補完・チャット中心**、**Claude Code = ターミナルからファイル横断の作業**、**Codex = ターミナルから Agent Skills でワークフローを追加**、と整理できます。各ツールの詳細と設定方法・FAQ は、ツール別の入口ページ（[Copilot](docs/copilot/README.md) ／ [Claude Code](docs/claude-code/README.md) ／ [Codex](docs/codex/README.md)）を参照してください。

> 各ドキュメントの冒頭には「**対象ツール**」「**実行環境**」ヘッダーを付けています。どのツールの話か、どこで実行するのかは、ページ先頭とこの表で確認できます。

---

> **注意**: このガイドは [github/awesome-copilot](https://github.com/github/awesome-copilot) をはじめとする各 upstream リポジトリおよび公式ドキュメントを元に作成しています。GitHub・OpenAI・Anthropic はこれらのカスタマイズの機能やセキュリティを保証するものではありません。利用前にカスタマイズの内容を確認してください。
