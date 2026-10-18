# MCP Skills 拡張 — Skill を MCP server から配る

> **対象ツール**: ツール横断（MCP server の開発者・MCP に対応したホスト） ｜ **実行環境**: CLI / IDE / Cloud / Chat UI ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-10-19

> [MCP Skills 拡張](https://modelcontextprotocol.io/extensions/skills/overview)（`io.modelcontextprotocol/skills`、[SEP-2640](https://modelcontextprotocol.io/seps/2640-skills-extension)）は、`SKILL.md` を含む Skill のディレクトリを、**ファイルとしてではなく MCP の Resources として**届ける公式の拡張です。MCP server が自分の tool の使い方を Skill として一緒に配れるようになります。このページでは、ファイルで配る Skill との違い、仕組み、対応状況、ホストに課された承認とセキュリティの要件を整理します。内容は 2026-10-19 に一次資料で確認したもので、実機・SDK での検証は行っていません。

---

## 1. 何が変わるのか

これまで Skill は、リポジトリの `.claude/skills/` や `.agents/skills/` などに**ファイルとして置き**、エージェントがそれを読む形が基本でした（配布の手段は [Skills 最新動向 7 節](../trends.md#7-skill-の発見配布更新)）。MCP Skills 拡張では、MCP server が Skill を Resources として公開し、ホスト（Claude・ChatGPT・IDE などのクライアント）が**必要になった時点で server から読み出します**。

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
| 更新 | ファイルを差し替える | Plugin を更新する | server を更新すれば即時 | server を更新すれば即時。ただし**中身が変われば承認をやり直す**（[4 節](#4-ホストに課された承認とセキュリティの要件)） |
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
| 状態ラベル | 本ガイドでは **Preview** として扱う。仕様は確定しているが、主要なホストの対応がまだ部分的なため（[3 節](#3-対応状況)） |

> OpenAI の文書は、この拡張を「draft SEP-2640」「stable MCP specification の一部ではない」と書いています。SEP は Final ですが、**拡張は core の仕様とは別に版を重ねる**ため、core の仕様書だけを見ても載っていません。拡張の仕様は ext-skills の `specification/stable/skills.mdx` が正です。

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

ホストはこの範囲の Skill を必ず扱える必要があり、server はこれを超える Skill を配るべきではありません。目録が完全なので、ホストはファイルを 1 つも取得する前に上限を確認できます。ただし**ホストごとにさらに小さい上限を持つことがあります**（ChatGPT の例は [3 節](#chatgpt-の取り込み)）。

### 取得は必要になってから

ホストは接続時・一覧取得時・承認時に**ファイルを先回りして取得してはなりません**。`SKILL.md` は Skill を読み込むときに、同梱ファイルはそれが読まれるときに取得します。Agent Skills の「段階的な読み込み」と同じ考え方を、ネットワーク越しにも守らせる取り決めです。

なお、`resources/read` で `SKILL.md` を読んだだけでは Skill は**有効になりません**。Skill として扱うのは、ホストが検証と承認を通した読み込みの経路だけです。汎用の Resource 読み取りツールで中身を見ても、それは普通の Resource の内容として扱われます。

---

## 3. 対応状況

2026-10-19 時点の[公式の対応表](https://modelcontextprotocol.io/extensions/client-matrix)と、Working Group の[実装一覧](https://github.com/modelcontextprotocol/ext-skills/blob/main/docs/implementations.md)をまとめます。どちらもコミュニティが更新する一覧で、自己申告を含みます。

**Claude Code・GitHub Copilot（VS Code）・Codex は、2026-10-19 時点でこの拡張に正式対応していません。** SEP には Claude Code を Anthropic 社内で試作したこと、gemini-cli と Codex のフォークで試作したことが記録されていますが、いずれも公開された製品の機能ではありません。手元のエージェントで今すぐ使える機能として扱わないでください。

### ホスト（Skill を読む側）

| ホスト | 提供元 | 状態 | 補足 |
|--------|--------|------|------|
| [ChatGPT（Plugin）](https://developers.openai.com/plugins/build/mcp-server#import-skills-from-the-mcp-server) | Official（OpenAI） | 部分対応 | Plugin の申請時に Skill を**静的なスナップショット**として取り込む（下記） |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Official（MCP） | 部分対応 | 2.6.0（2026-09-09）から。CLI で Skill を検証できる（[5 節](#5-server-を作る側の最小の確認)） |
| [mcpc](https://github.com/apify/mcpc) | Official（Apify） | 対応表では対応 | MCP の CLI クライアント |
| [fast-agent](https://github.com/evalstate/fast-agent) | Community | 部分対応 | 最初に server と端から端まで相互運用したクライアント |
| [MCPJam Inspector](https://github.com/MCPJam/inspector) | Official（MCPJam） | 部分対応 | アプリと CLI で Skill を表示し、拡張の capability を宣言する |
| Goose | Official（AAIF） | 計画中 | [aaif-goose/goose#12068](https://github.com/aaif-goose/goose/issues/12068) |

### SDK・server（Skill を配る側）

| 実装 | 状態 | 補足 |
|------|------|------|
| 公式 SDK（TypeScript・Python・Go・C#） | **実装中**（PR 段階） | 公式 SDK で正式に使える版はまだない |
| FastMCP の SkillsProvider | 実装中 | 公開済みの版は**独自の `skill://` 形式**のままで、この拡張とは URI・発見の方法が違う。SEP は移行を当面の優先課題としている |
| mcpkit（Go）・Tachyon（Java） | 対応（自己申告） | mcpkit は適合テストの server シナリオに合格 |
| [hf-mcp-server](https://github.com/huggingface/hf-mcp-server)（Hugging Face） | 対応 | `skills/list`・`skills/get`・`directoryRead`。HTTP の transport のみ |
| GitHub MCP Server | 試作 | デモ用のブランチで、merge の予定なし |

### ChatGPT の取り込み

ChatGPT の Plugin は、申請画面の **Scan Tools** を実行した時点で MCP server の Skill を取り込みます。**取り込まれるのは実行時に読みに行く Skill ではなく、申請時点の写し**です。Skill を直したら、もう一度 Scan Tools を実行し、取り込まれた内容を確認して、新しい版の Plugin を申請する必要があります。

| ChatGPT の上限（2026-10-19 確認） | 値 |
|----------------------------------|----|
| Skill の数 | 名前の異なる 5 件まで（一覧は 10 ページまで） |
| 1 Skill のファイル数 | 100 |
| `SKILL.md` | 256 KiB |
| 同梱ファイル 1 つ | 1 MiB |
| 1 Skill の合計 | 5 MiB |

仕様の上限（512 ファイル・16 MiB）より小さいため、**仕様に合っていても ChatGPT には取り込めない Skill があり得ます**。1 件でも検証に失敗するか上限を超えると、tool は読み込まれても Skill の取り込みは前のままになります。capability は `experimental` ではなく `extensions` に宣言する必要があり、旧来の宣言は認識されません。Plugin の申請手順そのものは [Skill の公開・共有](skill-publishing.md)を参照してください。

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
| **承認を中身に結びつける** | 承認を記憶する場合は、承認したときの全ファイルの URI と digest の組に結びつける。後でファイルが 1 つでも変わる・増える・減ると、**承認は取り消され、もう一度聞かれる** | 更新後に再承認を求められるか |
| **キャッシュは昇格させない** | 手元のキャッシュは、ホストしか書き込めない場所に置くか、読むたびに digest を計算し直す。キャッシュは手元の Skill を探す場所から外し、再起動後も server を切断した後も「MCP で届いたもの」として扱う。server を外したらキャッシュも消す | キャッシュの置き場所が `.claude/skills/` などの探索対象になっていないか |

### digest は信頼の根拠にならない

目録の digest には署名がなく、中身と同じ server が出しています。**digest が一致しても、「目録と中身が食い違っていない」ことしか分かりません。** server 自体が悪意を持っている場合や、途中の gateway が目録と中身を一緒に書き換えた場合は検出できません。仕様も「digest の一致をセキュリティの境界として扱ってはならない」と明記しています。

承認後に中身が差し替えられることは digest で防げますが、**承認した時点の中身が安全だったかどうかは、利用者が読んで判断するしかありません**。導入前の確認手順は [Skill / Plugin のセキュリティ 2 節](skill-security.md#2-導入前に何を確認するか)と同じです。

### pnpm の承認との違い

同じ「Skill の承認」でも、何に結びつくかが違います。

| | 承認の単位 | 中身が変わったとき |
|---|---|---|
| [pnpm の agent skills](../trends.md#7-6-pnpm--依存パッケージに同梱された-skill-をつなぐ) | パッケージ（以降のバージョンにも及ぶ） | 聞き直されない |
| MCP Skills 拡張 | Skill の全ファイルの URI と digest の組 | **承認が取り消され、聞き直される** |

pnpm の承認は「この発行元を信頼する」判断、MCP Skills 拡張の承認は「この中身を信頼する」判断です。前者は更新のたびに差分を自分で読む必要があり、後者は更新のたびに承認を求められます。どちらも、**承認したことを中身を読んだことの代わりにはできません**。

---

## 5. server を作る側の最小の確認

公式 SDK はまだ実装中のため、server を作る場合は SDK の対応状況を先に確認してください（[3 節](#sdkserverskill-を配る側)）。作った server が仕様に合っているかは、MCP Inspector の CLI で確かめられます。

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

Inspector の検証に通っても、**特定のホストで使えるとは限りません**。ChatGPT のように仕様より小さい上限を持つホストもあるため、配る先のホストの文書もあわせて確認してください。

### 配る前に人が確認すること

- Skill の本文に、手元での実行（shell・スクリプト）を前提とした手順が入っていないか。入っている場合、ホストは毎回承認を求めるため、利用者が何を承認するのかを本文に書いておく
- `allowed-tools` に頼った設計になっていないか（MCP では既定で無視される）
- 中身を頻繁に変える Skill は、更新のたびに利用者へ再承認を求めることになる。変更をまとめて出す運用にするか
- 同じ名前の有名な Skill がないか。あれば、利用者の混乱を避けるため接頭辞（`skill://<組織>/...`）で区別する

---

## 6. いま何をすればよいか

| 読者 | すること |
|------|---------|
| **Claude Code・Copilot・Codex をそのまま使う人** | 現時点で対応すべきことはありません。Skill は従来どおりファイルや Plugin で入れます。各製品が対応したときに備え、[4 節](#4-ホストに課された承認とセキュリティの要件)の「読者が確かめること」を覚えておく |
| **ChatGPT 向けに Plugin を作る人** | MCP server の Skill を Plugin に取り込めます。取り込みは申請時の写しなので、Skill を直したら Scan Tools と再申請が必要 |
| **MCP server を作る人** | server の使い方を Skill として一緒に配れます。公式 SDK の対応を待つか、対応済みの実装を使い、Inspector で検証する。FastMCP の現行版の `skill://` はこの拡張と形式が違う点に注意 |
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
- [modelcontextprotocol/ext-skills](https://github.com/modelcontextprotocol/ext-skills) — 仕様の正本（`specification/stable/skills.mdx`）、決定記録、設計の理由、実装一覧（`提供元`: Official / MCP ｜ `状態`: —）
- [Extension Support Matrix](https://modelcontextprotocol.io/extensions/client-matrix) — クライアントごとの拡張の対応表（`提供元`: Official / MCP、コミュニティが更新 ｜ `状態`: —）
- [Import skills from the MCP server](https://developers.openai.com/plugins/build/mcp-server#import-skills-from-the-mcp-server) — ChatGPT の Plugin が Skill を取り込む条件と上限（`提供元`: Official / OpenAI ｜ `状態`: —）
- [MCP Inspector CLI — Skill verification](https://github.com/modelcontextprotocol/inspector/blob/main/clients/cli/README.md#skill-verification---verify) — `--verify` の検証内容と終了コード（`提供元`: Official / MCP ｜ `状態`: —）
- [Agent Skills Specification](https://agentskills.io/specification) — Skill の書式。拡張はこれに委ねている（`提供元`: Official ｜ `状態`: —）
