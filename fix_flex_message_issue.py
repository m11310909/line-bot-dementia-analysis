#!/usr/bin/env python3
"""
修復 Flex Messages 顯示為純文字的問題
"""

import os
import subprocess
import time
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def start_line_bot_service():
    """啟動 LINE Bot 服務"""
    print("🚀 啟動 LINE Bot 服務")
    print("=" * 40)
    
    # 檢查服務是否已經在運行
    try:
        response = requests.get("https://e11767e116f9.ngrok-free.app/webhook", timeout=5)
        if response.status_code != 404:
            print("✅ LINE Bot 服務已在運行")
            return True
    except:
        pass
    
    # 啟動服務
    try:
        print("📦 啟動 enhanced_m1_m2_m3_integrated_api_fixed.py...")
        
        # 使用 uvicorn 啟動服務
        cmd = [
            "uvicorn", 
            "enhanced_m1_m2_m3_integrated_api_fixed:app",
            "--host", "0.0.0.0",
            "--port", "8005",
            "--reload"
        ]
        
        # 在背景啟動服務
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ 等待服務啟動...")
        time.sleep(5)  # 等待服務啟動
        
        # 檢查服務是否成功啟動
        try:
            response = requests.get("http://localhost:8005/health", timeout=10)
            if response.status_code == 200:
                print("✅ LINE Bot 服務啟動成功")
                return True
            else:
                print(f"⚠️ 服務啟動但健康檢查失敗: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 服務啟動失敗: {e}")
            return False
            
    except Exception as e:
        print(f"❌ 啟動服務時發生錯誤: {e}")
        return False

def test_flex_message_sending():
    """測試 Flex Message 發送"""
    print("\n🧪 測試 Flex Message 發送")
    print("=" * 40)
    
    # 創建測試 Flex Message
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
                        "text": "🎯 測試標題",
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
                        "text": "這是一個測試 Flex Message，用於驗證富文本顯示是否正常。",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    try:
        # 測試發送到本地 API
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"message": "測試訊息"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API 測試成功")
            result = response.json()
            print(f"   回應: {result.get('message', 'N/A')}")
        else:
            print(f"❌ API 測試失敗: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ API 測試失敗: {e}")

def check_webhook_configuration():
    """檢查 Webhook 配置"""
    print("\n🌐 檢查 Webhook 配置")
    print("=" * 40)
    
    webhook_url = "https://e11767e116f9.ngrok-free.app/webhook"
    
    print(f"📋 Webhook URL: {webhook_url}")
    
    # 檢查 webhook 是否可訪問
    try:
        response = requests.get(webhook_url, timeout=10)
        print(f"✅ Webhook 可訪問: {response.status_code}")
        
        if response.status_code == 404:
            print("⚠️ Webhook 返回 404，這表示:")
            print("   1. 服務未啟動")
            print("   2. 路由配置不正確")
            print("   3. ngrok 隧道未正確設置")
            
    except Exception as e:
        print(f"❌ Webhook 無法訪問: {e}")
        print("💡 建議:")
        print("   1. 檢查 ngrok 是否正在運行")
        print("   2. 確認 webhook URL 是否正確")
        print("   3. 檢查防火牆設置")

def create_test_script():
    """創建測試腳本"""
    print("\n📝 創建測試腳本")
    print("=" * 40)
    
    test_script = '''#!/usr/bin/env python3
"""
測試 Flex Message 發送
"""

import requests
import json

def test_flex_message():
    """測試 Flex Message 發送"""
    
    # 測試 Flex Message
    flex_message = {
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
                        "text": "🎯 測試標題",
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
                        "text": "這是一個測試 Flex Message，用於驗證富文本顯示是否正常。",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            }
        }
    }
    
    print("🎨 測試 Flex Message 結構:")
    print(json.dumps(flex_message, ensure_ascii=False, indent=2))
    
    # 測試 API
    try:
        response = requests.post(
            "http://localhost:8005/comprehensive-analysis",
            json={"message": "測試訊息"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API 測試成功")
            result = response.json()
            print(f"   回應: {result}")
        else:
            print(f"❌ API 測試失敗: {response.status_code}")
            print(f"   錯誤: {response.text}")
            
    except Exception as e:
        print(f"❌ API 測試失敗: {e}")

if __name__ == "__main__":
    test_flex_message()
'''
    
    with open("test_flex_message_simple.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ 測試腳本已創建: test_flex_message_simple.py")

def provide_solutions():
    """提供解決方案"""
    print("\n💡 解決方案")
    print("=" * 40)
    
    solutions = [
        "1. 啟動 LINE Bot 服務:",
        "   python3 enhanced_m1_m2_m3_integrated_api_fixed.py",
        "",
        "2. 或者使用 uvicorn 啟動:",
        "   uvicorn enhanced_m1_m2_m3_integrated_api_fixed:app --host 0.0.0.0 --port 8005 --reload",
        "",
        "3. 檢查 ngrok 隧道:",
        "   ngrok http 8005",
        "",
        "4. 更新 LINE Developer Console 中的 webhook URL",
        "",
        "5. 測試 Flex Message:",
        "   python3 test_flex_message_simple.py",
        "",
        "6. 檢查 LINE Bot 日誌以查看詳細錯誤信息"
    ]
    
    for solution in solutions:
        print(f"   {solution}")

def main():
    """主修復函數"""
    print("🔧 Flex Messages 問題修復工具")
    print("=" * 50)
    print()
    
    # 1. 啟動服務
    if start_line_bot_service():
        print("✅ 服務啟動成功")
    else:
        print("❌ 服務啟動失敗")
    
    # 2. 測試 Flex Message
    test_flex_message_sending()
    
    # 3. 檢查 Webhook 配置
    check_webhook_configuration()
    
    # 4. 創建測試腳本
    create_test_script()
    
    # 5. 提供解決方案
    provide_solutions()
    
    print("\n🎯 修復完成！")
    print("=" * 50)
    print("📝 下一步:")
    print("1. 確保 LINE Bot 服務正在運行")
    print("2. 在 LINE 中發送測試訊息")
    print("3. 檢查是否顯示為富文本格式")
    print("4. 如果仍有問題，查看服務日誌")

if __name__ == "__main__":
    main() 