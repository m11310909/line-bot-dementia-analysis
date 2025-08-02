#!/usr/bin/env python3
"""
測試 M1-M4 視覺化模組的 XAI 功能
"""

import requests
import json
import time

def test_xai_visualization():
    """測試 XAI 視覺化功能"""
    
    base_url = "http://localhost:8008"
    
    # 測試案例
    test_cases = [
        {
            "message": "媽媽總是忘記關瓦斯",
            "expected_module": "M1",
            "description": "M1 警訊分析 - 忘記關瓦斯"
        },
        {
            "message": "爸爸中度失智，經常迷路",
            "expected_module": "M2", 
            "description": "M2 病程階段 - 中度失智"
        },
        {
            "message": "爺爺有妄想症狀，懷疑有人偷東西",
            "expected_module": "M3",
            "description": "M3 BPSD 症狀 - 妄想症狀"
        },
        {
            "message": "需要醫療協助和照護資源",
            "expected_module": "M4",
            "description": "M4 照護需求 - 醫療和照護"
        }
    ]
    
    print("🧪 開始測試 M1-M4 XAI 視覺化功能")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['description']}")
        print(f"📝 輸入訊息: {test_case['message']}")
        
        try:
            # 測試自動模組選擇
            response = requests.post(
                f"{base_url}/analyze",
                json={"message": test_case['message'], "user_id": "test_user"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 自動模組選擇成功")
                print(f"📊 回應類型: {result.get('type', 'N/A')}")
                print(f"📝 回應長度: {len(json.dumps(result))} 字符")
                
                # 檢查 XAI 元素
                contents = result.get('contents', {})
                body = contents.get('body', {})
                body_contents = body.get('contents', [])
                
                xai_elements = []
                confidence_found = False
                reasoning_found = False
                
                for element in body_contents:
                    if isinstance(element, dict):
                        text = element.get('text', '')
                        # 檢查信心度元素
                        if 'AI 信心度' in text or '🎯' in text:
                            confidence_found = True
                            xai_elements.append(f"信心度: {text}")
                        # 檢查推理路徑元素
                        elif '推理路徑' in text or '🧠' in text:
                            reasoning_found = True
                            xai_elements.append(f"推理路徑: {text}")
                        # 檢查進度條元素
                        elif element.get('backgroundColor') and element.get('height') == '8px':
                            xai_elements.append("信心度進度條")
                
                if xai_elements:
                    print(f"🎯 檢測到 XAI 元素: {len(xai_elements)} 個")
                    for element in xai_elements[:3]:  # 顯示前3個
                        print(f"   - {element}")
                else:
                    print("⚠️ 未檢測到 XAI 元素")
                
                print(f"🎯 信心度視覺化: {'✅' if confidence_found else '❌'}")
                print(f"🧠 推理路徑: {'✅' if reasoning_found else '❌'}")
                    
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                print(f"錯誤訊息: {response.text}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {str(e)}")
        
        time.sleep(1)  # 避免請求過於頻繁
    
    # 測試 XAI 資訊端點
    print(f"\n🔍 測試 XAI 資訊端點")
    try:
        xai_response = requests.get(f"{base_url}/xai-info", timeout=10)
        if xai_response.status_code == 200:
            xai_info = xai_response.json()
            print(f"✅ XAI 資訊獲取成功")
            print(f"📊 版本: {xai_info.get('version', 'N/A')}")
            print(f"🎯 XAI 功能數量: {len(xai_info.get('xai_features', {}))}")
            print(f"📋 模組數量: {len(xai_info.get('modules', {}))}")
        else:
            print(f"❌ XAI 資訊獲取失敗: {xai_response.status_code}")
    except Exception as e:
        print(f"❌ XAI 資訊測試失敗: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 XAI 視覺化功能測試完成")

def test_individual_modules():
    """測試個別模組的 XAI 功能"""
    
    base_url = "http://localhost:8008"
    
    module_tests = [
        {
            "endpoint": "/analyze/m1",
            "message": "媽媽忘記關瓦斯",
            "description": "M1 警訊分析"
        },
        {
            "endpoint": "/analyze/m2", 
            "message": "爸爸中度失智",
            "description": "M2 病程階段"
        },
        {
            "endpoint": "/analyze/m3",
            "message": "爺爺有妄想症狀",
            "description": "M3 BPSD 症狀"
        },
        {
            "endpoint": "/analyze/m4",
            "message": "需要醫療協助",
            "description": "M4 照護需求"
        }
    ]
    
    print("\n🧪 測試個別模組的 XAI 功能")
    print("=" * 50)
    
    for test in module_tests:
        print(f"\n📋 測試: {test['description']}")
        print(f"📝 訊息: {test['message']}")
        
        try:
            response = requests.post(
                f"{base_url}{test['endpoint']}",
                json={"message": test['message'], "user_id": "test_user"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {test['description']} 成功")
                
                # 檢查信心度元素
                contents = result.get('contents', {})
                body = contents.get('body', {})
                body_contents = body.get('contents', [])
                
                confidence_found = False
                reasoning_found = False
                
                for element in body_contents:
                    if isinstance(element, dict):
                        text = element.get('text', '')
                        if 'AI 信心度' in text:
                            confidence_found = True
                        elif '推理路徑' in text:
                            reasoning_found = True
                
                print(f"🎯 信心度視覺化: {'✅' if confidence_found else '❌'}")
                print(f"🧠 推理路徑: {'✅' if reasoning_found else '❌'}")
                
            else:
                print(f"❌ 請求失敗: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {str(e)}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 啟動 M1-M4 XAI 視覺化測試")
    
    # 測試自動模組選擇
    test_xai_visualization()
    
    # 測試個別模組
    test_individual_modules()
    
    print("\n🎉 所有測試完成！") 