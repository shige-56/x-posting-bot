# X投稿BOT GitHub Actions対応版

## 概要

このバージョンはGitHub Actionsを使用して自動投稿を行うX投稿BOTです。9-22時の間に最大9回の投稿を、ランダムな確率で実行します。

## 特徴

- **GitHub Actions対応**: サーバー常時稼働不要
- **ランダム投稿**: 固定時間ではなく、確率ベースの投稿
- **効率的な配分**: 残り時間と残り投稿数を考慮した確率調整
- **自動履歴管理**: 投稿履歴の自動コミット・プッシュ

## セットアップ手順

### 1. リポジトリの準備

1. このコードをGitHubリポジトリにプッシュ
2. 必要なファイルが含まれていることを確認：
   - `x_posting_bot_advanced.py`
   - `x_bot_config_github.py`
   - `requirements.txt`
   - `kindle_unlimited_biz_10_with_links.csv`
   - `.github/workflows/post.yml`

### 2. GitHub Secretsの設定

リポジトリのSettings → Secrets and variables → Actionsで以下を設定：

```
X_API_KEY: あなたのX API Key
X_API_SECRET: あなたのX API Secret
X_ACCESS_TOKEN: あなたのX Access Token
X_ACCESS_TOKEN_SECRET: あなたのX Access Token Secret
X_BEARER_TOKEN: あなたのX Bearer Token
```

### 3. 設定ファイルの調整

`x_bot_config_github.py`で以下を調整：

```python
# 投稿時間（現在は9-22時）
POSTING_HOURS = (9, 22)

# 1日の最大投稿数（現在は9件）
POSTS_PER_DAY = 9

# 投稿確率の範囲
MIN_POSTING_PROBABILITY = 0.3  # 最小30%
MAX_POSTING_PROBABILITY = 0.8  # 最大80%
```

### 4. GitHub Actionsの有効化

1. リポジトリのActionsタブに移動
2. "X Posting Bot"ワークフローを有効化
3. 手動実行でテスト

## 動作仕様

### 投稿判定ロジック

1. **時間チェック**: 9-22時のみ実行
2. **制限チェック**: 1日最大9件の制限
3. **確率計算**: 残り時間と残り投稿数で確率を調整
4. **ランダム判定**: 計算された確率で投稿実行

### 確率計算例

- **9時**: 高確率（80%）で投稿（残り13時間、最大9回）
- **15時**: 中確率（60%）で投稿（残り7時間、残り投稿数による）
- **20時**: 低確率（30%）で投稿（残り2時間、残り投稿数による）

### スケジュール

- **実行頻度**: 9-22時の毎時（GitHub Actionsのcron）
- **タイムゾーン**: UTC（日本時間との時差に注意）

## ファイル構成

```
.github/workflows/post.yml          # GitHub Actions設定
x_posting_bot_advanced.py           # メインBOTスクリプト
x_bot_config_github.py              # GitHub Actions用設定
requirements.txt                    # Python依存関係
kindle_unlimited_biz_10_with_links.csv  # 投稿データ
posting_history.json                # 投稿履歴（自動生成）
x_bot.log                          # ログファイル（自動生成）
```

## トラブルシューティング

### よくある問題

1. **投稿されない**
   - GitHub Secretsが正しく設定されているか確認
   - ログファイルでエラーを確認
   - 投稿時間内かどうか確認

2. **重複投稿**
   - `posting_history.json`を確認
   - 手動実行を避ける

3. **API制限エラー**
   - X APIの制限を確認
   - 投稿頻度を下げる

### ログの確認

GitHub Actionsの実行ログで以下を確認：

```
投稿判定: 現在15時, 今日3/9件, 残り6件, 確率0.65, 結果投稿
✅ 投稿処理完了
```

## カスタマイズ

### 投稿時間の変更

`.github/workflows/post.yml`のcron設定を変更：

```yaml
- cron: '0 0-13 * * *'  # UTC 0-13時 = JST 9-22時
```

### 投稿確率の調整

`x_bot_config_github.py`で確率を調整：

```python
MIN_POSTING_PROBABILITY = 0.2  # より低い確率
MAX_POSTING_PROBABILITY = 0.9  # より高い確率
```

## セキュリティ

- API認証情報はGitHub Secretsで管理
- 投稿履歴は自動的にリポジトリにコミット
- ログファイルも自動的に保存

## 注意事項

- GitHub Actionsの無料プランには実行時間制限があります
- X APIの制限に注意してください
- 投稿内容は適切なものにしてください 