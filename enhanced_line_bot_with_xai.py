import os
import logging
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage
)
import httpx
import asyncio
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# LINE Bot credentials
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# Initialize LINE Bot API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# XAI Wrapper Service configuration
XAI_WRAPPER_URL = os.getenv('XAI_WRAPPER_URL', 'http://localhost:8009/analyze')
USE_XAI_WRAPPER = os.getenv('USE_XAI_WRAPPER', 'true').lower() == 'true'
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.6'))

class EnhancedMessageHandler:
    """Enhanced message handler with XAI visualization support"""
    
    def __init__(self):
        self.xai_wrapper_url = XAI_WRAPPER_URL
        self.use_xai_wrapper = USE_XAI_WRAPPER
        self.confidence_threshold = CONFIDENCE_THRESHOLD
    
    async def handle_text_message(self, event):
        """Handle text message with XAI enhancement"""
        user_input = event.message.text
        user_id = event.source.user_id
        
        logger.info(f"👤 Message from {user_id}: {user_input}")
        
        try:
            if self.use_xai_wrapper:
                # Use XAI wrapper service
                logger.info("🤖 Using XAI Wrapper Service")
                enhanced_response = await self.call_xai_wrapper(user_input, user_id)
                
                if enhanced_response and enhanced_response.get("xai_enhanced"):
                    xai_data = enhanced_response["xai_enhanced"]
                    confidence = xai_data.get("confidence", 0.0)
                    
                    if confidence >= self.confidence_threshold:
                        # Send enhanced Flex Message
                        flex_message = self.build_enhanced_flex_message(
                            module=xai_data["module"],
                            visualization_data=xai_data["visualization"],
                            original_response=enhanced_response["original_response"]
                        )
                        
                        line_bot_api.reply_message(
                            event.reply_token,
                            FlexSendMessage(alt_text="XAI 增強分析結果", contents=flex_message["contents"])
                        )
                        logger.info(f"✅ Sent XAI Enhanced Flex Message to {user_id}")
                    else:
                        # Fallback to original response
                        original_response = enhanced_response["original_response"]
                        if original_response.get("type") == "flex":
                            line_bot_api.reply_message(
                                event.reply_token,
                                FlexSendMessage(
                                    alt_text=original_response.get("altText", "分析結果"),
                                    contents=original_response["contents"]
                                )
                            )
                        else:
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=original_response.get("text", "抱歉，無法處理您的請求。"))
                            )
                        logger.info(f"✅ Sent fallback response to {user_id}")
                else:
                    # Fallback to direct chatbot API
                    logger.info("🔄 Falling back to direct chatbot API")
                    await self.handle_with_direct_api(event, user_input, user_id)
            else:
                # Use direct chatbot API
                await self.handle_with_direct_api(event, user_input, user_id)
                
        except Exception as e:
            logger.error(f"❌ Error handling message: {e}")
            # Send error message
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，系統暫時無法處理您的請求，請稍後再試。")
            )
    
    async def call_xai_wrapper(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Call XAI wrapper service"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    self.xai_wrapper_url,
                    json={
                        "user_input": user_input,
                        "user_id": user_id
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"❌ Error calling XAI wrapper: {e}")
            return None
    
    async def handle_with_direct_api(self, event, user_input: str, user_id: str):
        """Handle message with direct chatbot API"""
        try:
            # Call your existing chatbot API
            chatbot_api_url = "http://localhost:8008/analyze"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    chatbot_api_url,
                    json={
                        "message": user_input,
                        "user_id": user_id
                    }
                )
                response.raise_for_status()
                bot_response = response.json()
                
                # Send response
                if bot_response.get("type") == "flex":
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(
                            alt_text=bot_response.get("altText", "分析結果"),
                            contents=bot_response["contents"]
                        )
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=bot_response.get("text", "抱歉，無法處理您的請求。"))
                    )
                
                logger.info(f"✅ Sent direct API response to {user_id}")
                
        except Exception as e:
            logger.error(f"❌ Error calling direct API: {e}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，系統暫時無法處理您的請求，請稍後再試。")
            )
    
    def build_enhanced_flex_message(self, module: str, visualization_data: Dict[str, Any], original_response: Dict[str, Any]) -> Dict[str, Any]:
        """Build enhanced Flex Message with XAI visualization"""
        
        # Module-specific colors
        module_colors = {
            "M1": "#E74C3C",  # Red for warning signs
            "M2": "#E67E22",  # Orange for progression
            "M3": "#9B59B6",  # Purple for BPSD
            "M4": "#3498DB",  # Blue for care
            "general": "#27AE60"  # Green for general
        }
        
        confidence = visualization_data.get("confidence_score", 0.0)
        title = visualization_data.get("title", "分析結果")
        
        # Create header
        header_contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "color": "#ffffff",
                "size": "lg"
            }
        ]
        
        # Add confidence score if available
        if confidence > 0:
            header_contents.append({
                "type": "text",
                "text": f"信心度: {confidence:.1%}",
                "color": "#ffffff",
                "size": "sm"
            })
        
        # Create body content
        body_contents = [
            {
                "type": "text",
                "text": "🔍 XAI 分析結果",
                "weight": "bold",
                "size": "md",
                "color": "#333333"
            },
            {
                "type": "separator"
            }
        ]
        
        # Add module-specific content
        if module == "M1":
            evidence_highlights = visualization_data.get("evidence_highlights", [])
            for highlight in evidence_highlights[:3]:
                body_contents.append({
                    "type": "text",
                    "text": f"• {highlight['text']}",
                    "size": "sm",
                    "color": "#E74C3C",
                    "weight": "bold"
                })
        elif module == "M2":
            stage_indicators = visualization_data.get("stage_indicators", [])
            for indicator in stage_indicators[:3]:
                body_contents.append({
                    "type": "text",
                    "text": f"• {indicator}",
                    "size": "sm",
                    "color": "#E67E22"
                })
        elif module == "M3":
            symptoms = visualization_data.get("symptoms", [])
            for symptom in symptoms[:3]:
                body_contents.append({
                    "type": "text",
                    "text": f"• {symptom}",
                    "size": "sm",
                    "color": "#9B59B6"
                })
        elif module == "M4":
            care_needs = visualization_data.get("care_needs", [])
            for need in care_needs[:3]:
                body_contents.append({
                    "type": "text",
                    "text": f"• {need}",
                    "size": "sm",
                    "color": "#3498DB"
                })
        
        # Add reasoning path if available
        reasoning = visualization_data.get("reasoning_path", {})
        if reasoning.get("steps"):
            body_contents.extend([
                {
                    "type": "separator"
                },
                {
                    "type": "text",
                    "text": "🧠 分析過程",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#333333"
                }
            ])
            
            for step in reasoning["steps"][:2]:  # Show first 2 steps
                body_contents.append({
                    "type": "text",
                    "text": f"• {step['label']}: {step['description']}",
                    "size": "xs",
                    "color": "#666666",
                    "wrap": True
                })
        
        # Add recommendation
        body_contents.extend([
            {
                "type": "separator"
            },
            {
                "type": "text",
                "text": "💡 建議",
                "weight": "bold",
                "size": "sm",
                "color": "#333333"
            },
            {
                "type": "text",
                "text": "基於 XAI 分析結果，建議尋求專業醫療協助",
                "size": "sm",
                "color": "#666666",
                "wrap": True
            }
        ])
        
        return {
            "type": "flex",
            "altText": f"{title} - XAI 增強分析",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": header_contents,
                    "backgroundColor": module_colors.get(module, "#27AE60")
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": body_contents
                }
            }
        }

