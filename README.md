# X-Posting-Bot

Kindle Unlimitedのアソシエイトリンク生成とX（Twitter）への自動投稿を行うボットプロジェクトです。

## プロジェクト概要

このプロジェクトは以下の2つの主要機能を提供します：

1. **Kindle Unlimitedアソシエイトリンク生成スクリプト**
   - CSVファイルのタイトル列からKindle Unlimitedで商品を検索
   - Amazonアソシエイトリンクの自動生成
   - URL短縮機能対応

2. **X（Twitter）自動投稿ボット**
   - CSVファイルからランダムに投稿データを選択
   - GitHub Actions対応でサーバー常時稼働不要
   - 確率ベースのランダム投稿
   - 投稿履歴の自動管理

## 機能一覧

### Kindle Unlimitedリンク生成

- CSVファイルのタイトル列からKindle Unlimitedで商品を検索
- Amazon Product Advertising API (PA-API) 対応
- Amazonアソシエイトリンクの自動生成
- URL短縮機能（TinyURL API対応、Bitly API対応）
- 処理結果の統計情報表示
- レート制限対策（リクエスト間隔調整）

### X投稿ボット

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

### 2. Amazonアソシエイトタグの設定

スクリプト内の `affiliate_tag` 変数を実際のアソシエイトタグに変更してください：

```python
affiliate_tag = "your-affiliate-tag-20"  # 例: "yourname-20"
```

### 3. Amazon Product Advertising API (PA-API) の設定（推奨）

PA-APIを使用すると、より正確で効率的な商品検索が可能になります。

#### PA-API認証情報の取得

