from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.responses import JSONResponse
import json
import asyncio
from typing import Optional

from api.services.analysis_service import AnalysisService
from api.services.gemini_service import GeminiService
from api.core.security import verify_line_signature, check_memory_usage
from api.core.config import settings
from api.core.exceptions import handle_analysis_error
from flex.builders.m1_builder import M1FlexBuilder

# 初始化服務
app = FastAPI(
    title="失智症分析 API",
    description="LINE Bot 失智症早期警訊分析系統",
    version="2.0.0"
)

analysis_service = AnalysisService()
flex_builder = M1FlexBuilder()

@app.get("/")
async def root():
    return {"message": "失智症分析系統 API v2.0", "status": "running"}

@app.get("/health")
async def health_check():
    """健康檢查"""
    try:
        check_memory_usage()
        gemini_status = analysis_service.gemini_service.health_check()
        return {
            "status": "healthy",
            "gemini_configured": gemini_status,
            "available_modules": analysis_service.get_available_modules()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/analyze/{module}")
async def analyze_input(module: str, request: Request):
    """分析用戶輸入"""
    try:
        body = await request.json()
        user_input = body.get("user_input", "")
        
        if not user_input:
            raise HTTPException(400, "缺少 user_input 參數")
        
        result = await analysis_service.analyze(module, user_input)
        return result.dict()
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"分析錯誤: {e}")
        raise handle_analysis_error(e)

@app.post("/m1-flex")
async def m1_flex_analysis(request: Request):
    """M1 模組分析並回傳 Flex Message"""
    try:
        body = await request.json()
        user_input = body.get("user_input", "")
        
        if not user_input:
            raise HTTPException(400, "缺少 user_input 參數")
        
        # 執行分析
        result = await analysis_service.analyze("m1", user_input)
        
        # 建構 Flex Message
        flex_message = flex_builder.build_analysis_result(result)
        
        return {"flex_message": flex_message}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"M1 Flex 分析錯誤: {e}")
        raise handle_analysis_error(e)

@app.post("/webhook")
async def line_webhook(
    request: Request,
    x_line_signature: Optional[str] = Header(None, alias="X-Line-Signature")
):
    """LINE Bot Webhook 端點"""
    try:
        body = await request.body()
        
        # 驗證簽名（如果有設定）
        if settings.line_channel_secret and x_line_signature:
            verify_line_signature(body, x_line_signature)
        
        # 解析請求
        webhook_data = json.loads(body.decode('utf-8'))
        events = webhook_data.get('events', [])
        
        responses = []
        for event in events:
            if event.get('type') == 'message' and event.get('message', {}).get('type') == 'text':
                response = await handle_line_message(event)
                responses.append(response)
        
        return {"responses": responses}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Webhook 錯誤: {e}")
        return JSONResponse(status_code=200, content={"status": "ok"})

async def handle_line_message(event):
    """處理 LINE 訊息事件"""
    try:
        user_message = event.get('message', {}).get('text', '').strip()
        reply_token = event.get('replyToken')
        
        if not user_message:
            return {"error": "空訊息"}
        
        # 特殊指令處理
        if user_message.lower() in ['help', '幫助', '說明']:
            flex_message = flex_builder.build_help_message()
            return {
                "replyToken": reply_token,
                "messages": [flex_message]
            }
        
        # 一般分析
        result = await analysis_service.analyze("m1", user_message)
        flex_message = flex_builder.build_analysis_result(result)
        
        return {
            "replyToken": reply_token,
            "messages": [flex_message]
        }
        
    except Exception as e:
        print(f"處理 LINE 訊息錯誤: {e}")
        # 回傳簡單錯誤訊息
        return {
            "replyToken": event.get('replyToken'),
            "messages": [{
                "type": "text",
                "text": "抱歉，系統暫時無法處理您的請求，請稍後再試。"
            }]
        }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 啟動失智症分析 API 服務於端口 {settings.api_port}")
    uvicorn.run(app, host="0.0.0.0", port=settings.api_port)
