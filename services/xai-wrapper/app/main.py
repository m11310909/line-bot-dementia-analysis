from fastapi import FastAPI, HTTPException
from typing import Dict, Any, Optional
import httpx
import asyncio
import hashlib
import json
from datetime import datetime
from pydantic import BaseModel

from .module_detector import ModuleDetector
from .xai_analyzer import XAIAnalyzer
from .visualization_generator import VisualizationGenerator
from .cache_manager import CacheManager

app = FastAPI(title="XAI Wrapper Service", version="1.0.0")

class AnalysisRequest(BaseModel):
    user_input: str
    user_id: str
    context: Optional[Dict] = None

class XAIWrapperService:
    def __init__(self):
        self.bot_api_url = "https://dementia-helper-api.com"  # Replace with actual
        self.module_detector = ModuleDetector()
        self.xai_analyzer = XAIAnalyzer()
        self.viz_generator = VisualizationGenerator()
        self.cache = CacheManager()
        
    async def process_message(self, request: AnalysisRequest) -> Dict[str, Any]:
        # Check cache
        cache_key = f"analysis:{hashlib.md5(request.user_input.encode()).hexdigest()}"
        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
            
        # Call dementia bot API
        async with httpx.AsyncClient() as client:
            try:
                bot_response = await client.post(
                    self.bot_api_url,
                    json={"text": request.user_input},
                    timeout=10.0
                )
                bot_data = bot_response.json()
            except:
                bot_data = {"text": "無法連接到失智小幫手", "confidence": 0.3}
        
        # Extract keywords and classify intent
        keywords = await self.xai_analyzer.extract_keywords(request.user_input)
        intent = await self.xai_analyzer.classify_intent(request.user_input)
        
        # Detect module
        module = self.module_detector.detect(
            user_input=request.user_input,
            keywords=keywords,
            intent=intent,
            bot_response=bot_data
        )
        
        # Generate XAI analysis
        xai_data = await self.xai_analyzer.analyze(
            user_input=request.user_input,
            bot_response=bot_data,
            module=module
        )
        
        # Generate visualization
        visualization = await self.viz_generator.generate(
            module=module,
            xai_data=xai_data
        )
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": request.user_input,
            "module": module,
            "bot_response": bot_data,
            "xai_analysis": xai_data,
            "visualization": visualization,
            "confidence": xai_data["confidence"]
        }
        
        # Cache result
        await self.cache.set(cache_key, json.dumps(result), ttl=3600)
        
        return result

wrapper_service = XAIWrapperService()

@app.post("/api/v1/analyze")
async def analyze(request: AnalysisRequest):
    try:
        result = await wrapper_service.process_message(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "xai-wrapper"
    }
