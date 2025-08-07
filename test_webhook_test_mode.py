#!/usr/bin/env python3
"""
測試 Webhook（測試模式）
"""

import requests
import json
import time
import subprocess
import os

def test_webhook_test_mode():
    """在測試模式下測試 webhook"""
    print("🧪 測試 Webhook（測試模式）...")
    
    # 設置測試模式環境變數
    env = os.environ.copy()
    env["TEST_MODE"] = "true"
    
    # 啟動服務器（測試模式）
    print("🚀 啟動測試模式服務器...")
    process = subprocess.Popen(
        ["python3", "enhanced_m1_m2_m3_integrated_api_fixed.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待服務器啟動
    time.sleep(5)
    
    # 測試不同的訊息
    test_messages = [
        "我最近常常忘記事情",
        "我爸爸最近變得比較容易生氣",
        "我爺爺最近在熟悉的地方也會迷路",
        "我奶奶最近不太愛說話",
        "爸爸不會用洗衣機"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 測試 {i}: {message}")
        
        current_timestamp = int(time.time() * 1000)
        
        # 模擬 LINE Webhook 事件
        webhook_event = {
            "events": [
                {
                    "type": "message",
                    "mode": "active",
                    "timestamp": current_timestamp,
                    "source": {
                        "type": "user",
                        "userId": f"Utestuser{i}"
                    },
                    "webhookEventId": f"test-{current_timestamp}-{i}",
                    "deliveryContext": {
                        "isRedelivery": False
                    },
                    "message": {
                        "id": f"msg-{current_timestamp}-{i}",
                        "type": "text",
                        "quoteToken": "quote-token",
                        "text": message
                    },
                    "replyToken": f"reply-token-{current_timestamp}-{i}"
                }
            ],
            "destination": "Utestuser"
        }
        
        try:
            response = requests.post(
                "http://localhost:8005/test-webhook",
                json=webhook_event,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    print(f"✅ 測試 {i} 成功")
                else:
                    print(f"⚠️ 測試 {i} 部分成功: {result.get('message', '')}")
            else:
                print(f"❌ 測試 {i} 失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試 {i} 錯誤: {e}")
        
        time.sleep(1)
    
    # 停止服務器
    print("\n🛑 停止測試服務器...")
    process.terminate()
    process.wait()
    
    print("📋 測試完成")

if __name__ == "__main__":
    test_webhook_test_mode() 