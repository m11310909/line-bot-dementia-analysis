"""
Enhanced M1-M2-M3-M4 Integrated API
Implements the redesigned visualization system with LINE Flex Message and LIFF requirements
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Import the enhanced flex message generator
from enhanced_flex_message_generator import (
    EnhancedFlexMessageGenerator, 
    AnalysisResult, 
    create_enhanced_flex_message
)

# Import existing modules
from modules.m1_warning_signs import M1WarningSignsModule
from modules.m2_progression_matrix import M2ProgressionMatrixModule
from modules.m3_bpsd_classification import M3BPSDClassificationModule
from modules.m4_care_navigation import M4CareNavigationModule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced M1-M2-M3-M4 Integrated API",
    description="Redesigned visualization system for dementia analysis",
    version="2.0.0"
)

# Pydantic models
class UserInput(BaseModel):
    text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class AnalysisRequest(BaseModel):
    user_input: str
    modules: List[str] = ["M1", "M2", "M3", "M4"]
    confidence_threshold: float = 0.5
    max_results: int = 5

class AnalysisResponse(BaseModel):
    success: bool
    module_results: Dict[str, Any]
    flex_messages: List[Dict]
    timestamp: datetime
    user_input: str

# Initialize modules
m1_module = M1WarningSignsModule()
m2_module = M2ProgressionMatrixModule()
m3_module = M3BPSDClassificationModule()
m4_module = M4CareNavigationModule()

# Initialize enhanced flex message generator
flex_generator = EnhancedFlexMessageGenerator()

class EnhancedIntegratedEngine:
    def __init__(self):
        self.modules = {
            "M1": m1_module,
            "M2": m2_module,
            "M3": m3_module,
            "M4": m4_module
        }
        self.flex_generator = flex_generator
    
    def analyze_comprehensive(self, user_input: str, requested_modules: List[str] = None) -> Dict:
        """Comprehensive analysis using all modules"""
        if requested_modules is None:
            requested_modules = ["M1", "M2", "M3", "M4"]
        
        results = {}
        flex_messages = []
        
        for module_name in requested_modules:
            if module_name in self.modules:
                try:
                    # Analyze with specific module
                    module_result = self._analyze_with_module(module_name, user_input)
                    results[module_name] = module_result
                    
                    # Create enhanced flex message
                    analysis_result = AnalysisResult(
                        module=module_name,
                        confidence=module_result.get("confidence", 0.5),
                        matched_items=module_result.get("matched_items", []),
                        summary=module_result.get("summary", ""),
                        timestamp=datetime.now(),
                        user_input=user_input
                    )
                    
                    flex_message = create_enhanced_flex_message(module_name, analysis_result)
                    flex_messages.append({
                        "module": module_name,
                        "flex_message": flex_message
                    })
                    
                except Exception as e:
                    logger.error(f"Error analyzing with {module_name}: {str(e)}")
                    results[module_name] = {
                        "error": str(e),
                        "confidence": 0.0,
                        "matched_items": [],
                        "summary": f"分析 {module_name} 時發生錯誤"
                    }
        
        return {
            "success": True,
            "module_results": results,
            "flex_messages": flex_messages,
            "timestamp": datetime.now(),
            "user_input": user_input
        }
    
    def _analyze_with_module(self, module_name: str, user_input: str) -> Dict:
        """Analyze with specific module"""
        module = self.modules[module_name]
        
        if module_name == "M1":
            return module.analyze_warning_signs(user_input)
        elif module_name == "M2":
            return module.analyze_progression(user_input)
        elif module_name == "M3":
            return module.analyze_bpsd_symptoms(user_input)
        elif module_name == "M4":
            return module.analyze_care_tasks(user_input)
        else:
            raise ValueError(f"Unknown module: {module_name}")

# Initialize the engine
integrated_engine = EnhancedIntegratedEngine()

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Enhanced M1-M2-M3-M4 Integrated API",
        "version": "2.0.0",
        "description": "Redesigned visualization system for dementia analysis",
        "modules": ["M1", "M2", "M3", "M4"],
        "features": [
            "Enhanced Flex Message Design",
            "Senior-friendly Typography",
            "Progressive Information Disclosure",
            "Confidence Indicators",
            "LIFF Integration Ready"
        ]
    }

@app.get("/health")
async def health_check():
    """Enhanced health check with module status"""
    module_status = {}
    
    for module_name, module in integrated_engine.modules.items():
        try:
            # Test each module with a simple input
            test_result = integrated_engine._analyze_with_module(module_name, "測試")
            module_status[module_name] = {
                "status": "active",
                "confidence": test_result.get("confidence", 0.0)
            }
        except Exception as e:
            module_status[module_name] = {
                "status": "error",
                "error": str(e)
            }
    
    return {
        "status": "healthy",
        "mode": "enhanced",
        "modules": module_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze")
async def analyze_comprehensive(request: AnalysisRequest):
    """Comprehensive analysis endpoint"""
    try:
        result = integrated_engine.analyze_comprehensive(
            request.user_input,
            request.modules
        )
        
        return AnalysisResponse(**result)
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/{module_name}")
async def analyze_single_module(module_name: str, request: UserInput):
    """Single module analysis endpoint"""
    try:
        if module_name not in integrated_engine.modules:
            raise HTTPException(status_code=400, detail=f"Unknown module: {module_name}")
        
        module_result = integrated_engine._analyze_with_module(module_name, request.text)
        
        # Create enhanced flex message
        analysis_result = AnalysisResult(
            module=module_name,
            confidence=module_result.get("confidence", 0.5),
            matched_items=module_result.get("matched_items", []),
            summary=module_result.get("summary", ""),
            timestamp=datetime.now(),
            user_input=request.text
        )
        
        flex_message = create_enhanced_flex_message(module_name, analysis_result)
        
        return {
            "success": True,
            "module": module_name,
            "result": module_result,
            "flex_message": flex_message,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Module analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/flex/{module_name}")
async def get_flex_message(module_name: str, request: UserInput):
    """Get enhanced flex message for specific module"""
    try:
        if module_name not in integrated_engine.modules:
            raise HTTPException(status_code=400, detail=f"Unknown module: {module_name}")
        
        module_result = integrated_engine._analyze_with_module(module_name, request.text)
        
        # Create enhanced flex message
        analysis_result = AnalysisResult(
            module=module_name,
            confidence=module_result.get("confidence", 0.5),
            matched_items=module_result.get("matched_items", []),
            summary=module_result.get("summary", ""),
            timestamp=datetime.now(),
            user_input=request.text
        )
        
        flex_message = create_enhanced_flex_message(module_name, analysis_result)
        
        return {
            "type": "flex",
            "altText": f"{module_name} 分析結果",
            "contents": flex_message
        }
    
    except Exception as e:
        logger.error(f"Flex message error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/modules/{module_name}/status")
async def module_status(module_name: str):
    """Get specific module status"""
    if module_name not in integrated_engine.modules:
        raise HTTPException(status_code=400, detail=f"Unknown module: {module_name}")
    
    try:
        # Test the module
        test_result = integrated_engine._analyze_with_module(module_name, "測試")
        
        return {
            "module": module_name,
            "status": "active",
            "confidence": test_result.get("confidence", 0.0),
            "matched_items_count": len(test_result.get("matched_items", [])),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "module": module_name,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/design-system")
async def get_design_system():
    """Get design system information"""
    return {
        "design_system": {
            "colors": {
                "primary_blue": "#2196F3",
                "primary_green": "#4CAF50",
                "primary_orange": "#FF9800",
                "primary_red": "#F44336",
                "confidence_high": "#4CAF50",
                "confidence_medium": "#2196F3",
                "confidence_low": "#FF9800"
            },
            "typography": {
                "text_xs": "13px",
                "text_sm": "15px",
                "text_base": "17px",
                "text_lg": "19px",
                "text_xl": "21px"
            },
            "components": [
                "M1: 十大警訊比對卡",
                "M2: 病程階段對照",
                "M3: BPSD 症狀分類",
                "M4: 任務導航儀表板"
            ]
        }
    }

@app.post("/test-flex")
async def test_flex_message(request: UserInput):
    """Test endpoint for flex message generation"""
    try:
        # Create a sample analysis result for testing
        sample_result = AnalysisResult(
            module="M1",
            confidence=0.85,
            matched_items=[
                {
                    "id": "M1-01",
                    "name": "記憶力減退",
                    "normal_aging": "偶爾忘記鑰匙放哪裡",
                    "dementia_warning": "忘記剛吃過飯、重複問同樣問題",
                    "confidence": 0.85
                }
            ],
            summary="檢測到記憶力減退症狀，建議及早就醫評估",
            timestamp=datetime.now(),
            user_input=request.text
        )
        
        flex_message = create_enhanced_flex_message("M1", sample_result)
        
        return {
            "success": True,
            "flex_message": flex_message,
            "module": "M1",
            "confidence": 0.85
        }
    
    except Exception as e:
        logger.error(f"Test flex message error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "enhanced_m1_m2_m3_m4_integrated_api:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    ) 