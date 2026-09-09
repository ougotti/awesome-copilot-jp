# VS Code エディタウィンドウでの複数ルート運用（Experimental）

> **対象ツール**: VS Code 上の GitHub Copilot / Claude ｜ **実行環境**: IDE（VS Code） ｜ **対象読者**: エンジニア ｜ **最終更新**: 2026-09-09

> VS Code 1.136（2026-09-02 公開）で、**エディタウィンドウの Chat view** にある Copilot / Claude のエージェントセッションが、multi-root workspace（複数フォルダを 1 つのワークスペースにまとめる構成）を **Experimental** としてサポートしました。複数リポジトリを横断して扱う際に、設定・適用範囲・hooks の読み込み元をどう判断するかをまとめます。

---

## 1. 何ができるか — 単一フォルダ・multi-root・git worktree の違い

似た言葉が並ぶ機能なので、まず区別してください。

| 構成 | 何をするか | 本ページの対象か |
|------|-----------|-----------------|
| **単一フォルダ** | 1 つのリポジトリだけを開く。これまでの既定動作 | — |
| **multi-root workspace（本ページの対象）** | 複数フォルダ（例: `frontend/` と `backend/` の別リポジトリ）を 1 つのワークスペースにまとめ、**エディタウィンドウの Chat view** から横断して扱う | **対象** |
| **Git worktree（Agents window）** | 1 つのリポジトリを、ブランチごとに分離した作業コピーで並行実行する。[Skills 最新動向](../trends.md#9-2-idecli-側の対応状況)が扱う Agents window の機能で、**本ページとは別機能** | 対象外 |

**「複数フォルダを横断して見せる」multi-root と、「1 つのリポジトリを並行実行のために分離する」worktree は目的が違います。** 混同しないでください。

---

## 2. 対応環境と前提

| 項目 | 内容 |
|------|------|
| 提供元・状態 | Official（Microsoft）／**Experimental**（2026-09-02 公開、VS Code 1.136） |
| 対象 | **エディタウィンドウの Chat view** にある Copilot / Claude のエージェントセッション。**Agents window は対象外**です（同じ挙動だと一般化しないでください） |
| 設定 | `chat.agentHost.copilotAgent.multiRootEnabled` / `chat.agentHost.claudeAgent.multiRootEnabled` を settings.json、または VS Code の設定画面（Settings UI）で有効化する |

> 前提となる拡張機能・認証の詳細は公式ページに明示的な記載がありません。導入前に手元の VS Code バージョンで [公式ページ](https://code.visualstudio.com/updates/v1_136#_multi-root-workspaces-in-editor-window-experimental) を確認してください。

---

## 3. 最小手順（公式手順に基づく例／実機未検証）

**このガイドでは実機で確認していません。** 以下は公式ページの記述に基づく手順の例です。試す際は、まず読み取り専用の依頼で挙動を確かめてください。

```text
1. VS Code のワークスペースに、複数のフォルダ（例: frontend/ と backend/）を追加する
   （File > Add Folder to Workspace...）
2. 設定で multiRootEnabled を有効化する
   - chat.agentHost.copilotAgent.multiRootEnabled（Copilot を使う場合）
   - chat.agentHost.claudeAgent.multiRootEnabled（Claude を使う場合）
3. エディタウィンドウの Chat view で、読み取りだけの依頼を送る
   依頼例: 「frontend と backend、両方の README を読んで、それぞれの役割と
          根拠にしたファイルパスを教えて」
4. 応答が両方のフォルダを参照しているか、根拠パスが実在するファイルを
   指しているかを確認する
```

---

## 4. Hooks はどのフォルダから読むか

**Agent hooks は単一の workspace folder に限定されます。** 複数フォルダに hooks が存在する場合、**どのフォルダを読み込み元（primary folder）にするかを選ぶ**必要があります。選ばなかった側のフォルダの hooks は適用されません。

> hooks は設定された時点で自動実行されます。primary folder を選ぶ前に、**候補となる全フォルダの hooks の中身を確認**してください（[Skill / Plugin のセキュリティ](../dev-methods/skill-security.md)）。

instructions・Skill の検索範囲が multi-root でどう扱われるかは、公式ページに明示的な記載がありません。**hooks の挙動から類推せず、未確認として扱ってください。**

---

## 5. うまくいかない場合

| 症状 | 確認すること |
|------|-------------|
| 複数フォルダを認識しない | **Agents window ではなくエディタウィンドウの Chat view** を使っているか |
| 設定が効かない | `chat.agentHost.copilotAgent.multiRootEnabled` / `chat.agentHost.claudeAgent.multiRootEnabled` が settings.json に正しく反映されているか |
| hooks が一部のフォルダで動かない | 選択した primary folder と、hooks を置いたフォルダが一致しているか |

---

## 6. 変更を任せる前の確認

複数リポジトリを横断する依頼は、**「全体をまとめて見る」ことと「各リポジトリの変更を個別に確認する」ことの両立**が要ります。

- 生成された変更は、**フォルダ（リポジトリ）ごとに差分を分けて確認**する
- 一方のリポジトリの変更が、意図せずもう一方の前提を壊していないかを見る
- 不可逆な操作（push・デプロイ等）は、フォルダを横断する依頼であっても通常どおり承認境界の対象です（[エージェントに外部操作を与える手段の選び方](../dev-methods/tool-selection.md#8-承認境界--読み取り入力送信購入削除で分ける)）

---

## 関連ドキュメント

- [GitHub Copilot ガイド](README.md) — Copilot のカスタマイズ全般
- [Skills 最新動向「IDE・CLI 側の対応状況」](../trends.md#9-2-idecli-側の対応状況) — Agents window の Git worktree 機能（本ページの multi-root workspace とは別機能）
- [Skill / Plugin のセキュリティ](../dev-methods/skill-security.md) — hooks を有効化する前に中身を確認する理由
- [エージェントに外部操作を与える手段の選び方](../dev-methods/tool-selection.md) — 不可逆な操作の承認境界

## 参考リンク

- [VS Code 1.136 — Multi-root workspaces in editor window (Experimental)](https://code.visualstudio.com/updates/v1_136#_multi-root-workspaces-in-editor-window-experimental) — 公式リリースノート（2026-09-02 公開、2026-09-09 確認）
