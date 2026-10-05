# Claude Code の Mods — Claude Code の中で動くプラグイン

> **対象ツール**: Claude Code ｜ **実行環境**: CLI（ターミナル）／デスクトップアプリの Code タブ ｜ **対象読者**: エンジニア・組織の導入担当 ｜ **最終更新**: 2026-10-05

> Claude Code 2.1.287（2026-10-01）で、プラグインが Claude Code の**内部で関数として動き**、画面の描画やツール呼び出しまで書き換えられる **Mods** が加わりました。Skill や MCP と違って「ローカルの実行コードを Claude Code の中に入れる」仕組みなので、**便利さと同じ重さの信頼の問題**があります。このページは、何ができるか・何が既存の hooks と違うか・入れる前に何を確認するか・組織でどう止めるかを整理します。

[Claude Code のカスタマイズ機能](basics.md)にある Skill・フック・MCP は、どれも Claude Code の**外側**から働きかける仕組みでした。Mods は**内側**で動きます。公式ドキュメントでは、mod を「Claude Code の見た目と振る舞いを変えるプラグイン」と定義しています。

> **版と提供状況**: 公式ドキュメントによると、Mods は **Claude Code v2.1.287 以降で既定で有効**です。公式ドキュメントに Preview / GA の区別は見当たらなかったため、このページでは状態ラベルを付けません。events・メソッドは**版ごとに変わり得る**と公式が明記しており、詳細は手元の版が生成する型定義を優先してください（[4 節](#4-最小の-mod-を作って検証する)）。

---

## 1. Mods とは何か — 既存の拡張との違い

mod は、JavaScript / TypeScript の**イベントハンドラ**の集まりです。ツール呼び出し・プロンプト送信・画面の描画といったイベントが起きると Claude Code が関数を呼び、関数は次のいずれかを選べます。

| できること | 意味 | 例 |
|-----------|------|----|
| **Observe**（観察） | 何が起きたかを記録し、そのまま通す | ツール呼び出しの回数を数える |
| **Rewrite**（書き換え） | イベントを変えてから通す | スピナーの横に回数を足す |
| **Answer**（肩代わり） | 通常の処理を実行せず、自分で結果を返す | 危険なコマンドを断る |

mod は既存の拡張と次のように使い分けます（公式の比較表を、このガイドの観点で整理しました）。

| | Mod | フック（settings hook） | Skill | MCP サーバー |
|--|-----|------------------------|-------|-------------|
| 正体 | プラグイン内の関数。Claude Code が自分のプロセスで呼ぶ | イベントごとに実行されるシェルコマンド・HTTP・プロンプト | Claude が読む `SKILL.md` | 外部プロセスやサービス |
| 変えられるもの | ツール呼び出し・プロンプト・コマンド・ターン・**画面の描画** | 続行可否・引数・結果・追加コンテキスト | Claude の知識と手順 | Claude が使えるツール |
| 画面に描けるか | **描ける** | 描けない | 描けない | 描けない |
| 書くもの | JavaScript / TypeScript | スクリプトと `settings.json` | Markdown | 任意の言語のサーバー |
| 選ぶ場面 | ペイン・プロンプト上のバンド・独自コマンド・イベントの書き換え | 手持ちのスクリプトでブロック・許可・記録したい | 同じ指示を毎回貼っている | 外部システムへ届かせたい |

**迷ったら、まず既存の仕組みで足りるかを確認します。** 「危険なコマンドを止める」だけなら settings hook（[フック](basics.md#フック)）で足ります。mod を選ぶ理由は、画面に何かを描く・コマンドを足す・イベントを書き換える、のいずれかが必要なときです。

> **用語**: 公式ドキュメントでは、mod の関数も settings hook も「hook」と呼びます。区別のため、公式ページでは mod 側を hook、設定ファイル側を **settings hook** と書き分けています。このページも同じ書き分けに従います。

### 何ができるか

- **使える画面を描く**: トランスクリプトの横の**ペイン**や、プロンプト上の**バンド**（タブ・ボタン・テキスト欄つき）
- **Claude Code 自身の画面を描き直す**: ツール呼び出しの行・スピナー・Claude が質問するダイアログなど
- **ツール呼び出しやリクエストに割り込む**: 呼び出しを止めて利用者に質問する、ツールを実行せずに答える、リクエストを別のモデルへ送る
- **独自の `/command` を足す**: Claude のターンを待たず、Claude が作業中でも即座に自分の関数を実行する
- **hook 間で状態を共有する**: 同じファイル内の変数を共有できる（例: 一方が回数を数え、他方がスピナーの横に出す）

### 公式のサンプル

Anthropic は [claude-code-playground の `claude-code/mods`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods) にサンプルを置いています（**無保証・現状のまま**の共有）。

| サンプル | 内容 |
|---------|------|
| `token-weather` | コンテキストウィンドウの「予報」をプロンプトの上に描く |
| `blast-radius` | `rm -rf` や force push など危険なシェルコマンドを止め、影響範囲を示して、進める・中止するのボタンを出す |
| `replay-theater` | 直前のターンでのファイル編集を順に再生する `/replay` を足す |

---

## 2. 動く場所 — 描画は端末とデスクトップだけ

mod の hook は、プラグインを読み込むセッションなら**どこでも動きます**。一方、**描画**（ペイン・バンド・置き換えた行）が見えるのは端末とデスクトップアプリだけです。

| 実行場所 | hook は動くか | 描画は見えるか |
|---------|--------------|---------------|
| 端末の `claude`（エディタ内蔵端末・JetBrains プラグインを含む） | 動く | 見える |
| デスクトップアプリの Code タブ（WSL を除く） | 動く | 見える（端末専用の要素を除く） |
| デスクトップアプリの WSL セッション | **動かない**（WSL ではプラグイン非対応） | 見えない |
| VS Code 拡張のチャットパネル | 動く | **見えない** |
| `claude -p` と Agent SDK | 動く | 見えない |
| Remote Control（claude.ai・モバイルから） | 手元のマシン上のセッションで動く | 手元の端末に出る |
| クラウドセッション | クラウドへ届くプラグインなら動く | 見えない |

**VS Code 拡張や `claude -p` では、hook は動くのに描画は出ません。** 「画面に出ないから効いていない」と誤解しないでください。描画する mod は、描けない環境ではトランスクリプトへの 1 行やコマンドの返信に切り替える設計が必要です。

---

## 3. 入れる前に — 信頼の境界を理解する

> **mod は、入れた人の権限で動くコードです。** ファイルの読み書き、プロセスの起動、ネットワーク通信ができ、**サンドボックスの外**で動きます。

公式ドキュメントが挙げる、読み込まれた mod が到達できる範囲は次のとおりです。

| 範囲 | 内容 |
|------|------|
| 利用者として操作する | ユーザーアカウントが触れるファイルの読み書き、プログラムの起動、ネットワーク通信 |
| 秘密を読む | 環境変数や設定ファイル（API キーを含み得る） |
| セッションを見る | 送信するすべてのプロンプトと、Claude のすべてのツール呼び出し |
| セッションを変える | プロンプトやツール呼び出しの書き換え、利用者が入力したかのようなプロンプト送信、別セッションへのメッセージ送信 |
| 確認なしで動く | **承認プロンプトが出る前に**ツール呼び出しを承認する |
| 利用枠を使う | 利用者のプランや API キーでモデルを呼ぶ |

注意が必要な点を 3 つ挙げます。

1. **sandbox は mod を囲いません。** sandbox を有効にしても、隔離されるのは Claude が実行する Bash コマンドです。mod が起動したプロセスは sandbox の外で動きます。
2. **`ask` ルールや自分の `PreToolUse` フックの判断を、mod が上書きできる場合があります。** mod が先にツール呼び出しを承認すれば、`ask` ルールが本来出す確認が出ず、利用者自身の `PreToolUse` フックのブロックも通り得ます（`deny` ルールとの関係は [5 節](#5-組織で止める境界)で扱います）。
3. **承認プロンプトの表示は書き換えられません。** mod は画面の多くを描き直せますが、権限プロンプトが「何を表示するか」は変えられません。

### インストール前に `claude plugin validate` で中身を見る

実行せずに、その mod が**どのイベントを受け、何を Claude Code に頼むか**を一覧できます。プラグインのファイルを取得（例: リポジトリを clone）してから実行します。

```bash
claude plugin validate ./some-mod
```

出力の次の 2 行を読みます（公式ドキュメントの例）。

```text
  ❯ ./register.js hooks: session.start, tool.call, ui.render{component=Pane}
  ❯ ./register.js calls: $.fs.read, $.http.fetch, $.store.set, $.ui.open
```

`calls:` の行で、特に次を確認します。

| 呼び出し | 意味 |
|---------|------|
| `$.fs.read` / `$.fs.write` | 利用者が触れる場所のファイルを読み書きする |
| `$.process.run` / `$.process.spawn` | 利用者としてプログラムを起動する |
| `$.http.fetch` | ネットワークへリクエストする |
| `$.env.get` / `$.settings.read` | 環境変数・設定を読む（API キーを含み得る） |
| `$.env.set` | 以降に起動する Claude Code・コマンド・MCP サーバーの環境変数を変える |
| `$.mcp.call` | 接続済み MCP サーバーのツールを呼ぶ（セッションの権限ルールの下） |
| `$.model.complete` | 利用者のプラン・API キーでモデルを呼ぶ |
| `$.prompt.submit` | プロンプトを送る（利用者本人の発言として送れる） |
| `$.session.send` | 別セッション・サブエージェントの Claude が読むメッセージを送る |

`hooks:` の行では、`tool.call` と `prompt.submit` は**すべてのツール呼び出し・プロンプトを見て変えられる**こと、`tool.check` は**承認プロンプトの前に承認・拒否できる**こと、`session.append` は**会話の各行を保存前に書き換えられる**ことを意味します。

> **この確認でわかる範囲**: `validate` は静的解析で、コードを実行せずに読み取れる範囲を示します。公式は、読み取れない形で mods API を使う mod は**読み込みを拒否する**としています。ただし、これは「安全だと保証する」ものではありません。許可する呼び出しの範囲が、信頼できる作者かどうかと合っているかを人が判断します。

---

## 4. 最小の mod を作って検証する

mod は 3 ファイルです。`.js` / `.ts` は Claude Code が直接読み込むため、Node.js もバンドラも要りません。

```text
first-mod/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json    # modules キーで register.js を指す（これが mod の目印）
    └── register.js
```

`hooks/hooks.json` の `modules` キーがコードのパスを指すことで、プラグインが mod になります。

```json
{
  "description": "The first-mod hooks module",
  "modules": ["./register.js"]
}
```

公式チュートリアルの最小例は、ツール呼び出しの回数を数え、スピナーの横に出します。

```javascript
// hooks/register.js
let calls = 0

export function register(on) {
  // Claude がツールを使う直前
  on('tool.call', async ($, e, next) => {
    calls += 1
    $.ui.invalidate('ui.render')   // 回数を出すため再描画を頼む
    return next(e)                 // ツールは通常どおり実行する
  })

  // スピナーを描くたび
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
  })
}
```

hook が受け取る 3 つの引数は共通です。

| 引数 | 内容 |
|------|------|
| `$` | **mods API**。ファイル・プロセス・ネットワーク・描画など、mod の外へ出る手段はすべてここ |
| `e` | イベントの入力（ツール名・引数など） |
| `next` | 他の mod と Claude Code 本来の処理へイベントを渡し、結果を返す関数 |

**mod の外へ出る手段が `$` だけに限られている**ため、Claude Code は実行前に `claude plugin validate` で `calls:` を列挙できます。この前提を崩さないよう、公式は次のルールを定めています（静的解析が全 hook と全呼び出しを見つけるための条件です）。

- `$.store.get('notes')` のように、`$`・名前空間・メソッドを**完全な形で**書く（`const ui = $.ui` のような代入は検証に失敗）
- `on` のイベント名は**文字列リテラル**で書く
- import はプラグインディレクトリ内の相対パスのみ（例外は `claude-code`）。動的 `import()` は不可

### 開発の流れ

| やること | 方法 |
|---------|------|
| 1 セッションだけ読み込む | `claude --plugin-dir ./first-mod` |
| 編集を反映する | 保存すると hot reload される（`register` が再実行され、変数は初期化される） |
| 型定義で補完・型検査する | 読み込み時に `.claude-plugin/types/` へ版に合った `.d.ts` が生成される |
| 検証する | `claude plugin validate ./first-mod` |
| 自動テストを回す | `claude plugin test`（セッション・サインイン・ネットワークなしで実行） |
| Claude に書かせる | 説明すると、組み込みの `plugin-authoring` Skill を使って Claude が書く |

**Claude に mod を書かせた場合の承認**: 最初のファイルを保存した時点で、hot reload を有効にするか確認されます。承認すると、そのセッション限りで読み込まれます。`claude -p`・`dontAsk` モード・未信頼のワークスペース・`--safe-mode`・`disableAllHooks`・組織の managed settings がある場合は、Claude が書いた mod は読み込まれません。

> **自作 mod の配布**: mod はプラグインなので、`/plugin install <name>@<marketplace>` で入れます。共有はディレクトリや zip の受け渡し、チームのマーケットプレイス、組織の managed settings、公開マーケットプレイスから選びます。インストール済みのコピーはバージョンでキャッシュされるため、開発中は `--plugin-dir` で作業ディレクトリを読み込み、配布時にバージョンを上げます。

---

## 5. 組織で止める境界

mod は既定で有効です。組織の管理者は managed settings で、mod を許すか・どれを許すか・どの順で動かすかを決めます。

### 何もしないときに起きること

| 項目 | 既定の挙動 |
|------|-----------|
| mod | **有効**。許可されたマーケットプレイスからのインストールと、`--plugin-dir` での読み込みができる |
| 組み込みのガード | `sec-default@builtin`（`/plugin` では `cc-plugin-sec-default`）が、利用者の mod より先に読み込まれ、**利用者は無効にできない** |
| ガードが読み込まれる条件 | managed settings がある端末、または Team / Enterprise プランでサインインした利用者。**API キー・Bedrock・Google Cloud・Foundry で認証し、managed settings もない端末には読み込まれない** |
| ガードが守るもの | 組織の managed hook が受け取る内容と判断、system prompt、managed の `CLAUDE.md`、managed MCP サーバーのツールと説明を、利用者の mod が変えられないようにする |
| それ以外 | 許可される。利用者の権限で、ファイルの読み書き・プロセス起動・通信・ツール呼び出しの書き換え・承認が可能 |

2.1.289 では、**ユーザーがインストールしたプラグインが、組織管理の MCP サーバーのサインイン用ツールの説明を書き換えられた**問題も修正されています。ガードの境界は版ごとに塞がれているため、組織で運用するなら版を揃えて確認します。

### 優先されるルールと、効かない範囲

ガードが読み込まれている場合の優先関係です。

- **`deny` ルールが優先**: 利用者の mod は、`deny` ルールが拒否する呼び出しを承認できない（`allowModsToOverrideDenyRules` を `true` にしない限り）
- **managed の `PreToolUse` hook のブロックは最終**: mod が内容を書き換えても、managed hook は書き換え後の呼び出しに再度実行される
- **`ask` ルールは上書きされ得る**: mod が承認すれば、`ask` が出す確認は出ない。auto mode では、mod が承認した呼び出しは classifier の確認なしで実行される

> **`deny` ルールは mod 自身の `$.fs` / `$.process` を止めません。** 公式は、`Read(.env)` を `deny` にしても、mod は `$.fs.read` でそのファイルを読めると明記しています。これらの呼び出しを制限したい場合は、mod を読み込ませないか、**組織自身の policy mod** で処理します。

### 組織の方針ごとの設定

| 目的 | 設定 |
|------|------|
| 利用者がインストールした mod を読み込ませない（フックは残す） | managed settings の `pluginConfigs` で、`cc-plugin-sec-default@builtin` の `allowManagedModsOnly: true` |
| mod もフックも全部止める（managed のフックを含む） | `disableAllHooks: true`（**managed の `PreToolUse` も効かなくなる**） |
| 組織の mod だけ許可する | `allowManagedModsOnly` + 組織の mod の配布 + `disableSideloadFlags` |
| 承認済みマーケットプレイスの mod だけ許可する | マーケットプレイスの制限 + `disableSideloadFlags: true` |
| 任意の mod を許可し、組織の mod で他の mod を検査する | policy mod を `prependPlugins` で先頭に置く |

`allowManagedModsOnly` を managed settings に置いた場合の挙動です。

```json
{
  "pluginConfigs": {
    "cc-plugin-sec-default@builtin": {
      "options": { "allowManagedModsOnly": true }
    }
  }
}
```

- 利用者の mod は読み込まれない（インストールしたプラグイン・`--plugin-dir`・Claude が書いた mod のすべて）
- **組織の mod は読み込まれる**。ただし「組織の mod」と認められるには、managed の `enabledPlugins` で有効化され、managed settings が**端末上のディレクトリを絶対パス**で指すマーケットプレイスから、**相対パス**で読み込まれる必要がある。GitHub・git・URL・npm からコピーされるプラグインは**利用者の mod 扱い**になる
- 利用者はこの設定を打ち消せない。ガードは managed settings だけを読む（ユーザー・プロジェクト・ローカル設定や `--settings` の同じ項目は無効）
- 利用者の settings hook・ステータスライン・`/goal` は影響を受けない
- 組み込み mod は別々のスイッチを持つ

**組織の mod を置くディレクトリは、管理者だけが書き込める状態にします。** 書き込める人は、組織の mod を書き換えられるためです。

### policy mod で他の mod を検査する

`plugin.register` イベントは、他の mod が読み込まれる直前に、`claude plugin validate` と同じ呼び出し一覧を受け取ります。組織の mod はこの一覧を読んで、特定の呼び出しを使う mod を拒否できます。

```javascript
// acme-guard/hooks/register.js（公式ドキュメントの例を抜粋）
const BLOCKED_CALLS = ['process.run', 'process.spawn']

export function register(on) {
  on('plugin.register', async ($, e, next) => {
    const blocked = e.uses.calls.filter((call) => BLOCKED_CALLS.includes(call))
    if (e.tier === 'user' && blocked.length > 0) {
      return { refuse: 'Acme policy: mods may not call ' + blocked.join(', ') }
    }
    return next(e)
  })
}
```

**検査が失敗したときの向きに注意します。** 公式は、`plugin.register` の hook が例外を出すか制限時間を超えると、hook はスキップされて**検査が fail open になり、対象の mod が読み込まれる**と説明しています。fail closed にしたい場合は、検査を関数に分け、`.catch` で拒否を返します（`e.tier !== 'user'` の mod は通す）。また、mod を動かすワーカーが 3 回クラッシュすると、組み込み以外の mod（組織のものも含む）は、`/reload-plugins` か新規セッションまで外れます。**policy mod だけに依存した統制にはしない**でください。

---

## 6. 止め方

| 止めたい範囲 | 方法 |
|-------------|------|
| 特定の mod 1 つ | `/plugin` の **Installed** タブで無効化・アンインストール |
| インストール済みの全 mod（1 セッション） | `claude --safe-mode`（ほかのカスタマイズも無効になる） |
| インストールした全 mod（常時） | `~/.claude/settings.json` の `"disableAllHooks": true`（settings hook とカスタムステータスラインも止まる。組織が管理するものは動き続ける） |

- `disableAllHooks` と `allowManagedModsOnly` は **mod だけを止め、プラグイン自体は残します**。スキル・コマンド・エージェント・MCP サーバーは読み込まれます。
- 公式は、早期アクセスで `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` を設定していた場合は**削除する**よう案内しています。2.1.287 以降ではこの変数は無視され、`0` を設定しても mod は無効になりません。
- **組み込み mod は `--safe-mode` や `disableAllHooks` では止まりません。** それぞれ個別のスイッチがあります。
- 読み込まれている mod は、端末で `/plugin` を開くと、タブの下の薄い行（例: `1 mod active · first-mod`）で確認できます。組み込み mod はこの行に出ません。

---

## 7. 組み込み mod と「You should know」

Claude Code 自身の機能の一部も mod です。`/plugin` の **Installed** タブの **Built-in** に一覧されます。

| `/plugin` での名前 | 役割 | 止め方 |
|-------------------|------|--------|
| `cc-plugin-agents-md` | `AGENTS.md` をプロジェクト指示として読む | `/plugin` で無効化、または読み込む指示ファイルを選ぶ |
| `cc-plugin-diff` | `/diff` を担当し、ペインを描く | `/plugin` で無効化（`/diff` は Claude Code 本来の実装へ戻る） |
| `cc-plugin-plugin-authoring` | mod 作成用の `plugin-authoring` Skill を提供 | `/plugin` で無効化 |
| `cc-plugin-sec-default` | 組織が管理するものを利用者の mod から守るガード | **無効化できない**（管理者が順序を決める） |
| `cc-plugin-telemetry` | Claude Code と組み込み mod の分析記録を送る | `/plugin` で無効化、または `DISABLE_TELEMETRY` などで分析を止める |
| `cc-plugin-you-should-know` | 長いタスク中に、利用者が見落としそうなことを副エージェントが見つけてプロンプト上に出す | `/plugin` で無効化 |

**「You should know」は既定で無効です。** 2.1.287 の変更ログには「first-party セッションでテレメトリが有効なとき」向けとして載っており、`/plugin enable cc-plugin-you-should-know@builtin` で有効にします。公式ドキュメントの表では「組織で利用できる場合に、`/plugin` の **Installed → Show disabled** に出る」とされています。**使えるかどうかはプラン・組織・テレメトリ設定に依存する**ため、見つからなくても不具合とは限りません。

> **副エージェントが何を見るか**: 「見落としの指摘」は、副エージェントがセッションの内容を読む前提の機能です。有効にする前に、扱う情報の範囲（[生成AIを業務で安全に使う](../business/safety.md)）と、組織のテレメトリ方針を確認してください。この点は公式ドキュメントが詳しく述べていないため、ここでは推測せず、確認項目として挙げるにとどめます。

組み込み mod のうち `diff`・`agents-md`・`sec-default`・`telemetry` は、[claude-code リポジトリの `mods` ディレクトリ](https://github.com/anthropics/claude-code/tree/main/mods)にソースが公開されています。`sec-default` は、policy mod を書くときの手本として読めます。

---

## 8. 2.1.287〜2.1.289 の主な変更

| 版（日付） | 変更 |
|-----------|------|
| 2.1.287（2026-10-01） | **Mods を追加**。組み込み mod「You should know」を追加。agents view に `n:<text>` フィルタを追加 |
| 2.1.288（2026-10-02） | mod 向けに `$.ui.selection()`（全画面で直近に選択したテキストと、選択が 1 行に収まる場合はその行を取得）を追加。mod のボタンが再起動前に描いた画面で別のボタンの処理を実行し得た問題、プラグイン LSP の `${user_config.*}` 等が置換されずに渡された問題、`--plugin-dir` で読んだプラグインに「Configure options」が出ない問題を修正 |
| 2.1.289（2026-10-03） | `agent.spawn`（teammates 用）、プラグイン hook イベントをまたぐ agent id の一貫、`$.agent.list()` の idle・waiting 状態を追加。統制に関わる修正が中心（下表） |

2.1.289 で修正された、**統制に関わる項目**です。

| 修正内容 | 運用上の意味 |
|---------|-------------|
| 複合シェルコマンドの入れ子部分の `deny` / `ask` が、管理マシン上で利用者の mod の承認に勝てなかった | 管理マシンで mod を許可している組織は、この版以降へ揃える |
| IDE でシンボリックリンク経由で選択・変更されたファイルに `Read` の `deny` が効かなかった | 同上 |
| 環境変数のプレフィックス付きコマンド（例: `TZ="$HOME" rm -rf build`）や、変数代入が先頭にあるコマンドが、sandbox の自動許可下で Bash の `deny` / `ask` を回避し得た | sandbox の自動許可を使う場合は、この版以降へ揃える |
| 利用者のインストールしたプラグインが、組織管理 MCP サーバーのサインイン用ツールの説明を書き換えられた | managed MCP を使う組織は、この版以降へ揃える |
| mod が描画した行が例外を出すと、セッションが「回復不能なインターフェースエラー」で終了した（以降は mod 単独の失敗として扱う） | 描画する mod の障害が、セッション全体へ波及しにくくなった |

---

## 判断の目安

| 状況 | 選ぶもの |
|------|---------|
| 危険なコマンドをブロック・記録したい | まず [フック（settings hook）](basics.md#フック)。手持ちのスクリプトで足りる |
| 毎回同じ指示を貼っている | [Skill](basics.md#agent-skills) |
| 外部システムへ接続したい | MCP |
| 画面にペイン・バンドを出したい、独自の `/command` を足したい、イベントを書き換えたい | **mod** |
| 第三者の mod を入れたい | 作者・マーケットプレイスを確認し、`claude plugin validate` の `hooks:` / `calls:` を読む |
| 組織で利用者の mod を止めたい | `allowManagedModsOnly`（フックは残る）。全部止めるなら `disableAllHooks`（managed のフックも止まる） |
| 組織で一部の mod だけ許したい | マーケットプレイス制限 + `disableSideloadFlags`、または policy mod |

---

## 関連ドキュメント

- [Claude Code のカスタマイズ機能](basics.md) — Skill・フック・MCP・プラグインの使い分け
- [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md#実行コードを持つ拡張--claude-code-の-mods) — mod を含む、導入前の確認と組織での絞り込み
- [プラグインの可搬性](../dev-methods/plugin-portability.md) — mod は Claude Code 固有の構成要素を持つプラグインで、他のエージェントへは持ち出せない
- [Skills 最新動向 12 節](../trends.md#12-skill--plugin-のセキュリティ) — 統制の 3 段階（導入前・推論前・実行後）

## 参考リンク

- [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview) — 概要・動く場所・信頼の判断・組み込み mod（Anthropic 公式）
- [Create a mod](https://code.claude.com/docs/en/plugins/mods/create) — Claude に書かせる方法と、最小の mod のチュートリアル（Anthropic 公式）
- [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin) — managed settings・組み込みガード・policy mod（Anthropic 公式）
- [Mods reference](https://code.claude.com/docs/en/plugins/mods/reference) — events・メソッド・要素・制限（Anthropic 公式）
- [Claude Code changelog](https://code.claude.com/docs/en/changelog) — 2.1.287〜2.1.289 の変更（Anthropic 公式）
- [claude-code-playground の mods](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods) — 公式サンプル（無保証）
