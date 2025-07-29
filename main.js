# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from contextlib import asynccontextmanager
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot configuration
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')

if not channel_access_token or not channel_secret:
    logger.error("❌ Missing LINE Bot credentials in environment variables")

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ─── Lifespan handler ────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Dementia Care Bot 已啟動於 port {port}")
    yield
    # Shutdown
    logger.info("👋 Shutting down bot")

# ─── FastAPI app ────────────────────────────────────────────────────
app = FastAPI(
    title="Dementia Care Bot",
    version="1.0.0",
    lifespan=lifespan
)

# ─── 基本 GET 路由 ───────────────────────────────────────────────────
@app.get("/")
async def root():
    return PlainTextResponse("🤖 Dementia Care Bot 正在運行")

# ─── LINE Webhook 路由 ──────────────────────────────────────────────
@app.post("/callback")
async def callback(request: Request):
    # Get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature', '')

    # Get request body as text
    body = await request.body()
    body_str = body.decode('utf-8')

    logger.info(f"Webhook received: {body_str}")

    # Parse body
    try:
        body_data = json.loads(body_str)
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON in request body")
        return PlainTextResponse("OK", status_code=200)

    # Check if events exist
    if 'events' not in body_data or not isinstance(body_data['events'], list):
        logger.error("❌ Bad Request: events not found")
        # Still return 200 to prevent LINE 502 errors
        return PlainTextResponse("OK", status_code=200)

    # Handle webhook body
    try:
        handler.handle(body_str, signature)
        logger.info("✅ Events processed successfully")
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        # Still return 200 to prevent LINE 502 errors
        return PlainTextResponse("OK", status_code=200)
    except Exception as err:
        logger.error(f"❌ Webhook 處理錯誤: {err}")
        # Still return 200 to prevent LINE 502 errors
        return PlainTextResponse("OK", status_code=200)

    return PlainTextResponse("OK", status_code=200)

# ─── 處理文字訊息 ────────────────────────────────────────────────────
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle text message events"""
    try:
        # Create reply message
        reply_text = f"🧠 收到您的訊息:「{event.message.text}」\n\n目前系統正常運作中。"

        # Reply to user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )

        logger.info(f"Replied to message: {event.message.text}")

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        # Error is logged but not raised to ensure 200 response

# ─── Health check endpoint ──────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Dementia Care Bot"
    }

# ─── Run ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)