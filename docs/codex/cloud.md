# Codex Cloud — 開発環境を再利用し、結果をレビューする

> **対象ツール**: Codex Cloud・Codex Security Cloud（OpenAI） ｜ **実行環境**: Chat UI / Cloud ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-10-02

端末を閉じた後もコードの調査・修正・テストを進めたいときは、Codex Cloudの公開済み環境からタスクを始めます。環境にはリポジトリ、依存関係、ツール、アクセス設定をまとめ、各タスクは独立した作業領域で動きます。完了後は差分とテスト結果を確認して、コミットやPR作成へ進みます。

## 1. 最初に選ぶものと提供状況

| 目的 | 入口 | 提供元 | 状態・前提（2026-10-02確認） |
|------|------|--------|-----------------------------|
| 同じ開発環境を使ってコードの調査・修正を任せる。 | [Codex Cloud](https://learn.chatgpt.com/docs/cloud)の公開済み環境。 | Official | 参照した導入資料にGA / Previewの区分は明記なし。ChatGPTでのサインイン、対象リポジトリへのアクセス、workspaceの利用設定が前提。 |
| GitHubのコードを検査し、新しいcommitの指摘を確認する。 | Codex Security Cloud plugin。 | Official | **Research Preview**。[DevDay公式まとめ](https://learn.chatgpt.com/docs/whats-new/devday-2026)の表記に従う。GitHub接続と互換性のあるCloud environmentが必要。 |
| 手元のリポジトリを検査する。 | ローカル用[Codex Security plugin](https://learn.chatgpt.com/docs/security/plugin)。 | Official | Cloud版とは別plugin。導入条件はローカル版の公式ガイドで確認する。 |

利用可能なプランや管理者権限は[公式の料金・使用量](https://learn.chatgpt.com/docs/pricing)と[Cloud導入ガイド](https://learn.chatgpt.com/docs/cloud)で確認します。EnterpriseではCloudタスクの利用と、共有環境の作成・編集を管理する権限が別です。

本ページは開発者がCodex製品を使う手順です。自社アプリからdurable sessionを制御する[Agents API](../dev-methods/harness.md#openai-agents-api--codexハーネスをマネージドapiで使う)のsandbox設定は、そのAPI側の設計として確認してください。

## 2. 環境を準備し、最初のタスクを動かす

操作はChatGPTのWebまたはdesktop appで行います。作成前に、対象のGitHubリポジトリ、必要なruntime・packageの版、テストコマンド、接続するサービスを決めておきます。

1. 新しいタスクで **Work in → Cloud → Select environment → Create environment** を選びます。
2. 対象のGitHubリポジトリを選びます。接続を求められたら、そのリポジトリへアクセスできるアカウントで接続します。
3. **Get started** で準備を始めます。Codexが依存関係とツールを調べ、セットアップを実行・確認します。必要な版やテスト方法を会話で補います。
4. セットアップ報告、設定、準備されたファイル、テスト結果を確認し、未完了の作業を解消します。
5. 設定を保存し、**Publish** を選びます。**Environment published** を確認します。
6. **Start a new task** で目的を伝えます。結果の差分・テスト・残る課題を確認してから、コミットやPR作成へ進みます。

既存の公開済み環境を使う場合は、環境を選んでタスクを始めます。モバイルからも利用できますが、環境の作成・公開はWebまたはdesktop appで済ませます。同じタスクを開けば作業を継続し、新しいタスクを作れば公開済みの環境から別の作業を始めます。詳しくは[Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments)を参照してください。

## 3. Save・Publish・Republishで何が変わるか

| 操作・状態 | 変わるもの | 確認すること |
|-----------|------------|--------------|
| Save | 設定を保存する。一部の設定はセットアップ中の環境へすぐ反映される。 | 設定の保存だけで、新規タスク向けの準備済みファイルが公開されたとは判断しない。 |
| Publish | 準備済みfilesystemを新規タスク向けに公開する。 | 公開完了と、新規タスクでツール・テストが使えることを確認する。 |
| Republish | 変更して再確認した環境を、新規タスク向けに更新する。 | **Settings → Codex Cloud → Environments → … → Edit** で変更し、保存・再公開後に新規タスクで確認する。 |
| 既存タスク | そのタスク自身のファイル、未コミット変更、導入済みツールを保持する。 | 環境の再公開後も、既存タスクが更新済み環境へ置き換わるとは扱わない。 |

セットアップには、依存関係を準備する **Install script** と、サービスの起動・準備完了を確認する **Start skill** を記録できます。必要な変更を会話で伝え、確認してから再公開します。保存された状態はGitの代替にはならないため、重要な成果はコミットや必要な出力として残します（[公式の状態管理](https://learn.chatgpt.com/docs/environments/cloud-environments#reuse-and-update-saved-state)）。

## 4. 接続・secret・共有を確認する

| 設定 | 選ぶ場面・確認事項 |
|------|-------------------|
| Environment variable | プログラムが値を直接読む必要がある場合。値はプログラムへ直接渡る。 |
| Network secret | 指定したHTTPSサービスへcredentialを送る場合。プログラムにはplaceholderを渡し、proxyが許可先への通信で実値へ置換する。HTTPSのport 443が条件。 |
| Allowed domains | package registryやAPIの接続先を許可する。接続先の許可だけでは、認証情報やサービス内の権限は付与されない。 |
| Personal vault | 利用者ごとの値を供給する。共有環境が値を要求しても、共有されるのは要求であり、個人credentialではない。 |
| Privacy / Who can use | Enterprise workspaceへ環境を共有する範囲を決める。環境に持たせたcredentialや準備済みファイル、共有のサービスアクセスも確認する。 |

Network secretは通常の環境変数と別のkeyにし、必要な送信先を **Allowed domains** に設定します。環境所有のnetwork secretを保存すると、制限付きinternet accessへ送信先が追加されます。直接渡す変数や個人の値は送信先を追加しないため、実際のnetwork policyも確認します（[公式の変数・secret設定](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets)）。

共有環境を使えることは、他人のタスクを閲覧・編集できることを意味しません。各タスクは別の作業領域を持ちます。リポジトリと個人接続の権限は実行アカウントに依存し、環境所有のcredential・VPN・cloud identityは共有アクセスを与える場合があります。共有前にその範囲を確認します。Enterpriseの[Agent Security](https://learn.chatgpt.com/docs/enterprise/agent-security)による要件も環境の接続先設定と併せて確認します。

## 5. Security Cloudで検査結果をレビューする

Codex Security CloudはGitHubリポジトリを検査し、指摘・検証証拠・修正案を提示します。SASTや人のセキュリティレビューと併用する位置づけです。検証に失敗した指摘は未検証として残るため、再現に使ったコマンド・ログと検証結果を確認します（[公式FAQ](https://learn.chatgpt.com/docs/security/faq)）。

### 単発のリポジトリ検査

1. ChatGPTのWebまたはdesktop appで **Plugins** を開き、**Codex Security Cloud** を導入・有効化し、pluginまたはsidebarから開きます。
2. **New scan** で対象リポジトリを選びます。必要なら **Connect GitHub** で接続し、見つからないリポジトリは接続先とアクセス権を確認します。
3. 互換性のある **Cloud environment** を選び、**What to scan → Repository → Start scan** で始めます。環境がなければ、その画面の **Create environment** から準備します。
4. **Scans** で進行と成果を確認し、**Findings** で対象コード・検証証拠・修正の指針を読みます。
5. **Fix with Codex** が提示された指摘では修正案を生成し、差分とテストをレビューしてから **Create draft pull request** を選びます。

### 新しいcommitを継続して確認する

| 操作 | 確認すること |
|------|--------------|
| **New scan → Commit changes → Create** | 対象リポジトリと互換性のある環境を選ぶ。 |
| **Repositories → Monitoring settings** | 環境、確認する履歴の日数、監視の有効・一時停止を調整し、保存する。 |
| **Project context** | 生成されたthreat model（入口、信頼境界、認証の前提など）を読み、実際の構成に合わせて修正・保存する。 |

これらの操作は[Security Cloud setup](https://learn.chatgpt.com/docs/security/setup)に従います。threat modelの目的と見直し方は[公式ガイド](https://learn.chatgpt.com/docs/security/threat-model)を参照してください。

### 新しいCloud環境とLegacyのリンクを区別する

2026-10-02確認時点で、新しい環境の公式ページは **`cloud-environments`（複数形）**、[Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment)は **`cloud-environment`（単数形）** です。LegacyはCode Review・Linear・GitHub連携向けの環境を引き続き扱います。新しい環境のガイドでは廃止予定が示されていますが、終了日は明記されていません。

Security Cloud setup / FAQの環境設定リンクは、確認時点では単数形のLegacyページを指しています。**Security Cloud画面で互換性のある環境を選び、該当する公式手順を確認してください。** 本ページ2〜4節のPublish・network secretの説明を、そのままLegacyの設定へ当てはめないようにします。Legacyのsecretはセットアップ時だけ使えるなど、設定の意味が異なります。

## 6. 使う場面と結果の確認

以下は本ガイドの説明例です。実アカウントで検証済みの運用例ではありません。

| 場面 | 進め方 | 人が確認するもの |
|------|--------|------------------|
| 翌朝に修正案を確認したい。 | 公開済みの共通環境から、対象・完了条件・テストコマンドを指定したCloudタスクを開始する。 | 差分、テスト結果、未完了の項目。環境が準備されていれば、端末を閉じても作業は継続する。 |
| 新しいcommitの指摘を継続して読みたい。 | Security CloudでCommit changesの監視を設定し、threat modelを見直す。 | 対象コードと検証証拠、修正案の影響。draft PRを開いた後もCIとレビューを行う。 |

Cloudタスクの指示例は次のとおりです。ChatGPTで公開済み環境を選んでから入力します。

```text
〈Issue〉の修正案を作ってください。対象は〈リポジトリ・機能〉です。
完了条件は〈期待する動作〉、検証コマンドは〈テストコマンド〉です。
変更した内容、テスト結果、未確認の点をまとめ、PR作成前に差分を見せてください。
```

## 7. 利用前に確認する制約

2026-10-02時点の新しいCloud environmentsでは、Computer / browser use、GitLab、自前ホストのGitHub Enterprise Serverは未対応です。リポジトリ内のSkillsは使えますが、ローカルPCの個人Skillsは同期されません。GUI操作や個人のセットアップを前提とするタスクは、[公式のCurrent limitations](https://learn.chatgpt.com/docs/environments/cloud-environments#current-limitations)を確認してから実行先を選びます。

接続に失敗した場合は、接続先hostnameの許可、サービスの認証・権限、network secretの送信先とport、workspaceの要件を順に確認します。設定変更後は保存・公開または再公開し、**新規タスク**で必要なサービスとテストが動くことを確認します。

## 参考リンク

- [Codex Cloud](https://learn.chatgpt.com/docs/cloud) — 製品の導入と利用場面。
- [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) — 公開・更新、secret、共有、現在の制約。
- [Codex Cloud (Legacy)](https://learn.chatgpt.com/docs/environments/cloud-environment) — Legacyの設定。新しい環境との違いを確認する。
- [Security Cloud setup](https://learn.chatgpt.com/docs/security/setup) / [FAQ](https://learn.chatgpt.com/docs/security/faq) — scan、commit監視、検証・修正案。
- [DevDay 2026](https://learn.chatgpt.com/docs/whats-new/devday-2026) — 2026-09-29の発表まとめとResearch Previewの表記。
