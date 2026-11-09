# 今週のエージェント動向 — 使う段階から、更新・再開・改善を管理する段階へ

> **対象ツール**: GitHub Copilot / Claude Code・Claude API / Codex / Amazon WorkSpaces ｜ **実行環境**: CLI / IDE / Cloud ｜ **対象読者**: エージェントを継続して使う開発者・運用担当者 ｜ **最終更新**: 2026-11-04

エージェントに一度仕事を頼めるようになると、次は「同じ仕事を明日も任せられるか」が問題になります。Skill の依存先が変わる、会話が途切れる、クラウドに作業を移す、利用量の集計先が変わる。こうした変化も、継続して使うために扱う必要があります。

2026-10-29〜11-04の更新では、依存関係の更新を PR にする Dependabot の APM 対応、会話の送信量を減らす Claude API の Message threads、再開時の不具合を直す CLI の release が出ました。本記事はこれらを、**「エージェントを使う段階から、更新・再開・改善を管理する段階へ」**という切り口でつなぎます。これは各社が共同で掲げた方針ではなく、本記事の見立てです。

一次資料の確認日は **2026-11-04** です。公開日は公式 changelog の掲載日、CLI は正式 release の日付で記載します。製品・API・管理画面での実機検証は行っていません。10-28の GitHub Universe の発表は期間外の背景として扱い、詳しい説明は既存の[チームで常設するエージェント](team-automations.md)へ集約しています。

## 自分の運用に関係する更新を選ぶ

