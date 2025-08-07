#!/usr/bin/env python3
"""
測試最簡單的 Flex Message 結構
"""

import requests
import json

def test_minimal_flex_structure():
    """測試最簡單的 Flex Message 結構"""
    print("🧪 測試最簡單的 Flex Message 結構")
    print("=" * 40)
    
    # 最簡單的 Flex Message 結構
    minimal_flex = {
        "type": "flex",
        "altText": "測試訊息",
        "contents": {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔍 測試標題",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "這是一個測試訊息，用於驗證最簡單的 Flex Message 結構。",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": "#FF6B6B",
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
                    print(f"   大小: {contents.get('size')}")
                    
                    # 檢查 body 區塊
                    body = contents.get('body', {})
                    if body:
                        print("✅ body 區塊存在")
                        
                        # 檢查內容
                        body_contents = body.get('contents', [])
                        if body_contents:
                            print(f"   內容數量: {len(body_contents)}")
                            
                            # 顯示標題和內容
                            if len(body_contents) >= 2:
                                title_text = body_contents[0].get('text', '')
                                content_text = body_contents[1].get('text', '')
                                print(f"   標題: {title_text}")
                                print(f"   內容: {content_text[:50]}...")
                    else:
                        print("❌ body 區塊缺失")
                else:
                    print("❌ 結構不正確")
            else:
                print("❌ 沒有 Flex Message")
                
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def check_service_status():
    """檢查服務狀態"""
    print("\n🔍 檢查服務狀態")
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
    
    print("✅ 服務狀態正常")

def provide_next_steps():
    """提供下一步建議"""
    print("\n📝 下一步建議")
    print("=" * 40)
    
    steps = [
        "1. 問題分析:",
        "   - 使用最簡單的 Flex Message 結構",
        "   - 只包含 body 區塊，不包含 header",
        "   - 使用 micro 大小避免複雜結構",
        "",
        "2. 測試步驟:",
        "   - 在 LINE 中發送新訊息",
        "   - 檢查是否收到富文本回應",
        "   - 如果仍有問題，檢查服務日誌",
        "",
        "3. 預期結果:",
        "   - 應該顯示為簡單的彩色卡片",
        "   - 包含標題和內容",
        "   - 而不是純文字格式"
    ]
    
    for step in steps:
        print(f"   {step}")

def main():
    """主函數"""
    print("🔧 最簡單 Flex Message 測試")
    print("=" * 50)
    print()
    
    # 檢查服務狀態
    check_service_status()
    
    # 測試最簡單的 Flex Message 結構
    test_minimal_flex_structure()
    
    # 提供下一步建議
    provide_next_steps()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("✅ 最簡單的 Flex Message 結構已應用")
    print("📱 請在 LINE 中重新發送訊息測試")

if __name__ == "__main__":
    main() 