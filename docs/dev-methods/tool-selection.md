# エージェントに外部操作を与える手段の選び方 — API・connector・MCP・CLI・Computer Use

> **対象ツール**: ツール横断（Claude Code・Codex・GitHub Copilot ほか） ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-08

> [Skills 最新動向「Computer Use / Browser Use」](../trends.md#6-computer-use--browser-use)は「専用 Plugin・コネクタ・MCP がある場合は構造化された連携を優先する」と述べています。このページはその判断基準を独立させ、**API・connector・MCP・CLI・Computer Use をどの順で検討し、どこで承認を挟むか**を整理します。Computer Use そのものの機能解説は [trends.md 6 節](../trends.md#6-computer-use--browser-use)を参照してください。

---

## 1. 30 秒で選ぶ

| 状況 | 最初に検討する方式 |
|------|-------------------|
| 型付きの入出力・冪等性・監査ログが必要 | **構造化 API** |
| サードパーティ SaaS に薄く繋ぎたい、自前で認証を実装したくない | **connector / app** |
| エージェントに「何ができるか」を動的に発見させたい | **MCP** |
| ローカルのファイル操作・スクリプト実行で完結する | **CLI** |
| 上記のいずれも対象サービスに存在せず、画面を見て判断・操作する必要がある | **Computer Use**（最後の手段） |

**原則は「最も構造化された、利用可能な手段を優先する」ことです。** 下に行くほど、エージェントに渡す権限の範囲が広がり、失敗したときの検証コストも上がります。

---

## 2. 構造化 API — 型・エラー・冪等性・監査

対象サービスが REST / GraphQL 等の API を公開している場合、原則としてこれが第一候補です。

| 観点 | 何が効くか |
|------|-----------|
| 型 | リクエスト・レスポンスのスキーマが決まっており、パース失敗が構造化されたエラーとして返る |
| エラー | 「画面のエラーダイアログを読み取って解釈する」作業が要らない。ステータスコード・エラーコードで判定できる |
| 冪等性 | 同じリクエストを安全に再送できるか（`Idempotency-Key` 等）が、リトライ設計に直結する |
| 監査 | リクエスト・レスポンスのログがそのまま監査証跡になる。「何を送り、何が返ったか」が後から機械的に追える |

---

## 3. connector / app — 認証と提供範囲を委ねる

コネクタ（Claude の Connectors、ChatGPT の Apps SDK 連携、GitHub Copilot の各種統合等）は、OAuth などの認証と、API の呼び出し範囲（スコープ）をベンダー側の実装に委ねる方式です。自前で API 統合を実装するコストは下がりますが、**コネクタが公開している機能の範囲でしかエージェントは操作できません**。独自の業務ロジックが必要な場合は、下層の API を直接呼ぶ方が柔軟です。

---

## 4. MCP — エージェント向け discovery と tool schema

[MCP（Model Context Protocol）](https://modelcontextprotocol.io/specification/)は、LLM アプリケーションと外部ツール・データソースを標準化された方法でつなぐオープンプロトコルです（2026-07-28 版仕様）。サーバーは **Resources**（コンテキスト・データ）・**Prompts**（テンプレート化された会話）・**Tools**（モデルが実行できる関数）の 3 種類を公開し、クライアントは JSON-RPC 2.0 でこれを呼び出します。

connector との違いは、**「何ができるか」をエージェントが実行時に discovery できる**点です。connector は導入時に決まった機能だけを提供しますが、MCP サーバーはツール一覧とスキーマをその場で返します。

仕様自身が明記するセキュリティ原則は次のとおりです。

> Hosts must obtain explicit user consent before invoking any tool. Users should understand what each tool does before authorizing its use.

> \[Tool] descriptions of tool behavior such as annotations should be considered **untrusted**, unless obtained from a trusted server.

**ツールの説明文（annotation）自体を無条件に信用しない**、という点は、後述する「外部コンテンツを命令として扱わない」設計と直結します。

---

## 5. CLI — ローカル処理とスクリプト化

対象がネットワーク越しのサービスではなく、ローカルのファイル操作・ビルド・テスト実行である場合は CLI が最も直接的です。API 呼び出しのようなラウンドトリップも、Computer Use のような画面認識も要りません。ハーネスがどうツール呼び出しを管理するかは [AI エージェントの実行基盤（ハーネス）](harness.md)を参照してください。

---

## 6. Computer Use — API のない GUI と最終画面確認

Computer Use は、**専用の API・connector・MCP サーバーが存在しないサービスに対する最後の手段**です。OpenAI の公式ドキュメントも、対象アプリが専用 Plugin または MCP サーバーを公開している場合は「その構造化統合を優先する」と明記し、Computer Use は「コマンドラインツールや構造化統合では十分でない」タスク（ビジュアル検証、GUI 操作が本質的に必要な作業、アプリ横断のワークフロー）に絞るべきだとしています。

Google も 2026-06-24 に Gemini 3.5 Flash の Computer Use を発表し、ブラウザ・モバイル・デスクトップを横断して操作できるとしています。同発表は、これが関数呼び出しや組み込みツールに**代わる**ものではなく、それらを**補完する**ものだと位置づけています。

いずれのベンダーも「構造化された手段が使えるなら、そちらを優先する」という原則は共通しています。Computer Use 固有の機能・OS ごとの権限・Browser Use との違いは [trends.md 6 節](../trends.md#6-computer-use--browser-use)にまとめています。

---

## 7. fallback の順序と昇格条件

上から順に「使えるか」を確認し、使えない場合だけ次の手段へ落とします。

```
構造化 API → connector / app → MCP → CLI → Computer Use
```

**下の手段へ落ちるほど、エージェントに与える権限は広がります。** 読み取り専用の API しか使っていなかったタスクが、途中で「その操作は API にないので Computer Use で画面から行う」に切り替わる場合、これは**権限の昇格**です。昇格が起きた時点で、開始時点の承認をそのまま流用せず、**再承認を挟む**運用にしてください。この考え方は [ループエンジニアリング](loop-engineering.md)が扱う「無人で回すループの停止条件」とも重なります — 権限が変わる境界は、機械的に判定できる停止・確認ポイントとして設計するのが安全です。

---

## 8. 承認境界 — 読み取り／入力／送信／購入／削除で分ける

同じ「ツール呼び出し」でも、結果の重大さは操作によって大きく違います。承認を求めるタイミングは、操作の結果でグラデーションを付けてください。

| 操作の種類 | 典型例 | 承認の目安 |
|-----------|-------|-----------|
| 読み取り | ファイル閲覧、検索、画面のスクリーンショット | 事前承認は不要な場合が多い（範囲の限定は必要） |
| 入力 | フォームへの下書き入力、下書き保存 | 送信前であれば取り消し可能なことが多い |
| 送信・購入・削除 | メール送信、決済、リソース削除、外部への投稿 | **不可逆な操作**。実行前に必ず人の確認を挟む |

OpenAI のエージェント構築ガイドは、MCP ツールを使う場面について次のように述べています。

> Always enable tool approvals so end users can review and confirm every operation.

同ガイドはまた、外部から取得した信頼できない内容の扱いについて次の原則を挙げています。

> Pass untrusted inputs through user messages to limit their influence.

**エージェントが取得した外部コンテンツ（Web ページ、メール本文、Computer Use で読み取った画面の文字列など）は、常に「データ」として扱い、「エージェントへの指示」として実行してはいけません。** これは MCP の「ツールの説明文自体を信用しない」という原則（[4 節](#4-mcp--エージェント向け-discovery-と-tool-schema)）とも一致します。

**→ Skill・Plugin を導入する際の同種の判断は [Skill / Plugin のセキュリティ](skill-security.md)、コードを書かない方向けの確認事項は [生成AIを業務で安全に使う](../business/safety.md)を参照**

---

## 9. 方式ごとのテストと完了確認

「タスクが完了した」とエージェントが自己申告することと、実際に完了したことは別です。方式ごとに、機械的に確認できる完了の証跡を用意してください。

| 方式 | 完了確認の例 |
|------|-------------|
| 構造化 API | レスポンスのステータスコード・返却された ID |
| connector / app | コネクタが返す成功レスポンス、実行ログ |
| MCP | Tool の実行結果（構造化された戻り値） |
| CLI | 終了コード（exit code）、生成物の存在確認 |
| Computer Use | 最終画面のスクリーンショット、受領番号・確認メールなど画面外の証跡 |

不可逆な操作（[8 節](#8-承認境界--読み取り入力送信購入削除で分ける)）ほど、完了確認の証跡を残すことが重要になります。

---

## 対象外

- GUI 自動化ツールそのものの性能比較・ランキング
- CAPTCHA やアクセス制御の回避手法
- 各サービスの利用規約で禁止された自動操作
- サービスごとのログイン手順・資格情報の扱い（[生成AIを業務で安全に使う](../business/safety.md)を参照）

---

## 関連ドキュメント

- [Skills 最新動向「Computer Use / Browser Use」](../trends.md#6-computer-use--browser-use) — Computer Use / Browser Use 自体の機能解説
- [AI エージェントの実行基盤（ハーネス）](harness.md) — ツール呼び出しを管理する裏側の仕組み
- [ループエンジニアリング](loop-engineering.md) — 無人で回すループの停止条件・権限境界の設計
- [Skill / Plugin のセキュリティ](skill-security.md) — 導入前に何を確認するか
- [生成AIを業務で安全に使う](../business/safety.md) — コードを書かない方向けの確認事項

## 参考リンク

- [Computer Use](https://learn.chatgpt.com/docs/computer-use) — OpenAI 公式ドキュメント
- [Introducing computer use in Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/) — Google 公式発表（2026-06-24）
- [MCP Specification（2026-07-28）](https://modelcontextprotocol.io/specification/) — Model Context Protocol 公式仕様
- [Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety) — OpenAI 公式ガイド（信頼できない入力の扱い、ツール承認）
- [Summary Analysis of Responses to the RFI Regarding Security Considerations for AI Agents](https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai) — NIST（2026-05-18 公開）
