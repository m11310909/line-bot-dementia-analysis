#!/usr/bin/env python3
"""
測試 Flex Message 發送
"""

import requests
import json

def test_flex_message():
    """測試 Flex Message 發送"""
    
    # 測試 Flex Message
    flex_message = {
        "type": "flex",
        "altText": "測試 Flex Message",
        "contents": {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎯 測試標題",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    }
                ],
                "backgroundColor": "#FF6B6B",
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "這是一個測試 Flex Message，用於驗證富文本顯示是否正常。",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    print("🎨 測試 Flex Message 結構:")
    print(json.dumps(flex_message, ensure_ascii=False, indent=2))
    
    # 測試 API
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"message": "測試訊息"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API 測試成功")
            result = response.json()
            print(f"   回應: {result}")
        else:
            print(f"❌ API 測試失敗: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ API 測試失敗: {e}")

if __name__ == "__main__":
    test_flex_message()
