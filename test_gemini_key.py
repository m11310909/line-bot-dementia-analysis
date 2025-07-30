#!/usr/bin/env python3
"""
測試 Gemini API Key
"""

import os
from dotenv import load_dotenv

def test_gemini_key():
    """測試 Gemini API Key"""
    print("🔍 測試 Gemini API Key...")
    
    # 載入環境變數
    load_dotenv()
    
    # 檢查不同的 API Key 變數名
    api_keys = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'AISTUDIO_API_KEY': os.getenv('AISTUDIO_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
    }
    
    print("\n📋 API Key 狀態:")
    for key_name, key_value in api_keys.items():
        if key_value:
            if key_value.startswith('your_actual_') or key_value.startswith('your_'):
                print(f"❌ {key_name}: 未正確設置")
            else:
                print(f"✅ {key_name}: 已設置 ({key_value[:10]}...)")
        else:
            print(f"❌ {key_name}: 未設置")
    
    # 檢查 .env 檔案
    if os.path.exists('.env'):
        print("\n📝 .env 檔案內容:")
        with open('.env', 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for line in lines:
                if 'GEMINI_API_KEY' in line or 'AISTUDIO_API_KEY' in line:
                    print(f"  {line}")
    else:
        print("\n❌ .env 檔案不存在")
    
    # 建議
    print("\n💡 建議:")
    print("1. 在 .env 檔案中設置 GEMINI_API_KEY=your_actual_key")
    print("2. 或者設置 AISTUDIO_API_KEY=your_actual_key")
    print("3. 重新啟動 API")

if __name__ == "__main__":
    test_gemini_key() 