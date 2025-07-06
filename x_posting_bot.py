import pandas as pd
import random
import time
import json
import os
from datetime import datetime, timedelta
import schedule
import threading

class XPostingBot:
    def __init__(self, csv_file="kindle_unlimited_biz_10_with_links.csv"):
        """
        X投稿BOTの初期化
        
        Args:
            csv_file (str): 投稿データが含まれるCSVファイル
        """
        self.csv_file = csv_file
        self.posting_history_file = "posting_history.json"
        self.posting_history = self.load_posting_history()
        
        # 投稿設定
        self.posting_hours = (8, 22)  # 8:00-22:00
        self.posts_per_hour = (2, 3)  # 1時間に2-3回
        self.test_mode = True  # テストモード（実際の投稿は行わない）
        
        print("X投稿BOT初期化完了")
        print(f"投稿時間: {self.posting_hours[0]}:00-{self.posting_hours[1]}:00")
        print(f"投稿頻度: 1時間に{self.posts_per_hour[0]}-{self.posts_per_hour[1]}回")
        print(f"テストモード: {'有効' if self.test_mode else '無効'}")
    
    def load_posting_history(self):
        """
        投稿履歴を読み込み
        
        Returns:
            dict: 投稿履歴
        """
        if os.path.exists(self.posting_history_file):
            try:
                with open(self.posting_history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"投稿履歴読み込みエラー: {e}")
                return {}
        return {}
    
    def save_posting_history(self):
        """
        投稿履歴を保存
        """
        try:
            with open(self.posting_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.posting_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"投稿履歴保存エラー: {e}")
    
    def load_csv_data(self):
        """
        CSVファイルから投稿データを読み込み
        
        Returns:
            list: 投稿可能なデータのリスト
        """
        try:
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
            
            print(f"投稿可能データ: {len(available_posts)}件")
            return available_posts
            
        except Exception as e:
            print(f"CSV読み込みエラー: {e}")
            return []
    
    def get_available_posts(self, available_posts):
        """
        今日まだ投稿していない投稿データを取得
        
        Args:
            available_posts (list): 全投稿データ
            
        Returns:
            list: 今日投稿可能なデータ
        """
        today = datetime.now().strftime('%Y-%m-%d')
        posted_today = set()
        
        # 今日投稿済みのインデックスを取得
        for index_str, post_date in self.posting_history.items():
            if post_date == today:
                posted_today.add(int(index_str))
        
        # 今日投稿していないデータをフィルタ
        available_today = [post for post in available_posts if post['index'] not in posted_today]
        
        print(f"今日投稿可能: {len(available_today)}件")
        return available_today
    
    def create_post_content(self, post_data):
        """
        投稿内容を作成
        
        Args:
            post_data (dict): 投稿データ
            
        Returns:
            str: 投稿内容
        """
        # 投稿テンプレート（1行目のタイトルを削除）
        templates = [
            "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
            "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
            "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
            "{introduction}\n\n{short_url}\n\n#KUおすすめリスト",
            "{introduction}\n\n{short_url}\n\n#KUおすすめリスト"
        ]
        
        template = random.choice(templates)
        content = template.format(
            introduction=post_data['introduction'],
            short_url=post_data['short_url']
        )
        
        return content
    
    def post_to_x(self, content, post_data):
        """
        Xに投稿（テストモードではターミナルに表示）
        
        Args:
            content (str): 投稿内容
            post_data (dict): 投稿データ
        """
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.test_mode:
            # テストモード：ターミナルに表示
            print("\n" + "="*60)
            print(f"📱 X投稿イメージ ({current_time})")
            print("="*60)
            print(content)
            print("="*60)
            print(f"📊 投稿データ:")
            print(f"   No: {post_data['index']}")
            print(f"   タイトル: {post_data['title']}")
            print("="*60)
        else:
            # 実際のX投稿処理（将来的に実装）
            print(f"実際のX投稿: {content[:50]}...")
        
        # 投稿履歴に記録
        today = datetime.now().strftime('%Y-%m-%d')
        self.posting_history[str(post_data['index'])] = today
        self.save_posting_history()
    
    def schedule_random_posts(self):
        """
        ランダムな時間に投稿をスケジュール
        """
        available_posts = self.load_csv_data()
        if not available_posts:
            print("投稿可能なデータがありません")
            return
        
        available_today = self.get_available_posts(available_posts)
        if not available_today:
            print("今日投稿可能なデータがありません")
            return
        
        # ランダムに投稿データを選択
        post_data = random.choice(available_today)
        content = self.create_post_content(post_data)
        
        # 投稿実行
        self.post_to_x(content, post_data)
    
    def is_posting_time(self):
        """
        現在が投稿時間内かチェック
        
        Returns:
            bool: 投稿時間内かどうか
        """
        current_hour = datetime.now().hour
        return self.posting_hours[0] <= current_hour < self.posting_hours[1]
    
    def run_bot(self):
        """
        BOTを実行
        """
        print("X投稿BOT開始")
        print("投稿時間外の場合は待機します")
        
        while True:
            try:
                if self.is_posting_time():
                    self.schedule_random_posts()
                    
                    # ランダムな間隔で次の投稿をスケジュール
                    interval_minutes = random.randint(20, 40)  # 20-40分間隔
                    print(f"次の投稿まで {interval_minutes} 分待機")
                    time.sleep(interval_minutes * 60)
                else:
                    # 投稿時間外は1時間待機
                    print("投稿時間外です。1時間後に再チェック")
                    time.sleep(60 * 60)
                    
            except KeyboardInterrupt:
                print("\nBOTを停止します")
                break
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                print("BOTを停止します")
                break
    
    def test_single_post(self):
        """
        単発投稿テスト
        """
        print("単発投稿テストを実行します")
        self.schedule_random_posts()

def main():
    print("X投稿BOT テスト版")
    print("="*50)
    
    # BOT初期化
    bot = XPostingBot()
    
    # 単発テスト
    bot.test_single_post()
    
    # 継続実行するか確認
    response = input("\n継続実行しますか？ (y/N): ")
    if response.lower() == 'y':
        bot.run_bot()
    else:
        print("テスト終了")

if __name__ == "__main__":
    main() 