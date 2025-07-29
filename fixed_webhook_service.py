from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import json
import os
from typing import Optional

app = FastAPI(title="LINE Bot 失智症分析系統", version="2.0")

# 環境變數
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
GEMINI_KEY = os.getenv('AISTUDIO_API_KEY', '')

@app.get("/")
def read_root():
    return {
        "message": "LINE Bot 失智症分析系統",
        "status": "running",
        "webhook_ready": True,
        "secrets_check": {
            "LINE_TOKEN": "✅ 已設定" if LINE_TOKEN else "❌ 未設定",
            "LINE_SECRET": "✅ 已設定" if LINE_SECRET else "❌ 未設定",
            "GEMINI_KEY": "✅ 已設定" if GEMINI_KEY else "❌ 未設定"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "webhook": "ready"}

@app.post("/webhook")
async def line_webhook(request: Request):
    """LINE Bot Webhook 端點 - 修復版"""
    try:
        print("📨 收到 LINE webhook 請求")
        
        # 讀取請求內容
        body = await request.body()
        print(f"📝 請求內容: {body.decode('utf-8')[:200]}...")
        
        # 解析 JSON
        try:
            webhook_data = json.loads(body.decode('utf-8'))
            events = webhook_data.get('events', [])
            print(f"🎯 收到 {len(events)} 個事件")
            
            # 處理每個事件
            for event in events:
                event_type = event.get('type', 'unknown')
                print(f"📋 事件類型: {event_type}")
                
                if event_type == 'message':
                    message = event.get('message', {})
                    if message.get('type') == 'text':
                        user_text = message.get('text', '')
                        print(f"💬 使用者訊息: {user_text}")
                        
                        # 這裡可以加入實際的分析邏輯
                        # 目前先記錄，確保 webhook 正常工作
                        
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
        
        # 重要：必須回傳 200 狀態碼
        print("✅ Webhook 處理完成，回傳 200")
        return JSONResponse(
            status_code=200, 
            content={"status": "ok", "message": "webhook received"}
        )
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        # 即使有錯誤，也要回傳 200 避免 LINE 重試
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": str(e)}
        )

@app.get("/test-webhook")  
def test_webhook():
    """測試 webhook 功能"""
    return {
        "message": "Webhook 測試端點",
        "instructions": "請使用 POST 方法測試 /webhook",
        "expected_response": "200 OK"
    }

@app.post("/test-webhook")
async def test_webhook_post(request: Request):
    """測試 POST webhook"""
    try:
        body = await request.body()
        return JSONResponse(
            status_code=200,
            content={"status": "success", "received": body.decode('utf-8')[:100]}
        )
    except Exception as e:
        return JSONResponse(
            status_code=200,
            content={"status": "ok", "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 啟動修復版 LINE Bot Webhook 服務")
    print("✅ Webhook 端點: /webhook (確保回傳 200)")
    uvicorn.run(app, host="0.0.0.0", port=8000)
