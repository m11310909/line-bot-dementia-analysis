from linebot import WebhookHandler
from linebot.models import MessageEvent, TextMessage

handler = WebhookHandler("dummy_secret")

def handle_message(event):
    print("handle_message 被呼叫", event)

handler.add(MessageEvent, message=TextMessage)(handle_message)
print("已註冊 handler")

# 模擬事件
class DummyEvent:
    message = type("msg", (), {"text": "hi"})()
    source = type("src", (), {"user_id": "U123"})()
    reply_token = "token"

event = DummyEvent()
try:
    handler.handle_message(event)
except Exception as e:
    print("handler.handle_message 執行錯誤:", e)