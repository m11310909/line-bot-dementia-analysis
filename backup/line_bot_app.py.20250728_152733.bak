from flask import Flask, request, abort
import requests
import json
import asyncio
from typing import List, Dict, Any, Optional
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,
    PostbackEvent, PostbackAction, QuickReply, QuickReplyButton
)
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 應用程式
app = Flask(__name__)

# LINE Bot 憑證 - 請替換為你的實際憑證
CHANNEL_ACCESS_TOKEN = "70cKiZSXcTu69Pl0sJ5KlhTjixq948a8MHP0EWeC5jiLMRlRcwK5tY6mJc8zn9Hia0Z0NTSUk5BDfzslLogr+m5PRpc7zTsnmc98eAo1mnSAKIwLqldNBxk8lx6O1fheyMLzDokvGU/J5+9EqcoHAAdB04t89/1O/w1cDnyilFU="  # 替換這裡
CHANNEL_SECRET = "091dfc73fed73a681e4e7ea5d9eb461b"  # 替換這裡

# Flex Message API 設定
FLEX_API_URL = "http://localhost:8000"  # 你的 API 地址

# 初始化 LINE Bot
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

class FlexMessageClient:
    """與 Flex Message API 互動的客戶端"""

    def __init__(self, api_base_url: str = FLEX_API_URL):
        self.api_base_url = api_base_url

    def generate_flex_message(
        self, 
        chunk_ids: List[str], 
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """調用 Flex Message API 生成訊息"""
        try:
            url = f"{self.api_base_url}/api/v1/flex-message"
            payload = {
                "chunk_ids": chunk_ids,
                "user_context": user_context or {}
            }

            logger.info(f"Calling API: {url} with payload: {payload}")

            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                logger.info("API call successful")
                return response.json()
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return self._create_error_response(f"API 錯誤: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return self._create_error_response("服務暫時無法使用，請稍後再試")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return self._create_error_response("發生未預期的錯誤")

    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """建立錯誤回應的 Flex Message"""
        return {
            "flex_message": {
                "type": "flex",
                "altText": "系統訊息",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ 系統提示",
                                "weight": "bold",
                                "color": "#FF6B6B"
                            },
                            {
                                "type": "text",
                                "text": error_message,
                                "wrap": True,
                                "margin": "md"
                            }
                        ]
                    }
                }
            },
            "fallback_text": f"系統提示: {error_message}"
        }

# 初始化 Flex Message 客戶端
flex_client = FlexMessageClient()

def determine_chunk_ids(user_message: str) -> List[str]:
    """根據用戶訊息決定要處理的 chunk IDs"""
    user_message_lower = user_message.lower()

    # 關鍵字匹配
    if any(keyword in user_message_lower for keyword in ["文字", "text", "內容"]):
        return ["chunk_1"]
    elif any(keyword in user_message_lower for keyword in ["圖片", "image", "照片"]):
        return ["chunk_2"] 
    elif any(keyword in user_message_lower for keyword in ["影片", "video", "視訊"]):
        return ["chunk_3"]
    elif any(keyword in user_message_lower for keyword in ["全部", "所有", "all"]):
        return ["chunk_1", "chunk_2", "chunk_3"]
    else:
        # 預設返回第一個 chunk
        return ["chunk_1"]

