# プラグインの可搬性 — インストール前に `plugin.json` を見る

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex・Cursor・Kiro ほか） ｜ **実行環境**: IDE / CLI ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-09-03

> 「マルチエージェント対応」と書かれた Plugin が、実際に他のエージェントへ持っていけるとは限りません。ベンダー中立のオープン標準 **Agent Plugins 1.0.0** に乗っているかどうかは、`plugin.json` を 1 つ開けば判定できます。このページは、その判定手順と、判定した結果で何が変わるかを 1 か所にまとめた解説です。標準そのものの成り立ちと各ツールの対応状況は [Skills 最新動向 8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準)、Copilot での操作手順は [GitHub Copilot Plugins](../copilot/plugins.md) を参照してください。

---

## なぜ気にするのか

Plugin を入れる場面で、可搬性が問題になるのは次の 2 つのときです。

| 状況 | 可搬でないと起きること |
|------|----------------------|
| **エージェントを乗り換える** | Copilot から Cursor へ、Claude Code から Codex へ移るときに、Plugin の中身を書き直すことになる |
| **複数のエージェントを併用する** | 同じチーム標準を、エージェントごとに別々のリポジトリで維持することになる |

逆に、**1 つのエージェントを使い続けるなら可搬性は要りません**。ツール独自形式のほうが機能は多く、既存の Plugin をそのまま使い続ける分に移行は不要です。判定する意味があるのは、乗り換えや併用を検討している場合に限られます。

## `$schema` が切り替えスイッチ

