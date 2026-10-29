# チームで常設するエージェント — 名義・費用・起動条件・改善の設計

> **対象ツール**: GitHub Copilot（Copilot Automations・GitHub Agentic Workflows・Agent Merge） ｜ **実行環境**: Cloud ｜ **対象読者**: リポジトリの管理者・チームのリード・エージェントを無人で動かす人 ｜ **最終更新**: 2026-10-30

> これまでのコーディングエージェントは、**人が頼んで、人が結果を受け取る**道具でした。2026-10-28 の GitHub Universe で、GitHub は **リポジトリに属し、チームで編集し、Copilot の名義で動き、リポジトリの所有者に課金される** automation を出しました。同じ日に、PR の CI の失敗やコンフリクトを cloud で直し続ける Agent Merge、エージェントのワークフローを Markdown で書いて Actions で動かす Agentic Workflows の GA も発表されています。
>
> エージェントが特定の人の手を離れて常に動くようになると、**誰の名義で動くか、誰が払うか、何をきっかけに動くか、誰が改善を判断するか**を先に決める必要があります。このページはその決め方を、GitHub の機能を具体例にしてまとめます。記載は **2026-10-30 に確認した公式の changelog と docs** に基づきます。実機での検証はしていません。「本記事の提案」「本記事の見立て」と書いた部分は、公式の説明ではなく本記事の判断です。

---

## 1. 10-28 に何が出たか

