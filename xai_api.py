"""
XAI Flex Message API 端點實作
整合 RAG 檢索結果與 Flex Message 視覺化
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import asyncio
import logging
from datetime import datetime
import json

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="失智照護 XAI Flex Message API",
    description="提供可解釋性視覺化的失智症與長照資訊檢索服務",
    version="1.0.0"
)

# === Request/Response Models ===

class AnalyzeRequest(BaseModel):
    """分析請求模型"""
    query: str = Field(..., description="使用者查詢", min_length=1, max_length=500)
    module: Optional[str] = Field("hybrid", description="指定模組：dementia, ltc, hybrid")
    language: str = Field("zh-TW", description="語言：zh-TW, zh-CN, en")
    max_chunks: int = Field(5, description="最大返回 chunk 數量", ge=1, le=10)
    include_explanation: bool = Field(True, description="是否包含 XAI 解釋")
    user_context: Optional[Dict[str, Any]] = Field(None, description="使用者上下文")

class HealthCheckResponse(BaseModel):
    """健康檢查響應"""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]

# === Core API Endpoints ===

@app.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    """系統健康檢查"""
    try:
        services_status = {
            'api': 'healthy',
            'server': 'running'
        }
        
        return HealthCheckResponse(
            status='healthy',
            timestamp=datetime.now(),
            version='1.0.0',
            services=services_status
        )
        
    except Exception as e:
        logger.error(f"健康檢查失敗：{str(e)}")
        return HealthCheckResponse(
            status='unhealthy',
            timestamp=datetime.now(),
            version='1.0.0',
            services={'error': str(e)}
        )

@app.get("/")
async def root():
    """根路徑"""
    return {"message": "XAI Flex Message API is running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
