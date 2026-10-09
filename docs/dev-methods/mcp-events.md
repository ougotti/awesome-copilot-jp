# MCP Events — 外部の変化を受けてエージェントを動かす

> **対象ツール**: ChatGPT（Work chats・dots）と MCP サーバー ｜ **実行環境**: Chat UI / Cloud ｜ **対象読者**: エンジニア・MCP サーバー開発者 ｜ **最終更新**: 2026-10-08

> 通常の MCP は、エージェントが**呼んだときだけ** tool が動きます。MCP Events は逆向きで、**外部で起きた変化（文書へのコメント、チケットの更新など）をサーバーが通知し、それを受けてエージェントが作業を始める**仕組みです。このページは、ChatGPT が対応した MCP Events を、**利用者がやること**と**サーバー開発者がやること**に分けて整理します。

> **確認日: 2026-10-08**。OpenAI の [MCP Events](https://developers.openai.com/plugins/build/mcp-events) のドキュメントに基づきます。**MCP Events は draft の仕様**であり、ChatGPT はその一部（webhook による配信と callback の検証）に対応しています。標準化が完了した機能や GA として扱わないでください。また、ChatGPT での対応を他の MCP クライアントへ一般化しないでください。

---

## 1. 通常の tool・MCP Apps・Events の違い

| 仕組み | 誰が始めるか | 何が返るか | 詳しく |
|-------|-------------|-----------|-------|
| 通常の MCP tool | エージェント（呼んだとき） | テキストや構造化データ | [MCP ツールの契約設計](mcp-tool-contracts.md) |
| MCP Apps | エージェント（tool の結果として） | 会話内の UI | [MCP Apps](mcp-apps.md) |
| ChatGPT の Plugin Extensions | 利用者（サイドバー・パネル・ファイルビューアなど） | ChatGPT 固有の UI の入口 | [MCP Apps の ChatGPT 固有の拡張](mcp-apps.md#chatgpt-固有の拡張--plugin-extensions) |
| **MCP Events** | **外部の変化（サーバーが通知）** | 購読しているチャットで、利用者の指示に沿った作業が始まる | このページ |

## 2. 前提と対応範囲

| 項目 | 内容 |
|------|------|
| プロトコル | **MCP 2.0（protocol version `2026-07-28`）が必要** |
| 対応している配信 | webhook による配信と callback の検証 |
| 対応していない配信 | polling、streaming、draft の `gap` / `terminated` の制御通知 |
| 使える場所 | ChatGPT web の Work chats、デスクトップアプリの Work chats（Cloud を選択）、dots |
| 組織の制御 | plugin と、イベントで起動するタスクに対する workspace の制御が適用される |
| サーバー側に必要なもの | 購読を永続化する保存先と、callback URL への外向きの HTTPS 通信 |

## 3. 利用者の流れ — 監視を頼むときに決めること

1. サーバーが、対応しているイベントを一覧にする
2. 利用者が ChatGPT に、**何を監視し、どう対応するか**を伝える
3. ChatGPT がサーバーを通じて購読する（callback URL と署名用の secret を渡す）
4. サーバーが、条件に合うイベントをその URL へ送る
5. ChatGPT が、購読したチャットで、利用者の指示に沿ってイベントを処理する

**監視を頼む前に、次の 3 つを最初に決めます。**

| 決めること | 例 |
|-----------|----|
| 何を対象にするか（購読条件） | 「この文書への新しいコメント」だけ。全文書・全チャンネルにしない |
| 何をするか | 「コメントを要約し、回答案を作る。**投稿はしない**」 |
| いつやめるか（終了条件） | 「レビュー期限の 10 月 31 日まで」。期限を決めずに放置しない |

> **例: 文書へのコメントに回答案を作る**
> 「設計書 A に新しいコメントが付いたら、内容を要約して回答案をこのチャットに書いて。返信の投稿はしないで。10 月末で監視をやめて」
>
> 回答案を**自動で投稿させる**と、自分の投稿が新しいイベントになり、同じ処理が繰り返される可能性があります（[6 節](#6-失敗の観点--テストで確かめること)の自己再発火）。

## 4. サーバー開発者がやること

| 責任 | 内容 |
|------|------|
| 発見 | capabilities で `events` を示し、認証済みの MCP endpoint で `events/list`・`events/subscribe`・`events/unsubscribe` を実装する |
| 認可 | **そのアカウントが見てよいイベントだけ**を返し、購読を受け付ける前にアクセス権を確認する。購読中も権限を再確認し、**取り消されたら配信を止める** |
| 入力の検証 | イベント名と引数を検証する。`whsec_` で始まり、24〜64 バイトに復号できる secret を要求する |
| callback の検証 | 署名した challenge を送り、それを返す `2xx` 応答を要求する。失敗したらエラー `-32015` を返す |
| 永続化と冪等性 | 購読を**決定的な ID** で保存し、正規化した JSON で比較して重複を作らない。再起動後も購読を保持する |
| 署名 | Standard Webhooks で、購読ごとの secret を使って配信に署名する |
| 絞り込み | 文書 ID やチャンネル ID などの条件は、**配信前にサーバー側で**適用する |
| callback の安全 | HTTPS を必須にし、接続時に宛先を検証して**プライベート・非公開のアドレスを拒否**し、リダイレクトに従わない |

プロトコルの詳細なコードは、公式ドキュメントと [MCP Events の design sketch](https://github.com/modelcontextprotocol/experimental-ext-triggers-events/blob/main/docs/design-sketch-proposal.md) を参照してください。

## 5. 配信・重複・期限・再起動

| 観点 | 公式の説明 |
|------|-----------|
| 受け取りと処理は別 | **`2xx` は受け取りの確認**であり、ChatGPT はイベントを**非同期に**処理する。webhook が成功しても、タスクの処理が終わったわけではない |
| まとめて処理 | 別々に届いたイベントが、タスクのバッチ設定に従って 1 回の実行にまとめられることがある |
| 1 件の大きさ | 1 リクエストに 1 イベント、最大 256 KiB |
| 重複と再試行 | 再試行でも**同じ event ID** を使い、試行ごとに新しい timestamp と署名を付ける。一時的な失敗は指数バックオフで回数を限って再試行し、`410` / `413` は再試行しない |
| 順序 | 順不同で届き得る。**書き込みの tool は冪等にする** |
| 期限 | サーバーが付与した期限（`refreshBefore`）の前に、ChatGPT が `events/subscribe` を再度呼んで更新する。期限を過ぎると配信は止まる。`ttlMs: null` は期限なしの要求 |
| 再起動と取りこぼし | 購読の状態は再起動後も保持する。再生できるイベントは cursor で再開し、履歴がなければ `truncated: true` を返す。**再生できないイベントは、中断中に取りこぼした分をプロトコルでは回復できない** |

冪等性と重複の一般論は、[長時間タスクの信頼性設計](agent-reliability.md#5-冪等性重複実行外部副作用の扱い)と [MCP ツールの契約設計](mcp-tool-contracts.md) を参照してください。

## 6. 失敗の観点 — テストで確かめること

公式のテストの観点を、失敗の種類ごとにまとめます。

| 観点 | 確かめること |
|------|-------------|
| 発見と購読 | `server/discover` と `events/list` が届き、plugin のページにイベントが出る。購読すると `events/subscribe` が届き、検証が成功し、購読が保存される |
| 絞り込みの不一致 | 条件に**合う**イベントだけが届き、**合わない**イベントは届かない |
| 重複 | 同じイベントが重複して届いても、作業が二重にならない |
| 再起動後の購読 | 再起動をまたいで期限と更新が正しく動く |
| 失効・解除 | 解除したら配信が止まる。期限切れで配信が止まる |
| 権限の喪失 | アクセス権を取り消したら配信が止まる |
| 署名の不正 | 不正な署名の配信が拒否される |
| **自己再発火** | 依頼した作業が元のアプリのデータを変える場合、その変更が新しいイベントになって**繰り返しが起きない**（公式も、フィードバックループにならないか確認するよう明記） |
| バッチ | バッチ設定のオン・オフで期待どおりに処理される |

## 対象外

- 実際の plugin の登録・公開、購読の設定、外部への送信は扱いません。
- 全 MCP サーバーに Events 対応が必要だとは考えません。変化を待つ必要がない tool には不要です。
- MCP 本体の移行判断は [最新動向 13 節](../trends.md#13-mcp-2026-07-28-仕様と移行時の確認) を参照してください。

## 関連ドキュメント

- [MCP Apps — 会話内にUIを追加する](mcp-apps.md) — 会話内の UI と、ChatGPT 固有の Plugin Extensions
- [MCP ツールの契約設計](mcp-tool-contracts.md) — 入出力・副作用・再試行・冪等性
- [長時間タスクの信頼性設計](agent-reliability.md) — 重複実行と checkpoint
- [プラグインの可搬性](plugin-portability.md) — ホスト独自の拡張と可搬な部分の区別
- [Codex ガイド](../codex/README.md#個人の定期作業dotsteam-tasksを選ぶ) — dots と定期作業

## 参考リンク

- [MCP Events](https://developers.openai.com/plugins/build/mcp-events) — 前提、対応する配信、購読・認可・配信・解除・テスト（OpenAI 公式）
- [MCP Events design sketch](https://github.com/modelcontextprotocol/experimental-ext-triggers-events/blob/main/docs/design-sketch-proposal.md) — draft の設計案
- [Standard Webhooks](https://github.com/standard-webhooks/standard-webhooks) — 署名の方式
- [Dots](https://learn.chatgpt.com/docs/dots) — ChatGPT の dots（OpenAI 公式）
