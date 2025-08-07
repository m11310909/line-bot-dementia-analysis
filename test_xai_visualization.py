#!/usr/bin/env python3
"""
XAI 視覺化模組測試腳本
遵循 Cursor IDE 指南進行測試
"""

import requests
import json
import time
from typing import Dict, Any

def test_xai_visualization_flow():
    """測試完整的 XAI 視覺化流程"""
    print("🧪 XAI 視覺化模組測試")
    print("=" * 50)
    
    # 測試案例
    test_cases = [
        {
            "input": "爸爸不會用洗衣機",
            "expected_module": "M1",
            "description": "M1 警訊檢測 - 功能喪失"
        },
        {
            "input": "媽媽中度失智，需要協助",
            "expected_module": "M2", 
            "description": "M2 病程評估 - 階段判斷"
        },
        {
            "input": "爺爺最近情緒不穩定，常常發脾氣",
            "expected_module": "M3",
            "description": "M3 BPSD 症狀 - 情緒問題"
        },
        {
            "input": "需要照護建議和資源",
            "expected_module": "M4",
            "description": "M4 照護導航 - 資源需求"
        }
    ]
    
    api_url = "http://localhost:8005/comprehensive-analysis"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['description']}")
        print(f"輸入: {test_case['input']}")
        print(f"預期模組: {test_case['expected_module']}")
        
        try:
            # 發送請求
            response = requests.post(
                api_url,
                json={"user_input": test_case['input']},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API 回應成功")
                print(f"📊 使用模組: {result.get('modules_used', [])}")
                print(f"🔍 找到片段: {len(result.get('retrieved_chunks', []))}")
                print(f"⏱️  回應時間: {response.elapsed.total_seconds():.3f}秒")
                
                # 檢查是否包含預期模組
                if test_case['expected_module'] in result.get('modules_used', []):
                    print(f"✅ 正確檢測到 {test_case['expected_module']} 模組")
                else:
                    print(f"⚠️  未檢測到預期的 {test_case['expected_module']} 模組")
                    
            else:
                print(f"❌ API 錯誤: {response.status_code}")
                print(f"錯誤內容: {response.text}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 XAI 視覺化測試完成")


def test_individual_modules():
    """測試個別模組端點"""
    print("\n🧪 個別模組測試")
    print("=" * 50)
    
    modules = ["M1", "M2", "M3", "M4"]
    test_input = "我最近記憶力不好"
    
    for module in modules:
        print(f"\n📋 測試 {module} 模組")
        
        try:
            response = requests.post(
                f"http://localhost:8005/analyze/{module}",
                json={"user_input": test_input},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {module} 模組回應成功")
                print(f"📊 模組: {result.get('module', 'N/A')}")
                
                if module == "M1":
                    chunks = result.get('retrieved_chunks', [])
                    print(f"🔍 找到 {len(chunks)} 個 M1 片段")
                elif module == "M2":
                    stage = result.get('stage_detection', {})
                    print(f"📈 階段檢測: {stage}")
                elif module == "M3":
                    bpsd = result.get('bpsd_analysis')
                    print(f"🧠 BPSD 分析: {bpsd}")
                elif module == "M4":
                    suggestions = result.get('action_suggestions', [])
                    print(f"💡 建議數量: {len(suggestions)}")
                    
            else:
                print(f"❌ {module} 模組錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {module} 模組測試失敗: {e}")


def test_health_endpoints():
    """測試健康檢查端點"""
    print("\n🏥 健康檢查測試")
    print("=" * 50)
    
    endpoints = [
        ("/health", "系統健康"),
        ("/modules/status", "模組狀態"),
        ("/cache/stats", "快取統計"),
        ("/gemini/stats", "Gemini 統計")
    ]
    
    for endpoint, description in endpoints:
        print(f"\n📋 測試 {description}: {endpoint}")
        
        try:
            response = requests.get(f"http://localhost:8005{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description} 端點正常")
                if endpoint == "/health":
                    data = response.json()
                    print(f"📊 狀態: {data.get('status', 'N/A')}")
                    print(f"🔧 模組: {data.get('modules_status', {})}")
            else:
                print(f"❌ {description} 端點錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description} 測試失敗: {e}")


def test_webhook_status():
    """測試 Webhook 狀態"""
    print("\n🌐 Webhook 狀態測試")
    print("=" * 50)
    
    try:
        # 測試 ngrok webhook
        response = requests.get("https://0ac6705ad6a2.ngrok-free.app/webhook", timeout=5)
        
        if response.status_code == 405:  # Method Not Allowed 是預期的
            print("✅ Webhook 端點正常 (GET 方法不允許是預期的)")
        else:
            print(f"⚠️  Webhook 回應: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Webhook 測試失敗: {e}")


def main():
    """主測試函數"""
    print("🚀 XAI 視覺化模組完整測試")
    print("遵循 Cursor IDE 指南")
    print("=" * 60)
    
    # 等待服務啟動
    print("⏳ 等待服務啟動...")
    time.sleep(2)
    
    # 執行各項測試
    test_xai_visualization_flow()
    test_individual_modules()
    test_health_endpoints()
    test_webhook_status()
    
    print("\n" + "=" * 60)
    print("🎉 所有測試完成!")
    print("📊 系統狀態: 運行中")
    print("🌐 Webhook URL: https://0ac6705ad6a2.ngrok-free.app/webhook")


if __name__ == "__main__":
    main() 