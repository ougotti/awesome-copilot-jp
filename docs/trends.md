# Agent Skills・MCP・GUI 自動化の最新動向

> **対象ツール**: ツール横断 ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-21

> Agent Skills は `SKILL.md` だけで完結する仕組みから、MCP、Web データ取得、デプロイ、Computer Use と組み合わさる実行基盤へ広がっています。本ページは、現在注目度の高いテーマを公式情報に基づいて整理する**常設ページ**です。内容は冒頭の「最終更新」日時点の情報で、動向が変わるたびに本ページを改訂します。

## このページの更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2026-08-21 | 10 節に Snyk「ToxicSkills」調査の定量データを追加（一次記事を取得して検証）。MCP allowlists / managed settings の適用対象に JetBrains（2026-08-18 発表）を追記 |
| 2026-08-21 | 9 節に「ハーネスエンジニアリングという実践」を追加（Mitchell Hashimoto / OpenAI の 2026-02 の記事） |
| 2026-08-18 | 9 節に QM（Y Combinator の OSS ハーネス）を追加。ハーネスとコーディングツールの層関係、Skill の共有モデル、3 つのセキュリティポスチャを整理 |
| 2026-08-17 | 「10. Skill / Plugin のセキュリティ」「11. Skill が動く場所の広がり」「12. MCP の次期仕様」を新設。8 節を仕様原文で検証し、マニフェストの記述・MCP 設定の位置・可搬性の説明を訂正 |
| 2026-08-13 | 「Agent Plugins 1.0.0」を追加（マルチベンダー共通エージェント設定標準） |
| 2026-08-13 | 「AIエージェントの実行基盤（ハーネス）」を追加（Microsoft Copilot Studio を例に解説） |
| 2026-08-01 | 「Skill の発見・配布・更新」を追加（`gh skill` / Agent Finder・ARD / Copilot Plugins） |
| 2026-07-29 | 常設ページ化（旧タイトル「2026年7月版」）。ガイド全体の更新は [更新履歴（CHANGELOG）](../CHANGELOG.md) を参照 |
| 2026-07-22 | 初版公開（Matt Pocock's Skills / Context7 / Firecrawl / Vercel / Record & Replay / Computer Use の6テーマ） |

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

