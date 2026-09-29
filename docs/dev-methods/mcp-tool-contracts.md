# MCP ツールの契約設計 — 入出力・副作用・失敗を先に決める

> **対象ツール**: ツール横断（MCP を利用する Claude Code・Codex・GitHub Copilot ほか） ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: MCP サーバー開発者・エージェント運用者 ｜ **最終更新**: 2026-09-29

> [外部操作の手段の選び方](tool-selection.md)は「MCP を使うか」を、[MCP と A2A](agent-protocols.md)はプロトコルの役割を扱います。このページは **MCP の Tool を公開すると決めた後**、呼び出し側とサーバー側の契約をどう設計・検証するかに絞ります。以下は [MCP 2026-07-28 版の Tools 仕様](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)を基にしています。

---

## 1. 最初に決める 5 つのこと

| 決めること | 契約に書くもの | 動作で確かめること |
|---|---|---|
| 何をするか | 目的が一つに定まる `name`・`description` | 似た Tool の中から適切なものが選ばれるか。 |
| 何を受け取るか | `inputSchema` の型・必須項目・範囲 | 範囲外の値や余分な項目を拒否するか。 |
| 何を返すか | 必要なら `outputSchema`、`structuredContent` と短い `content` | 成功結果がスキーマに合い、利用者が結果を確認できるか。 |
| 何が変わるか | 読み取りと更新の別、更新対象、再試行条件 | 拒否・失敗・再送で予期しない副作用が出ないか。 |
| 誰が使えるか | 利用者・対象ごとのサーバー側認可、クライアント側の確認 | 権限外の対象に届かず、機微な操作を実行前に止められるか。 |

