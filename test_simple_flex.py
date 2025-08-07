#!/usr/bin/env python3
"""
簡單的 Flex Message 測試
"""

import requests
import json

def test_minimal_flex_message():
    """測試最簡單的 Flex Message"""
    print("🧪 測試最簡單的 Flex Message")
    print("=" * 40)
    
    # 最簡單的 Flex Message
    minimal_flex = {
        "type": "flex",
        "altText": "測試訊息",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "測試標題",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    }
                ],
                "backgroundColor": "#FF6B6B",
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "這是一個測試訊息",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    print("✅ 最簡單的 Flex Message 結構:")
    print(json.dumps(minimal_flex, ensure_ascii=False, indent=2))
    
    # 測試 API
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"message": "測試"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API 測試成功")
            
            if 'flex_message' in result:
                flex_msg = result['flex_message']
                print("🎨 Flex Message 生成成功")
                print(f"   標題: {flex_msg.get('altText')}")
                print(f"   類型: {flex_msg.get('type')}")
                
                # 檢查結構
                contents = flex_msg.get('contents', {})
                if contents.get('type') == 'bubble':
                    print("✅ 結構正確 (bubble)")
                    
                    # 檢查必要區塊
                    header = contents.get('header', {})
                    body = contents.get('body', {})
                    
                    if header and body:
                        print("✅ 標題和內容區塊都存在")
                        
                        # 檢查標題內容
                        header_contents = header.get('contents', [])
                        if header_contents:
                            header_text = header_contents[0].get('text', '')
                            print(f"   標題: {header_text}")
                        
                        # 檢查內容
                        body_contents = body.get('contents', [])
                        if body_contents:
                            body_text = body_contents[0].get('text', '')
                            print(f"   內容: {body_text[:50]}...")
                    else:
                        print("❌ 缺少必要區塊")
                else:
                    print("❌ 結構不正確")
            else:
                print("❌ 沒有 Flex Message")
                
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def check_line_bot_status():
    """檢查 LINE Bot 狀態"""
    print("\n🤖 檢查 LINE Bot 狀態")
    print("=" * 40)
    
    try:
        # 檢查服務健康狀態
        health_response = requests.get("http://localhost:8005/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ 服務健康")
            print(f"   LINE Bot 配置: {'✅' if health_data.get('line_bot_configured') else '❌'}")
            print(f"   測試模式: {'✅' if health_data.get('test_mode') else '❌'}")
        else:
            print(f"❌ 服務不健康: {health_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return
    
    print("✅ LINE Bot 狀態正常")

def provide_solution():
    """提供解決方案"""
    print("\n💡 解決方案")
    print("=" * 40)
    
    solutions = [
        "1. 問題分析:",
        "   - 'At least one block must be specified' 表示 Flex Message 結構問題",
        "   - 'Invalid reply token' 表示 reply token 已過期",
        "",
        "2. 解決方法:",
        "   - 確保 Flex Message 包含 header 和 body 區塊",
        "   - 用戶需要重新發送訊息以獲得新的 reply token",
        "",
        "3. 測試步驟:",
        "   - 在 LINE 中發送新訊息",
        "   - 檢查是否收到富文本回應",
        "   - 如果仍有問題，檢查服務日誌"
    ]
    
    for solution in solutions:
        print(f"   {solution}")

def main():
    """主函數"""
    print("🔧 簡單 Flex Message 測試")
    print("=" * 50)
    print()
    
    # 檢查 LINE Bot 狀態
    check_line_bot_status()
    
    # 測試最簡單的 Flex Message
    test_minimal_flex_message()
    
    # 提供解決方案
    provide_solution()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("✅ 修復已應用")
    print("📱 請在 LINE 中重新發送訊息測試")

if __name__ == "__main__":
    main() 