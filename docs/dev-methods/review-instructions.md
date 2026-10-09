# AI コードレビューはどの指示を読むか — head / base とレビュー基準の更新

> **対象ツール**: GitHub Copilot code review / Claude Code Code Review ｜ **実行環境**: Cloud（GitHub 上の PR レビュー） ｜ **対象読者**: AI レビューを運用する開発者・リポジトリ管理者 ｜ **最終更新**: 2026-10-10

> AI レビューの結果を確認するときは、コードの差分と一緒に「**どの版のレビュー基準を使ったか**」も確認します。たとえば、公開関数に説明文を求めるルールと、そのルールに従わないコードを同じ PR で変更した場合、レビュー結果にはコードとルールの両方の変更が影響し得ます。このページは、指示ファイルの参照元を確かめ、レビュー基準の変更を検証・承認する手順を整理します。

> **確認日: 2026-10-10**。GitHub の [Copilot code review](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review)・[About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)、Anthropic の [Code Review](https://code.claude.com/docs/en/code-review)・[Claude Code v2.1.292](https://github.com/anthropics/claude-code/releases/tag/v2.1.292) に基づきます。**提供状況と動作は公式資料の記載**、**3〜5 節の手順と検証例は本ガイドの提案**です。利用できるプラン・権限・組織設定は、各製品の公式の導入案内で確認してください。

---

## 1. head と base を先に区別する

`feature/review-rule` から `main` へマージする PR では、head は変更を提出する `feature/review-rule`、base は受け入れ先の `main` です。

| 用語 | この例での意味 | 確認する内容 |
|------|--------------|-------------|
| head | 変更を提出するブランチ | 新しいコードと、PR 内で変更された指示ファイル |
| base | マージ先のブランチ | マージ先で現在採用されているコードと指示ファイル |

ブランチ名だけでなく、**レビュー実行時点の commit SHA** を記録すると、後から追加 push があっても比較対象を追いやすくなります。

## 2. 公式に確認できる参照元

| 対象 | 提供元・状態 | 指示ファイルの参照元 | 適用範囲 |
|------|------------|--------------------|---------|
| GitHub.com 上の Copilot code review | Official | リポジトリの custom instructions・agent instructions・agent skills を **head** から読む | PR 内で変更した指示をマージ前に試せる（公式の例も同じ説明）。組織設定など、リポジトリ外の設定まで head から読むという意味ではない |
| Claude Code のマネージド Code Review | Official / research preview（Team・Enterprise） | v2.1.292 の修正告知では、PR が `CLAUDE.md` を編集するとき、その **base** 版を使う | この告知から、`REVIEW.md` やその他の関連ファイルの参照元まで一般化しない |

- **Copilot**: 「head branch（変更を含むブランチ）から読み、base branch からは読まない。`my-feature-branch` を `main` へマージするなら `my-feature-branch` の指示と skills を使うので、マージ前に同じ PR で試せる」と公式文書に注記があります。
- **Claude**: v2.1.292 の release に「PR が `CLAUDE.md` を編集すると、その規則が無視されていた問題を修正。base branch の版を使う」とあります。バージョン表記は修正の出典です。ローカルの CLI をその版へ更新することが、マネージドサービスの修正を受ける条件だとは示されていません。

### 同じ `CLAUDE.md` が、製品によって別の版で読まれる

Copilot code review は `.github/copilot-instructions.md`・`AGENTS.md`・`.github/instructions/**/*.instructions.md` に加えて、**`CLAUDE.md`・`GEMINI.md`・`REVIEW.md` も custom instructions として読みます**（公式文書に記載）。そのため、両方のレビューを有効にしたリポジトリで PR が `CLAUDE.md` を変更すると、次のようになり得ます。

| レビュー | 読む `CLAUDE.md` |
|---------|-----------------|
| Copilot code review | head（PR で変更した後の版） |
| Claude Code の Code Review | base（マージ先で採用済みの版） |

**2 つのレビューの指摘が食い違っても、片方の誤りとは限りません。** 読んだ基準の版が違う可能性を先に確認します。ほかのエージェント向けの指示ファイルが読まれる点は [プラグインの可搬性](plugin-portability.md#instruction-ファイルは別のエージェントにも読まれる) も参照してください。

### 実行場所をそろえて比べる

このページの head / base の比較は、**GitHub 上の PR レビュー**に限った話です。

- Copilot の custom instructions の対応は、GitHub.com と IDE で異なります（[環境別の対応表](https://docs.github.com/en/copilot/reference/custom-instructions-support)）。
- Claude Code のローカルの `/code-review` は、通常のセッションと同じく作業ツリーの `CLAUDE.md` に従い、マネージド Code Review 向けの `REVIEW.md` は**読みません**（[ローカルレビューが読む内容](https://code.claude.com/docs/en/code-review#what-the-review-reads-and-edits)）。
- 自前の GitHub Actions で AI レビューを動かす場合は、checkout する ref によって参照元が変わります。上の表をそのまま当てはめないでください。

## 3. レビュー基準を更新するときの手順

以下は、上の仕様から組み立てた運用上の提案です。

1. **変更の目的を書く。** 「誤検知を減らす」「新しい API の契約を確認する」など、追加・削除する規則と理由を PR 本文に書きます。
2. **基準の変更を独立して確認できる形にする。** できればルールの変更を別の PR にします。同時に変える必要があるなら、コード差分とルール差分の対応を説明し、人が両方を確認します。
3. **正常例と違反例を固定する。** 既存の正しいコードと、わざと規則を満たさない小さなサンプルを用意します。新旧の規則で、見逃しと誤検知の両方を比べます。
4. **製品の参照元に合わせて試す。**
   - head から読む製品（Copilot）: 試験用の PR で指示を変更して比べます。
   - base から読む `CLAUDE.md`（Claude Code Review）: 試験用のリポジトリやブランチに新旧の基準を用意し、**同じコード差分**をレビューできる構成にします。同じ PR で基準を変えても、その PR のレビューには新しい基準が使われません。
5. **採用後のレビュー実行を確かめる。** ルールを変更しただけで新しいレビューが済んだと思い込まず、対象の commit・実行日時・結果を確認します。

head から読む方式は、マージ前に新しい基準を試せます。その結果を採用の判断に使うときは、基準そのものの妥当性も人が確認します。base から読む方式は採用済みの基準を保てますが、新しい基準が同じ PR で反映されるとは限りません。**どちらの方式が安全か・精度が高いかは、ここからは判断できません。**

## 4. 小さな検証例

旧ルールを「新しい公開関数には説明文を付ける」、新ルールを「新しい公開関数には説明文と戻り値の説明を付ける」とします。**これは検証の設計例であり、実機で確認した結果ではありません。**

| ケース | コード側 | 指示側 | 確認すること |
|-------|---------|-------|-------------|
| A: 正常例 | 説明文と戻り値の説明がある関数を追加する | 旧・新それぞれ | 余計な指摘が出ないか |
| B: 違反例 | 説明文だけがある関数を追加する | 旧・新それぞれ | 新ルールでの不足を検出できるか |
| C: 同時変更 | B と同じ関数を追加する | 同じ PR で旧から新へ変更する | レビューが参照した版を、2 節の公式の説明・設定と照らし合わせる |

各ケースで次を残します。

- base / head の SHA
- 指示ファイルのパスと内容
- レビューの実行場所と設定（effort level など）
- 結果へのリンク

新旧を比べるときはコードの差分をそろえ、ルール以外の条件の変化を減らします。モデルの判断なので、1 回の結果で決めず、数回繰り返して揺れを見ます。

**指摘がなかったという結果だけでは、指示を読まなかったのか、読んでも検出できなかったのかを区別できません。** 参照元の確認と、レビュー品質の評価は分けて記録します。品質評価の設計は [Skill / エージェントの評価](evals.md#レビュー基準を変えたら新旧の版で同じ差分を比べる) を参照してください。

## 5. ルールの変更を誰が承認するか

指示ファイルの管理者を決め、必要なリポジトリでは **CODEOWNERS** と、code owner の承認を必須にする設定（branch protection の「Require review from Code Owners」または ruleset）を組み合わせます。**CODEOWNERS を置いただけではマージは制限されません。**

GitHub は、レビュー依頼を出す相手を決めるのに **base 側の CODEOWNERS** を使います（公式文書に記載）。採用済みの base 側で、実際に使っている指示ファイル・レビュー用の skills・CODEOWNERS 自身の所有者を決めておくと、変更の確認担当がはっきりします。

```text
# CODEOWNERS の例（説明用。パスとチーム名は架空）
/.github/copilot-instructions.md   @example-org/review-owners
/.github/instructions/             @example-org/review-owners
/.github/skills/code-review/       @example-org/review-owners
/AGENTS.md                         @example-org/review-owners
/CLAUDE.md                         @example-org/review-owners
/REVIEW.md                         @example-org/review-owners
/.github/CODEOWNERS                @example-org/repo-admins
```

基準を変える PR では、「何を新たに検出したいか」「どの指摘を減らしたいか」「正常例が通るか」を確認します。これを記録しておけば、後でレビューの傾向が変わったときに、**モデル・コード・基準のどれが変わったか**を調べやすくなります。

## 対象外

- 製品の安全性の順位付けや、公開されていない内部実装の推測は扱いません。
- Claude Code Review が `REVIEW.md` をどの版から読むかなど、今回の出典で確定できないことは断定しません。
- このリポジトリ自身の CODEOWNERS・保護ルールの変更は扱いません。
- 実測していない検出率は書きません。指示ファイルを読んだことと、指示に従ったことは同じではありません。

## 関連ドキュメント

- [GitHub Copilot ガイド — カスタマイズが効く場所](../copilot/README.md#カスタマイズが効く場所--レビューとエージェント) — code review の skills・MCP・effort level・API
- [Claude Code のカスタマイズ機能](../claude-code/basics.md#claudemd) — `CLAUDE.md` の配置と読み込み
- [Skill / エージェントの評価（evals）](evals.md) — 回帰評価と品質評価の設計
- [プラグインの可搬性](plugin-portability.md#instruction-ファイルは別のエージェントにも読まれる) — 別のエージェントにも読まれる instruction ファイル
- [Skill / Plugin のセキュリティ](skill-security.md) — 導入前の信頼と権限の確認

## 参考リンク

- [Using GitHub Copilot code review on GitHub](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review) — custom instructions・agent skills を head branch から読むこと、`CLAUDE.md`・`GEMINI.md`・`REVIEW.md` も読むこと（GitHub 公式）
- [Custom instructions support](https://docs.github.com/en/copilot/reference/custom-instructions-support) — 機能・環境ごとの対応表（GitHub 公式）
- [Claude Code v2.1.292](https://github.com/anthropics/claude-code/releases/tag/v2.1.292) — Code Review が PR で編集された `CLAUDE.md` の base 版を使う修正（Anthropic 公式・2026-10-06）
- [Code Review](https://code.claude.com/docs/en/code-review) — research preview の提供範囲、`CLAUDE.md` と `REVIEW.md` の役割、ローカルの `/code-review` が読む内容（Anthropic 公式）
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) — base branch の CODEOWNERS を使うこと、branch protection・ruleset との組み合わせ（GitHub 公式）
