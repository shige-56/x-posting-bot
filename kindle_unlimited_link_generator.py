import pandas as pd
import requests
import time
import re
from urllib.parse import quote
import json

class KindleUnlimitedLinkGenerator:
    def __init__(self, affiliate_tag):
        """
        Kindle Unlimitedリンク生成器の初期化
        
        Args:
            affiliate_tag (str): Amazonアソシエイトタグ
        """
        self.affiliate_tag = affiliate_tag
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
    
    def shorten_url(self, url):
        """
        URLを短縮する（簡易版）
        実際の短縮サービスを使用する場合は、適切なAPIキーが必要です
        
        Args:
            url (str): 短縮するURL
            
        Returns:
            str: 短縮URL（この実装では元のURLを返す）
        """
        # 注意: 実際の短縮サービスを使用する場合は、
        # TinyURL、Bitly、Google URL ShortenerなどのAPIを使用してください
        # ここでは簡易的に元のURLを返します
        return url
    
    def process_csv(self, input_file, output_file):
        """
        CSVファイルを処理してアソシエイトリンクを追加
        
        Args:
            input_file (str): 入力CSVファイル
            output_file (str): 出力CSVファイル
        """
        try:
            # CSVファイルを読み込み
            df = pd.read_csv(input_file)
            
            # 新しい列を追加
            df['商品URL'] = ''
            df['アソシエイトリンク'] = ''
            df['短縮URL'] = ''
            
            print(f"合計 {len(df)} 件のタイトルを処理します...")
            
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
                    short_url = self.shorten_url(affiliate_url)
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
            
        except Exception as e:
            print(f"CSV処理エラー: {e}")

def main():
    # Amazonアソシエイトタグを設定
    # 注意: 実際のアソシエイトタグに置き換えてください
    affiliate_tag = "your-affiliate-tag-20"  # 例: "yourname-20"
    
    # リンク生成器を作成
    generator = KindleUnlimitedLinkGenerator(affiliate_tag)
    
    # ファイル名を設定
    input_file = "kindle_unlimited_biz_10_clean.csv"
    output_file = "kindle_unlimited_biz_10_with_links.csv"
    
    # CSVファイルを処理
    generator.process_csv(input_file, output_file)

if __name__ == "__main__":
    main() 