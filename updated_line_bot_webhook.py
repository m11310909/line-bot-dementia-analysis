#!/usr/bin/env python3
"""
LINE Bot Webhook Service - Updated for RAG Integration
Optimized for running on Replit with enhanced M1 RAG API communication
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

# Create FastAPI app instance
app = FastAPI(
    title="LINE Bot Webhook - Enhanced RAG Edition",
    description="Webhook for LINE Bot dementia warning analysis with RAG on Replit",
    version="2.0.0"
)

# Environment variables (Replit Secrets)
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 🆕 Updated for RAG API integration
FLEX_API_URL = os.getenv('FLEX_API_URL', 'http://localhost:8002/m1-flex')  # ← 更新為 8002
RAG_HEALTH_URL = os.getenv('RAG_HEALTH_URL', 'http://localhost:8002/health')  # ← 新增健康檢查
RAG_ANALYZE_URL = os.getenv('RAG_ANALYZE_URL', 'http://localhost:8002/api/v1/analyze')  # ← 新增詳細分析

# Replit-specific configuration
REPL_SLUG = os.getenv('REPL_SLUG', 'workspace')
REPL_OWNER = os.getenv('REPL_OWNER', 'ke2211975')

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
    logger.error("❌ Missing LINE Bot credentials in Replit Secrets")

@app.get("/")
async def root():
    """Root endpoint with enhanced RAG information"""
    public_url = f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co"

    return {
        "message": "LINE Bot Webhook Service - Enhanced RAG Edition",
        "status": "running",
        "platform": "Replit",
        "version": "2.0.0",
        "line_bot_ready": line_bot_api is not None,
        "rag_api_url": FLEX_API_URL,
        "rag_health_url": RAG_HEALTH_URL,
        "public_url": public_url,
        "webhook_url": f"{public_url}/webhook",
        "features": [
            "🧠 Enhanced RAG Analysis",
            "🔍 Semantic Similarity Search", 
            "📊 Confidence Scoring",
            "💡 Multi-chunk Analysis",
            "🎯 Improved Accuracy"
        ],
        "endpoints": {
            "GET /": "Service information",
            "GET /health": "Health check", 
            "POST /webhook": "LINE Bot webhook",
            "GET /info": "Bot information",
            "GET /rag-status": "RAG API status"
        }
    }

@app.get("/rag-status")
async def rag_status():
    """RAG API specific status endpoint"""
    try:
        # 檢查 RAG API 健康狀態
        response = requests.get(RAG_HEALTH_URL, timeout=5)
        rag_health = response.json() if response.status_code == 200 else None

        return {
            "rag_api_status": "healthy" if response.status_code == 200 else "error",
            "rag_api_url": FLEX_API_URL,
            "rag_health_details": rag_health,
            "features": {
                "lightweight_rag": True,
                "semantic_search": True,
                "confidence_scoring": True,
                "multi_chunk_analysis": True,
                "rule_based_fallback": True
            },
            "timestamp": "2025-07-25T14:00:00Z"
        }
    except Exception as e:
        return {
            "rag_api_status": "error",
            "error": str(e),
            "rag_api_url": FLEX_API_URL
        }

@app.get("/health")
async def health_check():
    """Comprehensive health check including RAG API"""
    health_status = {
        "status": "healthy",
        "platform": "Replit",
        "version": "2.0.0",
        "services": {},
        "timestamp": "2025-07-25T14:00:00Z"
    }

    # Check LINE Bot API
    try:
        if line_bot_api:
            bot_info = line_bot_api.get_bot_info()
            health_status["services"]["line_bot"] = {
                "status": "ok",
                "bot_id": bot_info.user_id,
                "display_name": bot_info.display_name
            }
        else:
            health_status["services"]["line_bot"] = {"status": "not_configured"}
    except Exception as e:
        health_status["services"]["line_bot"] = {"status": "error", "error": str(e)}

    # 🆕 Check Enhanced RAG API
    try:
        response = requests.get(RAG_HEALTH_URL, timeout=5)
        if response.status_code == 200:
            rag_health = response.json()
            health_status["services"]["rag_api"] = {
                "status": "ok",
                "url": FLEX_API_URL,
                "components": rag_health.get("components", {}),
                "enhanced_features": True
            }
        else:
            health_status["services"]["rag_api"] = {
                "status": "error",
                "url": FLEX_API_URL,
                "http_status": response.status_code
            }
    except Exception as e:
        health_status["services"]["rag_api"] = {
            "status": "error", 
            "error": str(e),
            "url": FLEX_API_URL
        }

    # Overall status
    if any(service.get("status") == "error" for service in health_status["services"].values()):
        health_status["status"] = "degraded"

    return health_status

@app.post("/webhook")
async def webhook(request: Request):
    """Main webhook endpoint - unchanged for compatibility"""
    try:
        logger.info("📨 Webhook request received on Replit")

        if not handler or not line_bot_api:
            logger.error("❌ LINE Bot not configured")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "LINE Bot not configured",
                    "details": "Check Replit Secrets for LINE credentials"
                }
            )

        body = await request.body()
        signature = request.headers.get('X-Line-Signature', '')

        if not signature:
            logger.error("❌ Missing LINE signature")
            return JSONResponse(
                status_code=400,
                content={"error": "Missing X-Line-Signature header"}
            )

        try:
            body_str = body.decode('utf-8')
            handler.handle(body_str, signature)
            logger.info("✅ Webhook processed successfully")

        except InvalidSignatureError:
            logger.error("❌ Invalid LINE signature")
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid signature"}
            )
        except Exception as e:
            logger.error(f"❌ Webhook processing error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )

        return {"status": "ok", "platform": "Replit", "version": "2.0.0"}

    except Exception as e:
        logger.error(f"❌ Unexpected webhook error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "platform": "Replit"}
        )

def create_welcome_flex_message() -> Dict[str, Any]:
    """Create welcome flex message with RAG enhancement info"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "🧠 AI 失智症警訊分析助手",
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
                    "text": "歡迎使用 AI 增強版失智症早期警訊分析！",
                    "weight": "bold",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "🆕 v2.0 新功能：\n• 🔍 智能語義檢索\n• 📊 信心度評估\n• 💡 多資料源分析\n• 🎯 更高準確性",
                    "wrap": True,
                    "size": "sm",
                    "color": "#333333",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "📝 使用方式：直接描述行為變化\n💡 範例：媽媽最近常忘記關瓦斯",
                    "wrap": True,
                    "size": "sm"
                }
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "⚡ Enhanced by RAG + AI | ※ 僅供參考，不可取代專業診斷",
                "size": "xs",
                "color": "#999999",
                "align": "center"
            }],
            "paddingAll": "20px"
        }
    }

