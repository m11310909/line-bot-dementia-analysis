#!/usr/bin/env python3
"""
Simple Third-Party API Webhook
Direct integration with third-party API for LINE bot responses
"""

import os
import json
import logging
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# Third-party API Configuration
THIRD_PARTY_API_URL = os.getenv('THIRD_PARTY_API_URL', 'https://api.openai.com/v1/chat/completions')
THIRD_PARTY_API_KEY = os.getenv('THIRD_PARTY_API_KEY', 'your-api-key-here')

app = Flask(__name__)

# Initialize LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def call_third_party_api(user_message):
    """
    Call third-party API directly with user message
    Returns the API response as text
    """
    try:
        # Example using OpenAI API (you can modify for your specific API)
        headers = {
            'Authorization': f'Bearer {THIRD_PARTY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant. Answer in Traditional Chinese.'
                },
                {
                    'role': 'user',
                    'content': user_message
                }
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        logger.info(f"🔄 Calling third-party API: {THIRD_PARTY_API_URL}")
        response = requests.post(THIRD_PARTY_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            api_response = result['choices'][0]['message']['content']
            logger.info(f"✅ Third-party API response: {api_response[:100]}...")
            return api_response
        else:
            logger.error(f"❌ Third-party API error: {response.status_code} - {response.text}")
            return f"抱歉，API 服務暫時無法使用。錯誤代碼: {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error("❌ Third-party API timeout")
        return "抱歉，API 回應超時，請稍後再試。"
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Third-party API request error: {e}")
        return "抱歉，API 連線發生錯誤，請稍後再試。"
    except Exception as e:
        logger.error(f"❌ Third-party API unexpected error: {e}")
        return "抱歉，發生未預期的錯誤，請稍後再試。"

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
    return {
        "status": "healthy",
        "service": "Simple Third-Party API Webhook",
        "line_bot_configured": bool(LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET),
        "third_party_api_configured": bool(THIRD_PARTY_API_URL and THIRD_PARTY_API_KEY)
    }

@app.route("/test", methods=['POST'])
def test_api():
    """Test endpoint for API functionality"""
    try:
        data = request.get_json()
        test_message = data.get('message', 'Hello, how are you?')
        
        api_response = call_third_party_api(test_message)
        
        return {
            "status": "success",
            "input": test_message,
            "output": api_response,
            "api_url": THIRD_PARTY_API_URL
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }, 500

if __name__ == "__main__":
    logger.info("🚀 Starting Simple Third-Party API Webhook...")
    logger.info(f"📍 Third-party API URL: {THIRD_PARTY_API_URL}")
    logger.info(f"🔑 API Key configured: {'Yes' if THIRD_PARTY_API_KEY else 'No'}")
    
    app.run(host='0.0.0.0', port=8082, debug=False) 