> 「[7. Skill の発見・配布・更新](#7-skill-の発見配布更新)」以降は動画チャプター外の追補です。[配布と発見の仕組み](#7-skill-の発見配布更新)、[共通パッケージ標準](#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準)、[実行基盤](#9-aiエージェントの実行基盤ハーネス)、[導入時の安全性](#10-skill--plugin-のセキュリティ)、[Skill が動く場所](#11-skill-が動く場所の広がり)、[MCP の次期仕様](#12-mcp-の次期仕様)を扱います。

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
| 発見・配布・更新 | `gh skill` / Agent Finder / Copilot Plugins | Skillを探す・固定する・組織へ配る仕組み | 導入後の運用と組織標準化 |
| 業界標準 | Agent Plugins 1.0.0 | `SKILL.md` / `mcp.json` の共通パッケージ形式 | マルチベンダー間のSkill・MCP設定共有 |
| 実行基盤（ハーネス） | Microsoft Copilot Studio / QM | エージェントを動かす裏側の仕組みを理解する | エージェント設計・運用の全体把握 |
| 安全性 | `gh skill preview` / MCP allowlists | 導入前の内容確認と、組織での許可範囲の限定 | 業務利用・組織展開の前提 |
| 実行される場所 | Copilot code review / IDE の Skill 管理 | 対話の外（レビュー・IDE の常設機能）での実行 | 規約の自動適用と定常運用 |

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

skills.shで公開されている注目スキル集の一覧と導入方法は、**[skills.sh ガイド](dev-methods/skills-sh.md)** を参照してください。

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

## 7. Skill の発見・配布・更新

> `gh skill` / Agent Finder・ARD / Agent Plugins 1.0

ここまでの 6 テーマが「どんな Skill があるか」だとすれば、本節は **「Skill をどう探し、安全に導入し、更新・固定・配布するか」** です。この運用面を埋める仕組みが 3 つ揃いました。

| 仕組み | 役割 | 提供元 | 状態 |
|--------|------|--------|------|
| `gh skill` | GitHub CLI による Skill のライフサイクル管理（検索・確認・導入・更新・公開） | Official（GitHub） | Preview（2026-04-16 提供開始、GitHub CLI v2.90.0 以降） |
| Agent Finder / ARD | 必要になった時点で MCP サーバー・Skill・Canvas・Agent・Tool を Registry から発見する | Official（GitHub） | GA（2026-06-17 提供開始、全 Copilot プラン） |
| Agent Plugins 1.0 | Agent Skills と MCP サーバーを 1 つの配布単位にまとめる**ベンダー中立のオープン標準** | Official（複数ベンダー共同の標準） | GA（2026-08-06 仕様公開、GitHub 実装は 2026-08-12） |

---

### 7-1. `gh skill` — Skill のライフサイクル管理

GitHub CLI v2.90.0 以降で利用できます。GitHub Copilot、Claude Code、Cursor、Codex、Gemini CLI など多数の Agent Host に対応し、`--agent` で指定したホスト固有のディレクトリへ Skill を配置します（`gh skill install --help` で全対応ホストを確認できます）。

#### 探す・中身を見る

```powershell
gh skill search terraform
gh skill preview github/awesome-copilot documentation-writer
```

`search` は GitHub Code Search API で公開リポジトリの `SKILL.md` を検索し、名前や説明がクエリに一致する Skill を関連度順に返します（`--owner` で検索対象を特定ユーザー／組織に絞り込み可能）。`preview` は **インストールせずに `SKILL.md` の内容をターミナルで確認する**ためのコマンドです。

#### 導入する

```powershell
gh skill install github/awesome-copilot documentation-writer --agent claude-code --scope user
gh skill list
```

| フラグ | 意味 |
|--------|------|
| `--agent` | インストール先エージェントを指定する値。例: `github-copilot`（非対話実行時の既定）、`claude-code`、`cursor`、`codex`、`gemini-cli` 等 |
| `--scope` | `project`（現在の Git リポジトリ内。既定）または `user`（ホームディレクトリ、どこからでも利用可） |
| `--pin <string>` | 指定した git タグまたはコミット SHA に固定し、以降 `update` の対象から外す |
| `@<VERSION>` | Skill 名の後ろに付けて、特定のタグ・ブランチ・コミット SHA を指定して導入・プレビュー |

バージョンを指定しない場合、`install` はリポジトリの最新タグ付きリリース、無ければデフォルトブランチの HEAD を解決します。

#### 更新する

```powershell
gh skill update --all
```

`install` 時に、取得元リポジトリ・ref・**git tree SHA** が Skill 自身の `SKILL.md` frontmatter へ書き込まれます。この情報は Skill ファイルに同梱されるため、コピー・移動しても追跡が失われません。`update` はローカルとリモートの tree SHA を比較して実際に内容が変わった Skill だけを更新し、`--pin` した Skill は通知のみでスキップします（対象に含めるには `--unpin`）。

#### 公開する

```powershell
gh skill publish --dry-run
gh skill publish --fix
```

`publish` は Skill 名の命名規則やディレクトリ名との一致、必須 frontmatter（`name` / `description`）の有無など、[Agent Skills 仕様](https://agentskills.io/specification) への適合を検証します。`--dry-run` は公開せず検証のみ、`--fix` はインストール時に混入したメタデータ（`metadata.github-*`）を公開せずに取り除きます。検証に通ると、`tag protection` ・ secret scanning ・ code scanning といったリポジトリ設定の確認と、**immutable releases**（公開後は管理者でもリリース内容を変更できなくする設定）の有効化を対話的に案内します。

#### 安全に使う

- Skill は **GitHub による検証済みではありません**。プロンプトインジェクション、隠し指示、悪意あるスクリプトが含まれ得ます。
- 導入前に `gh skill preview` で `SKILL.md` と `scripts/` を読み、想定外のネットワーク通信や作業ツリー外への書き込みがないか確認してください。
- タグは後から差し替えられる可能性があるため、**コミット SHA での固定が最も安全**です。配布側で immutable releases を有効にすると、タグ指定でも内容が変わらなくなります。

---

### 7-2. Agent Finder / ARD — 必要な時に見つける

Agent Finder は、自然言語で書いたタスクに応じて、MCP サーバー・Skill・Canvas・Agent・Tool を Registry（インデックス）から検索し、候補をランキングして提示する仕組みです。**すべてを常時コンテキストへ詰め込まない**ため、Context Window の消費とツール選択の誤りを減らせます。

| 特徴 | 内容 |
|------|------|
| 発見と接続は別 | 候補を提示するだけで、勝手に接続・インストールしない |
| 対象リソース | MCP servers / Skills / Canvases / Agents / Tools |
| 組織制御 | Enterprise の managed settings で、発見・利用してよいリソースを限定できる |
| 対応プラン | 全 GitHub Copilot プラン |

#### ARD（Agentic Resource Discovery）

Agent Finder は、Google・Microsoft・GitHub・Hugging Face・GoDaddy などが策定するオープン仕様 **ARD** の実装です。仕様は 2 つの構成要素からなります。

| 構成要素 | 役割 |
|---------|------|
| Catalog | 提供元が自ドメインの `/.well-known/ai-catalog.json` に、公開するリソースを機械可読な形で掲載する |
| Registry | 複数の Catalog を集約し、タスクの意図に基づく検索を提供する |

Catalog には、Skill だけでなく OpenAPI で記述したツール、A2A エージェント、下位 Catalog への参照も含められます。オープン仕様であるため、社内向けの Private Registry を立てて、自組織の Skill カタログを同じ方式で運用することもできます。

#### skills.sh・GitHub 検索との関係

| 発見手段 | 対象範囲 | 実行主体 |
|---------|---------|---------|
| [skills.sh](https://skills.sh/) / `npx skills find` | 公開 Skill の Web ディレクトリ | 人が探す |
| `gh skill search` | GitHub 上の公開 `SKILL.md` | 人が探す |
| Agent Finder / ARD | Catalog を公開したリソース（公開・社内問わず） | エージェントがタスク実行中に探す |

> 人が事前に選ぶのが前者 2 つ、エージェントが必要になった時点で探すのが Agent Finder、という違いです。

---

### 7-3. GitHub Copilot Plugins — まとめて配る

Copilot Plugin は、`plugin.json` を持つディレクトリに Custom Agents・Skills・Hooks・MCP サーバー設定・LSP サーバー設定をまとめた配布単位です。Marketplace（`marketplace.json` を置いた Git リポジトリ）から導入します。

```powershell
copilot plugin marketplace list
copilot plugin marketplace browse awesome-copilot
copilot plugin install database-data-management@awesome-copilot
copilot plugin list
copilot plugin update database-data-management
```

Copilot CLI には `copilot-plugins`（GitHub 公式コレクション）と `awesome-copilot` が既定で登録されています。リポジトリの `.github/copilot/settings.json` に `enabledPlugins` を書けば、そのリポジトリの開発者全員へ同じ構成を適用できます。

**→ 構成・`enabledPlugins`・Claude Code Plugin との比較は [GitHub Copilot Plugins](copilot/plugins.md) を参照**

---

### 3 つの仕組みの比較

| 観点 | `npx skills` | `gh skill` | Copilot Plugin |
|------|-------------|-----------|----------------|
| 主用途 | Skill の検索・導入 | Skill のライフサイクル管理 | 複数拡張の一括配布 |
| 配布単位 | Skill | Skill | Plugin |
| 更新追跡 | CLI 依存 | provenance（git tree SHA） | Marketplace のバージョン |
| バージョン固定 | — | `--pin` / コミット SHA 指定 | Marketplace のバージョン / `source.sha`（commit SHA） |
| 対応 Host | 複数エージェント | 複数エージェント | 主に Copilot CLI / VS Code |
| 含められる要素 | Skills | Skills | Skills / Agents / Hooks / MCP / LSP |
| サプライチェーン対策 | 配布元の確認 | `preview` / pin / immutable releases | Marketplace と Enterprise ポリシー |
| 提供元 | Vercel（コミュニティ） | GitHub（公式） | GitHub（公式） |

### 使い分けの目安

| やりたいこと | 選ぶもの |
|-------------|---------|
| Skill を探して試す | `npx skills find` / `gh skill search` |
| 導入前に中身を確認する | `gh skill preview` |
| バージョンを固定して事故を防ぐ | `gh skill install ...@<コミットSHA>` または `--pin <コミットSHA>` |
| 自作 Skill を公開・配布する | `gh skill publish` |
| チーム標準の拡張一式を配る | Copilot Plugin + `enabledPlugins` |
| 組織で使えるリソースを制限する | Enterprise managed settings（Agent Finder / Plugins） |

---

## 8. Agent Plugins 1.0.0 — マルチベンダー共通のエージェント設定標準

2026 年 8 月、Amazon・Anysphere（Cursor）・Microsoft・OpenAI・Vercel が共同で **Agent Plugins 1.0.0** を公開しました。GitHub は 2026-08-12 に、VS Code・Copilot CLI・Copilot SDK・Copilot アプリでの対応を一般提供しています（全 Copilot プラン）。

Agent Plugins は、`SKILL.md`（スキル定義）と `mcp.json`（MCP サーバー設定）をひとつのパッケージにまとめ、**異なる AI エージェント間で同じ設定を共有できる共通フォーマット**です。

### 背景と位置づけ

これまでエージェントごとに設定形式が異なり、たとえば GitHub Copilot で使っているスキルを Cursor や ChatGPT に持ち込むには個別の書き直しが必要でした。Agent Plugins 1.0.0 はこの断絶を解消し、「一度書いたらどのエージェントでも使える」パッケージを目指しています。

ガバナンスは Technical Steering Committee が担い、憲章で **役職は企業ではなく個人が持ち、企業に議席を予約しない**こと、**単一ベンダーが Core Maintainer の過半数を占めないこと**が定められています。

### 対応状況（2026-08-13 時点）

| ツール | 対応状況 |
|--------|---------|
| GitHub Copilot（VS Code / CLI / Web） | 対応済み |
| Cursor | 対応済み |
| ChatGPT / OpenAI Codex | 対応済み |
| AWS Kiro | 対応済み |
| Google（Gemini 系エージェント） | 対応表明 |
| Claude Code（Anthropic） | 現時点では静観 |

### パッケージの構成

Agent Plugin パッケージの最小構成は `plugin.json`（メタデータ）と `skills/<スキル名>/SKILL.md`（スキル定義）です。

**v1 が標準化する構成要素は Skills と MCP サーバーの 2 種類だけ**で、配置場所は固定です。`plugin.json` で場所を上書きすることはできません。

| 構成要素 | 固定の配置場所 |
|---------|---------------|
| Skills | `skills/` 直下の各サブディレクトリの `SKILL.md` |
| MCP サーバー | プラグインルートの `mcp.json` |

```text
my-plugin/
├── plugin.json              # パッケージのメタデータ
├── skills/
│   └── my-skill/
│       └── SKILL.md         # スキル定義（既存の SKILL.md と同形式）
├── mcp.json                 # MCP サーバー設定（任意）
└── com.github.copilot/      # ツール独自拡張（任意・逆ドメイン名の名前空間）
```

`plugin.json` の例：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-skill-pack",
  "version": "1.0.0",
  "description": "共通スキルパック"
}
```

マニフェストで**注意が必要な点**が 2 つあります。

- **`$schema` は必須**です。値は上記の正式な識別子でなければなりません。
- **スキーマは閉じています。** 書ける最上位フィールドは `$schema` / `name` / `version` / `description` / `author` / `homepage` / `repository` / `license` / `keywords` / `extensions` の 10 個だけです。`skills` や `mcpServers` のような構成要素を指すフィールドは**仕様に存在せず**、クライアントは未知フィールドとして無視します。

Agents・Hooks・LSP など v1 が扱わない要素は、`extensions` フィールドか、逆ドメイン名の名前空間ディレクトリ（GitHub Copilot なら `com.github.copilot/`）へ置きます。

### GitHub Copilot での導入

Agent Plugins 1.0.0 対応の Copilot Plugin は、既存の `copilot plugin` コマンドでそのまま導入できます。

```powershell
copilot plugin marketplace list
copilot plugin install <plugin-name>@<marketplace>
```

VS Code では設定 UI または `.github/copilot/settings.json` の `enabledPlugins` で有効化します。詳しくは [GitHub Copilot Plugins](copilot/plugins.md) を参照してください。

### Copilot Plugins との関係

GitHub の Copilot Plugin（本ページ [7-3 節](#7-3-github-copilot-plugins--まとめて配る)）は Agent Plugins 1.0.0 に対応していますが、**Copilot Plugin なら自動的に可搬になるわけではありません**。

GitHub の実装では `$schema` は**任意**で、これを書くことが**可搬形式へのオプトイン**にあたります。

| | `$schema` を書く（可搬形式） | `$schema` を書かない（Copilot 独自形式） |
|---|---|---|
| 構成要素 | Skills と MCP サーバーのみ | Agents / Skills / Commands / Hooks / MCP / LSP |
| 配置場所 | `skills/` と `mcp.json` に固定 | マニフェストのフィールドで上書き可（`.mcp.json` 等） |
| 他エージェントでの利用 | できる | **できない** |

Copilot 独自形式は Agent Plugins の**上位互換**です。したがって Copilot Plugin をほかのエージェント（Cursor・ChatGPT 等）で使いたい場合は、`$schema` を追加し、ファイルを標準のディレクトリ構成へ整える作業が必要です。既存 Plugin をそのまま使い続ける分には**移行は不要**です。

**→ 2 つの形式の違いと移行の手順は [GitHub Copilot Plugins](copilot/plugins.md) を参照**

---

## 9. AIエージェントの実行基盤（ハーネス）

ChatGPT の「チャットに答える」段階から、タスクを自律的に実行する「エージェント時代」への移行に伴い、エージェントの裏側で動く**実行基盤（ハーネス）**への注目が高まっています。

「ハーネス（harness）」とは、AIモデルが外部ツールを呼び出したり、複数のステップを連鎖させたりするための仕組み全体を指す概念です。モデル本体とは別に、次の役割を担います。

| 役割 | 内容 |
|------|------|
| ツール呼び出し | 検索、データ取得、API 実行などをモデルの指示で動かす |
| 状態管理 | 会話履歴・タスク進捗・メモリを保持する |
| ループ制御 | 「計画 → 実行 → 評価」のサイクルを繰り返す |
| エラー処理 | ツール失敗・タイムアウトに対応し、再試行や代替ルートへ切り替える |
| 出力整形 | モデルの生成結果を次のツールや人間が扱いやすい形式に変換する |

### ハーネスエンジニアリングという実践

この領域には **ハーネスエンジニアリング（harness engineering）** という呼び名が付き、2026 年 2 月に相次いで公開された 2 本の記事を機に急速に広まりました。

1 本目は Mitchell Hashimoto（Terraform / Ghostty の作者）の [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) です。実践の定義がシンプルです。

> Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

エージェントの失敗をやり直しで済ませず、**同じ失敗が二度と起きないように環境の側を作り替える** — ルール、チェック、ガードレールを足していく営みをハーネスエンジニアリングと呼んでいます。

2 本目は OpenAI の [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) です。OpenAI 自身の報告では、3 人のチームが**コードを 1 行も手書きせず**、環境の設計 — ルール、フィードバックループ、文書構造、依存の順序 — に回ることで、約 5 か月（2025-08〜2026-01）で約 100 万行・1,500 件のマージ済み PR を出荷したとされています。

> エンジニアの仕事が「コードを書くこと」から「エージェントが確実に働ける環境を設計すること」へ移る、という主張の実証として引かれる事例です。数値は OpenAI の自己報告であり、そのまま一般化できる保証はありません。

### 実装を見る 2 つの入口

ハーネスは概念だけでは掴みにくいため、性格の異なる実装を 2 つ並べます。

| | Microsoft Copilot Studio | QM（Y Combinator） |
|---|---|---|
| 形態 | GUI・ローコードで構成する商用プラットフォーム | ソースを読める OSS（MIT） |
| 想定利用者 | 業務担当者・開発者 | 組織のプラットフォームエンジニア |
| 見えるもの | 設計の**考え方**を GUI 上で追える | 設計の**実装**をコードで追える |
| `提供元` / `状態` | Official（Microsoft） / GA | Official（Y Combinator） / **Experimental** |

### Microsoft Copilot Studio での実装例

Microsoft Copilot Studio は、ハーネスの概念を GUI で構成できるプラットフォームです。トピック（会話フロー）とアクション（ツール呼び出し）を組み合わせることで、エージェントがどのように計画を立て、ツールを順番に呼び出し、結果をユーザーへ返すかを定義できます。

| 役割 | Copilot Studio での対応 |
|------|------------------------|
| ツール呼び出し | コネクタ / Power Automate フロー / カスタム API |
| 状態管理 | 会話変数・グローバル変数 |
| ループ制御 | トピック内の条件分岐とリダイレクト |
| エラー処理 | エスカレーション・フォールバック トピック |
| 出力整形 | 応答メッセージのテンプレートと変数展開 |

### QM — ソースを読めるハーネス実装

[QM](https://github.com/yc-software/qm)（Quartermaster）は、Y Combinator が 2026 年 7 月末に MIT ライセンスで公開したハーネスです。同社が会計・法務・イベント・エンジニアリングの業務で内部利用してきたものを、そのまま OSS にしたと説明されています。

README の一文が性格をよく表しています。

> A multiplayer agent harness for work. In Slack and on the web.

**個人アシスタントではなく、会社単位で使うこと**を前提にしている点が特徴です。従業員はそれぞれ隔離されたワークスペースを持って独立して作業し、同時に Slack のチャンネル・グループ・プロジェクトで同じエージェントと協働できます。

| 分離の単位 | 何が分かれるか |
|-----------|---------------|
| 人ごと・部屋ごとのスコープ | メモリ、ファイル、キーチェーンの見え方、権限、cron、Web アプリ、**永続サンドボックス** |

#### ハーネスとコーディングツールの関係

QM でいちばん参考になるのは、**Pi・OpenCode・Codex・Claude Code が同じコアを駆動する**という設計です。ハーネスを差し替えても中心の仕組みは変わりません。

つまり本ガイドがツール別に解説している Claude Code や Codex は、**ハーネスから見れば差し替え可能な部品**にあたります。ハーネスはその上位にあり、認証・スコープ・権限・スケジュール・監査を引き受けます。

| 層 | 担うもの |
|----|---------|
| ハーネス（QM のコア） | 認証、スコープ、権限、配送、cron、監査、永続化 |
| コーディングツール（Claude Code / Codex / OpenCode / Pi） | 実際のエージェントループ |
| モデル | 推論 |

構成は、ヘッドレスなコアに Postgres（セッション・メモリ・キュー）とスコープ別サンドボックスを組み合わせた形です。Web UI・管理画面・公開ポータルはコアの HTTP API 上のプラグイン、Slack もオプションのプラグインとして扱われます。**ツールの面は小さく固定**されており、そのうちの `execute` がスコープ専用サンドボックス（インストールしたものが残る「永続的なコンピューター」）でコマンドを実行します。

> ハーネス・セッションストア・サンドボックス・メモリといった基盤はすべてインターフェースの背後にあり、実装は 1 つの結線ファイルで差し替えられます。「ハーネスとは何を抽象化する層なのか」を読み取る教材として有用です。

#### Skill の扱い — 4 つ目の配布モデル

QM の Skills は**スコープが所有し、付与（grant）によって共有**されます。管理者の承認で組織全体へ昇格させることができ、**git リポジトリから skill pack としてインポート**することもできます。

[7 節](#7-skill-の発見配布更新)で扱った `npx skills`・`gh skill`・Agent Plugins が「配る」仕組みだとすれば、QM のそれは**組織の中で誰に見せるかを制御する**仕組みです。配布と権限を同じ軸で扱っている点が異なります。

#### セキュリティポスチャ — 標準が空けた穴の埋め方

[10 節](#10-skill--plugin-のセキュリティ)で述べるとおり、Agent Plugins 1.0.0 は信頼モデル・権限・サンドボックスを定義せず、**安全性の担保は各クライアントに委ねられています**。QM はその負担を実際に引き受けた実装例として読めます。

組織は次の 3 つから 1 つを選び、より狭いスコープはそれを**強める方向にのみ**変更できます。

| ポスチャ | 挙動 |
|---------|------|
| **Strict** | すべてのツール呼び出しで人間の承認を待つ（副作用のないターン終了 2 つを除く） |
| **Auto**（既定） | **出所ラベルの付いた外部データ**とツール結果を、モデルへ渡す前に分類器で選別する。選別を自前のプロキシへ向けることもできる |
| **Dangerous** | 内容の選別もツール呼び出し間の停止もしない |

注目すべきは、**再帰的削除や破壊的な SQL などに対する事前宣言のコマンドポリシーが、Dangerous を含むすべてのポスチャで適用される**点です。「最も緩い設定でも外せない下限」を持たせる設計は、Skill や Plugin を組織へ入れる際の考え方としても参考になります。

#### 導入の前提と、成熟度についての但し書き

QM は**組織向けソフトであり、デスクトップアプリではありません**。運用者自身のクラウドアカウント、Postgres、そしてインフラを扱える担当者が前提になります。個人で試す類のものではない点に注意してください。

`SECURITY.md` は限界を率直に書いており、導入判断ではこちらのほうが重要です。

> It is early, experimental software: that design goal is not a promise that data cannot leak, a certification, or a substitute for a deployment-specific security review.

- **公開・マルチテナント向けの堅牢な境界ではない**と明記されている
- **悪意ある、または侵害された運用者からはデプロイを守らない**
- **組織管理者は権限を持つコンテンツ読み取り者**であり、単なるポリシー管理者ではない。管理者の閲覧はスコープに従い監査されるが、利用者の追加承認は要らない

最後の 1 点は、社内へ展開する際に事前に合意しておくべき性質です。

> 初期段階の OSS のため、構成・コマンド・要件は変わります。導入時は必ず [リポジトリ](https://github.com/yc-software/qm) の最新の記述を確認してください。

### ハーネスを意識する理由

- **モデルの性能だけでは不十分**: 同じモデルでも、ハーネス設計の差が出力品質・コスト・レイテンシを大きく左右する。
- **障害点の特定**: 問題が「モデルの判断ミス」か「ツール呼び出しの失敗」かを切り分けるには、ハーネスの構造を理解する必要がある。
- **再利用と標準化**: スキルや MCP サーバーも、ハーネスに組み込まれる部品として設計すると再利用しやすい。
- **安全性の実装先**: 標準が定めていない権限・承認・サンドボックスは、結局ハーネス側で決まる（[10 節](#10-skill--plugin-のセキュリティ)）。組織へ展開するなら、モデルやツールの選定と同じ比重でハーネスの既定値を確認する。

> 詳しくは [なぜ今、AI に「ハーネス」が必要なのか（ギークフジワラ）](https://www.geekfujiwara.com/tech/powerplatform/8591/) を参照してください。

---

## 10. Skill / Plugin のセキュリティ

[8 節](#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準)のとおり配布の仕組みは一気に整いましたが、**「入れてよい Skill か」を判断する仕組みは追いついていません**。2026 年 8 月時点の実像は、**標準化が進んだのは配布形式であり、安全性の担保は各クライアント任せのまま**という点にあります。

Skill と Plugin は「読み込ませる文書」ではなく、**エージェントの振る舞いを書き換える指示**であり、スクリプトや MCP 接続を同梱できます。ライブラリの依存追加と同じ慎重さが必要です。

### 10-1. オープン標準がまだ定義していないこと

Agent Plugins 1.0.0 は可搬なパッケージ形式を定めた一方で、安全性に関わる項目を**明示的に将来版へ先送り**しています。以下は仕様リポジトリの [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) に記載された内容です。

| 未定義の領域 | v1.0.0 の状態 | 実務上の意味 |
|-------------|--------------|-------------|
| 信頼モデル・権限・サンドボックス | 「信頼モデル、権限システム、サンドボックス要件を定義しない」 | Plugin が何にアクセスするかをマニフェストで宣言する欄がなく、クライアントが能力を制限する標準的な方法もない |
| **出自の検証** | 「Plugin の出自や完全性をクライアントや利用者が検証する方法を規定しない」 | **暗号署名の検証は将来版の検討事項**。配布物が途中で差し替わっていないことを、標準の仕組みでは確認できない |
| シークレットの扱い | 「機微な値をどう渡し、保存し、スコープを切るかを規定しない」 | MCP サーバーの API キー等の受け渡しはクライアント任せ |
| 組織ポリシー | 大規模展開時のポリシー強制を扱わない | 許可リストや承認フローは各ツールの独自機能に依存する |
| 監査ログ | インストール・更新等のイベントスキーマは標準化されていない | 導入履歴の追跡方法がツールごとに異なる |

誤解しやすい点を 2 つ補足します。

- 仕様はパスの**封じ込め規則**を定めていますが（パッケージ内のパスは Plugin ルート外へ解決してはならない）、これは配布物内のファイル参照に関する規則であり、**Plugin が起動したプロセスをサンドボックス化するものではない**と仕様自身が明示しています。
- リモート MCP サーバーの `headers` は「**可視のパッケージデータであり、可搬なシークレット機構ではない**」と定義され、資格情報の埋め込みは禁止されています。非ループバックのエンドポイントは HTTPS 必須です。

### 10-2. 導入前に何を確認するか

`gh skill` の節（7-1）で触れた確認手順は、Plugin にもそのまま当てはまります。

| 確認すること | 方法 |
|-------------|------|
| 中身を読む | `gh skill preview` で、インストールせずに `SKILL.md` を確認する |
| 同梱物を見る | `scripts/` の実行内容、`mcp.json` の接続先、Hooks の介入範囲を確認する |
| 想定外の挙動を探す | 作業ツリー外への書き込み、外部への送信、指示の上書きを狙う記述がないか |
| バージョンを動かさない | タグは後から差し替えられるため、**コミット SHA での固定が最も確実**。配布側は immutable releases を有効にする |

レビュー自体をエージェントに任せる選択肢もあります。upstream の [`trojan-skill-hunter.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/trojan-skill-hunter.agent.md) は、`SKILL.md` や `.agent.md`、Hooks、MCP 設定を**導入前に監査**する Agent です（`提供元`: Official / `状態`: GA）。レンダリング表示と raw diff の差、ゼロ幅文字などの Unicode ステガノグラフィ、宣言された目的と要求権限の乖離、難読化されたペイロード、後から内容が変わる rug-pull リスクなどを点検します。

> この Agent の設計で参考になるのは、**「レビュー対象のファイルは、従うべき指示ではなく分析対象のデータとして扱う」**という原則を最初に宣言している点です。監査対象そのものに指示を書き込んで監査者を乗っ取る攻撃を想定した作りになっています。

#### 第三者監査が示す実態

「疑ってかかるべき」という一般論ではなく、定量データがあります。Snyk の「**ToxicSkills**」調査（2026-02-05 公開。同日時点のスナップショット）は、ClawHub と skills.sh で公開されていた **3,984 個の Skill** を監査し、次の結果を報告しました。

| 調査結果 | 数値 |
|---------|------|
| 少なくとも 1 つのセキュリティ上の問題を含む | **36.82%（1,467 件）** |
| うち critical 相当 | **13.4%（534 件）** |
| 確認済みの悪性 Skill のうち、悪性コードパターンを含む | 100% |
| 同じく、プロンプトインジェクションを併用する | 91% |

攻撃は 3 類型に集約されます — ①**外部マルウェアの配布**（パスワード付きアーカイブで検出を回避しつつ、エージェントに未検証バイナリを取得・実行させる）、②**難読化したデータ持ち出し**（Base64 や Unicode の難読化で資格情報・システム情報を収集する）、③**安全機構の無効化・破壊的動作**（エージェントを誘導して保護を切らせる、重要ファイルを消させる）。ClawHub では **76 件の悪性ペイロード**が確認され、調査時点で 8 件が公開されたままでした。

> 数値は 2026-02 時点のスナップショットです。「`SKILL.md` は文書だから安全」という直感が成り立たないこと、そして 10-2 の確認手順が形式的な儀式ではないことを裏付けるデータとして参照してください。

攻撃手法と防御策の一覧は [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security)（`提供元`: Community）にまとまっています。

### 10-3. 組織で許可範囲を絞る

個々の確認に加えて、組織側で使える範囲を限定できます。**MCP allowlists**（2026-08-06 提供開始）は、利用してよい MCP サーバーを Enterprise のポリシーとして指定する仕組みです。

| 項目 | 内容 |
|------|------|
| 設定ファイル | `copilot/managed-settings.json` |
| キー | `allowedMcpServers`（許可）/ `deniedMcpServers`（拒否） |
| 指定方法 | `serverUrl`（リモート。ワイルドカード可）/ `serverCommand`（ローカル）/ `serverName`（表示名） |
| 適用対象 | Copilot アプリ / Copilot CLI / VS Code / GitHub Copilot for JetBrains（2026-08-18 追加） |
| 設定者 | Enterprise owner が、対象組織の `.github-private` リポジトリで設定する |

Plugin 側も同じ `managed-settings.json` の `enabledPlugins`・`extraKnownMarketplaces`・`strictKnownMarketplaces` で統制できます。2026-08-18 には GitHub Copilot for JetBrains も同じ `managed-settings.json` による統制対象に加わり、MCP の許可リスト・Plugin の marketplace 制限・エージェントの承認バイパス禁止（`permissions.disableBypassPermissionsMode`）を中央設定できるようになりました。Claude Code もこれらに相当する設定（`additionalMarketplaces` / `allowedMarketplaces` を同義エイリアスとして追加）を持っており、**設定キー名がツール間で近づき始めています**。

---

## 11. Skill が動く場所の広がり

2026 年前半までは「エージェントとの**対話中**に Skill を使う」のが中心でしたが、7〜8 月にかけて**対話の外**へ広がりました。同じ `SKILL.md` を、レビューや IDE の常設機能として効かせられるようになっています。

### 11-1. コードレビューに効かせる

**Copilot code review** が Agent Skills と MCP に対応し、2026-07-29 に一般提供となりました。チーム独自のコーディング規約や社内ツールを、レビューの判断材料として持ち込めます。

| 項目 | 内容 |
|------|------|
| Skill の配置 | リポジトリの `.github/skills/<スキル名>/SKILL.md` |
| MCP の設定 | リポジトリ設定 → Copilot → MCP servers |
| 資格情報 | リポジトリ設定 → Secrets and variables → **Agents** |
| 重要な制約 | code review からの **MCP ツール呼び出しは read-only に限定**される |
| 既定で有効 | GitHub MCP / Playwright MCP |
| 対象プラン | Pro / Pro+ / Business / Enterprise |

> **配置先を間違えやすい点**: ここで使う `.github/skills/` は、`gh skill install` が Skill を置く先（エージェントホストごとのディレクトリ）とは**別系統**です。レビューに効かせたい Skill は、リポジトリへコミットする必要があります。

レビューコメントには、Skill や MCP のコンテキストを使ったかどうかが表示されます。

あわせて **レビューの深さ**を選べるようになりました（2026-08-07 一般提供）。

| レベル | 用途 |
|--------|------|
| `Lite` | 単純な変更へのフィードバック |
| `Balanced` | より高い推論能力での分析が必要な変更 |

レビューごとに選べるほか、組織管理者が既定値を設定できます（組織設定 → Copilot → Copilot code review）。使用されたレベルは、タイムラインと PR の概要コメントに表示されます。

### 11-2. IDE・CLI 側の対応状況

各ツールが Skill / Plugin を「設定ファイルを手で置くもの」から「**UI で管理するもの**」へ移しつつあります。

| ツール | 押さえておく点 |
|--------|---------------|
| VS Code | 既存の **prompt ファイルを Skill へ変換**できる（AI Customizations 画面）。Agents window から Copilot / Claude / Codex のセッションを Git worktree で起動でき、サブエージェントのモデル・経過時間・ツール呼び出しを追跡できる |
| Visual Studio | Copilot CLI と同じ Copilot SDK を基盤とする Agent。**.NET / Azure チームが作成したビルトイン Skill** を同梱 |
| JetBrains | Marketplace またはソースリポジトリから Plugin を導入する UI。**Claude を agent provider に指定**して、カスタムエージェント・Skill・Instructions を利用できる |
| Codex | Agent Plugins に対応。**ローカル / 個人 / ワークスペース / リモート**のカタログを横断検索できる。Cursor 管理の Skill をインポートできる |
| Claude Code | Plugin marketplace が **GitLab に対応**（nested subgroup を含む）。`plugin validate` が `SKILL.md` の frontmatter の解析失敗を検出する |

> **実務上の落とし穴**: Codex は、コンテキストが逼迫すると Skill カタログを切り詰め、その旨を警告します。Skill は入れるほど良いわけではなく、**使う分だけ有効にする**ほうが安定します。

> 各ツールの機能は月次で更新されます。詳細と最新状態は、末尾の公式リリースノートを確認してください。

---

## 12. MCP の次期仕様

Skill と並ぶもう一方の柱である MCP も、2026-07-28 版の仕様で構造が変わりました。

| 変更点 | 内容 |
|--------|------|
| **stateless core** | セッションと初期化ステップを廃止。クライアントとサーバーのハンドシェイクを並列化できる |
| マルチラウンドトリップ要求 | **elicitation**（実行途中でユーザーへ追加入力を求める）に対応するリモートサーバーが増える |
| 認可の強化 | OAuth / OIDC |
| 拡張 | Apps・Tasks 向けのバージョン付き拡張 |

GitHub MCP Server は正式リリース前に先行対応済みです。**tier 1 SDK が後方互換を保っているため、利用者側の作業は不要**です。

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
| Skillを検索・固定・公開したい | `gh skill` |
| チームや組織へ拡張一式を配布したい | Copilot Plugins |
| 複数エージェント間でSkill・MCP設定を共有したい | Agent Plugins 1.0.0 対応パッケージ |
| 必要な時だけツールを見つけさせたい | Agent Finder / ARD |
| エージェントの内部動作・実行基盤を理解したい | ハーネスの概念（本ページ 9 節） |
| ハーネスの実装をコードで読みたい | QM（本ページ 9 節） |
| 組織全体で使うエージェント基盤を検討したい | QM（要: 自前のクラウド・Postgres・担当者） |
| 導入してよい Skill か判断したい | `gh skill preview` ＋ コミット SHA 固定 |
| 組織で使える MCP サーバーを限定したい | MCP allowlists（managed settings） |
| チームの規約をコードレビューに効かせたい | Copilot code review ＋ `.github/skills/` |
| 手持ちの prompt ファイルを Skill にしたい | VS Code の AI Customizations から変換 |

---

## 参考リンク

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [upstash/context7](https://github.com/upstash/context7)
- [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
- [OpenAI Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)
- [OpenAI Computer Use](https://learn.chatgpt.com/docs/computer-use)

### Skill の発見・配布・更新（本ページ 7 節）

- [Manage agent skills with GitHub CLI](https://github.blog/changelog/2026-04-16-manage-agent-skills-with-github-cli/) — `gh skill` の提供開始（公式）
- [gh skill マニュアル](https://cli.github.com/manual/gh_skill) — サブコマンドとフラグ（公式）
- [Adding agent skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) — Copilot への Skill 追加（公式）
- [Agent finder for GitHub Copilot now available](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/) — Agent Finder の提供開始（公式）
- [ARD Specification](https://agenticresourcediscovery.org/spec/) — Agentic Resource Discovery 仕様（公式）
- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — Plugin の概念と構成（公式）
- [Finding and installing plugins for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) — Plugin の導入手順（公式）
- [GitHub Copilot Plugins 日本語解説](copilot/plugins.md) — 本ガイド内の詳細ページ

### Agent Plugins 1.0.0（本ページ 8 節）

- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) — 仕様リポジトリ（公式）
- [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) — 仕様本文（公式）
- [Technical Charter](https://github.com/agentplugins/agent-plugins-spec/blob/main/GOVERNANCE.md) — ガバナンス（公式）
- [MAINTAINERS](https://github.com/agentplugins/agent-plugins-spec/blob/main/MAINTAINERS.md) — Core Maintainer 一覧（公式）
- [Agent Skills specification](https://agentskills.io/specification) — `SKILL.md` 形式の仕様（公式）
- [Agent Plugins 1.0 in VS Code, Copilot CLI, and the Copilot app](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app) — GitHub Changelog（公式）
- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — `plugin.json` のフィールド定義（公式）
- [「Agent Plugins 1.0.0」発表、異なるAIエージェント間でもスキルやMCPサーバ設定が共通化へ](https://www.publickey1.jp/blog/26/agent_plugins_100aimcpopenaiawsgoogle.html) — Publickey（解説記事）

### AIエージェントの実行基盤（ハーネス）（本ページ 9 節）

- [なぜ今、AI に「ハーネス」が必要なのか](https://www.geekfujiwara.com/tech/powerplatform/8591/) — ハーネスの概念と Microsoft Copilot Studio での実装例（ギークフジワラ）
- [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) — Mitchell Hashimoto によるハーネスエンジニアリングの定義（一次情報）
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI の実証報告（公式）
- [yc-software/qm](https://github.com/yc-software/qm) — QM のリポジトリと README（公式）
- [QM の SECURITY.md](https://github.com/yc-software/qm/blob/main/SECURITY.md) — 脅威モデル・運用者の前提・既知の限界（公式）

### Skill / Plugin のセキュリティ（本ページ 10 節）

- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Snyk ToxicSkills study](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) — ClawHub / skills.sh の 3,984 Skill の監査結果（Snyk・2026-02-05）
- [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) — MCP 許可リスト（公式）
- [Enterprise managed settings in GitHub Copilot for JetBrains](https://github.blog/changelog/2026-08-18-enterprise-managed-settings-in-github-copilot-for-jetbrains/) — JetBrains への managed settings 拡大（公式）
- [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) — 攻撃手法と防御策の一覧（コミュニティ）
- [Agents 一覧](copilot/agents.md) — 導入前監査に使える `trojan-skill-hunter` の解説（本ガイド）

### Skill が動く場所・MCP 次期仕様（本ページ 11・12 節）

- [Copilot code review: Agent skills and MCP now generally available](https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available/) — レビューでの Skill / MCP 対応（公式）
- [Copilot code review effort levels are generally available](https://github.blog/changelog/2026-08-07-copilot-code-review-effort-levels-are-generally-available/) — レビューの深さの選択（公式）
- [GitHub MCP Server supports the next MCP specification](https://github.blog/changelog/2026-07-23-github-mcp-server-supports-the-next-mcp-specification/) — MCP 次期仕様への対応（公式）
- [GitHub Copilot in Visual Studio Code, July 2026 releases](https://github.blog/changelog/2026-07-30-github-copilot-in-visual-studio-code-july-2026-releases/) — VS Code の更新（公式）
- [GitHub Copilot in Visual Studio — July update](https://github.blog/changelog/2026-07-30-github-copilot-in-visual-studio-july-update/) — Visual Studio の更新（公式）
- [GitHub Copilot for JetBrains expands BYOK capabilities](https://github.blog/changelog/2026-07-14-github-copilot-for-jetbrains-expands-byok-capabilities/) — JetBrains の Plugin 管理と agent provider（公式）
- [Claude Code changelog](https://code.claude.com/docs/en/changelog) — Claude Code の更新（公式）
- [Codex changelog](https://learn.chatgpt.com/docs/changelog) — Codex の更新（公式）

---

> 本ページの内容は冒頭の**最終更新**日時点の情報です。Skillの名称、導入方法、提供地域は変わる可能性があるため、導入時は各公式リンクを確認してください。
