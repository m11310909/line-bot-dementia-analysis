# 創建 line_test_bot.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
import requests

app = Flask(__name__)

# 你的 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = 'YOUR_CHANNEL_ACCESS_TOKEN'
LINE_CHANNEL_SECRET = 'YOUR_CHANNEL_SECRET'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 如果使用者輸入「測試」，就顯示 Flex Message
    if "測試" in user_message or "test" in user_message.lower():
        # 調用你的 XAI API
        api_response = requests.post(
            'http://localhost:8001/api/v1/flex-message',
            json={'chunk_ids': ['D001']},
            headers={'Content-Type': 'application/json'}
        )

        if api_response.status_code == 200:
            flex_data = api_response.json()

            # 創建 Flex Message
            flex_message = FlexSendMessage(
                alt_text=flex_data['fallback_text'],
                contents=flex_data['flex_message']
            )

            # 發送 Flex Message
            line_bot_api.reply_message(
                event.reply_token,
                flex_message
            )
        else:
            # 錯誤處理
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="抱歉，系統發生錯誤")
            )
    else:
        # 一般回應
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="請輸入「測試」來查看失智照護資訊")
        )

if __name__ == "__main__":
    app.run(port=5000)