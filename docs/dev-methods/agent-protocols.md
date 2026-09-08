# MCP と A2A — 役割の違いと併用方法

> **対象ツール**: ツール横断（Claude Code・Codex・GitHub Copilot ほか） ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-08

> [Skills 最新動向 13 節](../trends.md#エージェント間プロトコルの統治の集約--a2a-が-aaif-に合流)は、MCP と A2A が同じ Agentic AI Foundation（AAIF）の下に並んだという**統治の変化**を扱っています。このページはその前提となる**両プロトコルの責務の違いと、併用する際の構成**を独立して整理します。

---

## 1. MCP と A2A を 30 秒で見分ける表

| | MCP | A2A |
|---|-----|-----|
| つなぐもの | エージェントと**ツール・データソース** | エージェントと**エージェント** |
| 単位 | Tool・Resource・Prompt | Task・Message・Artifact |
| 相手の内部構造 | サーバーが公開するスキーマを呼ぶ | 相手の内部状態を知らずに発見・委譲・協働する |
| 発見の起点 | クライアントがサーバーに接続し、tool 一覧を取得する | クライアントが **Agent Card**（メタデータ）を取得する |
| 最新の安定版 | 2026-07-28 版仕様 | v1.0.1（2026-05-28） |

**「A2A が登場したので MCP を置き換える」わけではありません。** 別の層の問題を解いています。AAIF 自身も両者を次のように整理しています（[13 節](../trends.md#エージェント間プロトコルの統治の集約--a2a-が-aaif-に合流)より）。

| プロトコル | 担う層 |
|-----------|-------|
| MCP | **エージェントとツール**の接続 |
| A2A | **エージェントとエージェント**の連携 |

---

## 2. MCP — tool / resource / prompt と認証の位置づけ

[MCP（2026-07-28 版仕様）](https://modelcontextprotocol.io/specification/)は、サーバーが次の 3 種類を公開する構成です。

- **Tools** — モデルが実行できる関数
- **Resources** — ユーザーやモデルが使うコンテキスト・データ
- **Prompts** — テンプレート化された会話・ワークフロー

同版では、双方向ステートフルなハンドシェイク（`initialize` / `initialized` 交換と `Mcp-Session-Id`）を廃止し、**各リクエストが自己完結する**ステートレスなコアへ転換しました。認可面では、認可サーバーが `iss` パラメータを返すことをクライアントに検証させる（RFC 9207 準拠）など、OAuth / OIDC の強化が図られています。

MCP の認証・認可は「**クライアントとサーバー間**」、つまりエージェントとツールの間の話です。エージェント同士の認証・委任は、次に説明する A2A 側の関心事です。

**→ MCP のツール呼び出しをどの局面で選ぶかは [エージェントに外部操作を与える手段の選び方](tool-selection.md) を参照**

---

## 3. A2A — Agent Card / Task / Message / Artifact / streaming

[A2A（Agent2Agent、v1.0.1 仕様）](https://a2a-protocol.org/latest/specification/)は、次の要素でエージェント間連携を定義します。

| 要素 | 役割 |
|------|------|
| **Agent Card** | エージェントが公開するメタデータ。アイデンティティ、能力、スキル、エンドポイント、認証要件を記述し、クライアントが機能を動的に発見できるようにする |
| **Task** | A2A が管理する作業の基本単位。一意な ID を持ち、`SUBMITTED` / `WORKING` / `COMPLETED` などのライフサイクルを持つ。複数ターンの相互作用に対応する |
| **Message** | クライアントとエージェント間の通信単位。`user` / `agent` の role を持ち、複数の Part を含む。タスクの起動、追加入力の要求、状態通知に使う |
| **Artifact** | タスク実行の成果物（文書・画像・構造化データなど）。複数の Part で構成される |
| **streaming** | Task に対するリアルタイムの差分更新。Send Streaming Message・Subscribe to Task で配信する |

認証・認可は仕様の第 7 章で定義されており、サーバー側の身元検証・クライアント認証は「標準的な Web セキュリティの実践」に委ねられ、サーバーは「クライアントが認可された Task にしかアクセスできない」ことを保証すべきとされています。Task 処理中に追加の認可が必要になる場面（In-Task Authorization）も別途定義されています。

A2A はもともと Google が開発し、2025-06-23 に Open Source Summit North America で Linux Foundation へ寄贈されオープンな A2A Project になりました。2026-08-17 に、その A2A Project が MCP・goose・AGENTS.md と同じ AAIF の hosted project として合流した、というのが [13 節](../trends.md#エージェント間プロトコルの統治の集約--a2a-が-aaif-に合流)で扱っている変化です。

---

## 4. 構成例

**単一エージェントが MCP でツールに繋ぐ構成**（多くの場合これで足ります）

```
利用者 → Agent A → MCP tool（外部サービス・データソース）
```

**A2A で別のエージェントへ委譲し、その先で MCP を使う構成**

```
利用者 → Agent A --A2A--> Agent B → MCP tool（Agent B が持つ専門ツール）
```

Agent A は Agent B の内部実装（どの MCP サーバーを使っているか、どのモデルで動いているか）を知る必要がありません。**Agent B が何をできるかは Agent Card から発見し、実際の作業は Task としてやり取りします。** これが「エージェントとツール」（MCP）と「エージェントとエージェント」（A2A）の層が違うことの具体的な意味です。

---

## 5. Agent Plugins・Catalog・ハーネスとの境界

| 仕組み | 扱う対象 |
|--------|---------|
| MCP | エージェント **1 体**からツール・データソースへの接続 |
| A2A | エージェント **同士**の発見・委譲・協働 |
| Agent Plugins | Agent Skills と MCP サーバーを**1 つの配布単位にまとめる**パッケージ形式（[8 節](../trends.md#8-agent-plugins-100--マルチベンダー共通のエージェント設定標準)） |
| Catalog / Agent Finder・ARD | Skill・MCP サーバー・**A2A エージェント**などを実行時に**発見する**registry（[7-2 節](../trends.md#7-2-agent-finder--ard--必要な時に見つける)） |
| ハーネス | 認証・スコープ・権限・スケジュール・監査を引き受ける実行基盤（[AI エージェントの実行基盤](harness.md)） |

Catalog は「A2A エージェントも参照先に含められる」という発見の仕組みであり、A2A そのものの通信規約ではありません。ハーネスは MCP・A2A のどちらの呼び出しも、その上位で認証・権限・監査の対象として扱います。

---

## 6. 導入判断 — 単体で足りる場合、A2A が必要な場合

| 状況 | 判断 |
|------|------|
| 1 体のエージェントが複数のツール・データソースを呼び分けるだけで完結する | **MCP だけで足ります。** A2A を導入する理由がありません |
| 別チーム・別ベンダーが持つエージェントの機能を、実装を知らずに呼び出したい | A2A が候補になります |
| 単一プロセス内でサブエージェントに作業を分けたい（実装は自分たちで持つ） | まず、単一エージェント内のサブエージェント委任で足りないかを確認します。A2A が要るのは、実装を自分たちで持たない・別ベンダーのエージェントと連携する場合です |
| すでに MCP で構造化された連携ができている | それを A2A に置き換える理由はありません。A2A は MCP の代替ではなく、**エージェント間**という別の層に対する解です |

**多くの読者にとって、現時点では「A2A は不要」が答えです。** 導入するのは、自分たちが管理しないエージェントと連携する必要が具体的に生じたときで十分です。

---

## 7. 未解決事項

A2A・MCP の仕様が定義するのは「通信の規約」までです。次の論点は、仕様が保証する範囲の外にあり、実装者が個別に設計する必要があります。

- **agent identity** — Agent Card が名乗る「私」を、実際にどう検証するか
- **委任権限** — Agent A が Agent B に何を任せてよいか、Agent B の権限は Agent A よりどれだけ狭めるべきか
- **信頼** — 未知の Agent Card をどこまで信用してタスクを渡すか
- **監査** — エージェント間で委譲されたタスクを、誰が・いつ・何を指示したところまで追跡できるか
- **バージョン互換性** — A2A・MCP それぞれの仕様が今後も変わり続ける前提で、どう追従するか

これらは [Skill / Plugin のセキュリティ](skill-security.md)が扱う「導入前に何を確認するか」と地続きの論点です。**エージェント自身の ID・認可・委任権限の詳細は [AIエージェントのID・認可・委任権限](agent-identity.md) に集約しています。**

---

## 対象外

- A2A SDK の全 API・全言語実装の転載
- ベンダー別の対応数・参加組織数のランキング
- サンプルエージェントの実装チュートリアル
- MCP ロードマップ（[13 節](../trends.md#次に来るもの--2026-08-22-のロードマップ)の重点領域）を確定仕様として記載すること

## 関連ドキュメント

- [Skills 最新動向「MCP の次期仕様」「A2A が AAIF に合流」](../trends.md#13-mcp-の次期仕様) — 確定仕様とロードマップ、統治の変化
- [エージェントに外部操作を与える手段の選び方](tool-selection.md) — MCP をいつ選ぶか、承認境界の考え方
- [AI エージェントの実行基盤（ハーネス）](harness.md) — MCP・A2A の呼び出しを認証・権限・監査の対象として管理する層
- [Skill / Plugin のセキュリティ](skill-security.md) — 導入前の確認手順

## 参考リンク

- [MCP Specification（2026-07-28）](https://modelcontextprotocol.io/specification/) — Model Context Protocol 公式仕様
- [MCP 2026-07-28 リリースノート](https://blog.modelcontextprotocol.io/posts/2026-07-28/) — stateless core・認可強化・Apps/Tasks 拡張の変更点
- [A2A Specification（v1.0.1）](https://a2a-protocol.org/latest/specification/) — Agent2Agent Protocol 公式仕様
- [A2A Releases](https://github.com/a2aproject/A2A/releases) — バージョン履歴
- [Google Cloud donates A2A to the Linux Foundation](https://developers.googleblog.com/google-cloud-donates-a2a-to-linux-foundation/) — A2A の Linux Foundation への寄贈（2025-06-23）
