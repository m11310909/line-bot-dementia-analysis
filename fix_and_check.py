#!/usr/bin/env python3
"""
系統檢查和修復腳本
"""

import os
import sys
import subprocess
import json

def run_command(cmd):
    """執行命令並返回結果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_python_environment():
    """檢查 Python 環境"""
    print("🐍 檢查 Python 環境...")
    
    # 檢查 Python 版本
    success, stdout, stderr = run_command("python3 --version")
    if success:
        print(f"✅ Python 版本: {stdout.strip()}")
    else:
        print(f"❌ Python 版本檢查失敗: {stderr}")
    
    # 檢查必要套件
    packages = ['fastapi', 'redis', 'google.generativeai', 'linebot']
    for package in packages:
        success, stdout, stderr = run_command(f"python3 -c 'import {package}; print(\"✅ {package} 已安裝\")'")
        if success:
            print(f"✅ {package} 已安裝")
        else:
            print(f"❌ {package} 未安裝")
            # 嘗試安裝
            print(f"正在安裝 {package}...")
            install_success, _, _ = run_command(f"pip3 install {package}")
            if install_success:
                print(f"✅ {package} 安裝成功")
            else:
                print(f"❌ {package} 安裝失敗")

def check_redis():
    """檢查 Redis 狀態"""
    print("\n🔴 檢查 Redis 狀態...")
    
    # 檢查 Redis 是否運行
    success, stdout, stderr = run_command("brew services list | grep redis")
    if success and "started" in stdout:
        print("✅ Redis 正在運行")
    else:
        print("❌ Redis 未運行")
        print("正在啟動 Redis...")
        start_success, _, _ = run_command("brew services start redis")
        if start_success:
            print("✅ Redis 啟動成功")
        else:
            print("❌ Redis 啟動失敗")

def check_env_file():
    """檢查 .env 檔案"""
    print("\n📝 檢查 .env 檔案...")
    
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        
        # 讀取並檢查憑證
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'your_actual_channel_access_token_here' in content:
            print("❌ LINE Bot 憑證未設置")
        else:
            print("✅ LINE Bot 憑證已設置")
            
        if 'your_actual_gemini_api_key_here' in content:
            print("❌ Gemini API 憑證未設置")
        else:
            print("✅ Gemini API 憑證已設置")
    else:
        print("❌ .env 檔案不存在")
        create_env_file()

def create_env_file():
    """創建 .env 檔案"""
    print("正在創建 .env 檔案...")
    
    env_content = """# LINE Bot 憑證配置
LINE_CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token_here
LINE_CHANNEL_SECRET=your_actual_channel_secret_here

# API 配置
FLEX_API_URL=http://localhost:8005/comprehensive-analysis
RAG_HEALTH_URL=http://localhost:8005/health
RAG_ANALYZE_URL=http://localhost:8005/comprehensive-analysis

# 生產環境配置
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG_MODE=false

# Redis 配置
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# Gemini API 配置
AISTUDIO_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# 監控配置
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env 檔案已創建")
    print("⚠️  請編輯 .env 檔案並填入實際的憑證")

def check_api_status():
    """檢查 API 狀態"""
    print("\n🌐 檢查 API 狀態...")
    
    success, stdout, stderr = run_command("curl -s http://localhost:8005/health")
    if success and stdout:
        print("✅ API 正在運行")
        try:
            response = json.loads(stdout)
            print(f"API 回應: {response}")
        except:
            print(f"API 回應: {stdout}")
    else:
        print("❌ API 未運行")

def main():
    """主函數"""
    print("🔧 系統檢查和修復腳本")
    print("=" * 50)
    
    # 檢查 Python 環境
    check_python_environment()
    
    # 檢查 Redis
    check_redis()
    
    # 檢查 .env 檔案
    check_env_file()
    
    # 檢查 API 狀態
    check_api_status()
    
    print("\n" + "=" * 50)
    print("📋 檢查完成！")
    print("\n🎯 下一步操作：")
    print("1. 編輯 .env 檔案並填入實際憑證")
    print("2. 執行: python3 enhanced_m1_m2_m3_integrated_api.py")
    print("3. 或執行: ./start_simple.sh")

if __name__ == "__main__":
    main() 