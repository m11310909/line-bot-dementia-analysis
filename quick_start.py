#!/usr/bin/env python3
"""
快速啟動腳本
"""

import os
import subprocess
import sys
import time

def run_command(cmd, background=False):
    """執行命令"""
    try:
        if background:
            subprocess.Popen(cmd, shell=True)
            return True
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
    except Exception as e:
        print(f"❌ 命令執行失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 快速啟動腳本")
    print("=" * 40)
    
    # 1. 檢查並安裝必要套件
    print("📦 檢查 Python 套件...")
    packages = [
        "fastapi",
        "uvicorn", 
        "pydantic",
        "aiohttp",
        "python-multipart",
        "python-jose",
        "redis",
        "google-generativeai",
        "line-bot-sdk"
    ]
    
    for package in packages:
        print(f"檢查 {package}...")
        success = run_command(f"python3 -c 'import {package.replace(\"-\", \"_\")}; print(\"✅ {package} 已安裝\")'")
        if not success:
            print(f"安裝 {package}...")
            run_command(f"pip3 install {package}")
    
    # 2. 啟動 Redis
    print("\n🔴 啟動 Redis...")
    run_command("brew services start redis")
    time.sleep(2)
    
    # 3. 檢查 .env 檔案
    print("\n📝 檢查 .env 檔案...")
    if not os.path.exists('.env'):
        print("創建 .env 檔案...")
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
    else:
        print("✅ .env 檔案已存在")
    
    # 4. 啟動 API
    print("\n🌐 啟動 API...")
    print("正在啟動 enhanced_m1_m2_m3_integrated_api.py...")
    
    # 檢查 API 檔案是否存在
    if os.path.exists('enhanced_m1_m2_m3_integrated_api.py'):
        print("✅ 找到 API 檔案")
        print("🚀 啟動中...")
        print("按 Ctrl+C 停止")
        
        # 啟動 API
        run_command("python3 enhanced_m1_m2_m3_integrated_api.py", background=False)
    else:
        print("❌ 找不到 enhanced_m1_m2_m3_integrated_api.py")
        print("嘗試啟動 m1_m2_m3_integrated_api.py...")
        if os.path.exists('m1_m2_m3_integrated_api.py'):
            run_command("python3 m1_m2_m3_integrated_api.py", background=False)
        else:
            print("❌ 找不到任何 API 檔案")

if __name__ == "__main__":
    main() 