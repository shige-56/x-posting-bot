import pandas as pd
import requests
import time
import re
from urllib.parse import quote
import json
import os

# 設定ファイルの読み込み
try:
    from config import *
except ImportError:
    print("設定ファイル config.py が見つかりません。")
    print("config_example.py を config.py にコピーして、実際の値に変更してください。")
    exit(1)

class KindleUnlimitedLinkGenerator:
    def __init__(self):
        """
        Kindle Unlimitedリンク生成器の初期化
        設定ファイルから設定を読み込みます
        """
        self.affiliate_tag = AFFILIATE_TAG
        self.use_url_shortener = USE_URL_SHORTENER
        self.request_delay = REQUEST_DELAY
        self.search_timeout = SEARCH_TIMEOUT
        self.debug_mode = DEBUG_MODE
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        if self.debug_mode:
            print(f"設定読み込み完了:")
            print(f"  アソシエイトタグ: {self.affiliate_tag}")
            print(f"  URL短縮機能: {self.use_url_shortener}")
            print(f"  リクエスト間隔: {self.request_delay}秒")
            print(f"  タイムアウト: {self.search_timeout}秒")
    
    def search_kindle_unlimited(self, title):
        """
        Kindle Unlimitedでタイトルを検索して商品URLを取得
        
        Args:
            title (str): 検索するタイトル
            
        Returns:
            str: 商品URL（見つからない場合はNone）
        """
        try:
            # Kindle Unlimitedの検索URL
            search_url = "https://www.amazon.co.jp/s"
            params = {
                'k': title,
                'i': 'digital-text',  # Kindleストア
                'ref': 'sr_nr_i_0'
            }
            
            if self.debug_mode:
                print(f"  検索URL: {search_url}")
                print(f"  検索パラメータ: {params}")
            
            response = self.session.get(search_url, params=params, timeout=self.search_timeout)
            response.raise_for_status()
            
            # 最初の商品リンクを探す
            product_pattern = r'href="(/dp/[A-Z0-9]{10})'
            matches = re.findall(product_pattern, response.text)
            
            if matches:
                product_id = matches[0]
                product_url = f"https://www.amazon.co.jp{product_id}"
                
                if self.debug_mode:
                    print(f"  商品URL発見: {product_url}")
                
                return product_url
            
            if self.debug_mode:
                print(f"  商品URLが見つかりませんでした")
            
            return None
            
        except Exception as e:
            print(f"検索エラー ({title}): {e}")
            return None
    
    def create_affiliate_link(self, product_url):
        """
        Amazonアソシエイトリンクを作成
        
        Args:
            product_url (str): 商品URL
            
        Returns:
            str: アソシエイトリンク
        """
        if not product_url:
            return None
        
        # アソシエイトパラメータを追加
        separator = '&' if '?' in product_url else '?'
        affiliate_url = f"{product_url}{separator}tag={self.affiliate_tag}"
        
        if self.debug_mode:
            print(f"  アソシエイトリンク作成: {affiliate_url}")
        
        return affiliate_url
    
    def shorten_url_tinyurl(self, url):
        """
        TinyURL APIを使用してURLを短縮
        
        Args:
            url (str): 短縮するURL
            
        Returns:
            str: 短縮URL（エラーの場合は元のURL）
        """
        if not self.use_url_shortener:
            return url
            
        try:
            tinyurl_api = "http://tinyurl.com/api-create.php"
            params = {'url': url}
            
            response = self.session.get(tinyurl_api, params=params, timeout=self.search_timeout)
            response.raise_for_status()
            
            short_url = response.text
            
            if self.debug_mode:
                print(f"  TinyURL短縮: {short_url}")
            
            return short_url
            
        except Exception as e:
            print(f"TinyURL短縮エラー: {e}")
            return url
    
    def shorten_url_bitly(self, url):
        """
        Bitly APIを使用してURLを短縮
        
        Args:
            url (str): 短縮するURL
            
        Returns:
            str: 短縮URL（エラーの場合は元のURL）
        """
        if not self.use_url_shortener or not BITLY_TOKEN:
            return url
            
        try:
            bitly_api = "https://api-ssl.bitly.com/v4/shorten"
            headers = {
                'Authorization': f'Bearer {BITLY_TOKEN}',
                'Content-Type': 'application/json'
            }
            data = {'long_url': url}
            
            response = self.session.post(bitly_api, headers=headers, json=data, timeout=self.search_timeout)
            response.raise_for_status()
            
            result = response.json()
            short_url = result.get('link', url)
            
            if self.debug_mode:
                print(f"  Bitly短縮: {short_url}")
            
            return short_url
            
        except Exception as e:
            print(f"Bitly短縮エラー: {e}")
            return url
    
    def process_csv(self):
        """
        CSVファイルを処理してアソシエイトリンクを追加
        設定ファイルからファイル名を読み込みます
        """
        try:
            # 入力ファイルの存在確認
            if not os.path.exists(INPUT_FILE):
                print(f"エラー: 入力ファイル '{INPUT_FILE}' が見つかりません。")
                return
            
            # CSVファイルを読み込み
            df = pd.read_csv(INPUT_FILE)
            
            # 新しい列を追加
            df['商品URL'] = ''
            df['アソシエイトリンク'] = ''
            df['短縮URL'] = ''
            
            print(f"合計 {len(df)} 件のタイトルを処理します...")
            print(f"URL短縮機能: {'有効' if self.use_url_shortener else '無効'}")
            print(f"リクエスト間隔: {self.request_delay}秒")
            print("-" * 50)
            
            success_count = 0
            
            for index, row in df.iterrows():
                title = row['タイトル']
                print(f"処理中 ({index + 1}/{len(df)}): {title[:50]}...")
                
                # Kindle Unlimitedで検索
                product_url = self.search_kindle_unlimited(title)
                df.at[index, '商品URL'] = product_url if product_url else ''
                
                # アソシエイトリンクを作成
                if product_url:
                    affiliate_url = self.create_affiliate_link(product_url)
                    df.at[index, 'アソシエイトリンク'] = affiliate_url if affiliate_url else ''
                    
                    # URLを短縮
                    if BITLY_TOKEN:
                        short_url = self.shorten_url_bitly(affiliate_url)
                    else:
                        short_url = self.shorten_url_tinyurl(affiliate_url)
                    df.at[index, '短縮URL'] = short_url if short_url else ''
                    
                    success_count += 1
                else:
                    df.at[index, 'アソシエイトリンク'] = ''
                    df.at[index, '短縮URL'] = ''
                
                # レート制限を避けるため待機
                if index < len(df) - 1:  # 最後のリクエストでは待機しない
                    time.sleep(self.request_delay)
            
            # 結果をCSVファイルに保存
            df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print("-" * 50)
            print(f"処理完了！結果を '{OUTPUT_FILE}' に保存しました。")
            
            # 統計情報を表示
            print(f"\n=== 処理結果サマリー ===")
            print(f"総件数: {len(df)}")
            print(f"商品URL取得成功: {success_count}")
            print(f"成功率: {success_count/len(df)*100:.1f}%")
            
            # 失敗したタイトルの表示
            failed_titles = df[df['商品URL'] == '']['タイトル'].tolist()
            if failed_titles:
                print(f"\n失敗したタイトル ({len(failed_titles)}件):")
                for title in failed_titles:
                    print(f"  - {title}")
            
        except Exception as e:
            print(f"CSV処理エラー: {e}")

def main():
    print("Kindle Unlimited アソシエイトリンク生成スクリプト")
    print("=" * 50)
    
    # 設定の確認
    if AFFILIATE_TAG == "your-affiliate-tag-20":
        print("警告: アソシエイトタグがデフォルト値のままです。")
        print("config.py で実際のアソシエイトタグに変更してください。")
        response = input("続行しますか？ (y/N): ")
        if response.lower() != 'y':
            print("処理を中止しました。")
            return
    
    # リンク生成器を作成
    generator = KindleUnlimitedLinkGenerator()
    
    # CSVファイルを処理
    generator.process_csv()

if __name__ == "__main__":
    main() 