# Agentic Workflow: 自動マージ（automerge）

## 目的

`automerge` ラベルが付いたPull Requestに対し、
全CIチェック（lint・build・test）が成功した場合に自動でsquashマージする。
人手によるマージ操作を不要にする。

## トリガー

- Pull Requestにラベルが付与されたとき（`labeled`）
- `CI` ワークフローが完了したとき（`workflow_run: completed`）

どちらのイベントが先に発生しても、両条件が揃った時点で自動マージが実行される。

## 実行内容

### labeled イベントの場合

1. 付与されたラベルが `automerge` でなければ何もしない
2. 該当PRのCI結果を確認する（後述の手順3以降へ）

### workflow_run 完了イベントの場合

1. CIの結論が `success` でなければ何もしない
2. CIのHEAD SHAに対応するオープン中のPRを検索する
3. PRが見つからなければ何もしない

### 共通：マージ判定

1. PRに `automerge` ラベルが付いていなければスキップする
2. 必須チェック（`lint`・`build`・`test`）の全てが `completed` かつ `success` か確認する
3. いずれかのチェックが未完了または失敗していればスキップする
4. 全チェックが成功していればsquashマージを実行する

## 必要な権限

- `contents: write`（マージに必要）
- `pull-requests: write`（マージAPIに必要）
- `checks: read`（CIチェック結果の参照に必要）

## コンパイル済みファイル

このファイルをコンパイルすると `.github/workflows/auto-merge.yml` が生成される。

```yaml
name: 自動マージ（automerge）

on:
  pull_request:
    types:
      - labeled
  workflow_run:
    workflows:
      - CI
    types:
      - completed

jobs:
  auto-merge:
    name: CIパスかつautomergeラベルのPRを自動マージ
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      checks: read

    steps:
      - name: 自動マージ処理
        uses: actions/github-script@v7
        with:
          script: |
            let prNumber = null;

            if (context.eventName === 'pull_request') {
              // labeled イベント：automerge ラベルが追加された場合
              if (context.payload.label.name !== 'automerge') {
                console.log('automerge ラベル以外のためスキップします。');
                return;
              }
              prNumber = context.payload.pull_request.number;
            } else if (context.eventName === 'workflow_run') {
              // CI 完了イベント：該当 PR を特定する
              const run = context.payload.workflow_run;
              if (run.conclusion !== 'success') {
                console.log(`CI が成功していません（${run.conclusion}）。スキップします。`);
                return;
              }

              const headSha = run.head_sha;
              const { data: prs } = await github.rest.pulls.list({
                owner: context.repo.owner,
                repo: context.repo.repo,
                state: 'open',
                per_page: 100,
              });

              const matchedPr = prs.find(pr => pr.head.sha === headSha);
              if (!matchedPr) {
                console.log('対応するオープンPRが見つかりませんでした。');
                return;
              }
              prNumber = matchedPr.number;
            }

            if (prNumber === null) {
              console.log('PR番号を特定できませんでした。スキップします。');
              return;
            }

            // PR 情報を取得
            const { data: pr } = await github.rest.pulls.get({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: prNumber,
            });

            // automerge ラベルを確認
            const labels = pr.labels.map(l => l.name);
            if (!labels.includes('automerge')) {
              console.log(`PR #${prNumber} には automerge ラベルがありません。スキップします。`);
              return;
            }

            // CI ステータスを確認
            const { data: checks } = await github.rest.checks.listForRef({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: pr.head.sha,
            });

            const requiredChecks = ['lint', 'build', 'test'];
            const checkRuns = checks.check_runs;

            for (const required of requiredChecks) {
              const run = checkRuns.find(r => r.name === required);
              if (!run) {
                console.log(`必須チェック "${required}" が見つかりません。スキップします。`);
                return;
              }
              if (run.status !== 'completed' || run.conclusion !== 'success') {
                console.log(`チェック "${required}" が成功していません（status: ${run.status}, conclusion: ${run.conclusion}）。`);
                return;
              }
            }

            console.log(`PR #${prNumber} の全CIチェックが成功しました。自動マージを実行します。`);

            await github.rest.pulls.merge({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: prNumber,
              merge_method: 'squash',
            });

            console.log(`PR #${prNumber} を自動マージしました。`);
```
