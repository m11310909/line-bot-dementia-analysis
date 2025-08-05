#!/usr/bin/env python3
"""
LINE Bot Webhook Service - Enhanced RAG v2.0
Optimized for Replit with RAG API integration
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage, FollowEvent
import requests
import os
import logging
import traceback
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Webhook - Enhanced RAG v2.0",
    description="LINE Bot with RAG integration for dementia analysis",
    version="2.0.0"
)

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# RAG API URLs (updated to port 8002)
FLEX_API_URL = 'http://localhost:8002/m1-flex'
RAG_HEALTH_URL = 'http://localhost:8002/health'

# Replit config
REPL_SLUG = os.getenv('REPL_SLUG', 'workspace')
REPL_OWNER = os.getenv('REPL_OWNER', 'runner')

# Initialize LINE Bot
line_bot_api = None
handler = None

if LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET:
    try:
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(LINE_CHANNEL_SECRET)
        logger.info("✅ LINE Bot API initialized")
    except Exception as e:
        logger.error(f"❌ LINE Bot initialization failed: {e}")
else:
    logger.warning("⚠️  LINE Bot credentials not found - will run in demo mode")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LINE Bot Webhook - Enhanced RAG v2.0",
        "status": "running",
        "line_bot_ready": line_bot_api is not None,
        "rag_api_url": FLEX_API_URL,
        "version": "2.0.0",
        "features": [
            "🧠 RAG Enhanced Analysis",
            "🔍 Semantic Search",
            "📊 Confidence Scoring",
            "💡 Multi-chunk Analysis"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check with RAG status"""
    health = {
        "status": "healthy",
        "services": {},
        "timestamp": "2025-07-25T14:30:00Z"
    }

    # Check LINE Bot
    if line_bot_api:
        try:
            bot_info = line_bot_api.get_bot_info()
            health["services"]["line_bot"] = {
                "status": "ok",
                "bot_id": bot_info.user_id,
                "display_name": bot_info.display_name
            }
        except Exception as e:
            health["services"]["line_bot"] = {"status": "error", "error": str(e)}
    else:
        health["services"]["line_bot"] = {"status": "not_configured"}

    # Check RAG API
    try:
        response = requests.get(RAG_HEALTH_URL, timeout=5)
        if response.status_code == 200:
            rag_health = response.json()
            health["services"]["rag_api"] = {
                "status": "ok",
                "components": rag_health.get("components", {}),
                "version": rag_health.get("version", "unknown")
            }
        else:
            health["services"]["rag_api"] = {"status": "error", "http_status": response.status_code}
    except Exception as e:
        health["services"]["rag_api"] = {"status": "error", "error": str(e)}

    return health

@app.get("/rag-status")
async def rag_status():
    """RAG specific status"""
    try:
        response = requests.get(RAG_HEALTH_URL, timeout=5)
        if response.status_code == 200:
            return {
                "rag_status": "healthy",
                "details": response.json(),
                "api_url": FLEX_API_URL
            }
        else:
            return {"rag_status": "error", "http_status": response.status_code}
    except Exception as e:
        return {"rag_status": "error", "error": str(e)}

@app.post("/webhook")
async def webhook(request: Request):
    """Main LINE webhook endpoint"""
    try:
        logger.info("📨 Webhook request received")

        if not handler or not line_bot_api:
            return JSONResponse(
                status_code=500,
                content={"error": "LINE Bot not configured"}
            )

        body = await request.body()
        signature = request.headers.get('X-Line-Signature', '')

        if not signature:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing signature"}
            )

        try:
            body_str = body.decode('utf-8')
            handler.handle(body_str, signature)
            return {"status": "ok"}
        except InvalidSignatureError:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid signature"}
            )
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