| 現在の使い方 | 最初に読む節 |
|---|---|
| Skill・prompt・instructions を外部から取り込んでいる | [1. 更新をレビューできる形にする](#1-更新をレビューできる形にする) |
| 長い会話・無人実行・再開を使っている | [2. 再開できることを確かめる](#2-再開できることを確かめる) |
| 複数の実行環境やモデル提供元を使っている | [3. 実行場所と費用の集計先を追う](#3-実行場所と費用の集計先を追う) |
| 定期作業の結果から改善したい | [4. 改善案を受け入れる判断を残す](#4-改善案を受け入れる判断を残す) |

## 対象期間の更新一覧

| 公開日 | 更新・一次資料 | 提供元・状態 | 何が変わるか |
|---|---|---|---|
| 10-29 | [Codex CLI 0.166.0](https://developers.openai.com/codex/changelog/#github-release-428320524) | Official / GA（正式 release） | `codex queue --resume`、`codex doctor --network-only` を追加。再開・分岐時の承認設定とトークン集計などを修正。 |
| 11-02 | [Claude API の Message threads](https://platform.claude.com/docs/en/release-notes/overview) | Official / Preview（Beta） | 会話を短時間サーバー側で保持し、次の要求では新しいメッセージだけを送れる。 |
| 11-03 | [Dependabot の APM 対応](https://github.blog/changelog/2026-11-03-dependabot-version-updates-support-agent-package-manager/) | Official / GA | `apm.yml` の対応する Git 依存関係を更新する PR を作成。既存の `apm.lock.yaml` も再生成する。 |
| 11-03 | [Copilot の BYOK 利用指標](https://github.blog/changelog/2026-11-03-byok-and-enterprise-custom-models-in-the-copilot-usage-api/) | Official / GA（利用指標の拡張） | ローカルの BYOK と企業が設定した独自モデルを、Copilot 提供モデルの利用と分けて把握できる。 |
| 11-03 | [Copilot in JetBrains Air](https://github.blog/changelog/2026-11-03-github-copilot-is-now-available-in-jetbrains-air/) | Official / GA（連携の提供開始） | ACP 経由で IDE 内またはクラウドへ作業を委任し、結果をレビューできる。 |
| 11-03 | [AI agents 向け WorkSpaces の Linux・Windows 11 対応](https://aws.amazon.com/about-aws/whats-new/2026/11/workspaces-ai-agents-linux-windows-11/) | Official / GA（対応 OS の拡張） | Windows Server に加え、開発作業や業務アプリに合うデスクトップを選べる。 |
| 11-04 | [Claude Code 2.1.318](https://github.com/anthropics/claude-code/releases/tag/v2.1.318) | Official / GA（正式 release） | 共有ホームの設定保存、再起動後の作業フォルダ、workflow 再開時の重複実行などを修正。 |

## 1. 更新をレビューできる形にする

Dependabot の APM 対応によって、AI agent の Skill・prompt・instructions の依存関係も、更新 PR で扱えるようになりました。github.com の全プランで GA です。対象は `apm.yml` に宣言した対応する Git 依存関係で、**バージョン更新への対応**です。セキュリティ更新への対応ではありません。

設定の入口は `.github/dependabot.yml` です。`apm` の設定、`apm.yml` があるディレクトリ、更新頻度を指定します。対応する依存先と手順は[公式の案内](https://github.blog/changelog/2026-11-03-dependabot-version-updates-support-agent-package-manager/)を参照してください。APM 自体の役割は[最新動向の APM 解説](../trends.md#7-4-apm--宣言でチームの環境を再現する)で解説しています。

ここからは本記事の提案です。更新 PR をレビューするときは、バージョン番号とともに、**エージェントが読む手順や呼び出すツールがどう変わったか**を見ます。導入済みの Skill に小さな代表タスクを用意し、更新前後の結果を比べると、変更を受け入れる根拠が残ります。評価の作り方は[evals](evals.md)、配布元と内容の確認は[Skill / Plugin のセキュリティ](skill-security.md)へまとめています。

## 2. 再開できることを確かめる

Claude API の **Message threads は Beta** です。会話全体を毎回送り直す代わりに、最初に会話・指示・ツールを送り、以後は新しいメッセージと前の応答の ID を送ります。長い agent loop で要求サイズと最初のトークンまでの待ち時間を減らす仕組みです。

ただし thread は、最後の要求から **5分で期限切れ**となり、最終利用から1時間以内に削除されます。アプリケーション側が会話の正本を保持し、続行できない場合は履歴を再送して作り直す必要があります。SDK の helper の履歴もメモリ内にあるため、プロセス終了をまたぐ保存は別途必要です。ZDR・HIPAA の対象外である点を含め、利用条件は[Message threads の仕様](https://platform.claude.com/docs/en/build-with-claude/message-threads)で確認してください。

CLI 側でも、続行時の状態が修正されています。

| ツール | 今回確認した修正 | 本記事が提案する確認例 |
|---|---|---|
| Codex CLI 0.166.0 | 再開・分岐時に承認済みの approval / permission 設定を保持。推論トークン集計を保ち、早すぎる会話圧縮を防ぐ。 | 小さな作業を再開・分岐し、設定と会話の継続を確認する。 |
| Claude Code 2.1.318 | cloud / self-hosted runner の再起動後に承認したコマンドが、要求時と異なる開始フォルダで実行される問題を修正。移動できない場合は実行しない。 | 作業フォルダを変えた後の再開で、実行先を確認する。 |
| Claude Code 2.1.318 | 利用上限後に workflow を再開すると終了済み agent が再実行される問題や、共有ネットワークホームで設定・認証情報を保存する問題を修正。 | 終了済み処理の実行記録と、設定の保存結果を確認する。 |

出典は一覧の正式 release です。修正の掲載は、自分の外部サービスへの書き込みまで重複しないことの証明にはなりません。仕事の完了記録や冪等性の設計は、[長時間タスクの信頼性設計](agent-reliability.md)を参照してください。

## 3. 実行場所と費用の集計先を追う

Copilot in JetBrains Air は、既存の Copilot 契約を使って作業を実行します。クラウド実行には Air Teams を利用できる組織と管理者の有効化などが必要です。実行環境は新しい VM 上の Docker container で、**タスク間で状態を引き継ぎません**。また、Air の利用分析には Copilot 使用量が含まれず、Air 内で Copilot の支出上限を設定することもできません。[公式の前提条件と制約](https://github.blog/changelog/2026-11-03-github-copilot-is-now-available-in-jetbrains-air/)。

WorkSpaces の追加 OS 対応は、エージェントが使うアプリに合わせて環境を選ぶ更新です。Linux では root access を使った開発・テスト・スクリプト実行、Windows 11 では業務アプリの操作が想定されています。Windows Server と同様に IAM・ネットワーク隔離などの管理を引き継ぎます。[AWS の発表](https://aws.amazon.com/about-aws/whats-new/2026/11/workspaces-ai-agents-linux-windows-11/)

費用の把握にも更新があります。Copilot usage metrics API は、開発者が設定するローカルの BYOK と、管理者が設定する企業独自モデルを区別できるようになりました。ただし、集計経路には違いがあります。

| 利用形態 | 集計の性質 |
|---|---|
| ローカルの BYOK・ローカルモデル | client telemetry に依存。telemetry 無効時やトークン数を返さない provider では過少集計になる。 |
| 企業が設定した独自モデル | GitHub を通る要求をサーバー側で観測。`totals_by_client` 内で識別する。 |

出典: [BYOK の利用指標](https://github.blog/changelog/2026-11-03-byok-and-enterprise-custom-models-in-the-copilot-usage-api/)。既存の総計に利用が追加されるのではなく、既に含まれる利用を区別する更新です。利用指標を足し合わせるときは二重計上を避け、費用の判断には[エージェントの費用管理](agent-costs.md)も参照してください。

## 4. 改善案を受け入れる判断を残す

期間直前の10-28には、Copilot Automations が実行結果から prompt・tool・trigger の改善を提案する更新がありました。提案は適用前に人が確認します。[公式発表](https://github.blog/changelog/2026-10-28-copilot-automations-now-learn-from-outcomes-and-self-improve/)

この改善を、依存関係の更新や再開の検証とつなげることが、本記事の提案です。変更の入口が Dependabot の PR でも、automation からの改善案でも、**変更前後で何が良くなったかを確認する担当者と材料**が必要になります。常設する仕組みの名義・費用・起動条件、Agent Merge と Agentic Workflows の選び方は、既存の[チームで常設するエージェント](team-automations.md)にまとめています。

| 管理するもの | 残すと役立つ記録（本記事の提案） |
|---|---|
| Skill の更新 | 依存先の revision、手順の差分、代表タスクの更新前後の結果。 |
| 会話・処理の再開 | 会話の保存先、終了済み処理、再開時のフォルダ・権限、外部書き込みの識別子。 |
| 実行環境と費用 | 実行場所、課金先、使ったモデル提供元、指標に含まれない利用。 |
| 改善案 | 変更内容、比較した結果、受け入れた理由、戻す方法。 |

前回の[週次記事](agent-updates-2026-10-27.md)で扱った「任せ続けるための承認・再開・画面操作」に、今回は更新と改善の記録が加わります。まず自分が繰り返し任せる仕事を一つ選び、この表の記録を残すところから始められます。
