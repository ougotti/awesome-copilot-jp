# AI 導入の効果をどう測るか — 個人の出力と組織の成果を分ける

> **対象ツール**: ツール横断（GitHub Copilot・Claude Code・Codex ほか） ｜ **実行環境**: — ｜ **対象読者**: 開発チームのリーダー・エンジニアリングマネージャー・導入を判断する担当者 ｜ **最終更新**: 2026-10-24

> コーディングエージェントを入れると、PR の数やコードの量はすぐに増えます。しかし、それが**組織として出荷できるものが増えた**ことを意味するとは限りません。このページは、一次資料（DORA・METR・各製品の公式ドキュメント）が示す傾向と、その読み方の限界を整理し、導入の効果を測るときに**何を、どの順で、どれくらいの期間で見るか**をまとめます。Skill やエージェント自体の品質の測り方は [Skill / エージェントの評価（evals）](evals.md) を参照してください。

---

## 1. 最初に分ける — 測るものの 3 つの層

「AI で生産性が上がったか」という問いは、少なくとも 3 つの別の問いを含みます。層を混ぜると、増えたのが活動なのか成果なのかが分からなくなります。

| 層 | 問い | 指標の例 | 主な入手先 |
|---|---|---|---|
| **採用** | 使われているか | 利用者数・利用頻度・使われている Skill / agent / MCP | [Copilot usage metrics](../copilot/README.md#agentic-cli-の-customization-利用指標)、[Claude Enterprise Analytics API](https://platform.claude.com/docs/en/manage-claude/analytics-api) |
| **活動** | 何がどれだけ作られたか | PR の数・コードの行数・マージ率・レビュー時間 | Git の履歴、[PR のレビュー段階の時間](evals.md#pr-のレビュー待ち時間を品質スコアと混同しない) |
| **成果** | 組織として何が良くなったか | デリバリーの速さ（リードタイム・デプロイ頻度）・安定性（変更失敗率・復旧時間）・**手戻り** | DORA の指標、障害記録、利用者の満足度 |

製品が提供する指標の多くは**採用と活動**の層です。たとえば GitHub は 2026-10-22 に Copilot impact dashboard へ業界比較を加えましたが、比べるのはエージェント型の利用者の割合と、利用者・非利用者の PR のマージ率です（[GitHub 公式変更ログ](https://github.blog/changelog/2026-10-22-industry-comparisons-in-the-copilot-impact-dashboard)、オプトイン）。どちらも成果の層を直接は示しません。

> **層ごとに「上がってほしい方向」が違います。** 採用と活動は増えれば良いとは限らず、成果の層で手戻りや変更失敗率が増えていれば、活動の増加はむしろ負債です。

## 2. 一次資料が示していること

### DORA — AI は「増幅器」

Google の DORA チームの [State of AI-assisted Software Development 2025](https://dora.dev/research/2025/dora-report/) は、AI の主な役割を、組織がもともと持っている強みと弱みを**増幅するもの**と位置づけています。概要の一文は次のとおりです。

> AI acts as an amplifier, but the greatest returns come from focusing on the underlying sociotechnical systems.

つまり、テスト・レビュー・小さな変更・プラットフォームといった基盤が整っていれば AI はそれを伸ばし、整っていなければ問題も一緒に大きくします。DORA はこの観点から、AI の効果を引き出す能力を整理した [DORA AI Capabilities Model](https://dora.dev/ai/capabilities-model/report/)（2025-11 更新）と、導入の投資対効果を扱う [The ROI of AI-assisted Software Development](https://cloud.google.com/resources/content/dora-roi-of-ai-assisted-software-development) も公開しています。

> 本ガイドでは、DORA の報告書本体の数値は確認できた範囲でしか書きません。二次情報で広く引用されている数値（導入直後の落ち込みの幅、レビュー時間の増加率など）は、報告書本体で確認してから使ってください。

### METR — 体感と実測がずれる

METR は、経験豊富なオープンソースの開発者が**自分のリポジトリの実際の issue** に取り組む時間を、AI を使える条件と使えない条件にランダムに割り当てて比べました（[2025-07 の研究](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)）。

| 項目 | 2025 年前半のツール（2025-07 公開） | 2025 年後半のツール（[2026-02 の更新](https://metr.org/blog/2026-02-24-uplift-update/)） |
|---|---|---|
| 規模 | 開発者 16 人・issue 246 件 | 開発者 57 人・143 リポジトリ・800 件以上 |
| 推定 | AI ありで **19% 長くかかった**（95% 信頼区間 +2%〜+39%） | 前回からの参加者で 18% 短縮（−38%〜+9%）、新規の参加者で 4% 短縮（−15%〜+9%） |
| 体感 | 事前には 24% 速くなると予想し、終了後も 20% 速くなったと感じていた | — |
| METR 自身の評価 | 多くの開発者を遅くするという証拠ではないと明記。現在は「古い」結果と注記 | 実際の効果は推定より大きい可能性が高いが、**選択効果が大きく、根拠としては非常に弱い** |

2026-02 の更新で METR が挙げた「測れなくなった理由」は、そのまま組織での測定の注意点になります。

- **AI なしでは働きたくない人が参加を断る**。AI の効果が大きい人ほど測定から抜ける
- **AI なしではやりたくないタスクを持ち込まない**（30〜50% の開発者が該当と回答）。効果が大きいタスクほど抜ける
- **AI を使うと取り組むタスクの種類が変わる**。同じタスクの時間差では価値の差を表せない
- **エージェントの完了を待つ間に別のタスクを進める**ため、作業時間を正確に記録できない

> **Hacker News での受け止め（コミュニティの見方）**: 2025-07 の研究は [Hacker News で 700 点を超える議論](https://news.ycombinator.com/item?id=44522772)になりました。繰り返し出た論点は、①サンプルが 16 人と少ない、②参加者が担当リポジトリに精通しており、慣れない環境では結果が違うのではないか、③プロンプトの作成・出力の待ち・レビューに時間が移る、④大部分は速く作れても残りの仕上げに時間がかかる、⑤ツールの習熟度の差、などです。研究者側も議論に加わり、反論や補足をしています。**個人の経験談は研究の反証にはなりませんが、自分の組織で測るときに「どこで時間が増えているか」を見る観点として役立ちます。**

## 3. 指標の落とし穴

| 落とし穴 | 何が起きるか | 代わりに見るもの |
|---|---|---|
| **体感・自己申告** | METR のとおり、速くなったと感じても実測は逆のことがある | 実際の時間・成果の記録。アンケートは満足度として別に扱う |
| **PR の数・コードの量** | 増えるのは確実だが、出荷や品質と比例しない | マージ後の手戻り・revert・変更失敗率 |
| **リードタイムの短縮** | AI が数秒でコードを書くとリードタイムは縮むが、レビューを省いた結果かもしれない | レビューを経ずにマージされた PR の割合、レビュー段階ごとの時間 |
| **マージ率** | 高いほど良く見えるが、レビューが甘くなっても上がる | マージ後 90 日の revert・修正の割合（[エージェント生成 PR の観察研究](evals.md)） |
| **利用者と非利用者の比較** | 使う人と使わない人はもともと違う（選択効果） | 同じ人・同じ種類の仕事の導入前後、または導入時期をずらした比較 |
| **短すぎる評価期間** | 導入直後は学習とレビューの負担で一時的に下がることがある | 少なくとも数か月の推移。最初の数週間だけで判断しない |

## 4. 導入の効果を測る手順（設計例）

以下は本ガイドの設計例です。組織の規模と既存の計測の仕組みに合わせて調整してください。

1. **導入前の基準を取る** — 導入する数か月前から、成果の層（リードタイム・デプロイ頻度・変更失敗率・復旧時間・手戻り）と、レビュー段階の時間を記録しておく。基準がないと比べられない
2. **何を良くしたいかを先に 1〜2 個に絞る** — 「レビュー待ちを減らしたい」「小さな不具合の修正を早くしたい」など。全部を同時に良くしようとしない
3. **導入の時期をずらす** — チームごとに導入時期を変えると、時期の影響（繁忙期・組織変更）と AI の影響を分けやすい
4. **活動と成果を並べて見る** — PR 数が増えたら、同じ期間の手戻りとレビュー時間も見る。活動だけが増えて成果が横ばいなら、律速がどこにあるかを調べる（[人の仕事はどこに移るか](human-role.md)）
5. **採用の指標で「使われていない理由」を探す** — 使われていない Skill や MCP は、効果がないのか、知られていないのかを分ける
6. **数か月単位で判断する** — 導入直後の落ち込みを見込み、評価の時期を最初に決めておく

## 5. 製品の指標が測るもの・測らないもの

| 指標 | 測るもの | 測らないもの |
|---|---|---|
| Copilot usage metrics（Skill・agent・MCP・slash command・Plugin） | 採用。何がどれだけ使われたか（2026-10-22 から自作の項目も名前で） | 使った結果の品質。MCP は接続の試行回数で、tool の呼び出し数ではない |
| Copilot impact dashboard の業界比較 | エージェント型の利用者の割合、利用者・非利用者のマージ率の比較 | デリバリーの速さや安定性 |
| PR のレビュー段階の時間（`pull_request_review_times`） | 人が開き、人がレビューした PR の段階ごとの時間 | AI のレビュー、bot、作成者自身のレビュー |
| Claude Enterprise Analytics API | 利用者ごとの利用量・費用、活動の要約 | 成果物の品質 |
| OpenTelemetry（[ハーネスの観測](harness.md#動かした後に何が見えるか--opentelemetry-genai-semantic-conventions)） | ツール呼び出し・判定・止められた操作 | 組織の成果 |

**製品の指標だけで「効果があった」とは言えません。** 採用と活動の指標は、成果の指標と並べて初めて意味を持ちます。費用の指標は [エージェントの費用管理](agent-costs.md) と合わせて読みます。

## 人が確認すること

- 報告する数字が、採用・活動・成果のどの層かを明記しているか
- 活動の増加と同じ期間の、手戻り・変更失敗率・レビュー時間を見ているか
- 比較の相手（導入前・別のチーム）が、選択効果で偏っていないか
- 研究の数値を引用するとき、対象（どんな開発者・どんなタスク・いつのツール）を併記しているか

---

## 関連ドキュメント

- [Skill / エージェントの評価（evals）](evals.md) — Skill・エージェント自体の品質の測り方と、マージ後の revert・churn の観察研究
- [人の仕事はどこに移るか](human-role.md) — 活動が増えても成果が増えないとき、律速になりやすいレビューの扱い
- [エージェントの費用管理](agent-costs.md) — 効果と並べて見る費用の設計
- [AI 時代のコードレビュー](ai-code-review.md) — レビューの正しさの基準と AI レビュアーの精度
- [GitHub Copilot ガイド](../copilot/README.md#agentic-cli-の-customization-利用指標) — usage metrics の項目と読み方

## 参考リンク

- [State of AI-assisted Software Development 2025](https://dora.dev/research/2025/dora-report/) — DORA の 2025 年の報告書（Google、2026-10-24 確認）
- [DORA AI Capabilities Model](https://dora.dev/ai/capabilities-model/report/) ／ [The ROI of AI-assisted Software Development](https://cloud.google.com/resources/content/dora-roi-of-ai-assisted-software-development) — DORA の関連報告書（Google）
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR の 2025-07 の研究
- [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/) — METR の 2026-02 の更新と選択効果の説明
- [Industry comparisons in the Copilot impact dashboard](https://github.blog/changelog/2026-10-22-industry-comparisons-in-the-copilot-impact-dashboard) — GitHub 公式変更ログ（2026-10-22）
- [Hacker News: METR の研究の議論](https://news.ycombinator.com/item?id=44522772) — コミュニティの議論（2025-07、`提供元`: Community）
