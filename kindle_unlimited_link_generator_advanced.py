import pandas as pd
import requests
import time
import re
from urllib.parse import quote
import json

class KindleUnlimitedLinkGenerator:
    def __init__(self, affiliate_tag, use_url_shortener=True):
        """
        Kindle Unlimitedリンク生成器の初期化
        
        Args:
            affiliate_tag (str): Amazonアソシエイトタグ
            use_url_shortener (bool): URL短縮機能を使用するかどうか
        """
        self.affiliate_tag = affiliate_tag
        self.use_url_shortener = use_url_shortener
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
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
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            # 最初の商品リンクを探す
            # 商品リンクのパターンを検索
            product_pattern = r'href="(/dp/[A-Z0-9]{10})'
            matches = re.findall(product_pattern, response.text)
            
            if matches:
                product_id = matches[0]
                return f"https://www.amazon.co.jp{product_id}"
            
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
            
            response = self.session.get(tinyurl_api, params=params, timeout=10)
            response.raise_for_status()
            
            return response.text
            
        except Exception as e:
            print(f"URL短縮エラー: {e}")
            return url
    
    def shorten_url_bitly(self, url, bitly_token):
        """
        Bitly APIを使用してURLを短縮（APIキーが必要）
        
        Args:
            url (str): 短縮するURL
            bitly_token (str): Bitly APIトークン
            
        Returns:
            str: 短縮URL（エラーの場合は元のURL）
        """
        if not self.use_url_shortener or not bitly_token:
            return url
            
        try:
            bitly_api = "https://api-ssl.bitly.com/v4/shorten"
            headers = {
                'Authorization': f'Bearer {bitly_token}',
                'Content-Type': 'application/json'
            }
            data = {'long_url': url}
            
            response = self.session.post(bitly_api, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            return result.get('link', url)
            
        except Exception as e:
            print(f"Bitly短縮エラー: {e}")
            return url
    
    def process_csv(self, input_file, output_file, bitly_token=None):
        """
        CSVファイルを処理してアソシエイトリンクを追加
        
        Args:
            input_file (str): 入力CSVファイル
            output_file (str): 出力CSVファイル
            bitly_token (str): Bitly APIトークン（オプション）
        """
        try:
            # CSVファイルを読み込み
            df = pd.read_csv(input_file)
            
            # 新しい列を追加
            df['商品URL'] = ''
            df['アソシエイトリンク'] = ''
            df['短縮URL'] = ''
            
            print(f"合計 {len(df)} 件のタイトルを処理します...")
            print(f"URL短縮機能: {'有効' if self.use_url_shortener else '無効'}")
            
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
                    if bitly_token:
                        short_url = self.shorten_url_bitly(affiliate_url, bitly_token)
                    else:
                        short_url = self.shorten_url_tinyurl(affiliate_url)
                    df.at[index, '短縮URL'] = short_url if short_url else ''
                else:
                    df.at[index, 'アソシエイトリンク'] = ''
                    df.at[index, '短縮URL'] = ''
                
                # レート制限を避けるため少し待機
                time.sleep(1)
            
            # 結果をCSVファイルに保存
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"処理完了！結果を {output_file} に保存しました。")
            
            # 統計情報を表示
            success_count = df['商品URL'].notna().sum()
            print(f"成功: {success_count}/{len(df)} 件")
            
            # 結果のサマリーを表示
            print("\n=== 処理結果サマリー ===")
            print(f"総件数: {len(df)}")
            print(f"商品URL取得成功: {success_count}")
            print(f"成功率: {success_count/len(df)*100:.1f}%")
            
        except Exception as e:
            print(f"CSV処理エラー: {e}")

def main():
    # Amazonアソシエイトタグを設定
    # 注意: 実際のアソシエイトタグに置き換えてください
    affiliate_tag = "your-affiliate-tag-20"  # 例: "yourname-20"
    
    # Bitly APIトークン（オプション）
    # 注意: Bitlyを使用する場合は、有効なAPIトークンを設定してください
    bitly_token = None  # "your-bitly-token"
    
    # リンク生成器を作成
    generator = KindleUnlimitedLinkGenerator(
        affiliate_tag=affiliate_tag,
        use_url_shortener=True  # URL短縮機能を有効にする
    )
    
    # ファイル名を設定
    input_file = "kindle_unlimited_biz_10_clean.csv"
    output_file = "kindle_unlimited_biz_10_with_links_advanced.csv"
    
    # CSVファイルを処理
    generator.process_csv(input_file, output_file, bitly_token)

if __name__ == "__main__":
    main() 