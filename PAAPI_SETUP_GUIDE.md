# Amazon Product Advertising API (PA-API) セットアップガイド

このガイドでは、Amazon Product Advertising API (PA-API) の設定方法を詳しく説明します。

## PA-APIとは

Amazon Product Advertising APIは、Amazonの商品情報にアクセスするための公式APIです。スクレイピングと比べて以下の利点があります：

- **正確性**: 公式APIによる正確な商品情報
- **効率性**: 高速な検索処理
- **信頼性**: レート制限が明確
- **豊富な情報**: 価格、画像、レビュー数など
- **安定性**: サイト構造変更の影響を受けない

## セットアップ手順

### 1. Amazon Associates Central への登録

1. [Amazon Associates Central](https://affiliate-program.amazon.co.jp/) にアクセス
2. Amazonアカウントでログイン
3. アソシエイトプログラムに登録（まだの場合）

### 2. PA-APIの申請

1. Amazon Associates Centralにログイン
2. 左側のメニューから「ツール」を選択
3. 「Product Advertising API」をクリック
4. 「API キーを取得」ボタンをクリック
5. 利用規約に同意

### 3. 認証情報の取得

申請が承認されると、以下の情報が表示されます：

- **Access Key ID**: APIアクセス用の公開キー
- **Secret Access Key**: APIアクセス用の秘密キー
- **パートナータグ**: アソシエイトタグ（通常は同じ）

### 4. 設定ファイルの更新

`config_example.py` を `config.py` にコピーし、以下の設定を更新：

```python
# Amazon Product Advertising API設定
USE_PAAPI = True

# PA-API認証情報
PAAPI_ACCESS_KEY = "your-access-key"  # 実際のAccess Key ID
PAAPI_SECRET_KEY = "your-secret-key"  # 実際のSecret Access Key
PAAPI_PARTNER_TAG = "your-affiliate-tag-20"  # 実際のアソシエイトタグ
PAAPI_HOST = "webservices.amazon.co.jp"  # 日本の場合は固定
PAAPI_REGION = "us-west-2"  # リージョン（日本の場合は固定）
```

## 利用制限

### リクエスト制限

- **1日あたり**: 8,640リクエスト（1秒あたり1リクエスト）
- **1時間あたり**: 360リクエスト
- **1秒あたり**: 1リクエスト

### 利用規約

- 商用利用の場合は利用規約を確認
- アソシエイトプログラムの利用規約に従う
- 適切なアトリビューション（帰属表示）を行う

## トラブルシューティング

### よくある問題

#### 1. 認証エラー

**症状**: `InvalidClientTokenId` エラー

**解決方法**:
- Access Key IDが正しく設定されているか確認
- Secret Access Keyが正しく設定されているか確認
- パートナータグが正しく設定されているか確認

#### 2. リクエスト制限エラー

**症状**: `RequestThrottled` エラー

**解決方法**:
- リクエスト間隔を長くする（`REQUEST_DELAY` を増加）
- 1日のリクエスト数を確認

#### 3. 地域エラー

**症状**: `InvalidParameterValue` エラー

**解決方法**:
- `PAAPI_HOST` が `webservices.amazon.co.jp` に設定されているか確認
- `PAAPI_REGION` が `us-west-2` に設定されているか確認

### デバッグモードの有効化

問題の特定のために、デバッグモードを有効にできます：

```python
DEBUG_MODE = True
```

これにより、詳細なログが表示されます。

## セキュリティ

### 認証情報の保護

- Secret Access Keyは絶対に公開しないでください
- 設定ファイルはGitなどのバージョン管理システムにコミットしないでください
- 本番環境では環境変数を使用することを推奨

### 環境変数の使用（推奨）

セキュリティを向上させるため、環境変数を使用できます：

```python
import os

PAAPI_ACCESS_KEY = os.getenv('PAAPI_ACCESS_KEY')
PAAPI_SECRET_KEY = os.getenv('PAAPI_SECRET_KEY')
```

## パフォーマンス最適化

### リクエスト最適化

1. **バッチ処理**: 複数の商品を一度に検索
2. **キャッシュ**: 同じ商品の重複検索を避ける
3. **エラーハンドリング**: 失敗したリクエストの再試行

### 設定の調整

```python
# リクエスト間隔の調整
REQUEST_DELAY = 1.5  # 1.5秒間隔

# タイムアウトの調整
SEARCH_TIMEOUT = 15  # 15秒タイムアウト
```

## サポート

### 公式ドキュメント

- [Amazon Product Advertising API 5.0](https://webservices.amazon.com/paapi5/documentation/)
- [Amazon Associates Central](https://affiliate-program.amazon.co.jp/)

### コミュニティ

- Amazon Associates フォーラム
- Stack Overflow
- GitHub Issues

## 注意事項

- PA-APIの利用には申請と承認が必要です
- 商用利用の場合は利用規約を確認してください
- アソシエイトプログラムの利用規約に従ってください
- 適切なアトリビューション（帰属表示）を行ってください 