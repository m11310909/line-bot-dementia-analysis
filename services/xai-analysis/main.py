#!/usr/bin/env python3
"""
Dockerized XAI Analysis Service with Enhanced Visualization
Enhanced for microservices architecture
"""

import os
import json
import logging
import numpy as np
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
    title="XAI Analysis Service - Enhanced Visualization",
    description="Microservices-based XAI analysis for dementia care with enhanced visualization",
    version="3.0.0"
)

# Pydantic models
class AnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    include_visualization: bool = True

class AnalysisResponse(BaseModel):
    success: bool
    analysis_result: Dict[str, Any]
    confidence: float
    modules_used: List[str]
    visualization_data: Optional[Dict[str, Any]] = None
    explanation_path: Optional[List[str]] = None
    timestamp: datetime

# Initialize analysis modules with enhanced XAI
class EnhancedXAIAnalysisEngine:
    def __init__(self):
        self.modules = {
            "M1": self._analyze_warning_signs,
            "M2": self._analyze_progression,
            "M3": self._analyze_bpsd,
            "M4": self._analyze_care_navigation
        }
        self.explanation_templates = self._initialize_explanation_templates()
        logger.info("✅ Enhanced XAI Analysis Engine initialized")
    
    def _initialize_explanation_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize explanation templates for XAI"""
        return {
            "M1": {
                "high_confidence": "基於您描述的症状，系統識別出多個失智症警訊徵兆。這些症狀與臨床診斷標準高度吻合。",
                "medium_confidence": "您提到的症狀部分符合失智症警訊，建議進一步觀察和專業評估。",
                "low_confidence": "症狀描述較為模糊，建議提供更詳細的症狀描述或尋求專業醫療建議。"
            },
            "M2": {
                "early": "根據症狀表現，評估為早期階段。此時介入效果最佳，建議積極治療。",
                "middle": "症狀顯示已進入中期階段，需要更全面的照護計畫。",
                "late": "症狀符合晚期表現，需要專業照護團隊的全面支持。"
            },
            "M3": {
                "behavioral": "識別出行為症狀，這些症狀需要專業的照護策略。",
                "psychological": "發現心理症狀，建議尋求精神科醫師協助。",
                "mixed": "同時存在多種症狀，需要綜合治療方案。"
            },
            "M4": {
                "medical": "建議優先尋求醫療資源，進行專業診斷。",
                "care": "需要照護服務支持，建議聯繫相關機構。",
                "support": "建議尋求社會支持資源，減輕照護負擔。"
            }
        }
    
    def analyze_comprehensive(self, user_input: str, include_visualization: bool = True) -> Dict[str, Any]:
        """Comprehensive analysis using all modules with XAI visualization"""
        try:
            results = {}
            total_confidence = 0
            modules_used = []
            explanation_path = []
            
            for module_name, analyze_func in self.modules.items():
                try:
                    module_result = analyze_func(user_input)
                    results[module_name] = module_result
                    total_confidence += module_result.get("confidence", 0)
                    modules_used.append(module_name)
                    
                    # Add explanation to path
                    if module_result.get("explanation"):
                        explanation_path.append(f"{module_name}: {module_result['explanation']}")
                        
                except Exception as e:
                    logger.error(f"Module {module_name} analysis failed: {e}")
                    results[module_name] = {"error": str(e), "confidence": 0}
            
            avg_confidence = total_confidence / len(modules_used) if modules_used else 0
            
            # Generate visualization data
            visualization_data = None
            if include_visualization:
                visualization_data = self._generate_visualization_data(results, avg_confidence)
            
            return {
                "success": True,
                "analysis_result": results,
                "confidence": avg_confidence,
                "modules_used": modules_used,
                "summary": self._generate_summary(results),
                "explanation_path": explanation_path,
                "visualization_data": visualization_data,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "confidence": 0,
                "modules_used": [],
                "explanation_path": [],
                "visualization_data": None,
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_warning_signs(self, user_input: str) -> Dict[str, Any]:
        """M1: Enhanced warning signs analysis with XAI"""
        warning_signs = [
            "記憶力減退", "重複問問題", "忘記事情", "迷路", "語言困難",
            "判斷力下降", "情緒變化", "興趣喪失", "日常生活困難"
        ]
        
        matched_signs = [sign for sign in warning_signs if sign in user_input]
        confidence = len(matched_signs) / len(warning_signs) if warning_signs else 0
        
        # Generate XAI explanation
        if confidence > 0.7:
            explanation = self.explanation_templates["M1"]["high_confidence"]
        elif confidence > 0.4:
            explanation = self.explanation_templates["M1"]["medium_confidence"]
        else:
            explanation = self.explanation_templates["M1"]["low_confidence"]
        
        return {
            "module": "M1",
            "matched_signs": matched_signs,
            "confidence": confidence,
            "explanation": explanation,
            "summary": f"發現 {len(matched_signs)} 個警訊徵兆",
            "xai_features": {
                "feature_importance": {sign: 1.0 for sign in matched_signs},
                "decision_reasoning": f"基於症狀匹配度 {confidence:.2f} 進行評估"
            }
        }
    
    def _analyze_progression(self, user_input: str) -> Dict[str, Any]:
        """M2: Enhanced progression analysis with XAI"""
        # Enhanced analysis logic
        early_keywords = ["輕微", "偶爾", "初期", "剛開始"]
        middle_keywords = ["明顯", "經常", "影響", "困難"]
        late_keywords = ["嚴重", "完全", "無法", "依賴"]
        
        early_score = sum(1 for word in early_keywords if word in user_input)
        middle_score = sum(1 for word in middle_keywords if word in user_input)
        late_score = sum(1 for word in late_keywords if word in user_input)
        
        if late_score > middle_score and late_score > early_score:
            stage = "late"
            confidence = 0.8
        elif middle_score > early_score:
            stage = "middle"
            confidence = 0.7
        else:
            stage = "early"
            confidence = 0.6
        
        explanation = self.explanation_templates["M2"][stage]
        
        return {
            "module": "M2",
            "detected_stage": stage,
            "confidence": confidence,
            "explanation": explanation,
            "summary": f"評估為 {stage} 階段",
            "xai_features": {
                "stage_indicators": {
                    "early": early_score,
                    "middle": middle_score,
                    "late": late_score
                },
                "decision_reasoning": f"基於關鍵詞分析確定階段"
            }
        }
    
    def _analyze_bpsd(self, user_input: str) -> Dict[str, Any]:
        """M3: Enhanced BPSD analysis with XAI"""
        bpsd_types = ["妄想", "幻覺", "激動", "憂鬱", "焦慮", "冷漠"]
        detected_types = [bpsd for bpsd in bpsd_types if bpsd in user_input]
        
        confidence = len(detected_types) / len(bpsd_types) if bpsd_types else 0
        
        if len(detected_types) > 2:
            category = "mixed"
        elif any(t in ["妄想", "幻覺"] for t in detected_types):
            category = "psychological"
        else:
            category = "behavioral"
        
        explanation = self.explanation_templates["M3"][category]
        
        return {
            "module": "M3",
            "detected_bpsd": detected_types,
            "confidence": confidence,
            "explanation": explanation,
            "summary": f"識別出 {len(detected_types)} 種行為症狀",
            "xai_features": {
                "symptom_categories": {
                    "behavioral": [t for t in detected_types if t in ["激動", "冷漠"]],
                    "psychological": [t for t in detected_types if t in ["妄想", "幻覺"]],
                    "mood": [t for t in detected_types if t in ["憂鬱", "焦慮"]]
                },
                "decision_reasoning": f"基於症狀分類進行評估"
            }
        }
    
    def _analyze_care_navigation(self, user_input: str) -> Dict[str, Any]:
        """M4: Enhanced care navigation analysis with XAI"""
        care_resources = ["醫療資源", "照護服務", "社會支持", "經濟補助"]
        recommended_resources = care_resources[:2]  # Simplified logic
        
        # Determine primary need
        if "醫生" in user_input or "醫院" in user_input:
            primary_need = "medical"
        elif "照護" in user_input or "照顧" in user_input:
            primary_need = "care"
        else:
            primary_need = "support"
        
        explanation = self.explanation_templates["M4"][primary_need]
        
        return {
            "module": "M4",
            "recommended_resources": recommended_resources,
            "confidence": 0.8,
            "explanation": explanation,
            "summary": f"建議 {len(recommended_resources)} 項照護資源",
            "xai_features": {
                "resource_priority": {
                    "primary": primary_need,
                    "secondary": [r for r in care_resources if r not in recommended_resources]
                },
                "decision_reasoning": f"基於需求分析推薦資源"
            }
        }
    
    def _generate_visualization_data(self, results: Dict[str, Any], avg_confidence: float) -> Dict[str, Any]:
        """Generate visualization data for XAI"""
        try:
            # Confidence radar chart data
            confidence_data = {
                "labels": list(results.keys()),
                "values": [results[module].get("confidence", 0) for module in results.keys()]
            }
            
            # Module usage pie chart
            module_usage = {}
            for module_name, result in results.items():
                if "matched_signs" in result:
                    module_usage[module_name] = len(result["matched_signs"])
                elif "detected_bpsd" in result:
                    module_usage[module_name] = len(result["detected_bpsd"])
                else:
                    module_usage[module_name] = 1
            
            # Feature importance for each module
            feature_importance = {}
            for module_name, result in results.items():
                if "xai_features" in result:
                    feature_importance[module_name] = result["xai_features"]
            
            return {
                "confidence_radar": confidence_data,
                "module_usage": module_usage,
                "feature_importance": feature_importance,
                "overall_confidence": avg_confidence,
                "visualization_type": "xai_enhanced"
            }
        except Exception as e:
            logger.error(f"Visualization generation failed: {e}")
            return None
    
    def _generate_summary(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive summary with XAI insights"""
        summaries = []
        for module_name, result in results.items():
            if "summary" in result:
                summaries.append(result["summary"])
        
        return "；".join(summaries) if summaries else "分析完成"

