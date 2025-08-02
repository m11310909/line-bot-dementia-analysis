#!/usr/bin/env python3
"""
Dockerized LINE Bot Webhook Service
Enhanced for microservices architecture with ngrok support
"""

import os
import logging
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage, FollowEvent, PostbackEvent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/line-bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Webhook - Dockerized",
    description="Microservices-based LINE Bot for dementia analysis",
    version="3.0.0"
)

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
XAI_API_URL = os.getenv('XAI_API_URL', 'http://xai-analysis:8005')
RAG_API_URL = os.getenv('RAG_API_URL', 'http://rag-service:8006')
EXTERNAL_URL = os.getenv('EXTERNAL_URL', 'http://localhost:8081')

# Initialize LINE Bot API
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
    logger.error("❌ Missing LINE Bot credentials")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LINE Bot Webhook Service - Dockerized",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "external_url": EXTERNAL_URL,
        "webhook_url": f"{EXTERNAL_URL}/webhook",
        "services": {
            "xai_analysis": XAI_API_URL,
            "rag_service": RAG_API_URL
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check XAI Analysis service
        xai_health = requests.get(f"{XAI_API_URL}/health", timeout=5)
        xai_status = "healthy" if xai_health.status_code == 200 else "unhealthy"
        
        # Check RAG service
        rag_health = requests.get(f"{RAG_API_URL}/health", timeout=5)
        rag_status = "healthy" if rag_health.status_code == 200 else "unhealthy"
        
        return {
            "status": "healthy",
            "line_bot": "initialized" if line_bot_api else "not_initialized",
            "xai_analysis": xai_status,
            "rag_service": rag_status,
            "external_url": EXTERNAL_URL,
            "webhook_url": f"{EXTERNAL_URL}/webhook",
            "timestamp": "2025-08-02T12:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.get("/webhook-url")
async def get_webhook_url():
    """Get current webhook URL for LINE Developer Console"""
    return {
        "webhook_url": f"{EXTERNAL_URL}/webhook",
        "external_url": EXTERNAL_URL,
        "note": "Update this URL in LINE Developer Console"
    }

@app.post("/webhook")
async def webhook(request: Request):
    """LINE Bot webhook endpoint"""
    try:
        body = await request.body()
        signature = request.headers.get('X-Line-Signature', '')
        
        logger.info("📨 Webhook request received")
        
        # Verify signature
        try:
            handler.handle(body.decode('utf-8'), signature)
        except InvalidSignatureError:
            logger.error("❌ Invalid LINE signature")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        return JSONResponse(content={"status": "success"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def create_error_flex_message(error_msg: str):
    """Create error flex message"""
    return {
        "type": "flex",
        "altText": "系統暫時無法使用",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ 系統暫時無法使用",
                        "weight": "bold",
                        "color": "#FF0000"
                    },
                    {
                        "type": "text",
                        "text": error_msg,
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            }
        }
    }

def call_xai_analysis(user_input: str):
    """Call XAI Analysis service"""
    try:
        response = requests.post(
            f"{XAI_API_URL}/comprehensive-analysis",
            json={"text": user_input},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"XAI Analysis error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"XAI Analysis call failed: {e}")
        return None

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle text messages"""
    try:
        user_input = event.message.text
        user_id = event.source.user_id
        reply_token = event.reply_token
        
        logger.info(f"👤 Message from {user_id}: {user_input}")
        
        # Call XAI Analysis service
        analysis_result = call_xai_analysis(user_input)
        
        if analysis_result:
            # Create flex message from analysis result
            flex_message = create_analysis_flex_message(analysis_result)
            line_bot_api.reply_message(reply_token, FlexSendMessage(**flex_message))
            logger.info("✅ Message sent successfully")
        else:
            # Send error message
            error_message = create_error_flex_message("分析服務暫時無法使用，請稍後再試")
            line_bot_api.reply_message(reply_token, FlexSendMessage(**error_message))
            logger.error("❌ Failed to get analysis result")
            
    except LineBotApiError as e:
        logger.error(f"LINE Bot API error: {e}")
    except Exception as e:
        logger.error(f"Message handling error: {e}")

def create_analysis_flex_message(analysis_result):
    """Create flex message from analysis result"""
    # This is a simplified version - you can enhance this based on your needs
    return {
        "type": "flex",
        "altText": "分析結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 智能分析結果",
                        "weight": "bold",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": analysis_result.get("summary", "分析完成"),
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            }
        }
    }

@handler.add(FollowEvent)
def handle_follow(event):
    """Handle follow events"""
    try:
        user_id = event.source.user_id
        welcome_message = create_welcome_flex_message()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(**welcome_message))
        logger.info(f"👋 Welcome message sent to {user_id}")
    except Exception as e:
        logger.error(f"Follow event error: {e}")

def create_welcome_flex_message():
    """Create welcome flex message"""
    return {
        "type": "flex",
        "altText": "歡迎使用失智症照護助手",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症照護助手",
                        "weight": "bold",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "歡迎使用！我可以協助您：",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "• 評估失智症警訊\n• 了解病程發展\n• 處理行為症狀\n• 導航照護資源",
                        "wrap": True,
                        "margin": "sm"
                    }
                ]
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081) 