# MCP Events — 外部の更新から作業を続ける

> **対象ツール**: ChatGPT Work・dots、MCPサーバー開発 ｜ **実行環境**: Chat UI / Cloud ｜ **対象読者**: 業務の自動化担当・エンジニア・サーバー運用者 ｜ **最終更新**: 2026-10-02

新しい文書コメントや状態変更を受けて、ChatGPTが作業を続けるための仕組みです。通常のtoolが「エージェントから問い合わせる」入口なのに対し、Eventsではサーバーが購読条件に合う更新を届けます。本ページは[OpenAI公式のMCP Events実装ガイド](https://developers.openai.com/plugins/build/mcp-events)を2026-10-02に確認した内容です。

## 1. UI・tool・イベントを選ぶ

| 必要なこと | 選ぶ仕組み | 対応範囲・状態 |
|------------|------------|----------------|
| その場でデータを読む・操作する。 | MCP tools。 | ホストのtool対応とサーバーの認可を確認する。 |
| 会話内の表やフォームを人が操作する。 | [MCP Apps](mcp-apps.md)。 | MCPのUI拡張。対応ホストで描画する。 |
| ChatGPTのsidebar・会話横・file viewerにUIを出す。 | [Plugin Extensions](mcp-apps.md#chatgptのplugin-extensions2026-10-02確認)。 | OpenAI公式のホスト固有拡張。提供面・プランに条件がある。 |
| 更新を受けて監視中の仕事を続ける。 | MCP Events。 | OpenAI公式のChatGPT連携。採用するEvents仕様はDraftで、GAの標準仕様とは扱わない。 |

ChatGPTのMCP Eventsは **MCP 2.0（protocol version `2026-07-28`）** が前提です。2026-10-02確認時点で、**WebのWorkチャット、desktop appでCloudを選んだWorkチャット、dots** で利用できます。Pluginsとイベント起動に関するworkspace controlsも適用されます。CLIや他ホストの対応は、このChatGPT向けガイドからは判断できません。

対応しているのはDraftの **webhook deliveryとcallback verification** です。polling、streaming、`gap` / `terminated`制御通知はこの連携では非対応です。すべてのMCP利用者がEventsを導入する必要はありません。既存の時刻・Gmail / Slack / GitHub起動は[Scheduled tasks](../codex/README.md#6-定期イベントで動かすscheduled-tasks)、MCP本体の移行は[最新動向13節](../trends.md#13-mcp-2026-07-28-仕様と移行時の確認)を参照してください。

## 2. 利用者とサーバー運用者の準備

| 役割 | 用意すること | 最初に確認すること |
|------|--------------|--------------------|
| 利用者 | Events対応pluginへの接続、監視対象、絞り込み条件、行う作業、終了条件。 | 利用できるWork / Cloudの面とworkspace設定、接続アカウントで対象資料を読めるか。 |
| サーバー開発・運用者 | event discovery、購読API、永続ストレージ、callbackへのoutbound HTTPS、署名・検証・再送処理。 | 購読者の権限でevent一覧・対象・payloadを制限し、再起動・期限・失効を扱えるか。 |

利用者が毎回webhook URLやsecretを入力する構成ではありません。ChatGPTが購読時にcallback URLと署名secretを渡し、サーバーが検証して保持します。署名secretはログや説明用の出力へ含めません。

## 3. 最小例 — 文書コメントから要約と返信案を作る

これは説明用の依頼文で、実際の購読・外部送信はこのガイドでは検証していません。Events対応pluginを接続したWorkチャット（Web、またはdesktopのCloud）で入力する例です。

```text
文書「週次案件報告」の新しいレビューコメントを監視してください。
対象はこの文書の comment.created だけです。他の文書は対象外です。
新着ごとにコメントの出典を示し、論点を要約して返信案をこのチャットに作ってください。
返信の投稿や文書の更新は、私が確認して依頼してから行ってください。
自分が投稿したコメントは対象外にしてください。
2026-10-09 18:00（Asia/Tokyo）で購読を解除してください。
私が「監視を終了」と伝えた場合も解除し、停止結果を報告してください。
```

終了時刻・自身の投稿の除外がpluginのschemaや実装でどう表現されるかを確認します。指示文だけでサーバー側のfilterや期限が保証されるわけではありません。対応できない条件は、開始前に代替策と停止手順を決めます。

1. pluginの詳細にevent定義が表示されるか確認する。tools / eventsを変更した場合はrescanする。
2. サーバーの`events/list`で、`comment.created`と対象文書のfilterが発見される。
3. ChatGPTの`events/subscribe`に期待した条件が渡り、callback検証と購読保存が成功する。
4. 対象文書に試験コメントを作り、event受信後に出典・要約・返信案が作られるか確認する。対象外の文書では配信されないことも確かめる。
5. 「監視を終了」と伝え、`events/unsubscribe`とサーバーの購読状態を確認する。次の試験コメントが届かないことまで確認する。

**webhookの2xxは受領を示し、仕事の完了を示しません。** 処理は非同期で、複数eventが1回のtask runへまとめられる場合もあります。event受領、task run、返信案の完成を別々に確認します。停止後も、受領済みのrunや完了済みの外部操作は別に点検します。

## 4. サーバー側の購読ライフサイクル

同じ認証済みMCP endpointで、次の流れを実装します。具体的なSDK構文は[公式実装ガイド](https://developers.openai.com/plugins/build/mcp-events)を参照してください。

| 段階 | サーバーが行うこと |
|------|--------------------|
| 発見 | `server/discover`のcapabilitiesで`events`を広告する。`events/list`はevent名・delivery mode・購読引数の`inputSchema`・eventデータの`payloadSchema`を返す。利用者が許可された対象だけを見せる。 |
| 購読 | `events/subscribe`で所有者、event、引数、対象へのアクセスを確認する。同じprincipal / callback / event / 引数の再購読は同じ購読として扱い、正規化した引数で重複を防ぐ。 |
| callback検証 | 配信前に署名付きの短命・一回限りのchallengeを送る。2xxとchallengeの一致を確認し、成功は期限を設けてcacheする。 |
| 保存 | 所有者、filter、callback、secret、期限を永続化する。サーバー再起動後も購読を復元し、権限を継続的に再確認する。 |
| 配信 | 条件に合うeventだけを送る。`eventId`、`name`、timezone付き`timestamp`、schemaに合う`data`、`cursor`を持たせる。 |
| 更新 | `refreshBefore`より前に再購読し、同じ購読とcursorを保って期限を更新する。`ttlMs: null`の要求だけで無期限になったとは判断しない。 |
| 解除・失効 | `events/unsubscribe`は元のevent / 引数 / callbackを照合し、認可して冪等に解除する。解除・期限切れ・権限失効後の新しい配信を止める。 |

callbackは **HTTPSのみ** です。接続時のDNS解決先も検証してprivate / localなど公開されていない宛先を拒否し、redirectへ追従せず、hostnameのTLS検証を維持します。callback検証とevent配信の両方に適用します。

署名はStandard Webhooksに従い、`webhook-id` / `webhook-timestamp` / `webhook-signature`と`X-MCP-Subscription-Id`を使用します。署名したserializationの**同じbytes**を送ります。secret更新時は必要に応じて短い新旧重複期間を設けます。

## 5. 配信・回復の制約

| 条件 | 設計・確認すること |
|------|--------------------|
| 同じeventの再送 | `eventId`を保ち、timestampと署名は新しくする。一時的なエラーには上限付き指数backoffを使う。410 / 413には再送しない。 |
| 重複・順不同 | 配信順序を前提にせず、eventの重複排除と更新toolの冪等性をそれぞれ設計する。[tool契約の詳細](mcp-tool-contracts.md)を参照する。 |
| 大きいpayload | 1 requestに1 event、body全体は256 KiB以下。大きな資料は要約とIDを送り、認可した読み取りtoolで取得する。ユーザー由来の本文は指示ではなくデータとして扱う。 |
| replay | cursorは未配信eventを飛ばさない。履歴が失われたときは`truncated: true`、replay非対応は`cursor: null`。後者では取り逃したeventをこのprotocolで回収できないため、別の読み取り・突合手順を用意する。 |
| 接続・権限の失効 | 購読中も権限を再確認し、失効した対象の配信を止める。購読時の成功だけを認可の根拠にしない。 |
| 自分の操作が次のeventを作る | 投稿者・対象・処理済みIDなどで循環を防ぐ。eventの重複排除だけでは、新しいIDで発生する自己起動を防げない。 |

## 6. 導入前の確認項目

以下はサーバー・pluginの検証環境で行うチェックです。

- [ ] 対象eventは届き、filterに合わないevent・未許可の対象は配信されない。
- [ ] 同じ条件で二度購読しても二重配信されず、同じeventの再送で更新が重複しない。
- [ ] サーバー再起動後も購読が残り、期限前のrefresh・期限切れの停止が動く。
- [ ] 解除後・接続解除後・権限失効後に新しい配信が止まる。
- [ ] 不正な署名、callback検証の失敗、許可されないcallback宛先を検証用受信先で拒否する。
- [ ] burst時はbatchingの有無を変えて、受領数とrun・成果物を突合する。順不同・履歴消失からの回復も確認する。
- [ ] 書き込みが自身のeventを生む場合に循環せず、外部送信には利用者が指定した確認条件が守られる。

## 関連・公式資料

- [MCP Events（OpenAI公式）](https://developers.openai.com/plugins/build/mcp-events) — 対応面、購読・署名・callback・回復とChatGPTでの試験手順。
- [Draft MCP Events specification](https://github.com/modelcontextprotocol/experimental-ext-triggers-events/blob/main/docs/design-sketch-proposal.md) — 公式実装ガイドが参照するDraft。ChatGPTの対応範囲は実装ガイドで確認する。
- [Plugin Extensions（OpenAI公式）](https://developers.openai.com/plugins/build/extensions) — ChatGPTのUI拡張。
- [長時間タスクの信頼性設計](agent-reliability.md) — checkpoint、停止・再開、再試行の判断。
- [AIエージェントのID・認可・委任権限](agent-identity.md) — 認証、認可、個別操作の確認の区別。
