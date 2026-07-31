# Agent Skills・MCP・GUI 自動化の最新動向

> **対象ツール**: ツール横断 ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-01

> Agent Skills は `SKILL.md` だけで完結する仕組みから、MCP、Web データ取得、デプロイ、Computer Use と組み合わさる実行基盤へ広がっています。本ページは、現在注目度の高いテーマを公式情報に基づいて整理する**常設ページ**です。内容は冒頭の「最終更新」日時点の情報で、動向が変わるたびに本ページを改訂します。

## このページの更新履歴

| 日付 | 変更内容 |
|------|---------|
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

> 「[7. Skill の発見・配布・更新](#7-skill-の発見配布更新)」は動画チャプター外の追補です。GitHub 公式のエコシステム側の動き（CLI・Registry・Plugin）を扱います。

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

> `gh skill` / Agent Finder・ARD / GitHub Copilot Plugins

ここまでの 6 テーマが「どんな Skill があるか」だとすれば、本節は **「Skill をどう探し、安全に導入し、更新・固定・配布するか」** です。GitHub は 2026 年に、この運用面を埋める仕組みを 3 つ公式提供しました。

| 仕組み | 役割 | 提供状況 |
|--------|------|---------|
| `gh skill` | GitHub CLI による Skill のライフサイクル管理（検索・確認・導入・更新・公開） | Public Preview（2026-04-16 提供開始、GitHub CLI v2.90.0 以降） |
| Agent Finder / ARD | 必要になった時点で MCP サーバー・Skill・Canvas・Agent・Tool を Registry から発見する | 提供中（2026-06-17 提供開始、全 Copilot プラン） |
| Copilot Plugins | Agents・Skills・Hooks・MCP・LSP を 1 つの配布単位にまとめる | 提供中（Copilot CLI）／ VS Code は Preview |

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
| 必要な時だけツールを見つけさせたい | Agent Finder / ARD |

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

---

> 本ページの内容は冒頭の**最終更新**日時点の情報です。Skillの名称、導入方法、提供地域は変わる可能性があるため、導入時は各公式リンクを確認してください。
