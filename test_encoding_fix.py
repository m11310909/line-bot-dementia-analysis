#!/usr/bin/env python3
"""
測試編碼修復
"""

import requests
import json
import sys

def test_encoding():
    """測試編碼修復"""
    
    print("🔧 測試編碼修復")
    print("=" * 50)
    
    # 測試案例
    test_cases = [
        {
            "message": "媽媽最近常重複問同樣的問題",
            "description": "測試重複行為警訊"
        },
        {
            "message": "爸爸忘記關瓦斯爐",
            "description": "測試安全警訊"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試案例 {i}: {test_case['description']}")
        print(f"輸入: {test_case['message']}")
        
        try:
            # 調用 API
            response = requests.post(
                "http://localhost:8008/analyze/m1",
                json={
                    "message": test_case["message"],
                    "user_id": "test_user"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 檢查 JSON 編碼
                try:
                    json_str = json.dumps(result, ensure_ascii=False, indent=2)
                    print("✅ JSON 編碼正常")
                    
                    # 檢查關鍵中文字段
                    contents = result.get('contents', {})
                    if contents.get('type') == 'bubble':
                        body = contents.get('body', {})
                        body_contents = body.get('contents', [])
                        
                        # 檢查分析文字
                        for content in body_contents:
                            if content.get('type') == 'text':
                                text = content.get('text', '')
                                if '分析' in text or '警訊' in text:
                                    print(f"✅ 中文顯示正常: {text[:20]}...")
                                
                except UnicodeEncodeError as e:
                    print(f"❌ 編碼錯誤: {e}")
                    
                # 檢查回應大小
                response_size = len(json.dumps(result, ensure_ascii=False))
                print(f"📏 回應大小: {response_size} 字符")
                
                if response_size > 3000:
                    print("⚠️ 回應過大，可能導致截斷")
                
            else:
                print(f"❌ API 回應失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 編碼測試完成")

def check_system_encoding():
    """檢查系統編碼"""
    print("\n🔍 系統編碼檢查")
    print(f"Python 版本: {sys.version}")
    print(f"預設編碼: {sys.getdefaultencoding()}")
    print(f"檔案系統編碼: {sys.getfilesystemencoding()}")

if __name__ == "__main__":
    check_system_encoding()
    test_encoding() 