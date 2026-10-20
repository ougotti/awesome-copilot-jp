# Hermes Agent — 常駐して自分から連絡してくる OSS エージェント

> **対象ツール**: Hermes Agent（Nous Research） ｜ **実行環境**: CLI / Cloud（VPS・サーバーレス）/ Chat UI（Telegram などのメッセージアプリ） ｜ **対象読者**: 個人用の常駐エージェントを試したい人・導入を判断するエンジニア ｜ **最終更新**: 2026-10-21

> [Hermes Agent](https://github.com/NousResearch/hermes-agent) は、Nous Research が MIT ライセンスで公開しているエージェントです。Claude Code や Codex が「呼ぶと動く」のに対し、Hermes は **gateway が常駐し、決まった時刻やメッセージをきっかけに動いて、結果を Telegram などへ送ってきます**。このページは、Metics Media の動画 [Build Your First AI Agent in 20 Minutes (No Coding)](https://www.youtube.com/watch?v=rCkYVxOX-dI)（2026-10-19 公開）が紹介する構成（VPS + Telegram + 安価なモデル + 価格の監視）を、公式ドキュメントで裏を取りながら、実行場所・接続・承認・費用の層に分けて整理します。

> [!NOTE]
> 動画の概要欄には VPS と Nous Portal の**アフィリエイトリンク**が含まれます。本ガイドは特定の VPS やプランを推奨しません。価格・プラン名・モデル名は変わるため、本文には固定で書かず公式ページへリンクします。記載は 2026-10-21 時点の公式ドキュメント・README・release notes に基づき、実機での検証は行っていません。

---

## 30 秒で判断する

| こうしたい | Hermes は | 代わりの候補 |
|---|---|---|
| 寝ている間も定期的に確認して、**変化があったときだけ**スマホに知らせてほしい | 向いている。cron と gateway が中心機能 | [Codex の Scheduled tasks](../codex/README.md#6-定期イベントで動かすscheduled-tasks)、[Kiro Crew](harness.md#kiro-crew--常駐して動き続けるハーネス) |
| スマホのメッセージアプリから、自分専用のエージェントに話しかけたい | 向いている。Telegram・Discord・Slack・Signal など 1 つの gateway で受ける | [ChatGPT の dots](../codex/README.md#個人の定期作業dotsteam-tasksを選ぶ)（自分でサーバーを持たない） |
| モデルを自分で選び、費用を自分で管理したい | 向いている。Nous Portal・OpenRouter・各社の API キー・ローカルモデルを切り替えられる | [OpenCode](coding-agents.md#opencode--プロバイダーを選ぶ前提の設計) |
| リポジトリで開発作業を任せたい | 主目的ではない（できなくはない） | [コーディングエージェントの選び方](coding-agents.md) |
| サーバーの管理をしたくない、業務データを社外の VPS に置けない | 向いていない | [事務・ビジネス活用ガイド](../business/README.md) |

「ノーコード」でも、**サーバー・bot のトークン・API キー・課金・承認の設定を自分で持つ**ことに変わりはありません。8 節の最低ラインを読んでから始めてください。

## 1. チャットボット・コーディングエージェント・常駐エージェント

動画の冒頭の説明は「チャットボットは次のメッセージを待ち、エージェントは寝ている間も働く」です。本ガイドの言葉で言い直すと、違いは**誰が起動するか**と**状態がどこに残るか**です。

| | チャットボット（ChatGPT・Claude の Chat UI） | コーディングエージェント（Claude Code・Codex・Copilot CLI） | 常駐エージェント（Hermes Agent・Kiro Crew） |
|---|---|---|---|
| 起動するのは | 人のメッセージ | 人のコマンド・依頼（定期実行は追加機能） | **常駐プロセス**。時刻・メッセージ・webhook でも動く |
| 連絡の向き | 人 → AI | 人 → AI（結果は端末や PR で見る） | **AI → 人**（メッセージアプリへ送ってくる） |
| 状態が残る場所 | サービス側の会話履歴・メモリ | 作業ディレクトリ・セッション・設定ファイル | 常駐先のディスク（Hermes は `~/.hermes/`）|
| 手を動かす場所 | サービス側 | 手元の端末・クラウドの sandbox | 常駐先のマシン、または選んだ terminal backend |

[ループエンジニアリング](loop-engineering.md#ループの型)の分類では、Hermes の得意分野は**時間型と能動型**のループです。

## 2. 全体像 — 4 つの層

| 層 | Hermes での実体 | 確認すること |
|---|---|---|
| **入口（gateway）** | `hermes gateway`。Telegram・Discord・Slack・WhatsApp・Signal・Email など多数のプラットフォームを 1 プロセスで受ける。cron の tick もこのプロセスが担う | 誰が話しかけられるか（allowlist・DM pairing）。gateway を止めると cron も止まる |
| **エージェント本体** | ツール呼び出しのループ、Skills、memory、subagent、MCP 接続 | 承認モード（`approvals.mode`）、有効にするツール（`hermes tools`）|
| **手を動かす場所（terminal backend）** | local・Docker・SSH・Singularity・Modal・Daytona・Vercel Sandbox の 7 種類 | コマンドがどのマシンのどの権限で走るか |
| **モデル** | Nous Portal・OpenRouter・Anthropic・OpenAI・独自 endpoint・ローカル | 送信先、課金、モデルごとの tool calling の安定性 |

これとは別に、設定・API キー・セッション・cron を管理する **Web ダッシュボード**（`hermes dashboard`、既定は `127.0.0.1:9119`）と、デスクトップアプリがあります。[ハーネス](harness.md)の言葉でいえば、Hermes は**ハーネスとエージェント本体を 1 つにまとめた製品**です。QM や Kiro Crew のように Claude Code・Codex を部品として差し替える構成ではありません。

| 提供物 | `提供元` / `状態` |
|---|---|
| Hermes Agent 本体（CLI・gateway・TUI） | Official（Nous Research） / GA（v0.22.0 から SemVer の安定版チャネルが既定。2026-10-21 時点の最新は v0.22.2） |
| Nous Portal（モデルと Tool Gateway のサブスクリプション） | Official（Nous Research） / GA |
| VPS 事業者の 1-click テンプレート（動画の Hostinger など） | Community（ホスティング事業者が用意したもの。Nous Research の提供物ではない） |

## 3. どこで動かすか

常駐エージェントは「電源が入っている場所」に住みます。動画が VPS を選ぶのは、ノート PC を閉じても止まらないからです。

| 置き場所 | 向いている場合 | 注意 |
|---|---|---|
| 手元の PC（Linux / macOS / WSL2 / Windows ネイティブ / Android の Termux） | まず試す。ローカルのファイルやモデルを使う | スリープ・再起動で gateway と cron が止まる。エージェントは**自分の PC のアカウント権限**で動く |
| VPS（月額固定のサーバー） | 24 時間動かす。動画の構成 | サーバーの更新・ファイアウォール・ダッシュボードの公開範囲を自分で管理する。業務データを置いてよいか社内規程を確認する |
| サーバーレスの terminal backend（Modal・Daytona） | 使わない時間の費用を抑える。アイドル時に休止し、必要時に復帰する | gateway 自体はどこかで常駐が要る。backend の課金と保存期間を確認する |

> どの置き場所でも、**コマンドを実行する場所は terminal backend の設定で別に決まります**。VPS に置いた Hermes でも `local` のままなら、そのサーバー上で直接コマンドが走ります。分離したい場合は 8 節のとおり Docker などのコンテナ backend を選びます。

## 4. 最小の手順

ここでは自分のマシンや VPS に直接入れる場合を示します。VPS 事業者のテンプレートを使う場合は、インストールまでが済んだ状態から 4-2 以降に進みます（テンプレートの構成は提供元の説明を確認してください）。

### 4-1. インストール

Linux / macOS / WSL2 の**シェル**で実行します。

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Windows ネイティブは **PowerShell** で `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` を実行します。インストール先は Linux 系が `~/.hermes`、Windows ネイティブが `%LOCALAPPDATA%\hermes` です。`curl | bash` は配布元のスクリプトをそのまま実行するため、実行前に [README](https://github.com/NousResearch/hermes-agent) の記載と URL が一致していることを確認してください（[同名の別物という入口](skill-security.md#6-同名の別パッケージという入口)）。

### 4-2. モデルを選ぶ

同じシェルで実行します。

```bash
hermes setup
```

セットアップウィザードでプロバイダとモデルを選びます。後から変えるときは `hermes model`、会話の中では `/model` です。選び方は 5 節を参照してください。

### 4-3. Telegram とつなぐ

1. Telegram で `@BotFather` に `/newbot` を送り、bot を作ってトークンを受け取る（トークンは秘密情報。漏れたら `/revoke`）
2. `@userinfobot` などで**自分の数値のユーザー ID** を調べる（ユーザー名ではない）
3. シェルで `hermes gateway setup` を実行し、`TELEGRAM_BOT_TOKEN` と `TELEGRAM_ALLOWED_USERS`（自分の ID）を設定する。値は `~/.hermes/.env` に保存される
4. `hermes gateway` で起動し、Telegram から bot に話しかけて応答を確かめる

`TELEGRAM_ALLOWED_USERS` を設定しない場合、gateway は**全員を拒否**します。これは安全側の既定です。動かないからといって `GATEWAY_ALLOW_ALL_USERS=true` にしないでください（8 節）。

### 4-4. 常駐させる

```bash
hermes gateway install
```

Linux は systemd、macOS は launchd、Windows はタスクスケジューラに登録されます。サーバーの起動時から動かすには Linux で `sudo hermes gateway install --system` を使います。ログは `journalctl --user -u hermes-gateway -f` で追えます。

## 5. モデルの接続先を選ぶ

| 接続先 | 向いている場合 | 確認すること |
|---|---|---|
| **Nous Portal**（`hermes setup --portal`） | 1 回の OAuth で多数のモデルと Tool Gateway（Web 検索・画像生成・TTS・クラウドブラウザ）をまとめて使う。公式ドキュメントの推奨経路 | 無料プランは無料モデルのみで、Tool Gateway を含むのは有料プラン。ツールの利用もモデルと同じクレジットから引かれる（[Nous Portal](https://portal.nousresearch.com/)） |
| **OpenRouter** | 複数社のモデルを従量で切り替える | `provider_routing` で送信先を絞れる。どの事業者へ送られるかを確認する |
| **各社の API キー**（Anthropic・OpenAI など） | 契約済みの API をそのまま使う | 従量課金。キーは `~/.hermes/.env` に置き、`chmod 600` にする |
| **Claude Code / Codex のログインを借りる** | 手元にある CLI のログインを流用する | Anthropic の経路は**公式ドキュメントが「Claude Pro では使えない」と明記**し、Max プランに上乗せする追加クレジット（extra usage）を消費する。借りたログインを Hermes が更新すると、元の CLI の refresh token が無効になり得るため、避けたいなら `auth.adopt_external_logins: false` |
| **ローカル**（Ollama・llama.cpp） | データを外へ出さない。従量費用をなくす | Hermes は **64K トークン以上の context** を要求する。Ollama は既定が小さいので `OLLAMA_CONTEXT_LENGTH` を設定し、llama.cpp は `--jinja` がないと tool calling が動かない |

動画は費用を抑えるために DeepSeek の Flash 系を選んでいます。安いモデルは 1 回の費用が小さい一方、**ツール呼び出しの失敗や手順の取りこぼしが起きやすく、それが再試行と人の確認の手間に変わります**。監視のように同じ手順を繰り返す仕事では、6 節の方法で「LLM を呼ぶ回数」自体を減らすほうが効きます。

> 各社の利用規約で、借りたログインや別のクライアントからの利用が認められているかは、Hermes のドキュメントには書かれていません。業務で使う場合は契約側の条件を確認してください。

## 6. 動画の watcher を組み直す — 変化があったときだけ知らせる

動画の「最初の仕事」は、航空券の価格を決まった間隔で確認し、**変化があったときだけ**メッセージを送るものです。Hermes の cron には、この「何もなかった回を黙らせる」仕組みが 3 段階あります（[Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)）。

| 仕組み | 動き | LLM の費用 | 向いている場合 |
|---|---|---|---|
| **`[SILENT]`** | エージェントの最終応答に `[SILENT]` が入っていれば配信しない。出力はローカルに保存される。**失敗は必ず配信される** | 毎回かかる | 変化の判定に LLM の解釈が要る（ページの文章から読み取るなど） |
| **`wakeAgent` ゲート** | 事前に走るスクリプトの最終行が `{"wakeAgent": false}` なら、その回はエージェントを起動しない | 変化がない回は**かからない** | 変化の有無は機械的に判定でき、変化があったときだけ要約や判断を LLM に任せたい |
| **`no_agent` ジョブ** | スクリプトだけを動かし、stdout が空なら無音。非 0 終了やタイムアウトはエラーとして通知 | かからない | 通知文もスクリプトで作れる |

価格の監視なら、**取得と比較はスクリプト、変化があったときの説明だけ LLM** という `wakeAgent` の形が費用と確実さの釣り合いが取りやすい構成です。スクリプトは `$HERMES_HOME/scripts/` に置いたファイルだけが実行でき（コマンド文字列は拒否される）、`.sh` は bash、それ以外は Python で動きます。

ジョブは会話の中から `/cron add "every 6h" "…"` のように作るか、自然言語で頼むと Hermes が `cronjob_manage` ツールで作ります。CLI では `hermes cron create` です。`--script` などの指定方法は版で変わり得るため、`hermes cron create --help` で確認してください。

組む前に、cron の性質を 4 つ押さえておきます。

| 性質 | 意味 | 備え |
|---|---|---|
| **毎回新しいセッション** | 前回の価格を覚えていない | 比較の基準は自分のファイルに保存する。前回の出力を渡すなら `continuity=true` |
| **承認が要る操作は既定で拒否** | `approvals.cron_mode` の既定は `deny`。人がいない cron では、危険と判定されたコマンドは止まる | cron で必要な操作は事前に `command_allowlist` で明示する。全体を `off` にしない |
| **exactly-once は保証されない** | 途中で落ちた回は `unknown` になり、自動では再実行されない | 予約や購入のような外部への書き込みを cron に持たせない。持たせるなら[実行 ID で重複を確かめる](loop-engineering.md#定期実行の再実行と外部副作用--claude-code-21302) |
| **cron から cron は作れない**（既定） | `cron.allow_agent_scheduling` の既定は `false` | 増殖を防ぐ安全側の既定。変える理由がなければそのままにする |

> 価格比較サイトや航空会社のサイトは、自動取得を利用規約で禁じていることがあります。取得先の規約を確認し、可能なら公式の API や価格アラート機能を使ってください。

## 7. 費用の構造

動画は「サーバーの固定料金 + 1 メッセージあたり 1 セント未満」と説明しています。成り立つのは、**安いモデルを使い、LLM を呼ぶ回数が少ない**場合です。費用は次の 4 つに分けて見積もります。

| 費用 | かかり方 | 増える要因 |
|---|---|---|
| 置き場所 | VPS は月額固定（初回価格と更新価格が違うことが多い）。手元の PC なら電気代のみ | 常時稼働のためのスペック、バックアップ |
| モデル | 入出力のトークン数に比例 | 長い会話、ツール出力の大きいページ取得、高価なモデル、失敗による再試行 |
| ツール | Web 検索・ブラウザなどの Tool Gateway や外部 API の従量 | ページを毎回ブラウザで開く監視 |
| **見えにくい自動処理** | ターン終了後の**背景レビュー**（memory と Skill の更新）、`approvals.mode: smart` のリスク判定、cron の tick | 頻度の高い cron、背景レビューを高価なモデルで回す設定 |

見えにくい自動処理は設定で抑えられます。背景レビューには `auxiliary.background_review` で安いモデルを指定したり、`max_input_tokens` で上限を付けたり、`enabled: false` で止めたりできます。cron は 6 節の `wakeAgent` で「呼ばない回」を作ります。使用量はダッシュボードの Analytics で確認できます。

## 8. 公開前の最低ライン

メッセージアプリから話しかけられる常駐エージェントは、**サーバーのシェルを外から操作できる入口**と同じ重さで扱います（[Security](https://hermes-agent.nousresearch.com/docs/user-guide/security)）。

| 項目 | 最低限やること | 理由 |
|---|---|---|
| 話しかけられる人 | `TELEGRAM_ALLOWED_USERS` などのプラットフォーム別 allowlist か DM pairing（`hermes pairing approve <platform> <code>`）を使う。`GATEWAY_ALLOW_ALL_USERS=true` にしない | bot のユーザー名は検索で見つかる。許可されていない人の依頼でもコマンドが走り得る |
| コマンドの承認 | `approvals.mode` は既定の `smart` か `manual` にする。`off`（`--yolo`・`HERMES_YOLO_MODE=1`）にしない | `smart` は補助 LLM でリスクを判定し、判断がつかないものは人に聞く。`off` でも外せない最低限のブロック（`rm -rf /` など）はあるが、それ以外は通る |
| 実行場所 | `terminal.backend: docker` などのコンテナ backend にし、CPU・メモリ・ディスクの上限を付ける | コンテナ backend は `--cap-drop ALL`・`no-new-privileges` などで動く。ただし**コンテナ backend では危険コマンドの検査が省かれ、コンテナが境界になる**。コンテナに何をマウントするかが重要になる |
| 秘密情報 | `chmod 600 ~/.hermes/.env`。プロバイダの API キーや bot のトークンを `terminal.env_passthrough` に入れない | `write_file` は `.env` や `~/.ssh/` への書き込みを拒否するが、terminal ツールは同じ OS ユーザーで動くため、これは境界ではないと公式が明記している |
| ダッシュボード | `127.0.0.1` のまま使い、遠隔からは SSH トンネルか Tailscale で入る。インターネットに出すなら OAuth / OIDC の認証プロバイダを設定する | ダッシュボードは `.env` を読み書きし、エージェントのコマンドを実行できる。非ループバックでは認証プロバイダがないと起動を拒否する（fail-closed） |
| 実行ユーザー | gateway を root で動かさない | エージェントの権限がそのままサーバー全体の権限になる |
| 更新 | `hermes update` で追従し、release notes のセキュリティ修正を読む | v0.21.6（2026-10-08）はダッシュボード認証の迂回・email gateway の allowlist 突破・信頼できないリポジトリの git filter の実行などを修正した |

AGENTS.md や SOUL.md などのコンテキストファイルは、system prompt に入る前に注入のパターンを検査され、検出されると `[BLOCKED: ...]` として読み込まれません。ただし公式は**見た目のパターンによる判定であり、意図は判定しない**と明記しています。Web ページやメールなど外から届く内容は、引き続きデータとして扱ってください（[自然言語の判断と強制する制御を分ける](skill-security.md#自然言語の判断と強制する制御を分ける)）。

> 非エンジニアが業務で試す前に確認する項目は [生成AIを業務で安全に使う](../business/safety.md) にまとめています。

## 9. Skills と記憶

Hermes の Skills は [agentskills.io](https://agentskills.io/specification) 互換の `SKILL.md` で、`~/.hermes/skills/` が正本です。Claude Code や Codex と大きく違うのは、**エージェント自身が `skill_manage` ツールで Skill を作り、使いながら書き換える**ことです。記憶も同じで、`~/.hermes/memories/` の `MEMORY.md`（エージェントのメモ）と `USER.md`（利用者のプロフィール）を自分で更新し、全セッションを `~/.hermes/state.db` に残して全文検索します。

| 対象 | 既定の動き | 人が確認できるようにする設定 |
|---|---|---|
| Skill | 作成・更新はすぐ反映される | `skills.write_approval: true` で保留にし、`/skills diff <id>` を読んでから `/skills approve` / `reject` |
| memory | 保存はすぐディスクに反映され、次のセッションから prompt に入る | memory の `write_approval: true` で保留にし、`/memory pending` → `/memory approve` |
| 背景レビュー | ターン終了後に memory と Skill の更新を検討する | `auxiliary.background_review.enabled: false` で止める |

自動で育つことが Hermes の売りですが、**育った手順を誰もレビューしていない**状態にもなります。運用の考え方と Hub からの導入時の確認は [Skill / Plugin のセキュリティ](skill-security.md#エージェントが自分で書く-skill) にまとめています。

### Skills Hub と他ツールとの共有

`hermes skills install` は、公式の Hub に加えて `skills-sh`・`github`・`url`・`clawhub`・`lobehub` などの取得元から Skill を入れられます。インストール時には必ずセキュリティスキャンが走り、取得元の信頼レベル（`builtin` / `official` / `trusted` / `community`）と合わせて判定されます。`--force` で注意・警告の判定は越えられますが、`dangerous` の判定は越えられません。更新はインストール時のハッシュと比べて検出し、手元で編集した Skill は `--force` なしでは上書きしません。

他のツールと同じ Skill を使う場合は、`~/.hermes/config.yaml` の `skills.external_dirs` に `~/.agents/skills` などを並べます。同名の Skill は project → `~/.hermes/skills/` → `skills.create_dir` → `external_dirs` の順で上位が勝ちます。ただし**外部ディレクトリは書き込み保護の境界ではなく、Hermes が書ける場所ならエージェントが変更し得る**と公式が明記しています。`~/.agents/skills` は [Codex の個人用 Skill の置き場所](../codex/README.md)でもあるため、そのまま指定すると Hermes が育てた変更が Codex 側にも入ります。共有するなら読み取り専用の複製を指すか、`skills.write_approval` を有効にしてください。

リポジトリ内の `.hermes/skills/` と `.agents/skills/` は、`hermes skills trust` で信頼するまで自動では読み込まれません。clone したリポジトリの Skill が勝手に効かない、安全側の既定です。

### 他のエージェントから移る

OpenClaw を使っていた場合、セットアップウィザードが `~/.openclaw` を検出して移行を提案します。手動では `hermes claw migrate` で、`--dry-run` で内容を確認でき、`--preset user-data` で秘密情報を除外できます。移行した Skill は `~/.hermes/skills/openclaw-imports/` に入ります。**移行元で動いていたことは、Hermes での安全を意味しません**。Hermes ではエージェントが Skill を書き換えるため、取り込んだ Skill の `scripts/` と外部への通信を読んでから使ってください。

## 10. ほかの常駐型ハーネスとの違い

| 観点 | Hermes Agent | [Kiro Crew](harness.md#kiro-crew--常駐して動き続けるハーネス) | [QM](harness.md#qm--ソースを読めるハーネス実装) | [Letta Code](agent-memory.md) |
|---|---|---|---|---|
| 想定利用者 | 個人（自分専用のエージェント） | 個人・チームの開発者 | 組織（人ごと・部屋ごとのスコープ） | 記憶を持って学習し続けるエージェントを立てたい人 |
| エージェント本体 | 自前。モデルだけを選ぶ | Kiro CLI（Claude Code / Codex / KAS は Preview） | Claude Code / Codex / OpenCode / Pi を駆動 | 自前 |
| 入口 | 多数のメッセージアプリ、CLI、ダッシュボード、デスクトップアプリ | デスクトップ、Web、CLI、Slack / Discord / Teams | Slack、Web | CLI、デスクトップ、Slack など |
| 起動条件 | cron（`[SILENT]`・`wakeAgent`・`no_agent`）、メッセージ | 定期ジョブ、webhook、メッセージ、heartbeat | cron、メッセージ | 対話が中心（定期実行の有無は製品の現行情報を確認） |
| 安全の既定 | 承認 `smart`、cron は `deny`、allowlist なしなら全員拒否 | namespace / Seatbelt の分離強度を選ぶ | Strict / Auto / Dangerous のポスチャ | tool 実行の permission mode |
| 費用の前提 | 本体は無料。モデル・ツール・置き場所を自分で選ぶ | Kiro プランの利用枠 | 自社のクラウド・Postgres・運用担当 | 既定は Letta Cloud。local backend も選べる |

Hermes は**個人が自分の置き場所とモデルを選べる自由度**が最も高く、そのぶん**承認・公開範囲・費用の既定を自分で守る責任**も最も大きくなります。

---

## 関連ドキュメント

- [AI エージェントの実行基盤（ハーネス）](harness.md) — Kiro Crew・QM・OpenAI Agents API など、常駐・無人実行の土台の比較
- [ループエンジニアリング](loop-engineering.md) — 時間型・能動型のループと停止条件。定期実行の製品比較
- [エージェントの記憶基盤](agent-memory.md) — GBrain・Mem0・Graphiti・Letta。Hermes の外部メモリプロバイダとして使えるものもある
- [Skill / Plugin のセキュリティ](skill-security.md) — Hub から入れる Skill と、エージェントが自分で書く Skill の確認
- [長時間タスクの信頼性設計](agent-reliability.md) — 無人実行の再試行・冪等性
- [エージェントに外部操作を与える手段の選び方](tool-selection.md) — Web 取得・ブラウザ操作を与えるときの承認の重さ
- [生成AIを業務で安全に使う](../business/safety.md) — コードを書かない方が業務で試す前の確認
- [obra/superpowers](superpowers.md) — Hermes Agent 向けの導入手順もある Skill 集

## 参考リンク

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — README（MIT、インストール、gateway、terminal backend、OpenClaw からの移行）
- [Releases](https://github.com/NousResearch/hermes-agent/releases) — v0.22.0「The Threshold Release」（2026-10-13）、v0.22.2（2026-10-15）、v0.21.6 のセキュリティ修正（2026-10-08）
- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/) — 公式ドキュメント
  - [Security](https://hermes-agent.nousresearch.com/docs/user-guide/security) — 承認モード、allowlist と DM pairing、コンテナ隔離、秘密情報、注入対策
  - [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging) ／ [Telegram](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram) — 対応プラットフォーム、常駐方法、bot の作成
  - [Cron Scheduling](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) — `[SILENT]`・`wakeAgent`・`no_agent`、実行の性質
  - [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) — `skill_manage`、`write_approval`、Hub、`external_dirs`
  - [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) — `MEMORY.md` / `USER.md`、`state.db`、背景レビュー、外部プロバイダ
  - [Web Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard) — 既定の bind と認証
  - [Providers](https://hermes-agent.nousresearch.com/docs/integrations/providers) — Nous Portal・OpenRouter・Anthropic・Codex・ローカルモデル
- [Nous Portal](https://portal.nousresearch.com/) — プランとモデル単価（2026-10-21 確認）
- [Build Your First AI Agent in 20 Minutes (No Coding)](https://www.youtube.com/watch?v=rCkYVxOX-dI) — 本ページの起点にした動画（Metics Media、2026-10-19。概要欄にアフィリエイトリンクあり）
