#!/usr/bin/env python3
"""
⚡ 快速測試腳本 - XAI 系統即時驗證
提供快速的功能驗證和效能檢查
"""

import requests
import time
import json
from typing import Dict, Any

def quick_test_xai_system():
    """快速測試 XAI 系統"""
    print("⚡ XAI 系統快速測試")
    print("="*40)
    
    # 測試案例
    test_cases = [
        {
            "input": "爸爸忘記關瓦斯爐",
            "expected_module": "M1",
            "description": "M1 警訊測試"
        },
        {
            "input": "媽媽中度失智",
            "expected_module": "M2", 
            "description": "M2 病程測試"
        },
        {
            "input": "爺爺有妄想症狀",
            "expected_module": "M3",
            "description": "M3 BPSD 測試"
        },
        {
            "input": "需要醫療協助",
            "expected_module": "M4",
            "description": "M4 照護測試"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試 {i}: {test_case['description']}")
        print(f"   輸入: {test_case['input']}")
        print(f"   預期模組: {test_case['expected_module']}")
        
        # 測試即時階段
        print("   🔄 測試即時階段...", end=" ")
        start_time = time.time()
        
        try:
            response = requests.post(
                "http://localhost:8009/analyze",
                json={
                    "user_input": test_case["input"],
                    "user_id": "test_user",
                    "stage": "immediate"
                },
                timeout=5
            )
            
            response_time = time.time() - start_time
            response.raise_for_status()
            
            data = response.json()
            xai_data = data.get("xai_enhanced", {})
            
            actual_module = xai_data.get("module", "unknown")
            actual_confidence = xai_data.get("confidence", 0.0)
            
            module_correct = actual_module == test_case["expected_module"]
            status = "✅" if module_correct else "❌"
            
            print(f"{status} ({response_time:.2f}s)")
            print(f"   實際模組: {actual_module}")
            print(f"   信心度: {actual_confidence:.1%}")
            
            results.append({
                "test_case": test_case["description"],
                "input": test_case["input"],
                "expected_module": test_case["expected_module"],
                "actual_module": actual_module,
                "confidence": actual_confidence,
                "response_time": response_time,
                "success": module_correct
            })
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")
            results.append({
                "test_case": test_case["description"],
                "input": test_case["input"],
                "error": str(e),
                "success": False
            })
    
    # 打印總結
    print("\n" + "="*40)
    print("📊 快速測試總結")
    print("="*40)
    
    successful_tests = [r for r in results if r.get("success", False)]
    response_times = [r.get("response_time", 0) for r in results if "response_time" in r]
    
    print(f"✅ 成功測試: {len(successful_tests)}/{len(results)}")
    if response_times:
        print(f"⚡ 平均回應時間: {sum(response_times)/len(response_times):.2f}秒")
        print(f"⚡ 最快回應時間: {min(response_times):.2f}秒")
        print(f"⚡ 最慢回應時間: {max(response_times):.2f}秒")
    
    # 詳細結果
    print("\n📋 詳細結果:")
    for result in results:
        status = "✅" if result.get("success", False) else "❌"
        module_info = f"模組: {result.get('actual_module', 'unknown')}"
        confidence_info = f"信心度: {result.get('confidence', 0):.1%}" if "confidence" in result else ""
        time_info = f"時間: {result.get('response_time', 0):.2f}s" if "response_time" in result else ""
        
        print(f"   {status} {result['test_case']} - {module_info} {confidence_info} {time_info}")
    
    return results

def test_system_health():
    """測試系統健康狀態"""
    print("\n🏥 系統健康檢查")
    print("="*30)
    
    services = [
        {"name": "XAI Wrapper", "url": "http://localhost:8009/health"},
        {"name": "Chatbot API", "url": "http://localhost:8008/health"},
        {"name": "LINE Bot", "url": "http://localhost:8081/health"}
    ]
    
    for service in services:
        try:
            start_time = time.time()
            response = requests.get(service["url"], timeout=3)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✅ {service['name']}: 正常 ({response_time:.2f}s)")
            else:
                print(f"⚠️  {service['name']}: 異常 (狀態碼: {response.status_code})")
                
        except Exception as e:
            print(f"❌ {service['name']}: 無法連接 ({e})")

def test_visualization_stages():
    """測試不同視覺化階段"""
    print("\n🎨 視覺化階段測試")
    print("="*30)
    
    test_input = "爸爸忘記關瓦斯爐"
    stages = ["immediate", "quick", "detailed"]
    
    for stage in stages:
        print(f"\n🔄 測試 {stage.upper()} 階段...", end=" ")
        start_time = time.time()
        
        try:
            response = requests.post(
                "http://localhost:8009/analyze",
                json={
                    "user_input": test_input,
                    "user_id": "test_user",
                    "stage": stage
                },
                timeout=10
            )
            
            response_time = time.time() - start_time
            response.raise_for_status()
            
            data = response.json()
            xai_data = data.get("xai_enhanced", {})
            
            module = xai_data.get("module", "unknown")
            confidence = xai_data.get("confidence", 0.0)
            
            print(f"✅ ({response_time:.2f}s)")
            print(f"   模組: {module}")
            print(f"   信心度: {confidence:.1%}")
            
        except Exception as e:
            print(f"❌ 錯誤: {e}")

def main():
    """主函數"""
    print("🚀 XAI 系統快速測試")
    print("="*50)
    
    # 系統健康檢查
    test_system_health()
    
    # 快速功能測試
    results = quick_test_xai_system()
    
    # 視覺化階段測試
    test_visualization_stages()
    
    # 保存結果
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"quick_test_results_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 測試結果已保存至: {filename}")
    print("\n✅ 快速測試完成！")

if __name__ == "__main__":
    main()