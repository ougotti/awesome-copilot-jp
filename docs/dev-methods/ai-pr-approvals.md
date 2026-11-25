# AI に PR の承認を任せる前に決めること — Claude Ship の Approvals を例に

> **対象ツール**: ツール横断（Claude Ship の Code Review・PR Steward・Claude Approvals、Claude Code の `/ship`・`/steward`、GitHub Copilot approvals） ｜ **実行環境**: Cloud / CLI ｜ **対象読者**: リポジトリの管理者・チームのリード・ブランチ保護を設定する人 ｜ **最終更新**: 2026-11-25

> 2026-11-23、Anthropic は GitHub の PR を扱う 3 つのエージェントをまとめた **Claude Ship** を発表しました。レビュー（Code Review）、CI の失敗やコンフリクトを直し続ける修復（PR Steward）に加えて、**チームが書いた方針に沿って Claude が PR を approve する Claude Approvals** が入っています。Copilot にも 2026-09 から approval の機能があり（[GitHub Copilot ガイド](../copilot/README.md#プルリクエストの承認をどこまで-ai-に任せるか)）、「AI がレビューする」から「AI が承認する」へ範囲が広がりつつあります。
>
> このページは、Claude Approvals を具体例にして、**AI に承認を任せる前に決めること**（どの変更を任せるか、方針をどこに置き誰が変えられるか、ブランチ保護とどう組み合わせるか、誰の名義で何が push されるか、費用と止め方）をまとめます。記載は **2026-11-25 に確認した Anthropic の発表と Claude Code Docs** に基づきます。**実機・管理画面での検証はしていません。**「本記事の提案」「本記事の見立て」と書いた部分は、公式の説明ではなく本記事の判断です。

---

## 1. 11-23 に何が出たか

| 構成要素 | 提供元・状態 | 何をするか | approve / merge |
|---|---|---|---|
| **Code Review** | Official / GA | PR を読み、重大度つきのインラインコメントで指摘を返す | しない |
| **PR Steward** | Official / Beta | PR が開かれると見守りを始め、失敗した check・merge conflict・レビューの指摘を直す commit を PR の branch に push し続ける | **しない設計**。approve は Anthropic のサービス側で拒否される |
| **Claude Approvals** | Official / Beta | リポジトリの方針ファイルに従って PR を判定し、`Claude Approvals` という check を出す。方針が許せば approving review を出す | **approve する**。merge はしない |
| `/ship`・`/steward` | Official / Claude Code のコマンド | 手元の Claude Code から、commit・push・PR 作成・レビュー（`/ship` のみ）・修復の見守りまでを進める | 方針上は「merge は自分で」。ただし例外がある（[5 節](#5-誰の名義で何が-push-されるか)） |

- 対象は **Claude の Team と Enterprise**、**GitHub のリポジトリ**です。PR Steward は接続した GitHub Enterprise Server でも動きます。
- **Zero Data Retention・HIPAA の構成・顧客管理の暗号鍵（CMEK）を使う組織では使えません。** Claude Approvals は FERPA や Access Transparency の設定がある場合も始められない、と docs にあります。
- 発表は、Claude Ship も**バグや脆弱性を見逃すことがある**と明記し、まず **observe（観察）モード**で始めるよう勧めています。
- 発表には Claude Code チーム内での数字（merge された PR の増加、revert の減少）が載っていますが、Claude Ship 単独の効果として切り分けたものではないと読めます。本記事では効果の根拠としては扱いません（本記事の見立て）。

## 2. 「承認」は 3 つの設定に分かれている

AI の approve を考えるとき、次の 3 つを分けておくと議論が混ざりません。Copilot でも Claude でも同じ構造です。

| 段階 | Claude Approvals | Copilot approvals（参考） |
|---|---|---|
| **AI が判定を出す** | `Claude Approvals` の check。observe モードでは判定だけ出して approve しない | approval assessment。すべての Copilot review に表示される |
| **AI が approving review を出す** | 方針で `claude: approves` とし、適用されるすべての規則が同意したときだけ | 管理者が明示的に許可したときだけ（既定は無効） |
| **それが merge を止める・通す** | **GitHub 側で `Claude Approvals` を required status check にしたときだけ**、merge を止める。Claude の approving review は、GitHub の「必要な承認 1 件」に数えられる | "count toward merge requirements" の別の設定で決める |

つまり、**方針ファイルを置いただけでは merge は止まりません。** 逆に、required check にして必要な承認を 1 件にすると、**人が誰も操作しないまま merge される経路**ができます（auto-merge や merge queue を使っている場合。docs も明記しています）。この 2 つのどちらを望むのかを、導入の前に決めます（本記事の提案）。

## 3. どの変更を AI の承認に任せるか

### 3-1. 方針ファイルで書けること

Claude Approvals の方針は、リポジトリの **`.claude/approvals.yml`**（YAML）に書きます。docs の policy reference によると、規則ごとに次を指定できます。

- **`paths`**: glob で対象のファイルを絞る
- **`verdict`**: Claude の扱い（`approves`・`comments`・`blocks`）と、**人の承認（seats）**の数と、誰が数えられるか（人・bot・特定の login・`org/team` のチーム）
- **`if`**: PR の事実による条件（変更ファイル数・差分の行数・作者・ベースの branch など）。**CI の結果は条件に使えない**と書かれています
- **classifier**: Claude のレビュー結果や、リポジトリで自然言語で定義した判定（例: 変更のリスク）を参照する
- **`mode`**: `observe` か `enforce`（既定は enforce）

サブディレクトリに別の `.claude/approvals.yml` を置くと、近いほうの方針が効きます（`nested: inherit` で親の規則を引き継ぐこともできます）。

### 3-2. 任せる範囲の決め方（本記事の提案）

最初から「AI が承認してよい」範囲を広く取らず、**失敗しても戻しやすく、人のレビューの価値が低い変更**から始めます。

| 区分 | 例 | 方針の目安 |
|---|---|---|
| 任せやすい | ドキュメント、コメント、翻訳、テストデータの追加 | `claude: approves`、人の seats は 0 か 1 |
| 人を 1 人残す | アプリのコード全般 | `claude: comments`（Claude は指摘だけ）、seats 1 以上 |
| 人を複数・特定の人にする | 認証・権限・課金・暗号・データ削除・migration | `claude: comments` か `blocks`、seats に CODEOWNERS と同じチームを指定 |
| AI に触らせない | CI の workflow、`CODEOWNERS`、`.claude/` 配下、デプロイ設定、依存関係の lockfile | 人の承認を必須にする |

- **seats が 0 か 1 の規則は、作者本人や bot だけで埋まることがあります**（docs の注意）。「人が 1 人見た」ことを保証したいなら、数えてよい people を絞ります。
- 差分の大きさ（`pr/diff_lines` など）を条件に入れて、**大きい PR は自動承認の対象から外す**のが扱いやすい線引きです。2,000 ファイルを超える PR は評価できず失敗する、と docs にあります。

## 4. 方針をどこに置き、誰が変えられるか

AI に承認させる仕組みでは、**方針そのものを書き換えれば何でも通せる**ことが一番の弱点になります。Claude Approvals の docs は次のように説明しています。

- 方針は **default branch の内容**が使われます。PR の中で方針ファイルを変えても、その PR には効きません（文法の検査だけされる）。merge 後に新しい PR から効きます。
- 方針ファイルと `CODEOWNERS` などは **protected file** として扱われ、変える PR には書き込み権限を持つ人の承認が要る場合があります。**ただし、その人は作者本人でもよい**とされています。
- default branch に merge できる人は方針を変えられます。リポジトリの管理者は、GitHub 側で required check を外すこともできます。

このことから、次を勧めます（本記事の提案）。

1. `.claude/approvals.yml` と `.claude/classifiers/` を **`CODEOWNERS` で特定のチームの持ち物にし**、GitHub のブランチ保護で「Code Owner のレビューを必須」にする。方針の変更だけは必ず別の人が見る形にする。
2. ブランチ保護で「**新しい commit が push されたら古い承認を取り消す**」（Dismiss stale pull request approvals）か、「最新の push の承認を必須にする」を有効にする。docs もこれを勧めています。PR Steward が承認後に push したときに、古い承認で merge されるのを防げます。
3. GitHub の「必要な承認数」は **1 のままにし**、2 人目以降は方針の seats で表す。docs は、GitHub 側で 2 以上にすると Claude の承認と食い違う、と説明しています。

レビューの指示ファイルを head と base のどちらから読むかは製品ごとに違います（[AI コードレビューはどの指示を読むか](review-instructions.md)）。**承認の方針も「どの branch の内容が効くか」を確かめてから使う**のが安全です。

## 5. 誰の名義で何が push されるか

承認とは別に、修復のエージェントが**誰の名義で、どこまで書き込めるか**も決めておきます。

| 経路 | 名義 | 書き込めるもの | できないこと・止める仕組み |
|---|---|---|---|
| **PR Steward**（cloud） | Claude GitHub App（GHES では組織のアプリ） | PR の branch への commit、コメントへの返信。installation が許せば workflow ファイルも | approve・branch 保護や ruleset の変更・check run の書き込み・branch の削除・tag の push は**サービス側で拒否**。merge・auto-merge の有効化・force-push・**PR 以外の branch への push** は**GitHub の branch ルールに任されている** |
| **Claude Approvals** | `claude[bot]`（Claude が作った PR では `claude-approvals[bot]`） | approving review と check | merge はしない |
| **`/ship`・`/steward`**（手元） | **自分の `gh` / `git` の認証情報**。操作はすべて自分の名前で残る | commit・push・PR 作成・レビューの返信と resolve | 見守り中は merge・approve・auto-merge・force-push を Claude Code が止めるが、docs は**それで全部は防げない**と明記。auto-merge が有効な PR は merge され得る |

ここから分かることは 2 つです（本記事の見立て）。

- **PR Steward の安全性の多くは、GitHub の branch ルールに依存しています。** 守りたい branch に ruleset がなければ、push や force-push はエージェントの判断と許可ルールだけに頼ることになります。導入前に、default branch と release branch の ruleset を確かめてください。
- **`/ship` は「自分が書いた」ことになります。** 見守り中は、base branch のコード・他人の push・テスト・hook・リポジトリの Skill が**自分の認証情報で**動く、と docs は注意しています。base に merge できる人や自分の branch に push できる人を全員信頼できるリポジトリでだけ使います。なお docs には、**ネイティブの Windows では見守りが始まらない**と書かれています。

ID と権限の考え方は [AIエージェントのID・認可・委任権限](agent-identity.md) を参照してください。

## 6. 費用と止め方

金額や含まれる量は本記事では書きません。[Claude Ship の製品ページ](https://claude.com/product/claude-ship) と組織の設定画面で確かめてください。docs から分かる**仕組み**は次のとおりです。

| 項目 | 内容 |
|---|---|
| 課金先 | cloud の 3 つのエージェントは、プランに含まれる利用量とは別の **組織の usage credits** から引かれる。`/ship`・`/steward` は通常の Claude Code の利用として数えられる |
| observe モード | **observe でも課金される。** 方針が Claude のレビューを使うなら、observe 中もレビューが走る |
| 上限 | Owner が Organization settings > Usage で、組織全体・Code Review・classifier の実行それぞれに上限を設定できる。**PR Steward は Owner が設定するまで上限がない** |
| 上限に達したとき | Code Review の上限に達すると、Claude のレビューを必要とする check が通らなくなることがある。**merge が止まる側に倒れる**ので、上限の通知先と対応する人を決めておく（本記事の提案） |
| 止め方 | 組織全体では Approvals → PR Steward → Code Review の順に止める。**usage credits を切っても、有効なエージェントは止まらず課金が続く**と docs にある。PR 単位では、PR Steward はラベル `claude-pr-steward-watching` を外すか `@claude stop` とコメントする。手元の `/ship` は managed settings や環境変数で組織として無効にできる |

費用の上限の考え方は [エージェントの費用管理](agent-costs.md) を参照してください。

## 7. 導入の順番（本記事の提案）

1. **Code Review だけを入れて**、指摘の質と誤検知を数週間見る（[AI 時代のコードレビュー](ai-code-review.md) の測り方が使える）。
2. 守りたい branch の **ruleset・CODEOWNERS・古い承認の取り消し**を先に整える。
3. Claude Approvals を **`mode: observe`** で入れる。全パスで `claude: comments`・seats 1 以上から始め、check のタイトルに出る判定と、人の判断が食い違った PR を記録する。
4. 食い違いが少ない**狭いパス（ドキュメントなど）だけ** `claude: approves` に変え、`mode: observe` の行を消して merge し、`Claude Approvals` を required status check にする。docs の手順では、そのあと `.claude/` 配下に触れる PR で、人のレビュー待ちになることを確かめます。
5. PR Steward は、ruleset で守られた branch があることを確かめてから、**手動起動（`@claude steward`）**の設定で始める。
6. 範囲を広げるたびに、revert や事後の修正が増えていないかを見る。増えたら範囲を戻す。

> **Copilot と併用するリポジトリでは**、Copilot approvals と Claude Approvals の両方が approving review を出せる状態にしないでください。どちらの承認を merge 要件に数えるのかを 1 つに決め、もう一方は判定の表示だけにします（本記事の提案）。

## 8. コミュニティの見方 — Hacker News

> 以下は Hacker News の利用者の意見で、公式の説明でも本記事の確認結果でもありません。

TechCrunch の記事を紹介した投稿（[item 50621162](https://news.ycombinator.com/item?id=50621162)）は、2026-11-25 の確認時点で 4 points・2 comments と、まだ議論は小さいものでした。

- 投稿者は、方針に沿って AI が変更を自動で承認できる点を要点として挙げていました。
- 返信では、自分のチームはすでに同じことを自作の仕組みで行っているので、製品に入ったのは驚きではない、という経験が語られていました。
- 「AI が書いたコードを AI が承認する」ことへの懸念や、Copilot との比較・費用の議論は、確認時点では出ていませんでした。

報道の側では、AI が書いたコードを AI が承認する構図そのものを論点にする記事が複数ありました（[TechCrunch](https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/) など）。本記事ではこれらの評価を確かめていません。

## 関連ドキュメント

- [GitHub Copilot ガイド — プルリクエストの承認をどこまで AI に任せるか](../copilot/README.md#プルリクエストの承認をどこまで-ai-に任せるか) — Copilot approvals の設定階層とパス限定
- [AI コードレビューはどの指示を読むか](review-instructions.md) — レビューの基準が head と base のどちらから読まれるか
- [AI 時代のコードレビュー](ai-code-review.md) — AI レビュアーの誤検知・見逃しの測り方
- [人の仕事はどこに移るか](human-role.md) — レビューが律速になるときに人が持ち続ける仕事
- [チームで常設するエージェント](team-automations.md) — Copilot の Agent Merge と、常設エージェントの名義・費用
- [AIエージェントのID・認可・委任権限](agent-identity.md) — エージェントに渡す権限の設計
- [エージェントの費用管理](agent-costs.md) — 上限と配分の設計

## 参考リンク

- [Introducing Claude Ship](https://claude.com/resources/articles/introducing-claude-ship) — 発表。構成要素と状態、対象プラン、observe モードの推奨、見逃しの注意（Anthropic 公式・2026-11-23 公開・2026-11-25 確認）
- [Claude Ship](https://code.claude.com/docs/en/claude-ship) — 全体像、対象外の組織、課金と止める順番（Claude Code Docs・2026-11-25 確認）
- [Claude Approvals](https://code.claude.com/docs/en/approvals) / [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup) — observe から enforce への切り替え、required check（Claude Code Docs・2026-11-25 確認）
- [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy) — `.claude/approvals.yml` の書式、protected file、上限（Claude Code Docs・2026-11-25 確認）
- [Claude Approvals and your GitHub rules](https://code.claude.com/docs/en/approvals-github-rules) — ブランチ保護・必要な承認数・auto-merge と merge queue（Claude Code Docs・2026-11-25 確認）
- [PR Steward](https://code.claude.com/docs/en/pr-steward) / [What PR Steward can access](https://code.claude.com/docs/en/pr-steward-security) — 起動条件、止め方、名義と権限、拒否される操作（Claude Code Docs・2026-11-25 確認）
- [Get a pull request ready with /ship and /steward](https://code.claude.com/docs/en/ship-command) — 手元のコマンドの流れ、merge の例外、Windows での制限（Claude Code Docs・2026-11-25 確認）
- [Copilot code review can now approve pull requests](https://github.blog/changelog/2026-09-01-copilot-code-review-can-now-approve-pull-requests/) — Copilot approvals（GitHub 公式）
- [Anthropic launches Claude Ship](https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/) — 報道（TechCrunch）
- [Hacker News: Anthropic launches Claude Ship](https://news.ycombinator.com/item?id=50621162) — コミュニティの反応（2026-11-25 確認）
