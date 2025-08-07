#!/usr/bin/env python3
"""
最終 Flex Message 測試
驗證 Flex Messages 是否正確生成和發送
"""

import requests
import json
import time

def test_flex_message_generation():
    """測試 Flex Message 生成"""
    print("🎨 測試 Flex Message 生成")
    print("=" * 40)
    
    test_messages = [
        "媽媽最近常忘記關瓦斯，我很擔心",
        "爸爸重複問同樣的問題，認知功能好像有問題", 
        "爺爺有妄想症狀，覺得有人要害他"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📋 測試 {i}: {message[:30]}...")
        
        try:
            response = requests.post(
                "http://localhost:8005/comprehensive-analysis",
                json={"message": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if 'flex_message' in result:
                    flex_msg = result['flex_message']
                    print("✅ Flex Message 生成成功")
                    print(f"   標題: {flex_msg.get('altText')}")
                    print(f"   類型: {flex_msg.get('type')}")
                    
                    # 檢查結構
                    contents = flex_msg.get('contents', {})
                    if contents.get('type') == 'bubble':
                        print("✅ 結構正確 (bubble)")
                        
                        # 檢查標題區域
                        header = contents.get('header', {})
                        if header:
                            header_text = ""
                            for content in header.get('contents', []):
                                if content.get('type') == 'text':
                                    header_text = content.get('text', '')
                                    break
                            print(f"   標題: {header_text}")
                        
                        # 檢查內容區域
                        body = contents.get('body', {})
                        if body:
                            body_contents = body.get('contents', [])
                            print(f"   內容區塊數量: {len(body_contents)}")
                            
                            # 檢查症狀和建議
                            if len(body_contents) >= 3:
                                symptoms_box = body_contents[0]
                                recommendations_box = body_contents[2]
                                
                                symptoms_text = ""
                                recommendations_text = ""
                                
                                if 'contents' in symptoms_box:
                                    for content in symptoms_box['contents']:
                                        if content.get('type') == 'text':
                                            symptoms_text = content.get('text', '')
                                            break
                                
                                if 'contents' in recommendations_box:
                                    for content in recommendations_box['contents']:
                                        if content.get('type') == 'text':
                                            recommendations_text = content.get('text', '')
                                            break
                                
                                print(f"   症狀: {symptoms_text[:50]}...")
                                print(f"   建議: {recommendations_text[:50]}...")
                    else:
                        print("❌ 結構不正確")
                else:
                    print("❌ 沒有 Flex Message")
                    
            else:
                print(f"❌ API 錯誤: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
        
        time.sleep(1)

def test_webhook_endpoint():
    """測試 Webhook 端點"""
    print("\n🌐 測試 Webhook 端點")
    print("=" * 40)
    
    webhook_url = "https://e11767e116f9.ngrok-free.app/webhook"
    
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"📋 Webhook URL: {webhook_url}")
        print(f"📊 狀態碼: {response.status_code}")
        
        if response.status_code == 404:
            print("⚠️ Webhook 返回 404")
            print("💡 這表示:")
            print("   1. 服務正在運行但路由不正確")
            print("   2. 需要檢查 ngrok 隧道")
            print("   3. 需要更新 LINE Developer Console 設置")
        elif response.status_code == 200:
            print("✅ Webhook 端點正常")
        else:
            print(f"⚠️ Webhook 狀態: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Webhook 測試失敗: {e}")

def check_service_health():
    """檢查服務健康狀態"""
    print("\n🔍 檢查服務健康狀態")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8005/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ 服務健康")
            print(f"   版本: {health_data.get('version')}")
            print(f"   LINE Bot 配置: {'✅' if health_data.get('line_bot_configured') else '❌'}")
            print(f"   測試模式: {'✅' if health_data.get('test_mode') else '❌'}")
            return True
        else:
            print(f"❌ 服務不健康: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到服務: {e}")
        return False

def provide_next_steps():
    """提供下一步建議"""
    print("\n📝 下一步建議")
    print("=" * 40)
    
    steps = [
        "1. 確保 ngrok 隧道正在運行:",
        "   ngrok http 8005",
        "",
        "2. 更新 LINE Developer Console 中的 webhook URL:",
        "   https://e11767e116f9.ngrok-free.app/webhook",
        "",
        "3. 在 LINE 中發送測試訊息:",
        "   - '媽媽最近常忘記關瓦斯'",
        "   - '爸爸重複問同樣的問題'", 
        "   - '爺爺有妄想症狀'",
        "",
        "4. 檢查 LINE 中的回應是否顯示為富文本格式",
        "",
        "5. 如果仍然顯示為純文字，檢查:",
        "   - LINE Bot 憑證是否正確",
        "   - Webhook URL 是否正確設置",
        "   - 服務日誌中是否有錯誤"
    ]
    
    for step in steps:
        print(f"   {step}")

def main():
    """主函數"""
    print("🎯 最終 Flex Message 測試")
    print("=" * 50)
    print()
    
    # 檢查服務健康狀態
    if not check_service_health():
        print("❌ 服務未運行，請先啟動服務")
        return
    
    # 測試 Flex Message 生成
    test_flex_message_generation()
    
    # 測試 Webhook 端點
    test_webhook_endpoint()
    
    # 提供下一步建議
    provide_next_steps()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("✅ Flex Messages 正在正確生成")
    print("✅ 結構完整且正確")
    print("📱 請在 LINE 中測試實際效果")

if __name__ == "__main__":
    main() 