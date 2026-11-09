# エージェントの周辺ツールが終わるとき — Conductor の終了に学ぶ退出計画

> **対象ツール**: ツール横断（Conductor ほか、複数のコーディングエージェントを束ねる外部ツール） ｜ **実行環境**: CLI / Cloud（デスクトップアプリを含む） ｜ **対象読者**: 外部の並列実行ツールでエージェントを動かしている人・ツールを選ぶチームのリード ｜ **最終更新**: 2026-11-09

> Claude Code や Codex そのものではなく、それらを**まとめて動かす外側のツール**に、作業場所・会話・設定・認証を預ける使い方が広がっています。2026-11-04、そうしたツールの 1 つである Conductor が Meta への合流を発表し、**Conductor Cloud を 2026-11-20 に終了し、データの削除を始める**と告知しました。
>
> このページは、Conductor の利用者が期限までにやることを先にまとめます。そのうえで、ほかの周辺ツールにも当てはまる「何を預けていて、終わったら何が消えるか」の確かめ方と、次のツールを選ぶときの条件を書きます。記載は **2026-11-09 に確認した Conductor の公式の発表と changelog** に基づきます。実機での検証はしていません。「本記事の提案」「本記事の見立て」と書いた部分は、公式の説明ではなく本記事の判断です。

---

## 1. 何が起きたか

Conductor は、Claude Code・Codex・Cursor・OpenCode などのコーディングエージェントを、1 つの画面から並列に動かすツールです。Mac アプリ（ローカル）と、cloud で workspace を動かす Conductor Cloud があります。