Agent Plugins 1.0.0 では、`plugin.json` の `$schema` フィールドが**必須**です。値は正式な識別子でなければなりません。

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-skill-pack"
}
```

一方 GitHub Copilot の実装では `$schema` は**任意**で、書かなければ従来どおり Copilot 独自形式として動きます。つまり **`$schema` を書くことが可搬形式へのオプトイン**にあたります。Claude Code の `.claude-plugin/plugin.json` も同様に、標準とは別系統の独自形式です。

**`$schema` を書くと機能が増えるのではなく、制約を受け入れる代わりに可搬になります。** 次節の制約を飲めるかどうかが、オプトインするかの判断になります。

## 可搬形式が課す 3 つの制約

### 1. 構成要素は Skills と MCP の 2 種類だけ

v1 が標準化する構成要素はこの 2 つで、配置場所は固定です。`plugin.json` で場所を上書きすることはできません。

| 構成要素 | 固定の配置場所 |
|---------|---------------|
| Skills | `skills/` **直下**の各サブディレクトリの `SKILL.md` |
| MCP サーバー | プラグインルートの `mcp.json` |

`skills/` の直下より深い階層は探索されません。MCP 設定を `plugin.json` へ直接書くことも、`.mcp.json` のような別パスから読ませることもできません。Agents・Commands・Hooks・LSP は v1 の範囲外です。

### 2. マニフェストは 10 フィールドで閉じている

書ける最上位フィールドは `$schema` / `name` / `version` / `description` / `author` / `homepage` / `repository` / `license` / `keywords` / `extensions` の 10 個だけです。このうち**必須は `$schema` と `name` の 2 つ**です。

`skills` や `mcpServers` のような構成要素を指すフィールドは**仕様に存在しません**。未知の最上位フィールドを書いた場合、クライアントはそれを報告したうえで無視し、読み込み自体は続行します（致命的エラーにはなりません）。一方、既定フィールドの型違反など、それ以外のスキーマ違反はプラグイン全体の拒否につながります。

### 3. マニフェストの場所も固定

クライアントは**プラグインルートの `plugin.json`** を見ます。仕様は「可搬なマニフェストはプラグインごとに 1 つだけ」と定め、他のファイルがこれを置き換えたり補ったりすることを認めていません。

したがって `.claude-plugin/plugin.json` や `.github/plugin/plugin.json` **しか**持たないパッケージは、ルートに `plugin.json` がない時点で可搬形式のプラグインとして読み込まれません。

## 標準が用意した逃げ道

制約の外にあるものを捨てる必要はありません。仕様は、クライアント固有のものを置く場所を 2 つ定めています。**どちらも逆ドメイン名の名前空間**を使います。

| 置きたいもの | 置き場所 | 例 |
|---|---|---|
| クライアント固有の**設定値** | `plugin.json` の `extensions` フィールド配下 | `"extensions": { "com.anthropic.claude-code": { … } }` |
| クライアント固有の**ファイル** | 同名の最上位ディレクトリ | `com.github.copilot/` |

クライアントは、自分が実装していない名前空間の中身を**検証せずに無視**します。つまり Copilot 向けの Hooks を `extensions` に書き足しても、Cursor 側でエラーにはなりません。**可搬な部分だけが各クライアントで読まれる**、というのが標準の設計です。

## 判定手順

インストールしようとしている Plugin のリポジトリで、上から順に確認します。

| # | 見るもの | 可搬形式なら | 独自形式なら |
|---|---------|-------------|-------------|
| 1 | `plugin.json` の**場所** | プラグインルート直下にある | `.claude-plugin/` や `.github/plugin/` の下にしかない |
| 2 | `$schema` フィールド | ある。値は `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` | ない、または別の値 |
| 3 | 最上位フィールド | 10 個の範囲に収まっている | `skills` / `mcpServers` など構成要素を指す項目がある |
| 4 | MCP 設定のパス | ルートの `mcp.json` | `.mcp.json` や `.github/mcp.json` |
| 5 | `agents/` `hooks/` `commands/` `lsp.json` | ない（`extensions` か逆ドメイン名ディレクトリへ逃がしている） | ルート直下にそのまま置かれている |

**1 と 2 で決まり、3 〜 5 は裏づけ**です。1 か 2 のどちらかを満たさない時点で、そのパッケージは可搬形式ではありません。

> README の「Claude Code and GitHub Copilot 向け」「マルチエージェント対応」といった記述は、**この判定の代わりになりません**。複数エージェント向けに配っていても、実装は各エージェント独自形式の並置であることがあります（次節）。

## 実物で見る

いずれもクラウドベンダー公式のプラグイン集で、複数のエージェント向けに配っていますが、可搬性の結果は割れます（確認日: 2026-09-03）。

| | [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) の `aws-core` | [microsoft/power-platform-skills](https://github.com/microsoft/power-platform-skills) の `power-pages` |
|---|---|---|
| 提供元 | `Official`（Amazon Web Services） | `Official`（Microsoft） |
| `plugin.json` の場所 | プラグインルート直下 | `.claude-plugin/` の下のみ |
| `$schema` | **あり**（1.0.0 の正式な識別子） | **なし** |
| MCP 設定 | `mcp.json`（ルート） | `.mcp.json` |
| Hooks | `extensions` の `com.anthropic.claude-code` から、同名ディレクトリ配下の `hooks.json` を指す | `hooks/` にそのまま |
| 判定 | **可搬形式** | 可搬形式ではない |

`aws-core` は、逃げ道の使い方の実例になっています。Claude Code 固有の Hooks を捨てるのでも、標準の外側に置くのでもなく、`extensions` の逆ドメイン名の下へ寄せることで、**マニフェスト本体は 10 フィールドの範囲に収めたまま**です。あわせて `.claude-plugin/` / `.codex-plugin/` / `.cursor-plugin/` の互換シムも併置しており、標準に未対応のクライアントからも読める形にしています。

`power-pages` 側は、README に Claude Code と GitHub Copilot の両方が挙がっていても、パッケージとしては Claude Code 独自形式です。**これは欠陥ではなく選択です** — Agents・Hooks・MCP を含む構成は v1 の範囲に収まらないため、可搬形式に寄せれば機能を落とすことになります。読者にとって重要なのは優劣ではなく、**「両対応」と書いてあっても可搬とは限らない**という事実のほうです。

## 可搬にしても解決しないこと

**可搬形式にしても、安全性が標準側で担保されるわけではありません。** Agent Plugins 1.0.0 は、信頼モデル・権限・サンドボックス・出自の検証（暗号署名）・シークレットの扱い・組織ポリシー・監査ログを、いずれも明示的に将来版へ先送りしています。

仕様が定めるパスの封じ込め規則（パッケージ内のパスはプラグインルート外へ解決してはならない）も、**プラグインが起動したプロセスをサンドボックス化するものではない**と仕様自身が明示しています。

`$schema` があることは「持ち出せる」ことの根拠であって、「入れてよい」ことの根拠ではありません。

**→ 導入前に何を確認するか、組織でどう絞り込むかは [Skill / Plugin のセキュリティ](skill-security.md) を参照**

---

## 関連ドキュメント

- [Skills 最新動向 8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準) — 標準の成り立ち・ガバナンス・各ツールの対応状況
- [GitHub Copilot Plugins](../copilot/plugins.md) — Copilot 独自形式の構成要素と、`copilot plugin` コマンド・Marketplace・`enabledPlugins` の操作手順
- [Claude Code のカスタマイズ機能](../claude-code/basics.md#agent-plugins-100-との関係) — Claude Code 側の状況と、`SKILL.md` 単位で共有するという代替案
- [Skill / Plugin のセキュリティ](skill-security.md) — 標準が定義していない権限・承認・サンドボックスをどう埋めるか
- [コーディングエージェントの選び方](coding-agents.md#乗り換えるときに見る軸) — 乗り換えを検討するときの、可搬性以外の軸

## 参考リンク

- [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) — 仕様本文。マニフェスト・固定配置・クライアント拡張の規定（公式）
- [agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec) — 仕様リポジトリ（公式）
- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Agent Skills specification](https://agentskills.io/specification) — `SKILL.md` 形式の仕様（公式）
- [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) — Copilot 独自形式のマニフェスト項目（公式）
- [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws) — 可搬形式の実例（公式・Apache-2.0）
- [microsoft/power-platform-skills](https://github.com/microsoft/power-platform-skills) — 独自形式の実例（公式・MIT）
