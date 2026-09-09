# MCP Apps — 会話内にUIを追加する

> **対象ツール**: ツール横断（Claude・Claude Desktop・VS Code GitHub Copilot ほか対応ホスト） ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-09

[MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) は、MCP サーバーが tool 呼び出しの結果として**インタラクティブな UI**（HTML/JS）を返せるようにする拡張です。テキストの戻り値だけでは伝えづらい・操作しづらい場面を補う手段として、いつ使うか・どう作るか・対応していないホストでどうなるかを整理します。

---

## 1. テキストだけでは不便な場面

tool の戻り値をテキスト（表・JSON の整形）で返せば大抵は足ります。UI を検討するのは、次のような**操作**が必要になったときです。

- 表形式のデータを**並べ替え・絞り込み**しながら見たい（テキストだと毎回 tool を呼び直すしかない）
- グラフ・チャートなど、テキストでは表現しにくい可視化が要る
- フォームで**複数項目をまとめて入力**してから 1 回で送信したい（会話のターンごとに 1 項目ずつ聞くのは冗長）
- 候補一覧から**選択**させたい（自由記述より誤変換・表記揺れが少ない）

逆に、単発の値の確認・単純な一覧の表示・1〜2 項目の入力で済む場合は、UI を追加する理由がありません。テキストの tool 結果で十分です。

---

## 2. 30秒で見分ける表

