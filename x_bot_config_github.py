# X投稿BOT設定ファイル（GitHub Actions対応版）

import os

# 投稿設定（GitHub Actions対応）
POSTING_HOURS = (9, 22)  # 投稿時間: 9:00-22:00
POSTS_PER_DAY = 9  # 1日最大9件
POSTING_INTERVAL_MIN = (60, 120)  # 投稿間隔: 60-120分（1-2時間）

# GitHub Actions用設定
GITHUB_ACTIONS_MODE = True  # GitHub Actions実行モード
MIN_POSTING_PROBABILITY = 0.5  # 最小投稿確率（30%→50%に変更）
MAX_POSTING_PROBABILITY = 0.9  # 最大投稿確率（80%→90%に変更）

# ファイル設定
CSV_FILE = "kindle_unlimited_biz_10_with_links.csv"  # 新しい出力ファイル名
POSTING_HISTORY_FILE = "posting_history.json"

# テスト設定
TEST_MODE = False  # False: 実際のX投稿を有効にする

# X（Twitter）API設定（環境変数から取得）
X_API_KEY = os.getenv('X_API_KEY', "your-x-api-key")
X_API_SECRET = os.getenv('X_API_SECRET', "your-x-api-secret")
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN', "your-x-access-token")
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET', "your-x-access-token-secret")
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN', "your-x-bearer-token")

# 投稿テンプレート
POST_TEMPLATES = [
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
    "{introduction}\n\n{short_url}\n\n#KUおすすめリスト"
]

# エラー通知設定
ERROR_NOTIFICATION = True  # エラー時の通知
LOG_FILE = "x_bot.log"  # ログファイル 