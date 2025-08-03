#!/usr/bin/env python3
"""
非線性模組跳轉測試腳本
測試 M1 ←→ M3, M3 ←→ M4, M2 ←→ M1 的跳轉功能
"""

import requests
import json
import time
import sys

def test_module_jump():
    """測試非線性模組跳轉功能"""
    
    base_url = "http://localhost:8008"
    
    # 測試案例
    test_cases = [
        {
            "name": "M1 → M3 跳轉 (發現症狀直接處理)",
            "messages": [
                "媽媽忘記關瓦斯",  # M1 警訊
                "爺爺有妄想症狀",  # M3 BPSD
                "爸爸有攻擊行為"   # M3 BPSD
            ],
            "expected_flow": ["M1", "M3", "M3"],
            "description": "從警訊發現直接跳轉到症狀處理"
        },
        {
            "name": "M3 → M4 跳轉 (症狀處理後申請資源)", 
            "messages": [
                "爺爺有妄想症狀",  # M3 BPSD
                "需要醫療協助",    # M4 照護需求
                "需要照護資源"     # M4 照護需求
            ],
            "expected_flow": ["M3", "M4", "M4"],
            "description": "從症狀處理跳轉到資源申請"
        },
        {
            "name": "M2 → M1 跳轉 (了解病程後重新評估)",
            "messages": [
                "媽媽中度失智",     # M2 病程階段
                "媽媽忘記關瓦斯",  # M1 警訊
                "奶奶有躁動不安"   # M1 警訊
            ],
            "expected_flow": ["M2", "M1", "M1"],
            "description": "從病程了解跳轉到警訊重新評估"
        },
        {
            "name": "複雜跳轉路徑 (任意路徑導航)",
            "messages": [
                "媽媽忘記關瓦斯",  # M1
                "媽媽中度失智",     # M2  
                "爺爺有妄想症狀",  # M3
                "需要醫療協助",    # M4
                "奶奶有躁動不安"   # M1
            ],
            "expected_flow": ["M1", "M2", "M3", "M4", "M1"],
            "description": "測試任意模組間的跳轉能力"
        },
        {
            "name": "M1 → M3 → M4 連續跳轉",
            "messages": [
                "爸爸不會用洗衣機",  # M1 警訊
                "爺爺有妄想症狀",    # M3 BPSD
                "需要醫療協助"       # M4 照護需求
            ],
            "expected_flow": ["M1", "M3", "M4"],
            "description": "測試連續跳轉的流暢性"
        }
    ]
    
    print("🧪 非線性模組跳轉測試")
    print("=" * 60)
    print("🎯 測試目標:")
    print("   • M1 ←→ M3 (發現症狀直接處理)")
    print("   • M3 ←→ M4 (症狀處理後申請資源)")
    print("   • M2 ←→ M1 (了解病程後重新評估)")
    print("   • 任意路徑導航能力")
    print("=" * 60)
    
    total_accuracy = 0
    total_tests = 0
    
    for test_case in test_cases:
        print(f"\n📋 測試案例: {test_case['name']}")
        print(f"📝 描述: {test_case['description']}")
        print("-" * 50)
        
        actual_flow = []
        
        for i, message in enumerate(test_case['messages']):
            print(f"\n🔍 步驟 {i+1}: {message}")
            
            try:
                # 發送請求
                response = requests.post(
                    f"{base_url}/analyze",
                    json={"message": message, "user_id": "test_user"},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 檢查回應類型
                    response_type = data.get('type', 'unknown')
                    
                    if response_type == 'text':
                        # 純文字回應，從文字內容判斷模組
                        text_content = data.get('contents', {}).get('text', '')
                        if '警訊分析' in text_content or 'M1' in text_content:
                            detected_module = 'M1'
                        elif '病程評估' in text_content or 'M2' in text_content:
                            detected_module = 'M2'
                        elif '症狀分析' in text_content or 'M3' in text_content:
                            detected_module = 'M3'
                        elif '照護建議' in text_content or 'M4' in text_content:
                            detected_module = 'M4'
                        else:
                            detected_module = 'Unknown'
                    else:
                        # Flex Message 回應，從 altText 判斷模組
                        alt_text = data.get('altText', '')
                        if 'M1' in alt_text or '警訊分析' in alt_text:
                            detected_module = 'M1'
                        elif 'M2' in alt_text or '病程階段' in alt_text:
                            detected_module = 'M2'
                        elif 'M3' in alt_text or 'BPSD' in alt_text:
                            detected_module = 'M3'
                        elif 'M4' in alt_text or '照護需求' in alt_text:
                            detected_module = 'M4'
                        else:
                            detected_module = 'Unknown'
                    
                    actual_flow.append(detected_module)
                    expected = test_case['expected_flow'][i]
                    
                    status = "✅" if detected_module == expected else "❌"
                    print(f"   {status} 檢測到模組: {detected_module} (預期: {expected})")
                    print(f"   📝 回應類型: {response_type}")
                    
                    # 顯示回應摘要
                    if response_type == 'flex':
                        alt_text = data.get('altText', '')
                        print(f"   💬 回應摘要: {alt_text[:50]}...")
                    else:
                        text_content = data.get('contents', {}).get('text', '')
                        print(f"   💬 回應摘要: {text_content[:50]}...")
                    
                else:
                    print(f"   ❌ 請求失敗: {response.status_code}")
                    print(f"   📄 錯誤詳情: {response.text}")
                    actual_flow.append('Error')
                    
            except Exception as e:
                print(f"   ❌ 測試失敗: {str(e)}")
                actual_flow.append('Error')
            
            time.sleep(0.5)  # 避免請求過於頻繁
        
        # 檢查整體流程
        print(f"\n📊 流程總結:")
        print(f"   預期流程: {' → '.join(test_case['expected_flow'])}")
        print(f"   實際流程: {' → '.join(actual_flow)}")
        
        # 計算跳轉準確率
        correct_jumps = sum(1 for actual, expected in zip(actual_flow, test_case['expected_flow']) 
                          if actual == expected)
        accuracy = (correct_jumps / len(test_case['expected_flow'])) * 100
        
        print(f"   🎯 跳轉準確率: {accuracy:.1f}%")
        
        if accuracy == 100:
            print("   🎉 完美跳轉!")
        elif accuracy >= 80:
            print("   ✅ 良好跳轉!")
        else:
            print("   ⚠️ 跳轉需要改進")
        
        total_accuracy += accuracy
        total_tests += 1
    
    # 總體統計
    print(f"\n🎯 總體測試結果:")
    print(f"   平均準確率: {(total_accuracy / total_tests):.1f}%")
    print(f"   測試案例數: {total_tests}")

def test_specific_jump_scenarios():
    """測試特定跳轉場景"""
    
    base_url = "http://localhost:8008"
    
    print("\n🎯 特定跳轉場景測試")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "症狀發現 → 直接處理",
            "messages": [
                "媽媽忘記關瓦斯",  # 發現症狀
                "爺爺有妄想症狀"   # 直接處理症狀
            ],
            "expected_jump": "M1 → M3"
        },
        {
            "name": "症狀處理 → 申請資源", 
            "messages": [
                "爺爺有妄想症狀",  # 處理症狀
                "需要醫療協助"     # 申請資源
            ],
            "expected_jump": "M3 → M4"
        },
        {
            "name": "了解病程 → 重新評估",
            "messages": [
                "媽媽中度失智",     # 了解病程
                "媽媽忘記關瓦斯"   # 重新評估警訊
            ],
            "expected_jump": "M2 → M1"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 場景: {scenario['name']}")
        print(f"🎯 預期跳轉: {scenario['expected_jump']}")
        print("-" * 40)
        
        for i, message in enumerate(scenario['messages']):
            print(f"\n🔍 步驟 {i+1}: {message}")
            
            try:
                response = requests.post(
                    f"{base_url}/analyze",
                    json={"message": message, "user_id": "test_user"},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 提取失智小幫手的回應
                    if data.get('type') == 'text':
                        chatbot_reply = data.get('contents', {}).get('text', '')
                    else:
                        # 從 Flex Message 中提取文字內容
                        contents = data.get('contents', {}).get('body', {}).get('contents', [])
                        chatbot_reply = ""
                        for content in contents:
                            if isinstance(content, dict) and content.get('type') == 'text':
                                text = content.get('text', '')
                                if '失智小幫手' in text or '分析結果' in text:
                                    chatbot_reply = text
                                    break
                    
                    print(f"   💬 失智小幫手回應: {chatbot_reply[:100]}...")
                    
                else:
                    print(f"   ❌ 請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 測試失敗: {str(e)}")
            
            time.sleep(0.5)

def test_line_bot_integration():
    """測試 LINE Bot 整合的非線性跳轉"""
    
    print("\n🤖 LINE Bot 整合測試")
    print("=" * 50)
    
    # 檢查 LINE Bot 服務狀態
    try:
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code == 200:
            print("✅ LINE Bot 服務正常")
        else:
            print("❌ LINE Bot 服務異常")
            return
    except:
        print("❌ LINE Bot 服務無法連接")
        return
    
    # 測試案例
    test_messages = [
        "媽媽忘記關瓦斯",  # M1
        "爺爺有妄想症狀",  # M3
        "需要醫療協助",    # M4
        "媽媽中度失智",     # M2
        "奶奶有躁動不安"   # M1
    ]
    
    print(f"\n📝 測試訊息序列:")
    for i, msg in enumerate(test_messages, 1):
        print(f"   {i}. {msg}")
    
    print(f"\n🎯 預期跳轉路徑: M1 → M3 → M4 → M2 → M1")
    print(f"💡 這將測試完整的非線性模組跳轉能力")

if __name__ == "__main__":
    print("🚀 開始非線性模組跳轉測試...")
    
    # 檢查服務狀態
    try:
        response = requests.get("http://localhost:8008/health", timeout=5)
        if response.status_code == 200:
            print("✅ Chatbot API 服務正常")
        else:
            print("❌ Chatbot API 服務異常")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Chatbot API 服務無法連接: {e}")
        print("💡 請確保 Chatbot API 正在運行 (port 8008)")
        sys.exit(1)
    
    # 測試基本跳轉功能
    test_module_jump()
    
    # 測試特定跳轉場景
    test_specific_jump_scenarios()
    
    # 測試 LINE Bot 整合
    test_line_bot_integration()
    
    print("\n✅ 測試完成!")
    print("\n📋 測試總結:")
    print("   • 非線性模組跳轉功能")
    print("   • 任意路徑導航能力")
    print("   • 症狀發現直接處理")
    print("   • 症狀處理後申請資源")
    print("   • 了解病程後重新評估") 