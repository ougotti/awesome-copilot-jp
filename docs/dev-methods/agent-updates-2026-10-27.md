# 今週のエージェント動向 — 任せ続けるための承認・再開・画面操作

> **対象ツール**: GitHub Copilot / Claude Code / Codex・ChatGPT Work ｜ **実行環境**: CLI / IDE / Cloud / Chat UI ｜ **対象読者**: エージェントを開発・業務に使う人 ｜ **最終更新**: 2026-10-27

今週は、エージェントに仕事を任せた後の動作に関わる更新が出ています。Copilot は操作の許可をモデルが判断する assisted permissions を正式提供し、Claude Code はバックグラウンド実行や再開時の不具合を修正しました。OpenAI は画面の理解と操作を特徴に挙げる GPT-6.1 Terra を Work と Codex に追加しています。

これらを「任せ続けるための更新」と捉えるのは、各社の発表をもとにした本記事の見立てです。対象は **2026-10-26（月）〜10-27（火）時点**。前回の[最新動向](../trends.md)に含まれていなかった10-23公開の情報は、補足に分けました。一次資料は10-27に確認し、実機検証は行っていません。日付は公式発表の掲載日、GitHub release は UTC の公開日です。

## 今週の更新一覧

| 公開日 | 更新 | 提供元・状態 | 読者への影響 |
|---|---|---|---|
| 10-26 | Copilot assisted permissions | Official / GA | CLI・app・VS Code で操作をモデルが審査する。組織の `ask` が必ず人への確認になるとは限らない。 |
| 10-27 | Copilot CLI 1.0.104 | Official / GA | Assisted を experimental の有効化なしで使える。Autopilot の background task の待機動作にも変更。 |
| 10-26 | Claude Code 2.1.311 | Official / GA | subagent・MCP・worktree・会話の圧縮・再開に関わる修正。公開は21:51 UTCで、日本時間では10-27。 |
| 10-26 | GPT-6.1 Terra in Work and Codex | Official / GA（Work / Codex） | 画像・画面の理解と computer use を特徴に挙げるモデル。操作ツールの設定は別途必要。 |

## 1. Copilot — 承認をモデルに任せる範囲が正式な選択肢に

