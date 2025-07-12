#!/usr/bin/env python3
"""
投稿制限テストスクリプト
9回投稿後に10回目以降の投稿が制限されることを確認
"""

import os
import json
from datetime import datetime

def create_test_history():
    """テスト用の投稿履歴を作成（9回分）"""
    today = datetime.now().strftime('%Y-%m-%d')
    history = {}
    
    # 9回分の投稿履歴を作成
    for i in range(1, 10):
        history[str(i)] = today
    
    # 投稿履歴ファイルに保存
    with open('posting_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    print(f"テスト用投稿履歴を作成しました: {len(history)}件")
    return history

def test_posting_limit():
    """投稿制限のテスト"""
    print("="*60)
    print("📊 投稿制限テスト開始")
    print("="*60)
    
    # テスト用の投稿履歴を作成（9回分）
    history = create_test_history()
    
    print(f"現在の投稿履歴: {len(history)}件")
    print(f"投稿済みアイテム: {list(history.keys())}")
    
    # テストモードでBOTを実行
    print("\n" + "="*60)
    print("🤖 BOT実行テスト")
    print("="*60)
    
    # 環境変数を設定してBOTを実行
    os.environ['TEST_MODE'] = 'true'
    
    # BOTをインポートして実行
    from x_posting_bot_advanced import main
    main()

if __name__ == "__main__":
    test_posting_limit() 