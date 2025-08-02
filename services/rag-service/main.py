#!/usr/bin/env python3
"""
Dockerized RAG Service
Enhanced for microservices architecture
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/rag-service.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG Service - Dockerized",
    description="Microservices-based RAG for dementia knowledge retrieval",
    version="3.0.0"
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.5

class QueryResponse(BaseModel):
    success: bool
    results: List[Dict[str, Any]]
    confidence: float
    timestamp: datetime

# Initialize RAG engine
class RAGEngine:
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.vector_index = None  # Will be initialized with actual vector DB
        logger.info("✅ RAG Engine initialized")
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize knowledge base with dementia care information"""
        return {
            "warning_signs": {
                "記憶力減退": "經常忘記最近發生的事情，重複問同樣的問題",
                "語言困難": "找不到正確的詞彙，說話時停頓或猶豫",
                "迷路": "在熟悉的地方迷路，忘記回家的路",
                "判斷力下降": "做決定時出現困難，無法處理複雜情況",
                "情緒變化": "情緒不穩定，容易焦慮或憂鬱"
            },
            "care_guidelines": {
                "早期照護": "建立規律生活，保持認知活動，定期健康檢查",
                "中期照護": "提供安全環境，協助日常生活，尋求專業支援",
                "晚期照護": "全面照護支援，舒適照護，家屬心理支持"
            },
            "resources": {
                "醫療資源": "失智症門診、神經科醫師、精神科醫師",
                "照護服務": "居家照護、日間照護、機構照護",
                "社會支持": "失智症協會、家屬支持團體、照護者喘息服務",
                "經濟補助": "身心障礙手冊、長照服務、照護補助"
            }
        }
    
    def search_knowledge(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Search knowledge base for relevant information"""
        try:
            results = []
            total_confidence = 0
            
            # Search in warning signs
            for sign, description in self.knowledge_base["warning_signs"].items():
                if sign in query or any(word in query for word in sign.split()):
                    results.append({
                        "type": "warning_sign",
                        "title": sign,
                        "content": description,
                        "confidence": 0.8
                    })
                    total_confidence += 0.8
            
            # Search in care guidelines
            for guideline, description in self.knowledge_base["care_guidelines"].items():
                if guideline in query or any(word in query for word in guideline.split()):
                    results.append({
                        "type": "care_guideline",
                        "title": guideline,
                        "content": description,
                        "confidence": 0.7
                    })
                    total_confidence += 0.7
            
            # Search in resources
            for resource, description in self.knowledge_base["resources"].items():
                if resource in query or any(word in query for word in resource.split()):
                    results.append({
                        "type": "resource",
                        "title": resource,
                        "content": description,
                        "confidence": 0.6
                    })
                    total_confidence += 0.6
            
            # Sort by confidence and limit results
            results.sort(key=lambda x: x["confidence"], reverse=True)
            results = results[:top_k]
            
            avg_confidence = total_confidence / len(results) if results else 0
            
            return {
                "success": True,
                "results": results,
                "confidence": avg_confidence,
                "total_found": len(results)
            }
            
        except Exception as e:
            logger.error(f"Knowledge search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "confidence": 0
            }
    
    def get_relevant_knowledge(self, query: str) -> str:
        """Get relevant knowledge as text"""
        search_result = self.search_knowledge(query)
        if search_result["success"] and search_result["results"]:
            knowledge_parts = []
            for result in search_result["results"]:
                knowledge_parts.append(f"{result['title']}: {result['content']}")
            return "\n".join(knowledge_parts)
        return "未找到相關知識"

# Initialize RAG engine
rag_engine = RAGEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Service - Dockerized",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "knowledge_domains": ["warning_signs", "care_guidelines", "resources"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rag-service",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/search")
async def search_knowledge(request: QueryRequest):
    """Search knowledge base"""
    try:
        logger.info(f"🔍 Searching: {request.query[:50]}...")
        
        result = rag_engine.search_knowledge(
            request.query, 
            top_k=request.top_k
        )
        
        logger.info(f"✅ Search completed with {result.get('total_found', 0)} results")
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge/{domain}")
async def get_knowledge_domain(domain: str):
    """Get knowledge by domain"""
    try:
        if domain not in rag_engine.knowledge_base:
            raise HTTPException(status_code=400, detail=f"Domain {domain} not found")
        
        return {
            "domain": domain,
            "knowledge": rag_engine.knowledge_base[domain],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Get knowledge domain failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/domains")
async def list_domains():
    """List available knowledge domains"""
    return {
        "domains": list(rag_engine.knowledge_base.keys()),
        "descriptions": {
            "warning_signs": "失智症警訊徵兆",
            "care_guidelines": "照護指南",
            "resources": "照護資源"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006) 