# Initialize enhanced handler
enhanced_handler = EnhancedMessageHandler()

@app.route("/webhook", methods=['POST'])
def webhook():
    """Webhook endpoint for LINE Bot"""
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    logger.info("📨 Webhook request received")

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle text message events"""
    # Use asyncio to handle async function
    asyncio.run(enhanced_handler.handle_text_message(event))

@app.route("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Enhanced LINE Bot with XAI",
        "version": "2.0.0",
        "features": [
            "XAI visualization",
            "Module detection (M1-M4)",
            "Confidence-based responses",
            "Enhanced Flex Messages"
        ],
        "configuration": {
            "use_xai_wrapper": USE_XAI_WRAPPER,
            "xai_wrapper_url": XAI_WRAPPER_URL,
            "confidence_threshold": CONFIDENCE_THRESHOLD
        }
    }

@app.route("/")
def root():
    """Root endpoint"""
    return {
        "service": "Enhanced LINE Bot with XAI",
        "version": "2.0.0",
        "description": "LINE Bot with XAI visualization capabilities",
        "endpoints": {
            "POST /webhook": "LINE webhook endpoint",
            "GET /health": "Health check",
            "GET /": "Service information"
        }
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced LINE Bot with XAI...")
    logger.info(f"📍 XAI Wrapper URL: {XAI_WRAPPER_URL}")
    logger.info(f"📍 Use XAI Wrapper: {USE_XAI_WRAPPER}")
    logger.info(f"📍 Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    
    app.run(host='0.0.0.0', port=8081, debug=False) 