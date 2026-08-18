# GitHub Copilot Plugins

> **対象ツール**: GitHub Copilot（CLI / VS Code） ｜ **実行環境**: CLI（ターミナル）, IDE（VS Code） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-17

Plugin は、Custom Agents・Skills・Hooks・MCP サーバー設定・LSP サーバー設定を **1 つの配布単位** にまとめる仕組みです。Skill を 1 個ずつ配る代わりに、チームやプロジェクトに必要な拡張一式をまとめて配布・更新できます。

> **提供状況**: Copilot CLI・VS Code・Copilot SDK・Copilot アプリで一般提供です（全 Copilot プラン）。名称・コマンドは変わる可能性があるため、導入時は末尾の公式リンクを確認してください。

---

## 2 つの形式：可搬形式とツール独自形式

2026-08-06 に **Agent Plugins 1.0.0** というベンダー中立のオープン標準が公開され、Plugin には**形式が 2 つある**状態になりました。まずここを押さえると、以降の構成の説明が読み分けられます。

| | 可搬形式（Agent Plugins 1.0.0） | Copilot 独自形式（従来） |
|---|---|---|
| 目的 | 1 つ作って**複数のツールで使い回す** | Copilot の機能をすべて使う |
| 切り替え方 | `plugin.json` に正式な `$schema` を書く | `$schema` を書かない |
| マニフェスト | 項目が固定（`$schema` / `name` / `version` / `description` / `author` / `homepage` / `repository` / `license` / `keywords` / `extensions` のみ） | Copilot 独自の項目を書ける |
| 構成要素 | **Skills と MCP サーバーの 2 種類だけ** | Agents / Skills / Commands / Hooks / MCP / LSP |
| 配置場所 | 固定（`skills/` と `mcp.json`）。マニフェストで上書き不可 | マニフェストのフィールドで上書き可 |
| Agents・Hooks・LSP | 逆ドメイン名の名前空間へ置く（Copilot なら `com.github.copilot/`） | そのまま置ける |

**`$schema` が切り替えスイッチです。** GitHub の実装では `$schema` は任意であり、書かなければ従来どおり Copilot 独自形式として動きます。そのため **既存 Plugin の移行は不要**です。可搬形式へ寄せる場合の作業は、`$schema` の追加と、ファイルを標準のディレクトリ構成へ整えることが中心になります。

### 可搬形式の最小構成

