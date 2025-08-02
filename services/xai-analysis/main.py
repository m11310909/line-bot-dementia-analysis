#!/usr/bin/env python3
"""
Dockerized XAI Analysis Service
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
        logging.FileHandler('/app/logs/xai-analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="XAI Analysis Service - Dockerized",
    description="Microservices-based XAI analysis for dementia care",
    version="3.0.0"
)

# Pydantic models
class AnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    success: bool
    analysis_result: Dict[str, Any]
    confidence: float
    modules_used: List[str]
    timestamp: datetime

# Initialize analysis modules
class XAIAnalysisEngine:
    def __init__(self):
        self.modules = {
            "M1": self._analyze_warning_signs,
            "M2": self._analyze_progression,
            "M3": self._analyze_bpsd,
            "M4": self._analyze_care_navigation
        }
    
    def analyze_comprehensive(self, user_input: str) -> Dict[str, Any]:
        """Comprehensive analysis using all modules"""
        try:
            results = {}
            total_confidence = 0
            modules_used = []
            
            for module_name, analyze_func in self.modules.items():
                try:
                    module_result = analyze_func(user_input)
                    results[module_name] = module_result
                    total_confidence += module_result.get("confidence", 0)
                    modules_used.append(module_name)
                except Exception as e:
                    logger.error(f"Module {module_name} analysis failed: {e}")
                    results[module_name] = {"error": str(e), "confidence": 0}
            
            avg_confidence = total_confidence / len(modules_used) if modules_used else 0
            
            return {
                "success": True,
                "analysis_result": results,
                "confidence": avg_confidence,
                "modules_used": modules_used,
                "summary": self._generate_summary(results),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "confidence": 0,
                "modules_used": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_warning_signs(self, user_input: str) -> Dict[str, Any]:
        """M1: Warning signs analysis"""
        # Simplified analysis - you can enhance this
        warning_signs = [
            "記憶力減退", "重複問問題", "忘記事情", "迷路", "語言困難",
            "判斷力下降", "情緒變化", "興趣喪失", "日常生活困難"
        ]
        
        matched_signs = [sign for sign in warning_signs if sign in user_input]
        confidence = len(matched_signs) / len(warning_signs) if warning_signs else 0
        
        return {
            "module": "M1",
            "matched_signs": matched_signs,
            "confidence": confidence,
            "summary": f"發現 {len(matched_signs)} 個警訊徵兆"
        }
    
    def _analyze_progression(self, user_input: str) -> Dict[str, Any]:
        """M2: Progression analysis"""
        # Simplified analysis
        stages = ["早期", "中期", "晚期"]
        detected_stage = "早期"  # Simplified logic
        
        return {
            "module": "M2",
            "detected_stage": detected_stage,
            "confidence": 0.7,
            "summary": f"評估為 {detected_stage} 階段"
        }
    
    def _analyze_bpsd(self, user_input: str) -> Dict[str, Any]:
        """M3: BPSD analysis"""
        # Simplified analysis
        bpsd_types = ["妄想", "幻覺", "激動", "憂鬱", "焦慮", "冷漠"]
        detected_types = [bpsd for bpsd in bpsd_types if bpsd in user_input]
        
        return {
            "module": "M3",
            "detected_bpsd": detected_types,
            "confidence": len(detected_types) / len(bpsd_types) if bpsd_types else 0,
            "summary": f"識別出 {len(detected_types)} 種行為症狀"
        }
    
    def _analyze_care_navigation(self, user_input: str) -> Dict[str, Any]:
        """M4: Care navigation analysis"""
        # Simplified analysis
        care_resources = ["醫療資源", "照護服務", "社會支持", "經濟補助"]
        recommended_resources = care_resources[:2]  # Simplified logic
        
        return {
            "module": "M4",
            "recommended_resources": recommended_resources,
            "confidence": 0.8,
            "summary": f"建議 {len(recommended_resources)} 項照護資源"
        }
    
    def _generate_summary(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive summary"""
        summaries = []
        for module_name, result in results.items():
            if "summary" in result:
                summaries.append(result["summary"])
        
        return "；".join(summaries) if summaries else "分析完成"

# Initialize analysis engine
analysis_engine = XAIAnalysisEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "XAI Analysis Service - Dockerized",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "modules": ["M1", "M2", "M3", "M4"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "xai-analysis",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/comprehensive-analysis")
async def analyze_comprehensive(request: AnalysisRequest):
    """Comprehensive analysis endpoint"""
    try:
        logger.info(f"📊 Analyzing: {request.text[:50]}...")
        
        result = analysis_engine.analyze_comprehensive(request.text)
        
        logger.info(f"✅ Analysis completed with confidence: {result.get('confidence', 0):.2f}")
        
        return AnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/{module_name}")
async def analyze_single_module(module_name: str, request: AnalysisRequest):
    """Single module analysis endpoint"""
    try:
        if module_name not in analysis_engine.modules:
            raise HTTPException(status_code=400, detail=f"Module {module_name} not found")
        
        analyze_func = analysis_engine.modules[module_name]
        result = analyze_func(request.text)
        
        return {
            "success": True,
            "module": module_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Single module analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/modules")
async def list_modules():
    """List available modules"""
    return {
        "modules": list(analysis_engine.modules.keys()),
        "descriptions": {
            "M1": "Warning signs analysis",
            "M2": "Progression analysis", 
            "M3": "BPSD analysis",
            "M4": "Care navigation analysis"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005) 