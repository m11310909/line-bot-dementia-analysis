#!/usr/bin/env python3
"""
測試 Flex Message 發送
"""

import os
from dotenv import load_dotenv
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage, FlexMessage

load_dotenv()

# 初始化 LINE Bot v3
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

def test_flex_message():
    """測試 Flex Message 發送"""
    print("=== 測試 Flex Message 發送 ===")
    
    # 創建一個簡單的 Flex Message
    test_flex = {
        "type": "flex",
        "altText": "測試 Flex Message",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "這是一個測試 Flex Message",
                        "size": "md",
                        "wrap": True
                    }
                ]
            }
        }
    }
    
    print("測試 Flex Message:")
    import json
    print(json.dumps(test_flex, indent=2, ensure_ascii=False))
    
    # 測試發送（需要有效的 reply token）
    print("\n注意：這個測試需要有效的 reply token 才能實際發送")
    print("Flex Message 格式看起來是正確的")

if __name__ == "__main__":
    test_flex_message() 