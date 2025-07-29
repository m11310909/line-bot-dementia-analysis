from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="XAI Flex Message API", version="1.0.0")

# Simple in-memory knowledge base
KNOWLEDGE_BASE = {
    "dementia": [
        {
            "chunk_id": "D001",
            "title": "記憶力減退影響日常生活",
            "content": "忘記剛發生的事情、重複詢問同樣問題、需要依賴記憶輔助工具。",
            "confidence_score": 0.95,
            "keywords": ["記憶力", "健忘", "重複詢問"],
            "tags": ["十大警訊", "早期症狀"]
        }
    ],
    "ltc": [
        {
            "chunk_id": "L001", 
            "title": "長照2.0服務申請流程",
            "content": "撥打1966長照專線或至長照管理中心申請評估。",
            "confidence_score": 0.97,
            "keywords": ["長照2.0", "1966專線"],
            "tags": ["長照服務", "申請指南"]
        }
    ]
}

class AnalyzeRequest(BaseModel):
    query: str
    module: str = "hybrid"
    max_chunks: int = 5

@app.get("/")
async def root():
    return {"message": "XAI Flex Message API", "docs": "/docs"}

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "services": {"api": "running"}
    }

@app.post("/api/v1/analyze/{module}")
async def analyze_query(module: str, request: AnalyzeRequest):
    try:
        logger.info(f"查詢: {request.query}, 模組: {module}")
        
        # Simple keyword matching
        results = []
        search_modules = [module] if module != "hybrid" else ["dementia", "ltc"]
        
        for search_module in search_modules:
            if search_module in KNOWLEDGE_BASE:
                for item in KNOWLEDGE_BASE[search_module]:
                    # Simple matching logic
                    if any(keyword in request.query for keyword in item["keywords"]):
                        results.append({
                            "chunk_id": item["chunk_id"],
                            "module_id": search_module,
                            "chunk_type": "info",
                            "title": item["title"],
                            "content": item["content"],
                            "confidence_score": item["confidence_score"],
                            "keywords": item["keywords"],
                            "tags": item["tags"],
                            "explanation_data": {
                                "similarity_score": 0.8,
                                "authority_level": 0.9
                            }
                        })
        
        return {
            "chunks": results[:request.max_chunks],
            "total_found": len(results),
            "query_analysis": {"original_query": request.query},
            "processing_time": 0.1
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/flex-message")
async def generate_flex_message(chunk_ids: List[str]):
    try:
        return {
            "flex_message": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical", 
                    "contents": [
                        {
                            "type": "text",
                            "text": "失智照護資訊",
                            "weight": "bold",
                            "size": "lg"
                        },
                        {
                            "type": "text", 
                            "text": "相關資訊已為您準備完成",
                            "size": "sm",
                            "wrap": True
                        }
                    ]
                }
            },
            "fallback_text": "失智照護資訊",
            "metadata": {"generated_at": datetime.now().isoformat()}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
