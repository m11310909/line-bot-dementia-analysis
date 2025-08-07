#!/usr/bin/env python3
"""
測試 LINE Bot 配置
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_line_bot_config():
    """測試 LINE Bot 配置"""
    print("🔍 檢查 LINE Bot 配置...")
    
    # 檢查環境變數
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    channel_secret = os.getenv("LINE_CHANNEL_SECRET")
    
    print(f"📋 環境變數檢查:")
    print(f"   LINE_CHANNEL_ACCESS_TOKEN: {'✅ 已設置' if channel_access_token else '❌ 未設置'}")
    print(f"   LINE_CHANNEL_SECRET: {'✅ 已設置' if channel_secret else '❌ 未設置'}")
    
    if not channel_access_token:
        print("\n❌ LINE_CHANNEL_ACCESS_TOKEN 未設置")
        print("請在 .env 文件中設置:")
        print("LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here")
    
    if not channel_secret:
        print("\n❌ LINE_CHANNEL_SECRET 未設置")
        print("請在 .env 文件中設置:")
        print("LINE_CHANNEL_SECRET=your_channel_secret_here")
    
    if channel_access_token and channel_secret:
        print("\n✅ LINE Bot 配置完整")
        print("可以啟動 LINE Bot 服務")
    else:
        print("\n❌ LINE Bot 配置不完整")
        print("請設置必要的環境變數後再啟動服務")

if __name__ == "__main__":
    test_line_bot_config() 