10-26、GitHub は CLI・Copilot app・VS Code の **assisted permissions を GA** にしました。コマンド実行、ファイルパスへのアクセス、URL の取得などについて、モデルが安全と判断した対象の要求を自動で許可し、判断がつかないものは人に確認します。CLI の対話中は `/permissions` から選べます。[公式発表](https://github.blog/changelog/2026-10-26-github-copilot-assisted-permissions-generally-available/)

公式 docs によると、CLI のコマンド・ファイル読み書き・URL に対する enterprise の **`ask` ルールも、審査対象ならモデルの許可で満たせます**。deny は維持され、sandbox の迂回要求などは審査対象に入りません。Autopilot や非対話実行では、人の承認がなお必要な要求は拒否されます。モデルによる判断は sandbox やアクセス制限の代わりにはなりません。[承認の仕組み](https://docs.github.com/en/copilot/concepts/customizations/allowing-safe-commands)

チームで人の確認を残したい操作がある場合は、適用されるルールを確認する必要があります。管理者は Allow All を禁止したまま Assisted を使わせることも、Assisted を個別に無効化することもできます。[管理者向けの説明](https://github.blog/changelog/2026-10-26-github-copilot-assisted-permissions-generally-available/)

10-27の **CLI 1.0.104** は Assisted を experimental の有効化なしで使えるようにしました。また、interactive / SDK の Autopilot は、接続された background task を `COPILOT_TASK_WAIT_TIMEOUT_SECONDS` の経過後も待ち続けます。一方、**`-p --autopilot` は引き続きそのタイムアウトに従います**。対話で成功した仕事をバッチへ移す際に影響する違いです。[1.0.104 release](https://github.com/github/copilot-cli/releases/tag/v1.0.104)

## 2. Claude Code — 長い仕事の途中と、再開した後を修正

**2.1.311** には、複数のエージェントや外部ツールを使って仕事を続ける際の修正が入っています。

| 場面 | release note に記載された修正 |
|---|---|
| MCP の接続 | subagent 開始後に接続を終えた server のツールを、subagent が使えない問題を修正。 |
| worktree の寿命 | 子の background subagent が作業中なのに、隔離 worktree が削除される問題を修正。 |
| 会話の自動圧縮 | session 中に編集した `MEMORY.md` / `CLAUDE.md` の古い内容を見る問題を修正。 |
| session の再起動 | 終了済みの `/code-review` など subagent で動く Skill が、cloud / background session の再起動で再実行される問題を修正。 |
| 終了 hook | `SubagentStop` hook が subagent の実行中に繰り返し走る問題を修正。 |

出典: [Claude Code 2.1.311 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.311)。

これらは、既に任せている仕事が最後まで続くかを左右する修正です。自分の運用で影響を確認するなら、「親の終了後も子が動く仕事」「指示を変えた後に圧縮する会話」「完了後に再開する仕事」を小さな例で試すとよいでしょう。これは本記事からの検証提案です。外部書き込みの重複を防ぐ設計は、[長時間タスクの信頼性設計](agent-reliability.md)を参照してください。

## 3. Work・Codex — 画面を読んで操作するモデルの追加

OpenAI は10-26、**GPT-6.1 Terra を ChatGPT Work と Codex に提供開始**しました。公式更新は画像理解と computer use を特徴に挙げています。Work ではモデル一覧の Advanced から選択でき、Chat では利用できません。Enterprise でのアクセスは workspace の提供状況と管理者の制御に依存します。[公式更新](https://developers.openai.com/codex/changelog/#codex-2026-10-26-gpt-61-terra)、[モデルの案内](https://learn.chatgpt.com/docs/models?surface=app)

画面操作を試す際は、モデルの選択に加え、[Browser](https://learn.chatgpt.com/docs/browser) や [Computer Use](https://learn.chatgpt.com/docs/computer-use) の設定とアクセス条件を確認してください。本記事では操作精度や他モデルに対する優劣は検証していません。外部操作の手段は、[ツールの選び方](tool-selection.md)で比較できます。

## 前週からの補足 — 入口と利用状況も変わる

次の情報は10-23公開です。今週の新規発表と区別して、任せ方に関わる変更を補います。

| 更新 | 提供元・状態 | 何が変わるか・確認点 |
|---|---|---|
| [Copilot in Teams の通知と会話の統合](https://github.blog/changelog/2026-10-23-turn-notifications-into-code-with-github-copilot-in-teams/) | Official / Improvement | 通知から `@GitHub` に調査・修正・PR 作成を頼める。人がレビュー・テスト・マージする導線。旧 GitHub app は11-16に終了予定で、統合された app への移行が必要。 |
| [利用指標の `totals_by_client`](https://github.blog/changelog/2026-10-23-usage-metrics-api-adds-usage-from-tools-like-opencode/) | Official / Improvement | OpenCode など、Copilot をモデル提供元として使うツールの request・session・token を集計する。`request_count` はモデル呼び出し数で、指示した回数や完了した仕事数ではない。client は best-effort の分類で、検証済みの ID ではない。 |
| [Claude Code 2.1.310](https://github.com/anthropics/claude-code/releases/tag/v2.1.310) | Official / GA | Monitor tool と plugin monitors を Bedrock・Vertex・Foundry、telemetry / nonessential traffic 無効時にも拡大。Windows で Git Bash がなく hook のコマンドが引用文字列だけの場合に、ツール実行を通してしまう問題も修正。 |

Teams の更新は「仕事を頼む入口」、利用指標は「どのツールがモデルを使ったか」を広げます。利用量と成果を分けて見る方法は、[AI 導入の効果の測り方](ai-adoption-metrics.md)にまとめています。

## 自分の運用では何から確かめるか

| 現在の使い方 | 最初に確かめること |
|---|---|
| Copilot で手動承認が多い | Assisted に任せたい操作と、人の確認を残したい操作を分け、組織のルールとの関係を確認する。 |
| Autopilot をバッチに移したい | interactive / SDK と `-p --autopilot` の待機時間の違いを確認する。 |
| Claude Code で子エージェントや定期作業を使う | 修正版で worktree の寿命・圧縮後の指示・再開時の重複を確認する。 |
| ブラウザやデスクトップの仕事を頼みたい | Terra の利用可否と操作ツールの接続を確認し、小さな作業の結果から評価する。 |

承認画面の回数や稼働時間に加えて、**頼んだ結果が正しく得られたか**を記録すると、自分の仕事で任せられる範囲を判断しやすくなります。
