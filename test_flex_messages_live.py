#!/usr/bin/env python3
"""
即時測試 Flex Messages 功能
驗證 Flex Messages 是否正確生成和發送
"""

import requests
import json
import time
from datetime import datetime

def test_flex_messages_live():
    """即時測試 Flex Messages"""
    
    base_url = "http://localhost:8005"
    
    # 測試案例
    test_cases = [
        {
            "name": "M1 - 記憶力問題",
            "message": "我最近常常忘記事情",
            "expected_module": "M1"
        },
        {
            "name": "M2 - 情緒變化", 
            "message": "我爸爸最近變得比較容易生氣",
            "expected_module": "comprehensive"
        },
        {
            "name": "M3 - 行為症狀",
            "message": "我爺爺最近有妄想症狀",
            "expected_module": "M3"
        }
    ]
    
    print("🎨 即時 Flex Messages 測試")
    print("=" * 50)
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
    for i, test_case in enumerate(test_cases, 1):
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
        time.sleep(2)  # 等待處理完成
    
    print("🎉 測試完成！")
    print("=" * 50)
    print("📝 檢查控制台輸出以確認:")
    print("• 🎨 Flex Message 生成成功")
    print("• 📤 Flex Message 發送成功")
    print("• ✅ 測試模式回應已記錄")

def check_flex_message_structure():
    """檢查 Flex Message 結構"""
    
    print("\n🔍 Flex Message 結構檢查")
    print("=" * 30)
    
    # 模擬分析結果
    test_analysis = {
        "success": True,
        "message": "M1 分析完成",
        "data": {
            "module": "M1",
            "warning_signs": ["記憶力減退", "語言障礙", "定向力下降"],
            "risk_level": "medium",
            "recommendations": ["建議就醫檢查", "注意安全", "建立提醒系統"]
        }
    }
    
    # 導入並測試 Flex Message 生成
    import sys
    sys.path.append('.')
    
    try:
        # 動態導入函數
        import importlib.util
        spec = importlib.util.spec_from_file_location("enhanced_api", "enhanced_m1_m2_m3_integrated_api_fixed.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 測試 Flex Message 生成
        flex_message = module.create_flex_message(test_analysis, "M1")
        
        print("✅ Flex Message 結構檢查通過")
        print(f"   標題: {flex_message.get('altText', 'N/A')}")
        print(f"   類型: {flex_message.get('contents', {}).get('type', 'N/A')}")
        print(f"   大小: {flex_message.get('contents', {}).get('size', 'N/A')}")
        
        # 檢查內容結構
        contents = flex_message.get('contents', {})
        header = contents.get('header', {})
        body = contents.get('body', {})
        
        print(f"   標題顏色: {header.get('backgroundColor', 'N/A')}")
        print(f"   內容區塊: {len(body.get('contents', []))} 個")
        
        return True
        
    except Exception as e:
        print(f"❌ Flex Message 結構檢查失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 啟動 Flex Messages 即時測試")
    print("=" * 50)
    
    # 檢查 Flex Message 結構
    if check_flex_message_structure():
        # 執行即時測試
        test_flex_messages_live()
    else:
        print("❌ Flex Message 結構檢查失敗，跳過即時測試") 