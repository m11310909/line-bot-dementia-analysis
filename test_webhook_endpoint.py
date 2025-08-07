#!/usr/bin/env python3
"""
測試 Webhook 端點
"""

import requests
import json
import hmac
import hashlib
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_webhook_endpoint():
    """測試 Webhook 端點"""
    print("🔍 測試 Webhook 端點...")
    
    # 獲取 LINE Bot 憑證
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")
    if not channel_secret:
        print("❌ LINE_CHANNEL_SECRET 未設置")
        return
    
    # 模擬 LINE Webhook 事件
    webhook_event = {
        "events": [
            {
                "type": "message",
                "mode": "active",
                "timestamp": 1234567890,
                "source": {
                    "type": "user",
                    "userId": "U1234567890abcdef"
                },
                "webhookEventId": "01234567-89ab-cdef-0123-456789abcdef",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "message": {
                    "id": "14353798921116",
                    "type": "text",
                    "quoteToken": "quote-token",
                    "text": "測試訊息"
                },
                "replyToken": "reply-token"
            }
        ],
        "destination": "U1234567890abcdef"
    }
    
    # 轉換為 JSON 字符串
    body = json.dumps(webhook_event)
    
    # 生成簽名
    signature = hmac.new(
        channel_secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # 設置請求頭
    headers = {
        "Content-Type": "application/json",
        "X-Line-Signature": signature
    }
    
    # 發送請求到本地 webhook 端點
    try:
        response = requests.post(
            "http://localhost:8005/webhook",
            data=body,
            headers=headers,
            timeout=10
        )
        
        print(f"📋 測試結果:")
        print(f"   狀態碼: {response.status_code}")
        print(f"   回應: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook 端點測試成功")
        else:
            print("❌ Webhook 端點測試失敗")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到 webhook 端點")
        print("請確保 API 服務正在運行 (python3 enhanced_m1_m2_m3_integrated_api_fixed.py)")
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
    
    print("\n📝 測試完成")

if __name__ == "__main__":
    test_webhook_endpoint() 