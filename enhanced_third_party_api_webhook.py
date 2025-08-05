#!/usr/bin/env python3
"""
Enhanced Third-Party API Webhook
Supports multiple third-party APIs with direct LINE integration
"""

import os
import json
import logging
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from dotenv import load_dotenv
from third_party_api_config import API_CONFIGS

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# Third-party API Configuration
API_TYPE = os.getenv('API_TYPE', 'openai')  # openai, gemini, custom
API_KEY = os.getenv('API_KEY', 'your-api-key-here')
THIRD_PARTY_API_KEY = os.getenv('THIRD_PARTY_API_KEY', 'your-third-party-api-key-here')
GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY', 'your-google-gemini-api-key-here')

app = Flask(__name__)

# Initialize LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def call_third_party_api(user_message, api_type=API_TYPE):
    """
    Call third-party API directly with user message
    Returns the API response as text
    """
    try:
        if api_type not in API_CONFIGS:
            logger.error(f"❌ Unsupported API type: {api_type}")
            return f"抱歉，不支援的 API 類型: {api_type}"
        
        config = API_CONFIGS[api_type]['config']
        parser = API_CONFIGS[api_type]['parser']
        
        # Prepare headers with appropriate API key
        headers = {}
        api_key = API_KEY  # Default API key
        
        # Use specific API key based on API type
        if api_type == 'openai':
            api_key = API_KEY
        elif api_type == 'gemini':
            api_key = GOOGLE_GEMINI_API_KEY
        elif api_type == 'custom':
            api_key = THIRD_PARTY_API_KEY
        
        for key, value in config['headers'].items():
            if '{api_key}' in value:
                headers[key] = value.format(api_key=api_key)
            else:
                headers[key] = value
        
        # Prepare data
        data = config['data_template'].copy()
        if api_type == 'openai':
            data['messages'][1]['content'] = user_message
        elif api_type == 'gemini':
            data['contents'][0]['parts'][0]['text'] = data['contents'][0]['parts'][0]['text'].format(user_message=user_message)
        elif api_type == 'custom':
            data['message'] = user_message
        
        logger.info(f"🔄 Calling {api_type} API: {config['url']}")
        logger.info(f"📤 Sending message: {user_message[:50]}...")
        
        response = requests.post(config['url'], headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            api_response = parser(result)
            logger.info(f"✅ {api_type} API response: {api_response[:100]}...")
            return api_response
        else:
            logger.error(f"❌ {api_type} API error: {response.status_code} - {response.text}")
            return f"抱歉，{api_type} API 服務暫時無法使用。錯誤代碼: {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error(f"❌ {api_type} API timeout")
        return "抱歉，API 回應超時，請稍後再試。"
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ {api_type} API request error: {e}")
        return "抱歉，API 連線發生錯誤，請稍後再試。"
    except Exception as e:
        logger.error(f"❌ {api_type} API unexpected error: {e}")
        return f"抱歉，{api_type} API 發生未預期的錯誤: {str(e)}"

@app.route("/webhook", methods=['POST'])
def webhook():
    """LINE webhook endpoint"""
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
    user_id = event.source.user_id
    user_message = event.message.text
    reply_token = event.reply_token
    
    logger.info(f"📨 Message from {user_id}: {user_message}")
    
    try:
        # Call third-party API directly
        api_response = call_third_party_api(user_message)
        
        # Send response back to LINE
        text_message = TextSendMessage(text=api_response)
        line_bot_api.reply_message(reply_token, text_message)
        
        logger.info(f"✅ Sent response to {user_id}: {api_response[:50]}...")
        
    except Exception as e:
        logger.error(f"❌ Error handling message: {e}")
        error_message = TextSendMessage(text="抱歉，處理您的訊息時發生錯誤，請稍後再試。")
        line_bot_api.reply_message(reply_token, error_message)

@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Check API key configuration for different APIs
    openai_configured = bool(API_KEY and API_KEY != 'your-api-key-here')
    gemini_configured = bool(GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here')
    custom_configured = bool(THIRD_PARTY_API_KEY and THIRD_PARTY_API_KEY != 'your-third-party-api-key-here')
    
    return {
        "status": "healthy",
        "service": "Enhanced Third-Party API Webhook",
        "api_type": API_TYPE,
        "api_key_configured": openai_configured or gemini_configured or custom_configured,
        "openai_configured": openai_configured,
        "gemini_configured": gemini_configured,
        "custom_configured": custom_configured,
        "line_bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET),
        "supported_apis": list(API_CONFIGS.keys())
    }

@app.route("/test", methods=['POST'])
def test_api():
    """Test endpoint for API functionality"""
    try:
        data = request.get_json()
        test_message = data.get('message', 'Hello, how are you?')
        api_type = data.get('api_type', API_TYPE)
        
        api_response = call_third_party_api(test_message, api_type)
        
        return {
            "status": "success",
            "api_type": api_type,
            "input": test_message,
            "output": api_response
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }, 500

@app.route("/switch_api", methods=['POST'])
def switch_api():
    """Switch API type for testing"""
    try:
        data = request.get_json()
        new_api_type = data.get('api_type')
        
        if new_api_type not in API_CONFIGS:
            return {
                "status": "error",
                "error": f"Unsupported API type: {new_api_type}",
                "supported_apis": list(API_CONFIGS.keys())
            }, 400
        
        global API_TYPE
        API_TYPE = new_api_type
        
        return {
            "status": "success",
            "message": f"Switched to {API_TYPE} API",
            "api_type": API_TYPE
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }, 500

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Third-Party API Webhook...")
    logger.info(f"📍 API Type: {API_TYPE}")
    logger.info(f"🔑 OpenAI API Key configured: {'Yes' if API_KEY and API_KEY != 'your-api-key-here' else 'No'}")
    logger.info(f"🔑 Google Gemini API Key configured: {'Yes' if GOOGLE_GEMINI_API_KEY and GOOGLE_GEMINI_API_KEY != 'your-google-gemini-api-key-here' else 'No'}")
    logger.info(f"🔑 Third-Party API Key configured: {'Yes' if THIRD_PARTY_API_KEY and THIRD_PARTY_API_KEY != 'your-third-party-api-key-here' else 'No'}")
    logger.info(f"📋 Supported APIs: {list(API_CONFIGS.keys())}")
    
    app.run(host='0.0.0.0', port=8082, debug=False) 