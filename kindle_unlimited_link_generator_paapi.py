import pandas as pd
import requests
import time
import re
from urllib.parse import quote
import json
import os
from amazon_paapi import AmazonApi

# 設定ファイルの読み込み
try:
    from config import *
except ImportError:
    print("設定ファイル config.py が見つかりません。")
    print("config_example.py を config.py にコピーして、実際の値に変更してください。")
    exit(1)

class KindleUnlimitedLinkGeneratorPAAPI:
    def __init__(self):
        """
        Kindle Unlimitedリンク生成器の初期化（PA-API使用）
        設定ファイルから設定を読み込みます
        """
        self.affiliate_tag = AFFILIATE_TAG
        self.use_url_shortener = USE_URL_SHORTENER
        self.request_delay = REQUEST_DELAY
        self.search_timeout = SEARCH_TIMEOUT
        self.debug_mode = DEBUG_MODE
        self.use_paapi = USE_PAAPI
        
        # PA-APIクライアントの初期化
        if self.use_paapi:
            try:
                self.amazon = AmazonApi(
                    PAAPI_ACCESS_KEY,
                    PAAPI_SECRET_KEY,
                    PAAPI_PARTNER_TAG,
                    "JP"  # 日本の場合は"JP"
                )
                if self.debug_mode:
                    print("PA-APIクライアント初期化完了")
            except Exception as e:
                print(f"PA-API初期化エラー: {e}")
                print("スクレイピングモードに切り替えます")
                self.use_paapi = False
        
        # スクレイピング用セッション
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        if self.debug_mode:
            print(f"設定読み込み完了:")
            print(f"  アソシエイトタグ: {self.affiliate_tag}")
            print(f"  PA-API使用: {self.use_paapi}")
            print(f"  URL短縮機能: {self.use_url_shortener}")
            print(f"  リクエスト間隔: {self.request_delay}秒")
            print(f"  タイムアウト: {self.search_timeout}秒")
    
    def search_kindle_unlimited_paapi(self, title):
        """
        Amazon PA-APIを使用してKindle Unlimitedで商品を検索
        """
        try:
            if self.debug_mode:
                print(f"  PA-API検索: {title}")
            # 1回目: 通常検索
            search_result = self.amazon.search_items(
                keywords=title,
                search_index="KindleStore",
                item_count=1
            )
            if search_result and search_result.items:
                item = search_result.items[0]
                return {
                    'asin': item.asin,
                    'title': getattr(item.item_info.title, 'display_value', title) if hasattr(item, 'item_info') and hasattr(item.item_info, 'title') else title,
                    'url': f"https://www.amazon.co.jp/dp/{item.asin}",
                    'price': item.offers.listings[0].price.amount if hasattr(item, 'offers') and item.offers and hasattr(item.offers, 'listings') and item.offers.listings else None
                }
            # 2回目: タイトル短縮で再検索
            short_title = title.split('：')[0].split(':')[0].split('、')[0].split('，')[0][:20]
            if short_title != title:
                if self.debug_mode:
                    print(f"  タイトル短縮再検索: {short_title}")
                search_result = self.amazon.search_items(
                    keywords=short_title,
                    search_index="KindleStore",
                    item_count=1
                )
                if search_result and search_result.items:
                    item = search_result.items[0]
                    return {
                        'asin': item.asin,
                        'title': getattr(item.item_info.title, 'display_value', short_title) if hasattr(item, 'item_info') and hasattr(item.item_info, 'title') else short_title,
                        'url': f"https://www.amazon.co.jp/dp/{item.asin}",
                        'price': item.offers.listings[0].price.amount if hasattr(item, 'offers') and item.offers and hasattr(item.offers, 'listings') and item.offers.listings else None
                    }
            # 3回目: search_indexをAllにして再検索
            if self.debug_mode:
                print(f"  search_index=Allで再検索: {title}")
            search_result = self.amazon.search_items(
                keywords=title,
                search_index="All",
                item_count=1
            )
            if search_result and search_result.items:
                item = search_result.items[0]
                return {
                    'asin': item.asin,
                    'title': getattr(item.item_info.title, 'display_value', title) if hasattr(item, 'item_info') and hasattr(item.item_info, 'title') else title,
                    'url': f"https://www.amazon.co.jp/dp/{item.asin}",
                    'price': item.offers.listings[0].price.amount if hasattr(item, 'offers') and item.offers and hasattr(item.offers, 'listings') and item.offers.listings else None
                }
            return None
        except Exception as e:
            print(f"PA-API検索エラー ({title}): {e}")
            return None
    
    def search_kindle_unlimited_scraping(self, title):
        """
        スクレイピングでKindle Unlimitedを検索（フォールバック用）
        
        Args:
            title (str): 検索するタイトル
            
        Returns:
            dict: 商品情報（見つからない場合はNone）
        """
        try:
            if self.debug_mode:
                print(f"  スクレイピング検索: {title}")
            
            # Kindle Unlimitedの検索URL
            search_url = "https://www.amazon.co.jp/s"
            params = {
                'k': title,
                'i': 'digital-text',  # Kindleストア
                'ref': 'sr_nr_i_0'
            }
            
            response = self.session.get(search_url, params=params, timeout=self.search_timeout)
            response.raise_for_status()
            
            # 最初の商品リンクを探す
            product_pattern = r'href="(/dp/([A-Z0-9]{10}))'
            matches = re.findall(product_pattern, response.text)
            
            if matches:
                product_path, asin = matches[0]
                product_url = f"https://www.amazon.co.jp{product_path}"
                
                if self.debug_mode:
                    print(f"  商品URL発見: {product_url}")
                    print(f"  ASIN: {asin}")
                
                return {
                    'asin': asin,
                    'title': title,
                    'url': product_url,
                    'price': None
                }
            
            return None
            
        except Exception as e:
            print(f"スクレイピング検索エラー ({title}): {e}")
            return None
    
    def search_kindle_unlimited(self, title):
        """
        Kindle Unlimitedで商品を検索（PA-API優先、フォールバックでスクレイピング）
        
        Args:
            title (str): 検索するタイトル
            
        Returns:
            dict: 商品情報（見つからない場合はNone）
        """
        if self.use_paapi:
            result = self.search_kindle_unlimited_paapi(title)
            if result:
                return result
        
        # PA-APIが失敗した場合や無効な場合はスクレイピングを使用
        return self.search_kindle_unlimited_scraping(title)
    
    def create_affiliate_link(self, product_info):
        """
        Amazonアソシエイトリンクを作成
        
        Args:
            product_info (dict): 商品情報
            
        Returns:
            str: アソシエイトリンク
        """
        if not product_info or not product_info.get('url'):
            return None
        
        product_url = product_info['url']
        
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
            
            print(f"合計 {len(df)} 件のタイトルを処理します...")
            print(f"PA-API使用: {'有効' if self.use_paapi else '無効'}")
            print(f"URL短縮機能: {'有効' if self.use_url_shortener else '無効'}")
            print(f"リクエスト間隔: {self.request_delay}秒")
            print("-" * 50)
            
            success_count = 0
            successful_data = []  # 成功したデータのみを格納
            
            for index, row in df.iterrows():
                title = row['タイトル']
                introduction = row['一言紹介文']
                print(f"処理中 ({index + 1}/{len(df)}): {title[:50]}...")
                
                # Kindle Unlimitedで検索
                product_info = self.search_kindle_unlimited(title)
                
                if product_info:
                    # アソシエイトリンクを作成
                    affiliate_url = self.create_affiliate_link(product_info)
                    
                    if affiliate_url:
                        # URLを短縮
                        if BITLY_TOKEN:
                            short_url = self.shorten_url_bitly(affiliate_url)
                        else:
                            short_url = self.shorten_url_tinyurl(affiliate_url)
                        
                        # 成功したデータのみをリストに追加
                        successful_data.append({
                            'No': len(successful_data) + 1,
                            'タイトル': title,
                            '一言紹介文': introduction,
                            '短縮URL': short_url
                        })
                        
                        success_count += 1
                
                # レート制限を避けるため待機
                if index < len(df) - 1:  # 最後のリクエストでは待機しない
                    time.sleep(self.request_delay)
            
            # 成功したデータのみでDataFrameを作成
            result_df = pd.DataFrame(successful_data)
            
            # 結果をCSVファイルに保存
            result_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
            print("-" * 50)
            print(f"処理完了！結果を '{OUTPUT_FILE}' に保存しました。")
            
            # 統計情報を表示
            print(f"\n=== 処理結果サマリー ===")
            print(f"総件数: {len(df)}")
            print(f"商品URL取得成功: {success_count}")
            print(f"成功率: {success_count/len(df)*100:.1f}%")
            print(f"出力件数: {len(successful_data)}")
            
            # 失敗したタイトルの表示
            failed_count = len(df) - success_count
            if failed_count > 0:
                print(f"\n失敗したタイトル数: {failed_count}件")
            
        except Exception as e:
            print(f"CSV処理エラー: {e}")

def main():
    print("Kindle Unlimited アソシエイトリンク生成スクリプト（PA-API対応）")
    print("=" * 60)
    
    # 設定の確認
    if AFFILIATE_TAG == "your-affiliate-tag-20":
        print("警告: アソシエイトタグがデフォルト値のままです。")
        print("config.py で実際のアソシエイトタグに変更してください。")
        response = input("続行しますか？ (y/N): ")
        if response.lower() != 'y':
            print("処理を中止しました。")
            return
    
    if USE_PAAPI and (PAAPI_ACCESS_KEY == "your-access-key" or PAAPI_SECRET_KEY == "your-secret-key"):
        print("警告: PA-API認証情報がデフォルト値のままです。")
        print("config.py で実際のPA-API認証情報に変更してください。")
        print("PA-APIを使用しない場合は、USE_PAAPI = False に設定してください。")
        response = input("スクレイピングモードで続行しますか？ (y/N): ")
        if response.lower() != 'y':
            print("処理を中止しました。")
            return
    
    # リンク生成器を作成
    generator = KindleUnlimitedLinkGeneratorPAAPI()
    
    # CSVファイルを処理
    generator.process_csv()

if __name__ == "__main__":
    main() 