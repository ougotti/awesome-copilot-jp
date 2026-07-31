# GitHub Copilot Plugins

> **対象ツール**: GitHub Copilot（CLI / VS Code） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-08-01

Plugin は、Custom Agents・Skills・Hooks・MCP サーバー設定・LSP サーバー設定を **1 つの配布単位** にまとめる仕組みです。Skill を 1 個ずつ配る代わりに、チームやプロジェクトに必要な拡張一式をまとめて配布・更新できます。

> **提供状況**: Copilot CLI の Plugin は一般提供、VS Code の Agent plugins は Preview です。名称・コマンドは変わる可能性があるため、導入時は末尾の公式リンクを確認してください。

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

## Plugin の構成

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

VS Code では **Agent plugins（Preview）** として提供され、「Agent Plugins - Installed」ビューから有効化・無効化・アンインストールができます。有効／無効の状態は Plugin の設定とは別に保存されるため、共有しているワークスペース設定には影響しません。

---

## Claude Code の Plugin Marketplace との比較

| 観点 | GitHub Copilot Plugins | Claude Code Plugins |
|------|------------------------|---------------------|
| Marketplace の実体 | Git リポジトリ（`marketplace.json`） | Git リポジトリ（`.claude-plugin/marketplace.json`） |
| 登録コマンド | `copilot plugin marketplace add OWNER/REPO` | `/plugin marketplace add OWNER/REPO` |
| インストール | `copilot plugin install NAME@MARKETPLACE` | `/plugin install NAME@MARKETPLACE` |
| 含められる要素 | Agents / Skills / Commands / Hooks / MCP / LSP | Skills / Commands / Subagents / Hooks / MCP |
| 既定の Marketplace | `copilot-plugins` / `awesome-copilot` | なし（利用者が追加） |
| 組織での強制 | Enterprise managed settings | 設定ファイルの共有が中心 |

> どちらも「Git リポジトリを配布元にする」「`NAME@MARKETPLACE` 形式で指定する」点は共通です。大きな違いは、含められる要素（Copilot は LSP を含む）と、組織ポリシーによる制御の強さです。

---

## 安全に使うための確認事項

- Plugin は **GitHub による検証済みではありません**。導入前に配布元リポジトリと中身（`SKILL.md`、`hooks.json`、スクリプト）を確認してください。
- Hooks はエージェントの動作に介入し、MCP は外部サービスへ接続します。**何にアクセスするか**を導入前に把握してください。
- 組織で配布する場合は、Marketplace リポジトリを自組織で管理し、`enabledPlugins` と managed settings で許可範囲を明示してください。

---

## 参考リンク

- [About GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins) — Plugin の概念と構成（公式）
- [Finding and installing plugins for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing) — 検索・導入手順（公式）
- [Creating a plugin marketplace for GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) — Marketplace の作り方（公式）
- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — `copilot plugin` コマンドリファレンス（公式）
- [github/copilot-plugins](https://github.com/github/copilot-plugins) — 公式 Plugin コレクション
- [Agent plugins in VS Code (Preview)](https://code.visualstudio.com/docs/agent-customization/agent-plugins) — VS Code 側の解説（公式）

## 関連ドキュメント

- [GitHub Copilot ガイド](README.md) — Copilot のカスタマイズ全体像
- [Skills 最新動向](../trends.md) — `gh skill` / Agent Finder / ARD との位置づけと比較表
- [superpowers](../dev-methods/superpowers.md) — Copilot CLI へ Plugin として導入できる開発手法スキル集
