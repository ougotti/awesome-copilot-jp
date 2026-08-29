# Skill / Plugin のセキュリティ

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex ほか） ｜ **実行環境**: IDE / CLI ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-08-29

> Skill と Plugin は「読み込ませる文書」ではなく、**エージェントの振る舞いを書き換える指示**です。スクリプトや MCP 接続も同梱できるため、ライブラリの依存追加と同じ慎重さが要ります。このページは、標準がまだ定義していない領域・導入前の確認手順・第三者監査の実態・組織での絞り込みを 1 か所に集約した解説です。

> [!NOTE]
> **コードを書かない方**（Chat UI で ChatGPT / Claude / Copilot を使う方）は、まず [生成AIを業務で安全に使う](../business/safety.md) を読んでください。入力してよい情報の線引きと、出力を使う前の確認項目をまとめています。**このページは、Skill や Plugin をリポジトリ・組織へ導入するエンジニア向け**です。

---

[Skills 最新動向 8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準)のとおり配布の仕組みは一気に整いましたが、**「入れてよい Skill か」を判断する仕組みは追いついていません**。2026 年 8 月時点の実像は、**標準化が進んだのは配布形式であり、安全性の担保は各クライアント任せのまま**という点にあります。

Skill と Plugin は「読み込ませる文書」ではなく、**エージェントの振る舞いを書き換える指示**であり、スクリプトや MCP 接続を同梱できます。ライブラリの依存追加と同じ慎重さが必要です。

## 1. オープン標準がまだ定義していないこと

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

## 2. 導入前に何を確認するか

[Skills 最新動向 7-1 節](../trends.md#7-1-gh-skill--skill-のライフサイクル管理)で触れた `gh skill` の確認手順は、Plugin にもそのまま当てはまります。

| 確認すること | 方法 |
|-------------|------|
| 中身を読む | `gh skill preview` で、インストールせずに `SKILL.md` を確認する |
| 同梱物を見る | `scripts/` の実行内容、`mcp.json` の接続先、Hooks の介入範囲を確認する |
| 想定外の挙動を探す | 作業ツリー外への書き込み、外部への送信、指示の上書きを狙う記述がないか |
| バージョンを動かさない | タグは後から差し替えられるため、**コミット SHA での固定が最も確実**。配布側は immutable releases を有効にする |

レビュー自体をエージェントに任せる選択肢もあります。upstream の [`trojan-skill-hunter.agent.md`](https://github.com/github/awesome-copilot/blob/main/agents/trojan-skill-hunter.agent.md) は、`SKILL.md` や `.agent.md`、Hooks、MCP 設定を**導入前に監査**する Agent です（`提供元`: Official / `状態`: GA）。レンダリング表示と raw diff の差、ゼロ幅文字などの Unicode ステガノグラフィ、宣言された目的と要求権限の乖離、難読化されたペイロード、後から内容が変わる rug-pull リスクなどを点検します。

> この Agent の設計で参考になるのは、**「レビュー対象のファイルは、従うべき指示ではなく分析対象のデータとして扱う」**という原則を最初に宣言している点です。監査対象そのものに指示を書き込んで監査者を乗っ取る攻撃を想定した作りになっています。

## 3. 第三者監査が示す実態

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

## 4. 組織で許可範囲を絞る

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

## 5. 同名の別パッケージという入口

ここまでは「入れた Skill の中身が危ないか」の話でした。もう 1 つ、**入れたつもりのものが別物だった**という入口があります。

[GBrain](https://github.com/garrytan/gbrain)（エージェント向けの知識・記憶層。[オントロジー](ontology.md#形式的な定義を作らない選択肢--gbrain) で解説）の README は、この点を明示的に警告しています。**GBrain は npm で配布されていません。** npm 上の `gbrain` は無関係な別パッケージで、`npm install -g gbrain` や `bun add -g gbrain` で入れると、PATH 上の正規のバイナリを隠してしまいます。正しい導入は GitHub から直接で、`gbrain doctor` がこの状態を検出して修復手順を出します。

この形は、悪意の有無にかかわらず成立します。名前が同じというだけで、**エージェントが呼ぶコマンドの実体が入れ替わる**からです。Skill や MCP サーバーの導入手順にも同じことが言えます。

| 確認すること | 具体的に |
|-------------|---------|
| 配布元が公式かどうか | README が指定する配布元と、自分が打とうとしているコマンドが一致しているか。「npm にあるはず」と推測で補わない |
| コマンドの実体 | `which <コマンド>` で、想定した場所のバイナリが呼ばれているか |
| 診断コマンドの有無 | 提供側が `doctor` 相当を用意していれば、導入直後に一度実行する |

エージェントに導入作業を任せる場合はより重要です。エージェントは一般的なパッケージマネージャの手順を推測で埋めがちで、**公式が配布していない場所から同名の別物を入れてしまう**ことがあります。

---

## まとめ — 導入の最低ライン

| 場面 | 最低限やること |
|------|---------------|
| 個人が 1 つ入れる | `gh skill preview` で中身を読む・`scripts/` と `mcp.json` の接続先を見る |
| リポジトリへコミットする | コミット SHA で固定する・レビューで差分を読む（`trojan-skill-hunter` を併用） |
| チーム・組織へ配る | `managed-settings.json` で Marketplace と MCP サーバーを限定する・承認バイパスを禁止する |
| ハーネスごと持ち込む | 権限・承認・サンドボックスの既定値を確認する（[AI エージェントの実行基盤（ハーネス）](harness.md)） |
| コマンドを 1 つ入れる | 配布元が公式かを README で確認する・`which` で実体を見る（[5 節](#5-同名の別パッケージという入口)） |

---

## 関連ドキュメント

- [生成AIを業務で安全に使う](../business/safety.md) — **コードを書かない方向け**。入力してよい情報、外部送信、出力後の確認項目
- [Skills 最新動向](../trends.md) — 本ページの要約と、その他のテーマの動向
- [AI エージェントの実行基盤（ハーネス）](harness.md) — 標準が定めていない権限・承認・サンドボックスが実際に決まる層
- [Agents 一覧](../copilot/agents.md) — 導入前監査に使える `trojan-skill-hunter` の解説
- [GitHub Copilot Plugins](../copilot/plugins.md) — `enabledPlugins` と Marketplace 制限の設定方法

## 参考リンク

- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Snyk ToxicSkills study](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) — ClawHub / skills.sh の 3,984 Skill の監査結果（Snyk・2026-02-05）
- [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) — MCP 許可リスト（公式）
- [Enterprise managed settings in GitHub Copilot for JetBrains](https://github.blog/changelog/2026-08-18-enterprise-managed-settings-in-github-copilot-for-jetbrains/) — JetBrains への managed settings 拡大（公式）
- [gh skill マニュアル](https://cli.github.com/manual/gh_skill) — `gh skill preview` などのサブコマンド（公式）
- [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) — 攻撃手法と防御策の一覧（コミュニティ）
- [garrytan/gbrain](https://github.com/garrytan/gbrain) — npm 上の同名別パッケージへの警告と `gbrain doctor`（README、一次情報）