def create_error_flex_message(error_msg: str) -> Dict[str, Any]:
    """Create error flex message"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "⚠️ 系統暫時無法使用",
                "weight": "bold",
                "size": "lg",
                "color": "#ffffff"
            }],
            "backgroundColor": "#D70000",
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": f"{error_msg}。請稍後再試或諮詢專業醫師。",
                "wrap": True,
                "size": "md"
            }],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": "🔧 如持續發生問題，請檢查 RAG API 服務狀態",
                "size": "xs",
                "color": "#999999",
                "align": "center"
            }],
            "paddingAll": "20px"
        }
    }

def call_enhanced_rag_api(user_input: str) -> Optional[Dict[str, Any]]:
    """
    🆕 Call enhanced RAG API with improved error handling
    """
    try:
        logger.info(f"🔄 Calling enhanced RAG API: {FLEX_API_URL}")

        # 使用增強版 RAG API
        response = requests.post(
            FLEX_API_URL,
            json={"user_input": user_input},
            timeout=30,
            headers={"Content-Type": "application/json"}
        )

        logger.info(f"📊 RAG API response: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 🆕 Log RAG enhancement info
            if "rag_info" in result:
                rag_info = result["rag_info"]
                logger.info(f"🧠 RAG Analysis: {rag_info.get('analysis_method', 'unknown')} "
                           f"method, {rag_info.get('chunks_used', 0)} chunks, "
                           f"similarity: {rag_info.get('top_similarity', 0):.3f}")

            return result
        else:
            logger.error(f"❌ RAG API error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.Timeout:
        logger.error("⏰ RAG API timeout on Replit")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("🔗 Cannot connect to enhanced RAG API")
        return None
    except Exception as e:
        logger.error(f"❌ RAG API error: {e}")
        return None

# Event handlers - Enhanced for RAG integration
if handler and line_bot_api:
    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event):
        """🆕 Enhanced text message handler with RAG integration"""
        try:
            user_id = event.source.user_id
            user_text = event.message.text.strip()
            reply_token = event.reply_token

            logger.info(f"👤 Message from {user_id}: {user_text}")

            # Handle help/status commands
            if user_text.lower() in ['help', '幫助', '說明', 'start', '開始', 'rag', 'status', 'v2']:
                welcome_flex = create_welcome_flex_message()
                flex_message = FlexSendMessage(
                    alt_text="AI 增強版使用說明",
                    contents=welcome_flex
                )
                line_bot_api.reply_message(reply_token, flex_message)
                logger.info("📤 Sent enhanced welcome message")
                return

            # Input validation
            if len(user_text) < 5:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(
                        text="請提供更詳細的描述（至少5個字）\n\n💡 AI 分析範例：\n• 媽媽最近常忘記關瓦斯\n• 爸爸重複問同樣問題\n• 奶奶在熟悉地方迷路"
                    )
                )
                return

            if len(user_text) > 1000:
                line_bot_api.reply_message(
                    reply_token,
                    TextSendMessage(text="描述過長，請簡化在1000字以內")
                )
                return

            # 🆕 Call enhanced RAG API
            rag_response = call_enhanced_rag_api(user_text)

            if rag_response and "flex_message" in rag_response:
                # 🆕 Extract flex_message from RAG response
                flex_contents = rag_response["flex_message"]["contents"]

                flex_message = FlexSendMessage(
                    alt_text=rag_response["flex_message"].get("altText", "失智症警訊分析結果"),
                    contents=flex_contents
                )

                line_bot_api.reply_message(reply_token, flex_message)

                # 🆕 Enhanced logging with RAG info
                rag_info = rag_response.get("rag_info", {})
                analysis_data = rag_response.get("analysis_data", {})

                logger.info(f"✅ Sent enhanced analysis to {user_id}: "
                           f"Code={analysis_data.get('matched_warning_code', 'N/A')}, "
                           f"Confidence={analysis_data.get('confidence_level', 'N/A')}, "
                           f"Method={rag_info.get('analysis_method', 'N/A')}")

            else:
                error_flex = create_error_flex_message("AI 分析服務暫時無法使用")
                flex_message = FlexSendMessage(
                    alt_text="系統錯誤",
                    contents=error_flex
                )
                line_bot_api.reply_message(reply_token, flex_message)
                logger.warning(f"⚠️ Sent error message to {user_id}")

        except LineBotApiError as e:
            logger.error(f"❌ LINE Bot API error: {e}")
        except Exception as e:
            logger.error(f"❌ Enhanced text handler error: {e}")
            logger.error(traceback.format_exc())

    @handler.add(FollowEvent)
    def handle_follow(event):
        """Handle new followers with enhanced welcome"""
        try:
            user_id = event.source.user_id
            reply_token = event.reply_token
            logger.info(f"👋 New follower on Replit: {user_id}")

            welcome_flex = create_welcome_flex_message()
            flex_message = FlexSendMessage(
                alt_text="歡迎使用 AI 增強版失智症警訊分析",
                contents=welcome_flex
            )
            line_bot_api.reply_message(reply_token, flex_message)
            logger.info("📤 Sent enhanced welcome message to new follower")

        except LineBotApiError as e:
            logger.error(f"❌ LINE Bot API error in follow handler: {e}")
        except Exception as e:
            logger.error(f"❌ Follow handler error: {e}")

@app.get("/info")
async def bot_info():
    """Get bot information with RAG enhancement details"""
    try:
        if not line_bot_api:
            raise HTTPException(status_code=500, detail="LINE Bot not configured")

        bot_info = line_bot_api.get_bot_info()
        return {
            "bot_id": bot_info.user_id,
            "display_name": bot_info.display_name,
            "status": "active",
            "platform": "Replit",
            "version": "2.0.0",
            "enhancements": {
                "rag_integration": True,
                "semantic_search": True,
                "confidence_scoring": True,
                "multi_chunk_analysis": True
            },
            "repl_url": f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co",
            "webhook_url": f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co/webhook",
            "rag_api_url": FLEX_API_URL
        }
    except LineBotApiError as e:
        logger.error(f"Error getting bot info: {e}")
        raise HTTPException(status_code=500, detail="Cannot get bot information")

# Keep-alive endpoint for Replit
@app.get("/ping")
async def ping():
    """Simple ping endpoint to keep Replit alive"""
    return {"status": "pong", "platform": "Replit", "version": "2.0.0", "rag_enhanced": True}

# Test endpoint with RAG integration
@app.post("/test-webhook")
async def test_webhook():
    """🆕 Enhanced test webhook functionality"""
    return {
        "message": "Enhanced Webhook test endpoint",
        "line_bot_configured": line_bot_api is not None,
        "handler_configured": handler is not None,
        "rag_api_url": FLEX_API_URL,
        "rag_health_url": RAG_HEALTH_URL,
        "platform": "Replit",
        "version": "2.0.0",
        "enhancements": ["RAG", "Semantic Search", "Confidence Scoring"]
    }

# Main execution block
if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Enhanced LINE Bot Webhook on Replit...")
    print("=" * 60)
    print(f"📍 Platform: Replit")
    print(f"📍 Version: 2.0.0 (RAG Enhanced)")
    print(f"📍 Environment Check:")
    print(f"   LINE_CHANNEL_ACCESS_TOKEN: {'✅' if LINE_CHANNEL_ACCESS_TOKEN else '❌'}")
    print(f"   LINE_CHANNEL_SECRET: {'✅' if LINE_CHANNEL_SECRET else '❌'}")
    print(f"   RAG API URL: {FLEX_API_URL}")
    print(f"   RAG Health URL: {RAG_HEALTH_URL}")

    if REPL_SLUG and REPL_OWNER:
        webhook_url = f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co/webhook"
        print(f"🔗 Public Webhook URL: {webhook_url}")

    print(f"📡 Available endpoints:")
    print(f"   GET  /              - Service information (enhanced)")
    print(f"   GET  /health        - Health check (with RAG)")
    print(f"   GET  /rag-status    - RAG API specific status")
    print(f"   POST /webhook       - LINE webhook (enhanced)")
    print(f"   GET  /info          - Bot information (enhanced)")
    print(f"   GET  /ping          - Keep-alive ping")
    print(f"   POST /test-webhook  - Test endpoint (enhanced)")
    print("=" * 60)
    print("🆕 RAG Enhancements:")
    print("   🔍 Semantic similarity search")
    print("   📊 Dynamic confidence scoring")
    print("   💡 Multi-chunk analysis")
    print("   🎯 Improved accuracy")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,  # Keep original port for compatibility
        log_level="info"
    )
