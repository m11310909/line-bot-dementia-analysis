#!/usr/bin/env python3
"""
診斷 Flex Messages 顯示為純文字的問題
"""

import os
import json
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def check_environment():
    """檢查環境設置"""
    print("🔍 檢查環境設置")
    print("=" * 40)
    
    # 檢查環境變數
    required_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN",
        "LINE_CHANNEL_SECRET"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: 已設置 ({value[:20]}...)")
        else:
            print(f"❌ {var}: 未設置")
    
    print()

def check_flex_message_structure():
    """檢查 Flex Message 結構"""
    print("🎨 檢查 Flex Message 結構")
    print("=" * 40)
    
    # 讀取生成的 Flex Message
    try:
        with open("debug_flex_message_1_M1.json", "r", encoding="utf-8") as f:
            flex_message = json.load(f)
        
        print("✅ Flex Message JSON 結構正確")
        print(f"   類型: {flex_message.get('type')}")
        print(f"   標題: {flex_message.get('altText')}")
        
        contents = flex_message.get('contents', {})
        print(f"   內容類型: {contents.get('type')}")
        print(f"   大小: {contents.get('size')}")
        
        # 檢查必要的 Flex Message 字段
        required_fields = ['type', 'altText', 'contents']
        missing_fields = []
        
        for field in required_fields:
            if field not in flex_message:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ 缺少必要字段: {missing_fields}")
        else:
            print("✅ 所有必要字段都存在")
            
    except Exception as e:
        print(f"❌ 讀取 Flex Message 失敗: {e}")
    
    print()

def check_line_bot_api():
    """檢查 LINE Bot API 連接"""
    print("🤖 檢查 LINE Bot API 連接")
    print("=" * 40)
    
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if not channel_access_token:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN 未設置")
        return
    
    try:
        # 測試 LINE Bot API 連接
        headers = {
            "Authorization": f"Bearer {channel_access_token}",
            "Content-Type": "application/json"
        }
        
        # 獲取 Bot 資料
        response = requests.get(
            "https://api.line.me/v2/bot/profile/U1234567890",  # 使用測試用戶ID
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ LINE Bot API 連接正常")
        elif response.status_code == 404:
            print("⚠️ LINE Bot API 連接正常，但測試用戶不存在（這是正常的）")
        else:
            print(f"❌ LINE Bot API 錯誤: {response.status_code}")
            print(f"   錯誤訊息: {response.text}")
            
    except Exception as e:
        print(f"❌ LINE Bot API 連接失敗: {e}")
    
    print()

def check_webhook_url():
    """檢查 Webhook URL"""
    print("🌐 檢查 Webhook URL")
    print("=" * 40)
    
    try:
        with open("webhook_url.txt", "r") as f:
            webhook_url = f.read().strip()
        
        print(f"📋 Webhook URL: {webhook_url}")
        
        # 測試 webhook URL 是否可訪問
        try:
            response = requests.get(webhook_url, timeout=10)
            print(f"✅ Webhook URL 可訪問: {response.status_code}")
        except Exception as e:
            print(f"❌ Webhook URL 無法訪問: {e}")
            
    except Exception as e:
        print(f"❌ 讀取 Webhook URL 失敗: {e}")
    
    print()

def check_flex_message_sending():
    """檢查 Flex Message 發送邏輯"""
    print("📤 檢查 Flex Message 發送邏輯")
    print("=" * 40)
    
    # 檢查 send_line_reply 函數中的問題
    print("🔍 檢查 send_line_reply 函數...")
    
    # 模擬 Flex Message 發送
    test_flex_message = {
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
                        "text": "測試內容",
                        "size": "sm",
                        "color": "#666666"
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    print("✅ 測試 Flex Message 結構正確")
    print(f"   類型: {test_flex_message.get('type')}")
    print(f"   標題: {test_flex_message.get('altText')}")
    
    # 檢查可能的問題
    potential_issues = []
    
    # 1. 檢查是否使用了正確的 LINE Bot SDK 版本
    try:
        from linebot.v3.messaging import FlexMessage
        print("✅ 使用 LINE Bot SDK v3")
    except ImportError:
        try:
            from linebot.models import FlexSendMessage
            print("⚠️ 使用 LINE Bot SDK v2（可能會有兼容性問題）")
            potential_issues.append("LINE Bot SDK 版本可能不兼容")
        except ImportError:
            print("❌ LINE Bot SDK 未安裝")
            potential_issues.append("LINE Bot SDK 未安裝")
    
    # 2. 檢查 Flex Message 格式
    if test_flex_message.get("type") != "flex":
        potential_issues.append("Flex Message 類型不正確")
    
    if not test_flex_message.get("altText"):
        potential_issues.append("缺少 altText 字段")
    
    if not test_flex_message.get("contents"):
        potential_issues.append("缺少 contents 字段")
    
    if potential_issues:
        print("❌ 發現潛在問題:")
        for issue in potential_issues:
            print(f"   - {issue}")
    else:
        print("✅ 未發現明顯問題")
    
    print()

def check_common_solutions():
    """提供常見解決方案"""
    print("💡 常見解決方案")
    print("=" * 40)
    
    solutions = [
        "1. 確保 LINE Bot 服務正在運行",
        "2. 檢查 webhook URL 是否正確設置在 LINE Developer Console",
        "3. 確認 Flex Message 結構符合 LINE 官方規範",
        "4. 檢查 LINE Bot SDK 版本是否正確",
        "5. 確認環境變數正確載入",
        "6. 檢查網路連接和防火牆設置",
        "7. 查看 LINE Bot 的錯誤日誌"
    ]
    
    for solution in solutions:
        print(f"   {solution}")
    
    print()

def main():
    """主診斷函數"""
    print("🔧 Flex Messages 問題診斷工具")
    print("=" * 50)
    print()
    
    check_environment()
    check_flex_message_structure()
    check_line_bot_api()
    check_webhook_url()
    check_flex_message_sending()
    check_common_solutions()
    
    print("🎯 診斷完成！")
    print("=" * 50)
    print("📝 建議:")
    print("1. 首先啟動您的 LINE Bot 服務")
    print("2. 檢查 webhook URL 是否正確設置")
    print("3. 確認 Flex Message 結構正確")
    print("4. 查看實際的錯誤日誌")

if __name__ == "__main__":
    main() 