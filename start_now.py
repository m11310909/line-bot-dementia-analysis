#!/usr/bin/env python3
"""
直接啟動腳本 - 立即啟動 API
"""

import os
import subprocess
import sys

def start_api():
    """直接啟動 API"""
    print("🚀 直接啟動 API...")
    
    # 檢查 API 檔案
    api_files = ['enhanced_m1_m2_m3_integrated_api.py', 'm1_m2_m3_integrated_api.py']
    
    for api_file in api_files:
        if os.path.exists(api_file):
            print(f"✅ 找到 {api_file}")
            print("🚀 正在啟動...")
            print("按 Ctrl+C 停止")
            
            try:
                # 直接執行 API
                subprocess.run([sys.executable, api_file])
            except KeyboardInterrupt:
                print("\n⏹️  已停止")
            except Exception as e:
                print(f"❌ 啟動失敗: {e}")
            return
    
    print("❌ 找不到任何 API 檔案")

if __name__ == "__main__":
    start_api() 