公式の発表（[Conductor is joining Meta](https://www.conductor.build/announcement)）と [changelog 0.93.0](https://www.conductor.build/changelog/0.93.0-conductor-is-joining-meta)（2026-11-04）による予定は次のとおりです。

| 日付 | 何が起きるか | 利用者への影響 |
|---|---|---|
| 2026-11-04（水） | 新規登録とアプリのダウンロードを停止。既存の利用者は無料になる | 無料の利用者は Pro へ上げられない。Pro の利用者は Pro の機能を無料で使い続けられる |
| **2026-11-13（金）** | **Conductor Cloud が読み取り専用になる** | 過去の会話を読む・書き出すことはできるが、**新しいメッセージは送れない**。有料の契約者には返金がある |
| **2026-11-20（金）** | **Conductor Cloud を終了し、Cloud の利用者データの削除を始める** | 公式は、この日までに書き出すよう求めている |
| 2027 年の初め（日付は未定） | ローカルの Mac アプリの終了に向かう | それまでは新しいモデルへの対応と重大な不具合の修正が続く。アプリの終了時に Conductor の利用者データをすべて削除する |

- 発表は**日付だけで、時刻とタイムゾーンを書いていません**。日本からは、各日付の前日（日本時間）までに作業を終えておくのが安全です（本記事の提案）。
- 公式は、利用者データを売ったり学習に使ったりしたことはなく、今後もしない、としています。
- **オープンソース化については、発表に記載がありません。**
- Meta 自身の発表は、2026-11-09 時点で見つけられませんでした。買収の金額も公表されていません。共同創業者の 2 人は Meta Superintelligence Labs に加わると報じられています（[InfoWorld](https://www.infoworld.com/article/4245065/meta-acquires-conductor-as-ai-coding-shifts-toward-multi-agent-development.html)、[SiliconANGLE](https://siliconangle.com/2026/11/04/meta-acquires-ai-coding-startup-conductor-whose-app-runs-several-coding-agents-at-once/)）。これらは報道で、本記事では確かめていません。

## 2. Conductor を使っている人が 11-13 までにやること

11-13 を過ぎると Cloud の workspace は動かせなくなります。**動いている作業を終わらせて持ち出す**のは 11-13 まで、**書き出すだけ**なら 11-20 まで、と分けて考えます。

### 2-1. 全体を書き出す

公式の手順は **Settings → Account → Export data** です。全体のアーカイブを書き出せます。

ただし、**アーカイブの形式と、何が入るか（会話・workspace・差分・設定）は公式に書かれていません**。書き出したら、その場で開いて中身を確かめてください。

- 必要な会話（判断の経緯、レビューのやりとり）が読める形で入っているか
- Conductor に書いた setup の手順や、繰り返し使っていた prompt が入っているか
- 入っていないものがあれば、11-20 までに画面から手で写す

### 2-2. 続ける workspace はローカルへ移す

Cloud の workspace を右クリックして **Transfer to local** を選ぶと、**その workspace と会話を Mac へ移せます**。ただし公式の手順は、これを全体の書き出しとは別の操作として説明しています。workspace を 1 つずつ移しても、全体のアーカイブの代わりにはなりません。

**Git の branch・worktree・未 push の commit・PR の状態が一緒に移るかは、公式に書かれていません。** コードは Conductor の機能に頼らず、Git で持ち出します（本記事の提案）。

1. 作業中の workspace ごとに、**commit と push を済ませる**。未 push の commit が残っていないことを、remote の branch と見比べて確かめる。
2. 開いている PR と、その PR の branch の一覧を控える。PR は GitHub に残るが、どの workspace の作業だったかは Conductor の中にしかないことがある。
3. ローカルの worktree を片づける前に、**未 commit の変更と未 push の commit がないこと**を確かめる。worktree を消すと commit を失うことがあります（Claude Code にも、`--worktree` の終了時に確認なしで worktree と branch を消していた不具合がありました。[2.1.304〜2.1.307](../claude-code/basics.md#2130421307--統制が緩む変更と締まる見える変更)）。失った commit は `git reflog` で探します。

### 2-3. 渡した認証情報を片づける

Conductor は、GitHub や、エージェントを動かすためのアカウント（changelog には「Sign in with ChatGPT」や Claude のアカウントの利用量の表示があります）とつながっていました。**利用者が自分の Claude や ChatGPT の契約をどう渡していたかは、公式の資料からは確かめられませんでした。**

移行が終わったら、Conductor に渡したものを棚卸しします（本記事の提案）。

- GitHub の設定の **Applications**（Authorized OAuth Apps / GitHub Apps）に Conductor が残っていれば、権限を外す
- Conductor に貼った API key や token があれば、発行元で無効にし、必要なら作り直す
- cloud の workspace に置いた環境変数や secret を書き出していれば、その写しの置き場所も確かめる

ID と権限の考え方は [AIエージェントのID・認可・委任権限](agent-identity.md) を参照してください。

### 2-4. ローカルのアプリを使い続ける場合

Mac アプリは 2027 年の初めまで動きます。ただし、**新しいダウンロードは 11-04 に止まりました**。Mac を買い替えたり OS を入れ直したりすると、使い続けられなくなる可能性があります（本記事の見立て）。新しいモデルへの対応も 2027 年の初めまでで、その後に新しいインターフェースを出す予定とされていますが、中身は説明されていません。**数か月の猶予として使い、その間に移行先を決める**のが現実的です。

## 3. 周辺ツールに何を預けているか

Conductor に限らず、エージェントを束ねる外部ツールは、エージェント本体とは**別の層**にいろいろなものを持ちます。ツールが終わったときに何が消えるかは、層ごとに違います。

| 層 | 例 | ツールが終わると | 持ち運びやすくするには（本記事の提案） |
|---|---|---|---|
| **コード** | branch、worktree、commit | Git の remote に push してあれば残る。ツールだけが知っている worktree や未 push の commit は消え得る | 作業の区切りごとに push する。worktree は普通の Git の worktree として扱えるツールを選ぶ |
| **会話の記録** | エージェントとのやりとり、判断の経緯 | ツールの中にしかなければ消える | 残したい判断は PR の説明や issue に書く。エージェント本体が自分で会話を保存していることもあるので、置き場所を確かめておく |
| **手順と設定** | setup の script、よく使う prompt、エージェントごとの設定 | ツールの画面にだけ書いていれば消える | `AGENTS.md`・`CLAUDE.md`・Skill・script など**リポジトリのファイル**に置く（[エージェントが働きやすいリポジトリ](agent-ready-repo.md)） |
| **認証** | GitHub の OAuth、モデルの提供元のアカウント、API key | 権限だけが残ることがある | どのツールに何を渡したかを記録し、退出時に外す |
| **実行環境** | cloud の VM・コンテナ | 消える | 環境の作り方を script や Dev Container にしてリポジトリに置く |
| **契約と課金** | ツールの契約、モデルの利用料 | ツールの契約は返金や停止。モデルの契約は残る | モデルの契約を自分で持つ（ツールに代理で払ってもらわない）と、移っても同じ契約を使える |

この表で見ると、**リポジトリと Git の remote に置いたものは、ツールが終わっても残ります**。ツールの中にしかないものは、終了の告知から数週間で消えることがあります。Conductor の場合、告知から Cloud の終了まで 16 日でした。

## 4. 移行先をどう選ぶか

移行先は大きく 2 つあります。

### 4-1. エージェント本体の並列機能を使う

外部のツールを使わず、各製品が持つ並列実行の機能で足りるかをまず確かめます。

| 製品 | 並列・分離の仕組み | 本ガイドの解説 |
|---|---|---|
| Claude Code | サブエージェント、`--worktree` での作業場所の分離 | [サブエージェント](../claude-code/basics.md#サブエージェント) |
| Codex | managed Git worktree の作成・一覧の tool（0.162.0 以降） | [Codex の managed worktree で作業場所を分ける](harness.md#codex-の-managed-worktree-で作業場所を分ける) |
| GitHub Copilot | `/fleet` の並列サブエージェント、Dynamic workflows、cloud agent | [Copilot の HydraFusion と Dynamic workflows](multi-agent.md#copilot-の-hydrafusion-と-dynamic-workflows2026-09-3010-01) |

**複数のエージェントの製品をまたいで 1 つの画面で並べる**ことは、これらの機能ではできません。それが必要かどうかを、移行の前に確かめてください。複数体で動かすと費用も統合の手間も増えます。本当に分ける必要がある仕事かどうかは [マルチエージェントを使う境界線](multi-agent.md) と [エージェントの費用管理](agent-costs.md) で判断します。

### 4-2. 別の外部ツールへ移る

製品をまたいで並べたいなら、別の外部ツールに移ることになります。Hacker News の議論では、いくつかの移行先の名前が挙がっていました（[6 節](#6-コミュニティの見方--hacker-news)）。**本記事ではどのツールも確かめておらず、勧めているわけではありません。** 選ぶときは、次の節の条件で確かめてください。

## 5. 次のツールを選ぶ前に確かめる — 退出のしやすさ

周辺ツールは、機能だけでなく**やめやすさ**で選びます。導入の前に、次の点を確かめておきます（本記事の提案）。

| 確かめること | なぜ必要か |
|---|---|
| **データの書き出しの形式が文書になっているか** | Conductor のように、書き出しの手段はあっても中身が説明されていないことがある。試しに一度書き出して開いてみる |
| **作業場所が普通の Git の branch・worktree か** | ツール独自の形式だと、ツールなしでは開けない |
| **手順と設定をリポジトリのファイルに置けるか** | 画面にだけ書いた設定は、ツールと一緒に消える |
| **モデルの契約を自分で持てるか** | 自分の Claude・ChatGPT・Copilot の契約で動くなら、ツールを替えても契約はそのまま使える |
| **データがどこに置かれ、いつ消されるか** | ローカルだけか cloud にも置くか。終了時にいつ削除するかの方針があるか |
| **ライセンスと運営の体制** | ソースが公開されていれば、運営が終わっても自分で動かし続けられる可能性がある。ただし、公開されていても保守が止まれば、新しいモデルやエージェントの更新には追いつけなくなる |
| **終了の告知から停止までの期間** | 利用規約や公式の方針に、告知の期間が書かれているか。書かれていなければ、数週間で止まることもあると考えておく |

これは Conductor に固有の話ではありません。エージェントの周辺は新しいツールが多く、買収や方針の変更で終わることもあります。**ツールの中に置くものを少なくし、リポジトリと Git の remote に置くものを多くする**ほど、終わったときの被害は小さくなります。

導入前の安全面の確認は [Skill / Plugin のセキュリティ](skill-security.md)、外部操作の手段の選び方は [エージェントに外部操作を与える手段の選び方](tool-selection.md) を参照してください。

## 6. コミュニティの見方 — Hacker News

> 以下は Hacker News の利用者の意見で、公式の説明でも本記事の確認結果でもありません。

発表のスレッド「[Conductor is joining Meta](https://news.ycombinator.com/item?id=50369503)」は、2026-11-09 の確認時点で 218 points・225 comments でした。

- **祝福と戸惑い**: チームを祝う声と並んで、主力の開発ツールが使えなくなる戸惑いが多く見られました。「数か月どころか数週間だ」と、Cloud の期限の短さを指摘する声もありました。
- **オープンソース化の要望**: アプリの中核をオープンソースにしてほしいという要望が出ていました。読めた範囲では、チームからの返答はありませんでした。
- **移行先**: T3 Code・Orca・Paradev・Paseo などの名前が挙がっていました。Conductor の worktree を取り込めると説明しているツールもあります。ただし、**自分のツールを宣伝する書き込みも多く**、本記事ではどれも確かめていません。
- **依存のリスク**: 「オープンソースなら、創業者が買収されても残る」という趣旨の意見があり、[5 節](#5-次のツールを選ぶ前に確かめる--退出のしやすさ)のライセンスの論点と重なります。
- 共同創業者の 1 人がスレッドに書き込み、質問に答えると呼びかけていました。

## 関連ドキュメント

- [マルチエージェントを使う境界線](multi-agent.md) — 並列にする必要がある仕事かを判断する
- [コーディングエージェントの選び方](coding-agents.md) — エージェント本体の比較
- [エージェントの費用管理](agent-costs.md) — 並列実行で費用が増える仕組み
- [エージェントが働きやすいリポジトリ](agent-ready-repo.md) — 手順と設定をリポジトリに置く
- [AIエージェントのID・認可・委任権限](agent-identity.md) — 渡した権限を管理する

## 参考リンク

- [Conductor is joining Meta](https://www.conductor.build/announcement) — 終了までの予定、書き出しと Transfer to local の手順、データの方針（Conductor 公式・2026-11-09 確認）
- [Conductor changelog 0.93.0](https://www.conductor.build/changelog/0.93.0-conductor-is-joining-meta) — 2026-11-04 の告知と同じ予定・手順（Conductor 公式・2026-11-09 確認）
- [Conductor changelog](https://www.conductor.build/changelog) — 対応していたエージェントとモデルの履歴（Conductor 公式・2026-11-09 確認）
- [Meta acquires Conductor as AI coding shifts toward multi-agent development](https://www.infoworld.com/article/4245065/meta-acquires-conductor-as-ai-coding-shifts-toward-multi-agent-development.html) — 買収の報道（InfoWorld）
- [Meta acquires AI coding startup Conductor](https://siliconangle.com/2026/11/04/meta-acquires-ai-coding-startup-conductor-whose-app-runs-several-coding-agents-at-once/) — 買収の報道（SiliconANGLE）
- [Hacker News: Conductor is joining Meta](https://news.ycombinator.com/item?id=50369503) — コミュニティの反応（2026-11-09 確認）
