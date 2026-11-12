# 共有したダッシュボードは誰のアクセスで動くか — Claude Data の live sharing と既定の設定

> **対象ツール**: Claude（Claude Data・Claude Sheets・Claude Whiteboards） ｜ **実行環境**: Chat UI（web・デスクトップ・モバイル） ｜ **対象読者**: Team / Enterprise の組織のオーナー・データ基盤の担当者・ダッシュボードを作って配る人 ｜ **最終更新**: 2026-11-11

> 2026-11-10、Anthropic は **Claude Data**（旧 Claude Dashboards）を一般提供にし、**Claude Sheets** と **Claude Whiteboards** をベータで出しました。Claude Data は、接続したデータウェアハウスや業務アプリに Claude が問い合わせて、ダッシュボードを作る機能です。
>
> 業務で決めることは 2 つあります。1 つは、**Enterprise の組織では 2026-11-19 に Claude Data が既定でオンになる**ことへの対応です。もう 1 つは、ベータの **live sharing** を使うと、ダッシュボードを見る人の問い合わせが**作った人のアクセスで動く**ことです。データソースの権限を持たない人にも結果が見えるので、共有する前に範囲を決める必要があります。
>
> 記載は **2026-11-11 に確認した Anthropic の発表とヘルプセンター**に基づきます。実機・管理画面での検証はしていません。「本記事の提案」「本記事の見立て」と書いた部分は、公式の説明ではなく本記事の判断です。価格と利用上限の数値は本文に書かず、公式ページへリンクします。

---

## 1. 11-10 に何が出たか

| 機能 | 提供元・状態 | 内容 |
|---|---|---|
| **Claude Data**（旧 Claude Dashboards） | Official / GA | 接続したデータソースに Claude がグラフごとの SQL を書いて問い合わせ、ダッシュボードにする。2026-10 にベータで出た Dashboards の改称 |
| **certified queries**（Claude Data の一部） | Official / Preview（ベータ） | データの担当者が確かめた問い合わせに「certified」の印を付ける |
| **live sharing**（Claude Data の一部） | Official / Preview（ベータ） | 共有した相手が開いたとき、作った人のアクセスで最新のデータを読む |
| **Claude Sheets** | Official / Preview（ベータ） | Claude が作って編集する表。Claude の編集箇所が分かるように示される。公式は機能を「簡易な表計算」としており、Excel の機能が要るときは .xlsx か CSV に書き出す |
| **Claude Whiteboards** | Official / Preview（ベータ） | 共有のボード。議論を担当者と日付のついた予定表にまとめる |