```text
hello-plugin/
  plugin.json
  skills/
    greet/
      SKILL.md
```

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "hello-plugin"
}
```

`skills/` の**直下の子ディレクトリ**に `SKILL.md` があるものだけが Skill として認識されます（それより深い階層は探索されません）。`SKILL.md` の書式自体は [Agent Skills 仕様](https://agentskills.io/specification) が定めます。

### 標準側のガバナンス

| 項目 | 内容 |
|------|------|
| 意思決定 | Technical Steering Committee（Core Maintainer ＋ Lead Core Maintainer） |
| 役職の持ち主 | **企業ではなく個人**。企業に議席を予約しない |
| 制約 | **単一ベンダーが Core Maintainer の過半数を占めることを禁止** |
| Core Maintainer の所属 | Amazon / Cursor / Microsoft / OpenAI / Vercel |
| 対応クライアント | ChatGPT・Codex・Cursor・GitHub Copilot・Kiro・VS Code |

---

## Skill 単体と Plugin の使い分け

| 観点 | Skill 単体 | Plugin |
|------|-----------|--------|
| 配布単位 | `SKILL.md` を含む 1 ディレクトリ | `plugin.json` でまとめた複数の拡張 |
| 含められる要素 | 手順とその付随リソース | Agents / Skills / Commands / Hooks / MCP / LSP |
| 導入方法 | `gh skill install`、`npx skills add`、手動配置 | `copilot plugin install`、`enabledPlugins` |
| 向いている場面 | 1 つの作業手順を共有したい | チーム標準の拡張一式を配りたい |
| 更新の追跡 | Skill 単位（tree SHA・pin） | Plugin 単位（Marketplace のバージョン） |

> 単独の手順だけを配るなら Skill、外部連携（MCP）やイベント自動化（Hooks）まで含めて標準化するなら Plugin が適します。

---

## Plugin の構成（Copilot 独自形式）

以下は **`$schema` を書かない場合**の構成です。可搬形式では構成要素が Skills と MCP の 2 種類に限られ、配置場所も固定になります（前節を参照）。

Plugin の必須要素は `plugin.json` マニフェストの `name` フィールドだけです。マニフェスト自体は `plugin.json`（ルート）のほか `.plugin/plugin.json` や `.github/plugin/plugin.json`、`.claude-plugin/plugin.json` でも認識されます。以下の要素は、必要なものだけを含められます。

| 要素 | 配置場所 | 役割 |
|------|---------|------|
| マニフェスト | `plugin.json`（必須。`name` 以外は任意項目） | Plugin 名、説明、バージョン等のメタデータ |
| Custom Agents | `agents/*.agent.md` | 専門家ペルソナの定義 |
| Skills | `skills/<スキル名>/SKILL.md` | 関連リソース同梱の作業手順 |
| Commands | `commands/` 配下 | スラッシュコマンドの定義 |
| Hooks | ルートまたは `hooks/` の `hooks.json` | エージェントの動作に介入するイベントハンドラー |
| MCP サーバー設定 | ルートの `.mcp.json` または `.github/mcp.json` | 外部サービス連携（Model Context Protocol） |
| LSP サーバー設定 | ルートまたは `.github/` の `lsp.json` | 言語サーバー連携（Language Server Protocol） |

> 各要素の配置場所は `plugin.json` の `agents` / `skills` / `commands` / `hooks` / `mcpServers` / `lspServers` フィールドで上書きできます。詳細なフィールド定義は [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) を参照してください。
>
> これらの上書きフィールドと `.mcp.json` / `hooks.json` / `lsp.json` は **Copilot 独自の拡張**です。可搬形式では配置場所を上書きできず、MCP 設定を `plugin.json` へ直接書くこともできません。

```text
my-plugin/
  plugin.json            # 必須
  agents/
    db-reviewer.agent.md
  skills/
    migration-check/
      SKILL.md
  hooks.json
  .mcp.json
  lsp.json
```

---

## Marketplace

Marketplace は、Plugin の一覧を持つ **Git リポジトリ** です。リポジトリに `marketplace.json` を置くと、Copilot CLI がそのリポジトリを Marketplace として認識します。GitHub.com のほか、他の Git ホスティングサービスやローカル／共有ファイルシステムにも置けます。

Copilot CLI には、次の 2 つが既定で登録されています。

| Marketplace | 内容 |
|-------------|------|
| `copilot-plugins` | [github/copilot-plugins](https://github.com/github/copilot-plugins) — GitHub 公式の Plugin コレクション |
| `awesome-copilot` | [github/awesome-copilot](https://github.com/github/awesome-copilot) — カスタマイズ公式リポジトリの Plugin 群 |

---

## 導入手順

### 1. Marketplace を確認する

```powershell
copilot plugin marketplace list
copilot plugin marketplace browse awesome-copilot
```

### 2. Plugin をインストールする

```powershell
copilot plugin install database-data-management@awesome-copilot
copilot plugin list
```

Copilot CLI のセッション中は、スラッシュコマンドでも実行できます。

```text
/plugin install database-data-management@awesome-copilot
```

### 3. 更新・有効/無効・削除する

```powershell
copilot plugin update database-data-management   # 個別に更新
copilot plugin update --all                       # まとめて更新
copilot plugin disable database-data-management   # 無効化（アンインストールせず一時停止）
copilot plugin enable database-data-management    # 再度有効化
copilot plugin uninstall database-data-management
```

### 4. 独自の Marketplace を登録する

```powershell
copilot plugin marketplace add OWNER/REPO
copilot plugin marketplace update MARKETPLACE-NAME   # カタログを再取得（alias: refresh）
copilot plugin marketplace remove MARKETPLACE-NAME
```

> **注意**: 追加時は Marketplace リポジトリの `OWNER/REPO`（ローカルパスや Git URL も可）を、更新・削除時は登録済み一覧に表示される **Marketplace 名**（`marketplace.json` の `name` フィールドの値）を指定します。Plugin がインストール済みの Marketplace は、`--force` を付けない限り削除されません（`--force` を付けると、その Marketplace 由来の Plugin も削除されます）。`copilot-plugins` と `awesome-copilot` は組み込みの既定 Marketplace のため削除できません。

### インストール先とバージョン固定

Copilot CLI は Plugin を `~/.copilot/installed-plugins/<marketplace>/<plugin-name>/` に保存します。Marketplace を経由せず Git URL やローカルパスから直接インストールした Plugin は `~/.copilot/installed-plugins/_direct/<source-id>/` に入ります。インストールは **開発者ごと・マシンごと** です。

Marketplace の `marketplace.json` では、各 Plugin の `source` に GitHub リポジトリを指定でき、`ref`（タグ・ブランチ）に加えて **40 文字のフル commit SHA** を `sha` フィールドで指定すると、force-push やタグ・ブランチの移動に影響されない再現可能なインストールに固定できます。

---

## enabledPlugins による標準化

コマンドで 1 つずつ入れる（命令的）方法のほかに、設定ファイルへ書いて宣言的に有効化する方法があります。

| 設定ファイル | 適用範囲 | 用途 |
|-------------|---------|------|
| `~/.copilot/settings.json` | ユーザー全体 | 個人が常用する Plugin |
| `.github/copilot/settings.json` | リポジトリ | そのリポジトリの開発者全員に同じ Plugin を適用 |

```json
{
  "enabledPlugins": [
    "database-data-management@awesome-copilot"
  ]
}
```

リポジトリ側の設定ファイルをコミットしておけば、クローンした開発者が同じ Plugin 構成で作業を始められます。Copilot cloud agent（クラウド上のコーディングエージェント）は、この `enabledPlugins` を使う宣言的な方法のみに対応しています。既定で登録されていない Marketplace から導入したい場合は、同じ設定ファイルの `extraKnownMarketplaces` フィールドにも追加してください。

Enterprise では **managed settings** により、利用してよい Plugin を組織のポリシーとして強制し、自動インストールする Plugin を指定することもできます（VS Code・Copilot CLI・Copilot アプリが対象）。

---

## VS Code での利用

VS Code では **Agent plugins** として一般提供され、「Agent Plugins - Installed」ビューから有効化・無効化・アンインストールができます。有効／無効の状態は Plugin の設定とは別に保存されるため、共有しているワークスペース設定には影響しません。

導入済み Plugin は Customize または設定画面から、現在のバージョンの確認、個別更新、一括更新ができます。

---

## Claude Code の Plugin Marketplace との比較

| 観点 | GitHub Copilot Plugins | Claude Code Plugins |
|------|------------------------|---------------------|
| Marketplace の実体 | Git リポジトリ（`marketplace.json`） | Git リポジトリ（`.claude-plugin/marketplace.json`） |
| 登録コマンド | `copilot plugin marketplace add OWNER/REPO` | `/plugin marketplace add OWNER/REPO` |
| インストール | `copilot plugin install NAME@MARKETPLACE` | `/plugin install NAME@MARKETPLACE` |
| 含められる要素 | Agents / Skills / Commands / Hooks / MCP / LSP | Skills / Commands / Subagents / Hooks / MCP |
| 既定の Marketplace | `copilot-plugins` / `awesome-copilot` | なし（利用者が追加） |
| Marketplace のホスト | Git リポジトリ全般（GitHub 以外・ローカルも可） | GitHub のほか **GitLab**（2026-08 に対応。nested subgroup も可） |
| 組織での強制 | Enterprise managed settings | 設定ファイルの共有が中心 |

> どちらも「Git リポジトリを配布元にする」「`NAME@MARKETPLACE` 形式で指定する」点は共通です。大きな違いは、含められる要素（Copilot は LSP を含む）と、組織ポリシーによる制御の強さです。

設定キー名は両者で近づいてきています。Copilot の `extraKnownMarketplaces` / `strictKnownMarketplaces` に対し、Claude Code は `additionalMarketplaces` / `allowedMarketplaces` を同義のエイリアスとして受け付けます。

---

## 安全に使うための確認事項

- Plugin は **GitHub による検証済みではありません**。導入前に配布元リポジトリと中身（`SKILL.md`、`hooks.json`、スクリプト）を確認してください。
- Hooks はエージェントの動作に介入し、MCP は外部サービスへ接続します。**何にアクセスするか**を導入前に把握してください。
- 組織で配布する場合は、Marketplace リポジトリを自組織で管理し、`enabledPlugins` と managed settings で許可範囲を明示してください。
- バージョンを動かしたくない場合は、`marketplace.json` の `source.sha` に **40 文字のフル commit SHA** を指定してください（前述の「[インストール先とバージョン固定](#インストール先とバージョン固定)」を参照）。

### オープン標準が保証しないこと

可搬形式にしても、安全性が標準側で担保されるわけではありません。Agent Plugins 1.0.0 は次の項目を**将来版へ先送り**しています。

| 未定義の領域 | v1.0.0 の状態 |
|-------------|--------------|
| 信頼モデル・権限・サンドボックス | 定義しない。Plugin が何にアクセスするかを宣言する欄がない |
| **出自の検証** | 規定しない。**暗号署名の検証は将来版の検討事項** |
| シークレットの扱い | 規定しない。MCP の資格情報の渡し方はクライアント任せ |
| 組織ポリシー | 扱わない。許可リストは各ツールの独自機能に依存する |
| 監査ログ | インストール・更新等のイベントスキーマは標準化されていない |

2 点補足します。仕様が定めるパスの封じ込め規則（パッケージ内のパスは Plugin ルート外へ解決してはならない）は、**Plugin が起動したプロセスをサンドボックス化するものではない**と仕様自身が明示しています。また、リモート MCP サーバーの `headers` は「可視のパッケージデータであり、可搬なシークレット機構ではない」と定義され、**資格情報の埋め込みは禁止**されています。

### MCP サーバーを組織で限定する

**MCP allowlists**（2026-08-06 提供開始）で、利用してよい MCP サーバーを Enterprise のポリシーとして指定できます。

| 項目 | 内容 |
|------|------|
| 設定ファイル | `copilot/managed-settings.json` |
| キー | `allowedMcpServers`（許可）/ `deniedMcpServers`（拒否） |
| 指定方法 | `serverUrl`（リモート。ワイルドカード可）/ `serverCommand`（ローカル）/ `serverName`（表示名） |
| 適用対象 | Copilot アプリ / Copilot CLI / VS Code |
| 設定者 | Enterprise owner が、対象組織の `.github-private` リポジトリで設定する |

> `overridable` を指定した設定は、チーム側で上書きできます。

---

## 参考リンク

- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — Plugin の概念と構成（公式）
- [Finding and installing plugins for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) — 検索・導入手順（公式）
- [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) — Marketplace の作り方（公式）
- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — `copilot plugin` コマンドリファレンス（公式）
- [github/copilot-plugins](https://github.com/github/copilot-plugins) — 公式 Plugin コレクション
- [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins) — VS Code 側の解説（公式）

### Agent Plugins（オープン標準）

- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) — 仕様リポジトリ（公式）
- [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) — 仕様本文（公式）
- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Technical Charter](https://github.com/agentplugins/agent-plugins-spec/blob/main/GOVERNANCE.md) — ガバナンス（公式）
- [Agent Skills specification](https://agentskills.io/specification) — `SKILL.md` 形式の仕様（公式）
- [Agent Plugins 1.0 in VS Code, Copilot CLI, and the Copilot app](https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/) — GitHub 実装の提供開始（公式）
- [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) — MCP 許可リスト（公式）

## 関連ドキュメント

- [GitHub Copilot ガイド](README.md) — Copilot のカスタマイズ全体像
- [Skills 最新動向](../trends.md) — `gh skill` / Agent Finder / ARD との位置づけと比較表
- [superpowers](../dev-methods/superpowers.md) — Copilot CLI へ Plugin として導入できる開発手法スキル集
