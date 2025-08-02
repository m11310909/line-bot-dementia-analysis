#!/usr/bin/env python3
"""
Dockerized RAG Service with GPU Acceleration
Enhanced for microservices architecture
"""

import os
import json
import logging
import torch
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss

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
    title="RAG Service - GPU Accelerated",
    description="Microservices-based RAG for dementia knowledge retrieval with GPU acceleration",
    version="3.0.0"
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    threshold: float = 0.5
    use_gpu: bool = True

class QueryResponse(BaseModel):
    success: bool
    results: List[Dict[str, Any]]
    confidence: float
    gpu_used: bool
    processing_time: float
    timestamp: datetime

# Initialize RAG engine with GPU support
class GPUAcceleratedRAGEngine:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"🚀 Using device: {self.device}")
        
        # Initialize sentence transformer
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.model.to(self.device)
        
        # Initialize knowledge base
        self.knowledge_base = self._initialize_knowledge_base()
        self.vector_index = None
        self.embeddings = None
        
        # Build vector index
        self._build_vector_index()
        
        logger.info("✅ GPU Accelerated RAG Engine initialized")
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize knowledge base with dementia care information"""
        return {
            "warning_signs": {
                "記憶力減退": "經常忘記最近發生的事情，重複問同樣的問題，這是失智症最常見的早期症狀",
                "語言困難": "找不到正確的詞彙，說話時停頓或猶豫，可能忘記簡單的詞彙",
                "迷路": "在熟悉的地方迷路，忘記回家的路，方向感變差",
                "判斷力下降": "做決定時出現困難，無法處理複雜情況，財務管理能力下降",
                "情緒變化": "情緒不穩定，容易焦慮或憂鬱，性格可能發生改變"
            },
            "care_guidelines": {
                "早期照護": "建立規律生活，保持認知活動，定期健康檢查，維持社交活動",
                "中期照護": "提供安全環境，協助日常生活，尋求專業支援，建立照護計畫",
                "晚期照護": "全面照護支援，舒適照護，家屬心理支持，安寧照護準備"
            },
            "resources": {
                "醫療資源": "失智症門診、神經科醫師、精神科醫師、記憶門診、認知功能評估",
                "照護服務": "居家照護、日間照護、機構照護、喘息服務、照護者支持",
                "社會支持": "失智症協會、家屬支持團體、照護者喘息服務、心理諮商",
                "經濟補助": "身心障礙手冊、長照服務、照護補助、醫療補助、社會福利"
            },
            "treatment_options": {
                "藥物治療": "膽鹼酶抑制劑、NMDA受體拮抗劑、抗精神病藥物、抗憂鬱藥物",
                "非藥物治療": "認知訓練、音樂治療、藝術治療、園藝治療、寵物治療",
                "生活調整": "規律作息、營養均衡、適度運動、社交活動、環境安全"
            }
        }
    
    def _build_vector_index(self):
        """Build FAISS vector index for fast similarity search"""
        try:
            # Prepare documents
            documents = []
            for domain, items in self.knowledge_base.items():
                for title, content in items.items():
                    documents.append({
                        "id": f"{domain}_{title}",
                        "domain": domain,
                        "title": title,
                        "content": content,
                        "text": f"{title}: {content}"
                    })
            
            # Generate embeddings
            texts = [doc["text"] for doc in documents]
            embeddings = self.model.encode(texts, convert_to_tensor=True, device=self.device)
            
            # Convert to numpy for FAISS
            embeddings_np = embeddings.cpu().numpy().astype('float32')
            
            # Build FAISS index
            dimension = embeddings_np.shape[1]
            self.vector_index = faiss.IndexFlatIP(dimension)
            self.vector_index.add(embeddings_np)
            
            # Store documents for retrieval
            self.documents = documents
            self.embeddings = embeddings_np
            
            logger.info(f"✅ Vector index built with {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"❌ Failed to build vector index: {e}")
            self.vector_index = None
    
    def search_knowledge_gpu(self, query: str, top_k: int = 5, threshold: float = 0.5) -> Dict[str, Any]:
        """GPU-accelerated knowledge search"""
        try:
            start_time = datetime.now()
            
            # Generate query embedding
            query_embedding = self.model.encode([query], convert_to_tensor=True, device=self.device)
            query_vector = query_embedding.cpu().numpy().astype('float32')
            
            # Search in vector index
            if self.vector_index is not None:
                scores, indices = self.vector_index.search(query_vector, top_k)
                
                results = []
                for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if score >= threshold and idx < len(self.documents):
                        doc = self.documents[idx]
                        results.append({
                            "type": doc["domain"],
                            "title": doc["title"],
                            "content": doc["content"],
                            "confidence": float(score),
                            "rank": i + 1
                        })
            else:
                # Fallback to keyword search
                results = self._keyword_search(query, top_k)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            avg_confidence = sum(r["confidence"] for r in results) / len(results) if results else 0
            
            return {
                "success": True,
                "results": results,
                "confidence": avg_confidence,
                "total_found": len(results),
                "gpu_used": self.device.type == "cuda",
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"GPU search failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": [],
                "confidence": 0,
                "gpu_used": False,
                "processing_time": 0
            }
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Fallback keyword search"""
        results = []
        query_lower = query.lower()
        
        for domain, items in self.knowledge_base.items():
            for title, content in items.items():
                if query_lower in title.lower() or query_lower in content.lower():
                    results.append({
                        "type": domain,
                        "title": title,
                        "content": content,
                        "confidence": 0.6,
                        "rank": len(results) + 1
                    })
                    if len(results) >= top_k:
                        break
        
        return results

# Initialize RAG engine
rag_engine = GPUAcceleratedRAGEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Service - GPU Accelerated",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "gpu_available": torch.cuda.is_available(),
        "device": str(rag_engine.device),
        "knowledge_domains": ["warning_signs", "care_guidelines", "resources", "treatment_options"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rag-service",
        "version": "3.0.0",
        "gpu_available": torch.cuda.is_available(),
        "device": str(rag_engine.device),
        "vector_index_ready": rag_engine.vector_index is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/search")
async def search_knowledge(request: QueryRequest):
    """GPU-accelerated knowledge search"""
    try:
        logger.info(f"🔍 GPU Search: {request.query[:50]}...")
        
        result = rag_engine.search_knowledge_gpu(
            request.query, 
            top_k=request.top_k,
            threshold=request.threshold
        )
        
        logger.info(f"✅ Search completed with {result.get('total_found', 0)} results in {result.get('processing_time', 0):.3f}s")
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/gpu-status")
async def gpu_status():
    """Get GPU status and capabilities"""
    return {
        "cuda_available": torch.cuda.is_available(),
        "device": str(rag_engine.device),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "current_device": torch.cuda.current_device() if torch.cuda.is_available() else None,
        "device_name": torch.cuda.get_device_name() if torch.cuda.is_available() else "CPU"
    }

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
            "resources": "照護資源",
            "treatment_options": "治療選項"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006) 