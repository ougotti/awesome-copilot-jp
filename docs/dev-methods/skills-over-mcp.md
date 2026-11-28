# MCP Skills 拡張 — Skill を MCP server から配る

> **対象ツール**: ツール横断（MCP server の開発者・MCP に対応したホスト） ｜ **実行環境**: CLI / IDE / Cloud / Chat UI ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-11-28

> [MCP Skills 拡張](https://modelcontextprotocol.io/extensions/skills/overview)（`io.modelcontextprotocol/skills`、[SEP-2640](https://modelcontextprotocol.io/seps/2640-skills-extension)）は、`SKILL.md` を含む Skill のディレクトリを、**ファイルとしてではなく MCP の Resources として**届ける公式の拡張です。MCP server が自分の tool の使い方を Skill として一緒に配れるようになります。このページでは、ファイルで配る Skill との違い、仕組み、対応状況、ホストに課された承認とセキュリティの要件を整理します。内容は 2026-11-28 に一次資料で確認したもので、実機・SDK での検証は行っていません。

---

## 1. 何が変わるのか

これまで Skill は、リポジトリの `.claude/skills/` や `.agents/skills/` などに**ファイルとして置き**、エージェントがそれを読む形が基本でした（配布の手段は [Skills 最新動向 7 節](../trends.md#7-skill-の発見配布更新)）。MCP Skills 拡張では、MCP server が Skill を Resources として公開し、対応ホスト（Claude Code・VS Code など）が**必要になった時点で server から読み出します**。

SEP-2640 は、この拡張が必要な理由を 3 つ挙げています。

| 課題 | 内容 |
|------|------|
| 配布が分かれる | MCP server と、その server の使い方を教える Skill が、別々にバージョン管理・導入される。registry から server を入れた人は、対応する Skill があることを知る手段がない |
| instructions に収まらない | server の `instructions`（`server/discover` の結果に入る説明文）は実質的に短いものしか載せられず、大きなワークフローを書けない |
| 独自実装がばらばら | 公式の取り決めがないまま、各実装が独自の `skill://` URI を作り、意味が食い違っていた |

### ほかの届け方との違い

| | ファイルの Skill | Plugin（Copilot / Claude Code / Codex） | MCP server の `instructions` | **MCP Skills 拡張** |
|---|---|---|---|---|
| 置き場所 | リポジトリ・ユーザーのディレクトリ | Marketplace から取得して手元に展開 | server の応答 | **MCP server**（手元には必要な分だけ取得） |
| 更新 | ファイルを差し替える | Plugin を更新する | server を更新すれば即時 | server を更新すれば即時。**Skill 単位で保存した承認は中身が変わると取り直す**（[4 節](#4-ホストに課された承認とセキュリティの要件)） |
| 大きさ | 制限は実装次第 | 制限は実装次第 | 短い説明に限られる | 1 Skill あたり 512 ファイル・16 MiB まで（[2 節](#上限)） |
| 実行コード | 同梱できる | 同梱できる（hooks・MCP 設定など） | なし | 同梱はできるが、**明示的な承認なしに手元で実行させてはならない** |
| 向く場面 | チーム内で中身を管理したい | 複数の Skill・Agent・MCP 設定をまとめて配る | 短い使い方の注意 | **server とその使い方を一緒に版管理したい** |

MCP Skills 拡張は Plugin の代わりではありません。Plugin は「手元の環境に何を入れるか」の単位で、MCP Skills 拡張は「接続した server から何を読ませるか」の取り決めです。Skill の書式（ディレクトリ構成・frontmatter・名前の規則・段階的な読み込み）は [Agent Skills 仕様](https://agentskills.io/specification)にそのまま委ねられており、**拡張が定めるのは届け方だけ**です。

---

## 2. 仕組み

### 提供元と状態

| 項目 | 内容 |
|------|------|
| 提供元 | Official（MCP プロジェクトの Skills Over MCP Working Group。リポジトリは [modelcontextprotocol/ext-skills](https://github.com/modelcontextprotocol/ext-skills)、Apache-2.0） |
| SEP の状態 | **Final**（Extensions Track、2026-04-23 作成、[PR #2640](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2640) は 2026-09-13 に merge） |
| 対象のプロトコル | base protocol `2026-07-28` 以降（[13 節](../trends.md#13-mcp-2026-07-28-仕様と移行時の確認)の stateless core が前提）。2026-10-15 に仕様の型と例を `2026-07-28` の schema に合わせる改訂が入った |
| 状態ラベル | 拡張自体は **Beta（Preview）**。SEP の採択と各製品の対応状況は個別に確認する。[拡張のリリース段階](https://github.com/modelcontextprotocol/ext-skills#specification) ／ [製品別の対応表](#3-対応状況) |

> 拡張の仕様は MCP 本体と別に版を重ねます。作業部会は[現行の仕様本文](https://github.com/modelcontextprotocol/ext-skills/blob/main/specification/beta/skills.mdx)を beta として公開しています。

### 対応の宣言

拡張は opt-in です。server は capabilities の `extensions` に `io.modelcontextprotocol/skills` を宣言し、クライアントはその宣言を確認してから拡張の method を呼びます。拡張に対応していないクライアントにとって、`skill://` の Resources は**ただの Resources**として見えるだけなので、既存の接続は壊れません。

宣言した server は Resources の capability も宣言する必要があります。設定項目は `directoryRead`（後述の `resources/directory/read` に対応するか、既定 `false`）の 1 つだけです。

### Skill の住所 — `skill://`

Skill の各ファイルが 1 つの Resource になり、次の形の URI で指されます（`skill://` 以外のスキームも使えますが、推奨は `skill://` です）。

```
skill://<Skill のパス>/<Skill 内のファイルパス>
```

| 例 | 意味 |
|----|------|
| `skill://git-workflow/SKILL.md` | 名前が `git-workflow` の Skill の本体 |
| `skill://pdf-processing/scripts/extract.py` | `pdf-processing` に同梱されたスクリプト |
| `skill://acme/billing/refunds/SKILL.md` | `acme/billing` という整理用の接頭辞の下にある、名前が `refunds` の Skill |

**パスの最後の部分は、`SKILL.md` の frontmatter の `name` と一致しなければなりません。** 接頭辞は server が自由に決められます（部署・製品・版など）。

### 3 つの method

| method | 必須 | 役割 |
|--------|------|------|
| `skills/list` | 必須 | server が配る Skill の一覧。各 Skill について、**frontmatter をそのまま**と、**全ファイルの URI・SHA-256 digest・バイト数**を返す。ページ送りあり |
| `skills/get` | 必須 | URI を指定して 1 つの Skill の情報を返す。一覧に載っていない Skill にも答える |
| `resources/directory/read` | 任意（`directoryRead: true` のとき） | ディレクトリの直下の一覧を返す。「`templates/` から合うものを選ぶ」といった指示に対応するため |

ファイルの中身そのものは、MCP 標準の `resources/read` で読みます。`skills/list` の 1 件は**要約ではなく完全な目録（manifest）**で、ホストは一覧を取るだけで、登録・承認画面の表示・後で読むファイルの検証に必要な情報がそろいます。

`skills/list` の 1 件は次のような形です（説明用の架空の例。digest は省略しています）。

```json
{
  "uri": "skill://acme/billing/refunds/SKILL.md",
  "frontmatter": {
    "name": "refunds",
    "description": "社内規程に沿って返金依頼を処理する"
  },
  "resources": [
    { "uri": "skill://acme/billing/refunds/SKILL.md", "digest": "sha256:…", "size": 175 },
    { "uri": "skill://acme/billing/refunds/examples/email.md", "digest": "sha256:…", "size": 58 }
  ]
}
```

中身をその場で生成するため digest を出せない Skill は、`resources` に配列の代わりに文字列 `"dynamic"` を入れます。**`"dynamic"` の Skill は中身を検証できず、承認を中身に結びつけられないため、ホストは読み込みを断ってよい**とされています。

### 上限

| 上限 | 値 | 数える対象 |
|------|----|-----------|
| 1 Skill のファイル数 | 512 | `resources` の件数（`SKILL.md` を含む） |
| 1 Skill の合計サイズ | 16 MiB | `resources` の `size` の合計 |

ホストはこの範囲の Skill を必ず扱える必要があり、server はこれを超える Skill を配るべきではありません。目録が完全なので、ホストはファイルを 1 つも取得する前に上限を確認できます。製品側でスキャン対象に別の上限を設ける例もあります。[Claude Code の制限](https://code.claude.com/docs/en/mcp#mcp-skill-limitations)

### 取得は必要になってから

ホストは接続時・一覧取得時・承認時に**ファイルを先回りして取得してはなりません**。`SKILL.md` は Skill を読み込むときに、同梱ファイルはそれが読まれるときに取得します。Agent Skills の「段階的な読み込み」と同じ考え方を、ネットワーク越しにも守らせる取り決めです。

なお、`resources/read` で `SKILL.md` を読んだだけでは Skill は**有効になりません**。Skill として扱うのは、ホストが検証と承認を通した読み込みの経路だけです。汎用の Resource 読み取りツールで中身を見ても、それは普通の Resource の内容として扱われます。

---

## 3. 対応状況

2026-11-28 に各製品の案内と [MCP 作業部会の実装一覧](https://github.com/modelcontextprotocol/ext-skills/blob/ba23984ab9859c88663d1ce1d93fa81942cae5a2/docs/implementations.md)を照合しました。実装一覧には各開発元の自己申告も含まれます。

Claude Code と VS Code の Copilot では、接続先の Skill をチャットから呼び出せます。利用条件と承認画面の読み方は[利用者向けの手順](use-mcp-skills.md)にまとめました。

### ホスト（Skill を読む側）

| ホスト | 提供元 | 状態 | 補足 |
|--------|--------|------|------|
| [Claude Code](https://code.claude.com/docs/en/mcp#use-skills-from-mcp-servers) | Official（Anthropic） | Preview | 対話型セッションでサーバー名付きの Skill を呼び出せる。 |
| [VS Code の Copilot](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/skills-over-mcp-are-now-available-in-vs-code/4574580) | Official（Microsoft） | Preview | 1.147 以降の Copilot Agent Host セッションで発見・読み込みに対応。 |
| ChatGPT・Codex | Official（OpenAI） | 計画段階 | 作業部会の実装一覧によると、ChatGPT の Plugin 申請時に Skill の写しを取り込む機能は2026年11月に取り下げられた。 |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Official（MCP） | 部分対応 | 2.6.0（2026-09-09）から。CLI で Skill を検証できる（[5 節](#5-server-を作る側の最小の確認)） |
| [mcpc](https://github.com/apify/mcpc) | Official（Apify） | Preview | MCP の CLI クライアント。配信されたファイルのサイズと digest を確認できる。 |
| [fast-agent](https://github.com/evalstate/fast-agent) | Community | Preview | 配信された Skill を検証して読み込める。 |
| [MCPJam Inspector](https://github.com/MCPJam/inspector) | Official（MCPJam） | Preview | アプリ・CLI・SDK で digest と frontmatter を検証する。 |
| Goose | Official（AAIF） | 計画中 | [aaif-goose/goose#12068](https://github.com/aaif-goose/goose/issues/12068) |

### SDK・server（Skill を配る側）

| 実装 | 状態 | 補足 |
|------|------|------|
| [C# SDK 2.4.0](https://github.com/modelcontextprotocol/csharp-sdk/releases/tag/v2.4.0) | **Experimental** | 2026-11-07 公開。`ModelContextProtocol.Extensions.Skills` で Skills extension を実装。server primitive と typed request handler に合わせた初期実装で、ホスト側の対応や拡張自体の GA を意味しない |
| [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk/pull/3047) | Preview | 2.4.0 の `ext/skills` にサーバー側とクライアント側の API を収録。 |
| [Python SDK](https://github.com/modelcontextprotocol/python-sdk/pull/3485)・[Go SDK](https://github.com/modelcontextprotocol/go-sdk/pull/1238) | 開発中 | Python は取り込み済みでリリース待ち、Go はレビュー中。 |
| [FastMCP](https://gofastmcp.com/servers/skills) | Experimental | 4.2.0 で `SkillCatalogProvider` による配布とクライアントからの読み取りに対応。 |
| mcpkit（Go）・Tachyon（Java） | 対応（自己申告） | mcpkit は適合テストの server シナリオに合格 |
| [hf-mcp-server](https://github.com/huggingface/hf-mcp-server)（Hugging Face） | 対応 | `skills/list`・`skills/get`・`directoryRead`。HTTP の transport のみ |
| [GitHub MCP Server](https://github.com/github/github-mcp-server/pull/3685) | Preview | 2.2.0 以降で明示的に有効化できる。利用可能な toolset に応じて Skill を配る。 |

---

## 4. ホストに課された承認とセキュリティの要件

Skill は model に渡す指示文なので、MCP で届く Skill は prompt injection の入口になります。しかも tool の呼び出しと違い、server が書いた文字列を手元に置き、手元のツールで実行するよう model に指示できます。仕様はこのため、**MCP で届く Skill を、リモートの tool 呼び出しより危険度の高い入口として扱う**ようホストに求めています。

| 要件 | 内容 | 読者が確かめること |
|------|------|------------------|
| **中身は信頼できない入力** | 接続している server の Skill だからといって、権威のある指示として扱わない。ほかの context より上位にも置かない | ホストが MCP の Skill をほかの外部入力と同じ防御の対象にしているか |
| **出所を model に見せる** | Skill の内容が context に入るとき、どの server から来たかを付ける。手元のファイルの Skill と見分けがつかない形で出さない | 承認画面・会話の表示に server 名が出るか |
| **暗黙の実行をしない** | Skill ごとの明示的な承認なしに、手元でコードを実行させない。hooks や frontmatter のスクリプトだけでなく、本文の「このスクリプトを実行せよ」という指示に従う tool 呼び出しも同じ承認の対象 | MCP の Skill を有効にしている間も、shell 実行の承認が外れていないか |
| **`allowed-tools` を効かせない** | frontmatter の `allowed-tools` は、MCP で届いた場合、その Skill について利用者が明示的に認めない限り**無視する**。リモートの server が書いた `allowed-tools` は、手元の権限を広げてほしいという**要求**にすぎない | ファイルの Skill と同じ感覚で `allowed-tools` が効いていないか |
| **ほかの server を読ませない** | server A の Skill が、server B に対する `resources/read` を起こしてはならない。別の server を読む場合は、両方の server 名を示して毎回承認を取る | 複数の MCP server を接続したときの読み取り先 |
| **名前の衝突を許さない** | Skill の名前は server をまたいで一意ではない。人気の Skill と同じ名前で配る攻撃があり得るため、名前は server ごとの名前空間で解決し、手元の Skill を黙って上書きさせない。server の識別には、server の自己申告の名前ではなくホストが付けた名前を使う | 同名の Skill が出たとき、ホストが知らせるか |
| **入れ子の Skill は別に承認** | Skill の中にある別の `SKILL.md` は、親を承認しても承認されたことにならない | — |
| **承認を中身に結びつける** | Skill 単位の承認を記憶する場合は、承認したときの全ファイルの URI と digest の組に結びつける。後でファイルが 1 つでも変わる・増える・減ると、**承認は取り消され、もう一度聞かれる** | 更新後に再承認を求められるか |
| **キャッシュは昇格させない** | 手元のキャッシュは、ホストしか書き込めない場所に置くか、読むたびに digest を計算し直す。キャッシュは手元の Skill を探す場所から外し、再起動後も server を切断した後も「MCP で届いたもの」として扱う。server を外したらキャッシュも消す | キャッシュの置き場所が `.claude/skills/` などの探索対象になっていないか |

### digest は信頼の根拠にならない

目録の digest には署名がなく、中身と同じ server が出しています。**digest が一致しても、「目録と中身が食い違っていない」ことしか分かりません。** server 自体が悪意を持っている場合や、途中の gateway が目録と中身を一緒に書き換えた場合は検出できません。仕様も「digest の一致をセキュリティの境界として扱ってはならない」と明記しています。

保存した目録と取得したファイルの digest を照合すると差し替えを検出できますが、**承認した時点の中身が安全だったかどうかは、利用者が読んで判断するしかありません**。導入前の確認手順は [Skill / Plugin のセキュリティ 2 節](skill-security.md#2-導入前に何を確認するか)と同じです。

### pnpm の承認との違い

同じ「Skill の承認」でも、何に結びつくかが違います。

| | 承認の単位 | 中身が変わったとき |
|---|---|---|
| [pnpm の agent skills](../trends.md#7-6-pnpm--依存パッケージに同梱された-skill-をつなぐ) | パッケージ（以降のバージョンにも及ぶ） | 聞き直されない |
| MCP Skills 拡張（Skill 単位で保存した承認） | Skill の全ファイルの URI と digest の組 | **承認が取り消され、聞き直される** |

pnpm はパッケージ単位で承認します。MCP の仕様は、ホストが **Skill 単位の承認を保存する場合**に、承認時のファイル一覧と digest に結びつけることを求めます。サーバー単位で読み込みを許可する製品もあるので、[利用画面での承認の単位](use-mcp-skills.md)も確認してください。

---

## 5. server を作る側の最小の確認

使う言語に合う実装を[対応表](#sdkserverskill-を配る側)から選びます。サーバーが公開した Skill の目録とファイルは、MCP Inspector の CLI で検証できます。

**どこで実行するか**: server の動作を確認できる端末のシェル（PowerShell など）。Node.js が必要です。`<server>` には Inspector に渡す server の指定（起動コマンドや URL）を入れます。

```bash
npx @modelcontextprotocol/inspector --cli <server> --method skills/list --verify
```

1 つの Skill だけを確かめる場合は、`--method skills/get --uri <SKILL.md の URI> --verify` にします。

| 確認すること | 内容 |
|-------------|------|
| 終了コード | `0` は合格。`7` は仕様の必須要件に違反（digest の不一致・読めないファイルなど）、`8` は読み取りの上限で途中まで、`9` は `--require-digests` を付けたときに digest のない（`"dynamic"`）Skill があった |
| 出力 | 標準出力に Skill ごとの結果が 1 行ずつ（NDJSON）、標準エラーに 1 行の要約 |
| frontmatter の照合 | 一覧に載せた frontmatter と、実際の `SKILL.md` の frontmatter が一致しているか。digest では「一覧が中身を正直に説明しているか」までは分からないため、別に照合される |

Inspector で目録とファイルを検証した後、配布先のクライアントでも Skill 名の表示と読み込みを確認します。[Claude Code・VS Code での確認手順](use-mcp-skills.md)

### 配る前に人が確認すること

- Skill の本文に、手元での実行（shell・スクリプト）を前提とした手順が入っていないか。入っている場合は、利用者が Skill ごとの実行を判断できるよう、実行内容を本文に書く
- `allowed-tools` に頼った設計になっていないか（MCP では既定で無視される）
- Skill 単位で承認を記憶する環境では、ファイルが変わると再承認が必要になる。利用者が差分を確認できる形で変更をまとめるか
- 同じ名前の有名な Skill がないか。あれば、利用者の混乱を避けるため接頭辞（`skill://<組織>/...`）で区別する

---

## 6. いま何をすればよいか

| 読者 | すること |
|------|---------|
| **Claude Code・VS Code の Copilot を使う人** | [利用手順](use-mcp-skills.md)に沿って、接続先の Skill 名と読み込み時の承認を確認する。 |
| **ChatGPT・Codex 向けに Plugin を作る人** | Skill を配る場合は [Plugin に同梱する手順](skill-publishing.md)を使う。 |
| **MCP server を作る人** | 対応する SDK や FastMCP で Skill を公開し、Inspector で目録と配信内容を検証する。 |
| **組織の導入担当** | MCP server の許可リストを見直すとき、tool だけでなく**その server が Skill を配るか**も確認項目に加える。Skill を配る server は、手元の振る舞いを変える指示を持ち込める |

---

## 関連ドキュメント

- [Skills 最新動向 7 節「Skill の発見・配布・更新」](../trends.md#7-skill-の発見配布更新) — ファイル・Plugin・パッケージで Skill を配る仕組み
- [Skills 最新動向 13 節「MCP 2026-07-28 仕様と移行時の確認」](../trends.md#13-mcp-2026-07-28-仕様と移行時の確認) — この拡張の前提となる base protocol
- [Skill / Plugin のセキュリティ](skill-security.md) — 導入前の確認手順と承認の記憶の範囲
- [MCP Apps — 会話内にUIを追加する](mcp-apps.md) — 同じく MCP の公式拡張。tool 結果として UI を返す
- [MCP と A2A — 役割の違いと併用方法](agent-protocols.md) — MCP の Tools / Resources / Prompts
- [Skill の公開・共有](skill-publishing.md) — Codex / ChatGPT 向け Plugin の作成と配布

## 参考リンク

- [SEP-2640: Skills Extension](https://modelcontextprotocol.io/seps/2640-skills-extension) — 動機・仕様・セキュリティ要件・見送った機能（アーカイブ形式での配布）（`提供元`: Official / MCP ｜ `状態`: Final）
- [Skills over MCP — Overview](https://modelcontextprotocol.io/extensions/skills/overview) — 公式文書の概要と通信の流れ（`提供元`: Official / MCP ｜ `状態`: —）
- [modelcontextprotocol/ext-skills](https://github.com/modelcontextprotocol/ext-skills) — 仕様の正本（`specification/beta/skills.mdx`）、決定記録、設計の理由、実装一覧（`提供元`: Official / MCP ｜ `状態`: —）
- [Extension Support Matrix](https://modelcontextprotocol.io/extensions/client-matrix) — クライアントごとの拡張の対応表（`提供元`: Official / MCP、コミュニティが更新 ｜ `状態`: —）
- [MCP Skills 作業部会の実装一覧](https://github.com/modelcontextprotocol/ext-skills/blob/main/docs/implementations.md) — ホスト・SDK・サーバーごとの対応と各実装へのリンク。
- [MCP Inspector CLI — Skill verification](https://github.com/modelcontextprotocol/inspector/blob/main/clients/cli/README.md#skill-verification---verify) — `--verify` の検証内容と終了コード（`提供元`: Official / MCP ｜ `状態`: —）
- [Agent Skills Specification](https://agentskills.io/specification) — Skill の書式。拡張はこれに委ねている（`提供元`: Official ｜ `状態`: —）
