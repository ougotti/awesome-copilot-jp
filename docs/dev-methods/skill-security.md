# Skill / Plugin のセキュリティ

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex ほか） ｜ **実行環境**: IDE / CLI ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-10-28

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

2026-09-25 からは、これらの file の書式誤りや無効な team mapping を enterprise の AI controls ページの validator で確認できます。また、2026-10-22 に Copilot Business / Enterprise の「新機能の既定ポリシー」が GA になり、10-26 までに順次適用されます。**Unconfigured のまま**の MCP servers in Copilot などの policy は、適用の時点の global default に一度だけ従い、その後に global default を変えても変わりません。明示した設定は保持されます。**→ 期限前の確認手順は [GitHub Copilot ガイド](../copilot/README.md#新機能の既定ポリシー--2026-10-22-から適用) を参照**

### 実行する操作を `deny` / `ask` / `allow` に分ける

GitHub Copilot の **enterprise managed permissions** は、導入できる MCP や Plugin の範囲に加えて、エージェントが実行しようとする操作を中央で制御します（2026-09-09 一般提供）。対象は Copilot app、Copilot CLI、VS Code Agent Host のセッションです。

| セレクター | 制御する操作 | 設定例 |
|-----------|-------------|--------|
| `Shell` | シェルコマンド | 読み取り系は許可し、デプロイやパッケージ公開は毎回確認する |
| `Read` | ファイルの読み取り | 秘密情報を置くパスを拒否する |
| `Edit` | ファイルの作成・変更 | 生成物のディレクトリだけ許可する |
| `Domain` | ネットワーク接続先 | 社内 API は許可し、未知のドメインは確認する |

同じ操作へ複数の規則が一致した場合は **`deny` → `ask` → `allow`** の順で強い規則が優先されます。組織が `ask` にした操作は、その都度の新しい承認が必要です。利用者側の自動承認、承認バイパス、保存済みの許可、Hook で組織の確認を省略することはできません。

ただし、**規則が届いていないセッションには効きません**。Copilot CLI は 1.0.88（2026-09-22）より前の版で、`copilot --acp`（ACP サーバー）、`copilot --ahp-host`、`--server` で公開したセッションを、managed の MCP・permission・plugin の policy なしで動かしていました。エディタ連携などで CLI が裏側から起動される経路も含めて、版と実際の挙動を確認してください。**→ 確認手順は [GitHub Copilot ガイド](../copilot/README.md#copilot-cli-の別経路にも-managed-settings-が効く--1087--1088) を参照**

JetBrains では、同じ週に **enterprise managed sandbox** が Public Preview になりました。ファイルシステム、ネットワーク、プロキシ、開発ツール、macOS Keychain へのアクセスを中央設定し、利用者が制限を緩められないようにします。これはサンドボックスの管理であり、上記 4 セレクターによる操作単位の managed permissions が JetBrains でも一般提供された、という発表ではありません。

JetBrains 1.18.0 の **assisted approvals** も Public Preview ですが、これは Copilot agent セッションの低リスクなツール呼び出しを自動承認し、高リスクな操作では確認を求める仕組みです。enterprise managed permissions の `ask` を省略できるという発表ではありません。また、組み込み GitHub MCP Server の有効・無効と、Copilot agent セッションの MCP ツールごとの永続設定が加わりました。組織の MCP allowlist、組み込みサーバーの切り替え、個別ツールの設定は、それぞれ異なる制御面として確認してください。

### Claude Code の 1 コマンド限定許可と managed MCP

Claude Code 2.1.271 では、auto mode + sandbox の Bash / PowerShell / Monitor に `allowed_domains` が加わりました。これは**そのコマンドが必要とする host をレビューし、そのコマンドの間だけ開く**仕組みです。永続的なネットワーク allowlist や、MCP サーバー自体の許可リストではありません。

同じ版では Plugin install / update の `--json` が示したコマンドを、`--accept-command <sha256>` で完全一致した 1 件だけ承認できます。`-y` の代替として、承認対象のコマンドが後から変わっていないことを確認する境界です。

組織管理では、読み取れない / parse できない `managed-mcp.json` を黙って無視せず、**exclusive MCP control を維持したまま user / project / Plugin の MCP を読み込まない fail-closed** へ修正されました。また 2.1.273 では、server-managed settings と併用したときに `allowManagedMcpServersOnly` / `deniedMcpServers` / `disableClaudeAiConnectors` が無視される問題も修正されています。運用確認は「設定ファイルがあるか」だけでなく、startup warning と実際の MCP 一覧まで見ます。

2.1.280〜2.1.282（2026-09-22〜24）では、この「managed を下位の設定で弱めない」方向がさらに広がりました。symlink 経由の書き込みは実際の着地点で判定され、repository 外への書き込みを `acceptEdits` や allow rule が承認しなくなりました。`allowManagedPermissionRulesOnly` の下では Skill / command / Plugin manifest の `allowed-tools` が自らの tool を事前承認できず、project / local 設定は sandbox の除外コマンドや OpenTelemetry の送信先を変えられません。`--setting-sources` の制限は teammates や `/bg` などの別 session にも引き継がれます。版ごとの一覧は [Claude Code のカスタマイズ機能](../claude-code/basics.md#managed-settings-を下位の設定で弱められない変更) にまとめています。

2.1.283（2026-09-25）では、managed の `sandbox` に無効な値が 1 つあってもブロック全体が無視されなくなり（その値だけ fail-closed）、`Skill(anthropic-skills:<name>)` の deny は Claude Desktop が Plugin として配信した同じ Skill にも効くようになりました。また、**対話型のターミナルと VS Code 拡張のセッションは、設定がなければ auto mode で始まる**ようになり、対象が Enterprise・Claude API・Bedrock・Google Cloud・Foundry にも広がりました。承認の判定が人から classifier へ移るため、Enterprise / API 利用の組織は、配布前に managed の `permissions.disableAutoMode` か `permissions.defaultMode` を決めてください。**→ [auto mode が既定の開始モードになる範囲](../claude-code/basics.md#auto-mode-が既定の開始モードになる範囲--21283)**

### 実行コードを持つ拡張 — Claude Code の Mods

Claude Code 2.1.287（2026-10-01）の **Mods** は、プラグインが Claude Code の**内部で関数として動く**仕組みです。Skill が「読ませる文書」、MCP が「外部のツール」であるのに対し、mod は**利用者の権限で動くローカルのコード**で、すべてのプロンプトとツール呼び出しを見て書き換え、承認プロンプトが出る前にツール呼び出しを承認することもできます。**sandbox は mod を囲いません**（sandbox が隔離するのは Claude が実行する Bash コマンドです）。

導入前の確認は、`claude plugin validate ./some-mod` の `hooks:`（受けるイベント）と `calls:`（`$.fs.write`・`$.process.run`・`$.http.fetch` など、外へ出る手段）を読むことから始めます。組織では、既定のガード `sec-default` が managed の hook・system prompt・managed MCP を利用者の mod から守りますが、それ以外は許可されます。利用者の mod を止める `allowManagedModsOnly`、全フックまで止める `disableAllHooks`（**managed の `PreToolUse` も効かなくなる**）、`deny` ルールが mod 自身の `$.fs` / `$.process` を止めない点など、境界の詳細は専用ページにまとめています。

**→ [Claude Code の Mods](../claude-code/mods.md#3-入れる前に--信頼の境界を理解する)**

### 実行場所ごとの隔離境界を分ける

2026-09 下旬には、sandbox と network の制御が複数の製品で同時に更新されました。名前が似ていても、**どこで動く処理を、誰が強制するか**が違います。

| 仕組み | 実行場所 | 強制する主体 | 設定の単位 | 注意点 |
|--------|---------|-------------|-----------|--------|
| Copilot の local sandbox（**GA**、2026-10-07） | 利用者のマシン上で Copilot が起動するツールとコマンド（CLI・app・Agent Host を使う VS Code の session） | OS（MXC が共通 policy を各 OS の制御へ変換）。CLI は強制できなければその session で無効化し、managed の `sandbox.failIfUnavailable` でモデルとツールの実行を止められる | CLI と app で別々に設定。enterprise の managed settings で必須化でき、通常の設定では解除できない | ローカルの MCP / LSP サーバーは既定で対象、**リモートの MCP サーバーは対象外**。組み込みのファイル操作はベストエフォート。VM / コンテナではない軽量な隔離 |
| VS Code の Dev Container session | local folder（1.138）または SSH / Tunnel / WSL 上の remote project（1.139） | container と、Docker が動く host | project の Dev Container configuration と `chat.agentHost.devContainer.enabled` | toolchain の隔離が主目的。network・secret・tool 権限は別に設計する |
| Copilot の cloud sandbox（Public Preview） | GitHub がホストする使い捨ての Linux 環境 | GitHub | 組織の「Cloud Sandbox access」ポリシー（既定は無効）。cloud agent のポリシーと設定を共有する | local sandbox の設定は適用されない。利用量に応じて課金 |
| Codex CLI 0.157 の network policy | Codex が行う HTTP / WebSocket 通信 | Codex | Codex の network 設定 | redirect 先と継続中の通信にも適用され、policy 変更で失効した通信は cancel される |
| Claude Code の sandbox | 利用者のマシン上の Bash など | Claude Code と OS | settings と managed settings | managed の制限下では、project / local 設定から除外コマンドを追加できない（2.1.282） |

表の各行は互いに置き換えられません。たとえば Dev Container で動かしても、container から外部へ出る通信を制限したことにはならず、local sandbox を有効にしても cloud で動く session は守られません。導入時は、**エージェントが実際に動く場所**を先に特定し、その場所で効く制御を確認します。

**→ 各製品の設定手順は [GitHub Copilot ガイド](../copilot/README.md#copilot-の-local-sandboxga)・[Codex ガイド](../codex/README.md#codex-cli-0157--通信中も効く-network-policy-と-session-の継続) を参照**

**→ ここまでは「何を許可するか」の話でした。「エージェント自身を誰として認証し、その権限を他のエージェントへどこまで委任してよいか」は [AIエージェントのID・認可・委任権限](agent-identity.md) を参照してください。**

---

## 5. 統制が効く 3 つの段階

ここまでは「入れる前に読む」「組織で許可範囲を絞る」という**導入前**の話でした。2026 年 8〜9 月には、その前後へ統制の範囲が広がっています。Claude の組織向け機能を例に取ると、3 つの段階に整理できます。

| 段階 | 何をするか | 例 |
|------|-----------|-----|
| **導入前** | 入れてよいものかを検査する | Skill / Plugin のセキュリティスキャン（第三者製の Skill・Plugin をアップロード・編集の時点で検査） |
| **推論前** | 実行される直前に許可・拒否を判定する | Inference hooks（組織の AI セキュリティサーバーが allow / deny を返すまで待つ。2026-10-20 に Beta を終了。Anthropic が組織のために動かす Code Review などは[対象外](#2026-10-1810-22-の権限境界の更新)） |
| **実行後** | 何が行われたかを後から確認する | Compliance API（セッションのトランスクリプトを取得する。2026-10-15 から、保存された Instructions も取得できる＝[Beta](#2026-10-1510-17-の権限境界の更新)） |

**導入前だけでは埋まらない穴がある**、というのがこの並びの意味です。中身が安全な Skill でも、渡される入力や実行される文脈まではスキャンできません。推論前の判定と実行後の監査は、そこを埋める層です。

一方で、いずれも**組織向けプランと事前設定が前提**です。個人利用では [2 節](#2-導入前に何を確認するか)の導入前チェックが引き続き主役になります。

**→ Claude での具体的な設定・利用条件は [Claude Code のカスタマイズ機能](../claude-code/basics.md#組織での統制--導入前推論前実行後) を参照**

### 承認画面が副作用より先とは限らない — Kiro IDEの修正済み事例

`ask` や確認画面があることだけでは、**ファイル書き込みや外部通信が承認応答まで停止している**とは限りません。AWSが2026-09-11に公開した [CVE-2026-89332](https://aws.amazon.com/security/security-bulletins/2026-111-aws/) は、その順序を確認する必要性が表れたKiro IDE固有の事例です。

1. 細工されたrepositoryにより、未信頼workspaceのsettings fileをKiro agentが変更し、Kiro Powers registry URLを外部endpointへ向けられる可能性があった
2. Kiro IDEは変更内容とURLを承認画面へ表示した
3. しかし、承認への応答を待つ時点でsettings fileはすでにdiskへ書き込まれていた
4. 応答前にPowers panelを開くと、そのURLへのrequestが発生し、workspaceの機微情報が送信される可能性があった

この問題の対象は **Kiro IDE 0.8.135未満**で、**0.8.135以上で修正済み**です。AWSは最新版への更新と、旧版で開いたproject内にcredentialsがあった場合のrotationを推奨しており、workaroundはありません。これは旧Kiro IDEの実装に関するCVEです。Kiro CLI、Kiro Web、Kiro Crew、PowersやAgent Pluginsの仕様全体に同じ問題があるという意味ではなく、現在のKiro IDE 1.xに未修正の問題が残ることも示していません。

承認機能を評価するときは、UIの有無に加えて次の時点を実際の実装とtraceで確認します。

| 確認する境界 | 確認内容 |
|-------------|---------|
| ファイル書き込み | 承認前に一時領域や本来のsettings fileへ反映されていないか |
| 設定の再読み込み | 未承認の変更をpanel、extension、agentが読み込まないか |
| 外部通信 | DNS解決やHTTP requestを含め、送信前に停止しているか |
| 拒否後 | 書き込み済みの値、cache、接続先がrollbackされるか |

Kiro IDEを利用している場合は最新版へ更新します。0.8.135未満で開いたprojectにcredentialsが存在した場合は、AWSの推奨に沿ってrotationを検討してください。未信頼repositoryを開く際は、workspace settingsとregistry / MCP endpointの変更も確認対象に含めます。

### Managed Agents はツール呼び出しごとに判定する

Claude Platform の **Managed Agents permission policies**（Beta）は、サーバー上のエージェントがツールを呼ぶたびに `always_allow`、`always_ask`、`auto` のいずれかで判定します。`auto` はツール名、入力、セッションの文脈から allow / deny / ask を決めますが、**人間による確認を必須にする設定ではありません**。人が必ず止めて確認する操作は `always_ask` にします。`auto` が deny と判定した呼び出しを利用者が上書きすることもできません。

このポリシーは Managed Agents が提供するツールと MCP ツールに適用され、API 利用者が定義する custom tools は対象外です。custom tools の認可と監査はアプリ側で実装します。判定結果はイベントの `evaluated_permission`（通常は `evaluation` を含む）で追跡でき、必要なら `ant beta:sessions connect` で進行中セッションを確認・誘導・応答できます。

GitHub と Anthropic の機能は、どちらも「実行時の権限」を扱いますが、同じ設定モデルではありません。

| 観点 | GitHub Copilot managed permissions | Claude Managed Agents permission policies |
|------|------------------------------------|-------------------------------------------|
| 判定単位 | `Shell` / `Read` / `Edit` / `Domain` の規則に一致する操作 | サーバー上の agent / MCP tool call |
| 結果 | `deny` / `ask` / `allow` | allow / deny / ask |
| 人の確認を必須にする方法 | 組織の `ask`。保存済み許可や自動承認では省略できない | `always_ask`。`auto` は人の確認を保証しない |
| 監査 | 管理設定と各セッションの承認操作 | イベントの `evaluated_permission` |
| 対象外に注意するもの | 対応面以外のクライアント。JetBrains の発表は managed sandbox | custom tools。Claude Code のローカル権限設定とは別機能 |

#### Web ツールが取得できる URL を絞る（2026-10-07）

ツール呼び出しの判定とは別に、Managed Agents では **web ツールが到達できる先**も絞られました（[release notes](https://platform.claude.com/docs/en/release-notes/overview)、2026-10-16 確認。API での実行は未検証）。prompt injection で「この URL にデータを付けて取得せよ」と誘導される経路を狭める変更です。

| 変更 | 挙動 | 運用上の意味 |
|------|------|-------------|
| **`web_fetch` は session に既出の URL だけを取得する** | 利用者のメッセージ、`web_search` の結果、`web_fetch` が以前に返したページに現れた URL は取得できる。**Claude の出力・system prompt・添付文書・`bash` / `read` / MCP などの tool 出力にだけ現れた URL** は `url_not_in_prior_context` エラーになる | モデルが自分で組み立てた URL や、読み込んだ文書に埋め込まれた URL へは取りに行かない。取得させたい URL は `user.message` event で渡す |
| `limited` networking の `allowed_hosts` が web ツールにも効く | `web_fetch` は対象外の host で `url_not_allowed`、`web_search` は対象外の host の結果を省く。`allowed_hosts` が空なら、どちらも何も返さない | `allow_package_managers` / `allow_mcp_servers` は web ツールの host を増やさない。web ツールに必要な host は `allowed_hosts` に明示する |
| `allowed_domains` の検査 | 有効な web ツールの `allowed_domains` に `allowed_hosts` 外の entry があると、session の作成・更新が 400 になる | `allowed_hosts` の entry は `*.` で始まらない限り**完全一致**。`["example.com"]` は `docs.example.com` を含まない |

unrestricted networking と self-hosted 環境はこの制限の対象外です。社内の文書や MCP の結果に含まれる URL を agent に取得させる設計にしていた場合は、その URL を利用者のメッセージとして渡す流れに変える必要があります。

2026-10-20 には、この上に**組織の層**が加わりました（[release notes](https://platform.claude.com/docs/en/release-notes/overview)、2026-10-22 確認。管理画面・API での実行は未検証）。

| 変更 | 挙動 |
|------|------|
| 組織単位で Web fetch を無効化 | 組織の管理者が Claude Console の **Capabilities** で Web fetch を止めると、web fetch tool を含む Messages API の request は 400 になる。Managed Agents の session では `web_fetch` の呼び出しが agent へのエラー結果として返る |
| 組織のドメイン制限 | 有効にしたまま、同じ画面で許可・ブロックするドメインを決められる。Managed Agents の `web_fetch` は、**組織のリストと agent の `allowed_domains` / `blocked_domains` の両方**を通った URL だけを取得し、redirect 先も検査する |
| `web_search` | Managed Agents の session も組織の「Allow web search」（10-06 から）とドメイン制限（10-14 から）に従い、組織と agent の両方の設定で許可された結果だけを受け取る |

agent ごとの設定と組織の設定は**両方を満たす必要がある**ため、組織の制限を入れると、これまで動いていた agent の取得が止まり得ます。入れる前に、agent が取得している host を一覧にしてください。

**→ Managed Agents をハーネスとして運用するときの介入方法は [AI エージェントの実行基盤](harness.md#実行中の権限判定と介入--claude-managed-agents) を参照**

### コンテキストの除外は、Skill / MCP の統制と別に効く

GitHub Copilot の **content exclusion** は、機密ファイルを Copilot のコンテキストへ取り込ませない組織設定です（Copilot app / CLI で 2026-09-02 に GA、Copilot Business / Enterprise）。ただし **これは「Copilot が取り込む経路」への制御であり、MCP サーバーや Skill が別の経路で同じファイルを読む場合の防御にはなりません。** VS Code の Copilot Chat の Edit mode / Agent mode は現時点で非対応であるなど、対応面にも差があります。本節の allowlist・推論前の判定と**組み合わせて**使ってください。

**→ 対応面・非対応面の一覧は [GitHub Copilot ガイド](../copilot/README.md#組織の統制--content-exclusion) を参照**

### 共有フォルダを読ませる前に、4 つの層を別々に確認する

Claude Code 2.1.292（2026-10-06）では、ネットワーク（UNC）パスのファイル読み取りで `PreToolUse` フックの承認や auto mode が確認を飛ばしていた問題、Windows の別表記パスでの `rm -rf` の誤認識、読み取り中のリンク差し替え、途中で現れた sandbox の読み取り拒否パスの扱いが修正されました。共有フォルダを扱うときは、次の 4 つを**別々に**確認します。

| 層 | 確認すること |
|----|-------------|
| フック・auto mode の判断 | UNC パスで確認が出るか（2.1.292 以降） |
| permission ルール | 必要なサブフォルダだけを許可し、機密は `Read` の deny で止めているか |
| sandbox | `denyRead` は sandbox 内のコマンドに効き、Read ツールは止めない |
| OS・共有側のアクセス権 | Claude Code の許可に関係なく、ここが上限になる |

**→ [Claude Code のカスタマイズ機能](../claude-code/basics.md#共有フォルダと-windows-のパスを扱う前に--21292-の修正)**

### 自然言語の判断と、強制する制御を分ける

Claude Code の `prompt` / `agent` フックは、モデルが自然言語の条件を解釈して許可・拒否を決めます。2.1.294（2026-10-08）では、「〜をブロックせよ」のような**命令文で書いたフックが、本来ブロックすべき操作を通していた**問題が修正されました。モデルの判断は言い回し・版・入力で変わり得ます。`prompt` / `agent` の不正出力・タイムアウト・モデルエラーの未確認範囲と、2.1.295 から `command` / `http` で明示できる `onFailure: "block"` を区別してください。**必ず止めたい操作は、permission ルール・`command` フック・managed settings・sandbox で止め**、自然言語のフックは補助的なチェックに使います。**→ [Claude Code のカスタマイズ機能](../claude-code/basics.md#自然言語のフックは書き方で結果が変わる--21294-の修正)**

### 2026-10-03〜10-10 の権限境界の更新

2026-10-13 に公式資料を再確認しました。各 CLI は Official / GA（正式 release）ですが、OS・実行場所ごとの保証まで共通ではありません。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| hook の実行失敗 | Claude Code 2.1.295 の `onFailure: "block"` は同期 command / HTTP hook の失敗を止める。Stop 系・background hook は対象外。2.1.296 は managed denial / turn 終了 / MCP 出力更新を修正 | [Claude Code](../claude-code/basics.md#フックの実行失敗も止める--2129521296)、[Hooks reference](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails) |
| token と network | Copilot CLI 1.0.92〜1.0.95 は ambient token、managed domain 上限、Assisted Permissions、credential 注入先を別々に制御する | [Copilot CLI](../copilot/README.md#cli-10921095--token通信先承認を別々に制御する)、[changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) |
| 権限の引き継ぎ | Codex 0.161〜0.162 は escalation 後の denied read / network と、background task 開始時の権限を維持。Linux sandbox 構築・Windows temp の修正は分けて確認する | [Codex CLI](../codex/README.md#codex-cli-0160101621--権限を維持して再開する)、[0.161.0](https://github.com/openai/codex/releases/tag/rust-v0.161.0)・[0.162.0](https://github.com/openai/codex/releases/tag/rust-v0.162.0) |

managed policy を利用者の設定や起動 flag で弱められると想定せず、許可ケースと拒否ケースの両方を試してください。

### 2026-10-10〜10-14 の権限境界の更新

2026-10-14 に公式資料を確認しました。GitHub Copilot の更新が中心で、**policy が確実に届くこと**と**無人実行で承認がどう扱われるか**が変わりました。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| policy の到達 | `forceRemoteSettingsRefresh: true` で、Copilot CLI・VS Code・Copilot app は起動時に policy の再取得が必須になり、確認できなければ fail-closed になる。可用性と引き換えなので、対象を絞って使う | [GitHub Copilot ガイド](../copilot/README.md#managed-settings-の強制更新と最小-client-version2026-10-13)、[変更ログ](https://github.blog/changelog/2026-10-13-enterprise-managed-settings-enforcement-updates) |
| client の版 | managed settings に `sandbox` キーを含めると最小 client version が強制される。古い版に固定した端末は更新まで使えない | 同上 |
| sandbox の回避 | VS Code 1.141 の Agent Host は、unified managed settings の `sandbox.enabled: true` / `allowBypass: false` で回避を禁止できる（Preview）。旧 policy の `ChatAgentSandboxEnabled` は Agent Host では上書きできる既定値に変わった | [VS Code 1.141](../copilot/README.md#vs-code-1141--sandbox-の必須化旧-policy-の移行session-間の指示) |
| 無人実行の承認 | Copilot CLI 1.0.97 の Autopilot では、`preToolUse` hook の `ask` が **deny** になる。custom agent 単位の hook は、組織や repository の hook に**追加して**動く | [Copilot CLI](../copilot/README.md#cli-10961097--hook-の適用範囲と無人実行での承認) |
| 監査ログ | Copilot CLI 1.0.96 は permission の判定主体を timeline に表示。telemetry は identity と 5 種類の本文を個別に有効化でき、既定はすべてオフ | [OTel の設定](../copilot/README.md#誰の操作かを付ける本文を種類ごとに取る2026-10-12) |

「`ask` にしておけば人が確認する」は、**人が見ている対話の session でだけ成り立つ前提**です。無人実行では、確認を求める操作は止まる（deny）と考え、通したい操作は条件を絞った `allow` として書き分けてください。また、policy の配布と client の更新の順番を誤ると、統制を強めたつもりで利用者全員を止めることがあります。

### 2026-10-14〜10-16 の権限境界の更新

2026-10-16 に公式資料を確認しました。Claude Code では**既存の rule の一致範囲**と**hook が受け取れない・答えられないときの扱い**が、VS Code では**統制を入れたときに使える harness**が、Claude Managed Agents と Codex では**外部への取得と再開時の権限**が変わっています。release note と公式 docs の照合のみで、実機での拒否は確認していません。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| rule の一致範囲 | Claude Code 2.1.299 で、MCP の allow rule と agent の `tools:` が**書いたサーバー名にだけ一致**する。`mcp__a` は `a__b` を許可しない。名前に `__` を含むサーバーへの deny / ask が効いていなかった問題も修正 | [Claude Code](../claude-code/basics.md#2129921301--mcp-の許可ルールの完全一致化と-hook-の-fail-closed-化)、[2.1.299](https://github.com/anthropics/claude-code/releases/tag/v2.1.299) |
| hook の失敗 | plugin hook が受け取れない・答えを返せない操作は拒否。Windows で Git for Windows がないときの PreToolUse / PermissionRequest hook の fail-open を修正 | 同上 |
| hook の書き換え | 2.1.300 で `updatedInput` を tool の入力として検証し、未知のキーを捨てる。Cowork の cloud session では hook の `setMode` を無視し、auto mode の hook は shell / subagent を承認できない | [2.1.300](https://github.com/anthropics/claude-code/releases/tag/v2.1.300) |
| 判定の監査 | 2.1.301 の `tool_decision` event に `classifier_verdict`・`permission_mode` が加わり、classifier と rule の判定を区別できる | [ハーネスの OTel](harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions) |
| 統制と harness | VS Code 1.142 は、managed の `permissions` か `sandbox.enabled: true` があると Copilot harness を必須にし、Claude・Codex・terminal chat を使えなくする。回避用の `temporaryDefaultToLocalHarness` は統制も外す。Assisted Permissions は `permissions.allow` / `ask` / `deny` と併用できない | [VS Code 1.142](../copilot/README.md#vs-code-1142--統制を入れると-copilot-harness-へ移るpermission-mode-を絞る) |
| 再開時の権限 | Codex CLI 0.163.0 は、再開した thread の permission と network の承認を復元する。明示した override と現在の managed policy が優先。network proxy は DNS 解決前に hostname を確認し、credential の別名による inspection hook の回避を塞いだ | [Codex CLI](../codex/README.md#codex-cli-01630--再開時の権限復元network-proxy-の強化応答中の-steer) |
| 外部への取得 | Claude Managed Agents の `web_fetch` は session に既出の URL だけを取得し、`limited` networking の `allowed_hosts` が web ツールにも効く（2026-10-07） | [Web ツールの URL 制限](#web-ツールが取得できる-url-を絞る2026-10-07) |
| 外部の監視基盤 | Claude Managed Agents の OpenTelemetry export（beta、2026-10-14）。Full content は prompt と tool の結果を Anthropic の外へ送る。配送は best effort で、監査ログの代わりにならない | [ハーネス](harness.md#claude-apimanaged-agents-の-trace-を自分の監視基盤へ送る2026-10-14beta) |

前方一致で広く許可していた rule は、更新で**狭まる**方向に変わります。更新前に `mcp__` の rule を棚卸しし、許可したいサーバーを `mcp__<server>__*` で明示してください。逆に VS Code 1.142 では、統制を**強める**設定を入れた時点で、利用者が使える harness が変わります。どちらも、配布前に検証用の端末で挙動を確かめてください。

### 2026-10-15〜10-17 の権限境界の更新

2026-10-17 に公式資料を確認しました。**無人実行の既定値**、**会話から操作できる repository の範囲**、**保存された指示の監査**が変わっています。release note と公式 docs の照合のみで、実機・管理画面での確認はしていません。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| 開始モード | Claude Code 2.1.302 で、permission mode を指定しない `claude -p` / Agent SDK は、third-party provider・telemetry off・新規インストール直後でも `default` で始まる。`--permission-mode auto` は auto のまま。**無人実行では permission mode を明示**し、止めたいものは managed settings で決める | [Claude Code](../claude-code/basics.md#21302--無人実行の開始モードと-subagent-の実行方式)、[2.1.302](https://github.com/anthropics/claude-code/releases/tag/v2.1.302) |
| subagent の実行形態 | fork subagent が `-p`・SDK・desktop・VS Code でも既定で有効、desktop / VS Code では main conversation の subagent が常に background。**文脈の引き継ぎ・background 実行と、権限・sandbox は別の設定**。background かどうかで権限が決まるわけではないため、subagent に渡す tool と権限は別に確認する | 同上、[マルチエージェント](multi-agent.md#3-agent-as-tool-専門作業を隔離して呼び出す) |
| hook の並列度 | `prompt` / `agent` hook は同じイベントにつき同時に 12 個まで。順序に依存する判定や、外部へ書き込む hook は並列でも壊れないかを確認する | [Claude Code](../claude-code/basics.md#21302--無人実行の開始モードと-subagent-の実行方式) |
| 会話から届く repository | GitHub in Slack / Teams（2026-10-15、Improvement）が 1 つの会話で複数の repository を扱えるようになった。**会話が見える範囲と、GitHub で操作できる repository の範囲は別の層**。書き込みの前に対象の owner / repository / branch を明示して確かめる | [GitHub Copilot ガイド](../copilot/README.md#slack--teams-から複数の-repository-を扱う2026-10-15) |
| 保存された指示の監査 | Claude Compliance API（Beta、Enterprise）の `user_preferences` で、claude.ai の Instructions for Claude と Cowork の Global instructions を取得できる。**監査用の読み取り**であり、指示を配布・上書きする機能ではない | 下記 |

**保存された指示を監査する — Compliance API の `user_preferences`（2026-10-15、Beta）**

`GET /v1/compliance/organizations/{org_uuid}/user_preferences` は、組織の現メンバーが保存した **Instructions for Claude**（`conversation_preferences`）と Cowork の **Global instructions**（`cowork_global_instructions`）を返します。Claude Enterprise 組織向けの Beta です。

| 確認すること | 公式の記載 |
|---|---|
| 鍵と scope | 既存の Compliance Access Key に **`read:compliance_user_data`** が必要。`read:compliance_org_data` だけでは 403 になる |
| 返る範囲 | 既定では、どちらかを設定したメンバーだけ。`include_unset=true` で全員（未設定は `null`）。`user_ids[]` で最大 10 人に絞れる |
| pagination | `limit`（既定 20、最大 100）と `page`。`next_page` が `null` になるまで続け、各ページで同じ `include_unset` / `user_ids[]` を送る。空のページでも最後とは限らない |
| 重複 | どちらも**アカウント単位の設定**のため、複数の組織に属するメンバーの同じ本文が、組織ごとに返る |

運用では次を推奨します（本ガイドの設計例）。

- 指示の本文は**利用者のデータ**として扱い、取得する担当者・保存先・保存期間・閲覧のログを、会話の transcript と同じ基準で決める
- 複数の組織で同じ本文を取得する場合は、ユーザー ID で重複を除き、同じ本文を何か所にも保存しない
- 指示に機密情報や認証情報が書かれていないかの点検に使い、見つけたら本人に削除を依頼する。この API で指示を書き換えることはできない
- 組織として強制したい指示は、利用者の Instructions ではなく managed settings など管理者が配る仕組みに置く

出典: [Claude Platform release notes（2026-10-15）](https://platform.claude.com/docs/en/release-notes/overview)、[List user preferences](https://platform.claude.com/docs/en/manage-claude/compliance-org-data#list-user-preferences)（2026-10-17 確認、API 実行は未検証）。

### 2026-10-18〜10-22 の権限境界の更新

2026-10-22 に公式資料を確認しました（Claude Code 2.1.309 と Codex 0.164.0 の行は 2026-10-23 に追加）。この期間は、**更新するだけで今までより通るようになる変更**が複数の製品で入っています。release note と公式 docs の照合のみで、実機・管理画面での確認はしていません。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| MCP の allowlist | Claude Code 2.1.305 で、`allowedMcpServers` が `managed-mcp.json` の stdio server のうち `${VAR}` を `env` にだけ使うものを絞り込まなくなった。allowlist から外していたものは**更新で読み込まれる**。止めるなら `deniedMcpServers` に書く。**allowlist だけで止める設計は、製品の更新で穴が開くことがある** | [Claude Code](../claude-code/basics.md#2130421307--統制が緩む変更と締まる見える変更)、[2.1.305](https://github.com/anthropics/claude-code/releases/tag/v2.1.305) |
| sandbox | Claude Code 2.1.305 の `sandbox.allowNestedUserNamespaces` は、公式が「sandbox のファイル保護を迂回できる」と明記。Chromium などのために有効にした端末の sandbox は、書き込み境界として扱わない | 同上 |
| 人が決める確認 | Claude Code 2.1.304 の Mods の `decider: "person"` で、確認を承認画面か host の callback に限り、誰にも聞けない場面では拒否にできる。[自然言語の判断と強制する制御を分ける](#自然言語の判断と強制する制御を分ける)ときの、強制側の部品になる | [Claude Code の Mods](../claude-code/mods.md)、[2.1.304](https://github.com/anthropics/claude-code/releases/tag/v2.1.304) |
| Skill の許可 | Claude Code 2.1.304 で、hook を止められた Skill は `allowed-tools` も持ち込めない。2.1.305 で `allowManagedPermissionRulesOnly` が desktop の plugin の `allowed-tools` にも及ぶ | [Claude Code](../claude-code/basics.md#2130421307--統制が緩む変更と締まる見える変更) |
| 止めた記録 | Claude Code 2.1.307 の OTel `claude_code.safety_event` で、rule・auto mode・hook・sandbox が止めた・確認を求めた tool 呼び出しを集計できる | [2.1.307](https://github.com/anthropics/claude-code/releases/tag/v2.1.307) |
| sandbox の通信 | Copilot CLI 1.0.100 で、sandbox が **localhost と private network へのアクセスを既定で許可**。sandbox を「外へ出られない」前提にしていた構成では、社内の管理画面・DB・メタデータ endpoint に届くようになる。network 設定で明示的に絞る | [GitHub Copilot ガイド](../copilot/README.md#cli-1010010102-と-vs-code-1143--sandbox-の既定とskillplugin指示の入り方) |
| 信頼と導入の結びつき | Copilot CLI 1.0.100 で、信頼済みのリポジトリの Plugin を chat の前に自動で導入・更新する。VS Code 1.143 は組織が必須とした agent plugin を自動で導入する。**リポジトリを信頼する操作が、コードを入れる操作も兼ねる**ようになった | 同上 |
| 「verified」の意味 | Copilot CLI 1.0.100 の GitHub のインストールリンクは「verified」な Skill / Plugin を入れるとするが、基準は公開されていない（2026-10-22 確認）。[2 節](#2-導入前に何を確認するか)の確認を省かない | 同上 |
| 推論前の判定 | Inference hooks が 2026-10-20 に Beta を終了（Claude Enterprise）。ただし Anthropic が組織のために動かす Code Review・Claude Security のスキャン・smart reports、Bedrock / Google Cloud、Claude Platform の API 組織は対象外。**判定を通らない経路を一覧にしてから**、DLP の担当範囲を決める | [Claude Code の組織での統制](../claude-code/basics.md#導入時に確認すること)、[Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks) |
| 組織単位の Web 取得 | Claude Console の Capabilities で Web fetch を組織ごと無効化でき、Managed Agents の `web_fetch` は組織のドメイン制限と agent の `allowed_domains` / `blocked_domains` の**両方**を通った URL だけを取得する（redirect 先も対象）。`web_search` も組織の設定に従う（2026-10-20） | [Web ツールの URL 制限](#web-ツールが取得できる-url-を絞る2026-10-07)、[release notes](https://platform.claude.com/docs/en/release-notes/overview) |
| 最終顧客ごとの識別 | Claude API の user profiles（2026-10-20）で、自社サービスの顧客ごとの request を識別し、執行措置を 1 顧客に限定できる。制限・解除は organization webhooks（Beta）で受け取れる | [AIエージェントのID・認可・委任権限](agent-identity.md#誰のための-request-かをモデル提供者に伝える--claude-api-の-user-profiles2026-10-20) |
| sandbox の外で動いていた処理 | Claude Code 2.1.309（10-22）で、sandbox の Bash が**シェルの起動ファイルを sandbox の外で毎回実行していた**問題、`--mcp-config` の設定ファイルを sandbox 内から書き換えられた問題、`Edit(path)` の deny をリダイレクトで回避できた問題、Windows の PowerShell hook が終了コード 2 で止まらず fail-open していた問題を修正。**sandbox を境界にする端末は 2.1.309 以上に揃える** | [Claude Code](../claude-code/basics.md#21309--sandbox-と権限の境界の修正rewind-で戻らない操作)、[2.1.309](https://github.com/anthropics/claude-code/releases/tag/v2.1.309) |
| MCP の認証と資格情報 | Codex CLI 0.164.0（10-23）で、enterprise の MCP 接続を Codex のアカウントの権限か専用サインインで認証できる。リモートの Bash と Zsh snapshot では資格情報を伏せる。**伏せるのは表示とログで、コマンドへ渡すこと自体は止めない** | [Codex CLI 0.164.0](../codex/README.md#codex-cli-01640--presetsenterprise-mcp-の認証資格情報のマスク) |
| 依存パッケージの入口 | GitHub package firewall（2026-10-20、Public Preview、Enterprise Cloud、現時点は npm のみ）が、パッケージのメタデータ取得とダウンロードを、クールダウン期間・Advisory Database・attestation の検査で止める。coding agent や CI はレジストリへ直接つながず firewall を経由させる。**エージェントが入れる依存**の入口を、Skill とは別に絞る手段 | [GitHub package firewall](https://github.blog/changelog/2026-10-20-github-package-firewall-in-public-preview) |
| モデルの方針 | Copilot model policy API（2026-10-19、GA）で、enterprise・enterprise team・agent app・organization のモデルの提供範囲を API で取得・変更できる。enterprise は organization か team への委任を選ぶ | [GitHub Copilot ガイド](../copilot/README.md#モデルの方針を-api-で管理する--copilot-model-policy-api2026-10-19)、[changelog](https://github.blog/changelog/2026-10-19-copilot-model-policy-api-for-enterprise-orgs-and-teams) |

### 2026-10-23〜10-24 の権限境界の更新

2026-10-28 に公式資料を確認しました。release note と公式 changelog の照合のみで、実機・管理画面での確認はしていません。

| 層 | 変更と運用上の意味 | 詳細・一次情報 |
|---|---|---|
| hook の fail-open | Claude Code 2.1.310 で、**Windows で Git Bash がなく、hook の `command` が引用符で囲んだ文字列だけ**のとき、PreToolUse / PermissionRequest hook が実行されずに tool の呼び出しが通っていた問題を修正。**この条件の修正であり、すべての hook が fail-closed になったわけではない**。Windows に hook を配る組織は 2.1.310 以上に揃え、hook を起動できない状態で操作が止まるかを確かめる | [Claude Code 2.1.310](../claude-code/basics.md#21310--windows-の-hooksymlink-の行き先sandbox-が動かない理由) |
| 読み取りの確認 | 同じ版で、読み取りの確認画面に symbolic link の行き先を表示。**表示された名前ではなく、実際に読まれるファイル**を見て承認する | 同上 |
| sandbox が動かない理由 | Linux の `/sandbox` が Ubuntu の AppArmor による user namespace の制限を示すようになった。**sandbox が動かないことを、承認や除外を広げて回避しない**。ホストの制限を先に確かめる | 同上 |
| role と実行権限 | Enterprise の custom role で、cloud session と Remote Control を role ごとに許可できる。**role で使えることと、各リポジトリ・tool で実行できることは別の層** | 同上 |
| 通知からの書き込み | Teams の GitHub app で、届いた通知から Copilot に修正と PR の作成を頼める。通知が見える会話の参加者と、書き込むアカウントの権限を分けて確認する。旧 app は 2026-11-16 に廃止 | [GitHub Copilot ガイド](../copilot/README.md#teams-の通知から修正pr-まで進める2026-10-23と旧-app-の廃止11-16) |

### ローカルモデル・offline・telemetry は別の境界

「ローカルモデルを使う」ことと、「外部へ何も送らない」ことは同じではありません。GitHub Copilot CLI 1.0.94-0（2026-10-07）は `/model` で起動中の Ollama のモデルを追加できるようになりましたが、公式は**ローカルモデルの選択では offline mode にならず、GitHub の telemetry も止まらない**と明記しています。offline mode（`COPILOT_OFFLINE=true`）を有効にしても、provider がリモートならプロンプトとコード文脈はその provider へ送られます。**モデル・送信先・offline・telemetry を別々に確認**してください。**→ [GitHub Copilot ガイド](../copilot/README.md#ローカルモデルを使う--ollama-の発見と-offline-modecli-1094-0)**

### 承認の記憶がどこまで及ぶか

導入時の allowlist と同じく、**実行時に一度与えた承認がどの範囲で再利用されるか**も確認対象です。Codex CLI 0.152.0（2026-09-01）では、記憶された MCP tool の承認が**選択中の app account 単位**で扱われるようになりました。アカウントを切り替えれば、以前に与えた承認はそのまま引き継がれません。

これは権限分離そのものではなく、**記憶済みの承認の適用範囲**の話です。過大評価せず、marketplace の出自確認（[6 節](#6-同名の別パッケージという入口)）と併せて扱ってください。

導入時の承認にも、同じ確認が要ります。pnpm 12.11.0（2026-10-09）の agent skills は、依存パッケージが同梱した Skill を `pnpm approve` で承認したものだけリンクします。ただし**承認はパッケージ単位で、以降のバージョンにも及びます**。更新で Skill の中身が変わっても、新しい Skill が増えても、改めては聞かれません。pnpm は Skill の中身を読まず、承認画面にも Skill 名しか出ません。承認は「この発行元を信頼する」という判断として扱い、依存を更新するたびに `node_modules/<パッケージ>/skills/` の差分を読んでください。止めたいパッケージは `pnpm-workspace.yaml` の `permissions` で `skills: false` にし、機能ごと止めるなら `skills.dirs` を空リストにします。**→ [Skills 最新動向 7-6 節](../trends.md#7-6-pnpm--依存パッケージに同梱された-skill-をつなぐ)**

反対に、承認を**中身に**結びつける設計もあります。MCP の Skills 拡張（SEP-2640）は、MCP server から届く Skill について、記憶した承認を承認時の全ファイルの URI と SHA-256 digest の組に結びつけるようホストに求めています。1 ファイルでも変わる・増える・減ると承認は取り消され、もう一度聞かれます。あわせて、frontmatter の `allowed-tools` は利用者が認めない限り無視し、手元でのコード実行には Skill ごとの承認を取ることも求めています。ただし digest は同じ server が出す署名のない値なので、**承認した時点の中身が安全かどうかは保証しません**。**→ [MCP Skills 拡張 4 節](skills-over-mcp.md#4-ホストに課された承認とセキュリティの要件)**

**→ Codex の Plugin / MCP 運用は [Codex ガイド](../codex/README.md#5-plugin-でまとめて配る2026-08-の追加) を参照**

### 学習した memory を policy とみなさない

承認と同様に、**エージェントが書き込んだ memory がどこまで波及するか**も確認対象です。2026-09-25、GitHub の agentic autofix が Copilot Memory を使うようになりました（当時は両機能とも Public Preview、Copilot Memory を有効にしている場合。agentic autofix 自体は 2026-10-15 に [GA](../copilot/README.md#セキュリティ-alert-を直すエージェントとpr-の脆弱性検出--agentic-autofix-と-ai-scan)）。autofix は既存の memory を security alert 修正の文脈として読み、作成した修正の pattern を新しい memory として保存します。GitHub は、この memory が他の security alert の修正や、Copilot code review・Copilot cloud agent にも repository 固有の安全な開発 pattern として使われると説明しています。

memory は、組織が承認した規約ではなく**更新も削除もできる repository 固有の文脈**です。誤った修正 pattern が保存されると、後続の review や cloud agent の作業にも影響し得ます。

- security の規約として強制したい内容は、memory ではなく instructions・review の設定・managed settings など、レビューを通る場所に置く
- autofix の結果をマージする前の人の確認を省略しない
- どの memory が作られたかを定期的に確認し、誤りは削除・訂正する

**→ memory を長時間タスクの状態管理と区別する考え方は [長時間タスクの信頼性設計](agent-reliability.md#学習する-memory-を-checkpoint-と混同しない) を参照**

### エージェントが自分で書く Skill

memory と同じ問題は、**Skill そのもの**でも起きます。ここまでの確認は「人が選んで入れる Skill」を前提にしていましたが、エージェントが使いながら Skill を作り、書き換える製品が出てきました。[Hermes Agent](hermes-agent.md#9-skills-と記憶)（Nous Research、MIT）は `skill_manage` ツールで Skill を作成・部分修正・削除し、複雑なタスクの後やターン終了後の背景レビューでも更新します。既定では書き込みがすぐ反映され、**次回以降の手順そのものが、誰もレビューしないまま変わります**。

人が入れる Skill との違いは、導入前の確認が効かないことです。`gh skill preview` やコミット SHA の固定は「入れる瞬間」を押さえる手段で、入れた後に中身を書き換える主体がエージェント自身だと届きません。

| 確認すること | Hermes での方法 | 一般化した原則 |
|---|---|---|
| 書き込みを人が見てから反映する | `skills.write_approval: true` で保留にし、`/skills diff <id>` を読んで `/skills approve` / `reject` | 自動で育つ手順は、反映前の差分を人が読む |
| 自動の更新を止める | `auxiliary.background_review.enabled: false` | 学習のタイミングを、利用者が把握できる操作に限る |
| 他のツールへ波及させない | `skills.external_dirs` は**書き込み保護の境界ではない**と公式が明記。Claude Code・Codex と共有するディレクトリを指すと、そちらの Skill も書き換わり得る | 書き換えるエージェントと、固定して使うエージェントでディレクトリを分ける |
| 中身の検査を過信しない | 作成時のリンターは助言だけで書き込みを止めない。コンテキストファイルの注入検査も「見た目のパターンによる判定」と明記 | パターン検査は意図を判定しない |

Hermes の Hub（`hermes skills install`）は、インストール時に必ずスキャンを走らせ、取得元の信頼レベル（`builtin` / `official` / `trusted` / `community`）と合わせて判定します。`--force` で警告は越えられても `dangerous` の判定は越えられない設計で、[2 節](#2-導入前に何を確認するか)の確認を CLI が代行する形です。ただし取得元には [3 節](#3-第三者監査が示す実態)の監査対象だった ClawHub や skills.sh も含まれます。スキャンを通ったことは、`scripts/` の実行内容や外部への送信先を読んだことの代わりになりません。

本ガイドでは、自分で書き換えるエージェントを使う場合、**Skill のディレクトリを git で管理し、定期的に差分を読む**運用を推奨します。誤った手順が保存されたら、memory と同じく削除・訂正してください。

### OAuth consentを操作承認とみなさない

外部providerへのOAuth consentは、指定scopeで代理アクセスするgrantを作る手続きです。接続済みでtokenを再利用できても、個々の送信・公開・削除・購入まで承認済みという意味ではありません。

組織のIdPで利用者を認証し、downstream providerのgrantを同じ利用者・sessionへ結びつける**session binding**と、不可逆操作の直前に止める**human approval**を別々に実装します。tokenはbrowser、IDE、prompt、ログへ返さず、vault等で利用者・provider・scope・audienceに結びつけて保管・失効します。

**→ 用語、session binding、AgentCore Consent Portalの実装例は [AIエージェントのID・認可・委任権限](agent-identity.md#5-end-user-oauth-consentとsession-binding) を参照**

---

## 6. 同名の別パッケージという入口

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
| 依存パッケージから受け取る（pnpm） | 承認を発行元への信頼として扱い、依存を更新するたびに `skills/` の差分を読む（[5 節](#承認の記憶がどこまで及ぶか)） |
| チーム・組織へ配る | `managed-settings.json` で Marketplace と MCP サーバーを限定し、実行操作を `deny` / `ask` / `allow` に分ける |
| ハーネスごと持ち込む | 権限・承認・サンドボックスの既定値を確認する（[AI エージェントの実行基盤（ハーネス）](harness.md)） |
| エージェントが Skill を書き換える | 書き込みを承認制にし、Skill のディレクトリを git で管理して差分を読む。固定して使うツールとディレクトリを共有しない（[5 節](#エージェントが自分で書く-skill)） |
| コマンドを 1 つ入れる | 配布元が公式かを README で確認する・`which` で実体を見る（[6 節](#6-同名の別パッケージという入口)） |
| 組織で全社に展開する | 導入前の検査に加え、**推論前の許可判定と実行後の監査**まで設計する（[5 節](#5-統制が効く-3-つの段階)。いずれも組織向けプランが前提） |

---

## 関連ドキュメント

- [Skill / エージェントの評価（evals）](evals.md) — このページの**導入前**チェックに対して、**導入後**に実際に効いているかを測る話
- [エージェントに外部操作を与える手段の選び方](tool-selection.md) — 読み取り／入力／送信／購入／削除で承認の重さを分ける考え方
- [生成AIを業務で安全に使う](../business/safety.md) — **コードを書かない方向け**。入力してよい情報、外部送信、出力後の確認項目
- [Skills 最新動向](../trends.md) — 本ページの要約と、その他のテーマの動向
- [AI エージェントの実行基盤（ハーネス）](harness.md) — 標準が定めていない権限・承認・サンドボックスが実際に決まる層
- [Claude Code の Mods](../claude-code/mods.md) — 実行コードを持つ拡張の信頼境界、`plugin validate` での事前確認、`allowManagedModsOnly`
- [MCP Skills 拡張](skills-over-mcp.md) — MCP server から届く Skill の出所表示、内容に結びついた承認、`allowed-tools` の無視
- [Hermes Agent](hermes-agent.md) — Skill と memory を自分で書き換える常駐エージェント。Hub からの導入時のスキャン、`external_dirs` の共有
- [Agents 一覧](../copilot/agents.md) — 導入前監査に使える `trojan-skill-hunter` の解説
- [GitHub Copilot Plugins](../copilot/plugins.md) — `enabledPlugins` と Marketplace 制限の設定方法

## 参考リンク

- [Future Considerations](https://github.com/agentplugins/agent-plugins-spec/blob/main/FUTURE_CONSIDERATIONS.md) — v1.0.0 が扱わない領域（公式）
- [Snyk ToxicSkills study](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) — ClawHub / skills.sh の 3,984 Skill の監査結果（Snyk・2026-02-05）
- [MCP allowlists in enterprise managed settings](https://github.blog/changelog/2026-08-06-mcp-allowlists-in-enterprise-managed-settings/) — MCP 許可リスト（公式）
- [Enterprise managed settings in GitHub Copilot for JetBrains](https://github.blog/changelog/2026-08-18-enterprise-managed-settings-in-github-copilot-for-jetbrains/) — JetBrains への managed settings 拡大（公式）
- [Enterprise managed permissions for GitHub Copilot agent operations](https://github.blog/changelog/2026-09-09-enterprise-managed-permissions-for-github-copilot-agent-operations/) — 操作単位の managed permissions 一般提供（公式）
- [Enterprise managed settings reference](https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/enterprise-administrators/enterprise-managed-settings) — `deny` / `ask` / `allow` の優先順位と対象面（公式）
- [Enterprise managed sandbox in Copilot for JetBrains](https://github.blog/changelog/2026-09-08-enterprise-managed-sandbox-in-copilot-for-jetbrains/) — JetBrains の managed sandbox Public Preview（公式）
- [New features and improvements in Copilot for JetBrains](https://github.blog/changelog/2026-09-22-new-features-and-improvements-in-copilot-for-jetbrains/) — assisted approvals と MCP ツール制御（公式・2026-09-22）
- [gh skill マニュアル](https://cli.github.com/manual/gh_skill) — `gh skill preview` などのサブコマンド（公式）
- [Hermes Agent — Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) ／ [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) — `skill_manage`・`skills.write_approval`・Hub のスキャンと信頼レベル・`external_dirs`・背景レビュー（Nous Research 公式、2026-10-21 確認）
- [pnpm — Agent Skills](https://pnpm.io/agent-skills) ／ [設定 `permissions`](https://pnpm.io/settings/build#permissions) — 同梱 Skill の承認がパッケージ単位で以降のバージョンにも及ぶこと（pnpm 公式、2026-10-18 確認）
- [awesome-agent-skills-security](https://github.com/LLMSecurity/awesome-agent-skills-security) — 攻撃手法と防御策の一覧（コミュニティ）
- [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks) — 推論前の allow / deny 判定（Anthropic 公式）
- [Compliance API — session transcripts](https://platform.claude.com/docs/en/manage-claude/compliance-sessions) — 実行後のセッション取得（Anthropic 公式）
- [Compliance API — List user preferences](https://platform.claude.com/docs/en/manage-claude/compliance-org-data#list-user-preferences) — 保存された Instructions / Global instructions の取得（Anthropic 公式、Beta）
- [Managed Agents permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies) — ツール呼び出し単位の権限判定（Anthropic 公式・Beta）
- [Claude Code v2.1.271](https://github.com/anthropics/claude-code/releases/tag/v2.1.271) ／ [v2.1.273](https://github.com/anthropics/claude-code/releases/tag/v2.1.273) — command-scoped domain、Plugin command hash、managed MCP の fail-closed / 適用修正（公式）
- [Claude Code v2.1.280](https://github.com/anthropics/claude-code/releases/tag/v2.1.280) ／ [v2.1.281](https://github.com/anthropics/claude-code/releases/tag/v2.1.281) ／ [v2.1.282](https://github.com/anthropics/claude-code/releases/tag/v2.1.282) — symlink の着地点判定、setting source の伝播、managed rule の優先（公式・2026-09-22〜24）
- [Claude Code v2.1.283](https://github.com/anthropics/claude-code/releases/tag/v2.1.283) ／ [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) — managed `sandbox` の fail-closed、Skill deny rule の適用範囲、auto mode の開始モードの拡大（Anthropic 公式・2026-09-25）
- [Copilot CLI changelog](https://github.com/github/copilot-cli/blob/main/changelog.md) — 1.0.88 で ACP / AHP / `--server` のセッションに managed settings を適用（GitHub 公式・2026-09-22）
- [Local sandboxing in the GitHub Copilot app](https://github.blog/changelog/2026-09-23-local-sandboxing-in-the-github-copilot-app/) — project 単位の local sandbox と、cloud / remote / CLI との区別（GitHub 公式・2026-09-23、Public Preview）
- [VS Code 1.139 release notes](https://code.visualstudio.com/updates/v1_139) — remote host 上の Dev Container session（Microsoft 公式・2026-09-23）
- [Codex CLI 0.157.0 release](https://github.com/openai/codex/releases/tag/rust-v0.157.0) — redirect 後と継続中の通信への network policy 適用（OpenAI 公式・2026-09-25）
- [Enterprise managed settings in-product validator](https://github.blog/changelog/2026-09-25-enterprise-managed-settings-in-product-validator/) ／ [Default enablement of Copilot features](https://github.blog/changelog/2026-09-24-default-enablement-of-copilot-features-for-copilot-business-and-enterprise/) — managed settings の検証と新機能の既定ポリシー（GitHub 公式）
- [Agentic autofix now uses Copilot Memory](https://github.blog/changelog/2026-09-25-agentic-autofix-now-uses-copilot-memory/) — autofix による memory の読み書きと他機能への波及（GitHub 公式・2026-09-25、Public Preview）
- [Connect to a running session](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/sessions-connect) — Managed Agents の実行中セッションへの接続（Anthropic 公式）
- [CVE-2026-89332 — Kiro IDE Sensitive Workspace Data Exfiltration](https://aws.amazon.com/security/security-bulletins/2026-111-aws/) — AWSがImportantとして公開し、0.8.135以上で修正済み（`提供元`: Official / AWS ｜ `状態`: —）
- [CVE Record: CVE-2026-89332](https://www.cve.org/CVERecord?id=CVE-2026-89332) — 公開済みのCVE登録情報（`提供元`: Official / CVE Program ｜ `状態`: —）
- [Kiro Powers](https://kiro.dev/docs/powers/) — PowersがAgent Plugins形式でSkillとMCP設定を読み込む現在の仕様（`提供元`: Official / Kiro ｜ `状態`: —、2026-09-15確認）
- [Kiro Permissions](https://kiro.dev/docs/permissions/) — `deny` / `ask` / `allow` を含む現在の権限設定（`提供元`: Official / Kiro ｜ `状態`: —、2026-09-15確認）
- [garrytan/gbrain](https://github.com/garrytan/gbrain) — npm 上の同名別パッケージへの警告と `gbrain doctor`（README、一次情報）
