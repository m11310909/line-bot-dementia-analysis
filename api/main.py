from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import asyncio
from api.modules.m1.analyzer import analyze_symptoms
from api.core.genai_client import genai_client

app = FastAPI(title="XAI Flex Message API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    user_input: str
    user_id: str = "anonymous"

class AnalysisResponse(BaseModel):
    success: bool
    data: dict = None
    error: str = None

@app.post("/api/m1/analyze", response_model=AnalysisResponse)
async def analyze_m1(request: AnalysisRequest):
    """M1 症狀分析端點"""
    try:
        if not request.user_input.strip():
            raise HTTPException(status_code=400, detail="用戶輸入不能為空")
        
        if len(request.user_input) > 500:
            raise HTTPException(status_code=400, detail="輸入內容過長")
        
        result = await analyze_symptoms(request.user_input)
        
        return AnalysisResponse(success=True, data=result)
        
    except Exception as e:
        return AnalysisResponse(success=False, error=str(e))

@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy", "service": "XAI Flex Message API"}

@app.on_event("shutdown")
async def shutdown_event():
    """清理資源"""
    await genai_client.close()

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False, workers=1)
