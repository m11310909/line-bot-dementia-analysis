#!/usr/bin/env python3
"""
Flex Messages 演示腳本
展示增強版 LINE Bot 的視覺化功能
"""

import requests
import json
import time
from datetime import datetime

def demo_flex_messages():
    """演示 Flex Messages 功能"""
    
    base_url = "http://localhost:8005"
    
    # 測試案例
    test_messages = [
        {
            "name": "記憶力問題",
            "message": "我最近常常忘記事情",
            "expected_module": "M1"
        },
        {
            "name": "情緒變化",
            "message": "我爸爸最近變得比較容易生氣",
            "expected_module": "comprehensive"
        },
        {
            "name": "空間認知",
            "message": "我爺爺最近在熟悉的地方也會迷路",
            "expected_module": "comprehensive"
        },
        {
            "name": "社交退縮",
            "message": "我奶奶最近不太愛說話",
            "expected_module": "comprehensive"
        },
        {
            "name": "日常生活",
            "message": "爸爸不會用洗衣機",
            "expected_module": "comprehensive"
        }
    ]
    
    print("🎨 Flex Messages 演示")
    print("=" * 50)
    print(f"🌐 服務地址: {base_url}")
    print(f"⏰ 開始時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 檢查服務狀態
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ 服務狀態: {health_data.get('status', 'unknown')}")
            print(f"📱 LINE Bot 配置: {'✅ 已配置' if health_data.get('line_bot_configured') else '❌ 未配置'}")
            print(f"🧪 測試模式: {'✅ 啟用' if health_data.get('test_mode') else '❌ 停用'}")
        else:
            print(f"❌ 服務狀態檢查失敗: {health_response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ 無法連接到服務: {e}")
        return
    
    print()
    
    # 執行測試案例
    for i, test_case in enumerate(test_messages, 1):
        print(f"📋 測試案例 {i}: {test_case['name']}")
        print(f"💬 訊息: {test_case['message']}")
        print(f"🎯 預期模組: {test_case['expected_module']}")
        print("-" * 40)
        
        # 構建測試請求
        test_payload = {
            "events": [{
                "type": "message",
                "mode": "active",
                "timestamp": int(time.time() * 1000),
                "source": {
                    "type": "user",
                    "userId": f"Utestuser{i}"
                },
                "webhookEventId": f"test-{int(time.time() * 1000)}-{i}",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "replyToken": f"reply-token-{int(time.time() * 1000)}",
                "message": {
                    "id": f"test-message-{i}",
                    "type": "text",
                    "text": test_case['message'],
                    "quoteToken": f"quote-token-{i}"
                }
            }]
        }
        
        try:
            # 發送測試請求
            response = requests.post(
                f"{base_url}/test-webhook",
                json=test_payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 請求成功")
                print(f"   處理事件數: {result.get('processed_events', 0)}")
                print(f"   狀態: {result.get('status', 'unknown')}")
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                print(f"   錯誤: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 請求錯誤: {e}")
        
        print()
        time.sleep(1)  # 避免請求過於頻繁
    
    print("🎉 演示完成！")
    print("=" * 50)
    print("📝 說明:")
    print("• 每個測試案例都會生成對應的 Flex Message")
    print("• Flex Message 包含彩色標題、症狀列表和建議")
    print("• 不同模組使用不同的顏色主題")
    print("• 測試模式下不會實際發送 LINE 訊息")
    print()
    print("🔗 相關文件:")
    print("• FLEX_MESSAGES_IMPLEMENTATION_GUIDE.md - 詳細實現指南")
    print("• test_flex_messages.py - Flex Message 測試工具")
    print("• enhanced_m1_m2_m3_integrated_api_fixed.py - 主服務文件")

def show_flex_message_examples():
    """顯示 Flex Message 範例"""
    
    print("\n🎨 Flex Message 範例")
    print("=" * 30)
    
    examples = [
        {
            "module": "M1",
            "color": "#FF6B6B",
            "title": "🔍 M1 分析結果",
            "symptoms": ["記憶力減退", "語言障礙", "定向力下降"],
            "recommendations": ["建議就醫檢查", "注意安全", "建立提醒系統"]
        },
        {
            "module": "M2", 
            "color": "#4ECDC4",
            "title": "🔍 M2 分析結果",
            "symptoms": ["認知功能下降", "行為改變", "情緒波動"],
            "recommendations": ["認知訓練", "環境安全", "情緒支持"]
        },
        {
            "module": "M3",
            "color": "#45B7D1", 
            "title": "🔍 M3 分析結果",
            "symptoms": ["妄想", "幻覺", "攻擊行為"],
            "recommendations": ["藥物治療", "行為療法", "環境調整"]
        }
    ]
    
    for example in examples:
        print(f"\n📋 {example['module']} 模組")
        print(f"🎨 顏色: {example['color']}")
        print(f"📝 標題: {example['title']}")
        print(f"📋 症狀: {', '.join(example['symptoms'])}")
        print(f"💡 建議: {', '.join(example['recommendations'])}")

if __name__ == "__main__":
    print("🚀 啟動 Flex Messages 演示")
    print("=" * 50)
    
    # 顯示範例
    show_flex_message_examples()
    
    # 執行演示
    demo_flex_messages() 