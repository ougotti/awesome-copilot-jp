# ループエンジニアリング

> **対象ツール**: ツール横断（Claude Code・Codex 等） ｜ **実行環境**: CLI / デスクトップ / Cloud ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-12

> エージェントに毎ターン指示を出す代わりに、**エージェントに指示を出し続ける「ループ」の側を設計する**実践を **ループエンジニアリング（loop engineering）** と呼びます。2026-06-07 に Addy Osmani（Google Chrome）が [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) で命名しました。このページは概念、ループの構成要素、停止条件の作り方、そして落とし穴をまとめた解説です。ループが動く土台については [AI エージェントの実行基盤（ハーネス）](harness.md) を参照してください。

---

## 使いどころの判断

ループは「常に良い」ものではありません。まず、目の前の作業が向いているかを判断してください。

| 状況 | 向き / 不向き |
|------|--------------|
| 完了条件を機械が判定できる（テストが通る・指標がしきい値を超える） | **向いている** |
| 同じ手順を定期的に繰り返す（Issue のトリアージ、依存の更新、リンク切れ点検） | **向いている** |
| 作業を小さく区切れて、1 回の実行が短い | **向いている** |
| 完了条件が主観的（「デザインを良くする」「読みやすくする」） | 不向き。人が判断する |
| 設計方針そのものを決める、前例のない仕様を作る | 不向き。人が判断する |
| 失敗したときの影響が大きく、巻き戻せない（本番反映・外部への送信） | 不向き。ループの外に承認を置く |

---

## 何が変わるのか

従来のやり方では、人がプロンプトを書き、結果を見て、次のプロンプトを書きます。この「次を促す役」を人が担い続ける限り、進む速度は人が画面の前にいる時間で決まります。

ループエンジニアリングは、この役割をシステムへ渡します。人は**目的と停止条件**を定義し、ループが発見・実行・検証・次の判断を繰り返します。原典が引用する 2 つの発言が、変化の中身を端的に示しています。

> You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents.
> — Peter Steinberger

> I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops.
> — Boris Cherny（Anthropic, Claude Code）

注意すべきは、**これは「簡単になる」話ではない**ことです。プロンプトの巧拙よりも、停止条件の定義・検証の分離・状態の持ち方といった設計判断が問われます。

---

## 用語の階層

「プロンプト」「コンテキスト」「ハーネス」「ループ」は、対立する流派ではなく**層**です。下の層が弱いまま上の層を積むと、ループは誤りを増幅します。

| 層 | 設計する対象 | 本ガイドの該当ページ |
|----|-------------|--------------------|
| プロンプトエンジニアリング | モデルに送る言葉 | — |
| コンテキストエンジニアリング | モデルが見る情報一式（コード・文書・履歴・メモリ） | [Skills 最新動向](../trends.md) |
| ハーネスエンジニアリング | エージェントが動く環境（ツール・権限・サンドボックス・観測） | [AI エージェントの実行基盤（ハーネス）](harness.md) |
| **ループエンジニアリング** | エージェントを目標へ向けて回す反復サイクル | 本ページ |

Osmani はループエンジニアリングをハーネスエンジニアリングの「one floor above（1 つ上の階）」と位置づけています。ハーネスが弱ければ、ループはその弱点を繰り返し踏むだけになります。

---

## ループの構成要素

原典が挙げる 5 つの部品と、それを支える外部状態です。

