from flask import Flask, request, abort
from linebot.webhook import WebhookHandler
from linebot.models import MessageEvent, TextMessage, FlexMessage, FlexContainer
from linebot import LineBotApi, WebhookHandler as V2WebhookHandler
import httpx
import asyncio
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot configuration
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

XAI_SERVICE_URL = os.getenv('XAI_SERVICE_URL', 'http://localhost:8005')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle LINE message events"""
    user_input = event.message.text
    user_id = event.source.user_id
    reply_token = event.reply_token
    
    # Process with XAI wrapper
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(process_with_xai(user_input, user_id))
    
    # Send response
    if result and result.get('confidence', 0) > 0.6:
        # Send Flex Message
        flex_json = create_flex_message(result)
        try:
            line_bot_api.reply_message(
                reply_token,
                FlexMessage(
                    alt_text=f"分析結果: {result['module']}",
                    contents=FlexContainer.new_from_json_dict(flex_json)
                )
            )
        except Exception as e:
            logger.error(f"Flex message error: {e}")
            # Fallback to text
            line_bot_api.reply_message(
                reply_token,
                TextMessage(text=result.get('bot_response', {}).get('text', '處理中...'))
            )
    else:
        # Low confidence - send text only
        line_bot_api.reply_message(
            reply_token,
            TextMessage(text="請提供更多資訊以便分析")
        )

async def process_with_xai(user_input: str, user_id: str):
    """Call XAI wrapper service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{XAI_SERVICE_URL}/api/v1/analyze",
                json={"user_input": user_input, "user_id": user_id},
                timeout=8.0
            )
            return response.json()
        except Exception as e:
            logger.error(f"XAI service error: {e}")
            return None

def create_flex_message(result):
    """Create Flex Message from XAI result"""
    module = result.get('module', 'M1')
    viz = result.get('visualization', {})
    
    if module == 'M1':
        return create_m1_flex(viz)
    # Add other modules as needed
    return create_default_flex(result)

def create_m1_flex(viz):
    """Create M1 warning signs comparison Flex Message"""
    flex_data = viz.get('flex_message', {})
    confidence = flex_data.get('confidence_bar', {})
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "AI 分析結果",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"信心度: {confidence.get('label', 'N/A')}",
                    "size": "sm",
                    "color": confidence.get('color', '#666666')
                }
            ]
        }
    }

def create_default_flex(result):
    """Create default Flex Message"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": result.get('bot_response', {}).get('text', '分析完成'),
                    "wrap": True
                }
            ]
        }
    }

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        abort(400)
    
    return 'OK'

@app.route("/health", methods=['GET'])
def health():
    return {"status": "healthy", "service": "line-bot"}

if __name__ == "__main__":
    app.run(port=8081, debug=True)
