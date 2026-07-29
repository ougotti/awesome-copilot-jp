# 2026年7月版：Agent Skills・MCP・GUI 自動化の最新動向

> **対象ツール**: ツール横断 ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-07-29

> Agent Skills は `SKILL.md` だけで完結する仕組みから、MCP、Web データ取得、デプロイ、Computer Use と組み合わさる実行基盤へ広がっています。本ページでは、2026年7月22日時点で注目度の高い6テーマを公式情報に基づいて整理します。

## 動画チャプター対応表

| 時刻 | テーマ | このページで扱う内容 |
|------|--------|----------------------|
| 07:43 | Matt Pocock's Skills | 実務開発プロセスを分割・合成可能なSkillにする |
| 15:08 | Context7 | 最新のライブラリ文書をSkillsまたはMCPで取得する |
| 15:55 | Firecrawl | 検索・スクレイピング・ブラウザ操作をエージェントへ追加する |
| 18:41 | Vercel | Agent Skillsの配布基盤とVercel公式Skill集 |
| 21:08 | Record & Replay | 人間の操作を見せて再利用可能なSkillへ変換する |
| 24:51 | Computer Use / Browser Use | デスクトップ／ブラウザGUIを視覚的に操作する |

> `Versel` ではなく、正式な表記は **Vercel** です。

---

## 全体像

| 分類 | 代表例 | エージェントに追加するもの | 向いている用途 |
|------|--------|----------------------------|----------------|
| 開発プロセス | mattpocock/skills | 要件整理、設計、TDD、レビューの手順 | AI駆動開発の品質安定化 |
| 最新ドキュメント | Context7 | バージョン別API・コード例 | ライブラリ仕様の確認 |
| Webデータ | Firecrawl | 検索、抽出、クロール、操作 | 調査、RAG、サイト分析 |
| Skill配布・実践 | Vercel / skills.sh | Skillの検索・導入、React等の公式知見 | Skill導入とWeb開発 |
| 操作の記録 | Record & Replay | 実演から生成した再利用可能なSkill | 定型GUI業務 |
| GUI実行 | Computer Use / Browser Use | 画面認識、クリック、入力、検証 | APIのないアプリやWeb画面 |

---

## 1. Matt Pocock's Skills