1. [Amazon Associates Central](https://affiliate-program.amazon.co.jp/) にログイン
2. 「ツール」→「Product Advertising API」を選択
3. 「API キーを取得」をクリック
4. 以下の情報を取得：
   - Access Key ID
   - Secret Access Key
   - パートナータグ（アソシエイトタグと同じ）

#### 設定ファイルの更新

`config.py` で以下の設定を更新：

```python
USE_PAAPI = True
PAAPI_ACCESS_KEY = "your-access-key"
PAAPI_SECRET_KEY = "your-secret-key"
PAAPI_PARTNER_TAG = "your-affiliate-tag-20"
```

### 4. X（Twitter）API設定（X投稿ボット使用時）

X Developer Portalでアプリケーションを作成し、以下の認証情報を取得してください：

1. **API Key** と **API Secret**
2. **Access Token** と **Access Token Secret**
3. **Bearer Token**

## 使用方法

### Kindle Unlimitedリンク生成

#### 基本版（スクレイピング）

```bash
python kindle_unlimited_link_generator.py
```

#### 改良版（URL短縮機能付き）

```bash
python kindle_unlimited_link_generator_advanced.py
```

#### 設定ファイル版

```bash
python kindle_unlimited_link_generator_config.py
```

#### PA-API対応版（推奨）

```bash
python kindle_unlimited_link_generator_paapi.py
```

### X投稿ボット

#### 基本版（ローカル実行）

```bash
python x_posting_bot.py
```

#### 設定ファイル対応版（ローカル実行）

```bash
python x_posting_bot_advanced.py
```

#### GitHub Actions版（自動実行）

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

## 入力ファイル形式

### Kindle Unlimitedリンク生成用CSV

CSVファイルは以下の形式である必要があります：

```csv
No,タイトル,一言紹介文
1,コンサル一年目が学ぶこと 新人・就活生からベテランまで一生役立つ究極のベーシックスキル30選,「仕事の基本がわからない」と悩む方に...
```

### X投稿ボット用CSV

以下の列が含まれている必要があります：

```csv
No,タイトル,一言紹介文,短縮URL
1,コンサル一年目が学ぶこと...,「仕事の基本がわからない」と悩む方に...,https://tinyurl.com/xxx
```

## 出力ファイル形式

### Kindle Unlimitedリンク生成

処理後のCSVファイルには以下の列が追加されます：

- `ASIN`: Amazon商品のASIN（PA-API使用時）
- `商品URL`: Amazon商品ページのURL
- `アソシエイトリンク`: アソシエイトパラメータ付きのURL
- `短縮URL`: 短縮されたURL
- `価格`: 商品価格（PA-API使用時）

### X投稿ボット

- `posting_history.json`: 投稿履歴（自動生成）
- `x_bot.log`: ログファイル（自動生成）

## 投稿文の形式

```
一言紹介文

短縮URL

#KUおすすめリスト
```

## PA-API vs スクレイピング

### PA-APIの利点

- **正確性**: 公式APIによる正確な商品情報
- **効率性**: 高速な検索処理
- **信頼性**: レート制限が明確
- **豊富な情報**: 価格、画像、レビュー数など
- **安定性**: サイト構造変更の影響を受けない

### スクレイピングの利点

- **設定不要**: APIキーが不要
- **即座に使用可能**: 追加設定なしで動作

## ファイル構成

```
x-posting-bot/
├── .github/workflows/
│   └── post.yml                    # GitHub Actions設定
├── kindle_unlimited_link_generator.py           # 基本版リンク生成
├── kindle_unlimited_link_generator_advanced.py  # 改良版リンク生成
├── kindle_unlimited_link_generator_config.py    # 設定ファイル版
├── kindle_unlimited_link_generator_paapi.py     # PA-API対応版
├── x_posting_bot.py                # 基本版X投稿ボット
├── x_posting_bot_advanced.py       # 設定ファイル対応版X投稿ボット
├── x_bot_config.py                 # 通常の設定ファイル
├── x_bot_config_github.py          # GitHub Actions用設定ファイル
├── config.py                       # Kindle Unlimited用設定
├── requirements.txt                 # Python依存関係
├── kindle_unlimited_biz_10_clean.csv            # 元データ
├── kindle_unlimited_biz_10_with_links.csv       # 処理済みデータ
├── posting_history.json            # 投稿履歴（自動生成）
├── x_bot.log                      # ログファイル（自動生成）
├── README.md                       # このファイル
├── X_BOT_README.md                # X投稿ボット詳細説明
├── GITHUB_ACTIONS_README.md       # GitHub Actions詳細説明
└── PAAPI_SETUP_GUIDE.md           # PA-API設定ガイド
```

## 注意事項

### Amazonアソシエイトプログラムについて

- Amazonアソシエイトプログラムに登録が必要です
- アソシエイトタグは必ず実際のものに変更してください
- 利用規約を遵守してください

### PA-APIについて

- PA-APIの利用には申請と承認が必要です
- 1日あたりのリクエスト制限があります
- 商用利用の場合は利用規約を確認してください

### X投稿ボットについて

- X（Twitter）APIのレート制限に注意してください
- 投稿内容は事前に確認してから実行してください
- GitHub Actionsの無料プランには実行時間制限があります

### レート制限について

- Amazonのサーバーに負荷をかけないよう、リクエスト間に1秒の待機時間を設けています
- 大量のリクエストを行う場合は、さらに長い間隔を設定することを推奨します

### URL短縮サービスについて

#### TinyURL（無料）
- APIキー不要
- 1日あたりの制限あり
- 基本的な短縮機能

#### Bitly（有料）
- APIキーが必要
- より詳細な分析機能
- カスタムドメイン対応

## トラブルシューティング

### Kindle Unlimitedリンク生成

1. **商品が見つからない**
   - タイトルが正確でない可能性があります
   - 検索結果の最初の商品が対象となります

2. **PA-API認証エラー**
   - 認証情報が正しく設定されているか確認してください
   - PA-APIの申請が承認されているか確認してください

3. **ネットワークエラー**
   - インターネット接続を確認してください
   - ファイアウォールの設定を確認してください

4. **CSVファイルエラー**
   - ファイルの文字エンコーディングがUTF-8であることを確認してください
   - カンマ区切り（CSV）形式であることを確認してください

### X投稿ボット

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

## カスタマイズ

### Kindle Unlimitedリンク生成

#### 検索パラメータの調整

PA-API使用時は、`search_kindle_unlimited_paapi` メソッド内のパラメータを調整できます：

```python
search_result = self.amazon.search_items(
    keywords=title,
    search_index="KindleStore",
    item_count=1,
    resources=[
        "Images.Primary.Medium",
        "ItemInfo.Title",
        "Offers.Listings.Price"
    ]
)
```

#### 待機時間の調整

レート制限を避けるため、`time.sleep(1)` の値を調整できます：

```python
time.sleep(2)  # 2秒待機
```

### X投稿ボット

#### 投稿時間の変更

```python
POSTING_HOURS = (9, 21)  # 9:00-21:00に変更
```

#### 投稿頻度の変更

```python
POSTS_PER_DAY = 5  # 1日5件に変更
POSTING_INTERVAL_MIN = (30, 60)  # 30-60分間隔に変更
```

#### 投稿テンプレートの変更

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

このスクリプトは教育目的で作成されています。商用利用の際は、AmazonアソシエイトプログラムとX（Twitter）の利用規約を遵守してください。

## サポート

問題や質問がある場合は、以下の点を確認してください：

1. 必要なパッケージがインストールされているか
2. Amazonアソシエイトタグが正しく設定されているか
3. PA-APIを使用する場合は認証情報が正しく設定されているか
4. X投稿ボットを使用する場合はX API認証情報が正しく設定されているか
5. 入力CSVファイルの形式が正しいか
6. インターネット接続が安定しているか

## 詳細ドキュメント

- [X投稿ボット詳細説明](X_BOT_README.md)
- [GitHub Actions詳細説明](GITHUB_ACTIONS_README.md)
- [PA-API設定ガイド](PAAPI_SETUP_GUIDE.md) 