#!/usr/bin/env python3
"""
即時測試 Flex Messages
"""

import requests
import json
import time

def test_flex_message_live():
    """即時測試 Flex Message"""
    
    print("🧪 即時測試 Flex Message")
    print("=" * 40)
    
    # 測試數據
    test_cases = [
        {
            "name": "M1 記憶力測試",
            "message": "媽媽最近常忘記關瓦斯，我很擔心"
        },
        {
            "name": "M2 認知功能測試", 
            "message": "爸爸重複問同樣的問題，認知功能好像有問題"
        },
        {
            "name": "M3 行為症狀測試",
            "message": "爺爺有妄想症狀，覺得有人要害他"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 測試案例 {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # 發送測試請求
            response = requests.post(
                "http://localhost:8005/comprehensive-analysis",
                json={"message": test_case["message"]},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API 回應成功")
                print(f"   訊息: {result.get('message', 'N/A')}")
                
                # 檢查是否有 Flex Message
                if 'flex_message' in result:
                    flex_msg = result['flex_message']
                    print("🎨 Flex Message 生成成功")
                    print(f"   標題: {flex_msg.get('altText', 'N/A')}")
                    print(f"   類型: {flex_msg.get('type', 'N/A')}")
                    
                    # 檢查內容結構
                    contents = flex_msg.get('contents', {})
                    if contents.get('type') == 'bubble':
                        print("✅ Flex Message 結構正確")
                        
                        # 檢查標題和內容
                        header = contents.get('header', {})
                        body = contents.get('body', {})
                        
                        if header and body:
                            print("✅ 標題和內容區域都存在")
                        else:
                            print("⚠️ 標題或內容區域缺失")
                    else:
                        print("❌ Flex Message 結構不正確")
                else:
                    print("❌ 回應中沒有 Flex Message")
                    
            else:
                print(f"❌ API 錯誤: {response.status_code}")
                print(f"   錯誤: {response.text}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
        
        # 等待一下再進行下一個測試
        time.sleep(1)
    
    print("\n🎯 測試完成！")
    print("=" * 40)
    print("📝 如果所有測試都通過，請在 LINE 中發送測試訊息")
    print("💡 建議測試訊息:")
    print("   - '媽媽最近常忘記關瓦斯'")
    print("   - '爸爸重複問同樣的問題'")
    print("   - '爺爺有妄想症狀'")

def check_service_status():
    """檢查服務狀態"""
    print("🔍 檢查服務狀態")
    print("=" * 40)
    
    try:
        # 檢查健康狀態
        health_response = requests.get("http://localhost:8005/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ 服務健康狀態良好")
            print(f"   版本: {health_data.get('version', 'N/A')}")
            print(f"   LINE Bot 配置: {'✅' if health_data.get('line_bot_configured') else '❌'}")
            print(f"   測試模式: {'✅' if health_data.get('test_mode') else '❌'}")
        else:
            print(f"❌ 服務健康檢查失敗: {health_response.status_code}")
            
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return False
    
    return True

def main():
    """主函數"""
    print("🚀 Flex Message 即時測試")
    print("=" * 50)
    print()
    
    # 檢查服務狀態
    if not check_service_status():
        print("❌ 服務未運行，請先啟動服務")
        return
    
    # 執行測試
    test_flex_message_live()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("📱 現在請在 LINE 中發送測試訊息")
    print("🎨 檢查是否顯示為富文本格式而不是純文字")

if __name__ == "__main__":
    main() 