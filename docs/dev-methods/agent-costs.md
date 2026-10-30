# エージェントの費用管理 — 予算・上限・配分の設計

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex） ｜ **実行環境**: — ｜ **対象読者**: 導入を担当する管理者・チームのリード・費用を見積もる担当者 ｜ **最終更新**: 2026-10-24

> チャットの補完と違い、コーディングエージェントは 1 回の依頼でファイルを読み、ツールを呼び、何度も推論します。費用は依頼の回数ではなく**扱った文脈の量**で決まるため、同じ人が同じような作業をしても月によって大きく変わります。このページは、費用が膨らむ仕組み、製品ごとの上限と可視化の仕組み、チームでの配分の考え方をまとめます。**価格・含まれる量・料率は変わるため本文には書かず、各社の公式ページへリンクします。**記載は 2026-10-24 時点の公式ドキュメントに基づきます。

---

## 1. 費用が膨らむ仕組み

| 要因 | 何が起きるか | 抑え方 |
|---|---|---|
| **長い文脈** | エージェントは会話全体を毎回送る。ツールを使うたびに、その結果を含めてまた送る。1 日開いたままの session では、短い質問でも全履歴の分がかかる | 無関係な作業の前に会話を切り替える（Claude Code の `/clear`）。長い作業は区切りで要約させる |
| **大きなツールの出力** | テストのログやファイルの全文がそのまま文脈に入る | hook で必要な行だけに絞る、subagent に読ませて要約だけを返させる |
| **毎回読む指示ファイル** | `CLAUDE.md`・`AGENTS.md`・instructions は毎回の費用になる | 短く保ち、特定の作業の手順は Skill に移す（[エージェントが働きやすいリポジトリ](agent-ready-repo.md)） |
| **並列の subagent・agent team** | それぞれが自分の文脈を持つ。Claude Code の公式ドキュメントは、plan mode の agent team は通常の session の**約 7 倍**の token を使うと説明している | 本当に分ける必要がある仕事だけを分ける（[マルチエージェントを使う境界線](multi-agent.md)） |
| **背景の自動処理** | 定期実行、セッション間のメッセージ、goal の確認、要約などが、人がいない間も文脈を送る | 定期実行の間隔と停止条件を決める（[ループエンジニアリング](loop-engineering.md)） |
| **高価なモデルと深い推論** | 推論の token は出力として課金される | 作業に合わせてモデルと effort を選ぶ |
| **再試行と遠回り** | 方向を誤ったまま進むと、やり直しの分も払う | 計画を先に確かめる、早めに止めて戻す |

