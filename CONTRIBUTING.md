# コントリビューションガイド

このリポジトリへの貢献を歓迎します。

## このリポジトリについて

[github/awesome-copilot](https://github.com/github/awesome-copilot) の内容を日本語で解説するガイドです。新規エントリの追加は upstream リポジトリへ行い、このリポジトリでは日本語解説の改善・追記を受け付けます。

## 貢献できること

- 日本語訳・解説の誤りの修正
- 説明が不足しているエントリへの補足
- 新しい使用例・活用シーンの追加
- リンク切れの報告・修正

## Pull Request の手順

1. このリポジトリをフォーク
2. 作業ブランチを作成: `git checkout -b fix/description`
3. 変更をコミット: `git commit -m "fix: 説明の修正内容"`
4. プッシュ: `git push origin fix/description`
5. Pull Request を作成

## 編集ルール

- 説明文は日本語で書く
- エントリは `[ファイル名](upstream-url) - 説明。` の形式を維持する
- テーブルの列幅は揃える
- 句点（。）で終わる

## 新規ファイルの追跡

upstream に新規ファイルが追加された場合は、`scripts/known-files.json` と対応する `docs/` のドキュメントに追記してください。

## 行動規範

建設的なフィードバックを心がけ、誰もが貢献しやすい環境を維持してください。
