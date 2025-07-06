# Kindle Unlimited アソシエイトリンク生成スクリプト設定ファイル
# このファイルを config.py にコピーして、実際の値に変更してください

# Amazonアソシエイトタグ（必須）
# Amazonアソシエイトプログラムで取得したタグを設定してください
AFFILIATE_TAG = "kotora01409-22"  # 例: "yourname-20"

# Amazon Product Advertising API設定（推奨）
# Amazon PA-APIを使用する場合は、以下の設定が必要です
USE_PAAPI = True  # True: PA-APIを使用, False: スクレイピングを使用

# PA-API認証情報（Amazon Associates Centralで取得）
PAAPI_ACCESS_KEY = "AKPAFNQY581750389326"  # Access Key ID
PAAPI_SECRET_KEY = "zsfRAVAJEmC2xgeDcVdih/6EMSLdkWgQyLUV7LIL"  # Secret Access Key
PAAPI_PARTNER_TAG = "kotora01409-22"  # パートナータグ（アソシエイトタグと同じ）
PAAPI_HOST = "webservices.amazon.co.jp"  # 日本の場合は固定
PAAPI_REGION = "us-west-2"  # リージョン（日本の場合は固定）

# URL短縮機能の設定
USE_URL_SHORTENER = True  # True: 短縮機能を使用, False: 使用しない

# Bitly API設定（オプション）
# Bitlyを使用する場合は、有効なAPIトークンを設定してください
BITLY_TOKEN = None  # 例: "your-bitly-token"

# ファイル設定
INPUT_FILE = "kindle_unlimited_biz_10_clean.csv"
OUTPUT_FILE = "kindle_unlimited_biz_10_with_links.csv"

# レート制限設定
REQUEST_DELAY = 1  # リクエスト間の待機時間（秒）

# 検索設定
SEARCH_TIMEOUT = 10  # 検索リクエストのタイムアウト時間（秒）

# デバッグ設定
DEBUG_MODE = False  # True: デバッグ情報を表示, False: 最小限の情報のみ表示 