| 発表 | 提供元・状態 | 何が変わるか |
|---|---|---|
| [Shared Copilot Automations](https://github.blog/changelog/2026-10-28-build-shared-workflows-for-your-team-with-copilot-automations) | Official / 状態の記載なし（段階的に提供中） | これまで個人のものだった automation を、リポジトリの持ち物として作れる。名義は Copilot、課金はリポジトリの所有者 |
| [新しい trigger・tool・費用の上限](https://github.blog/changelog/2026-10-28-new-tools-triggers-and-cost-controls-for-copilot-automations) | Official / 状態の記載なし | REST API からの起動、24 種類の GitHub イベント、automation どうしの連鎖、20 種類の GitHub tool、MCP server の tool、run・日・週・月の AI credits の上限 |
| [自己改善する Automations](https://github.blog/changelog/2026-10-28-copilot-automations-now-learn-from-outcomes-and-self-improve) | Official / 状態の記載なし | GitHub 上の結果（ラベルが直されたか、コメントが採用されたか、PR がマージされたか）から、prompt・tool・trigger の改善案を出す。適用は人が決める |
| [Agent Merge in the cloud](https://github.blog/changelog/2026-10-28-agent-merge-watches-and-fixes-pull-requests-in-the-cloud) | Official / 状態の記載なし | PR の merge box の **Watch and fix** から、CI の失敗とコンフリクトを Copilot に直させ続ける |
| [GitHub Agentic Workflows](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available) | Official / GA | Markdown で書いたエージェントのワークフローを Actions YAML にコンパイルして動かす。既定は読み取り専用 |
| [つながった Copilot cloud の体験](https://github.blog/changelog/2026-10-28-work-from-anywhere-with-a-new-connected-copilot-cloud-experience) | Official / GA（有料プラン） | 同じ cloud session を web・Mobile・CLI・app・VS Code・Slack・Teams で続けられる。cloud sandbox の課金は 2026-11 から、Actions の利用枠から使える |

> **同じ「Automations」でも、VS Code のものとは別物です。** [VS Code 1.137 の Automations](../copilot/README.md#automations--エージェントタスクを定期実行する) は**手元の VS Code で動く** Preview 機能です。このページで扱う Copilot Automations は **Copilot cloud agent として GitHub 上で動きます**。VS Code 1.144 以降で `chat.automations.cloud.enabled` を有効にすると、Agents ウィンドウに cloud の automation も表示されます（[About Copilot automations](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations)）。

## 2. Automations と Agentic Workflows のどちらで作るか

どちらも「イベントや予定をきっかけに、エージェントにリポジトリの仕事をさせる」仕組みです。大きな違いは**定義をどこに置き、誰がどうレビューするか**にあります。GitHub の docs も、automation をコードとして保存したい、PR でレビューしたい、別のコーディングエージェントで動かしたい場合は Agentic Workflows を見るよう案内しています。

| 観点 | Copilot Automations | GitHub Agentic Workflows |
|---|---|---|
| 定義の置き場所 | GitHub 上の設定。**Git に commit されず、PR でレビューされない**。shared の automation は GitHub 上で変更履歴を見られる | リポジトリの Markdown ファイル。`gh aw` で Actions YAML にコンパイルし、**PR でレビューする** |
| 作る場所 | リポジトリの Agents タブ・Copilot app・VS Code（1.144 以降）・REST API | `gh aw` CLI 拡張（[quickstart](https://github.github.com/gh-aw/)） |
| 動かすエージェント | Copilot cloud agent | 既定は Copilot CLI。ほかのコーディングエージェントも選べる |
| 実行環境 | Copilot cloud agent の session | GitHub Actions。既存の runner group と policy をそのまま使い、self-hosted の ARC でも動く |
| 権限の絞り方 | 使える **tool を選ぶ** | 既定で読み取り専用。sandbox のコンテナと Agent Workflow Firewall の中で動き、書き込みは **safe outputs** で検査され、専用の threat detection の job が変更を確かめてから適用する |
| 使えるリポジトリ | **private と internal だけ**（public は不可） | github.com の Free・Team・Enterprise。既定の Copilot CLI を使うなら Copilot のライセンスが必要 |
| 費用の見通し | 作るときに run・日・週・月の上限を設定 | `gh aw forecast` で AI credits の月の幅を見積もる |

**選び方（本記事の提案）**

- **まず試して、prompt と tool を画面で調整したい** → Automations。自己改善の仕組みもこちらにある。
- **定義の変更を PR で承認したい、監査で「いつ誰が何を変えたか」をコードの履歴で示したい** → Agentic Workflows。
- **public リポジトリで動かしたい** → Automations は使えないため Agentic Workflows。
- 試すのは Automations、定着したら Agentic Workflows に移す、という順番もあり得ます。ただし移すときは定義を書き直すことになり、自動で変換されるわけではありません。

> Agentic Workflows の GA の告知には、導入企業の担当者による効果の数字（週 29 時間の削減、コミットの 91% を AI が作成、など）が載っています。これは事例としての主張で、本記事では確かめていません。自分のチームで効果を測る方法は [AI 導入の効果をどう測るか](ai-adoption-metrics.md) を参照してください。

## 3. 誰の名義で動き、誰が払うか — personal と shared

automation には **personal** と **shared** の 2 つの型があり、**作った後で型を変えることはできません**（[About Copilot automations](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations#personal-and-shared-automations)）。

| | personal | shared |
|---|---|---|
| automation を見られる人 | 作った人だけ | リポジトリの read 権限を持つ全員 |
| **run を見られる人** | **リポジトリの read 権限を持つ全員** | リポジトリの read 権限を持つ全員 |
| 編集できる人 | 作った人だけ | リポジトリの write 権限を持つ全員 |
| AI credits を払う人 | 作った人 | リポジトリを所有する organization（個人のリポジトリなら所有者の Copilot の契約） |
| GitHub 上の操作の名義 | 作った人 | **Copilot** |
| 作った人が抜けたら | — | リポジトリに属するので動き続ける |

この表から、運用で気をつけることが 4 つ出てきます。

1. **shared が作った PR には、既定で承認が 1 つ多く要ります。** リポジトリが 1 つ以上の承認を必須にしている場合です。管理者は rulesets ではこの追加の要件を外せますが、branch protection rules では外せません。personal の automation が作った PR は作った人の名義なので、その人は自分で承認できません。承認を必須にしているリポジトリでは、どちらの型でも、既定では作った本人だけでエージェントの PR をマージできないようになっています。
2. **組織のリポジトリで shared を動かすには、管理者の設定が要ります。** 「Allow use of Copilot cloud agent billed to the organization」のポリシーを有効にします。
3. **作った人がいなくなっても動き続けることは、裏を返すと、誰も見ていない automation が残るということです。** shared の automation ごとに、結果を見て止める判断をする担当者を決めておくことを勧めます（本記事の提案）。所有者・実行主体・承認者・監査者の分け方は、[AI エージェントの ID・認可・委任権限](agent-identity.md#7-所有者実行主体承認者監査者の責任分界)にまとめています。
4. **prompt と session のログは、read 権限を持つ人に全部見えます。** personal の automation でも run はリポジトリの read 権限者に見えます。prompt に秘密の情報や個人的なメモを書かないでください。

## 4. 何をきっかけに動くか — trigger と入力の信頼

| trigger | 内容 |
|---|---|
| 予定 | 毎時・毎日・毎週 |
| GitHub のイベント | issue の作成、PR の作成・更新に加え、10-28 に 24 種類が追加された（issue の担当・ラベル・クローズ、PR のレビュー依頼・コンフリクト・レビュー提出、discussion、code scanning・secret scanning・Dependabot の alert など）。issue や PR には検索クエリや変更ファイルのフィルタを付けられる |
| REST API | すべての automation を API から起動でき、prompt に渡す文脈を付けられる。Jira・Sentry・PagerDuty などの webhook を受けて呼ぶ使い方を想定している（[Trigger an automation API](https://docs.github.com/rest/agent-automations/agent-automations?apiVersion=2026-03-10)） |
| 別の automation | 「Automation run succeeded / failed」の trigger と、各 trigger の **Can be triggered by** の設定で、automation をつないで多段のワークフローにできる |

**入力の信頼について、既定で守られていること**

- **write 権限を持たない人が起こしたイベントは、既定で無視されます。** 外部の人が開いた issue に書かれた指示で Copilot が動く、という prompt injection を防ぐためです。必要なら許可できますが、許可すると issue の本文が攻撃の入口になります。
- **automation が開いた PR では、既定で Actions のワークフローが自動では動きません。** write 権限を持つ人が承認してから動きます。
- **Can be triggered by の既定は「Only users」** です。「Users and Copilot」にすると、Copilot が開いた PR のようなほかの automation の出力でも起動します。

> **連鎖させるときは、自分自身を起動し続けないかを確かめてください（本記事の提案）。** たとえば「PR が開かれたら修正の PR を開く」automation を「Users and Copilot」にすると、自分の出力で自分が起動しうる構成になります。連鎖は「成功・失敗の trigger」で一方向につなぎ、各 automation に後述の費用の上限を付けておくと、止まらない連鎖の被害を抑えられます。外部のイベントでエージェントを動かすときの重複と自己再発火の確かめ方は、[MCP Events](mcp-events.md#6-失敗の観点--テストで確かめること) も参考になります。

## 5. 何をしてよいか — tool とリポジトリの設定

automation がしてよいことは、作るときに選ぶ **tool** で決まります。docs は、tool の選択を automation の範囲を決める**主な手段**と位置づけ、仕事に要る tool だけを与えるよう勧めています。GitHub 上で **Suggest tools** を押すと prompt から tool を提案させられますが、提案をそのまま受け入れず、一つずつ必要かを確かめてください。

| tool の種類 | 届く範囲 |
|---|---|
| GitHub の tool | automation が属する**1 つのリポジトリの中だけ**。10-28 に、添付のアップロード、ワークフローの再実行、**PR のマージ**、コメントの更新・非表示、PR の draft と ready の切り替え、discussion の読み書きなど 20 種類が追加された |
| MCP server の tool | リポジトリの MCP の設定に登録した server から選ぶ。**範囲はリポジトリに限られず、server の設定と認証情報が許す範囲すべて**（ほかのリポジトリや外部のシステムを含む） |

**PR のマージ**の tool が加わったことで、automation が自分の作った変更をマージまで進める構成も作れるようになりました。人のレビューを残したいなら、この tool を与えないか、branch のルールで必須の承認を設定してください。

automation は、リポジトリの **Copilot cloud agent の設定を引き継ぎます**。custom instructions・Agent Skills・firewall のルール・secrets と variables です。つまり、`.github/copilot-instructions.md` や Skill を変えると、**そのリポジトリのすべての automation の動きが変わります**。指示ファイルの変更をレビューするときは、automation への影響も考えてください（[エージェントが働きやすいリポジトリ](agent-ready-repo.md#5-指示ファイルを保守する)）。

## 6. 費用の上限 — 止まるものと止まらないもの

automation の run はそれぞれ Copilot cloud agent の session を 1 つ始め、**GitHub AI Credits と GitHub Actions の分**を使います。AI credits の上限は automation ごとに設定でき、**設定しなければ上限なしで動きます**（[Controlling costs with AI credits limits](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations#controlling-costs-with-ai-credits-limits)）。

| 上限 | 達したとき | リセット |
|---|---|---|
| run ごと（最小 30 AI credits） | **その run を止める** | — |
| 日 | 新しい run を始めない。**動いている run は止めない** | 毎日 00:00 UTC（日本時間 9:00） |
| 週 | 同上 | 毎週月曜 00:00 UTC |
| 月 | 同上 | 毎月 1 日 00:00 UTC |

1 回の run の費用を抑えたいなら、**run ごとの上限**を必ず設定してください。日・週・月の上限だけでは、長く動く 1 回の run を止められません。

ほかに、費用の扱いで間違えやすい点があります。

- **Actions の分は AI credits とは別に、リポジトリの所有者に課金されます。**
- cloud sandbox の課金は 2026-11 から始まります。Actions の利用枠は、決まった分数ではなく**金額で表す共有の枠**になり、hosted runner・cloud sandbox・larger runner（Team と Enterprise Cloud）で共有します。使う計算資源の料率が高いほど、早く枠を使い切ります（[cloud の体験の告知](https://github.blog/changelog/2026-10-28-work-from-anywhere-with-a-new-connected-copilot-cloud-experience)）。
- **Agent Merge の AI credits は、PR の作者ではなく、Watch and fix を有効にした人に課金されます。**

組織全体の予算の階層と、上限に達したときの止まり方は [エージェントの費用管理](agent-costs.md#github-copilot--ai-credits-と予算の階層) を参照してください。無人のループに費用の上限を入れる考え方は [ループエンジニアリング](loop-engineering.md#停止条件の作り方) にあります。

## 7. 自己改善する automation — 改善案を誰が判断するか

automation は、作業中に足りない tool に気づいたときや、結果を振り返ったときに、自分やほかの automation の prompt・tool・trigger の**改善案**を出せます。Copilot に頼むと、仕事をする automation と、その結果を評価して改善案を出す automation を組み合わせた **automation group** を作ってくれます。

GitHub の例では、カスタムのコードレビューを次の 2 つで組みます。

1. PR が開かれたら変更をレビューしてコメントする automation
2. 開発者がそのコメントにどう反応したかを週に 1 度分析し、1 の改善案を出す automation

改善案が出ると通知が届き、人が内容を見て適用するか捨てるかを決めます。**勝手には適用されません。**

**手がかりは成果そのものではなく、成果の代わりの指標です（本記事の見立て）。** 「ラベルが直されなかった」は誰も見ていないだけかもしれません。「コメントが採用された」は、指摘が正しかったことと同じではありません。「PR がマージされた」を手がかりにすると、小さく無難な PR に寄っていく可能性もあります。改善案は、prompt の変更のレビューと同じように扱ってください。

- 改善案が**どの指標を良くしようとしているか**を読む
- 適用する前と後で、同じ入力に対する結果を比べる（[評価から改善・検証・昇格へつなぐ](evals.md#7-評価から改善検証昇格へつなぐ)）
- automation は Git に入らないため、変更の記録は GitHub 上の変更履歴にしか残りません。理由を残したいなら、適用したときに issue などに書いておく

## 8. Agent Merge — PR をマージできる状態に保ち続ける

PR の merge box で **Watch and fix** を選ぶと、Copilot は指定した妨げ（**Actions のワークフローの失敗**・**base branch とのコンフリクト**、またはその両方）を見張り、現れたら cloud の開発環境で直し始めます。始めた理由は PR のタイムラインに出ます。自分が作るすべての PR で自動で有効にする設定もあります（[Agent Merge の docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/get-pull-requests-ready-to-merge)）。

| 確認すること | 内容 |
|---|---|
| 前提 | 有料の Copilot プランで Copilot in the cloud を使えること。リポジトリの **Enable automations** のポリシーが有効であること |
| 対象外 | stacked PR、fork から開かれた PR |
| 動く環境 | cloud sandbox ではなく **Actions ベースの開発環境**。`copilot-setup-steps.yml`、custom instructions、Agent Skills を使う |
| auto-merge との関係 | **別の機能**。Agent Merge を有効にしても auto-merge は有効にならない。両方を使うと、Copilot が PR をマージできる状態に保ち、条件がそろったところで GitHub がマージする |
| 止め方 | merge box の **Unassign Copilot**。有効にした人か、write 権限を持つ人ができる |

docs は、Agent Merge が人のレビューやリポジトリのマージの要件を**置き換えない**と明記しています。

> **「CI を通すための修正」は、テストを弱めて通すことでも達成できてしまいます（本記事の見立て）。** Agent Merge が入れた commit は、何を直したかに加えて、**テストの削除・skip・期待値の書き換えがないか**を確かめてください。点検の手順は [AI 時代のコードレビュー](ai-code-review.md#テストの変更のチェックリスト) にあります。auto-merge と組み合わせるなら、必須のレビューと status check を先に設定し、Copilot の commit の後にも人の承認が要る状態にしておきます。

## 9. 最初の 1 本を作る手順（本記事の提案）

1. **仕事を 1 つに絞る** — 「新しい issue に再現手順があるか確かめ、足りなければ質問のコメントを付ける」のように、結果を人がすぐ確かめられるもの
2. **personal で作る** — リポジトリの Agents タブ → Automations から作る。型は後で変えられないので、チームで使うと決めたら shared で作り直す
3. **trigger を狭くする** — イベントの trigger なら、検索クエリや変更ファイルのフィルタで対象を絞る。write 権限のない人のイベントは無視されたままにする
4. **tool を最小にする** — まずコメントだけ。push・PR の作成・マージは、結果を何回か見てから足す。MCP server の tool は、その server が届く範囲を確かめてから選ぶ
5. **run ごとの上限を設定する** — 日・週の上限も付けておく
6. **session のログを読む** — 数回動いた後で、prompt どおりに動いたか、余計な操作がないかを確かめる
7. **担当者を決めて shared にする** — 結果を見る人、止める判断をする人を決めてから広げる

## 10. ほかのツールで同じことをするなら

Copilot Automations のように **cloud で動き、リポジトリに属し、チームで共有する**形の automation は、2026-10-30 時点ではほかのツールに同じ形のものがありません。予定やイベントで動かす仕組みは各ツールにあるため、**実行する場所・状態の寿命・承認・停止条件**で比べてください。Codex の Scheduled tasks、Claude Code の `/loop`、VS Code のローカルの Automations、Kiro Crew、Hermes Agent の cron の比較は、[ループエンジニアリング](loop-engineering.md#定期実行を選ぶときの比較)にまとめています。

## コミュニティの見方

> **Hacker News での受け止め（コミュニティの見方）**: 2026-10-30 時点で、Universe 関連の投稿（[GitHub Universe 2026 の概要](https://news.ycombinator.com/item?id=50276062)、[Copilot Fusion](https://news.ycombinator.com/item?id=50278478) など）はいずれも数点にとどまり、Automations や Agent Merge について中身のある議論はまだ起きていません。概要の投稿には、GitHub の基盤の信頼性の改善に期待するコメントが 1 件付いた程度です。議論が出てきたら追記します。

## 人が確認すること

- shared の automation ごとに、結果を見て止める判断をする担当者が決まっているか
- 組織のポリシー（cloud agent・automations・組織への課金）が意図どおりになっているか
- write 権限のない人のイベントを許可している automation がないか。あるなら、その理由
- 「Users and Copilot」で起動する automation が、自分や別の automation の出力で起動し続けないか
- すべての automation に**run ごとの** AI credits の上限があるか
- マージや MCP server の tool を与えた automation で、人の承認がどこに残っているか
- 自己改善の改善案を、適用前と後の結果を比べてから受け入れているか
- Agent Merge の commit で、テストが弱められていないか

---

## 関連ドキュメント

- [ループエンジニアリング](loop-engineering.md) — 定期実行の比較と停止条件の作り方
- [AI エージェントの ID・認可・委任権限](agent-identity.md) — 所有者・実行主体・承認者・監査者の分け方
- [エージェントの費用管理](agent-costs.md) — Copilot の予算の階層と止まり方
- [Skill / エージェントの評価（evals）](evals.md) — 改善案を受け入れる前に比べる方法
- [AI 時代のコードレビュー](ai-code-review.md) — テストの削除・弱化の点検
- [エージェントが働きやすいリポジトリ](agent-ready-repo.md) — automation も読む指示ファイルの保守
- [GitHub Copilot ガイド](../copilot/README.md) — VS Code のローカルの Automations と Agentic Workflows の導入

## 参考リンク

- [Build shared workflows for your team with Copilot Automations](https://github.blog/changelog/2026-10-28-build-shared-workflows-for-your-team-with-copilot-automations) ／ [New tools, triggers, and cost controls for Copilot Automations](https://github.blog/changelog/2026-10-28-new-tools-triggers-and-cost-controls-for-copilot-automations) ／ [Copilot Automations now learn from outcomes and self-improve](https://github.blog/changelog/2026-10-28-copilot-automations-now-learn-from-outcomes-and-self-improve) — Automations の 10-28 の更新（GitHub 公式）
- [About Copilot automations](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automations) — 型・trigger・tool・費用の上限・改善案・安全の仕組み（GitHub 公式、2026-10-30 確認）
- [Trigger an automation API](https://docs.github.com/rest/agent-automations/agent-automations?apiVersion=2026-03-10) — 外部のシステムから起動する REST API（GitHub 公式）
- [GitHub Agentic Workflows generally available](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available) ／ [GitHub Agentic Workflows のドキュメント](https://github.github.com/gh-aw/) ／ [githubnext/agentics](https://github.com/githubnext/agentics) — GA の告知、導入手順、ワークフローの例（GitHub 公式・GitHub Next）
- [Agent Merge watches and fixes pull requests in the cloud](https://github.blog/changelog/2026-10-28-agent-merge-watches-and-fixes-pull-requests-in-the-cloud) ／ [Getting pull requests ready to merge with Agent Merge](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/get-pull-requests-ready-to-merge) — Agent Merge の告知と docs（GitHub 公式、2026-10-30 確認）
- [Work from anywhere with a new, connected Copilot cloud experience](https://github.blog/changelog/2026-10-28-work-from-anywhere-with-a-new-connected-copilot-cloud-experience) — cloud session の継続、cloud sandbox、Actions の利用枠（GitHub 公式）
- [Hacker News: GitHub Universe 2026: Evolving every layer of the stack](https://news.ycombinator.com/item?id=50276062) — コミュニティの反応（2026-10、`提供元`: Community）
