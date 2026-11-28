# MCP サーバーの Skill を Claude Code・VS Code で使う

> **対象ツール**: Claude Code・GitHub Copilot（VS Code） ｜ **実行環境**: CLI / IDE ｜ **対象読者**: MCP サーバーを使う開発者・チーム管理者 ｜ **最終更新**: 2026-11-28

たとえば、社内の文書サーバーが検索ツールと「週報を作る」Skill を一緒に配っていれば、利用者は週報のテンプレートを各リポジトリにコピーせずに済みます。サーバーが **Skills over MCP** に対応していると、チャットの入力欄で提供元を確認し、その手順を呼び出せます。

| 使う環境 | 提供元・状態 | 始める前に確認すること |
|---|---|---|
| Claude Code の対話型ターミナル | Anthropic / Official / Preview（公開ベータ） | 公式ガイドの要件は v2.1.331 以降。ターミナルで `claude --version` を確認する。Anthropic への直接接続、対応モデル、サインイン方法に応じた提供条件がある。[対応環境](https://code.claude.com/docs/en/mcp#where-mcp-skills-are-supported) |
| VS Code の Copilot Agent Host セッション | Microsoft / Official / Preview | VS Code 1.147 以降。設定で `chat.agentHost.mcpSkills.enabled` が有効か確認し、Copilot の新しいチャットを開く。[Microsoft の利用例](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/skills-over-mcp-are-now-available-in-vs-code/4574580) |

## 接続済みのサーバーで一つ試す

1. **サーバーの配布内容を確認する。** 利用中の MCP サーバーの案内で、Skills 拡張と試したい Skill の名前を確認します。たとえば検索ツールに接続できていても、週報の Skill を使うには、サーバー側でその Skill を公開している必要があります。[MCP Skills 拡張の仕組み](skills-over-mcp.md)
2. **チャットの入力欄に `/` を入力する。** たとえば、サーバー名が `team-docs`、Skill 名が `weekly-report` なら、候補は `/team-docs:weekly-report` です。これは架空の例なので、実際には一覧に表示された名前を選びます。Claude Code の対話型ターミナルでは `/skills` でも一覧を開けます。Claude のコネクタや Plugin 経由のサーバーには接頭辞が付きます。[Claude Code の呼び出し方](https://code.claude.com/docs/en/mcp#find-and-call-mcp-skills-by-name)
3. **手元で確認できる入力で呼び出す。** 週報の例なら「このメモから今週の完了項目だけを箇条書きにして」と依頼します。表示された配布元と、結果に含まれる項目を元のメモと照合すれば、目的の Skill を選べたか確認できます。

## 読み込みを許可すると、次回も確認されるか

| 場面 | その場で選ぶこと | 次回への影響 |
|---|---|---|
| Claude Code が Manual モードで Skill を選んだ | 確認画面にある Skill 名とサーバーを確認する。 | **Allow this version** を選ぶと、その Skill のファイルが変わるまで承認を記憶する。ターミナルでは `/permissions` でルールを削除できる。 |
| Claude Code の auto モード、または自分でコマンドを入力した | auto モードでは分類器が読み込みを判定する。利用者が直接入力した Skill コマンドは通常、読み込み時の確認を省く。 | 管理者は特定の Skill を `deny` にして、直接入力した場合もブロックできる。 |
| VS Code の Copilot がサーバーの Skill を初めて読む | 確認画面に表示された**サーバー名**を見る。まず試すなら **Allow Once** を選ぶ。 | Allow Once はそのセッションで有効。**Always Allow** はそのサーバーに対する選択として保存される。同じサーバーが配る別の Skill にも関わる。 |

ここで判断するのは、サーバーの手順をエージェントに読ませるかどうかです。週報の下書きを作った後に投稿ツールを呼ぶ場合は、投稿先と、そのツールに設定された権限も確認します。[Claude Code の承認ルール](https://code.claude.com/docs/en/mcp#approvals-for-mcp-skills) ／ [VS Code のサーバー単位の承認](https://github.com/microsoft/vscode/pull/345956)

## ツールは見えるのに Skill が出ないとき

| 環境 | 確認する場所 |
|---|---|
| Claude Code のターミナル | `/mcp` で接続先と Protocol を確認する。サーバー側で MCP `2026-07-28` 以降と Skills 拡張に対応しているかを確かめる。クラウドセッションや `claude -p` はこのベータの対象外。 |
| Claude Team / Enterprise の利用者 | `/login` で利用する場合、既定はオフ。コネクタ経由なら管理者が組織の Skills と Connectors の **Skills over MCP** を確認する。それ以外のサーバーなら、管理設定の `disableDirectMcpSkills` が `false` かを確認する。 |
| VS Code の Copilot | Agent Host 用の MCP 設定にサーバーがあるかを確認する。機能を有効にした後の新しいセッションで、Skills ページの **Skills from …** に配布元が出るかを見る。 |

公開ベータの利用条件は2026-11-28に公式資料で確認しました。本記事の手順は実機未検証です。[Anthropic のトラブルシューティング](https://code.claude.com/docs/en/mcp#troubleshoot-mcp-skills) ／ [VS Code の実装と確認手順](https://github.com/microsoft/vscode/pull/345956)
