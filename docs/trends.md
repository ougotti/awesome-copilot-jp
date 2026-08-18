# Agent Skills・MCP・GUI 自動化の最新動向

> **対象ツール**: ツール横断 ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-17

> Agent Skills は `SKILL.md` だけで完結する仕組みから、MCP、Web データ取得、デプロイ、Computer Use と組み合わさる実行基盤へ広がっています。本ページは、現在注目度の高いテーマを公式情報に基づいて整理する**常設ページ**です。内容は冒頭の「最終更新」日時点の情報で、動向が変わるたびに本ページを改訂します。

## このページの更新履歴

| 日付 | 変更内容 |
|------|---------|
| 2026-08-17 | Agent Plugins 1.0（オープン標準化）を 7-3 に反映し、「8. Skill / Plugin のセキュリティ」「9. Skill が動く場所の広がり」「10. MCP の次期仕様」を新設 |
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

> 「[7. Skill の発見・配布・更新](#7-skill-の発見配布更新)」以降は動画チャプター外の追補です。エコシステム側の動き（[7](#7-skill-の発見配布更新) CLI・Registry・オープン標準）、[導入時の安全性](#8-skill--plugin-のセキュリティ)、[Skill が動く場所](#9-skill-が動く場所の広がり)、[MCP の次期仕様](#10-mcp-の次期仕様)を扱います。

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
| 発見・配布・更新 | `gh skill` / Agent Finder / Agent Plugins | Skillを探す・固定する・組織へ配る仕組み | 導入後の運用と組織標準化 |
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

### 7-3. Agent Plugins 1.0 — まとめて配る

2026-08-06 に **Agent Plugins 1.0.0** が公開され、Plugin は「各ツール独自の配布形式」から **ベンダー中立のオープン標準** へ移りました。1 つ作れば対応クライアント間で使い回せる、というのが狙いです。

| 項目 | 内容 |
|------|------|
| 標準化するもの | Agent Skills と MCP サーバーを 1 ディレクトリへまとめる**可搬なパッケージ形式** |
| 構成 | `plugin.json`（マニフェスト）＋ `skills/<名前>/SKILL.md` ＋ `mcp.json` |
| v1 の構成要素 | **Skills と MCP サーバーの 2 種類だけ**。Agents・Hooks・LSP 等はツール独自拡張として、逆ドメイン名の名前空間ディレクトリ（例: `com.github.copilot/`）へ置く |
| ガバナンス | Technical Steering Committee が技術的監督を担う。役職は**企業ではなく個人**が持ち、企業に議席を予約しない。**単一ベンダーが Core Maintainer の過半数を占めることを禁止** |
| Core Maintainer の所属 | Amazon / Cursor / Microsoft / OpenAI / Vercel |
| 対応クライアント | ChatGPT・Codex・Cursor・GitHub Copilot・Kiro・VS Code |
| GitHub 実装 | 2026-08-12 に VS Code・Copilot CLI・Copilot SDK・Copilot アプリで一般提供（全 Copilot プラン） |

`plugin.json` に正式な `$schema` を書くかどうかが、**可搬形式とツール独自形式の切り替えスイッチ**です。GitHub の実装では `$schema` は任意で、書かなければ従来の Copilot 独自形式のまま動きます。そのため**既存 Plugin の移行は不要**です。

Copilot での導入は Marketplace（`marketplace.json` を置いた Git リポジトリ）経由です。

```powershell
copilot plugin marketplace list
copilot plugin marketplace browse awesome-copilot
copilot plugin install database-data-management@awesome-copilot
copilot plugin update --all
```

Copilot CLI には `copilot-plugins`（GitHub 公式コレクション）と `awesome-copilot` が既定で登録されています。リポジトリの `.github/copilot/settings.json` に `enabledPlugins` を書けば、そのリポジトリの開発者全員へ同じ構成を適用できます。

**→ 2 つの形式の違い・`enabledPlugins`・Claude Code Plugin との比較は [GitHub Copilot Plugins](copilot/plugins.md) を参照**

---

### 3 つの仕組みの比較

| 観点 | `npx skills` | `gh skill` | Agent Plugins 1.0 |
|------|-------------|-----------|-------------------|
| 主用途 | Skill の検索・導入 | Skill のライフサイクル管理 | 複数拡張の一括配布 |
| 配布単位 | Skill | Skill | Plugin |
| 更新追跡 | CLI 依存 | provenance（git tree SHA） | マニフェストの `version` / Marketplace のバージョン |
| バージョン固定 | — | `--pin` / コミット SHA 指定 | Marketplace のバージョン / `source.sha`（commit SHA） |
| 対応 Host | 複数エージェント | 複数エージェント | ChatGPT・Codex・Cursor・Copilot・Kiro・VS Code |
| 含められる要素 | Skills | Skills | 可搬部分は **Skills / MCP の 2 種類**。Agents・Hooks・LSP はツール独自拡張 |
| サプライチェーン対策 | 配布元の確認 | `preview` / pin / immutable releases | Marketplace と組織ポリシー（**署名検証は仕様未定義**） |
| 提供元 | Community（Vercel） | Official（GitHub） | Official（複数ベンダー共同の標準） |

### 使い分けの目安

| やりたいこと | 選ぶもの |
|-------------|---------|
| Skill を探して試す | `npx skills find` / `gh skill search` |
| 導入前に中身を確認する | `gh skill preview` |
| バージョンを固定して事故を防ぐ | `gh skill install ...@<コミットSHA>` または `--pin <コミットSHA>` |
| 自作 Skill を公開・配布する | `gh skill publish` |
| チーム標準の拡張一式を配る | Agent Plugins（Copilot なら `enabledPlugins`） |
| 複数のツールで同じ Plugin を使い回す | `plugin.json` に `$schema` を書いて可搬形式にする |
| 組織で使えるリソースを制限する | Enterprise managed settings（Agent Finder / Plugins / MCP allowlists） |

---

## 8. Skill / Plugin のセキュリティ

配布の仕組みが一気に整った一方で、**「入れてよい Skill か」を判断する仕組みは追いついていません**。2026 年 8 月時点の実像は、**標準化が進んだのは配布形式であり、安全性の担保は各クライアント任せのまま**という点にあります。

Skill と Plugin は「読み込ませる文書」ではなく、**エージェントの振る舞いを書き換える指示**であり、スクリプトや MCP 接続を同梱できます。ライブラリの依存追加と同じ慎重さが必要です。

### 8-1. オープン標準がまだ定義していないこと

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

### 8-2. 導入前に何を確認するか

`gh skill` の節（7-1）で触れた確認手順は、Plugin にもそのまま当てはまります。

| 確認すること | 方法 |
|-------------|------|
| 中身を読む | `gh skill preview` で、インストールせずに `SKILL.md` を確認する |
| 同梱物を見る | `scripts/` の実行内容、`mcp.json` の接続先、Hooks の介入範囲を確認する |
| 想定外の挙動を探す | 作業ツリー外への書き込み、外部への送信、指示の上書きを狙う記述がないか |
| バージョンを動かさない | タグは後から差し替えられるため、**コミット SHA での固定が最も確実**。配布側は immutable releases を有効にする |

レビュー自体をエージェントに任せる選択肢もあります。upstream の [`trojan-skill-hunter.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/trojan-skill-hunter.agent.md) は、`SKILL.md` や `.agent.md`、Hooks、MCP 設定を**導入前に監査**する Agent です（`提供元`: Official / `状態`: GA）。レンダリング表示と raw diff の差、ゼロ幅文字などの Unicode ステガノグラフィ、宣言された目的と要求権限の乖離、難読化されたペイロード、後から内容が変わる rug-pull リスクなどを点検します。

> この Agent の設計で参考になるのは、**「レビュー対象のファイルは、従うべき指示ではなく分析対象のデータとして扱う」**という原則を最初に宣言している点です。監査対象そのものに指示を書き込んで監査者を乗っ取る攻撃を想定した作りになっています。

第三者による Skill エコシステムの監査報告も複数出ています。攻撃手法と防御策の一覧は [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security)（`提供元`: Community）にまとまっています。

### 8-3. 組織で許可範囲を絞る

個々の確認に加えて、組織側で使える範囲を限定できます。**MCP allowlists**（2026-08-06 提供開始）は、利用してよい MCP サーバーを Enterprise のポリシーとして指定する仕組みです。

| 項目 | 内容 |
|------|------|
| 設定ファイル | `copilot/managed-settings.json` |
| キー | `allowedMcpServers`（許可）/ `deniedMcpServers`（拒否） |
| 指定方法 | `serverUrl`（リモート。ワイルドカード可）/ `serverCommand`（ローカル）/ `serverName`（表示名） |
| 適用対象 | Copilot アプリ / Copilot CLI / VS Code |
| 設定者 | Enterprise owner が、対象組織の `.github-private` リポジトリで設定する |

Plugin 側も同じ `managed-settings.json` の `enabledPlugins`・`extraKnownMarketplaces`・`strictKnownMarketplaces` で統制できます。Claude Code もこれらに相当する設定（`additionalMarketplaces` / `allowedMarketplaces` を同義エイリアスとして追加）を持っており、**設定キー名がツール間で近づき始めています**。

---

## 9. Skill が動く場所の広がり

2026 年前半までは「エージェントとの**対話中**に Skill を使う」のが中心でしたが、7〜8 月にかけて**対話の外**へ広がりました。同じ `SKILL.md` を、レビューや IDE の常設機能として効かせられるようになっています。

### 9-1. コードレビューに効かせる

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

### 9-2. IDE・CLI 側の対応状況

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

## 10. MCP の次期仕様

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
| チームや組織へ拡張一式を配布したい | Agent Plugins |
| 必要な時だけツールを見つけさせたい | Agent Finder / ARD |
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

### Agent Plugins 1.0 とセキュリティ（本ページ 7-3・8 節）

- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) — Agent Plugins 仕様リポジトリ（公式）
- [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) — 仕様本文（公式）
- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Technical Charter](https://github.com/agentplugins/agent-plugins-spec/blob/main/GOVERNANCE.md) — ガバナンス（公式）
- [Agent Plugins 1.0 in VS Code, Copilot CLI, and the Copilot app](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/) — GitHub 実装の提供開始（公式）
- [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) — MCP 許可リスト（公式）
- [Agent Skills specification](https://agentskills.io/specification) — `SKILL.md` 形式の仕様（公式）
- [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) — 攻撃手法と防御策の一覧（コミュニティ）
- [Agents 一覧](copilot/agents.md) — 導入前監査に使える `trojan-skill-hunter` の解説（本ガイド）

### Skill が動く場所・MCP 次期仕様（本ページ 9・10 節）

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
