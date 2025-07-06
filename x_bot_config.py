# X投稿BOT設定ファイル

# 投稿設定（GitHub Actions対応）
POSTING_HOURS = (9, 22)  # 投稿時間: 9:00-22:00
POSTS_PER_DAY = 9  # 1日最大9件
POSTING_INTERVAL_MIN = (60, 120)  # 投稿間隔: 60-120分（1-2時間）

# GitHub Actions用設定
GITHUB_ACTIONS_MODE = True  # GitHub Actions実行モード
MIN_POSTING_PROBABILITY = 0.3  # 最小投稿確率
MAX_POSTING_PROBABILITY = 0.8  # 最大投稿確率

# ファイル設定
CSV_FILE = "kindle_unlimited_biz_10_with_links.csv"  # 新しい出力ファイル名
POSTING_HISTORY_FILE = "posting_history.json"

# テスト設定
TEST_MODE = False  # False: 実際のX投稿を有効にする

# X（Twitter）API設定
X_API_KEY = "7jVdeL25hg6pzUa2gMMW5ow3x"
X_API_SECRET = "oEpwpunURdCy9g3RTOajqmecXXNzs7UFW8W5YWMsvnDJEQsOaA"
X_ACCESS_TOKEN = "1936333255432978435-2As5zNVXHdGDyNxcj0Fy24lNfNf38C"
X_ACCESS_TOKEN_SECRET = "YTqf9fO1BS6Y6qzqvWxapOBjbPtBNlfwyCwZsRYRWGGcN"
X_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJyb2gEAAAAAdwCBB1v0X%2Ff56kB24%2BgiBE0U7Jk%3DRCarLNCS04bo9lvGXXwgkDRbHryv8nAf2SzhGDUaaVzn2uMtp1"

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