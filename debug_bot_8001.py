from fastapi import FastAPI, Request
import uvicorn
import json
import os

app = FastAPI()

LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')

@app.get("/")
def root():
    return {
        "status": "running on port 8001",
        "line_token_exists": bool(LINE_TOKEN),
        "webhook_url": "需要更新為 :8001/webhook"
    }

@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        webhook_data = json.loads(body.decode('utf-8'))
        
        print("=" * 50)
        print("📨 收到 LINE webhook 請求")
        
        for event in webhook_data.get('events', []):
            if event.get('type') == 'message':
                message = event.get('message', {})
                user_text = message.get('text', '')
                reply_token = event.get('replyToken')
                
                print(f"👤 使用者訊息: '{user_text}'")
                print(f"🔄 Reply Token: {reply_token}")
                print(f"💰 LINE_TOKEN: {'✅ 存在' if LINE_TOKEN else '❌ 未設定'}")
                
        print("=" * 50)
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return {"status": "ok"}

if __name__ == "__main__":
    print("🚀 啟動除錯版 LINE Bot (Port 8001)")
    uvicorn.run(app, host="0.0.0.0", port=8001)
