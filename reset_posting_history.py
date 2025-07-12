#!/usr/bin/env python3
"""
投稿履歴リセットスクリプト
テスト用の投稿履歴をクリアして本番環境をクリーンにする
"""

import json
import os

def reset_posting_history():
    """投稿履歴をリセット"""
    history_file = "posting_history.json"
    
    # 現在の投稿履歴を確認
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            current_history = json.load(f)
        print(f"現在の投稿履歴: {len(current_history)}件")
        print(f"投稿済みアイテム: {list(current_history.keys())}")
    else:
        print("投稿履歴ファイルが存在しません")
        current_history = {}
    
    # 確認
    response = input("投稿履歴をリセットしますか？ (y/N): ")
    if response.lower() != 'y':
        print("リセットをキャンセルしました")
        return
    
    # 投稿履歴をクリア
    empty_history = {}
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(empty_history, f, ensure_ascii=False, indent=2)
    
    print("✅ 投稿履歴をリセットしました")
    print(f"削除された投稿数: {len(current_history)}件")

if __name__ == "__main__":
    print("="*60)
    print("🔄 投稿履歴リセットツール")
    print("="*60)
    reset_posting_history() 