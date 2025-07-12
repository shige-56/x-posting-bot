# X投稿BOT

CSVファイルの一言紹介文と短縮URLを使って、X（Twitter）に自動投稿するBOTです。

## 機能

- CSVファイルからランダムに投稿データを選択
- **GitHub Actions対応**: サーバー常時稼働不要
- **ランダム投稿**: 固定時間ではなく、確率ベースの投稿
- **効率的な配分**: 残り時間と残り投稿数を考慮した確率調整
- 1度投稿した内容は次の日まで重複投稿しない
- 投稿履歴の管理
- テストモード（実際の投稿は行わない）
- **実際のX（Twitter）投稿機能**
- ログ機能とエラーハンドリング
- 統計情報の表示
- **自動履歴管理**: 投稿履歴の自動コミット・プッシュ

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

#### 通常版（`x_bot_config.py`）

```python
# 投稿設定
POSTING_HOURS = (9, 22)  # 投稿時間: 9:00-22:00
POSTS_PER_DAY = 9  # 1日最大9件
POSTING_INTERVAL_MIN = (60, 120)  # 投稿間隔: 60-120分（1-2時間）

# テスト設定
TEST_MODE = False  # False: 実際のX投稿を有効にする

# X（Twitter）API設定
X_API_KEY = "your-x-api-key"
X_API_SECRET = "your-x-api-secret"
X_ACCESS_TOKEN = "your-x-access-token"
X_ACCESS_TOKEN_SECRET = "your-x-access-token-secret"
X_BEARER_TOKEN = "your-x-bearer-token"
```

#### GitHub Actions版（`x_bot_config_github.py`）

```python
# GitHub Actions用設定
GITHUB_ACTIONS_MODE = True  # GitHub Actions実行モード
MIN_POSTING_PROBABILITY = 0.5  # 最小投稿確率
MAX_POSTING_PROBABILITY = 0.9  # 最大投稿確率

# 環境変数からAPI認証情報を取得
X_API_KEY = os.getenv('X_API_KEY', "your-x-api-key")
X_API_SECRET = os.getenv('X_API_SECRET', "your-x-api-secret")
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN', "your-x-access-token")
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET', "your-x-access-token-secret")
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN', "your-x-bearer-token")
```

## 使用方法

### 基本版（ローカル実行）

```bash
python x_posting_bot.py
```

### 設定ファイル対応版（ローカル実行）

```bash
python x_posting_bot_advanced.py
```

### GitHub Actions版（自動実行）

1. **GitHub Secretsの設定**
   
   リポジトリのSettings → Secrets and variables → Actionsで以下を設定：
   ```
   X_API_KEY: あなたのX API Key
   X_API_SECRET: あなたのX API Secret
   X_ACCESS_TOKEN: あなたのX Access Token
   X_ACCESS_TOKEN_SECRET: あなたのX Access Token Secret
   X_BEARER_TOKEN: あなたのX Bearer Token
   ```

2. **GitHub Actionsの有効化**
   
   リポジトリのActionsタブで"X Posting Bot"ワークフローを有効化

3. **手動実行でテスト**
   
   Actionsタブから手動実行で動作確認

## 投稿文の形式

```
一言紹介文

短縮URL

#KUおすすめリスト
```

## 動作の流れ

### ローカル実行版

1. **初期化**: CSVファイルと投稿履歴を読み込み、X API認証
2. **投稿時間チェック**: 9:00-22:00の間かチェック
3. **データ選択**: 今日まだ投稿していないデータからランダム選択
4. **投稿内容作成**: テンプレートを使って投稿内容を生成
5. **投稿実行**: テストモードではターミナルに表示、実際の投稿も実行
6. **履歴記録**: 投稿履歴を保存
7. **待機**: ランダムな間隔で次の投稿まで待機

### GitHub Actions版

