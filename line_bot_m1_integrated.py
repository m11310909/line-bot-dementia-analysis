#!/usr/bin/env python3
"""
LINE Bot Webhook Service - M1 Enhanced Visualization Integration
Integrated with M1.fig design specifications
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot.v3 import LineBotApi, WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError, LineBotApiError
from linebot.v3.messaging import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage, FollowEvent
import requests
import os
import logging
import traceback
import json
from typing import Optional, Dict, Any
from datetime import datetime

# Import M1 visualization modules
try:
    from xai_flex.m1_enhanced_visualization import M1EnhancedVisualizationGenerator, WarningLevel
    from xai_flex.m1_integration import M1IntegrationManager
    M1_AVAILABLE = True
except ImportError:
    # Fallback to simple version
    M1_AVAILABLE = False
    print("⚠️ M1 modules not available, using fallback")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Webhook - M1 Enhanced v3.0",
    description="LINE Bot with M1 visualization integration",
    version="3.0.0"
)

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# API URLs
RAG_API_URL = 'http://localhost:8002/api/v1/analyze/m1'
FLEX_API_URL = 'http://localhost:8002/api/v1/flex-message'
HEALTH_URL = 'http://localhost:8002/health'

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

# Initialize M1 modules
m1_generator = None
m1_integration = None

if M1_AVAILABLE:
    try:
        m1_generator = M1EnhancedVisualizationGenerator()
        # Skip integration manager for now to avoid log file issues
        logger.info("✅ M1 visualization modules initialized")
    except Exception as e:
        logger.error(f"❌ M1 modules initialization failed: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LINE Bot Webhook - M1 Enhanced v3.0",
        "status": "running",
        "line_bot_ready": line_bot_api is not None,
        "m1_modules_ready": M1_AVAILABLE and m1_generator is not None,
        "rag_api_url": RAG_API_URL,
        "version": "3.0.0",
        "features": [
            "🧠 M1 Enhanced Visualization",
            "🎨 Design System Integration",
            "🔍 XAI Confidence Display",
            "📊 Comparison Cards",
            "♿ Accessibility Features"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check with M1 status"""
    health = {
        "status": "healthy",
        "services": {},
        "timestamp": datetime.now().isoformat()
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

    # Check M1 modules
    if M1_AVAILABLE and m1_generator:
        health["services"]["m1_modules"] = {"status": "ok"}
    else:
        health["services"]["m1_modules"] = {"status": "not_available"}

    # Check RAG API
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            health["services"]["rag_api"] = {"status": "ok"}
        else:
            health["services"]["rag_api"] = {"status": "error", "code": response.status_code}
    except Exception as e:
        health["services"]["rag_api"] = {"status": "error", "error": str(e)}

    return health

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

def create_m1_welcome_message() -> Dict[str, Any]:
    """Create welcome message with M1 design"""
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 AI 失智症警訊分析",
                    "size": "lg",
                    "weight": "bold",
                    "color": "#212121"
                },
                {
                    "type": "text",
                    "text": "M1 十大警訊比對卡",
                    "size": "sm",
                    "color": "#666666",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#F5F5F5",
            "contents": [
                {
                    "type": "text",
                    "text": "請描述您觀察到的症狀，AI 將協助分析是否為失智症警訊。",
                    "size": "sm",
                    "color": "#666666",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "💡 範例：\n• 媽媽最近常忘記關瓦斯\n• 爸爸重複問同樣問題\n• 爺爺在熟悉環境中迷路",
                    "size": "xs",
                    "color": "#2196F3",
                    "wrap": True,
                    "margin": "md"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF",
            "contents": [
                {
                    "type": "text",
                    "text": "開始分析",
                    "size": "sm",
                    "color": "#2196F3",
                    "align": "center",
                    "margin": "md"
                }
            ]
        }
    }

def call_m1_analysis_api(user_input: str) -> Optional[Dict[str, Any]]:
    """Call M1 analysis API"""
    try:
        # Prepare request
        request_data = {
            "query": user_input,
            "user_context": {
                "platform": "line",
                "timestamp": datetime.now().isoformat()
            }
        }

        logger.info(f"🔍 Calling M1 analysis API: {user_input[:50]}...")
        
        response = requests.post(
            RAG_API_URL,
            json=request_data,
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ M1 analysis successful: {result.get('confidence_score', 0)}")
            return result
        else:
            logger.error(f"❌ M1 API error: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"❌ M1 API call failed: {e}")
        return None

def create_m1_fallback_response(user_input: str) -> Dict[str, Any]:
    """Create fallback M1 response when API is unavailable"""
    try:
        # Simple analysis based on keywords
        keywords = {
            "忘記": {"confidence": 0.75, "level": "caution"},
            "迷路": {"confidence": 0.80, "level": "warning"},
            "重複": {"confidence": 0.70, "level": "caution"},
            "瓦斯": {"confidence": 0.85, "level": "warning"},
            "鑰匙": {"confidence": 0.65, "level": "normal"},
            "約會": {"confidence": 0.75, "level": "caution"}
        }
        
        # Find matching keywords
        matched_keywords = []
        for keyword, data in keywords.items():
            if keyword in user_input:
                matched_keywords.append((keyword, data))
        
        if matched_keywords:
            # Use the highest confidence match
            best_match = max(matched_keywords, key=lambda x: x[1]["confidence"])
            keyword, data = best_match
            
            return {
                "confidence_score": data["confidence"],
                "comparison_data": {
                    "normal_aging": "偶爾忘記但能回想起來",
                    "dementia_warning": f"經常{keyword}且無法回想"
                },
                "key_finding": f"觀察到{keyword}相關症狀，建議進一步評估",
                "warning_level": data["level"]
            }
        else:
            # Default response
            return {
                "confidence_score": 0.50,
                "comparison_data": {
                    "normal_aging": "一般記憶力衰退",
                    "dementia_warning": "需要更多資訊評估"
                },
                "key_finding": "請提供更詳細的症狀描述",
                "warning_level": "normal"
            }
    except Exception as e:
        logger.error(f"Fallback analysis failed: {e}")
        return {
            "confidence_score": 0.0,
            "comparison_data": {
                "normal_aging": "無法分析",
                "dementia_warning": "請諮詢專業醫師"
            },
            "key_finding": "分析服務暫時無法使用",
            "warning_level": "normal"
        }

# Event handlers
if handler and line_bot_api:
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        """Handle text messages with M1 integration"""
        try:
            user_id = event.source.user_id
            user_text = event.message.text.strip()
            reply_token = event.reply_token

            logger.info(f"👤 Message from {user_id}: {user_text}")

            # Handle commands
            if user_text.lower() in ['help', '幫助', 'start', '開始', 'm1']:
                welcome_flex = create_m1_welcome_message()
                flex_message = FlexSendMessage(
                    alt_text="AI 失智症警訊分析 - 使用說明",
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

            # Try M1 API first
            rag_response = call_m1_analysis_api(user_text)
            
            if not rag_response and M1_AVAILABLE and m1_generator:
                # Use fallback M1 analysis
                logger.info("🔄 Using M1 fallback analysis")
                analysis_data = create_m1_fallback_response(user_text)
                
                # Generate M1 Flex Message
                flex_message_data = m1_generator.generate_m1_flex_message(analysis_data)
                
                flex_message = FlexSendMessage(
                    alt_text=flex_message_data.get("altText", "失智症警訊分析結果"),
                    contents=flex_message_data.get("contents", {})
                )
                
                line_bot_api.reply_message(reply_token, flex_message)
                logger.info(f"✅ M1 fallback analysis sent to {user_id}")
                return

            elif rag_response and "flex_message" in rag_response:
                # Use RAG API response
                flex_contents = rag_response["flex_message"]["contents"]
                alt_text = rag_response["flex_message"].get("altText", "失智症警訊分析結果")

                flex_message = FlexSendMessage(
                    alt_text=alt_text,
                    contents=flex_contents
                )

                line_bot_api.reply_message(reply_token, flex_message)
                logger.info(f"✅ RAG analysis sent to {user_id}")
            else:
                # Error response
                error_text = "抱歉，AI 分析服務暫時無法使用，請稍後再試或諮詢專業醫師。\n\n如需協助，請輸入「幫助」查看使用說明。"
                line_bot_api.reply_message(reply_token, TextSendMessage(text=error_text))
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

            welcome_flex = create_m1_welcome_message()
            flex_message = FlexSendMessage(
                alt_text="歡迎使用 AI 失智症警訊分析",
                contents=welcome_flex
            )
            line_bot_api.reply_message(reply_token, flex_message)

        except LineBotApiError as e:
            logger.error(f"❌ Follow handler error: {e}")

@app.get("/info")
async def bot_info():
    """Get bot information"""
    return {
        "bot_name": "AI 失智症警訊分析",
        "version": "3.0.0",
        "features": [
            "M1 Enhanced Visualization",
            "XAI Confidence Display",
            "Comparison Cards",
            "Accessibility Features"
        ],
        "m1_available": M1_AVAILABLE,
        "line_bot_ready": line_bot_api is not None
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"pong": "M1 Enhanced v3.0"}

@app.post("/test")
async def test_endpoint():
    """Test endpoint for M1 visualization"""
    if not M1_AVAILABLE or not m1_generator:
        return {"error": "M1 modules not available"}
    
    try:
        # Test M1 visualization
        test_data = {
            "confidence_score": 0.85,
            "comparison_data": {
                "normal_aging": "偶爾忘記鑰匙位置，但能回想起來",
                "dementia_warning": "經常忘記重要約會，且無法回想"
            },
            "key_finding": "記憶力衰退模式符合輕度認知障礙徵兆",
            "warning_level": "caution"
        }
        
        flex_message = m1_generator.generate_m1_flex_message(test_data)
        return {
            "status": "success",
            "m1_test": flex_message
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 