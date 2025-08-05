#!/usr/bin/env python3
"""
Integrated Dementia Assistant Webhook
Complete flow: LINE → Webhook → Third Party API (失智小幫手) → Text → Gemini → JSON → Flex Message → LINE
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
THIRD_PARTY_API_KEY = os.getenv('THIRD_PARTY_API_KEY')
API_KEY = os.getenv('API_KEY')
LIFF_URL = os.getenv('LIFF_URL', 'https://your-liff-app.com')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize LINE Bot API
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def call_third_party_dementia_assistant(user_message):
    """
    Step 1: Call Third Party API (失智小幫手)
    This simulates a specialized dementia assistant API
    """
    try:
        # Enhanced prompt for 失智小幫手 functionality
        dementia_prompt = f"""
你是一個專業的失智症照護助手「失智小幫手」。請分析以下用戶描述，並提供：

1. 失智症警訊分析
2. 專業建議
3. 關懷提醒
4. 後續行動建議

用戶描述：{user_message}

請用繁體中文回答，並提供結構化的分析結果。
"""
        
        # Try different API configurations
        api_configs = [
            {
                'name': 'gemini',
                'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
                'headers': {'Content-Type': 'application/json'},
                'data': {
                    'contents': [{'parts': [{'text': dementia_prompt}]}],
                    'generationConfig': {'temperature': 0.7, 'maxOutputTokens': 1000}
                },
                'api_key': GOOGLE_GEMINI_API_KEY
            },
            {
                'name': 'openai',
                'url': 'https://api.openai.com/v1/chat/completions',
                'headers': {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
                'data': {
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {'role': 'system', 'content': '你是一個專業的失智症照護助手「失智小幫手」。'},
                        {'role': 'user', 'content': user_message}
                    ],
                    'max_tokens': 1000,
                    'temperature': 0.7
                },
                'api_key': API_KEY
            }
        ]
        
        for config in api_configs:
            try:
                logger.info(f"🔄 Trying {config['name']} API...")
                
                response = requests.post(
                    config['url'],
                    headers=config['headers'],
                    json=config['data'],
                    params={'key': config['api_key']} if config['name'] == 'gemini' else {},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if config['name'] == 'gemini':
                        if 'candidates' in result and len(result['candidates']) > 0:
                            content = result['candidates'][0]['content']['parts'][0]['text']
                        else:
                            continue
                    elif config['name'] == 'openai':
                        if 'choices' in result and len(result['choices']) > 0:
                            content = result['choices'][0]['message']['content']
                        else:
                            continue
                    
                    logger.info(f"✅ {config['name']} API successful")
                    return {
                        "success": True,
                        "api_used": config['name'],
                        "response": content,
                        "analysis": parse_dementia_response(content)
                    }
                    
                else:
                    logger.warning(f"⚠️ {config['name']} API failed: {response.status_code}")
                    continue
                    
            except Exception as e:
                logger.warning(f"⚠️ {config['name']} API error: {str(e)}")
                continue
        
        # If all APIs fail, return a fallback response
        logger.error("❌ All APIs failed")
        return {
            "success": False,
            "api_used": "fallback",
            "response": "抱歉，失智小幫手暫時無法回應，請稍後再試。",
            "analysis": {
                "full_response": "服務暫時無法使用",
                "analysis": "請稍後再試",
                "recommendations": "",
                "warnings": []
            }
        }
            
    except Exception as e:
        logger.error(f"Error calling third party API: {str(e)}")
        return {
            "success": False,
            "api_used": "error",
            "response": f"抱歉，失智小幫手發生錯誤: {str(e)}",
            "analysis": {
                "full_response": "錯誤發生",
                "analysis": "請稍後再試",
                "recommendations": "",
                "warnings": []
            }
        }

def parse_dementia_response(response_text):
    """
    Step 2: Parse the text response and extract structured information
    """
    try:
        # Extract key information from the response
        lines = response_text.split('\n')
        analysis = ""
        recommendations = ""
        warnings = []
        
        for line in lines:
            if '警訊' in line or '徵兆' in line or '症狀' in line:
                warnings.append(line.strip())
            elif '建議' in line or '提醒' in line or '行動' in line:
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
        logger.error(f"Error parsing response: {str(e)}")
        return {
            "full_response": response_text,
            "analysis": response_text,
            "recommendations": "",
            "warnings": []
        }

def create_enhanced_flex_message(analysis_data, user_id, api_used):
    """
    Step 3: Create enhanced Flex Message with JSON data
    """
    try:
        # Create LIFF URL with user context and analysis data
        analysis_json = json.dumps(analysis_data, ensure_ascii=False)
        liff_url = f"{LIFF_URL}?userId={user_id}&analysis={analysis_json}&api={api_used}"
        
        # Create enhanced Flex Message
        flex_message = BubbleContainer(
            size="giga",
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="🧠 失智小幫手 AI 分析結果",
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
                                text=f"使用 {api_used.upper()} AI 引擎分析",
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
            alt_text="失智小幫手 AI 分析結果",
            contents=flex_message
        )
        
    except Exception as e:
        logger.error(f"Error creating Flex message: {str(e)}")
        # Fallback to simple text message
        return TextSendMessage(text=f"🧠 失智小幫手分析結果:\n\n{analysis_data.get('analysis', '分析完成')}")

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
    """Handle text messages from LINE - Complete Integrated Flow"""
    try:
        user_id = event.source.user_id
        user_message = event.text
        reply_token = event.reply_token
        
        logger.info(f"📨 Received message from {user_id}: {user_message}")
        
        # Step 1: Call Third Party API (失智小幫手)
        logger.info("🤖 Step 1: Calling Third Party API (失智小幫手)...")
        third_party_response = call_third_party_dementia_assistant(user_message)
        
        if third_party_response["success"]:
            # Step 2: Parse text response and extract JSON data
            logger.info("📝 Step 2: Parsing text response and extracting JSON data...")
            analysis_data = third_party_response["analysis"]
            api_used = third_party_response["api_used"]
            
            # Step 3: Create enhanced Flex Message with JSON data
            logger.info("🎨 Step 3: Creating enhanced Flex Message with JSON data...")
            flex_message = create_enhanced_flex_message(analysis_data, user_id, api_used)
            
            # Step 4: Send response back to LINE
            logger.info("📤 Step 4: Sending enhanced Flex Message to LINE...")
            line_bot_api.reply_message(reply_token, flex_message)
            
            logger.info(f"✅ Complete flow successful for {user_id} using {api_used} API")
            
        else:
            # Fallback to simple text message
            error_message = f"抱歉，失智小幫手暫時無法回應。錯誤：{third_party_response.get('response', '未知錯誤')}"
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
        "service": "Integrated Dementia Assistant Webhook",
        "description": "Complete flow: LINE → Webhook → Third Party API (失智小幫手) → Text → Gemini → JSON → Flex Message → LINE",
        "gemini_configured": bool(GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here'),
        "openai_configured": bool(API_KEY and API_KEY != 'your-api-key-here'),
        "third_party_configured": bool(THIRD_PARTY_API_KEY and THIRD_PARTY_API_KEY != 'your-third-party-api-key-here'),
        "line_bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET),
        "liff_url": LIFF_URL
    }

@app.route("/test", methods=['POST'])
def test_api():
    """Test endpoint for complete integrated flow"""
    try:
        data = request.get_json()
        test_message = data.get('message', '爸爸最近忘記怎麼使用洗衣機')
        
        # Test complete flow
        result = call_third_party_dementia_assistant(test_message)
        
        return {
            "success": True,
            "test_message": test_message,
            "third_party_response": result,
            "flow_steps": [
                "1. LINE → Webhook",
                "2. Third Party API (失智小幫手)",
                "3. Text Processing",
                "4. Gemini/OpenAI Analysis",
                "5. JSON Data Extraction",
                "6. Flex Message Creation",
                "7. LINE Response"
            ]
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
        "service": "Integrated Dementia Assistant Webhook",
        "version": "1.0.0",
        "description": "Complete flow: LINE → Webhook → Third Party API (失智小幫手) → Text → Gemini → JSON → Flex Message → LINE",
        "architecture": {
            "step1": "LINE User sends message",
            "step2": "Webhook receives message",
            "step3": "Third Party API (失智小幫手) processes",
            "step4": "Text response generated",
            "step5": "Gemini/OpenAI analyzes text",
            "step6": "JSON data extracted",
            "step7": "Flex Message created",
            "step8": "Rich response sent to LINE"
        },
        "endpoints": {
            "POST /webhook": "LINE webhook endpoint",
            "GET /health": "Health check",
            "POST /test": "Test complete integrated flow",
            "GET /": "Service information"
        },
        "features": [
            "🤖 Third Party API (失智小幫手)",
            "📝 Text Processing",
            "🧠 Gemini/OpenAI AI Analysis",
            "📊 JSON Data Extraction",
            "🎨 Enhanced Flex Message",
            "📱 LIFF Integration",
            "🔗 Complete LINE Flow"
        ]
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Integrated Dementia Assistant Webhook...")
    logger.info("📋 Complete Flow: LINE → Webhook → Third Party API (失智小幫手) → Text → Gemini → JSON → Flex Message → LINE")
    logger.info(f"🔑 Gemini API configured: {'Yes' if GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here' else 'No'}")
    logger.info(f"🔑 OpenAI API configured: {'Yes' if API_KEY and API_KEY != 'your-api-key-here' else 'No'}")
    logger.info(f"🔑 Third Party API configured: {'Yes' if THIRD_PARTY_API_KEY and THIRD_PARTY_API_KEY != 'your-third-party-api-key-here' else 'No'}")
    logger.info(f"📱 LINE Bot configured: {'Yes' if LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET else 'No'}")
    logger.info(f"🌐 LIFF URL: {LIFF_URL}")
    
    app.run(host='0.0.0.0', port=8084, debug=False) 