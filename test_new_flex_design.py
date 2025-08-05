#!/usr/bin/env python3
"""
測試新的 Flex Message 設計
"""

import requests
import json
from datetime import datetime

def test_new_flex_design():
    """測試新的 Flex Message 設計"""
    
    # 測試案例
    test_cases = [
        {
            "message": "媽媽最近常重複問同樣的問題",
            "description": "測試重複行為警訊"
        },
        {
            "message": "爸爸忘記關瓦斯爐",
            "description": "測試安全警訊"
        },
        {
            "message": "爺爺有妄想症狀",
            "description": "測試 BPSD 症狀"
        }
    ]
    
    print("🧪 測試新的 Flex Message 設計")
    print("=" * 50)
    
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
                print(f"✅ API 回應成功")
                print(f"📊 回應類型: {result.get('type', 'N/A')}")
                print(f"📏 回應大小: {len(json.dumps(result))} 字符")
                
                # 檢查 Flex Message 結構
                if result.get('type') == 'flex':
                    contents = result.get('contents', {})
                    if contents.get('type') == 'bubble':
                        print("✅ Flex Message 結構正確")
                        
                        # 檢查標題
                        header = contents.get('header', {})
                        if header.get('backgroundColor') == '#27AE60':
                            print("✅ 綠色標題設計正確")
                        
                        # 檢查底部按鈕
                        footer = contents.get('footer', {})
                        footer_contents = footer.get('contents', [])
                        if len(footer_contents) >= 3:
                            print("✅ 底部按鈕設計正確")
                            for button in footer_contents:
                                if button.get('type') == 'button':
                                    label = button.get('action', {}).get('label', '')
                                    print(f"   - {label}")
                
            else:
                print(f"❌ API 回應失敗: {response.status_code}")
                print(f"錯誤: {response.text}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 測試完成")

if __name__ == "__main__":
    test_new_flex_design() 