from fastapi import FastAPI, Request
import uvicorn
import json
import os

app = FastAPI()

LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')

@app.get("/")
def root():
    return {
        "status": "running",
        "line_token_exists": bool(LINE_TOKEN),
        "line_token_preview": LINE_TOKEN[:20] + "..." if LINE_TOKEN else "未設定"
    }

@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        webhook_data = json.loads(body.decode('utf-8'))
        
        print("=" * 50)
        print("📨 收到 LINE webhook 請求")
        print(f"完整資料: {json.dumps(webhook_data, indent=2, ensure_ascii=False)}")
        
        for event in webhook_data.get('events', []):
            print(f"事件類型: {event.get('type')}")
            if event.get('type') == 'message':
                message = event.get('message', {})
                user_text = message.get('text', '')
                reply_token = event.get('replyToken')
                
                print(f"👤 使用者訊息: '{user_text}'")
                print(f"🔄 Reply Token: {reply_token}")
                print(f"💰 LINE_TOKEN 存在: {bool(LINE_TOKEN)}")
                
                if not LINE_TOKEN:
                    print("❌ 無法回覆：LINE_TOKEN 未設定")
                else:
                    print("✅ 準備發送回覆...")
                    # 這裡先不實際發送，只是記錄
                    
        print("=" * 50)
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return {"status": "ok"}

if __name__ == "__main__":
    print("🚀 啟動除錯版 LINE Bot")
    print(f"LINE_TOKEN 狀態: {'✅ 已設定' if LINE_TOKEN else '❌ 未設定'}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
