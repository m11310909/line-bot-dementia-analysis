#!/usr/bin/env python3
"""
設置 ngrok 來暴露 Webhook
"""

import os
import subprocess
import time
import requests
import json

def check_ngrok_installed():
    """檢查 ngrok 是否已安裝"""
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok 已安裝")
            return True
        else:
            print("❌ ngrok 未安裝")
            return False
    except FileNotFoundError:
        print("❌ ngrok 未安裝")
        return False

def install_ngrok():
    """安裝 ngrok"""
    print("📦 安裝 ngrok...")
    
    try:
        # 使用 Homebrew 安裝 ngrok
        subprocess.run(['brew', 'install', 'ngrok'], check=True)
        print("✅ ngrok 安裝成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 使用 Homebrew 安裝失敗")
        
        # 嘗試手動下載
        print("📥 嘗試手動下載 ngrok...")
        try:
            # 下載 ngrok
            subprocess.run(['curl', '-O', 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.tgz'], check=True)
            subprocess.run(['tar', '-xzf', 'ngrok-v3-stable-darwin-amd64.tgz'], check=True)
            subprocess.run(['sudo', 'mv', 'ngrok', '/usr/local/bin/'], check=True)
            subprocess.run(['rm', 'ngrok-v3-stable-darwin-amd64.tgz'], check=True)
            print("✅ ngrok 手動安裝成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 手動安裝失敗: {e}")
            return False

def check_api_running():
    """檢查 API 是否在運行"""
    try:
        response = requests.get('http://localhost:8005/health', timeout=5)
        if response.status_code == 200:
            print("✅ API 正在運行 (端口 8005)")
            return True
        else:
            print("❌ API 未正常運行")
            return False
    except requests.exceptions.RequestException:
        print("❌ API 未運行或端口被佔用")
        return False

def start_ngrok():
    """啟動 ngrok"""
    print("🚀 啟動 ngrok...")
    
    try:
        # 啟動 ngrok，暴露端口 8005
        process = subprocess.Popen(
            ['ngrok', 'http', '8005'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待 ngrok 啟動
        time.sleep(3)
        
        # 獲取 ngrok 的公共 URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"✅ ngrok 啟動成功")
                    print(f"🌐 公共 URL: {public_url}")
                    print(f"🔗 Webhook URL: {public_url}/webhook")
                    return public_url
                else:
                    print("❌ 無法獲取 ngrok URL")
                    return None
            else:
                print("❌ 無法連接到 ngrok API")
                return None
        except requests.exceptions.RequestException:
            print("❌ 無法獲取 ngrok URL")
            return None
            
    except Exception as e:
        print(f"❌ 啟動 ngrok 失敗: {e}")
        return None

def create_webhook_config(webhook_url):
    """創建 Webhook 配置說明"""
    print("\n📋 Webhook 配置說明:")
    print("=" * 50)
    print(f"1. 登入 LINE Developers Console")
    print(f"2. 選擇您的 Channel")
    print(f"3. 進入 'Messaging API' 設定")
    print(f"4. 在 'Webhook URL' 欄位填入:")
    print(f"   {webhook_url}/webhook")
    print(f"5. 開啟 'Use webhook' 選項")
    print(f"6. 點擊 'Verify' 按鈕測試連接")
    print("=" * 50)

def save_webhook_info(webhook_url):
    """保存 Webhook 資訊"""
    info = {
        "webhook_url": f"{webhook_url}/webhook",
        "api_url": webhook_url,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open('webhook_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"💾 Webhook 資訊已保存到 webhook_info.json")

def main():
    """主函數"""
    print("🌐 ngrok Webhook 設置工具")
    print("=" * 40)
    
    # 檢查 ngrok 是否已安裝
    if not check_ngrok_installed():
        print("\n📦 正在安裝 ngrok...")
        if not install_ngrok():
            print("❌ ngrok 安裝失敗")
            return
    
    # 檢查 API 是否在運行
    print("\n🔍 檢查 API 狀態...")
    if not check_api_running():
        print("⚠️  API 未運行，請先啟動 API:")
        print("python3 enhanced_m1_m2_m3_integrated_api.py")
        return
    
    # 啟動 ngrok
    print("\n🚀 啟動 ngrok...")
    webhook_url = start_ngrok()
    
    if webhook_url:
        # 創建配置說明
        create_webhook_config(webhook_url)
        
        # 保存資訊
        save_webhook_info(webhook_url)
        
        print(f"\n✅ 設置完成！")
        print(f"📝 請將 Webhook URL 設定到 LINE Developers Console")
        print(f"🔗 Webhook URL: {webhook_url}/webhook")
    else:
        print("❌ ngrok 啟動失敗")

if __name__ == "__main__":
    main() 