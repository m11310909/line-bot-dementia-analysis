#!/usr/bin/env python3
"""
測試 webhook 修復
"""

import requests
import json
import hmac
import hashlib
import base64

def test_webhook():
    """測試 webhook 端點"""
    print("🧪 測試 Webhook 修復")
    print("="*50)
    
    # 測試 1: 健康檢查
    print("1. 測試健康檢查...")
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            print("✅ 健康檢查通過")
        else:
            print(f"❌ 健康檢查失敗: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ 健康檢查錯誤: {e}")
        return
    
    # 測試 2: 直接測試 webhook 端點
    print("\n2. 測試 webhook 端點...")
    try:
        response = requests.post(
            "http://localhost:8005/webhook",
            json={"test": "webhook"},
            timeout=5
        )
        print(f"📊 回應狀態: {response.status_code}")
        print(f"📝 回應內容: {response.text}")
    except Exception as e:
        print(f"❌ Webhook 測試錯誤: {e}")
    
    # 測試 3: 測試 ngrok webhook
    print("\n3. 測試 ngrok webhook...")
    try:
        response = requests.post(
            "https://e11767e116f9.ngrok-free.app/webhook",
            json={"test": "webhook"},
            timeout=10
        )
        print(f"📊 回應狀態: {response.status_code}")
        print(f"📝 回應內容: {response.text}")
    except Exception as e:
        print(f"❌ Ngrok webhook 測試錯誤: {e}")
    
    # 測試 4: 測試 LINE Bot 模擬請求
    print("\n4. 測試 LINE Bot 模擬請求...")
    try:
        # 模擬 LINE Bot 事件
        line_event = {
            "events": [
                {
                    "type": "message",
                    "message": {
                        "type": "text",
                        "id": "test_message_id",
                        "text": "爸爸忘記關瓦斯爐"
                    },
                    "replyToken": "test_reply_token",
                    "source": {
                        "userId": "test_user_id",
                        "type": "user"
                    }
                }
            ]
        }
        
        # 生成簽名
        channel_secret = "091dfc73fed73a681e4e7ea5d9eb461b"  # 從 .env 獲取
        body = json.dumps(line_event)
        signature = base64.b64encode(
            hmac.new(
                channel_secret.encode('utf-8'),
                body.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        headers = {
            "Content-Type": "application/json",
            "X-Line-Signature": signature
        }
        
        response = requests.post(
            "http://localhost:8005/webhook",
            data=body,
            headers=headers,
            timeout=10
        )
        print(f"📊 回應狀態: {response.status_code}")
        print(f"📝 回應內容: {response.text}")
        
    except Exception as e:
        print(f"❌ LINE Bot 模擬測試錯誤: {e}")
    
    print("\n🎉 測試完成!")

if __name__ == "__main__":
    test_webhook() 