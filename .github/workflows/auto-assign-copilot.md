# Agentic Workflow: Issue自動割り当て（Copilot）

## 目的

軽微な更新に関するIssueを検知し、GitHub Copilot coding agent（`@copilot`）を
自動で担当者に割り当てることで、人手による作業割り当てを不要にする。

## トリガー

- Issueが新規作成されたとき（`opened`）
- Issueにラベルが付与されたとき（`labeled`）

## 判定条件

以下のいずれかを満たすIssueを対象とする：

- タイトルに `[更新通知]` を含む
- ラベル `update` が付いている
- ラベル `maintenance` が付いている

いずれの条件も満たさない場合は何もしない。

## 実行内容

1. Issueのタイトルとラベルを確認する
2. 上記の判定条件を満たしていれば、`copilot` をassigneeとして追加する
3. 割り当て結果をログに出力する

## 必要な権限

- `issues: write`（assigneeの追加に必要）

## コンパイル済みファイル

このファイルをコンパイルすると `.github/workflows/auto-assign-copilot.yml` が生成される。

```yaml
name: Issue自動割り当て（Copilot）

on:
  issues:
    types:
      - opened
      - labeled

jobs:
  auto-assign:
    name: 軽微な更新IssueをCopilotに割り当て
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - name: 条件確認・Copilot割り当て
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const title = issue.title || '';
            const labels = issue.labels.map(l => l.name);

            const isTitleMatch = title.includes('[更新通知]');
            const isLabelMatch = labels.includes('update') || labels.includes('maintenance');

            if (!isTitleMatch && !isLabelMatch) {
              console.log('条件不一致のためスキップします。');
              console.log(`タイトル: ${title}`);
              console.log(`ラベル: ${labels.join(', ')}`);
              return;
            }

            console.log('条件一致：@copilot を assignee に追加します。');

            await github.rest.issues.addAssignees({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              assignees: ['copilot'],
            });

            console.log(`Issue #${issue.number} に copilot を割り当てました。`);
```
