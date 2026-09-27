# エージェントの記憶基盤 — GBrain・Mem0・Graphiti・Letta を比べる

> **対象ツール**: ツール横断（Claude Code・Codex・GitHub Copilot ほか MCP クライアント） ｜ **実行環境**: CLI / Cloud ｜ **対象読者**: エンジニア・プラットフォーム担当 ｜ **最終更新**: 2026-09-27

> AI エージェントの「外部記憶」をうたう OSS・製品は増えていますが、同じ種類のものではありません。事実を貯める**記憶層**、時間とともに変わる事実を追う**時系列ナレッジグラフ**、記憶を持つ**エージェントの実行基盤**、文書を検索して渡す **RAG アプリ**が混ざっています。このページは、GBrain・Mem0・Graphiti / Zep・Letta と、境界確認のための AnythingLLM・Open WebUI を、一次情報（各 README と公式ドキュメント、**2026-09-27 確認**）に基づいて横並びにし、「複数のエージェントから使うローカルの共通知識基盤として何を選ぶか」を判断する材料をまとめます。GBrain 自体の設計と、オントロジー・ナレッジグラフとの関係は [オントロジー](ontology.md#形式的な定義を作らない選択肢--gbrain) を参照してください。

---

## 1. 最初に分ける — 4 つのカテゴリ

候補を並べる前に、何を中心に作られたものかで分けます。比較表の数字や機能名より、この分類のほうが選定を左右します。

| カテゴリ | 中心にあるもの | 該当 | エージェントとの関係 |
|---------|---------------|------|--------------------|
| **記憶層（Memory Layer）** | 事実・好み・決定事項を保存し、検索して返す | GBrain、Mem0 | 既存のエージェントに**外付け**する。MCP や SDK で読み書きさせる |
| **時系列ナレッジグラフ** | 実体・関係・事実と、その**有効期間**を持つグラフ | Graphiti（OSS）/ Zep（マネージド） | 外付けする。ただし保存時に LLM が抽出・重複判定を行う |
| **記憶を持つ実行基盤（Agent Runtime）** | 記憶・スキル・system prompt を自ら書き換えるエージェント本体 | Letta（Letta Code / Letta Harness） | **エージェントそのもの**を置き換える。記憶はその内部にある |
| **RAG 中心のチャットアプリ** | 文書を取り込み、検索してチャットへ渡す | AnythingLLM、Open WebUI | 人が使うチャット画面。MCP は**外部ツールを使う側**として対応する |

要点は 2 つです。

- **Letta は「記憶の部品」ではありません。** 旧来の Letta（MemGPT）API server は `letta-ai/letta` の archive ブランチへ移され、現在の本体は、記憶を持つエージェント実行基盤の [Letta Code](https://github.com/letta-ai/letta-code)（ドキュメント上は Letta Harness）です。Claude Code や Codex に記憶を足す用途とは前提が違います。
- **AnythingLLM と Open WebUI は、他のエージェントへ記憶を提供する側ではありません。** どちらも MCP サーバーを**呼び出す**機能を持ち、ユーザーごとの memory 機能もありますが、Claude Code や Codex から共通の記憶として読み書きする MCP サーバーを公開する製品としては説明されていません。RAG の文書検索と、エージェントの記憶は別カテゴリとして扱います。

---

## 2. 比較表 — 設計

| 観点 | GBrain | Mem0 | Graphiti / Zep | Letta Code | AnythingLLM / Open WebUI |
|------|--------|------|----------------|------------|--------------------------|
| **主用途** | エージェント向けの知識・記憶層。出典つきで事実を保存し、訂正・撤回できる | 会話・ユーザー・エージェントの記憶層（User / Session / Agent の多層） | 時系列の context graph。事実がいつ真で、いつ置き換わったかを追う | 記憶・identity を持ち、長期に学習する stateful agent の実行基盤 | 文書中心の RAG チャット。memory は利用者ごとの補助機能 |
| **データモデル** | git 管理の **Markdown が正**。PGLite（既定）または Postgres + pgvector へ索引。型付きの関係グラフ | ベクトルストア（OSS 既定は Qdrant、self-hosted server は Postgres + pgvector）と履歴 DB。entity linking | グラフ DB（Neo4j / FalkorDB / Amazon Neptune。Kuzu は非推奨）。entity・fact（有効期間つき）・episode（出典） | MemFS（memory block を含む文脈を git で追跡）。Cloud または local backend に状態を保存 | 各アプリの DB（SQLite / PostgreSQL 等）とベクトル DB |
| **記憶の更新** | 明示的な書き込みが基本。信頼されたローカル書き込みは参照を**LLM なしで**パターン抽出して関係を張る | 会話を渡すと **LLM が事実を抽出**。2026-04 の新アルゴリズムは ADD のみで上書き・削除をしない | episode を取り込むたびに **LLM が entity 抽出・重複判定・要約**。古い事実は削除せず無効化 | エージェント自身が memory・skill・prompt を書き換える。定期的な「dreaming」で整理 | 手動登録と、有効化した場合の自動抽出。既定はオフ（AnythingLLM） |
| **検索** | keyword（keyless でも可）→ vector + keyword の hybrid + reranker。`think` は引用つき統合回答と「まだ分かっていないこと」を返す | semantic・BM25 keyword・entity matching の並列 + 融合。時間を考慮した検索 | semantic + BM25 keyword + graph traversal の hybrid。時点を指定した問い合わせ | メッセージ検索（`/search`）と、エージェントが自分の memory を読む | ベクトル検索（Open WebUI は BM25 との hybrid にも対応） |
| **LLM への依存** | 保存と keyword 検索は LLM 不要。embedding・rerank・synthesis・enrichment を設定すると外部へテキストが送られる | 保存（抽出）に LLM が必要。既定は OpenAI | 保存時に複数回の LLM 呼び出しが必要。structured output に対応したモデルを推奨 | エージェント本体が LLM で動く | 回答生成に LLM が必要。ローカル LLM も選べる |

> **ベンチマークの数値はそのまま比べないでください。** Mem0 は LoCoMo / LongMemEval の改善を公表していますが、README は「マネージド版の独自最適化を含み、OSS 版では同一の数値にならない」と明記しています。GBrain の BrainBench も、特定のコーパスでの結果だと README が断っています。測定条件が違う数値を横に並べて優劣を決めず、自分のデータで試します（[Skill / エージェントの評価](evals.md)）。

---

## 3. 比較表 — 運用

| 観点 | GBrain | Mem0 | Graphiti / Zep | Letta Code | AnythingLLM / Open WebUI |
|------|--------|------|----------------|------------|--------------------------|
| **MCP** | **MCP サーバー**。stdio（`gbrain serve`）と HTTP（`gbrain serve --http`、OAuth 2.1 と scope） | **公式 MCP サーバーは Platform のホスト型**（`https://mcp.mem0.ai/mcp`）。記憶は Mem0 のアカウント側に保存される | Graphiti の **MCP サーバー**（HTTP が既定、stdio も可）。Docker + Neo4j / FalkorDB で動かす | Agent SDK から MCP サーバーへ**接続する側**。Letta Cloud には、他の MCP クライアントから Letta エージェントを作成・呼び出す hosted MCP server がある | MCP サーバーを**使う側**（AnythingLLM は設定ファイル、Open WebUI は Streamable HTTP） |
| **完全ローカル** | 可能。`gbrain init --pglite --no-embedding` で keyless・サーバーなし | OSS ライブラリ / self-hosted server は可能（Ollama 等のローカル LLM を設定）。既定は OpenAI | 可能（ローカル LLM は OpenAI 互換 endpoint 経由）。小さなモデルでは抽出に失敗しやすいと README が注意 | 可能。local backend では状態が端末内に留まり、アカウント不要。**既定は Letta Cloud** | 可能（ローカル LLM・ローカルのベクトル DB） |
| **主なコスト** | keyless なら API 費用なし。embedding / rerank / 常時稼働の enrichment を有効にすると API とサーバー費用 | 書き込みごとの LLM 抽出 + embedding。Platform の料金は公式の料金ページで確認 | 取り込みごとに複数回の LLM 呼び出し + グラフ DB の運用。Zep の料金は公式の料金ページで確認 | エージェント実行そのものの LLM 費用。Cloud 機能はアカウントが必要 | 回答生成の LLM と、取り込み時の embedding |
| **マルチユーザー** | 個人が既定。Postgres と HTTP サーバーで共有ブレインを構成できる（company brain のチュートリアルあり） | `user_id` / `agent_id` 等で記憶を分ける。Platform は organization / project | Graphiti は `group_id` で分ける。ユーザー・スレッド管理は Zep 側の機能 | personal agent と、組織で共有する agent teammate（Cloud） | どちらもマルチユーザー対応（AnythingLLM は Docker 版のみ） |
| **権限管理** | HTTP サーバーで OAuth client ごとに `read` / `write` / `admin` / `agent` の scope。ただしローカルファイルや共有 DB の認証情報は**別の信頼境界**で、source 設定だけでは分離されないと README が明記 | self-hosted server はユーザーごとの API key と request audit log。Platform は organization / project のメンバーと role | Graphiti は自前で実装する（README は Zep 側にガバナンスとセキュリティ保証を置く） | tool 実行の permission mode と承認。組織の権限は Enterprise 機能 | Open WebUI は RBAC・グループ・LDAP / SSO / SCIM。AnythingLLM は Docker 版の multi-user 権限 |
| **運用負荷** | PGLite なら小さい。大規模・共有は Postgres、常時稼働の enrichment は 8GB 以上のサーバー | ライブラリは小さい。self-hosted server は Docker スタック | グラフ DB の構築・バックアップ、LLM の同時実行数（`SEMAPHORE_LIMIT`）の調整 | CLI / デスクトップは小さい。常時稼働は App Server を別に運用 | Docker 1 つから始められる |
| **ライセンス** | MIT | Apache-2.0（Platform は商用サービス） | Apache-2.0（Zep は商用サービス） | Apache-2.0（Letta Cloud は商用サービス） | AnythingLLM: MIT ／ Open WebUI: 独自の Open WebUI License（ブランド表示の維持が条件） |
| **提供元 / 状態** | Community / Experimental | Community（Mem0 社） / GA | Community（Zep 社） / Experimental（`graphiti-core` 0.30 系） | Community（Letta 社） / Experimental（`@letta-ai/letta-code` 0.33 系） | Community / GA |

> 表の値は 2026-09-27 時点の README と公式ドキュメントに基づきます。どの候補も更新が速く、既定の保存先・MCP の提供形態・ライセンスが変わることがあります。導入時に各リポジトリを再確認してください。

---

## 4. 得意な用途と弱点

| 候補 | 向いている用途 | 弱点・注意点 |
|------|---------------|-------------|
| **GBrain** | 個人やチームの知識を Markdown で持ち、複数のコーディングエージェントから同じ事実を引く。出典と「分かっていないこと」を明示させたい | 開発が非常に速く、手順が頻繁に変わる。HTTP 経由の書き込みでは関係の抽出が即時に行われない。Markdown export は DB の完全なバックアップではない（DB のみのページや履歴は別途バックアップが必要） |
| **Mem0** | チャットボットやアシスタントで、利用者ごとの好み・履歴を覚えさせる。SDK から数行で組み込みたい | 書き込みごとに LLM を呼ぶ。新アルゴリズムは上書きしないため、古い事実が残り続ける（検索時の時間考慮に依存する）。コーディングエージェント向けの公式 MCP はホスト型 |
| **Graphiti / Zep** | 状態が変わるデータ（顧客の契約、担当者の異動など）で「いま何が真か」「以前は何だったか」を問う。事実から出典の episode をたどりたい | 取り込みの LLM 費用とグラフ DB の運用が重い。抽出品質がモデルに左右される。ガバナンス・スケール・管理画面はマネージドの Zep 側の機能 |
| **Letta Code** | 記憶を持って長期に学習する常駐エージェントを、別の実行基盤として立てる。Slack 等から同じエージェントに話しかける | 既存の Claude Code / Codex に記憶を足す用途ではない。既定の保存先は Letta Cloud で、ローカルに留めるには local backend を明示する。旧 API server から移行が必要 |
| **AnythingLLM / Open WebUI** | 社内文書をローカルで検索させるチャット環境を、複数の利用者に提供する | 他のエージェントの記憶基盤にはならない。記憶機能は利用者ごとで、件数上限もある（AnythingLLM は workspace あたり 20 件など） |

---

## 5. Claude Code・Codex・Copilot から共通の記憶として使えるか

「どのエージェントからも同じ事実を読み書きしたい」という用途では、**自分で動かせる MCP サーバーを持つか**が最初の分かれ目です。

| 候補 | 複数のエージェントから使う方法 | 確認すること |
|------|------------------------------|-------------|
| GBrain | ローカルは stdio（`claude mcp add gbrain -- gbrain serve` など）。複数の端末からは `gbrain serve --http` と OAuth の scope つき token。Claude Code / Codex には Plugin も用意されている | エージェントごとに scope を分ける。`--surface verbs` で公開する tool を 7 つの記憶操作に絞れる |
| Mem0 | 公式の hosted MCP サーバーに各クライアントを接続する | 記憶が Mem0 のアカウント（クラウド）に保存されることを許容できるか |
| Graphiti | Graphiti MCP サーバーを HTTP または stdio で起動し、各クライアントを接続する | `group_id` をどう分けるか。取り込みの LLM 費用 |
| Letta Code | 記憶は Letta のエージェント内部にある。他のエージェントからは hosted MCP server（Letta Cloud）でエージェントへ話しかける形 | 「記憶を共有する」のではなく「記憶を持つ別のエージェントに頼む」構成になる |
| AnythingLLM / Open WebUI | 対象外（MCP は使う側） | — |

どの方式でも、MCP サーバーとして接続したエージェントは記憶を**書き換えられます**。誤った事実や、プロンプトインジェクションで書き込まれた内容が、別のエージェントの判断に使われる可能性があります。書き込みを許すエージェントと読み取りだけのエージェントを分け、書き込みの出典を残してください（[Skill / Plugin のセキュリティ](skill-security.md#学習した-memory-を-policy-とみなさない)）。

---

## 6. ローカルに置くメリットとデメリット

| | 内容 |
|---|------|
| **メリット** | 記憶の本文が自分の管理下に留まる。ベンダーのサービス終了や方針変更の影響を受けにくい。API 費用を抑えられる（GBrain の keyless 構成など） |
| **デメリット** | バックアップ・更新・障害対応を自分で行う。複数端末から使うには HTTP 公開と認証が必要になる。ローカル LLM では抽出品質が下がることがある（Graphiti は README で注意している） |
| **見落としやすい点** | 「ローカルに置いた」だけでは外部送信がなくなるとは限らない。embedding・rerank・抽出・要約にクラウドのモデルを設定すれば、そこへテキストが送られる。GBrain の README も、keyless でも**エージェントのモデルには想起した記憶が渡る**と明記している |

完全にローカルで閉じたい場合は、保存先だけでなく、**埋め込み・抽出・回答生成のモデルの接続先**と、エージェント本体のモデルの接続先まで確認します。

---

## 7. 用途別の選び方

| やりたいこと | 第一候補 | 理由 |
|-------------|---------|------|
| Claude Code・Codex など複数のコーディングエージェントに、ローカルで共通の記憶を持たせたい | **GBrain** | keyless・サーバーなしで始められ、stdio / HTTP の MCP サーバーと scope つきの共有に対応する。Markdown が正なので中身を人が読める |
| 自社のチャットボットやアプリに、利用者ごとの記憶を SDK で組み込みたい | **Mem0** | User / Session / Agent の記憶を API で扱える。OSS から始めて Platform へ移行できる |
| 時間とともに変わる事実を、履歴つきで問い合わせたい | **Graphiti**（運用を任せるなら **Zep**） | 事実ごとに有効期間を持ち、古い事実を削除せず無効化する |
| 記憶を持ち、自分で学習し続ける常駐エージェントを立てたい | **Letta Code** | 記憶・スキル・prompt の書き換えまで含めた実行基盤 |
| 社内文書をローカルで検索できるチャット環境を、チームに配りたい | **AnythingLLM** / **Open WebUI** | 記憶基盤ではなく RAG アプリとして選ぶ |
| 語彙・規則を全社で定義し、権限つきでエージェントに渡したい | この比較の外 | [オントロジー](ontology.md)の AWS Context Ontology Accelerator や Palantir Foundry Ontology が対象 |

迷う場合は、**書き込みに LLM が要るか**（費用と誤抽出のリスク）と、**記憶の正本がどこにあるか**（Markdown / DB / クラウド）の 2 点から絞ると判断しやすくなります。

---

## 8. 導入前に確認すること

- [ ] 記憶の正本はどこか。バックアップはその正本を含むか（Markdown export だけでは不十分な場合がある）
- [ ] 書き込み・検索・要約のそれぞれで、どのモデルにテキストが送られるか
- [ ] 書き込みを許すエージェントと、読み取りだけのエージェントを分けられるか
- [ ] 誤った記憶を訂正・削除する手順があるか。削除が物理削除か無効化か
- [ ] 複数人で共有する場合、認証のない経路（ローカルファイル、共有 DB の認証情報）から他人の記憶を読めないか
- [ ] 同名の別パッケージを入れていないか（GBrain は npm 上の同名パッケージと無関係。[Skill / Plugin のセキュリティ](skill-security.md#6-同名の別パッケージという入口)）
- [ ] テレメトリの送信有無と無効化の方法（Graphiti・AnythingLLM は README に opt-out 方法を記載）

---

## 関連ドキュメント

- [オントロジー](ontology.md) — GBrain の設計と、形式的な語彙定義（オントロジー / ナレッジグラフ / RAG / GraphRAG）との切り分け
- [AI エージェントの実行基盤（ハーネス）](harness.md) — 記憶を「どこで動くエージェントに」渡すかという実行環境の層
- [ループエンジニアリング](loop-engineering.md) — ループの外部状態として記憶を使う設計
- [長時間タスクの信頼性設計](agent-reliability.md#学習する-memory-を-checkpoint-と混同しない) — 学習する memory と checkpoint の違い
- [Skill / Plugin のセキュリティ](skill-security.md) — エージェントに書き込ませる範囲と、同名パッケージへの注意
- [MCP と A2A — 役割の違いと併用方法](agent-protocols.md) — 記憶基盤を MCP で公開するときのプロトコル上の位置づけ

## 参考リンク

- [garrytan/gbrain](https://github.com/garrytan/gbrain) — README：keyless 構成、PGLite / Postgres、MCP（stdio / HTTP・OAuth scope）、共有時の信頼境界（MIT、2026-09-27 確認）
- [mem0ai/mem0](https://github.com/mem0ai/mem0) — README：Library / Self-Hosted / Cloud、2026-04 の新アルゴリズムとベンチマークの前提（Apache-2.0）
- [Mem0 Open Source overview](https://docs.mem0.ai/open-source/overview) ／ [Mem0 MCP](https://docs.mem0.ai/platform/mem0-mcp) — OSS の既定構成と、ホスト型 MCP サーバー（Mem0 公式ドキュメント）
- [getzep/graphiti](https://github.com/getzep/graphiti) — README：context graph、Zep との違い、対応グラフ DB、ローカル LLM、テレメトリ（Apache-2.0）
- [Graphiti MCP server](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md) — HTTP / stdio、`group_id`（Zep 公式）
- [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) — Graphiti / Zep の設計論文（arXiv:2501.13956）
- [letta-ai/letta-code](https://github.com/letta-ai/letta-code) ／ [letta-ai/letta](https://github.com/letta-ai/letta) — 現行の Letta Code と、旧 API server の archive 移行（Apache-2.0）
- [Letta documentation](https://docs.letta.com) — MemFS、local backend と self-hosting、hosted MCP server（Letta 公式）
- [Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) ／ [MCP Compatibility](https://docs.anythingllm.com/mcp-compatibility/overview) ／ [Memories](https://docs.anythingllm.com/features/memories) — MCP クライアントとしての対応と memory の範囲（MIT）
- [open-webui/open-webui](https://github.com/open-webui/open-webui) ／ [MCP support](https://docs.openwebui.com/features/extensibility/mcp) — RBAC、ローカル RAG、MCP（Streamable HTTP）クライアント（Open WebUI License）
