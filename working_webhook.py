#!/usr/bin/env python3
"""
Fixed LINE Bot Webhook Service for Dementia Analysis
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage, FollowEvent
import requests
import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Webhook - Fixed Edition",
    description="Working webhook for LINE Bot dementia analysis",
    version="3.0.0"
)

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
AISTUDIO_API_KEY = os.getenv('AISTUDIO_API_KEY')

# RAG API configuration
RAG_API_BASE = "http://localhost:8004"
RAG_HEALTH_URL = f"{RAG_API_BASE}/health"
RAG_ANALYZE_URL = f"{RAG_API_BASE}/m1-flex"  # Use the working endpoint

# Replit configuration
REPL_SLUG = os.getenv('REPL_SLUG', 'workspace')
REPL_OWNER = os.getenv('REPL_OWNER', 'ke2211975')

# Initialize LINE Bot
line_bot_api = None
handler = None

if LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET:
    try:
        line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(LINE_CHANNEL_SECRET)
        logger.info("✅ LINE Bot API initialized successfully")
    except Exception as e:
        logger.error(f"❌ LINE Bot initialization failed: {e}")
else:
    logger.error("❌ Missing LINE Bot credentials")

@app.get("/")
async def root():
    """Root endpoint"""
    public_url = f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co"
    return {
        "message": "LINE Bot Webhook - Fixed Edition",
        "status": "running",
        "line_bot_ready": line_bot_api is not None,
        "rag_api_url": RAG_API_BASE,
        "webhook_url": f"{public_url}/webhook"
    }

@app.get("/health")
async def health_check():
    """Health check"""
    health_status = {
        "status": "healthy",
        "services": {}
    }

    # Check LINE Bot
    try:
        if line_bot_api:
            bot_info = line_bot_api.get_bot_info()
            health_status["services"]["line_bot"] = {
                "status": "ok",
                "bot_id": bot_info.user_id
            }
        else:
            health_status["services"]["line_bot"] = {"status": "not_configured"}
    except Exception as e:
        health_status["services"]["line_bot"] = {"status": "error", "error": str(e)}

    # Check RAG API
    try:
        response = requests.get(RAG_HEALTH_URL, timeout=5)
        if response.status_code == 200:
            health_status["services"]["rag_api"] = {"status": "ok"}
        else:
            health_status["services"]["rag_api"] = {"status": "error"}
    except Exception as e:
        health_status["services"]["rag_api"] = {"status": "error", "error": str(e)}

    return health_status

def call_rag_api(user_input: str) -> Optional[Dict[str, Any]]:
    """Call RAG API and return response"""
    try:
        logger.info(f"🔄 Calling RAG API with: {user_input}")
        
        response = requests.post(
            RAG_ANALYZE_URL,
            json={"user_input": user_input},
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"📊 RAG API response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ RAG API returned valid response")
            return result
        else:
            logger.error(f"❌ RAG API error: {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"❌ RAG API call failed: {e}")
        return None

@app.post("/webhook")
async def webhook(request: Request):
    """LINE webhook endpoint"""
    try:
        body = await request.body()
        signature = request.headers.get('X-Line-Signature', '')
        
        if not handler:
            raise HTTPException(status_code=500, detail="Handler not configured")
        
        handler.handle(body.decode('utf-8'), signature)
        return JSONResponse(content={"status": "ok"})
        
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Event handlers
if handler and line_bot_api:
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        try:
            user_text = event.message.text.strip()
            reply_token = event.reply_token

            logger.info(f"👤 Message received: {user_text}")

            # Handle help commands
            if user_text.lower() in ['help', '幫助', 'start', '開始']:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="🧠 歡迎使用失智症警訊分析助手！\n\n請描述您觀察到的行為變化，我會協助分析是否為失智症警訊。\n\n範例：「奶奶經常迷路」")
                )
                return

            # Call RAG API for analysis
            rag_response = call_rag_api(user_text)
            
            if rag_response and "flex_message" in rag_response:
                # Extract flex message content
                flex_contents = rag_response["flex_message"]["contents"]
                alt_text = rag_response["flex_message"].get("altText", "失智症警訊分析結果")
                
                # Create and send flex message
                flex_message = FlexSendMessage(
                    alt_text=alt_text,
                    contents=flex_contents
                )
                
                line_bot_api.reply_message(reply_token, flex_message)
                logger.info(f"✅ Sent analysis result for: {user_text}")
                
            else:
                # Fallback response
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="抱歉，分析服務暫時無法使用。請稍後再試或直接諮詢專業醫師。")
                )
                logger.warning(f"⚠️ RAG API failed, sent fallback message")

        except Exception as e:
            logger.error(f"❌ Message handler error: {e}")
            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="系統發生錯誤，請稍後再試。")
                )
            except:
                pass

    @handler.add(FollowEvent)
    def handle_follow(event):
        """Handle when user follows the bot"""
        try:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="🧠 歡迎使用失智症警訊分析助手！\n\n請描述您觀察到的行為變化，我會協助分析是否為失智症警訊。")
            )
            logger.info("✅ Sent welcome message to new follower")
        except Exception as e:
            logger.error(f"❌ Follow handler error: {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 3000))
    
    print("🚀 Starting LINE Bot Webhook...")
    print(f"📍 RAG API: {RAG_API_BASE}")
    print(f"📍 Webhook Port: {port}")
    print(f"📍 LINE Bot Ready: {line_bot_api is not None}")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
