# Kindle Unlimited アソシエイトリンク生成スクリプト

このスクリプトは、CSVファイル内のタイトル列を使ってKindle Unlimitedで検索し、Amazonアソシエイトリンクの短縮URLを生成するツールです。

## 機能

- CSVファイルのタイトル列からKindle Unlimitedで商品を検索
- Amazon Product Advertising API (PA-API) 対応
- Amazonアソシエイトリンクの自動生成
- URL短縮機能（TinyURL API対応、Bitly API対応）
- 処理結果の統計情報表示
- レート制限対策（リクエスト間隔調整）

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

## 使用方法

### 基本版（スクレイピング）

```bash
python kindle_unlimited_link_generator.py
```

### 改良版（URL短縮機能付き）

```bash
python kindle_unlimited_link_generator_advanced.py
```

### 設定ファイル版

```bash
python kindle_unlimited_link_generator_config.py
```

### PA-API対応版（推奨）

```bash
python kindle_unlimited_link_generator_paapi.py
```

## 入力ファイル形式

CSVファイルは以下の形式である必要があります：

```csv
No,タイトル,一言紹介文
1,コンサル一年目が学ぶこと 新人・就活生からベテランまで一生役立つ究極のベーシックスキル30選,「仕事の基本がわからない」と悩む方に...
```

## 出力ファイル形式

処理後のCSVファイルには以下の列が追加されます：

- `ASIN`: Amazon商品のASIN（PA-API使用時）
- `商品URL`: Amazon商品ページのURL
- `アソシエイトリンク`: アソシエイトパラメータ付きのURL
- `短縮URL`: 短縮されたURL
- `価格`: 商品価格（PA-API使用時）

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

## 注意事項

### Amazonアソシエイトプログラムについて

- Amazonアソシエイトプログラムに登録が必要です
- アソシエイトタグは必ず実際のものに変更してください
- 利用規約を遵守してください

### PA-APIについて

- PA-APIの利用には申請と承認が必要です
- 1日あたりのリクエスト制限があります
- 商用利用の場合は利用規約を確認してください

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

### よくある問題

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

## カスタマイズ

### 検索パラメータの調整

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

### 待機時間の調整

レート制限を避けるため、`time.sleep(1)` の値を調整できます：

```python
time.sleep(2)  # 2秒待機
```

## ライセンス

このスクリプトは教育目的で作成されています。商用利用の際は、Amazonアソシエイトプログラムの利用規約を遵守してください。

## サポート

問題や質問がある場合は、以下の点を確認してください：

1. 必要なパッケージがインストールされているか
2. Amazonアソシエイトタグが正しく設定されているか
3. PA-APIを使用する場合は認証情報が正しく設定されているか
4. 入力CSVファイルの形式が正しいか
5. インターネット接続が安定しているか 