`inputSchema` は引数の形を記述する JSON Schema です。2026-07-28 版ではルートを object とし、指定しなければ JSON Schema 2020-12 として扱われます。`outputSchema` は任意ですが、定義した場合、サーバーはそれに適合する `structuredContent` を返す必要があります。これらのスキーマは **入力値や戻り値の型**を定めるものであり、利用者が操作を許されているかは別途サーバーが判定します。[Tools 仕様](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#security-considerations)は入力検証・アクセス制御・レート制限・出力のサニタイズをサーバーの要件としています。

## 2. 読み取りと更新を別の Tool にする

架空の社内 Issue 管理サービスを考えます。「Issue の現状を確認する」と「Issue をクローズする」を一つの `manage_issue` に混ぜると、Tool の名前だけでは副作用を判断できません。次の二つに分けると、呼び出し前に結果を見積もれます。

| Tool | 入力 | 結果 | 副作用 |
|---|---|---|---|
| `get_issue` | `issue_id` | 状態・現在の `version`・URL | なし。 |
| `close_issue` | `issue_id`・`expected_version`・`request_id` | 更新後の状態・`version`・`operation_id` | 指定 Issue の状態を変える。 |

`close_issue` の Tool 定義例です。これは **Tool 記述子の例**であり、この JSON だけで動く MCP サーバーにはなりません。`request_id` と `expected_version` はこのサービスで設計した引数で、MCP の予約フィールドではありません。

```json
{
  "name": "close_issue",
  "description": "指定した Issue をクローズする。呼び出し前に対象と現在の状態を確認する。",
  "inputSchema": {
    "type": "object",
    "properties": {
      "issue_id": { "type": "string", "minLength": 1 },
      "expected_version": { "type": "integer", "minimum": 0 },
      "request_id": { "type": "string", "minLength": 1 }
    },
    "required": ["issue_id", "expected_version", "request_id"],
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "issue_id": { "type": "string" },
      "state": { "const": "closed" },
      "version": { "type": "integer" },
      "operation_id": { "type": "string" }
    },
    "required": ["issue_id", "state", "version", "operation_id"],
    "additionalProperties": false
  },
  "annotations": {
    "readOnlyHint": false,
    "destructiveHint": true,
    "idempotentHint": true
  }
}
```

この例で `idempotentHint: true` と宣言できるのは、**サーバーが同じ呼び出しの重複実行を防ぐ場合だけ**です。サーバーは利用者と `request_id` の組で最初の結果を記録し、同じ引数で再送されたら同じ `operation_id` と結果を返します。同じキーに異なる引数が来たら拒否します。初回は `expected_version` と現在の版を照合し、更新と重複記録を一つの原子的な処理にします。これが実装できなければ `idempotentHint` を付けず、タイムアウト後の自動再試行を安全とみなしてはいけません。再試行全体の設計は [長時間タスクの信頼性設計](agent-reliability.md#5-冪等性重複実行外部副作用の扱い)を参照してください。

`readOnlyHint`・`destructiveHint`・`idempotentHint` は **ヒント**です。外部の相手や Web に触れる範囲を表す `openWorldHint` もあり、未指定時は `true` とみなされます。[ToolAnnotations の定義](https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations)と[公式解説](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)は、未信頼のサーバーが付けた注釈を安全性の証明として扱わないよう求めています。`readOnlyHint: true` でも、実際に書き込めない権限と実装で制限してください。

## 3. 成功・失敗をモデルにも機械にも伝える

成功時は、機械が読む `structuredContent` に `outputSchema` に合う値を入れます。`content` にも同じ値を JSON テキストとして含めると、構造化結果を読まないクライアントとの互換性を保てます。2026-07-28 版では `structuredContent` は object に限らず任意の JSON 値を取れますが、ここではキーを持つ object にして結果の意味を明示します。[Tools 仕様](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#structured-content)の推奨に沿った、**Tool 呼び出し結果の中身**の例です。

```json
{
  "resultType": "complete",
  "content": [
    { "type": "text", "text": "{\"issue_id\":\"ISS-42\",\"state\":\"closed\",\"version\":8,\"operation_id\":\"op-73\"}" }
  ],
  "structuredContent": {
    "issue_id": "ISS-42",
    "state": "closed",
    "version": 8,
    "operation_id": "op-73"
  },
  "isError": false
}
```

失敗は原因で分けます。**存在しない Tool や壊れたリクエスト**は JSON-RPC の protocol error、**業務上の失敗**（古い版、不正な日付、下流 API の失敗など）は `isError: true` の Tool 結果として返します。後者はモデルが引数を修正できる情報を含め、秘密情報や内部ログをそのまま返さないようにします。[Tools 仕様の Error Handling](https://modelcontextprotocol.io/specification/2026-07-28/server/tools#error-handling)に区別が示されています。

```json
{
  "resultType": "complete",
  "content": [
    { "type": "text", "text": "Issue ISS-42 の版が変わりました。状態を取得し直してください。" }
  ],
  "isError": true
}
```

大量の検索結果を返す Tool なら、業務データ側にも `limit`・`cursor` を設け、1 回の出力を制限します。`tools/list` 自身のページングは **Tool 定義の一覧**を分割する仕組みで、`search_issues` が返す **Issue 一覧**のページングとは別です。特定の呼び出しの結果をどこまで返すかは、その Tool の契約で決めます。

## 4. 確認 UI とサーバー側認可を分ける

MCP は Tool の呼び出しを人が拒否できる設計を推奨していますが、特定の確認画面をプロトコルで強制しません。機微な更新の **実行前確認**はクライアント側で、対象 Issue を操作できるかの **認可**はサーバー側で行います。サーバーは `issue_id` と利用者の権限を毎回照合し、`expected_version` も再確認します。画面で一度確認したという事実だけで、権限や状態の再確認を省略してはいけません。[Tools 仕様の User Interaction Model と Security Considerations](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)を参照してください。OAuth scope・token audience・委任権限の詳細は [AI エージェントの ID・認可](agent-identity.md)にまとめています。

## 5. 最小の確認手順

Tool を実装したら、開発中のサーバーを [MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector) に接続します。Node.js 22.19.0 以降が必要です。PowerShell で `npx @modelcontextprotocol/inspector` を実行し、表示された URL を開いて、対象サーバーの起動コマンドまたは URL を指定します。これは**開発用の手動確認**であり、この記事の JSON を実行するコマンドではありません。

| 確認場所 | 試す操作 | 期待する結果 |
|---|---|---|
| Inspector | `tools/list` で Tool 定義を読む。 | 名前・説明・入出力スキーマ・注釈が意図どおりである。 |
| Inspector / サーバーのテスト | `get_issue` で対象を読む。 | 状態と `version` が返り、対象の状態は変わらない。 |
| Inspector / サーバーのテスト | `close_issue` を有効な版で呼ぶ。 | 戻り値が `outputSchema` に合い、対象だけが更新される。 |
| サーバーのテスト | 古い `expected_version` や権限外の Issue を渡す。 | 更新せず、呼び出し元が失敗を判別できる。 |
| サーバーのテスト | 同一の `request_id` と引数で再送する。 | 状態更新が重複せず、同じ操作の結果を返す。 |
| Inspector CLI（`--method tools/call --tool-name missing_tool`） | 存在しない Tool を呼ぶ。 | Tool の業務エラーではなく protocol error になる。 |
| 利用するホスト | 機微な更新の実行前表示を確認し、拒否する。 | 対象と引数を確認でき、拒否時はサーバーへ更新呼び出しが届かない。 |

確認 UI の有無・表示・記憶した承認の範囲はホストに依存します。Inspector での契約確認に加え、**実際に使うホスト**でも更新前の表示と拒否時の動作を確認してください。仕様への適合検査だけで、業務上の認可や副作用の正しさまでは証明できません。

## 参考資料

| 資料 | 提供元 | 状態 | 確認する箇所 |
|---|---|---|---|
| [MCP 2026-07-28 Tools 仕様](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) | Official（MCP） | —（仕様） | Tool 定義、結果、エラー、セキュリティ要件。 |
| [MCP ToolAnnotations](https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations) | Official（MCP） | —（仕様） | 副作用・再試行の注釈と、信頼の限界。 |
| [MCP Inspector](https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector) | Official（MCP） | —（状態の明記なし） | 接続方法と手動の Tool 呼び出し。 |
| [TypeScript SDK v2: Tools](https://ts.sdk.modelcontextprotocol.io/v2/servers/tools.html) | Official（MCP） | GA | `registerTool` と入出力スキーマを実装する際の例。 |