> **キャッシュの寿命にも注意します。** 休憩のあと最初の依頼は、キャッシュが切れていると全文脈を処理し直します。Claude Code は `/usage` の Session に prompt cache の利用状況と、キャッシュが切れた理由の候補を表示します（[Manage costs effectively](https://code.claude.com/docs/en/costs)）。

## 2. 製品ごとの上限と可視化

### GitHub Copilot — AI Credits と予算の階層

2026-06-01 から、Copilot はすべてのプランで **GitHub AI Credits** の消費に基づく課金になりました。消費量は、モデルごとの料率で入力・出力・キャッシュの token から計算されます（[Updates to GitHub Copilot billing and plans](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/)）。Business / Enterprise の各ライセンスには一定量の credits が含まれ、組織で共有するプールになります。

予算は 4 つの階層で設定でき、**止まり方が階層によって違います**（[Budgets for usage-based billing](https://docs.github.com/en/copilot/concepts/billing/budgets-for-usage-based-billing)）。

| 階層 | 効く時点 | 上限に達したとき |
|---|---|---|
| **利用者単位**（全員共通・cost center 単位・個人） | 常に | **必ず止まる**。より具体的な設定が優先（個人 > cost center 単位 > 全員共通） |
| organization | プールを使い切った後の従量課金 | 「上限到達時に利用を停止」を**有効にしたときだけ**止まる。既定は無効で、課金が続く |
| cost center | 同上 | 同上。止まるのはその cost center の利用者だけ |
| enterprise | 同上 | 同上。enterprise の予算は月の総額の上限ではなく、「ライセンス料 + 予算」が上限になる |

これとは別に、**included usage controls** は、cost center がプールから引き出せる量をプールを使い切る**前**に制限します。上限はライセンスの数から自動で計算されます。

**誤解しやすい点**: organization・cost center・enterprise の予算は、既定では**通知だけで止まりません**。止めたいなら「上限到達時に利用を停止」を有効にするか、利用者単位の予算を設定します。逆に利用者単位の予算は、上位の予算を増やしても解除されません。

> **Hacker News での受け止め（コミュニティの見方）**: 移行の発表は [Hacker News で 700 点を超える議論](https://news.ycombinator.com/item?id=47923357)になりました。繰り返し出たのは、①モデルごとの料率で同じ使い方でも支払額が読みにくくなった、②上位モデルとエージェント型の使い方では 1 回の依頼の消費が大きい、③API の直接利用や別のツールとの比較、④年間契約や組織のシート課金との組み合わせへの懸念です。**読みにくさは、組織の側で上限と可視化を先に用意する理由になります。**

### Claude Code — 利用の上限・usage credits・workspace の上限

Claude Code は API の token の消費で課金され、どこで上限を決めるかは**サインインの方法**で変わります（[Manage costs effectively](https://code.claude.com/docs/en/costs)）。

| 利用の形 | 費用を見る場所 | 上限を決める場所 | 利用者ごとの数字 |
|---|---|---|---|
| Claude for Teams / Enterprise | 組織の analytics の spend report | 席ごとの利用上限が既定の天井。超えて使わせるなら usage credits を有効にし、組織・グループ・個人の spend limit を設定 | spend report の CSV、Enterprise は Enterprise Analytics API |
| Claude Console（API） | Console の usage ページ | **workspace の spend limit**（Claude Code 用の workspace が自動で作られる）、workspace の rate limit | Console の dashboard、Claude Code Analytics API |
| Amazon Bedrock・Google Cloud・Microsoft Foundry | 各クラウドの請求画面 | 各クラウドの予算の仕組み | OpenTelemetry、Claude apps gateway（利用者ごとの spend limit）、LLM gateway |

公式ドキュメントは、企業での導入の平均として **1 人あたり稼働日で約 13 ドル、月 150〜250 ドル**、利用者の 9 割は稼働日あたり 30 ドル未満と示しています。あわせて、モデル・コードベースの大きさ・使い方で大きく変わるため、**小さなグループで試して基準を取ってから広げる**よう勧めています。

手元で使える仕組みは次のとおりです。

- **`/usage`** — session の token と費用の見積もり、prompt cache の利用状況。Pro / Max / Team / Enterprise では、Skill・subagent・Plugin・MCP server ごとの利用の内訳、10% 以上を占める使い方への改善の提案、重い `/loop` の一覧（2.1.305 から `f` で提案の一部を適用）
- **`modelPricing`**（managed settings）— 契約の料率で費用を表示させる。表示を変えるだけで、請求は変わらない
- **`--max-budget-usd`** — `claude -p` などの実行の費用の上限
- **OpenTelemetry** — すべての利用の形で、利用者ごとの token と費用を自分の監視基盤へ送れる唯一の方法（[ハーネスの観測](harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions)）

### Codex — ChatGPT のプランの利用枠と credits

Codex は ChatGPT のプランに含まれ、**ChatGPT Work などと共通の利用枠と credits** を使います。Business の workspace は含まれる量を超えると共有の credit pool を使い、Enterprise / Edu は契約の形（credits で払うか、USD の token 課金か）で上限の決め方が違います。管理者は**利用者ごとの月の上限**と、**workspace 全体の上限**（credits なら超過分の上限、token 課金なら月の予算）を別々に設定し、両者は独立して効きます（[ChatGPT usage limits and spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits)、[Codex Pricing](https://developers.openai.com/codex/pricing)）。ページによって料率の記載が食い違うことがあるため、使う前に最新のヘルプを確認してください。

## 3. チームでの配分を決める

| 決めること | 選択肢と考え方 |
|---|---|
| **誰が上限を持つか** | 利用者ごと・チームごと・プロジェクトごと。無人の定期実行や CI は人と分け、専用の上限を持たせる |
| **超えたときどうするか** | 止める／通知だけ／申請して増やす。止めると作業が途中で切れるため、無人実行は止める、対話の作業は通知と申請、のように分ける |
| **どの単位で配るか** | Copilot は cost center、Claude は組織・グループ・個人と workspace、Codex は利用者と workspace。製品の単位に合わせて社内の部門を対応させる |
| **何と並べて見るか** | 費用だけでは高いか安いか決められない。同じ期間の[導入の効果](ai-adoption-metrics.md)と並べる |
| **どれくらいの期間で見直すか** | 使い方が定着するまでは月ごと。特定の利用者に集中していたら、使い方の内訳（Claude Code の `/usage` の内訳など）を一緒に見る |

**費用の上限は、ループの停止条件にも入れます。** 無人で回すループには、回数・時間に加えて**費用の上限**を持たせてください（[停止条件の作り方](loop-engineering.md#停止条件の作り方)）。Claude Code の `--max-budget-usd`、Copilot の利用者単位の予算は、そのための部品として使えます。

## 4. 費用を減らす習慣

製品の公式ドキュメントが勧めることのうち、どのツールにも当てはまるものです。

1. **作業ごとに会話を切り替える** — 古い文脈を毎回払わない
2. **具体的に頼む** — 「このコードベースを改善して」は広く読ませる。対象のファイルと関数を指定する
3. **確かめる手段を渡す** — テスト・期待する出力を渡すと、やり直しが減る
4. **作業に合ったモデルを選ぶ** — すべてを最上位のモデルにしない。subagent には小さいモデルを
5. **使っていない MCP server を止める** — 一覧の定義も文脈に入る。CLI で済むものは CLI を使う
6. **方向がずれたら早く止める** — 遠回りの分も払っている

## 人が確認すること

- 組織・cost center・enterprise の予算が「通知だけ」になっていないか（Copilot）
- 無人の実行に、人とは別の上限があるか
- 費用の見積もり（`/usage` など）と実際の請求の違いを把握しているか
- 費用の数字を、導入の効果の数字と並べて見ているか

---

## 関連ドキュメント

- [AI 導入の効果をどう測るか](ai-adoption-metrics.md) — 費用と並べて見る効果の測り方
- [チームで常設するエージェント](team-automations.md#6-費用の上限--止まるものと止まらないもの) — Copilot Automations の run・日・週・月の上限の止まり方と、Agent Merge の課金先
- [エージェントが働きやすいリポジトリ](agent-ready-repo.md) — 毎回読まれる指示ファイルを短く保つ
- [マルチエージェントを使う境界線](multi-agent.md) — 分けると文脈の数だけ費用がかかる
- [ループエンジニアリング](loop-engineering.md) — 停止条件に費用の上限を入れる
- [Hermes Agent](hermes-agent.md#7-費用の構造) — 自分で動かす常駐エージェントの費用の内訳

## 参考リンク

- [Updates to GitHub Copilot billing and plans](https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/) ／ [GitHub Copilot is moving to usage-based billing](https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/) — Copilot の AI Credits への移行（GitHub 公式）
- [Budgets for usage-based billing](https://docs.github.com/en/copilot/concepts/billing/budgets-for-usage-based-billing) ／ [Setting up budgets](https://docs.github.com/en/billing/how-tos/set-up-budgets) ／ [Cost centers](https://docs.github.com/en/billing/concepts/cost-centers) ／ [Models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) — 予算の階層と止まり方（GitHub 公式、2026-10-24 確認）
- [Manage costs effectively](https://code.claude.com/docs/en/costs) — Claude Code の費用の確認・組織での上限・減らし方（Anthropic 公式、2026-10-24 確認）
- [ChatGPT usage limits and spend controls](https://learn.chatgpt.com/docs/enterprise/usage-limits) ／ [Codex Pricing](https://developers.openai.com/codex/pricing) ／ [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan) — Codex の利用枠と credits（OpenAI 公式）
- [Hacker News: Copilot の usage-based billing への移行の議論](https://news.ycombinator.com/item?id=47923357) — コミュニティの議論（2026-04、`提供元`: Community）
