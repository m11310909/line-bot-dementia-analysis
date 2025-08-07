#!/usr/bin/env python3
"""
簡單的 Webhook 測試
"""

import requests
import json

def test_simple_webhook():
    """簡單的 webhook 測試"""
    print("🔍 簡單 Webhook 測試...")
    
    # 簡單的測試數據
    test_data = {
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "text": "測試"
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://localhost:8005/webhook",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"📋 測試結果:")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_simple_webhook() 