出典は [発表記事](https://claude.com/resources/articles/sheets-whiteboards-data) と [Get started with Claude Data](https://support.claude.com/en/articles/17454700) です。使えるプランは公式ページで確かめてください。発表記事は Sheets と Whiteboards を有料プランすべてで使えるとしています。

> **Claude Meetings について。** 同じ日に、Claude が会議に参加する「Claude Meetings」のベータが報じられました（[TechCrunch](https://techcrunch.com/2026/11/10/anthropic-launches-claude-meetings-to-turn-workplace-discussions-into-plans-and-tasks/)）。ただし、2026-11-11 時点で **Anthropic の発表記事とヘルプセンターには、Claude Meetings の説明を見つけられませんでした**。録音や文字起こしの扱いも報道には書かれていません。本記事では扱わず、公式の資料が出てから取り上げます。

## 2. 組織のオーナーが決めること — 既定の設定

設定の場所は **Organization settings → Artifacts** の Templates です。certified queries と live sharing の設定は Data の下にあり、Data をオフにすると表示されません（[Artifacts admin guide](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans)）。

| 設定 | Team の既定 | Enterprise の既定 |
|---|---|---|
| Claude Data | オン | **2026-11-19 に既定でオンになる**。オーナーがそれまでに設定を保存していれば、その設定が残る |
| certified queries | オン | オフ |
| live sharing | オン | オフ |
| Sheets・Whiteboards | オン | オフ（オーナーがオンにするまで） |
| 組織外へのメールでの招待 | オン | オフ |

- **Enterprise は 11-19 までに判断が要ります。** 何もしないと Claude Data がオンになります。使わせない、または一部の人だけに使わせるなら、期日より前に設定を保存します。Enterprise では custom role で、Data・Sheets・Whiteboards をグループごとに許可できます。
- 発表は**日付だけで、時刻とタイムゾーンを書いていません**。日本からは 11-18（日本時間）までに設定を済ませておくのが安全です（本記事の提案）。
- **Team は、すでに live sharing までオンです。** 止めたい組織は自分でオフにします。
- リンクでの外部共有（External sharing）の既定は、admin guide から読み取れませんでした。管理画面で現在の値を確かめてください。
- HIPAA 対応・CMEK・教育機関など、組織外の人を招待できない構成があります。該当する組織は admin guide の条件を確かめてください。

## 3. live sharing の仕組み — 見る人ではなく、作った人のアクセスで動く

ダッシュボードを共有したとき、データを誰の権限で読むかは 2 通りあります。

| | live sharing を使わない | live sharing を使う（ベータ） |
|---|---|---|
| データを読む権限 | **見る人それぞれ**の接続 | **作った人**の接続 |
| データソースの権限がない人 | データを読めない | **結果が見える** |
| 見る人が実行できる問い合わせ | 自分の権限の範囲 | ダッシュボードが使う問い合わせだけ。それ以外は作った人のアクセスでは実行できない |
| 問い合わせの変更 | — | 編集者の承認が要る |
| 有効にする操作 | — | 作った人が Sources のメニューで、コネクタごとに「Your access」を選ぶ |

公式の説明は、live sharing が作った人のデータソースへのアクセスで動き、共有された人は自分にそのソースの権限がなくても結果を見られる、というものです。

**これは、データソース側で決めた権限を、ダッシュボードの共有範囲で上書きすることになります**（本記事の見立て）。たとえば、売上のテーブルを読める人をデータウェアハウスで絞っていても、読める人が live sharing でダッシュボードを配れば、配られた全員がその集計を見られます。

公式の資料から確かめられなかった点もあります。

- **行レベルのアクセス制御（見る人によって見える行を変える設定）がどう働くか**は、書かれていません。作った人のアクセスで動く以上、見る人ごとの絞り込みは効かないと考えておくのが安全です（本記事の見立て）。
- **組織外の人に live sharing が働くか**は、明記されていません。ダッシュボード自体は組織外へ共有できるとされています。一方 admin guide は、組織外の人やサインインしていない人には、接続したアプリと Claude の機能が働かないとしています。
- **キャッシュした結果がどこに保存されるか**と、**見る人に Claude の席（seat）が要るか**は、書かれていません。

## 4. 作って配る人が共有の前に確かめること

次は本記事の提案です。

1. **共有する相手の全員に、その集計を見せてよいか。** live sharing では、相手のデータソースの権限は確かめられません。作った人が判断します。
2. **グラフの問い合わせを開いて読む。** Claude はグラフごとに SQL を書きます。公式も、グラフの問い合わせを開いて確かめられるとしています。集計の条件（期間、除外、重複の扱い）が意図どおりかを見ます。数値は元のシステムの値と 1 か所は突き合わせます。
3. **個人が特定できる列を出していないか。** 集計のつもりでも、絞り込みの組み合わせで個人の値が見えることがあります。
4. **いつのデータかを見る。** 公式の説明では、Claude は決まった時刻に更新するのではなく、開いたときに必要なら更新します。各グラフには最後に更新した時刻が表示されます。会議で数字を読む前に確かめます。
5. **自分が異動・退職したらどうなるか。** live sharing は作った人のアクセスに頼ります。作った人の権限がなくなった後の挙動は、公式の資料から確かめられませんでした。長く使うダッシュボードは、担当者と引き継ぎ先を決めておきます。

共有する情報の線引きは [生成AIを業務で安全に使う](safety.md) も参照してください。

## 5. certified queries — 「確かめた数字」の印を誰が付けるか

certified queries は、確かめた問い合わせに印を付け、ダッシュボードのグラフに「certified」と表示する仕組みです（ベータ）。

- **印を付けられる人**: データの担当チームのほか、その Data の成果物に書き込みの権限を持つ人です。
- **定義の取り込み**: dbt・Looker・Cube の定義を、MCP のコネクタ経由で使えます。
- **編集すると印が外れる**: certified の問い合わせを書き換えると、印はなくなります。
- **Git で管理できる**: 組織が問い合わせを Git で管理する Plugin に置いている場合、変更は GitHub の PR のレビューを通ります。オーナーは、どの marketplace と Plugin を使うかを設定で選びます。**この選択を消すと、既存の印もなくなります。**

**書き込みの権限を持つ人なら印を付けられる点に注意が要ります**（本記事の見立て）。印が「データチームが確かめた」という意味になるのは、書き込みの権限をデータチームに絞るか、Git の PR を通す構成にしたときだけです。印の意味を組織で決め、決めたとおりになる構成を選んでください。Plugin の配り方は [Copilot の Plugins](../copilot/plugins.md) や [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md) の考え方が参考になります。

## 6. 費用と記録

| 観点 | 公式の説明 |
|---|---|
| **利用量** | Claude Data の利用は、プランの利用上限に数えられる。Team と席数で契約する Enterprise は**各利用者の席の上限**から使い、利用量で契約する Enterprise は**組織に請求**される。数値は [Artifacts admin guide](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans) と料金のページで確かめる |
| **監査** | Compliance API に、Data の成果物の作成・閲覧・編集・削除のイベントが残る。**中身は記録されない** |
| **棚卸し** | オーナーは、公開された成果物の一覧を種類「Data」で絞り、所有者と公開範囲を見られる |
| **履歴** | 所有者は以前の版に戻せる。戻すと全員に反映される |
| **保持** | Enterprise の独自の保持期間は成果物にも及ぶことがあり、その期間だれも開かなければ削除され得る。**問い合わせの結果に固有の保持の説明は見つからなかった** |

live sharing で見る人が開いたときの利用量が、作った人と見る人のどちらに数えられるかは、公式の資料から確かめられませんでした。多くの人に配る前に、少人数で試して利用量の動きを見ることを勧めます（本記事の提案）。費用の考え方は [エージェントの費用管理](../dev-methods/agent-costs.md) を参照してください。

## 7. 導入の順番（本記事の提案）

1. **Enterprise は 11-19 の前に、Data をオンにするかを決めて保存する。** 決めきれなければ、いったんオフで保存し、試すグループだけに custom role で許可する。
2. **live sharing は後回しにする。** まず、見る人それぞれの接続で読む共有（live sharing なし）で使い、データソース側の権限がそのまま効く状態で慣れる。
3. **live sharing を使うダッシュボードの条件を決める。** たとえば「全社に公開してよい集計だけ」「個人が特定できる列を含まない」など。
4. **月に 1 回、種類「Data」で公開された成果物を棚卸しする。** 所有者がいなくなったもの、公開範囲が広すぎるものを見直す。
5. **certified の印の意味を文書にする。** 誰が付けてよいか、Git の PR を通すかを決める。

## 8. コミュニティの見方 — Hacker News

> 以下は Hacker News の利用者の意見で、公式の説明でも本記事の確認結果でもありません。

発表のスレッド「[Claude Whiteboards, Claude Sheets, and Claude Data](https://news.ycombinator.com/item?id=50443716)」は、2026-11-11 の確認時点で約 150 points・119 comments でした。コメントは一部だけを読んでいます。

- **囲い込みへの警戒**: 成果物が Claude の中に溜まることで、ほかへ移りにくくなるという見方がありました。
- **製品の広げすぎへの疑問**: 周辺の製品を増やすことや、API の顧客と競合することを疑問視する声がありました。
- **表計算の位置づけ**: Excel は受け渡しの形式になるという意見と、大きな会社は今も Excel で動いているという意見に分かれていました。
- **データの見え方**: エージェントが何を読んだかを見たい、データを外へ送ることが心配だ、という声がありました。
- **live sharing の権限の仕組みは、読めた範囲ではほとんど話題になっていませんでした。**

囲い込みの論点は、[エージェントの周辺ツールが終わるとき](../dev-methods/tool-exit-plan.md)の「何を預けているか」の確かめ方と重なります。

## 関連ドキュメント

- [生成AIを業務で安全に使う](safety.md) — 入力してよい情報と、出力後に確認する項目
- [事務・バックオフィス活用ガイド](office-work.md) — 表・文書・スライドを作る実践
- [AIエージェントのID・認可・委任権限](../dev-methods/agent-identity.md) — 誰の権限で動くかを分けて考える
- [チームで常設するエージェント](../dev-methods/team-automations.md) — 作った人の名義と組織の名義の違い
- [エージェントの費用管理](../dev-methods/agent-costs.md) — 利用量を誰が負担するか

## 参考リンク

- [Introducing Claude Whiteboards, Claude Sheets, and Claude Data](https://claude.com/resources/articles/sheets-whiteboards-data) — 2026-11-10 の発表。状態、既定の設定、連携先（Anthropic 公式・2026-11-11 確認）
- [Get started with Claude Data](https://support.claude.com/en/articles/17454700) — live sharing・certified queries・更新の仕組み、Enterprise の 11-19 の既定（Anthropic 公式・2026-11-11 確認。ページの更新日は相対表示で、日付は読み取れなかった）
- [Artifacts admin guide for Team and Enterprise plans](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans) — 設定の場所、プランごとの既定、利用量、Compliance API、組織外への共有（Anthropic 公式・2026-11-11 確認）
- [Dashboards and Motion](https://claude.com/resources/articles/dashboards-and-motion) — 2026-10-08 の Claude Dashboards のベータの発表（Anthropic 公式・2026-11-11 確認）
- [Anthropic launches Claude Meetings](https://techcrunch.com/2026/11/10/anthropic-launches-claude-meetings-to-turn-workplace-discussions-into-plans-and-tasks/) — Claude Meetings の報道（TechCrunch。公式の資料では確かめていない）
- [Hacker News: Claude Whiteboards, Claude Sheets, and Claude Data](https://news.ycombinator.com/item?id=50443716) — コミュニティの反応（2026-11-11 確認）
