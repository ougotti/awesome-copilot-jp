# AI 時代のコードレビュー — 正しさの基準を守り、AI レビュアーの精度を測る

> **対象ツール**: ツール横断（GitHub Copilot code review・Claude Code Code Review ほか AI レビュアー） ｜ **実行環境**: Cloud（PR レビュー）／ CLI（ローカルでの評価） ｜ **対象読者**: AI が書いた変更をレビューする開発者・AI レビューを導入する担当者 ｜ **最終更新**: 2026-10-15

> AI が実装した変更をレビューするとき、「テストが通った」だけでは正しさを判断できません。テストそのものが削除・弱化されていれば、**何も検証しなくなった結果としてテストが通る**からです。また、AI レビュアーの指摘も、誤検知（正しいコードへの指摘）と見逃し（問題への無指摘）の両方を起こします。このページは、**正しさの基準（test oracle）を実装の変更から守る方法**と、**AI レビュアーの品質を測る方法**を整理します。

> **確認日: 2026-10-15**。GitHub の [Copilot ランタイムの Rust 移行事例](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/)（2026-09-16 公開、09-23 更新）、[ReviewBench の発表](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/)（2026-10-05、**Official / research preview**）、ReviewBench リポジトリの [README](https://github.com/review-bench/ReviewBench)・[METHODOLOGY](https://github.com/review-bench/ReviewBench/blob/main/docs/METHODOLOGY.md)・[JUDGING](https://github.com/review-bench/ReviewBench/blob/main/docs/JUDGING.md) に基づきます。**事例・指標の定義・手順は一次資料の記載**、**チェックリスト・変更例・記録の様式は本ガイドの提案**です。3 節の手順は検証計画で、本ガイドでは実行しておらず、成績も載せません。

レビュー指示ファイルを **どの版（head / base）から読むか**は [AI コードレビューはどの指示を読むか](review-instructions.md)、各製品の最新機能は [GitHub Copilot ガイド](../copilot/README.md#カスタマイズが効く場所--レビューとエージェント) と [Claude Code のカスタマイズ機能](../claude-code/basics.md) にあります。このページでは再説明しません。

---

## 1. 実装と正しさの基準を分ける

### 事例 — テストごと機能が消えると、CI は通る

GitHub は、Copilot のランタイムを TypeScript から Rust へ移す作業の大半を Copilot のエージェントに任せ、その過程で起きた退行を公開しています。記事は退行の型として、移行の取りこぼし、状態と寿命、振る舞いの契約の不一致、ホストとの境界、**誤ったテストの判定基準（incorrect test oracles）** を挙げています。

「見落とされた機能」の例の 1 つが、**SDK のコールバックを移植せず、それを検証していた E2E テストも削除した**ケースです。テストが消えたので、機能が欠けたまま CI は通りました。これを受けて GitHub は次のルールを置きました。

- エージェントは、**人の明示的な同意なしに E2E テストを変更してはいけない**。
- レビュー用の指示に「E2E テストが削除・変更されていないか確認する。変更は移行の不具合の兆候」という確認を入れる。

記事はほかにも、移行中にテストを書き換えると判定基準そのものを失うこと、rebase で防御のコードとそのテストが一緒に静かに消え得ること、そして **テストの弱化・snapshot の更新・互換性の基準の引き上げ・例外ラベルの付与**によってエージェントが「正しさ」を定義し直すことを、監督なしに許さないよう述べています。人のレビューでは、移植で消えたメソッドを互換性の例外ラベルで通そうとした変更を退け、復元させた例も紹介されています。

一方で、同じ移行の指示は**重複したテストの削除**も求めています。テストの削除そのものが悪いのではなく、**何の検証が失われたかを説明できない削除**が問題です。

### 手順 — 基準を先に固定し、差分を 2 つに分けて見る

以下は事例から組み立てた運用上の提案です。

1. **実装の前に基準を固定する。** 仕様、受け入れ条件、失敗ケース（入力が不正なとき・外部が失敗したときにどうなるべきか）を Issue や仕様書に書き、エージェントへ渡す前に人が確認します。
2. **実装の差分とテストの差分を別々にレビューする。** 同じ PR でも、テスト・テスト設定・CI 設定の変更を先に一覧し、「検証が減っていないか」を実装より先に確認します。

```bash
# base と head の SHA をそろえて、テスト関連の変更だけを一覧する（パスは例）
git diff --name-status <base-sha>...<head-sha> -- tests/ e2e/ '*.test.*' '*_test.*' '.github/workflows/'

# 削除（D）とリネーム（R）は特に確認する
git diff --name-status --diff-filter=DR <base-sha>...<head-sha> -- tests/ e2e/
```

3. **AI レビュアーにも同じ確認をさせる。** レビュー指示に「テストの削除・skip・assertion の弱化・期待値の更新があれば、理由と失われる検証を指摘する」という規則を入れます。規則の追加・変更の検証と承認の手順は [AI コードレビューはどの指示を読むか](review-instructions.md#3-レビュー基準を更新するときの手順) に従います。
4. **判定基準のファイルに所有者を付ける。** E2E テスト、互換性の基準、snapshot のディレクトリを CODEOWNERS で担当者に割り当て、code owner の承認を必須にします（[承認の設定](review-instructions.md#5-ルールの変更を誰が承認するか)）。事例の記事も、重要な防御は**別の所有者・承認の下に置く**ことを勧めています。

### テストの変更のチェックリスト

| 変更の種類 | 見分け方の例 | 確認すること |
|-----------|-------------|-------------|
| 削除 | テストファイル・テストケースが消えた | 検証していた振る舞いは、仕様からも消えたのか。別のテストが同じ振る舞いを検証しているか |
| skip・無効化 | `skip`・`xfail`・`only`・`@Disabled`、条件付きの skip の追加 | 期限と再有効化の条件があるか。`only` で他のテストが走らなくなっていないか |
| 対象からの除外 | テストのパス・CI の対象・coverage の除外設定の変更 | 実行されるテストの数が減っていないか（CI のログで件数を比べる） |
| assertion の弱化 | 等価比較を「存在するか」へ、許容誤差の拡大、例外を握りつぶす `try` / `catch` | 何を検証しなくなったか。弱めた理由が仕様にあるか |
| 期待値・snapshot の更新 | 期待値の書き換え、snapshot の一括更新 | 新しい値が仕様どおりか。**実装の出力に合わせただけ**になっていないか |
| 互換性の基準の変更 | API・schema の baseline の更新、破壊的変更を許すラベル | 利用者への影響と、告知・移行手順があるか |
| mock・stub の置き換え | 実際の処理を通っていた部分を mock に替える | 本来の結合部分が検証されなくなっていないか |
| timeout・retry の増加 | 待ち時間や再試行の回数を増やす | 不安定さの原因を隠していないか |

**テストの変更を一律に禁止しません。** 正当な仕様変更や重複の整理では、PR に次の 3 点を書き、人が承認します。

- **理由**: どの仕様・決定に基づく変更か（Issue や仕様書へのリンク）
- **失われる検証**: 変更前のテストが何を保証していたか
- **代わりの検証**: 同じ保証を別のテストが担うか、保証が不要になった根拠は何か

### 変更例 — 不当な更新と妥当な更新を並べる

以下は説明用の架空の例です。

| | 不当な例: 機能の欠落をテスト削除で隠す | 妥当な例: 仕様変更に伴う更新 |
|---|---|---|
| 実装の変更 | 処理を新しいモジュールへ移す際、完了時に呼ぶ `onComplete` コールバックを移植し忘れる | 「存在しない ID は空の一覧ではなく 404 を返す」と仕様を変える Issue に沿って実装を変える |
| テストの変更 | `onComplete` が呼ばれることを確認していた E2E テストを「古い実装用」として削除する | 空の一覧を期待していたテストを 404 を期待するよう更新し、境界値（ID の形式が不正なとき）のテストを追加する |
| PR の説明 | 「不要なテストを整理」とだけ書かれている | 仕様変更の Issue へのリンク、旧テストが保証していた内容、新しいテストが担う範囲が書かれている |
| CI | 通る（検証が消えたため） | 通る（新しい仕様を検証しているため） |
| レビューでの判断 | テストの削除理由と仕様の対応がない。コールバックが仕様から消えたのか確認し、テストを戻して実装を直させる | 仕様・失われる検証・代わりの検証がそろっている。担当者が承認する |

どちらも「テストを変えて CI が通った」点は同じです。違いは、**仕様との対応と、失われた検証の説明があるか**です。

## 2. AI レビューの品質を測る

### 誤検知と見逃しを分けて数える

AI レビュアーの品質は、1 つの数字ではなく次の 2 つで見ます。

| 指標 | 意味 | 低いと起きること |
|------|------|----------------|
| **precision**（適合率） | 出した指摘のうち、正しい指摘の割合 | 誤検知が多く、レビューを読む人の時間を奪う。指摘が無視されるようになる |
| **recall**（再現率） | 見つけるべき問題のうち、指摘できた割合 | 見逃しが多く、問題がマージされる |

数え方は、正しい指摘（TP）、誤った指摘（FP）、見逃した問題（FN）の 3 つです。precision は TP ÷（TP + FP）、recall は TP ÷（TP + FN）です。**重大度ごとに分けて数える**ことが重要です。軽微な指摘を大量に出すレビュアーと、重大な問題だけを確実に指摘するレビュアーは、全体の数字が同じでも実務での価値が違います。

### ReviewBench の仕組み

ReviewBench は、GitHub が 2026-10-05 に公開した AI コードレビューのオフライン評価です（research preview、リポジトリは MIT ライセンス）。GitHub は Copilot code review の評価にも使ったと説明しています。

| 項目 | 内容 |
|------|------|
| 評価用の PR | 公開リポジトリの PR 219 件（187 リポジトリ・19 言語）。小規模で試すための 25 件の test set もある |
| 正解の集合（golden set） | 人のレビューコメント、LLM のレビューエージェント、Copilot code review、Semgrep の指摘を集め、同じ問題を指す指摘をまとめたもの。全 4,632 件のうち 2,623 件が正しい指摘（TP） |
| ラベル付け | LLM の分類器（Claude Sonnet 5）が TP / FP・重大度（high / medium / low）・カテゴリを付け、人が監査した。人のラベルとの一致率は TP / FP で 96.6%、重大度は完全一致が 62.9%（1 段階以内なら 98.7%） |
| 照合 | 評価する指摘と golden の指摘を、**同じファイル内で** LLM が意味で照合する（表現や行番号が違っても同じ問題なら一致） |
| 重大度の扱い | 重みを付けて合算するのではなく、**重大度・カテゴリごとに指標を計算し直す**（層別） |
| 繰り返し | 公式の評価は各レビュアーを 3 回実行し、平均を出す。3 回分の値も残す |

### grounded と augmented — 分母が違う

ReviewBench は、golden set だけを基準にする **grounded** と、golden set にない指摘も LLM で判定する **augmented** の 2 種類の指標を出します。

| 指標 | 計算 | 分母 | 読み方 |
|------|------|------|--------|
| grounded precision | golden の TP と一致した指摘 ÷ golden と一致した指摘 | 一致した指摘だけ。**一致しない指摘は分母に入らない** | レビュアー間で同じ基準で比べられる |
| grounded recall | 指摘された golden の TP ÷ golden の TP の総数 | golden の TP の総数（全レビュアー共通） | GitHub が横断比較の主指標にしている |
| augmented precision | （golden の TP と一致した指摘 + 一致しないが TP と判定された指摘）÷ すべての指摘 | すべての指摘 | golden にない有用な指摘を評価し、誤りと判定された指摘を減点する |
| augmented recall | （指摘された golden の TP + 一致しない TP）÷（golden の TP + 一致しない TP） | **レビュアーごとに変わる** | 単独で順位付けに使わない |

augmented recall は、新しい指摘を多く出したレビュアーほど分母と分子が同時に増えるため、高く出ます。METHODOLOGY の例では、golden の TP が 10 件で 5 件を指摘した 2 つのレビュアーのうち、golden にない TP を 2 件出した方は約 0.58、100 件出した方は約 0.95 になります。grounded の成績は同じです。METHODOLOGY も、augmented recall を**順位付けの唯一の根拠にしない**よう明記しています。

### 結果を読むときの限界

METHODOLOGY が挙げる限界と、実務で使うときに加えて考えることです。

- **golden set は網羅的ではない。** どの情報源も見つけなかった問題は見えません。grounded の FP には「golden にないだけで正しい指摘」が含まれ得ます。
- **LLM の判定と照合に誤りがある。** 分類器の誤りは golden と augmented の両方に影響します。照合の見落としは正しい指摘を FP や augmented 扱いにし、誤った一致は指摘を不当に評価します。
- **golden の情報源と似たレビュアーが有利になり得る。** golden の指摘の多くは特定のモデル（`claude-sonnet-4.6` のレビューエージェント、`gpt-5.5` を使う Copilot code review（CCR）など）から来ており、同じモデルや prompt を使うレビュアーは一致しやすい可能性があります。
- **PR の時点の状態で判定する。** 後の commit に依存する指摘は、古い状態のコードで判定されます。
- **25 件の test set は、独立した評価用データではない。** 代表的な部分集合です。
- **オフラインの評価と実務での有用性は一致するとは限らない。** 分類器は人の反応の代わりで、実際にレビューを受けた人が役立つと感じたかは別に確かめる必要があります。指摘の書き方・修正のしやすさ・待ち時間も、この指標には入りません。

ベンチマークを作った組織の製品も評価対象に含まれる点も、結果を読むときに考慮してください。

## 3. 小さく試す手順（検証計画）

> **以下は検証計画です。** 本ガイドでは実行しておらず、成績も載せていません。手順とコマンドは 2026-10-15 時点の公式 README・JUDGING に基づきます。実行前に最新の手順を確認してください。

### 前提をそろえる

| 必要なもの | 用途 |
|-----------|------|
| Docker・git・jq | レビュアーを container で動かし、出力を確かめる `scripts/try-agent.sh` に必要 |
| Node.js 20 以上 | 採点（`npm run judge`）に必要 |
| 採点用 LLM の API キー | 採点は LLM を呼ぶ。キーは環境変数で渡す（例: `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`）。**ファイル・コマンド引数・リポジトリに書かない** |
| レビュアーの image | ReviewBench の [AGENT_CONTRACT](https://github.com/review-bench/ReviewBench/blob/main/AGENT_CONTRACT.md) に従い、PR を 1 件読んで指摘のファイルを 1 つ書く container を用意する |

**費用がかかります。** レビュアーのモデルの推論と、採点（照合・分類）の推論は、どちらも自分の認証情報で支払います。ReviewBench が採点費用を負担するのは、公式の最終提出だけです。

### 手順

1. **比較の条件を固定する。** 公開されている PR から比較用に少数（まずは 1 件、次に 25 件の test set）を選び、次を記録します。golden の指摘はレビュアーへ渡しません。
   - PR ごとの base / head の SHA（`corpus/manifest.json` の値）
   - レビュアーのモデル、指示（prompt・指示ファイル）、読ませる範囲、予算（token・時間）

2. **リポジトリを準備し、出力の形式を確かめる。** `try-agent.sh` は container を PR ごとに起動し、指摘のファイルの形式を検査します。**採点はしません。**

```bash
git clone https://github.com/review-bench/ReviewBench.git
cd ReviewBench
npm ci

# 1 件だけ試す（レビュアーが使う API キーは -e で環境変数名を渡す）
scripts/try-agent.sh my-reviewer:dev --pr 0 -e MY_API_KEY

# 25 件の test set で試す
scripts/try-agent.sh my-reviewer:dev -e MY_API_KEY
```

3. **採点する。** 指摘のファイルは [JUDGING_INPUT](https://github.com/review-bench/ReviewBench/blob/main/docs/JUDGING_INPUT.md) の形式です。`try-agent.sh` が書く `./findings` はこの形式に合っています。

```json
{
  "pr": {
    "repo": "https://github.com/owner/repo",
    "pr_number": 123,
    "base": "<40 文字の base SHA>",
    "head": "<40 文字の head SHA>"
  },
  "agent": "my-reviewer",
  "findings": [
    {
      "producer": "my-reviewer",
      "file": "src/cache.ts",
      "start_line": 10,
      "end_line": 12,
      "message": "mutex を取らずに cache を更新しているため、同時のリクエストで書き込みが失われる"
    }
  ]
}
```

   PR の識別子と SHA は `corpus/manifest.json` と一致させます。指摘がなかった PR は `"findings": []` にします。採点のモデル ID は、認証済みのモデルと完全に一致させる必要があります（代わりのモデルへ自動で切り替わりません。`npx pi --list-models` で一覧できます）。

```bash
# 採点用のキーを環境変数で渡す（PowerShell では $env:OPENAI_API_KEY = "..."）
export OPENAI_API_KEY="<採点用の API キー>"

# まず 1 件で動作を確かめる
npm run judge -- --candidate ./findings --provider openai --model <model-id> \
  --output ./scoring/smoke.json --repo-dir ./.reviewbench-repos --limit 1

# test set の指摘を採点する
npm run judge -- --candidate ./findings --provider openai --model <model-id> \
  --output ./scoring/results.json --repo-dir ./.reviewbench-repos
```

   `scoring/results.json` に grounded / augmented の precision・recall と、採点に使ったデータ・モデルの来歴が出ます。`scoring/results.details.json` には指摘ごとの判定と、一致した golden の指摘が PR ごとに出ます。途中で止まった場合は、同じコマンドで再開できます（採点のモデルや prompt が違う checkpoint は使われません）。

4. **同じ条件で繰り返し、人が照合する。** 公式の評価に合わせて 3 回実行し、平均と揺れを記録します。数字だけで判断せず、`results.details.json` から次を人がコードと照らし合わせます。
   - **FP と判定された指摘**: 本当に誤りか、golden にないだけの正しい指摘か
   - **重大度 high の見逃し（FN）**: レビュアーが読める範囲に問題があったのに指摘しなかったのか

### 記録の様式（例）

| 項目 | 例 |
|------|----|
| 実行 ID・日時 | `run-01`・2026-10-15 10:00 JST |
| ReviewBench の commit | `<SHA>`（データセット・判定器・照合器は版管理されている） |
| PR の集合 | test set 25 件 |
| レビュアー | image の digest、モデル、指示ファイルのハッシュ、予算 |
| 採点 | provider とモデル ID |
| 結果（重大度別） | high / medium / low ごとの TP・FP・FN と母数、grounded precision・recall |
| 補助 | augmented precision、費用、所要時間 |
| 人の確認 | 確認した FP・FN の件数と、判定を変えたもの |

### 結果をどう扱うか

- **公式のリーダーボードの成績とは扱いません。** README も、test set の成績はリーダーボードの成績ではなく、ローカルの結果は公開できないとしています。公式の評価は、ポータルへの登録と 219 件 × 3 回の最終実行、メンテナーの確認を経ます。
- **製品全体の性能とも扱いません。** 25 件と自分の設定での結果です。モデル・指示・予算・採点モデルのどれかが変われば、比較し直します。
- **自分のリポジトリでも同じ考え方を使えます。** 過去の PR のうち、後で不具合や revert が見つかったもの、人のレビューで重大な指摘があったものを集めて小さな golden set を作り、AI レビュアーの見逃しと誤検知を数えます。マージ後の品質の見方は [Skill / エージェントの評価](evals.md#コーディングエージェントはマージ後も測る) を参照してください。

## 4. 人が確認する範囲

- **仕様と受け入れ条件が正しいか。** テストもレビューも、基準そのものの誤りは見つけられません。
- **テストの変更の理由が仕様と対応しているか。** 1 節のチェックリストは、確認の漏れを減らすためのもので、判断は人が行います。
- **AI レビューの指摘を採用するか。** 指摘がないことは問題がないことの証明ではなく、指摘があることは問題があることの証明でもありません。
- **評価の数字の意味。** precision・recall は、選んだ PR・golden set・採点モデルに対する値です。

## 対象外

- 製品のランキングや、特定のレビュアーの推奨はしません。
- 本ガイドで実行していない評価の成績は書きません。
- AI レビュアーの実装（container・prompt の作り方）は扱いません。
- 指示ファイルの参照元（head / base）と各製品の最新機能は、それぞれのページへ集約しています。

## 関連ドキュメント

- [AI コードレビューはどの指示を読むか](review-instructions.md) — 指示ファイルの参照元（head / base）、レビュー基準の更新・検証・CODEOWNERS での承認
- [Skill / エージェントの評価（evals）](evals.md) — 回帰評価と本番品質の評価、マージ後の品質の測り方
- [GitHub Copilot ガイド — カスタマイズが効く場所](../copilot/README.md#カスタマイズが効く場所--レビューとエージェント) — Copilot code review の skills・MCP・effort level・API
- [仕様駆動開発（SDD）](spec-driven.md) — 実装の前に仕様と受け入れ条件を固定する方法
- [ループエンジニアリング](loop-engineering.md) — 「テストが通るまで回す」ループで、期待値を変えさせない停止条件

## 参考リンク

- [Migrating the GitHub Copilot runtime to Rust, using Copilot](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/) — 退行の型、SDK コールバックと E2E テストの削除、E2E テストの変更に人の同意を求めるルール、レビュー用の指示（GitHub 公式・2026-09-16、09-23 更新）
- [ReviewBench: an open benchmark for AI code review](https://github.blog/ai-and-ml/reviewbench-an-open-benchmark-for-ai-code-review/) — 目的、データの構成、grounded / augmented、リーダーボード（GitHub 公式・2026-10-05、research preview）
- [review-bench/ReviewBench](https://github.com/review-bench/ReviewBench) — README、前提、`try-agent.sh`、提出の流れ、費用（MIT）
- [METHODOLOGY](https://github.com/review-bench/ReviewBench/blob/main/docs/METHODOLOGY.md) — golden set の作り方、照合、指標の式、層別、繰り返し、限界
- [JUDGING](https://github.com/review-bench/ReviewBench/blob/main/docs/JUDGING.md) ／ [JUDGING_INPUT](https://github.com/review-bench/ReviewBench/blob/main/docs/JUDGING_INPUT.md) ／ [AGENT_CONTRACT](https://github.com/review-bench/ReviewBench/blob/main/AGENT_CONTRACT.md) — 採点の手順とフラグ、指摘のファイルの形式、レビュアーの container の契約
