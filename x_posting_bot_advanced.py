import pandas as pd
import random
import time
import json
import os
import logging
from datetime import datetime, timedelta
import schedule
import threading
import tweepy

# 設定ファイルの読み込み（GitHub Actions対応版を優先）
try:
    from x_bot_config_github import *
    print("GitHub Actions用設定ファイルを使用")
except ImportError:
    try:
        from x_bot_config import *
        print("通常の設定ファイルを使用")
    except ImportError:
        print("設定ファイルが見つかりません。")
        exit(1)

# テスト用設定のインポート
try:
    from x_bot_config_github import TEST_POSTING_HOURS, TEST_POSTS_PER_DAY
except ImportError:
    TEST_POSTING_HOURS = (0, 23)
    TEST_POSTS_PER_DAY = 999

class XPostingBotAdvanced:
    def __init__(self):
        """
        X投稿BOTの初期化（GitHub Actions対応版）
        """
        self.csv_file = CSV_FILE
        self.posting_history_file = POSTING_HISTORY_FILE
        
        # 設定を読み込み
        self.posting_hours = POSTING_HOURS
        self.posts_per_day = POSTS_PER_DAY
        self.posting_interval_min = POSTING_INTERVAL_MIN
        self.test_mode = TEST_MODE
        self.post_templates = POST_TEMPLATES
        self.error_notification = ERROR_NOTIFICATION
        self.log_file = LOG_FILE
        
        # GitHub Actions用設定
        self.github_actions_mode = GITHUB_ACTIONS_MODE
        self.min_posting_probability = MIN_POSTING_PROBABILITY
        self.max_posting_probability = MAX_POSTING_PROBABILITY
        
        # 先にログ設定
        self.setup_logging()
        
        # テスト用設定の確認
        test_mode_env = os.getenv('TEST_MODE', 'false').lower()
        if test_mode_env == 'true':
            # テストモードでは投稿時間制限を外す
            self.posting_hours = TEST_POSTING_HOURS
            self.posts_per_day = POSTS_PER_DAY  # 本番と同じ9回制限
            self.test_mode = True
            self.logger.info("テストモードが有効です（投稿時間制限なし、9回制限あり）")
        
        # 投稿履歴を読み込み
        self.posting_history = self.load_posting_history()
        
        # X API設定
        self.x_api_key = X_API_KEY
        self.x_api_secret = X_API_SECRET
        self.x_access_token = X_ACCESS_TOKEN
        self.x_access_token_secret = X_ACCESS_TOKEN_SECRET
        self.x_bearer_token = X_BEARER_TOKEN
        
        # X APIクライアントの初期化
        self.x_client = None
        if not self.test_mode:
            self.setup_x_api()
        
        # 統計情報
        self.stats = {
            'total_posts': 0,
            'successful_posts': 0,
            'failed_posts': 0,
            'last_post_time': None
        }
        
        self.logger.info("X投稿BOT初期化完了（GitHub Actions対応版）")
        self.logger.info(f"投稿時間: {self.posting_hours[0]}:00-{self.posting_hours[1]}:00")
        self.logger.info(f"投稿頻度: 1日に{self.posts_per_day}件")
        self.logger.info(f"GitHub Actionsモード: {'有効' if self.github_actions_mode else '無効'}")
        self.logger.info(f"テストモード: {'有効' if self.test_mode else '無効'}")
    
    def setup_x_api(self):
        """
        X（Twitter）APIクライアントを初期化
        """
        try:
            # OAuth 1.0a User Context認証
            auth = tweepy.OAuthHandler(self.x_api_key, self.x_api_secret)
            auth.set_access_token(self.x_access_token, self.x_access_token_secret)
            
            # API v2クライアント
            self.x_client = tweepy.Client(
                bearer_token=self.x_bearer_token,
                consumer_key=self.x_api_key,
                consumer_secret=self.x_api_secret,
                access_token=self.x_access_token,
                access_token_secret=self.x_access_token_secret,
                wait_on_rate_limit=True
            )
            
            # 認証テスト
            me = self.x_client.get_me()
            self.logger.info(f"X API認証成功: @{me.data.username}")
            
        except Exception as e:
            self.logger.error(f"X API初期化エラー: {e}")
            print(f"X API初期化エラー: {e}")
            print("テストモードに切り替えます")
            self.test_mode = True
            self.x_client = None
    
    def setup_logging(self):
        """
        ログ設定を初期化
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_posting_history(self):
        """
        投稿履歴を読み込み
        """
        if os.path.exists(self.posting_history_file):
            try:
                with open(self.posting_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # 日付が変わった場合、古い投稿履歴を自動削除
                today = datetime.now().strftime('%Y-%m-%d')
                cleaned_history = {}
                for index_str, post_date in history.items():
                    if post_date == today:
                        cleaned_history[index_str] = post_date
                
                # 古い履歴が削除された場合、ファイルを更新
                if len(cleaned_history) != len(history):
                    with open(self.posting_history_file, 'w', encoding='utf-8') as f:
                        json.dump(cleaned_history, f, ensure_ascii=False, indent=2)
                    self.logger.info(f"古い投稿履歴を自動削除しました (削除前: {len(history)}件 → 削除後: {len(cleaned_history)}件)")
                else:
                    self.logger.info(f"投稿履歴読み込み完了: {len(cleaned_history)}件")
                
                return cleaned_history
                
            except Exception as e:
                self.logger.error(f"投稿履歴読み込みエラー: {e}")
                return {}
        return {}
    
    def save_posting_history(self):
        """
        投稿履歴を保存
        """
        try:
            with open(self.posting_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.posting_history, f, ensure_ascii=False, indent=2)
            self.logger.info(f"投稿履歴を保存しました: {len(self.posting_history)}件")
        except Exception as e:
            self.logger.error(f"投稿履歴保存エラー: {e}")
    
    def add_to_posting_history(self, post_data):
        """
        投稿履歴に追加
        """
        today = datetime.now().strftime('%Y-%m-%d')
        index_str = str(post_data['index'])
        
        # 重複チェック
        if index_str in self.posting_history and self.posting_history[index_str] == today:
            self.logger.warning(f"重複投稿を防ぎました: {index_str} (今日既に投稿済み)")
            return False
        
        # 投稿履歴に追加
        self.posting_history[index_str] = today
        self.save_posting_history()
        
        self.logger.info(f"投稿履歴に追加: {index_str} -> {today}")
        return True
    
    def load_csv_data(self):
        """
        CSVファイルから投稿データを読み込み
        """
        try:
            if not os.path.exists(self.csv_file):
                self.logger.error(f"CSVファイルが見つかりません: {self.csv_file}")
                return []
            
            df = pd.read_csv(self.csv_file)
            available_posts = []
            
            for index, row in df.iterrows():
                # 短縮URLがある行のみ対象
                if pd.notna(row['短縮URL']) and row['短縮URL'] != '':
                    post_data = {
                        'index': row['No'],  # No列を使用
                        'title': row['タイトル'],
                        'introduction': row['一言紹介文'],
                        'short_url': row['短縮URL']
                    }
                    available_posts.append(post_data)
            
            self.logger.info(f"投稿可能データ: {len(available_posts)}件")
            return available_posts
            
        except Exception as e:
            self.logger.error(f"CSV読み込みエラー: {e}")
            return []
    
    def get_posted_today_count(self):
        """
        今日の投稿数を取得（統一されたカウント処理）
        """
        today = datetime.now().strftime('%Y-%m-%d')
        posted_today = len([k for k, v in self.posting_history.items() if v == today])
        
        # デバッグ情報を追加
        self.logger.info(f"今日({today})の投稿数: {posted_today}件")
        if posted_today > 0:
            posted_items = [k for k, v in self.posting_history.items() if v == today]
            self.logger.info(f"投稿済みアイテム: {posted_items}")
        
        return posted_today
    
    def get_available_posts(self, available_posts):
        """
        今日まだ投稿していない投稿データを取得
        """
        today = datetime.now().strftime('%Y-%m-%d')
        posted_today = set()
        
        # 今日投稿済みのインデックスを取得
        for index_str, post_date in self.posting_history.items():
            if post_date == today:
                posted_today.add(int(index_str))
        
        # 今日投稿していないデータをフィルタ
        available_today = [post for post in available_posts if post['index'] not in posted_today]
        
        # 1日の投稿制限をチェック
        posted_count = self.get_posted_today_count()
        if posted_count >= self.posts_per_day:
            self.logger.info(f"今日の投稿制限({self.posts_per_day}件)に達しました")
            return []
        
        self.logger.info(f"今日投稿可能: {len(available_today)}件 (今日の投稿数: {posted_count}/{self.posts_per_day})")
        return available_today
    
    def create_post_content(self, post_data):
        """
        投稿内容を作成
        """
        template = random.choice(self.post_templates)
        content = template.format(
            introduction=post_data['introduction'],
            short_url=post_data['short_url']
        )
        
        return content
    
    def post_to_x(self, content, post_data):
        """
        Xに投稿（テストモードではターミナルに表示、実際の投稿も実行）
        """
        current_time = datetime.now()
        
        try:
            if self.test_mode:
                # テストモード：ターミナルに表示
                print("\n" + "="*60)
                print(f"📱 X投稿イメージ ({current_time.strftime('%Y-%m-%d %H:%M:%S')})")
                print("="*60)
                print(content)
                print("="*60)
                print(f"📊 投稿データ:")
                print(f"   No: {post_data['index']}")
                print(f"   タイトル: {post_data['title']}")
                print("="*60)
                
                self.logger.info(f"テスト投稿成功: {post_data['title'][:30]}...")
            else:
                # 実際のX投稿処理
                if self.x_client:
                    # 投稿実行
                    response = self.x_client.create_tweet(text=content)
                    tweet_id = response.data['id']
                    
                    self.logger.info(f"X投稿成功: Tweet ID {tweet_id}")
                    print(f"✅ X投稿成功: {post_data['title'][:30]}...")
                    print(f"   Tweet ID: {tweet_id}")
                else:
                    self.logger.error("X APIクライアントが初期化されていません")
                    print("❌ X APIクライアントが初期化されていません")
                    return False
            
            # 新しい履歴管理機能を使用
            if not self.add_to_posting_history(post_data):
                self.logger.warning("重複投稿を防ぎました")
                return False
            
            # 統計情報を更新
            self.stats['total_posts'] += 1
            self.stats['successful_posts'] += 1
            self.stats['last_post_time'] = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            return True
            
        except Exception as e:
            self.logger.error(f"投稿エラー: {e}")
            print(f"❌ 投稿エラー: {e}")
            self.stats['failed_posts'] += 1
            return False
    
    def schedule_random_posts(self):
        """
        ランダムな時間に投稿をスケジュール
        """
        try:
            available_posts = self.load_csv_data()
            if not available_posts:
                self.logger.warning("投稿可能なデータがありません")
                return False
            
            available_today = self.get_available_posts(available_posts)
            if not available_today:
                posted_count = self.get_posted_today_count()
                if posted_count >= self.posts_per_day:
                    self.logger.warning(f"今日の投稿制限({self.posts_per_day}件)に達しました")
                    print(f"今日の投稿制限({self.posts_per_day}件)に達しました")
                else:
                    self.logger.warning("今日投稿可能なデータがありません")
                return False
            
            # ランダムに投稿データを選択
            post_data = random.choice(available_today)
            content = self.create_post_content(post_data)
            
            # 投稿実行
            success = self.post_to_x(content, post_data)
            
            if success:
                self.logger.info(f"投稿成功: {post_data['title'][:30]}...")
            else:
                self.logger.error(f"投稿失敗: {post_data['title'][:30]}...")
            
            return success
            
        except Exception as e:
            self.logger.error(f"投稿スケジュールエラー: {e}")
            return False
    
    def should_post_now(self):
        """
        GitHub Actions対応の投稿判定ロジック
        現在が投稿時間内で、ランダム確率で投稿するかどうかを判定
        """
        # GitHub ActionsはUTC時間で動作するため、日本時間に変換
        current_hour = datetime.now().hour
        jst_hour = (current_hour + 9) % 24  # UTC+9で日本時間
        
        self.logger.info(f"UTC時間: {current_hour}時, 日本時間: {jst_hour}時")
        
        # 投稿時間外の場合は投稿しない（日本時間で判定）
        if not (self.posting_hours[0] <= jst_hour <= self.posting_hours[1]):
            self.logger.info(f"投稿時間外です（日本時間: {jst_hour}時、投稿時間: {self.posting_hours[0]}-{self.posting_hours[1]}時）")
            print(f"⏭️ 投稿時間外（日本時間: {jst_hour}時）")
            return False
        
        # 今日の投稿回数をチェック
        today_posts = self.get_posted_today_count()
        
        # 今日の上限に達している場合は投稿しない
        if today_posts >= self.posts_per_day:
            self.logger.info(f"今日の投稿制限に達しています（{today_posts}/{self.posts_per_day}件）")
            print(f"⏭️ 今日の投稿制限に達しています（{today_posts}/{self.posts_per_day}件）")
            return False
        
        # 残り時間と残り投稿回数で確率を調整（日本時間で計算）
        remaining_hours = self.posting_hours[1] - jst_hour + 1
        remaining_posts = self.posts_per_day - today_posts
        
        # 効率的な投稿確率計算
        if remaining_posts >= remaining_hours:
            # 残り投稿数が残り時間より多い場合、高確率で投稿
            probability = self.max_posting_probability
        else:
            # 残り投稿数が少ない場合、確率を調整
            base_probability = remaining_posts / remaining_hours
            probability = max(self.min_posting_probability, 
                            min(self.max_posting_probability, base_probability * 0.8))
        
        # ランダム判定
        should_post = random.random() < probability
        
        self.logger.info(f"投稿判定: 日本時間{jst_hour}時, 今日{today_posts}/{self.posts_per_day}件, "
                        f"残り{remaining_posts}件, 確率{probability:.2f}, 結果{'投稿' if should_post else 'スキップ'}")
        
        if should_post:
            print(f"✅ 投稿判定: 日本時間{jst_hour}時, 今日{today_posts}/{self.posts_per_day}件, 残り{remaining_posts}件, 確率{probability:.2f}")
        else:
            print(f"⏭️ 投稿スキップ: 日本時間{jst_hour}時, 今日{today_posts}/{self.posts_per_day}件, 残り{remaining_posts}件, 確率{probability:.2f}")
        
        return should_post
    
    def get_next_posting_time(self):
        """
        次の投稿時間を計算（1日の投稿制限を考慮）
        """
        posted_today = self.get_posted_today_count()
        
        if posted_today >= self.posts_per_day:
            # 今日の投稿制限に達した場合、明日まで待機
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # 残り投稿可能件数
        remaining_posts = self.posts_per_day - posted_today
        
        # 残り時間を計算（現在時刻から22:00まで）
        now = datetime.now()
        end_time = now.replace(hour=22, minute=0, second=0, microsecond=0)
        
        if now >= end_time:
            # 22:00を過ぎている場合、明日まで待機
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # 残り時間を残り投稿数で割って、適切な間隔を計算
        remaining_minutes = (end_time - now).total_seconds() / 60
        if remaining_posts > 0:
            # 残り時間を残り投稿数で割り、ランダム要素を加える
            base_interval = remaining_minutes / remaining_posts
            # 基本間隔の±30%の範囲でランダム化
            min_interval = max(60, base_interval * 0.7)  # 最低60分
            max_interval = min(180, base_interval * 1.3)  # 最高180分
            interval_minutes = random.uniform(min_interval, max_interval)
        else:
            interval_minutes = random.randint(60, 120)
        
        return now + timedelta(minutes=interval_minutes)
    
    def print_stats(self):
        """
        統計情報を表示
        """
        print("\n" + "="*50)
        print("📊 BOT統計情報")
        print("="*50)
        print(f"総投稿数: {self.stats['total_posts']}")
        print(f"成功投稿数: {self.stats['successful_posts']}")
        print(f"失敗投稿数: {self.stats['failed_posts']}")
        print(f"成功率: {self.stats['successful_posts']/max(1, self.stats['total_posts'])*100:.1f}%")
        print(f"最後の投稿: {self.stats['last_post_time'] or 'なし'}")
        print("="*50)
    
    def run_bot(self):
        """
        GitHub Actions対応のBOT実行（単発実行）
        """
        self.logger.info("X投稿BOT開始（GitHub Actions対応版）")
        print("X投稿BOT開始（GitHub Actions対応版）")
        
        # 投稿判定を実行
        if self.should_post_now():
            success = self.schedule_random_posts()
            
            if success:
                self.logger.info("投稿処理完了")
                print("✅ 投稿処理完了")
            else:
                self.logger.warning("投稿処理失敗")
                print("❌ 投稿処理失敗")
        else:
            self.logger.info("投稿スキップ（条件不適合）")
            print("⏭️ 投稿スキップ（条件不適合）")
        
        # 統計情報を表示
        self.print_stats()
        
        self.logger.info("X投稿BOT終了")
        print("X投稿BOT終了")

def main():
    print("X投稿BOT GitHub Actions対応版")
    print("="*60)
    
    # X API設定の確認
    if not TEST_MODE:
        if (X_API_KEY == "your-x-api-key" or X_API_SECRET == "your-x-api-secret" or 
            X_ACCESS_TOKEN == "your-x-access-token" or X_ACCESS_TOKEN_SECRET == "your-x-access-token-secret" or
            X_BEARER_TOKEN == "your-x-bearer-token"):
            print("警告: X API認証情報がデフォルト値のままです。")
            print("x_bot_config.py で実際のX API認証情報に変更してください。")
            print("テストモードで続行します。")
            # テストモードに強制変更
            import x_bot_config
            x_bot_config.TEST_MODE = True
    
    # BOT初期化
    bot = XPostingBotAdvanced()
    
    # 今日の投稿履歴を確認
    today = datetime.now().strftime('%Y-%m-%d')
    posted_today = bot.get_posted_today_count()
    remaining_posts = bot.posts_per_day - posted_today
    
    # 現在時刻の情報を表示
    current_time = datetime.now()
    print(f"実行時刻: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"今日({today})の投稿数: {posted_today}/{bot.posts_per_day}件 (残り{remaining_posts}件)")
    
    # BOT実行
    bot.run_bot()

if __name__ == "__main__":
    main() 