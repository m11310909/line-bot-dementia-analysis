#!/usr/bin/env python3
"""
Stable RAG API - Enhanced version with better error handling and stability
"""

import os
import json
import logging
import signal
import sys
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

# Configure logging with more detailed information
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stable RAG API",
    description="Enhanced and stable RAG API for dementia analysis",
    version="2.1.0"
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

# Global variables for monitoring
startup_time = datetime.now()
request_count = 0
error_count = 0

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Initialize modules with error handling
def initialize_modules():
    """Initialize all modules with error handling"""
    modules = {}
    try:
        logger.info("Initializing M1 module...")
        modules["M1"] = M1WarningSignsModule()
        logger.info("M1 module initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize M1 module: {e}")
        modules["M1"] = None
    
    try:
        logger.info("Initializing M2 module...")
        modules["M2"] = M2ProgressionMatrixModule()
        logger.info("M2 module initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize M2 module: {e}")
        modules["M2"] = None
    
    try:
        logger.info("Initializing M3 module...")
        modules["M3"] = M3BPSDClassificationModule()
        logger.info("M3 module initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize M3 module: {e}")
        modules["M3"] = None
    
    try:
        logger.info("Initializing M4 module...")
        modules["M4"] = M4CareNavigationModule()
        logger.info("M4 module initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize M4 module: {e}")
        modules["M4"] = None
    
    return modules

# Initialize modules
modules = initialize_modules()

# Initialize enhanced flex message generator
try:
    flex_generator = EnhancedFlexMessageGenerator()
    logger.info("Flex message generator initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize flex message generator: {e}")
    flex_generator = None

class StableIntegratedEngine:
    def __init__(self):
        self.modules = modules
        self.flex_generator = flex_generator
        self.request_count = 0
        self.error_count = 0
    
    def _analyze_with_module(self, module_name: str, user_input: str) -> Dict:
        """Analyze with specific module with enhanced error handling"""
        global request_count, error_count
        request_count += 1
        
        try:
            if module_name not in self.modules or self.modules[module_name] is None:
                raise Exception(f"Module {module_name} not available")
            
            module = self.modules[module_name]
            
            if module_name == "M1":
                result = module.analyze_warning_signs(user_input)
            elif module_name == "M2":
                result = module.analyze_progression(user_input)
            elif module_name == "M3":
                result = module.analyze_bpsd_symptoms(user_input)
            elif module_name == "M4":
                result = module.analyze_care_needs(user_input)
            else:
                raise Exception(f"Unknown module: {module_name}")
            
            logger.info(f"Module {module_name} analysis completed successfully")
            return result
            
        except Exception as e:
            error_count += 1
            logger.error(f"Module {module_name} analysis failed: {e}")
            return {
                "error": str(e),
                "confidence": 0.0,
                "matched_items": [],
                "summary": f"Module {module_name} analysis failed"
            }
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        return {
            "startup_time": startup_time.isoformat(),
            "uptime_seconds": (datetime.now() - startup_time).total_seconds(),
            "request_count": request_count,
            "error_count": error_count,
            "success_rate": ((request_count - error_count) / max(request_count, 1)) * 100,
            "modules_available": len([m for m in self.modules.values() if m is not None])
        }

# Initialize the engine
integrated_engine = StableIntegratedEngine()

@app.on_event("startup")
async def startup_event():
    """Handle startup events"""
    logger.info("Stable RAG API starting up...")
    logger.info(f"Available modules: {[name for name, module in modules.items() if module is not None]}")

@app.on_event("shutdown")
async def shutdown_event():
    """Handle shutdown events"""
    logger.info("Stable RAG API shutting down...")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "Stable RAG API is running",
        "version": "2.1.0",
        "status": "healthy",
        "startup_time": startup_time.isoformat(),
        "uptime_seconds": (datetime.now() - startup_time).total_seconds()
    }

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    try:
        # Test each module
        module_status = {}
        for module_name, module in modules.items():
            if module is not None:
                try:
                    # Quick test with sample input
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
            else:
                module_status[module_name] = {
                    "status": "unavailable"
                }
        
        stats = integrated_engine.get_system_stats()
        
        return {
            "status": "healthy",
            "mode": "stable",
            "modules": module_status,
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/analyze/{module_name}")
async def analyze_single_module(module_name: str, request: UserInput):
    """Single module analysis endpoint with enhanced error handling"""
    try:
        if module_name not in integrated_engine.modules:
            raise HTTPException(status_code=400, detail=f"Unknown module: {module_name}")
        
        if integrated_engine.modules[module_name] is None:
            raise HTTPException(status_code=503, detail=f"Module {module_name} is not available")
        
        module_result = integrated_engine._analyze_with_module(module_name, request.text)
        
        # Check if analysis failed
        if "error" in module_result:
            raise HTTPException(status_code=500, detail=module_result["error"])
        
        # Create enhanced flex message
        try:
            analysis_result = AnalysisResult(
                module=module_name,
                confidence=module_result.get("confidence", 0.5),
                matched_items=module_result.get("matched_items", []),
                summary=module_result.get("summary", ""),
                timestamp=datetime.now(),
                user_input=request.text
            )
            
            flex_message = create_enhanced_flex_message(module_name, analysis_result)
        except Exception as e:
            logger.error(f"Flex message creation failed: {e}")
            flex_message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "分析完成",
                            "weight": "bold"
                        }
                    ]
                }
            }
        
        return {
            "success": True,
            "module": module_name,
            "result": module_result,
            "flex_message": flex_message,
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Module analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return integrated_engine.get_system_stats()

if __name__ == "__main__":
    logger.info("Starting Stable RAG API...")
    uvicorn.run(
        "stable_rag_api:app",
        host="0.0.0.0",
        port=8005,
        reload=False,  # Disable auto-reload for stability
        log_level="info",
        access_log=True
    ) 