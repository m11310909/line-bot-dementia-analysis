#!/usr/bin/env python3
"""
測試第三方 API 失智症小幫手1 的連接和回應
支援 OpenAI API 和其他自定義 API
"""

import requests
import json
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_openai_api(api_key: str, test_messages: list):
    """測試 OpenAI API"""
    print("🤖 測試 OpenAI API")
    print(f"🔑 API Key: {'已設定' if api_key else '未設定'}")
    print("-" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    for i, message in enumerate(test_messages, 1):
        print(f"📝 測試 {i}: {message}")
        
        # OpenAI API 請求格式
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一個專業的失智症照護助手，專門協助家屬處理失智症相關問題。請用中文回答，並提供實用的建議。"
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"📊 狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"✅ 成功: {content[:100]}...")
                else:
                    print("❌ 回應格式錯誤")
            else:
                print(f"❌ 錯誤: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ 請求失敗: {str(e)}")
        
        print("-" * 50)

def test_custom_api(api_url: str, api_key: str, api_name: str, test_messages: list):
    """測試自定義 API"""
    print(f"🧪 測試 {api_name}")
    print(f"📍 API URL: {api_url}")
    print(f"🔑 API Key: {'已設定' if api_key else '未設定'}")
    print("-" * 50)
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    for i, message in enumerate(test_messages, 1):
        print(f"📝 測試 {i}: {message}")
        
        try:
            response = requests.post(
                api_url,
                json={"message": message, "user_id": "test_user"},
                headers=headers,
                timeout=30
            )
            
            print(f"📊 狀態碼: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ 成功: {str(result)[:200]}...")
                except:
                    print(f"✅ 成功: {response.text[:200]}...")
            else:
                print(f"❌ 錯誤: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ 請求失敗: {str(e)}")
        
        print("-" * 50)

def main():
    """主測試函數"""
    
    # 獲取配置
    api_url = os.getenv('THIRD_PARTY_API_URL')
    api_key = os.getenv('THIRD_PARTY_API_KEY')
    api_name = os.getenv('THIRD_PARTY_API_NAME', '第三方 API')
    
    if not api_url:
        print("❌ 錯誤：未設定 THIRD_PARTY_API_URL")
        print("請在 .env 文件中設定正確的 API URL")
        return
    
    # 測試訊息
    test_messages = [
        "媽媽最近常忘記關瓦斯爐",
        "爸爸中度失智，需要全天候照顧",
        "爺爺有妄想症狀，常說有人要害他",
        "需要醫療協助和照護資源"
    ]
    
    # 判斷 API 類型
    if "openai.com" in api_url or "api.openai.com" in api_url:
        test_openai_api(api_key, test_messages)
    else:
        test_custom_api(api_url, api_key, api_name, test_messages)
    
    print("🏁 測試完成")
    print("\n💡 提示：")
    print("- 如果測試成功，您可以啟動 LINE Bot 服務")
    print("- 如果測試失敗，請檢查 API URL 和 Key 是否正確")
    print("- 參考 THIRD_PARTY_API_SETUP.md 獲取詳細配置說明")

if __name__ == "__main__":
    main() 