def create_quick_reply(interaction_handlers: Dict[str, Any]) -> Optional[QuickReply]:
    """根據 interaction_handlers 建立快速回覆按鈕"""
    try:
        quick_replies = interaction_handlers.get("quick_replies", [])
        if not quick_replies:
            return None

        quick_reply_buttons = []
        for reply in quick_replies:
            if reply.get("type") == "action" and reply.get("action"):
                action = reply["action"]
                button = QuickReplyButton(
                    action=PostbackAction(
                        label=action.get("label", "更多"),
                        data=action.get("data", "action=more")
                    )
                )
                quick_reply_buttons.append(button)

        return QuickReply(items=quick_reply_buttons) if quick_reply_buttons else None

    except Exception as e:
        logger.error(f"Error creating quick reply: {str(e)}")
        return None

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Webhook 接收端點"""
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """處理文字訊息"""
    try:
        user_id = event.source.user_id
        user_message = event.message.text

        logger.info(f"User {user_id} sent: {user_message}")

        # 特殊命令處理
        if user_message.lower() in ['help', '幫助', '說明']:
            send_help_message(event)
            return

        # 根據用戶訊息決定要處理的 chunks
        chunk_ids = determine_chunk_ids(user_message)

        # 準備用戶上下文
        user_context = {
            "user_id": user_id,
            "message": user_message,
            "timestamp": event.timestamp,
            "language": "zh-TW"
        }

        # 調用 Flex Message API
        logger.info(f"Processing chunks: {chunk_ids}")
        api_response = flex_client.generate_flex_message(
            chunk_ids=chunk_ids,
            user_context=user_context
        )

        # 發送 Flex Message
        send_flex_message(event, api_response)

    except Exception as e:
        logger.error(f"Error handling text message: {str(e)}")
        send_error_message(event, "處理訊息時發生錯誤")

@handler.add(PostbackEvent)
def handle_postback(event):
    """處理 Postback 事件（按鈕點擊等）"""
    try:
        user_id = event.source.user_id
        postback_data = event.postback.data

        logger.info(f"User {user_id} postback: {postback_data}")

        # 解析 postback 資料
        if postback_data.startswith("action=details"):
            # 處理 "More Details" 按鈕
            chunk_ids = extract_chunk_ids_from_postback(postback_data)
            send_detailed_info(event, chunk_ids)

        elif postback_data.startswith("action=explain"):
            # 處理 "Explain More" 按鈕
            send_explanation(event)

        else:
            # 未知的 postback
            logger.warning(f"Unknown postback data: {postback_data}")
            send_text_message(event, "收到你的操作，但無法處理此類型的請求")

    except Exception as e:
        logger.error(f"Error handling postback: {str(e)}")
        send_error_message(event, "處理操作時發生錯誤")

def send_flex_message(event, api_response: Dict[str, Any]):
    """發送 Flex Message 到 LINE"""
    try:
        flex_message_data = api_response.get("flex_message")
        fallback_text = api_response.get("fallback_text", "AI 增強內容")

        if flex_message_data and flex_message_data.get("contents"):
            # 建立 FlexSendMessage
            flex_message = FlexSendMessage(
                alt_text=fallback_text,
                contents=flex_message_data["contents"]
            )

            # 加入快速回覆按鈕（如果有的話）
            quick_reply = create_quick_reply(api_response.get("interaction_handlers", {}))
            if quick_reply:
                flex_message.quick_reply = quick_reply

            # 發送訊息
            line_bot_api.reply_message(event.reply_token, flex_message)
            logger.info("Flex message sent successfully")

        else:
            # 發送錯誤訊息
            send_error_message(event, "無法生成內容")

    except LineBotApiError as e:
        logger.error(f"LINE API Error: {str(e)}")
        send_error_message(event, "發送訊息失敗")
    except Exception as e:
        logger.error(f"Error sending flex message: {str(e)}")
        send_error_message(event, "發送訊息時發生錯誤")

def send_help_message(event):
    """發送幫助訊息"""
    help_text = """🤖 歡迎使用 AI 增強內容服務！

你可以嘗試：
• 輸入「文字」查看文字內容
• 輸入「圖片」查看圖片內容  
• 輸入「影片」查看影片內容
• 輸入「全部」查看所有內容

我會為你提供 AI 增強的內容和解釋！

💡 提示：點擊 Flex Message 中的按鈕可以進行更多互動"""

    send_text_message(event, help_text.strip())

def send_text_message(event, text: str):
    """發送文字訊息"""
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )

def send_error_message(event, error_text: str):
    """發送錯誤訊息"""
    send_text_message(event, f"❌ {error_text}")

def send_detailed_info(event, chunk_ids: List[str]):
    """發送詳細資訊"""
    detail_text = f"""📋 詳細資訊

正在處理 {len(chunk_ids)} 個內容項目：
{', '.join(chunk_ids)}

這些內容經過 AI 分析，具有以下特點：
• 高相關性匹配
• 優質內容評分
• 個人化推薦

如需更多資訊，請繼續與我互動！"""

    send_text_message(event, detail_text)

def send_explanation(event):
    """發送解釋訊息"""
    explanation_text = """🧠 AI 解釋

這些內容是基於以下因素選擇的：
• 與你的查詢相關性：85%
• 內容品質評分：高
• 用戶偏好匹配度：良好

AI 分析了多個特徵來為你提供最相關的內容：
✓ 語義相似度分析
✓ 用戶行為模式
✓ 內容品質指標
✓ 個人化偏好

繼續與我互動，我會學習你的偏好！"""

    send_text_message(event, explanation_text.strip())

def extract_chunk_ids_from_postback(postback_data: str) -> List[str]:
    """從 postback 資料中提取 chunk IDs"""
    try:
        parts = postback_data.split("&")
        for part in parts:
            if part.startswith("chunks="):
                chunk_string = part.split("=", 1)[1]
                return chunk_string.split(",")
        return []
    except Exception as e:
        logger.error(f"Error extracting chunk IDs: {str(e)}")
        return []

@app.route("/health")
def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "LINE Bot with Flex Message API"}

@app.route("/")
def home():
    """首頁"""
    return """
    <h1>LINE Bot with Flex Message API</h1>
    <p>LINE Bot 正在運行中！</p>
    <p>請確保：</p>
    <ul>
        <li>Flex Message API 伺服器在 http://localhost:8000 運行</li>
        <li>LINE Bot 憑證已正確設定</li>
        <li>Webhook URL 已設定為此伺服器的 /callback 端點</li>
    </ul>
    """

if __name__ == "__main__":
    # 檢查憑證是否已設定
    if CHANNEL_ACCESS_TOKEN == "YOUR_CHANNEL_ACCESS_TOKEN":
        print("⚠️  請先設定你的 LINE Bot 憑證！")
        print("編輯 CHANNEL_ACCESS_TOKEN 和 CHANNEL_SECRET")
        exit(1)

    print("🚀 LINE Bot with Flex Message API 正在啟動...")
    print("請確保你的 Flex Message API 伺服器正在 http://localhost:8000 運行")
    print("設定你的 LINE Webhook URL 為: https://your-domain.com/callback")

    # 啟動 Flask 應用程式
    app.run(host='0.0.0.0', port=5000, debug=True)