| | 通常の tool 呼び出し（テキスト結果） | MCP Apps（UI resource） | Computer Use |
|---|---|---|---|
| 返すもの | 文字列・構造化データ | HTML/JS の UI（サンドボックス化された iframe） | なし（既存 GUI を画面ごしに操作） |
| 対象 | エージェントが読む | **人間がその場で操作**する | エージェントが画面を見て操作する |
| 前提 | ホストが tool 結果を表示できればよい | **ホストが MCP Apps に対応している必要がある**（[5 節](#5-対応ホストの確認とfallback)） | API のない GUI しか手段がない場合の最終手段 |
| 主な用途 | 大半のツール呼び出し | 表の並べ替え・可視化・複数項目フォームなど、その場の操作が要る場面 | ブラウザ操作の自動化など |

**Computer Use との違いに注意してください。** Computer Use は「人間の代わりにエージェントが GUI を操作する」手段（[エージェントに外部操作を与える手段の選び方 6 節](tool-selection.md#6-computer-use--api-のない-gui-と最終画面確認)）です。MCP Apps は逆に、**エージェントが人間に操作させるための UI を tool 結果として提供する**手段であり、操作する主体が異なります。

---

## 3. 仕組み

MCP Apps は既存の MCP の tool・resource の仕組みに乗ります。新しいプロトコル層を足すのではなく、次の組み合わせです。

1. **tool** の定義に `_meta.ui.resourceUri` を持たせ、どの UI resource を使うかを示す
2. その resource を `ui://` スキームで公開する。中身は HTML/JS のバンドル
3. ホストは tool 呼び出しの結果を受け取ると、対応する `ui://` resource を**サンドボックス化された iframe**内で描画する
4. iframe 内の UI は MCP サーバーと直接通信しない。**postMessage 経由で `ui/` プレフィックスの JSON-RPC メソッド**（`ui/callTool` など）をホストへ送り、ホストが仲介して実際の tool 呼び出しをサーバーへ渡す

**iframe はサーバーへの直接アクセス経路を持ちません。** すべてホストを経由するため、ホスト側が承認・権限・レート制限を挟む余地があります（[6 節](#6-データの見え方外部通信権限の境界)）。

---

## 4. 最小例（架空の地域別売上データ）

公式の [Build a UI for an MCP Server](https://modelcontextprotocol.io/extensions/apps/build) ガイドに沿った最小構成です。ここではコードは転載せず、架空の「地域別売上（読み取り専用）」を表示する例として、前提から期待結果までの手順だけを示します。実コードは公式ガイドを参照してください。

**前提**

- Node.js が動く CLI 環境（作業ディレクトリは任意の新規プロジェクトフォルダ）
- Claude Code などのコーディングエージェントを使う場合、`/plugin marketplace add modelcontextprotocol/ext-apps` → `/plugin install mcp-apps@modelcontextprotocol-ext-apps` でスキルを導入すると雛形生成を任せられる（Claude Code 以外は `npx skills add modelcontextprotocol/ext-apps`）
- 手動で組む場合は、`registerAppTool` / `registerAppResource`（サーバー側）と、UI 側の `App` クラス（`.connect()` でホストに接続し、`.ontoolresult` で tool 結果を受け取り、`.callServerTool()` でサーバーの別 tool を呼び戻す）を使う

**起動**

1. サーバーをビルドし、ローカルで起動する（公式ガイドのビルド・serve 手順に従う）
2. 地域別売上を返す tool（例: `get_regional_sales`）が `_meta.ui.resourceUri` で UI resource を指すことを確認する

**ホスト接続**

- 対応ホスト（[5 節](#5-対応ホストの確認とfallback)）から、ローカルサーバーへ接続する。Claude で試す場合は、`cloudflared` などのトンネル経由でカスタムコネクタとして登録する方法と、同梱の basic-host テストサーバーで確認する方法の 2 通りが公式ガイドに載っている
- 実運用のリモート配布は本ページの対象外（[対象外](#対象外)）

**期待結果**

- 会話内で「地域別の売上を見せて」のように依頼すると、tool が呼ばれ、その結果として地域別の表（並べ替え可能な UI）がその場に描画される
- 表内で並べ替え・絞り込みをしても、追加の会話ターンなしにその場で反映される（サーバー側の別 tool を呼び直す設計にした場合は `callServerTool()` 経由で反映される）

> このデータセットは架空のものです。実データに置き換える場合は、[6 節](#6-データの見え方外部通信権限の境界)のデータ露出範囲を必ず見直してください。

---

## 5. 対応ホストの確認とfallback

**MCP Apps は「対応しているホストでのみ」UI が描画されます。すべての MCP クライアントで動くわけではありません。** 公式ページが明示している対応ホスト（2026-09 時点）は次のとおりです。

- Claude / Claude Desktop
- VS Code GitHub Copilot
- Microsoft 365 Copilot
- Goose
- Postman
- MCPJam
- Archestra.AI

> Host support varies by client — 公式ページ自身がこう明記しています。上記リストは今後変わるため、導入前に[公式ページの Client support 節](https://modelcontextprotocol.io/extensions/apps/overview)で最新状況を確認してください。

**対応していないホストでは何が起きるか。** tool 自体は通常の MCP tool として動作し続けます。UI resource が描画されないだけで、**tool のテキスト/構造化データとしての戻り値はそのまま使えます。** UI はあくまで戻り値に対する追加の表現手段であり、UI 抜きでも意味が通るテキスト結果を tool 側で用意しておくのが安全な設計です（対応ホストでは UI、非対応ホストではテキストにフォールバックする、という前提で tool の戻り値を設計してください）。

---

## 6. データの見え方・外部通信・権限の境界

UI は**サンドボックス化された iframe**内で動きます。境界は主に 2 つの `_meta.ui` フィールドで宣言します。

| フィールド | 役割 |
|-----------|------|
| `_meta.ui.permissions` | iframe に許可する操作範囲を宣言する |
| `_meta.ui.csp` | iframe に適用する Content Security Policy。外部リソースの読み込み先を制限する |

**iframe から MCP サーバーへの経路は、常にホストの仲介を通ります。** UI が直接サーバーへリクエストを送ることはできず、`postMessage` で `ui/callTool` などをホストに依頼し、ホストが実際の tool 呼び出しを行います。これにより、ホスト側が承認を挟む・呼び出し内容を検査する余地が生まれます。

**この構図は [エージェントに外部操作を与える手段の選び方 8 節「承認境界」](tool-selection.md#8-承認境界--読み取り入力送信購入削除で分ける)と地続きです。** UI 上のボタンが「読み取り」なのか「送信・削除などの不可逆操作」なのかで、ホスト側にどこまで承認を挟ませるべきかが変わります。UI を設計する際は、ボタン 1 つが呼び出す tool の性質（読み取り／入力／送信・購入・削除）を意識し、不可逆な操作には UI 内でも確認ステップを設けてください。

**データの見え方についても要注意です。** UI に渡すデータは tool の戻り値に含まれる範囲がそのまま iframe 内で見える前提で設計してください。会話履歴やシステムプロンプトが自動的に UI 側へ渡るわけではありませんが、tool が返す `_meta` や resource の中身に機微な情報を含めないよう、サーバー側の tool 設計で範囲を絞る必要があります。

---

## 7. 自分のツールにUIを付けるか判断する

| 状況 | 判断 |
|------|------|
| tool の戻り値が単純な値・短い一覧で、テキストのまま十分伝わる | UI は不要です |
| 表の並べ替え・絞り込み・可視化など、**その場での操作**が繰り返し必要になる | MCP Apps の導入候補です |
| 複数項目をまとめて入力させたい（会話ターンで 1 項目ずつ聞くと冗長） | フォーム UI の導入候補です |
| 利用者のホストが MCP Apps に対応しているか不明・対応ホストを選べない | まずテキストの戻り値だけで tool を作り、対応ホストが確認できてから UI を追加する（[5 節](#5-対応ホストの確認とfallback)の fallback 前提を活かす） |
| UI 内のボタンが送信・購入・削除など不可逆な操作を呼ぶ | UI 内にも確認ステップを設け、ホスト側の承認境界（[6 節](#6-データの見え方外部通信権限の境界)）を前提に設計する |

**多くの tool にとって、UI は「あれば嬉しい」であって「必須」ではありません。** 対応ホストが限られる以上、UI 抜きでも成立するテキスト結果を先に作り、UI はその上に重ねる追加要素として位置づけるのが安全です。

---

## 対象外

- MCP Apps SDK の全 API・全言語実装の転載
- リモートホスティング・本番配布のインフラ構成（公式ガイドのローカル検証手順の範囲まで）
- 個別ホスト（Claude Desktop・VS Code Copilot 等）ごとの UI 描画差分の網羅的な比較
- Computer Use の詳細な使い分け（[エージェントに外部操作を与える手段の選び方 6 節](tool-selection.md#6-computer-use--api-のない-gui-と最終画面確認)を参照）

## 関連ドキュメント

- [エージェントに外部操作を与える手段の選び方](tool-selection.md) — 承認境界（8 節）、Computer Use との違い（6 節）
- [MCP と A2A — 役割の違いと併用方法](agent-protocols.md) — MCP の tool / resource / prompt の基本構造
- [Skills 最新動向](../trends.md#13-mcp-の次期仕様) — MCP 2026-07-28 仕様全体と Apps・Tasks 拡張の位置づけ

## 参考リンク

- [MCP Apps Overview](https://modelcontextprotocol.io/extensions/apps/overview) — 拡張の仕組み、対応ホスト一覧、セキュリティモデル
- [Build a UI for an MCP Server](https://modelcontextprotocol.io/extensions/apps/build) — 最小構成の作り方、テスト手順
- [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps) — 公式 SDK・サンプル実装
