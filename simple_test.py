#!/usr/bin/env python3
"""
簡單測試腳本
"""

import os
import sys

def simple_test():
    """簡單測試"""
    print("🧪 簡單測試開始...")
    
    # 1. 檢查 Python
    print(f"✅ Python {sys.version.split()[0]}")
    
    # 2. 檢查套件
    packages = ['fastapi', 'redis', 'google.generativeai']
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except:
            print(f"❌ {pkg}")
    
    # 3. 檢查檔案
    files = ['.env', 'enhanced_m1_m2_m3_integrated_api.py']
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    print("\n🎯 測試完成！")

if __name__ == "__main__":
    simple_test() 