# Initialize analysis engine
analysis_engine = EnhancedXAIAnalysisEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "XAI Analysis Service - Enhanced Visualization",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "xai_features": ["confidence_radar", "feature_importance", "explanation_path"],
        "modules": ["M1", "M2", "M3", "M4"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "xai-analysis",
        "version": "3.0.0",
        "xai_enhanced": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/comprehensive-analysis")
async def analyze_comprehensive(request: AnalysisRequest):
    """Comprehensive analysis endpoint with XAI visualization"""
    try:
        logger.info(f"📊 XAI Analysis: {request.text[:50]}...")
        
        result = analysis_engine.analyze_comprehensive(
            request.text, 
            include_visualization=request.include_visualization
        )
        
        logger.info(f"✅ XAI Analysis completed with confidence: {result.get('confidence', 0):.2f}")
        
        return AnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ XAI Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/{module_name}")
async def analyze_single_module(module_name: str, request: AnalysisRequest):
    """Single module analysis endpoint with XAI"""
    try:
        if module_name not in analysis_engine.modules:
            raise HTTPException(status_code=400, detail=f"Module {module_name} not found")
        
        analyze_func = analysis_engine.modules[module_name]
        result = analyze_func(request.text)
        
        return {
            "success": True,
            "module": module_name,
            "result": result,
            "xai_enhanced": True,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Single module analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/xai-features")
async def get_xai_features():
    """Get available XAI features"""
    return {
        "features": [
            "confidence_radar",
            "feature_importance", 
            "explanation_path",
            "decision_reasoning",
            "visualization_data"
        ],
        "modules": list(analysis_engine.modules.keys()),
        "explanations": analysis_engine.explanation_templates
    }

@app.get("/modules")
async def list_modules():
    """List available modules"""
    return {
        "modules": list(analysis_engine.modules.keys()),
        "descriptions": {
            "M1": "Warning signs analysis with XAI",
            "M2": "Progression analysis with XAI", 
            "M3": "BPSD analysis with XAI",
            "M4": "Care navigation analysis with XAI"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005) 