| 要素 | 役割 | ないとどうなるか |
|------|------|----------------|
| **自動実行（automations）** | 発見・トリアージを定期的に起動する | 人が起動する限り「ループ」にならない |
| **ワークツリー（worktrees）** | 並列作業を隔離した作業コピーで動かす | 複数のエージェントが同じファイルを奪い合う |
| **スキル（skills）** | プロジェクト知識を `SKILL.md` に固定する | 毎回同じ前提を説明し直すことになる |
| **プラグイン / コネクタ** | MCP で Issue トラッカー・DB・Slack 等につなぐ | ループが現実の作業対象に触れられない |
| **サブエージェント** | 検証役を実行役と分ける | モデルが自分の答案を自分で採点する |
| **外部状態** | 進捗・次の一手を Markdown やボードに残す（実装例: [GBrain](ontology.md#形式的な定義を作らない選択肢--gbrain)） | 実行のたびに文脈が失われ、同じ作業を繰り返す |

外部状態は「置き場所を決めるだけ」に見えて、無人で回すほど効いてきます。ループが 1 周するたびに得た判断を残せなければ、次の周回は同じ調査をやり直します。Markdown ファイルやボードで足りることも多く、**エージェントが読み書きできる形**であることのほうが、道具の高機能さより重要です。

検証役を分ける点は特に重要です。実装したエージェント自身に「できたか」を判定させると、**作った側が採点する**構図になります。作る役（maker）と確かめる役（checker）を分けてください。

---

## ループの型

[Practical Loop Engineering](https://addyosmani.com/blog/practical-loop-engineering/)（2026-08-14）は、ループを 4 つに整理しています。

| 型 | 起動のしかた | 例 |
|----|------------|-----|
| ターン型 | 人が 1 手ずつ進める | 通常の対話。ループの前段階 |
| 目標型 | 条件が満たされるまで反復する | 「ローカルのテストが全部通るまで直す」 |
| 時間型 | 一定間隔で起動する | 「24 時間ごとに新しい Issue を確認する」 |
| 能動型 | イベント／スケジュールで起動し、その場に人がいない | 「`bug` ラベルの Issue が付いたら修正案を作る」 |

組み合わせると、たとえば「24 時間ごとに `bug` ラベルの Issue を確認し、あれば目標型ループでテストが通るまで修正する」という形になります。

### 製品機能としての起動条件 — Codex の Scheduled tasks

時間型・能動型の起動は、自分でスケジューラを組まなくても製品側で用意されています。Codex の [Scheduled tasks](../codex/README.md#6-定期イベントで動かすscheduled-tasks) は、時刻ベースの繰り返しに加えて **Gmail・Slack・GitHub のイベント**を起点にできます。**1 タスクで複数のイベントトリガーは使えますが、イベントトリガーと時刻ベースのスケジュールは併用できません。**

ここで役割を分けて考えると設計が楽になります — **Skill が手順の定義**、**Plugin が外部接続**、**Scheduled task が起動条件**、**worktree やサンドボックスが実行境界**です。ループの部品をどこに置くかの目安になります。

### IDE で保存して回す — VS Code Automations

VS Code 1.137（2026-09-09）の **Automations**（Preview）は、保存した prompt、workspace、agent / model / permission options、schedule からエージェントタスクを起動します。`chat.automations.enabled` を有効にし、Agents ウィンドウの Automations から作成します。スケジュールは Manual / Hourly / Daily / Weekly です。

公式手順が最初の schedule を **Manual** にするのは、無人実行へ移る前に同じ構成で `Run now` を試すためです。初回の History で応答、変更、承認要求、消費量を確認してから繰り返しを有効にします。Git workspace では、選んだ agent が分離に対応していれば New Worktree と基準ブランチを指定できます。

ローカル実行の条件も設計に含めてください。Agent Host を使うスケジュールには Agent Host process、それ以外には VS Code のウィンドウが必要で、マシンを起動したままにします。中断後は catch-up run が起きる場合がありますが、逃した回がすべて再実行される保証はありません。同じ Automation は一度に 1 セッションだけ実行し、次の時刻が来ても並列には開始しません。

保存時に選んだ権限でファイル読み取り・コマンド・変更を実行できますが、**保存しても組織ポリシーは迂回されず、将来の実行で承認が必要になる場合があります**。無人化する前に、承認が残る操作を prompt から分離してください。

### OSS 側の起動条件 — Kiro Crew

同じ「起動条件を製品側に持たせる」形は OSS でも出てきました。AWS が 2026-08-04 に Apache-2.0 で公開した [Kiro Crew](harness.md#kiro-crew--常駐して動き続けるハーネス) は、常駐したまま次の 3 つで起動します。

| 型 | Kiro Crew での実装 |
|----|------------------|
| 時間型 | タイムゾーンを解釈する定期ジョブ。結果は指定した面（Web ダッシュボード・Slack 等のチャネル）へ届く |
| 能動型 | 認証済み webhook とメッセージイベント |
| 能動型（監視） | ハートビート。作業が終わるか、人の判断が要る状態になるまで見張り続ける |

Codex の Scheduled tasks との違いは 2 点です。**起動条件の実装を読める**こと、そして**エージェントの側が終わらない**ことです。Scheduled tasks は起動のたびにタスクを立てますが、Kiro Crew は常駐したセッションが起動条件を受け取り、メモリと過去のセッションを引き継ぎます。

長時間タスクは計画・実行・検証・失敗時の再試行までツール側が回すため、**[停止条件](#停止条件の作り方)を渡す側で決めておく必要はむしろ大きくなります**。「終わるまで」ではなく、機械が判定できる条件と上限を仕様に書いてください。

> 本体は無償の OSS ですが、**動かすには Kiro のプランが必要**です（エージェントの利用は Kiro アカウントの枠を消費します）。

### 定期実行を選ぶときの比較

同じ「automation」や「schedule」という名前でも、常駐場所と状態の寿命が違います。特に VS Code Automations はローカル IDE の Preview 機能であり、クラウドのジョブ基盤ではありません。

| 観点 | VS Code Automations | Codex Scheduled tasks | Claude Code `/loop` | Kiro Crew |
|------|---------------------|-----------------------|---------------------|-----------|
| 主な起動条件 | Manual / Hourly / Daily / Weekly | 時刻、または Gmail / Slack / GitHub のイベント | 固定間隔、またはセッション中に選ぶ間隔 | 定期ジョブ、webhook、メッセージ、heartbeat |
| 実行場所 | ローカルの Agent Host process または VS Code window | デスクトップのローカル実行、または提供面に応じた実行先 | 開いているローカルセッション | 常駐する Kiro Crew 実行環境 |
| workspace / 分離 | workspace なしも可。対応 agent は New Worktree を選べる | ローカルでは作業中 checkout / Git worktree を選べる | 現在のセッションと作業ディレクトリを継承 | エージェントごとの workspace と sandbox 強度を設計する |
| 権限・承認 | session configuration を保存。組織ポリシーは迂回せず、run ごとに承認が残り得る | タスクの実行環境・サンドボックス・承認設定に従う | 現在のセッションの権限を継承 | standard / strict / off の分離と audit を運用者が設定する |
| 停止・重複実行 | disable は次回以降だけ。実行中は History から Stop。同一 Automation は直列 | 各起動でタスクを作る。重複時の扱いは対象面の現行仕様を確認する | `Esc` または task の削除。busy 中は turn 後に 1 回実行し、取り逃した回を全 replay しない | heartbeat / task の終了条件と上限を仕様に置く |

選択の基準は単純です。IDE の作業構成をそのまま定期化するなら VS Code、時刻だけでなく外部イベントも入口にするなら Codex、開いている会話内の短い監視なら `/loop`、セッションを越えて常駐しメモリやチャネルを持たせるなら Kiro Crew が候補になります。どれを使う場合も、[停止条件](#停止条件の作り方)と影響の大きい操作の承認を先に決めます。

### 実行した知識を次の周回へ戻す — Runme + WebMCP

OpenAI が公開している Codex の事例は、**無人実行そのものより「実行で得た知識を次回へ戻すこと」に価値を置いた**ループです。Runme のノートブックを軸に、次の順で回ります。

1. ノートブックに目的と過去の文脈を置く
2. Codex が計画を書き、**人が承認するまで実行を待つ**
3. 実行したコマンド・出力・解釈・失敗した経路を同じノートブックに残す
4. 生成された索引ファイル経由で、共有・検索できるようにする
5. 次回の実行が、前回の判断と結果を再利用する

技術的な要は **WebMCP** です。静的なクライアントサイドの Web アプリが、**専用の MCP サーバーを立てずに**ブラウザ側の限定されたツールをエージェントへ公開できます。

この事例が示すのは、[外部状態](#ループの構成要素)と[承認境界](#落とし穴)を両立させる形です。人は「計画が実行に足るか」と「結果を出荷してよいか」を判断し、繰り返しの実行と記録はループが担います。

---

## 停止条件の作り方

ループの品質は、ほぼ停止条件で決まります。**機械が真偽を判定できる条件**にしてください。

| 良い停止条件 | 悪い停止条件 |
|-------------|-------------|
| 対象のテストがすべて通る | 「ちゃんと動くようにする」 |
| Lighthouse スコアが 92 以上になる | 「表示を速くする」 |
| 連続する 2 ターンで改善が出ない（打ち切り） | 上限なしで「良くなるまで」 |
| コントリビューションガイドの違反が 0 件 | 「レビューで通りそうな状態」 |

同じコマンドを結果が変わらないまま繰り返している場合、そのループは進んでいません。**回数・時間・コストの上限**も併せて決めてください。

---

## 実践の入口（Claude Code の場合）

Claude Code には、ループを組むための機能がひととおり揃っています。詳細は公式リファレンスを一次情報として確認してください。

| やること | 使うもの |
|---------|---------|
| 条件が満たされるまで作業を続けさせる | `/goal`（[Commands](https://code.claude.com/docs/en/commands) / [Goal](https://code.claude.com/docs/en/goal)） |
| プロンプトを一定間隔で繰り返す | `/loop`（[Commands](https://code.claude.com/docs/en/commands) / [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks)） |
| プロジェクト知識を固定する | `SKILL.md`（[Claude Code のカスタマイズ機能](../claude-code/basics.md)） |
| 外部ツールへつなぐ | [MCP サーバー](../claude-code/basics.md#mcpmodel-context-protocol統合) ／ [プラグイン](../claude-code/basics.md#プラグイン) |
| 検証役を分ける | サブエージェント |

コマンド一覧のスナップショットは [Claude Code コマンド一覧](../claude-code/commands.md) にありますが、この領域は更新が速いため、実際に使えるものはセッション中の `/help` で確認するのが確実です。

---

## 落とし穴

原典が挙げる 3 つは、どれも「速くなった代償」として現れます。

| 落とし穴 | 内容 | 対処 |
|---------|------|------|
| **無人の誤り** | 人がいないところで回るループは、人がいないところで誤り続ける | 影響の大きい操作はループの外に出し、承認を挟む |
| **理解の負債** | 出荷の速度が、自分の理解が追いつく速度を追い越す | レビュー対象を減らさない。読んでいないコードを「済み」にしない |
| **思考の放棄** | 出てきたものをそのまま受け入れる癖がつき、品質が下がり続ける | 停止条件と検証を自分で書き続ける。判断は委譲しない |

> Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go.
> — Addy Osmani

内側のループ（実行・検証）はエージェントが回してよく、外側のループ（何を出荷するかの判断と説明責任）は人が持つ、という切り分けが [Own the Outer Loop](https://addyosmani.com/blog/own-the-outer-loop/)（2026-07-15）で示されています。委譲するのは作業であって、判断ではありません。

---

## 関連ドキュメント

- [AI エージェントの実行基盤（ハーネス）](harness.md) — ループが動く土台。ハーネスが弱いとループはその弱点を増幅する
- [Skills 最新動向](../trends.md) — ハーネスを含む横断的な動向
- [オントロジー](ontology.md) — ループに渡す業務知識そのものを定義する。外部状態の実装例（GBrain）も同ページ
- [コーディングエージェントの選び方](coding-agents.md) — ループの中で実際に作業するツールの比較
- [Skill / Plugin のセキュリティ](skill-security.md) — 無人で回すループに何を触らせてよいかの線引き
- [Claude Code のカスタマイズ機能](../claude-code/basics.md) — `SKILL.md`・フック・MCP の設定
- [マルチエージェントを使う境界線](multi-agent.md) — 1 つのループを複数エージェントに分けるべきかの判断基準。停止条件の考え方はここでも共通
- [長時間タスクの信頼性設計](agent-reliability.md) — 「実行中に失敗が起きる」ことを前提にした checkpoint・再開・冪等性の設計。本ページの停止条件・落とし穴の先にある話

## 参考リンク

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) — 用語の初出（2026-06-07、一次情報）
- [Loop Engineering（O'Reilly Radar 再掲）](https://www.oreilly.com/radar/loop-engineering/) — 同記事の再掲（2026-06-22）
- [Own the Outer Loop](https://addyosmani.com/blog/own-the-outer-loop/) — 内側のループと外側のループの分担（2026-07-15、一次情報）
- [Practical Loop Engineering](https://addyosmani.com/blog/practical-loop-engineering/) — ループの型と停止条件の実務（2026-08-14、一次情報）
- [Loop, Harness, Context Engineering: The Terms Explained](https://www.codecentric.de/en/knowledge-hub/blog/loop-harness-context-engineering-explained) — 用語階層の整理（codecentric、2026-07-05）
- [Automating repetitive work at OpenAI with Codex](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex) — Runme + WebMCP による反復作業のループ化（OpenAI 公式）
- [Scheduled tasks](https://learn.chatgpt.com/docs/automations) — 時刻・イベントでの起動と、その前提条件（公式）
- [VS Code 1.137 release notes](https://code.visualstudio.com/updates/v1_137) — Automations の公開（Microsoft 公式・2026-09-09、Preview）
- [Automate recurring agent tasks](https://code.visualstudio.com/docs/agents/run/automations) — 保存内容、初回実行、schedule、ローカル実行条件（Microsoft 公式・Preview）
- [Kiro Crew ドキュメント](https://kiro.dev/docs/crew/) — 定期ジョブ・ハートビート・webhook による起動（公式）
- [Claude Code Commands](https://code.claude.com/docs/en/commands) — `/goal`・`/loop` の公式リファレンス
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) — `/loop` のセッション寿命・権限・停止条件（Anthropic 公式）
