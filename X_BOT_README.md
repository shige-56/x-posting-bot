# X投稿BOT

CSVファイルの一言紹介文と短縮URLを使って、X（Twitter）に自動投稿するBOTです。

## 機能

- CSVファイルからランダムに投稿データを選択
- 8:00-22:00の間で1時間に2-3回ランダム投稿
- 1度投稿した内容は次の日まで重複投稿しない
- 投稿履歴の管理
- テストモード（実際の投稿は行わない）
- **実際のX（Twitter）投稿機能**
- ログ機能とエラーハンドリング
- 統計情報の表示

## セットアップ

### 1. 必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. CSVファイルの準備

`kindle_unlimited_biz_10_with_links.csv` ファイルが必要です。
以下の列が含まれている必要があります：

- `No`: 連番
- `タイトル`: 書籍のタイトル
- `一言紹介文`: 投稿に使用する紹介文
- `短縮URL`: 投稿に使用する短縮URL

### 3. X（Twitter）API設定（実際の投稿を行う場合）

X Developer Portalでアプリケーションを作成し、以下の認証情報を取得してください：

1. **API Key** と **API Secret**
2. **Access Token** と **Access Token Secret**
3. **Bearer Token**

### 4. 設定ファイルの確認

`x_bot_config.py` で以下の設定を確認・変更してください：

```python
# 投稿設定
POSTING_HOURS = (8, 22)  # 投稿時間: 8:00-22:00
POSTS_PER_HOUR = (2, 3)  # 1時間に2-3回
POSTING_INTERVAL_MIN = (20, 40)  # 投稿間隔: 20-40分

# テスト設定
TEST_MODE = False  # False: 実際のX投稿を有効にする

# X（Twitter）API設定
X_API_KEY = "your-x-api-key"
X_API_SECRET = "your-x-api-secret"
X_ACCESS_TOKEN = "your-x-access-token"
X_ACCESS_TOKEN_SECRET = "your-x-access-token-secret"
X_BEARER_TOKEN = "your-x-bearer-token"
```

## 使用方法

### 基本版

```bash
python x_posting_bot.py
```

### 設定ファイル対応版（推奨）

```bash
python x_posting_bot_advanced.py
```

## 実際のX投稿への移行

### 1. X Developer Portalでの設定

1. [X Developer Portal](https://developer.twitter.com/) にアクセス
2. アプリケーションを作成
3. 必要な権限を設定（Read and Write）
4. 認証情報を取得

### 2. 設定ファイルの更新

`x_bot_config.py` で以下を設定：

```python
TEST_MODE = False  # テストモードを無効化

# 実際の認証情報に変更
X_API_KEY = "実際のAPI Key"
X_API_SECRET = "実際のAPI Secret"
X_ACCESS_TOKEN = "実際のAccess Token"
X_ACCESS_TOKEN_SECRET = "実際のAccess Token Secret"
X_BEARER_TOKEN = "実際のBearer Token"
```

### 3. 投稿テスト

設定後、まず単発テストで動作確認：

```bash
python x_posting_bot_advanced.py
```

### 4. 継続実行

テストが成功したら、継続実行を選択してBOTを開始します。

## 投稿文の形式

```
一言紹介文

短縮URL

#KUおすすめリスト
```

## 動作の流れ

1. **初期化**: CSVファイルと投稿履歴を読み込み、X API認証
2. **投稿時間チェック**: 8:00-22:00の間かチェック
3. **データ選択**: 今日まだ投稿していないデータからランダム選択
4. **投稿内容作成**: テンプレートを使って投稿内容を生成
5. **投稿実行**: テストモードではターミナルに表示、実際の投稿も実行
6. **履歴記録**: 投稿履歴を保存
7. **待機**: ランダムな間隔で次の投稿まで待機

## 投稿テンプレート

現在はシンプルな形式で、一言紹介文から始まります：

```
{introduction}

{short_url}

#KUおすすめリスト
```

## ファイル構成

- `x_posting_bot.py`: 基本版BOT
- `x_posting_bot_advanced.py`: 設定ファイル対応版BOT（X API対応）
- `x_bot_config.py`: 設定ファイル
- `posting_history.json`: 投稿履歴（自動生成）
- `x_bot.log`: ログファイル（自動生成）

## 投稿履歴の管理

BOTは `posting_history.json` ファイルで投稿履歴を管理します：

```json
{
  "1": "2024-01-15",
  "3": "2024-01-15",
  "7": "2024-01-15"
}
```

- キー: CSVファイルのNo列の値
- 値: 投稿した日付

同じ日付に投稿した内容は、次の日まで再投稿されません。

## テストモード

`TEST_MODE = True` の場合：

- 実際のX投稿は行いません
- ターミナルに投稿イメージを表示します
- 投稿履歴は正常に記録されます

## エラーハンドリング

- CSVファイルが見つからない場合
- 投稿可能なデータがない場合
- 投稿時間外の場合
- X API認証エラーの場合
- 投稿失敗の場合
- 予期しないエラーの場合

エラーが発生した場合は、ログファイルに詳細が記録されます。

## 統計情報

BOT停止時に以下の統計情報が表示されます：

- 総投稿数
- 成功投稿数
- 失敗投稿数
- 成功率
- 最後の投稿時間

## 注意事項

- 投稿時間外は自動的に待機します
- Ctrl+C で安全に停止できます
- 投稿履歴は自動的に保存されます
- ログファイルで動作状況を確認できます
- **X APIのレート制限に注意してください**
- **投稿内容は事前に確認してから実行してください**

## トラブルシューティング

### よくある問題

1. **CSVファイルが見つからない**
   - ファイル名とパスを確認してください
   - 必要な列が含まれているか確認してください

2. **投稿可能なデータがない**
   - 短縮URLが設定されているか確認してください
   - 今日の投稿履歴を確認してください

3. **投稿時間外のメッセージ**
   - 8:00-22:00の間で実行してください
   - 設定で投稿時間を変更できます

4. **X API認証エラー**
   - 認証情報が正しく設定されているか確認してください
   - X Developer Portalでアプリケーションの権限を確認してください

5. **投稿失敗**
   - 投稿内容が文字数制限内か確認してください
   - X APIのレート制限に引っかかっていないか確認してください

## カスタマイズ

### 投稿時間の変更

```python
POSTING_HOURS = (9, 21)  # 9:00-21:00に変更
```

### 投稿頻度の変更

```python
POSTS_PER_HOUR = (1, 2)  # 1時間に1-2回に変更
POSTING_INTERVAL_MIN = (30, 60)  # 30-60分間隔に変更
```

### 投稿テンプレートの変更

```python
POST_TEMPLATES = [
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    # 新しいテンプレートを追加
    "{introduction}\n\n{short_url}\n\n#KindleUnlimited #ビジネス書"
]
```

## ライセンス

このスクリプトは教育目的で作成されています。商用利用の際は、X（Twitter）の利用規約を遵守してください。 