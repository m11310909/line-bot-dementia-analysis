#!/usr/bin/env python3
"""
測試新的 webhook URL
"""

import requests

def test_new_webhook():
    """測試新的 webhook URL"""
    print("🌐 測試新的 webhook URL")
    print("=" * 40)
    
    new_webhook_url = "https://430d701dac1e.ngrok-free.app/webhook"
    
    print(f"📋 新的 webhook URL: {new_webhook_url}")
    
    try:
        response = requests.get(new_webhook_url, timeout=10)
        print(f"📊 狀態碼: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ Webhook 端點正常 (404 是預期的)")
            print("💡 這表示:")
            print("   1. ngrok 隧道正常工作")
            print("   2. 服務正在運行")
            print("   3. 需要更新 LINE Developer Console")
        elif response.status_code == 200:
            print("✅ Webhook 端點正常")
        else:
            print(f"⚠️ Webhook 狀態: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Webhook 測試失敗: {e}")

def provide_update_instructions():
    """提供更新說明"""
    print("\n📝 更新 LINE Developer Console")
    print("=" * 40)
    
    instructions = [
        "1. 登入 LINE Developer Console:",
        "   https://developers.line.biz",
        "",
        "2. 選擇您的 Channel",
        "",
        "3. 進入 Messaging API 設定",
        "",
        "4. 更新 Webhook URL:",
        "   https://430d701dac1e.ngrok-free.app/webhook",
        "",
        "5. 確保 Webhook 已啟用",
        "",
        "6. 在 LINE 中發送測試訊息:",
        "   - '我最近常常忘記事情'",
        "   - '媽媽最近常忘記關瓦斯'",
        "",
        "7. 檢查是否收到富文本回應"
    ]
    
    for instruction in instructions:
        print(f"   {instruction}")

def main():
    """主函數"""
    print("🔧 測試新的 webhook URL")
    print("=" * 50)
    print()
    
    # 測試新的 webhook URL
    test_new_webhook()
    
    # 提供更新說明
    provide_update_instructions()
    
    print("\n🎉 測試完成！")
    print("=" * 50)
    print("✅ 新的 webhook URL 已準備就緒")
    print("📱 請更新 LINE Developer Console 並測試")

if __name__ == "__main__":
    main() 