1. **時間チェック**: 9-22時のみ実行
2. **制限チェック**: 1日最大9件の制限
3. **確率計算**: 残り時間と残り投稿数で確率を調整
4. **ランダム判定**: 計算された確率で投稿実行
5. **自動履歴管理**: 投稿履歴の自動コミット・プッシュ

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
- `x_bot_config.py`: 通常の設定ファイル
- `x_bot_config_github.py`: GitHub Actions用設定ファイル
- `posting_history.json`: 投稿履歴（自動生成）
- `x_bot.log`: ログファイル（自動生成）
- `.github/workflows/post.yml`: GitHub Actions設定

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

## GitHub Actions版の特徴

### 投稿判定ロジック

1. **時間チェック**: 9-22時のみ実行
2. **制限チェック**: 1日最大9件の制限
3. **確率計算**: 残り時間と残り投稿数で確率を調整
4. **ランダム判定**: 計算された確率で投稿実行

### 確率計算例

- **9時**: 高確率（90%）で投稿（残り13時間、最大9回）
- **15時**: 中確率（70%）で投稿（残り7時間、残り投稿数による）
- **20時**: 低確率（50%）で投稿（残り2時間、残り投稿数による）

### スケジュール

- **実行頻度**: 9-22時の毎時（GitHub Actionsのcron）
- **タイムゾーン**: UTC（日本時間との時差に注意）

## 注意事項

- 投稿時間外は自動的に待機します
- Ctrl+C で安全に停止できます
- 投稿履歴は自動的に保存されます
- ログファイルで動作状況を確認できます
- **X APIのレート制限に注意してください**
- **投稿内容は事前に確認してから実行してください**
- **GitHub Actionsの無料プランには実行時間制限があります**

## トラブルシューティング

### よくある問題

1. **CSVファイルが見つからない**
   - ファイル名とパスを確認してください
   - 必要な列が含まれているか確認してください

2. **投稿可能なデータがない**
   - 短縮URLが設定されているか確認してください
   - 今日の投稿履歴を確認してください

3. **投稿時間外のメッセージ**
   - 9:00-22:00の間で実行してください
   - 設定で投稿時間を変更できます

4. **X API認証エラー**
   - 認証情報が正しく設定されているか確認してください
   - X Developer Portalでアプリケーションの権限を確認してください

5. **投稿失敗**
   - 投稿内容が文字数制限内か確認してください
   - X APIのレート制限に引っかかっていないか確認してください

6. **GitHub Actions版で投稿されない**
   - GitHub Secretsが正しく設定されているか確認
   - ログファイルでエラーを確認
   - 投稿時間内かどうか確認

### ログの確認

GitHub Actionsの実行ログで以下を確認：

```
投稿判定: 現在15時, 今日3/9件, 残り6件, 確率0.65, 結果投稿
✅ 投稿処理完了
```

## カスタマイズ

### 投稿時間の変更

#### ローカル実行版
```python
POSTING_HOURS = (9, 21)  # 9:00-21:00に変更
```

#### GitHub Actions版
`.github/workflows/post.yml`のcron設定を変更：
```yaml
- cron: '0 0-13 * * *'  # UTC 0-13時 = JST 9-22時
```

### 投稿頻度の変更

#### ローカル実行版
```python
POSTS_PER_DAY = 5  # 1日5件に変更
POSTING_INTERVAL_MIN = (30, 60)  # 30-60分間隔に変更
```

#### GitHub Actions版
```python
POSTS_PER_DAY = 5  # 1日5件に変更
MIN_POSTING_PROBABILITY = 0.2  # より低い確率
MAX_POSTING_PROBABILITY = 0.9  # より高い確率
```

### 投稿テンプレートの変更

```python
POST_TEMPLATES = [
    "📚 {introduction}\n\n🔗 {short_url}\n\n#KUおすすめリスト #KindleUnlimited",
    "💡 {introduction}\n\n📖 {short_url}\n\n#KUおすすめリスト"
]
```

## セキュリティ

- API認証情報はGitHub Secretsで管理
- 投稿履歴は自動的にリポジトリにコミット
- ログファイルも自動的に保存

## ライセンス

このスクリプトは教育目的で作成されています。商用利用の際は、X（Twitter）の利用規約を遵守してください。 