def create_welcome_message():
    """Create welcome Flex message"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "🧠 AI 失智症警訊分析",
                "weight": "bold",
                "size": "lg",
                "color": "#ffffff"
            }],
            "backgroundColor": "#005073",
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "歡迎使用 RAG 增強版分析！",
                    "weight": "bold",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "🆕 v2.0 新功能：\n• 🔍 智能語義檢索\n• 📊 信心度評估\n• 💡 多資料源分析",
                    "wrap": True,
                    "size": "sm",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "💡 使用方式：\n直接描述行為變化\n\n範例：媽媽最近常忘記關瓦斯",
                    "wrap": True,
                    "size": "sm"
                }
            ],
            "paddingAll": "20px"
        }
    }

def call_rag_api(user_input: str):
    """Call RAG API"""
    try:
        logger.info(f"🔄 Calling RAG API: {user_input}")

        response = requests.post(
            FLEX_API_URL,
            json={"user_input": user_input},
            timeout=30,
            headers={"Content-Type": "application/json"}
        )

        logger.info(f"📊 RAG API response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # Log RAG info
            if "rag_info" in result:
                rag_info = result["rag_info"]
                logger.info(f"🧠 RAG: method={rag_info.get('analysis_method')}, "
                           f"chunks={rag_info.get('chunks_used')}, "
                           f"similarity={rag_info.get('top_similarity', 0):.3f}")

            return result
        else:
            logger.error(f"❌ RAG API error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"❌ RAG API error: {e}")
        return None

# Event handlers
if handler and line_bot_api:
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        """Handle text messages"""
        try:
            user_id = event.source.user_id
            user_text = event.message.text.strip()
            reply_token = event.reply_token

            logger.info(f"👤 Message from {user_id}: {user_text}")

            # Handle commands
            if user_text.lower() in ['help', '幫助', 'start', '開始', 'v2']:
                welcome_flex = create_welcome_message()
                flex_message = FlexSendMessage(
                    alt_text="使用說明",
                    contents=welcome_flex
                )
                line_bot_api.reply_message(reply_token, flex_message)
                return

            # Input validation
            if len(user_text) < 5:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="請提供更詳細的描述（至少5個字）\n\n💡 範例：\n• 媽媽最近常忘記關瓦斯\n• 爸爸重複問同樣問題"
                    )
                )
                return

            if len(user_text) > 1000:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="描述過長，請簡化在1000字以內")
                )
                return

            # Call RAG API
            rag_response = call_rag_api(user_text)

            if rag_response and "flex_message" in rag_response:
                # Extract Flex message from RAG response
                flex_contents = rag_response["flex_message"]["contents"]
                alt_text = rag_response["flex_message"].get("altText", "失智症警訊分析結果")

                flex_message = FlexSendMessage(
                    alt_text=alt_text,
                    contents=[flex_contents]  # Wrap in array as LINE expects
                )

                line_bot_api.reply_message(reply_token, flex_message)

                # Enhanced logging
                analysis_data = rag_response.get("analysis_data", {})
                logger.info(f"✅ Analysis sent: "
                           f"code={analysis_data.get('matched_warning_code')}, "
                           f"confidence={analysis_data.get('confidence_level')}")
            else:
                # Error response
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="抱歉，AI 分析服務暫時無法使用，請稍後再試或諮詢專業醫師。\n\n如需協助，請輸入「幫助」查看使用說明。"
                    )
                )
                logger.warning(f"⚠️ Sent error message to {user_id}")

        except LineBotApiError as e:
            logger.error(f"❌ LINE Bot API error: {e}")
        except Exception as e:
            logger.error(f"❌ Message handler error: {e}")
            logger.error(traceback.format_exc())

    @handler.add(FollowEvent)
    def handle_follow(event):
        """Handle new followers"""
        try:
            user_id = event.source.user_id
            reply_token = event.reply_token
            logger.info(f"👋 New follower: {user_id}")

            welcome_flex = create_welcome_message()
            flex_message = FlexSendMessage(
                alt_text="歡迎使用 AI 失智症警訊分析",
                contents=welcome_flex
            )
            line_bot_api.reply_message(reply_token, flex_message)

        except LineBotApiError as e:
            logger.error(f"❌ Follow handler error: {e}")

@app.get("/info")
async def bot_info():
    """Bot information"""
    if not line_bot_api:
        raise HTTPException(status_code=500, detail="LINE Bot not configured")

    try:
        bot_info = line_bot_api.get_bot_info()
        return {
            "bot_id": bot_info.user_id,
            "display_name": bot_info.display_name,
            "status": "active",
            "version": "2.0.0",
            "rag_enhanced": True,
            "rag_api_url": FLEX_API_URL
        }
    except LineBotApiError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
async def ping():
    """Keep alive"""
    return {"status": "pong", "version": "2.0.0", "rag_enhanced": True}

@app.post("/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "LINE Bot v2.0 test",
        "line_bot_ready": line_bot_api is not None,
        "rag_api_url": FLEX_API_URL,
        "features": ["RAG", "Semantic Search", "Confidence Scoring"]
    }

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Enhanced LINE Bot v2.0...")
    print("=" * 50)
    print(f"LINE Bot: {'✅' if line_bot_api else '❌'}")
    print(f"RAG API: {FLEX_API_URL}")
    print("=" * 50)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        log_level="info"
    )