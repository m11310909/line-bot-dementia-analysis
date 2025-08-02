#!/usr/bin/env python3
"""
BoN-MAV Service - Phase 3 Advanced Features
Bag of Networks - Multi-Aspect Validation system
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
        logging.FileHandler('/app/logs/bon-mav.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BoN-MAV Service",
    description="Bag of Networks - Multi-Aspect Validation system for dementia analysis",
    version="3.0.0"
)

# Pydantic models
class MAVRequest(BaseModel):
    text: str
    user_id: str
    session_id: Optional[str] = None
    networks: List[str] = ["symptom", "severity", "context", "temporal"]
    validation_mode: str = "ensemble"  # ensemble, individual, weighted

class MAVResponse(BaseModel):
    success: bool
    network_results: Dict[str, Any]
    ensemble_result: Dict[str, Any]
    validation_score: float
    confidence_intervals: Dict[str, List[float]]
    recommendations: List[str]
    timestamp: datetime

class BoNMAVEngine:
    """Bag of Networks - Multi-Aspect Validation Engine"""
    
    def __init__(self):
        self.networks = {
            "symptom": self._symptom_network,
            "severity": self._severity_network,
            "context": self._context_network,
            "temporal": self._temporal_network,
            "behavioral": self._behavioral_network,
            "cognitive": self._cognitive_network
        }
        self.network_weights = self._initialize_network_weights()
        self.validation_rules = self._initialize_validation_rules()
        logger.info("✅ BoN-MAV Engine initialized")
    
    def _initialize_network_weights(self) -> Dict[str, float]:
        """Initialize weights for each network"""
        return {
            "symptom": 0.25,
            "severity": 0.20,
            "context": 0.15,
            "temporal": 0.15,
            "behavioral": 0.15,
            "cognitive": 0.10
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize validation rules for each network"""
        return {
            "symptom": {
                "memory_keywords": ["忘記", "記憶", "重複", "記不住"],
                "language_keywords": ["語言", "說話", "表達", "詞彙"],
                "orientation_keywords": ["迷路", "方向", "地點", "時間"],
                "judgment_keywords": ["判斷", "決定", "選擇", "邏輯"],
                "confidence_threshold": 0.6
            },
            "severity": {
                "mild_indicators": ["偶爾", "輕微", "一點點", "剛開始"],
                "moderate_indicators": ["經常", "明顯", "影響", "困難"],
                "severe_indicators": ["嚴重", "完全", "無法", "依賴"],
                "confidence_threshold": 0.7
            },
            "context": {
                "family_context": ["家人", "爸爸", "媽媽", "爺爺", "奶奶"],
                "daily_context": ["生活", "工作", "日常", "家務"],
                "social_context": ["朋友", "鄰居", "同事", "社交"],
                "medical_context": ["醫生", "醫院", "檢查", "治療"],
                "confidence_threshold": 0.5
            },
            "temporal": {
                "recent_indicators": ["最近", "這幾天", "上週", "一個月"],
                "progressive_indicators": ["越來越", "逐漸", "慢慢", "持續"],
                "sudden_indicators": ["突然", "一下子", "瞬間", "立即"],
                "confidence_threshold": 0.6
            },
            "behavioral": {
                "agitation_keywords": ["激動", "煩躁", "不安", "焦慮"],
                "apathy_keywords": ["冷漠", "無興趣", "退縮", "被動"],
                "psychosis_keywords": ["妄想", "幻覺", "懷疑", "被害"],
                "confidence_threshold": 0.6
            },
            "cognitive": {
                "attention_keywords": ["注意力", "專注", "分心", "集中"],
                "executive_keywords": ["計劃", "組織", "執行", "控制"],
                "visuospatial_keywords": ["空間", "視覺", "方向", "距離"],
                "confidence_threshold": 0.6
            }
        }
    
    def validate_multi_aspect(self, text: str, requested_networks: List[str], mode: str = "ensemble") -> Dict[str, Any]:
        """Perform multi-aspect validation using Bag of Networks"""
        try:
            network_results = {}
            total_confidence = 0
            validated_count = 0
            
            # Run each requested network
            for network_name in requested_networks:
                if network_name in self.networks:
                    network_result = self.networks[network_name](text)
                    network_results[network_name] = network_result
                    
                    if network_result.get("validated", False):
                        validated_count += 1
                        total_confidence += network_result.get("confidence", 0)
                else:
                    network_results[network_name] = {
                        "validated": False,
                        "confidence": 0,
                        "reason": f"Network '{network_name}' not supported"
                    }
            
            # Calculate ensemble result based on mode
            if mode == "ensemble":
                ensemble_result = self._calculate_ensemble_result(network_results)
            elif mode == "weighted":
                ensemble_result = self._calculate_weighted_result(network_results)
            else:  # individual
                ensemble_result = self._calculate_individual_result(network_results)
            
            # Calculate validation metrics
            validation_score = validated_count / len(requested_networks) if requested_networks else 0
            confidence_intervals = self._calculate_confidence_intervals(network_results)
            
            # Generate recommendations
            recommendations = self._generate_mav_recommendations(network_results, validation_score)
            
            return {
                "success": True,
                "network_results": network_results,
                "ensemble_result": ensemble_result,
                "validation_score": validation_score,
                "confidence_intervals": confidence_intervals,
                "recommendations": recommendations,
                "validated_count": validated_count,
                "total_networks": len(requested_networks),
                "mode": mode
            }
            
        except Exception as e:
            logger.error(f"MAV validation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "network_results": {},
                "ensemble_result": {},
                "validation_score": 0,
                "confidence_intervals": {},
                "recommendations": ["驗證過程發生錯誤"]
            }
    
    def _symptom_network(self, text: str) -> Dict[str, Any]:
        """Symptom network validation"""
        rules = self.validation_rules["symptom"]
        
        # Check each symptom category
        memory_score = sum(1 for kw in rules["memory_keywords"] if kw in text)
        language_score = sum(1 for kw in rules["language_keywords"] if kw in text)
        orientation_score = sum(1 for kw in rules["orientation_keywords"] if kw in text)
        judgment_score = sum(1 for kw in rules["judgment_keywords"] if kw in text)
        
        total_symptoms = memory_score + language_score + orientation_score + judgment_score
        confidence = min(1.0, total_symptoms / 4.0)  # Normalize to 0-1
        
        validated = confidence >= rules["confidence_threshold"]
        
        symptom_categories = {
            "memory": memory_score,
            "language": language_score,
            "orientation": orientation_score,
            "judgment": judgment_score
        }
        
        return {
            "validated": validated,
            "confidence": confidence,
            "symptom_categories": symptom_categories,
            "total_symptoms": total_symptoms,
            "reason": f"症狀網路驗證: {total_symptoms} 個症狀類別"
        }
    
    def _severity_network(self, text: str) -> Dict[str, Any]:
        """Severity network validation"""
        rules = self.validation_rules["severity"]
        
        mild_score = sum(1 for kw in rules["mild_indicators"] if kw in text)
        moderate_score = sum(1 for kw in rules["moderate_indicators"] if kw in text)
        severe_score = sum(1 for kw in rules["severe_indicators"] if kw in text)
        
        total_indicators = mild_score + moderate_score + severe_score
        
        if total_indicators == 0:
            severity = "unknown"
            confidence = 0
        elif severe_score > moderate_score and severe_score > mild_score:
            severity = "severe"
            confidence = 0.8
        elif moderate_score > mild_score:
            severity = "moderate"
            confidence = 0.7
        else:
            severity = "mild"
            confidence = 0.6
        
        validated = confidence >= rules["confidence_threshold"]
        
        return {
            "validated": validated,
            "confidence": confidence,
            "severity": severity,
            "indicators": {
                "mild": mild_score,
                "moderate": moderate_score,
                "severe": severe_score
            },
            "reason": f"嚴重程度網路驗證: {severity} 程度"
        }
    
    def _context_network(self, text: str) -> Dict[str, Any]:
        """Context network validation"""
        rules = self.validation_rules["context"]
        
        family_score = sum(1 for kw in rules["family_context"] if kw in text)
        daily_score = sum(1 for kw in rules["daily_context"] if kw in text)
        social_score = sum(1 for kw in rules["social_context"] if kw in text)
        medical_score = sum(1 for kw in rules["medical_context"] if kw in text)
        
        total_contexts = family_score + daily_score + social_score + medical_score
        confidence = min(1.0, total_contexts / 4.0)  # Normalize to 0-1
        
        validated = confidence >= rules["confidence_threshold"]
        
        context_categories = {
            "family": family_score,
            "daily": daily_score,
            "social": social_score,
            "medical": medical_score
        }
        
        return {
            "validated": validated,
            "confidence": confidence,
            "context_categories": context_categories,
            "total_contexts": total_contexts,
            "reason": f"情境網路驗證: {total_contexts} 個情境類別"
        }
    
    def _temporal_network(self, text: str) -> Dict[str, Any]:
        """Temporal network validation"""
        rules = self.validation_rules["temporal"]
        
        recent_score = sum(1 for kw in rules["recent_indicators"] if kw in text)
        progressive_score = sum(1 for kw in rules["progressive_indicators"] if kw in text)
        sudden_score = sum(1 for kw in rules["sudden_indicators"] if kw in text)
        
        total_temporal = recent_score + progressive_score + sudden_score
        confidence = min(1.0, total_temporal / 3.0)  # Normalize to 0-1
        
        validated = confidence >= rules["confidence_threshold"]
        
        temporal_patterns = {
            "recent": recent_score,
            "progressive": progressive_score,
            "sudden": sudden_score
        }
        
        return {
            "validated": validated,
            "confidence": confidence,
            "temporal_patterns": temporal_patterns,
            "total_temporal": total_temporal,
            "reason": f"時間網路驗證: {total_temporal} 個時間模式"
        }
    
    def _behavioral_network(self, text: str) -> Dict[str, Any]:
        """Behavioral network validation"""
        rules = self.validation_rules["behavioral"]
        
        agitation_score = sum(1 for kw in rules["agitation_keywords"] if kw in text)
        apathy_score = sum(1 for kw in rules["apathy_keywords"] if kw in text)
        psychosis_score = sum(1 for kw in rules["psychosis_keywords"] if kw in text)
        
        total_behavioral = agitation_score + apathy_score + psychosis_score
        confidence = min(1.0, total_behavioral / 3.0)  # Normalize to 0-1
        
        validated = confidence >= rules["confidence_threshold"]
        
        behavioral_patterns = {
            "agitation": agitation_score,
            "apathy": apathy_score,
            "psychosis": psychosis_score
        }
        
        return {
            "validated": validated,
            "confidence": confidence,
            "behavioral_patterns": behavioral_patterns,
            "total_behavioral": total_behavioral,
            "reason": f"行為網路驗證: {total_behavioral} 個行為模式"
        }
    
    def _cognitive_network(self, text: str) -> Dict[str, Any]:
        """Cognitive network validation"""
        rules = self.validation_rules["cognitive"]
        
        attention_score = sum(1 for kw in rules["attention_keywords"] if kw in text)
        executive_score = sum(1 for kw in rules["executive_keywords"] if kw in text)
        visuospatial_score = sum(1 for kw in rules["visuospatial_keywords"] if kw in text)
        
        total_cognitive = attention_score + executive_score + visuospatial_score
        confidence = min(1.0, total_cognitive / 3.0)  # Normalize to 0-1
        
        validated = confidence >= rules["confidence_threshold"]
        
        cognitive_patterns = {
            "attention": attention_score,
            "executive": executive_score,
            "visuospatial": visuospatial_score
        }
        
        return {
            "validated": validated,
            "confidence": confidence,
            "cognitive_patterns": cognitive_patterns,
            "total_cognitive": total_cognitive,
            "reason": f"認知網路驗證: {total_cognitive} 個認知模式"
        }
    
    def _calculate_ensemble_result(self, network_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ensemble result from all networks"""
        valid_results = [result for result in network_results.values() if result.get("validated", False)]
        
        if not valid_results:
            return {
                "ensemble_confidence": 0,
                "ensemble_validated": False,
                "reason": "沒有網路通過驗證"
            }
        
        total_confidence = sum(result.get("confidence", 0) for result in valid_results)
        ensemble_confidence = total_confidence / len(valid_results)
        
        return {
            "ensemble_confidence": ensemble_confidence,
            "ensemble_validated": ensemble_confidence >= 0.6,
            "valid_networks": len(valid_results),
            "reason": f"集成驗證: {len(valid_results)} 個網路通過驗證"
        }
    
    def _calculate_weighted_result(self, network_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate weighted result based on network weights"""
        weighted_confidence = 0
        total_weight = 0
        
        for network_name, result in network_results.items():
            if network_name in self.network_weights:
                weight = self.network_weights[network_name]
                confidence = result.get("confidence", 0)
                weighted_confidence += weight * confidence
                total_weight += weight
        
        if total_weight == 0:
            return {
                "weighted_confidence": 0,
                "weighted_validated": False,
                "reason": "沒有有效的網路權重"
            }
        
        final_confidence = weighted_confidence / total_weight
        
        return {
            "weighted_confidence": final_confidence,
            "weighted_validated": final_confidence >= 0.6,
            "total_weight": total_weight,
            "reason": f"權重驗證: 加權信心度 {final_confidence:.2f}"
        }
    
    def _calculate_individual_result(self, network_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate individual result for each network"""
        individual_results = {}
        
        for network_name, result in network_results.items():
            individual_results[network_name] = {
                "validated": result.get("validated", False),
                "confidence": result.get("confidence", 0),
                "reason": result.get("reason", "未知")
            }
        
        return {
            "individual_results": individual_results,
            "validated_networks": [name for name, result in individual_results.items() if result["validated"]],
            "reason": "個別網路驗證完成"
        }
    
    def _calculate_confidence_intervals(self, network_results: Dict[str, Any]) -> Dict[str, List[float]]:
        """Calculate confidence intervals for each network"""
        intervals = {}
        
        for network_name, result in network_results.items():
            confidence = result.get("confidence", 0)
            # Simple confidence interval calculation
            lower = max(0, confidence - 0.1)
            upper = min(1, confidence + 0.1)
            intervals[network_name] = [lower, upper]
        
        return intervals
    
    def _generate_mav_recommendations(self, network_results: Dict[str, Any], validation_score: float) -> List[str]:
        """Generate recommendations based on MAV results"""
        recommendations = []
        
        if validation_score < 0.5:
            recommendations.append("建議提供更詳細的症狀描述以改善驗證準確性")
        
        # Check specific network recommendations
        for network_name, result in network_results.items():
            if not result.get("validated", False):
                if network_name == "symptom":
                    recommendations.append("建議描述更多具體症狀")
                elif network_name == "severity":
                    recommendations.append("建議提供症狀嚴重程度的具體描述")
                elif network_name == "context":
                    recommendations.append("建議提供更多情境背景資訊")
                elif network_name == "temporal":
                    recommendations.append("建議提供症狀發生的時間模式")
        
        if validation_score >= 0.8:
            recommendations.append("驗證結果良好，可以進行進一步的專業分析")
        
        if not recommendations:
            recommendations.append("驗證通過，建議尋求專業醫療評估")
        
        return recommendations

# Initialize MAV engine
mav_engine = BoNMAVEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BoN-MAV Service",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "available_networks": list(mav_engine.networks.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "bon-mav",
        "version": "3.0.0",
        "networks_loaded": len(mav_engine.networks),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/validate")
async def validate_multi_aspect(request: MAVRequest):
    """Perform multi-aspect validation"""
    try:
        logger.info(f"🔍 MAV Validation: {request.networks} for user {request.user_id}")
        
        result = mav_engine.validate_multi_aspect(
            request.text, 
            request.networks, 
            request.validation_mode
        )
        
        logger.info(f"✅ MAV Validation completed with score: {result.get('validation_score', 0):.2f}")
        
        return MAVResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ MAV Validation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/networks")
async def list_networks():
    """List available validation networks"""
    return {
        "networks": list(mav_engine.networks.keys()),
        "descriptions": {
            "symptom": "症狀網路驗證",
            "severity": "嚴重程度網路驗證",
            "context": "情境網路驗證",
            "temporal": "時間網路驗證",
            "behavioral": "行為網路驗證",
            "cognitive": "認知網路驗證"
        },
        "weights": mav_engine.network_weights
    }

@app.get("/rules")
async def get_validation_rules():
    """Get validation rules for each network"""
    return {
        "rules": mav_engine.validation_rules,
        "total_networks": len(mav_engine.networks)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008) 