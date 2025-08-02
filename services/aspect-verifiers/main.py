#!/usr/bin/env python3
"""
Aspect Verifiers Service - Phase 3 Advanced Features
Multi-aspect verification and validation system
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
        logging.FileHandler('/app/logs/aspect-verifiers.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Aspect Verifiers Service",
    description="Multi-aspect verification and validation system for dementia analysis",
    version="3.0.0"
)

# Pydantic models
class VerificationRequest(BaseModel):
    text: str
    user_id: str
    session_id: Optional[str] = None
    aspects: List[str] = ["symptom", "severity", "urgency", "context"]
    include_confidence: bool = True

class VerificationResponse(BaseModel):
    success: bool
    verified_aspects: Dict[str, Any]
    overall_confidence: float
    verification_score: float
    recommendations: List[str]
    timestamp: datetime

class AspectVerificationEngine:
    """Multi-aspect verification engine"""
    
    def __init__(self):
        self.aspects = {
            "symptom": self._verify_symptom,
            "severity": self._verify_severity,
            "urgency": self._verify_urgency,
            "context": self._verify_context,
            "consistency": self._verify_consistency,
            "reliability": self._verify_reliability
        }
        self.verification_rules = self._initialize_verification_rules()
        logger.info("✅ Aspect Verification Engine initialized")
    
    def _initialize_verification_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize verification rules for each aspect"""
        return {
            "symptom": {
                "keywords": ["記憶", "忘記", "迷路", "語言", "判斷", "情緒", "妄想", "幻覺"],
                "patterns": [
                    r"經常.*忘記",
                    r"重複.*問題",
                    r"找不到.*路",
                    r"說不出.*話"
                ],
                "confidence_threshold": 0.6
            },
            "severity": {
                "mild_keywords": ["偶爾", "輕微", "剛開始", "一點點"],
                "moderate_keywords": ["經常", "明顯", "影響", "困難"],
                "severe_keywords": ["嚴重", "完全", "無法", "依賴"],
                "confidence_threshold": 0.7
            },
            "urgency": {
                "high_urgency": ["危險", "緊急", "立即", "馬上", "安全"],
                "medium_urgency": ["建議", "需要", "應該", "最好"],
                "low_urgency": ["觀察", "注意", "了解", "知道"],
                "confidence_threshold": 0.5
            },
            "context": {
                "family_context": ["家人", "爸爸", "媽媽", "爺爺", "奶奶"],
                "daily_context": ["生活", "工作", "日常", "家務"],
                "social_context": ["朋友", "鄰居", "同事", "社交"],
                "confidence_threshold": 0.4
            },
            "consistency": {
                "symptom_consistency": {
                    "memory": ["記憶", "忘記", "重複"],
                    "language": ["語言", "說話", "表達"],
                    "orientation": ["迷路", "方向", "地點"],
                    "judgment": ["判斷", "決定", "選擇"]
                },
                "confidence_threshold": 0.6
            },
            "reliability": {
                "source_indicators": ["親眼看到", "家人說", "醫生說", "觀察到"],
                "detail_indicators": ["具體", "詳細", "清楚", "明確"],
                "time_indicators": ["最近", "這幾天", "上週", "一個月"],
                "confidence_threshold": 0.5
            }
        }
    
    def verify_aspects(self, text: str, requested_aspects: List[str]) -> Dict[str, Any]:
        """Verify multiple aspects of the input text"""
        try:
            results = {}
            total_confidence = 0
            verified_count = 0
            
            for aspect in requested_aspects:
                if aspect in self.aspects:
                    aspect_result = self.aspects[aspect](text)
                    results[aspect] = aspect_result
                    
                    if aspect_result.get("verified", False):
                        verified_count += 1
                        total_confidence += aspect_result.get("confidence", 0)
                else:
                    results[aspect] = {
                        "verified": False,
                        "confidence": 0,
                        "reason": f"Aspect '{aspect}' not supported"
                    }
            
            # Calculate overall metrics
            overall_confidence = total_confidence / len(requested_aspects) if requested_aspects else 0
            verification_score = verified_count / len(requested_aspects) if requested_aspects else 0
            
            # Generate recommendations
            recommendations = self._generate_recommendations(results, overall_confidence)
            
            return {
                "success": True,
                "verified_aspects": results,
                "overall_confidence": overall_confidence,
                "verification_score": verification_score,
                "recommendations": recommendations,
                "verified_count": verified_count,
                "total_aspects": len(requested_aspects)
            }
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "verified_aspects": {},
                "overall_confidence": 0,
                "verification_score": 0,
                "recommendations": ["驗證過程發生錯誤"]
            }
    
    def _verify_symptom(self, text: str) -> Dict[str, Any]:
        """Verify symptom-related aspects"""
        rules = self.verification_rules["symptom"]
        keywords = rules["keywords"]
        
        matched_keywords = [kw for kw in keywords if kw in text]
        confidence = len(matched_keywords) / len(keywords) if keywords else 0
        
        verified = confidence >= rules["confidence_threshold"]
        
        return {
            "verified": verified,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "symptom_count": len(matched_keywords),
            "reason": f"發現 {len(matched_keywords)} 個症狀關鍵詞" if matched_keywords else "未發現明確症狀"
        }
    
    def _verify_severity(self, text: str) -> Dict[str, Any]:
        """Verify severity assessment"""
        rules = self.verification_rules["severity"]
        
        mild_count = sum(1 for kw in rules["mild_keywords"] if kw in text)
        moderate_count = sum(1 for kw in rules["moderate_keywords"] if kw in text)
        severe_count = sum(1 for kw in rules["severe_keywords"] if kw in text)
        
        total_indicators = mild_count + moderate_count + severe_count
        
        if total_indicators == 0:
            severity = "unknown"
            confidence = 0
        elif severe_count > moderate_count and severe_count > mild_count:
            severity = "severe"
            confidence = 0.8
        elif moderate_count > mild_count:
            severity = "moderate"
            confidence = 0.7
        else:
            severity = "mild"
            confidence = 0.6
        
        verified = confidence >= rules["confidence_threshold"]
        
        return {
            "verified": verified,
            "confidence": confidence,
            "severity": severity,
            "indicators": {
                "mild": mild_count,
                "moderate": moderate_count,
                "severe": severe_count
            },
            "reason": f"評估為 {severity} 程度"
        }
    
    def _verify_urgency(self, text: str) -> Dict[str, Any]:
        """Verify urgency assessment"""
        rules = self.verification_rules["urgency"]
        
        high_count = sum(1 for kw in rules["high_urgency"] if kw in text)
        medium_count = sum(1 for kw in rules["medium_urgency"] if kw in text)
        low_count = sum(1 for kw in rules["low_urgency"] if kw in text)
        
        total_indicators = high_count + medium_count + low_count
        
        if total_indicators == 0:
            urgency = "unknown"
            confidence = 0
        elif high_count > 0:
            urgency = "high"
            confidence = 0.9
        elif medium_count > low_count:
            urgency = "medium"
            confidence = 0.7
        else:
            urgency = "low"
            confidence = 0.5
        
        verified = confidence >= rules["confidence_threshold"]
        
        return {
            "verified": verified,
            "confidence": confidence,
            "urgency": urgency,
            "indicators": {
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "reason": f"評估為 {urgency} 緊急程度"
        }
    
    def _verify_context(self, text: str) -> Dict[str, Any]:
        """Verify contextual information"""
        rules = self.verification_rules["context"]
        
        family_count = sum(1 for kw in rules["family_context"] if kw in text)
        daily_count = sum(1 for kw in rules["daily_context"] if kw in text)
        social_count = sum(1 for kw in rules["social_context"] if kw in text)
        
        total_contexts = family_count + daily_count + social_count
        confidence = min(1.0, total_contexts / 3.0)  # Normalize to 0-1
        
        verified = confidence >= rules["confidence_threshold"]
        
        contexts = []
        if family_count > 0:
            contexts.append("family")
        if daily_count > 0:
            contexts.append("daily")
        if social_count > 0:
            contexts.append("social")
        
        return {
            "verified": verified,
            "confidence": confidence,
            "contexts": contexts,
            "indicators": {
                "family": family_count,
                "daily": daily_count,
                "social": social_count
            },
            "reason": f"識別出 {len(contexts)} 個情境背景"
        }
    
    def _verify_consistency(self, text: str) -> Dict[str, Any]:
        """Verify consistency of symptoms"""
        rules = self.verification_rules["consistency"]
        symptom_consistency = rules["symptom_consistency"]
        
        consistency_scores = {}
        for category, keywords in symptom_consistency.items():
            matched = [kw for kw in keywords if kw in text]
            consistency_scores[category] = len(matched)
        
        total_symptoms = sum(consistency_scores.values())
        consistency_ratio = total_symptoms / len(symptom_consistency) if symptom_consistency else 0
        
        verified = consistency_ratio >= rules["confidence_threshold"]
        
        return {
            "verified": verified,
            "confidence": consistency_ratio,
            "symptom_categories": consistency_scores,
            "total_symptoms": total_symptoms,
            "reason": f"症狀一致性評估: {consistency_ratio:.2f}"
        }
    
    def _verify_reliability(self, text: str) -> Dict[str, Any]:
        """Verify reliability of information"""
        rules = self.verification_rules["reliability"]
        
        source_count = sum(1 for kw in rules["source_indicators"] if kw in text)
        detail_count = sum(1 for kw in rules["detail_indicators"] if kw in text)
        time_count = sum(1 for kw in rules["time_indicators"] if kw in text)
        
        total_reliability = source_count + detail_count + time_count
        reliability_score = min(1.0, total_reliability / 6.0)  # Normalize to 0-1
        
        verified = reliability_score >= rules["confidence_threshold"]
        
        return {
            "verified": verified,
            "confidence": reliability_score,
            "indicators": {
                "source": source_count,
                "detail": detail_count,
                "time": time_count
            },
            "reason": f"資訊可靠性評估: {reliability_score:.2f}"
        }
    
    def _generate_recommendations(self, results: Dict[str, Any], overall_confidence: float) -> List[str]:
        """Generate recommendations based on verification results"""
        recommendations = []
        
        if overall_confidence < 0.5:
            recommendations.append("建議提供更詳細的症狀描述")
        
        if "symptom" in results and results["symptom"].get("symptom_count", 0) < 2:
            recommendations.append("建議描述更多具體症狀")
        
        if "severity" in results and results["severity"].get("severity") == "severe":
            recommendations.append("建議立即尋求專業醫療協助")
        
        if "urgency" in results and results["urgency"].get("urgency") == "high":
            recommendations.append("建議優先處理安全相關問題")
        
        if "context" in results and len(results["context"].get("contexts", [])) < 2:
            recommendations.append("建議提供更多情境背景資訊")
        
        if "reliability" in results and results["reliability"].get("confidence", 0) < 0.5:
            recommendations.append("建議提供更具體的觀察細節")
        
        if not recommendations:
            recommendations.append("資訊驗證通過，可以進行進一步分析")
        
        return recommendations

# Initialize verification engine
verification_engine = AspectVerificationEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Aspect Verifiers Service",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "available_aspects": list(verification_engine.aspects.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "aspect-verifiers",
        "version": "3.0.0",
        "aspects_loaded": len(verification_engine.aspects),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/verify")
async def verify_aspects(request: VerificationRequest):
    """Verify multiple aspects of input text"""
    try:
        logger.info(f"🔍 Verifying aspects: {request.aspects} for user {request.user_id}")
        
        result = verification_engine.verify_aspects(request.text, request.aspects)
        
        logger.info(f"✅ Verification completed with score: {result.get('verification_score', 0):.2f}")
        
        return VerificationResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/aspects")
async def list_aspects():
    """List available verification aspects"""
    return {
        "aspects": list(verification_engine.aspects.keys()),
        "descriptions": {
            "symptom": "症狀相關驗證",
            "severity": "嚴重程度驗證",
            "urgency": "緊急程度驗證",
            "context": "情境背景驗證",
            "consistency": "症狀一致性驗證",
            "reliability": "資訊可靠性驗證"
        }
    }

@app.get("/rules")
async def get_verification_rules():
    """Get verification rules for each aspect"""
    return {
        "rules": verification_engine.verification_rules,
        "total_aspects": len(verification_engine.aspects)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007) 