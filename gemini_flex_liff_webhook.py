#!/usr/bin/env python3
"""
Gemini Flex LIFF Webhook
Complete flow: LINE → Webhook → Third Party API (小幫手) → Gemini → Visualization (Flex Message + LIFF) → LINE
"""
import os
import json
import logging
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage, 
    MessageEvent, 
    TextMessage,
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent,
    ButtonComponent,
    URIAction
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
LIFF_URL = os.getenv('LIFF_URL', 'https://your-liff-app.com')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize LINE Bot API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def call_gemini_api(user_message):
    """Call Google Gemini API with enhanced prompt for 小幫手 (Little Helper)"""
    try:
        # Enhanced prompt for 小幫手 functionality
        enhanced_prompt = f"""
你是一個專業的失智症警訊分析助手「小幫手」。請分析以下用戶描述，並提供：

1. 失智症警訊分析
2. 專業建議
3. 關懷提醒
4. 後續行動建議

用戶描述：{user_message}

請用繁體中文回答，並提供結構化的分析結果。
"""
        
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": enhanced_prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=data,
            params={"key": GOOGLE_GEMINI_API_KEY}
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return {
                    "success": True,
                    "response": content,
                    "analysis": parse_gemini_response(content)
                }
            else:
                return {"success": False, "error": "No response from Gemini API"}
        else:
            return {"success": False, "error": f"Gemini API error: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        return {"success": False, "error": str(e)}

def parse_gemini_response(response_text):
    """Parse Gemini response and extract key information"""
    try:
        # Extract key information from the response
        lines = response_text.split('\n')
        analysis = ""
        recommendations = ""
        warnings = []
        
        for line in lines:
            if '警訊' in line or '徵兆' in line:
                warnings.append(line.strip())
            elif '建議' in line or '提醒' in line:
                recommendations += line.strip() + "\n"
            else:
                analysis += line.strip() + "\n"
        
        return {
            "full_response": response_text,
            "analysis": analysis.strip(),
            "recommendations": recommendations.strip(),
            "warnings": warnings
        }
    except Exception as e:
        logger.error(f"Error parsing Gemini response: {str(e)}")
        return {
            "full_response": response_text,
            "analysis": response_text,
            "recommendations": "",
            "warnings": []
        }

def create_flex_message_with_liff(analysis_data, user_id):
    """Create Flex Message with LIFF integration"""
    try:
        # Create LIFF URL with user context
        liff_url = f"{LIFF_URL}?userId={user_id}&analysis={analysis_data.get('analysis', '')}"
        
        flex_message = BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="🧠 小幫手 AI 分析結果",
                        weight="bold",
                        size="lg",
                        color="#1DB446"
                    ),
                    TextComponent(
                        text=analysis_data.get('analysis', '分析完成'),
                        wrap=True,
                        margin="md",
                        size="sm"
                    ),
                    BoxComponent(
                        layout="vertical",
                        margin="lg",
                        contents=[
                            TextComponent(
                                text="📋 詳細分析報告",
                                weight="bold",
                                size="sm",
                                color="#666666"
                            ),
                            TextComponent(
                                text="點擊下方按鈕查看完整分析",
                                size="xs",
                                color="#999999",
                                margin="sm"
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    ButtonComponent(
                        style="primary",
                        color="#1DB446",
                        action=URIAction(
                            label="📊 查看詳細報告",
                            uri=liff_url
                        )
                    ),
                    ButtonComponent(
                        style="secondary",
                        margin="sm",
                        action=URIAction(
                            label="💬 諮詢專業醫師",
                            uri="https://line.me/R/ti/p/@your-doctor-bot"
                        )
                    )
                ]
            )
        )
        
        return FlexSendMessage(
            alt_text="小幫手 AI 分析結果",
            contents=flex_message
        )
        
    except Exception as e:
        logger.error(f"Error creating Flex message: {str(e)}")
        # Fallback to simple text message
        return TextSendMessage(text=f"🧠 小幫手分析結果:\n\n{analysis_data.get('analysis', '分析完成')}")

@app.route("/webhook", methods=['POST'])
def webhook():
    """Handle LINE webhook"""
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle text messages from LINE"""
    try:
        user_id = event.source.user_id
        user_message = event.text
        reply_token = event.reply_token
        
        logger.info(f"📨 Received message from {user_id}: {user_message}")
        
        # Step 1: Call Gemini API (Third Party API - 小幫手)
        logger.info("🤖 Calling Gemini API (小幫手)...")
        gemini_response = call_gemini_api(user_message)
        
        if gemini_response["success"]:
            # Step 2: Parse and analyze the response
            analysis_data = gemini_response["analysis"]
            
            # Step 3: Create Flex Message with LIFF integration
            logger.info("🎨 Creating Flex Message with LIFF...")
            flex_message = create_flex_message_with_liff(analysis_data, user_id)
            
            # Step 4: Send response back to LINE
            logger.info("📤 Sending response to LINE...")
            line_bot_api.reply_message(reply_token, flex_message)
            
            logger.info(f"✅ Successfully processed message for {user_id}")
            
        else:
            # Fallback to simple text message
            error_message = f"抱歉，小幫手暫時無法回應。錯誤：{gemini_response.get('error', '未知錯誤')}"
            text_message = TextSendMessage(text=error_message)
            line_bot_api.reply_message(reply_token, text_message)
            
    except Exception as e:
        logger.error(f"❌ Error processing message: {str(e)}")
        error_message = TextSendMessage(text="抱歉，處理您的訊息時發生錯誤，請稍後再試。")
        line_bot_api.reply_message(reply_token, error_message)

@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Gemini Flex LIFF Webhook",
        "gemini_configured": bool(GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here'),
        "line_bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET),
        "liff_url": LIFF_URL
    }

@app.route("/test", methods=['POST'])
def test_api():
    """Test endpoint for API functionality"""
    try:
        data = request.get_json()
        test_message = data.get('message', '你好，小幫手')
        
        # Test Gemini API call
        result = call_gemini_api(test_message)
        
        return {
            "success": True,
            "test_message": test_message,
            "gemini_response": result,
            "liff_url": f"{LIFF_URL}?test=true"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.route("/", methods=['GET'])
def home():
    """Home endpoint with service information"""
    return {
        "service": "Gemini Flex LIFF Webhook",
        "version": "1.0.0",
        "description": "Complete flow: LINE → Webhook → Third Party API (小幫手) → Gemini → Visualization (Flex Message + LIFF) → LINE",
        "endpoints": {
            "POST /webhook": "LINE webhook endpoint",
            "GET /health": "Health check",
            "POST /test": "Test API functionality",
            "GET /": "Service information"
        },
        "features": [
            "🧠 Gemini AI Integration",
            "🎨 Flex Message Visualization", 
            "📱 LIFF Integration",
            "🔗 Complete LINE Flow"
        ]
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Gemini Flex LIFF Webhook...")
    logger.info(f"🔑 Gemini API configured: {'Yes' if GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here' else 'No'}")
    logger.info(f"📱 LINE Bot configured: {'Yes' if LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET else 'No'}")
    logger.info(f"🌐 LIFF URL: {LIFF_URL}")
    
    app.run(host='0.0.0.0', port=8083, debug=False) 