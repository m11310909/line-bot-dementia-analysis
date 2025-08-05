#!/usr/bin/env python3
"""
測試簡化版 Flex Message
"""

import requests
import json

def test_simplified_flex():
    """測試簡化版 Flex Message"""
    
    print("🧪 測試簡化版 Flex Message")
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
                print(f"✅ API 回應成功")
                
                # 檢查回應大小
                response_size = len(json.dumps(result, ensure_ascii=False))
                print(f"📏 回應大小: {response_size} 字符")
                
                if response_size < 1500:
                    print("✅ 回應大小適中，避免截斷")
                else:
                    print("⚠️ 回應仍然較大")
                
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
                        if len(footer_contents) >= 2:
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
    print("🎯 簡化版測試完成")

if __name__ == "__main__":
    test_simplified_flex() 