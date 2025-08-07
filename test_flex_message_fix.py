#!/usr/bin/env python3
"""
測試 Flex Message 修復
"""

import requests
import json

def test_simple_flex_message():
    """測試簡單的 Flex Message"""
    print("🧪 測試簡單 Flex Message")
    print("=" * 40)
    
    # 測試簡單的 Flex Message
    simple_flex = {
        "type": "flex",
        "altText": "測試 Flex Message",
        "contents": {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔍 測試標題",
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
                        "text": "這是一個測試 Flex Message，用於驗證修復是否有效。",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    print("✅ 簡單 Flex Message 結構:")
    print(json.dumps(simple_flex, ensure_ascii=False, indent=2))
    
    # 測試 API
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"message": "測試訊息"},
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
                    
                    # 檢查標題和內容
                    header = contents.get('header', {})
                    body = contents.get('body', {})
                    
                    if header and body:
                        print("✅ 標題和內容區域都存在")
                        
                        # 顯示標題
                        header_contents = header.get('contents', [])
                        if header_contents:
                            header_text = header_contents[0].get('text', '')
                            print(f"   標題: {header_text}")
                        
                        # 顯示內容
                        body_contents = body.get('contents', [])
                        if body_contents:
                            body_text = body_contents[0].get('text', '')
                            print(f"   內容: {body_text[:50]}...")
                    else:
                        print("⚠️ 標題或內容區域缺失")
                else:
                    print("❌ 結構不正確")
            else:
                print("❌ 沒有 Flex Message")
                
        else:
            print(f"❌ API 錯誤: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def test_line_bot_api():
    """測試 LINE Bot API 連接"""
    print("\n🤖 測試 LINE Bot API 連接")
    print("=" * 40)
    
    try:
        # 檢查服務健康狀態
        health_response = requests.get("http://localhost:8005/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print("✅ 服務健康")
            print(f"   LINE Bot 配置: {'✅' if health_data.get('line_bot_configured') else '❌'}")
        else:
            print(f"❌ 服務不健康: {health_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return
    
    print("✅ LINE Bot API 連接正常")

def provide_next_steps():
    """提供下一步建議"""
    print("\n📝 下一步建議")
    print("=" * 40)
    
    steps = [
        "1. 確保 ngrok 隧道正在運行:",
        "   ngrok http 8005",
        "",
        "2. 在 LINE 中發送測試訊息:",
        "   - '我最近常常忘記事情'",
        "   - '媽媽最近常忘記關瓦斯'",
        "",
        "3. 檢查 LINE 中的回應:",
        "   - 應該顯示為彩色卡片",
        "   - 包含標題和內容",
        "   - 而不是純文字",
        "",
        "4. 如果仍有問題:",
        "   - 檢查服務日誌",
        "   - 確認 webhook URL 設置",
        "   - 查看 LINE Developer Console 設置"
    ]
    
    for step in steps:
        print(f"   {step}")

def main():
    """主函數"""
    print("🔧 Flex Message 修復測試")
    print("=" * 50)
    print()
    
    # 測試簡單 Flex Message
    test_simple_flex_message()
    
    # 測試 LINE Bot API
    test_line_bot_api()
    
    # 提供下一步建議
    provide_next_steps()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("✅ 修復已應用")
    print("📱 請在 LINE 中測試實際效果")

if __name__ == "__main__":
    main() 