[mattpocock/skills](https://github.com/mattpocock/skills) は、「vibe coding」ではなく実務エンジニアリングを安定して進めるためのSkill集です。巨大な一枚岩の開発手順ではなく、小さく変更しやすいSkillを組み合わせます。

2026年7月時点では、従来の `to-prd` / `to-issues` から、現在の構成へ発展しています。

| 段階 | 主なSkill | 役割 |
|------|-----------|------|
| 認識合わせ | `grill-me` / `grill-with-docs` | 曖昧な要件や設計判断を質問で詰める |
| 仕様化 | `to-spec` | 会話を仕様としてIssue trackerへ公開する |
| タスク分解 | `to-tickets` | 依存関係を持つtracer-bullet型チケットへ分解する |
| 実装 | `implement` / `tdd` | 合意した境界でTDDを回しながら実装する |
| 長期調査 | `wayfinder` / `research` | 1セッションを超える調査を分割し、一次情報を記録する |
| 品質確認 | `code-review` / `diagnosing-bugs` | 仕様と標準の2軸レビュー、体系的デバッグを行う |

### インストール

```powershell
npx skills@latest add mattpocock/skills
```

Claude Codeでは管理されたプラグインとして導入する方法もあります。

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

詳しくは [mattpocock/skills 日本語解説](dev-methods/mattpocock-skills.md) を参照してください。

---

## 2. Context7

[Context7](https://github.com/upstash/context7) は、利用中のライブラリに対応した最新・バージョン別のドキュメントとコード例を、エージェントのコンテキストへ取り込む仕組みです。

### 2つの利用形態

| 形態 | 仕組み | 特徴 |
|------|--------|------|
| CLI + Skills | Skillが `ctx7` CLIを呼ぶ | MCPなしで利用できる |
| MCP | `resolve-library-id` / `query-docs` をツールとして公開 | エージェントが必要時にネイティブ呼び出しできる |

### セットアップ

```powershell
npx ctx7 setup
```

特定バージョンやライブラリIDを明示すると、曖昧なマッチングを減らせます。

```text
Next.js 14 のMiddlewareを実装して。use context7
Supabase認証を /supabase/supabase の文書に基づいて実装して。
```

> APIキーなしでも始められる構成がありますが、公式READMEでは高いrate limitを得るため無料APIキーを推奨しています。また、公開リポジトリはMCPサーバーのソースであり、APIバックエンド・解析・クロール基盤は非公開です。

---

## 3. Firecrawl

[Firecrawl](https://github.com/firecrawl/firecrawl) は、Webを検索・取得し、LLMが扱いやすいMarkdownや構造化JSONへ変換するWeb context基盤です。2026年には、APIだけでなくSkills、Codexプラグイン、MCPとしても利用できます。

### 主な機能

| 機能 | 用途 |
|------|------|
| Search | Web検索と検索結果本文の取得 |
| Scrape | URLをMarkdown、HTML、JSON、スクリーンショットへ変換 |
| Crawl / Map | サイト全体の巡回、URL一覧化 |
| Interact | クリック、入力、待機などを行ってから抽出 |
| Agent | 必要な情報を自然言語で指定して自律収集 |
| Parse | Web上のPDF・DOCXなどから情報を抽出 |

### Skillとして導入

```powershell
npx -y firecrawl-cli@latest init --all --browser
```

用途別には、次の公式配布物があります。

- [firecrawl-codex-plugin](https://github.com/firecrawl/firecrawl-codex-plugin) — Codex向けに検索・抽出・クロール等のSkillをまとめたプラグイン
- [firecrawl-claude-plugin](https://github.com/firecrawl/firecrawl-claude-plugin) — Claude Code向けSkill
- [firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) — MCP互換クライアント向け
- [firecrawl-workflows](https://github.com/firecrawl/firecrawl-workflows) — 調査レポート、SEO監査、QA、ナレッジベース等の成果物指向Skill

> Context7が「ライブラリ文書の取得」に特化するのに対し、Firecrawlは「一般のWebを検索・抽出・操作する」ための基盤です。

---

## 4. Vercel：Skills配布基盤と公式Skill集

Vercel周辺には、役割の異なる2つのプロジェクトがあります。

### vercel-labs/skills

[vercel-labs/skills](https://github.com/vercel-labs/skills) は、Agent Skillsを検索・インストールする `npx skills` CLIの公式リポジトリです。[skills.sh](https://skills.sh/) が公開Skillの検索入口になります。

```powershell
npx skills find react
npx skills add vercel-labs/agent-skills
```

### vercel-labs/agent-skills

[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) は、Vercel公式のWeb開発向けSkill集です。

| Skill | 主な用途 |
|-------|----------|
| `vercel-optimize` | Vercelのコスト、性能、キャッシュ、Functions利用状況を監査 |
| `react-best-practices` | React / Next.jsの性能ルールを適用 |
| `web-design-guidelines` | アクセシビリティ、性能、UXを監査 |
| `writing-guidelines` | Vercelの文書作成ルールでレビュー |
| `react-native-guidelines` | React Native / Expoの性能・設計を確認 |
| `react-view-transitions` | React View Transition APIを実装 |
| `composition-patterns` | boolean propsの増殖を避ける構成へ改善 |
| `vercel-deploy-claimable` | 会話から譲渡可能なVercelデプロイを作成 |

> Next.js固有のAgent Skillsは、バージョンとのずれを防ぐため [vercel/next.js の `skills` ディレクトリ](https://github.com/vercel/next.js/tree/canary/skills) へ移動しています。

---

## 5. Codex Record & Replay

[Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) は、ユーザーがMac上で行う作業をCodexに見せ、その実演から再利用可能なSkillを作成する機能です。単純な座標マクロではなく、手順の意図・入力・成功条件を整理したSkillを生成し、再実行時には利用可能なツールを選択します。

### 向いている作業

- 経費申請、駐車場予約などの定型業務
- 設定済みIssueの作成
- 動画の公開
- 定期レポートのダウンロード
- 手順は安定しているが、文章で説明するより見せた方が早い作業

### 重要な条件

- 2026年7月時点では **macOSで利用可能**
- 初期提供地域からEEA、英国、スイスは除外
- **Computer Useが有効**であることが前提
- `requirements.toml` で `[features].computer_use = false` の場合は利用不可
- 複数Skill、MCP、コネクタ、配布メタデータまでまとめる場合はPlugin化が適する

---

## 6. Computer Use / Browser Use

[Computer Use](https://learn.chatgpt.com/docs/computer-use) は、CodexまたはChatGPT WorkがGUIを見て、クリック、入力、メニュー操作、画面検証を行う機能です。CLIやMCPでは届かないデスクトップアプリや、APIのない画面操作に使います。

### Browser Useとの関係

| 機能 | 操作対象 | 特徴 |
|------|----------|------|
| Built-in browser | ChatGPT内の独立ブラウザプロファイル | 通常のブラウザとはCookieやログイン状態を共有しない |
| Computer Use in browser | 組み込みブラウザ上のWeb UI | ページを開く、クリック、入力、スクリーンショット、結果確認 |
| Chrome連携 | ユーザーが許可したChrome環境 | ログイン済みサイトを扱えるが、許可範囲を絞る必要がある |
| Desktop Computer Use | macOS / Windowsアプリ | APIのないGUI操作、設定変更、GUI固有バグの再現 |

### OSごとの差

- **macOS** — Screen RecordingとAccessibility権限が必要。対応構成ではバックグラウンド利用やLocked useがある。
- **Windows** — アクティブなデスクトップを前景で操作するため、実行中はポインターやキーボード操作を占有する。

> 対象サービスに専用Plugin、コネクタ、MCPがある場合は、データ取得や反復処理では構造化された連携を優先します。Computer Useは、画面を見なければ判断・操作できない場面に絞ると安定します。

---

## 使い分け

| やりたいこと | 第一候補 |
|--------------|----------|
| 最新のReact / AWS SDK等の使い方を知りたい | Context7 |
| 複数サイトを調査し、MarkdownやJSONにしたい | Firecrawl |
| React / Next.jsコードを公式ルールで監査したい | Vercel Agent Skills |
| 要件整理からTDD・レビューまでの開発手順を改善したい | Matt Pocock's Skills |
| 毎回同じGUI操作をSkill化したい | Record & Replay |
| APIのないデスクトップ／Web画面を直接操作したい | Computer Use / Browser Use |

---

## 参考リンク

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [upstash/context7](https://github.com/upstash/context7)
- [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- [OpenAI Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)
- [OpenAI Computer Use](https://learn.chatgpt.com/docs/computer-use)

---

> **更新基準日：2026年7月22日**。Skillの名称、導入方法、提供地域は変わる可能性があるため、導入時は各公式リンクを確認してください。
