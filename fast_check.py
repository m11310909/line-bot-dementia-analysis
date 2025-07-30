#!/usr/bin/env python3
"""
快速檢查腳本 - 只做最基本的檢查
"""

import os
import sys

def quick_check():
    """快速檢查"""
    print("⚡ 快速檢查開始...")
    
    # 1. 檢查 Python 版本
    print(f"🐍 Python 版本: {sys.version}")
    
    # 2. 檢查必要套件
    print("\n📦 檢查套件...")
    packages = ['fastapi', 'redis', 'google.generativeai']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安裝")
        except ImportError:
            print(f"❌ {package} 未安裝")
    
    # 3. 檢查 .env 檔案
    print("\n📝 檢查 .env 檔案...")
    if os.path.exists('.env'):
        print("✅ .env 檔案存在")
        with open('.env', 'r') as f:
            content = f.read()
            if 'your_actual_channel_access_token_here' in content:
                print("❌ LINE Bot 憑證未設置")
            else:
                print("✅ LINE Bot 憑證已設置")
    else:
        print("❌ .env 檔案不存在")
    
    # 4. 檢查 API 檔案
    print("\n🌐 檢查 API 檔案...")
    api_files = ['enhanced_m1_m2_m3_integrated_api.py', 'm1_m2_m3_integrated_api.py']
    for api_file in api_files:
        if os.path.exists(api_file):
            print(f"✅ {api_file} 存在")
            break
    else:
        print("❌ 找不到 API 檔案")
    
    print("\n🎯 快速檢查完成！")
    print("下一步：python3 enhanced_m1_m2_m3_integrated_api.py")

if __name__ == "__main__":
    quick_check() 