#!/usr/bin/env python3
"""
測試文字訊息格式
"""

import requests
import json

def test_text_message_format():
    """測試文字訊息格式"""
    print("🧪 測試文字訊息格式")
    print("=" * 50)
    
    test_cases = [
        {
            "input": "爸爸不會用洗衣機",
            "description": "M1 警訊檢測 - 功能喪失"
        },
        {
            "input": "媽媽中度失智，需要協助",
            "description": "M2 病程評估 - 階段判斷"
        },
        {
            "input": "爺爺最近情緒不穩定，常常發脾氣",
            "description": "M3 BPSD 症狀 - 情緒問題"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['description']}")
        print(f"輸入: {test_case['input']}")
        
        try:
            response = requests.post(
                "http://localhost:8005/comprehensive-analysis",
                json={"user_input": test_case['input']},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # 模擬文字訊息格式
                summary = result.get('comprehensive_summary', '分析完成')
                modules_used = result.get('modules_used', [])
                chunks_found = len(result.get('retrieved_chunks', []))
                
                text_response = f"🧠 失智症分析結果\n\n"
                text_response += f"📊 分析摘要: {summary}\n\n"
                
                if modules_used:
                    text_response += f"🔍 使用模組: {', '.join(modules_used)}\n"
                text_response += f"📋 找到相關片段: {chunks_found} 個\n\n"
                
                text_response += "💬 請提供更多詳細資訊以獲得更好的建議。"
                
                print("✅ 文字訊息格式:")
                print("-" * 40)
                print(text_response)
                print("-" * 40)
                print(f"📏 訊息長度: {len(text_response)} 字符")
                
            else:
                print(f"❌ API 錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")

def test_webhook_text_message():
    """測試 Webhook 文字訊息"""
    print("\n🌐 測試 Webhook 文字訊息")
    print("=" * 50)
    
    # 模擬 LINE webhook 請求
    webhook_data = {
        "destination": "test_destination",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "test_message_id",
                    "text": "爸爸不會用洗衣機"
                },
                "replyToken": "test_reply_token",
                "source": {
                    "type": "user",
                    "userId": "test_user_id"
                }
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://0ac6705ad6a2.ngrok-free.app/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Webhook 回應狀態: {response.status_code}")
        print(f"📝 回應內容: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Webhook 文字訊息處理成功")
        else:
            print("⚠️  Webhook 處理可能有問題")
            
    except Exception as e:
        print(f"❌ Webhook 測試失敗: {e}")

def main():
    """主測試函數"""
    print("🚀 文字訊息格式測試")
    print("=" * 60)
    
    # 測試文字訊息格式
    test_text_message_format()
    
    # 測試 Webhook 文字訊息
    test_webhook_text_message()
    
    print("\n" + "=" * 60)
    print("🎉 文字訊息測試完成!")
    print("📱 系統現在使用純文字訊息回應")
    print("🌐 Webhook URL: https://0ac6705ad6a2.ngrok-free.app/webhook")

if __name__ == "__main__":
    main() 