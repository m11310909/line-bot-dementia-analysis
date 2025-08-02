from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import logging
from typing import Dict, Any, Optional
import json
from .flex_builder import XAIFlexMessageBuilder
from .optimized_visualization import OptimizedVisualizationGenerator, VisualizationStage, VisualizationCache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="XAI Wrapper Service",
    description="Enhanced wrapper for dementia chatbot API with XAI visualization",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    user_input: str
    user_id: Optional[str] = "default_user"
    context: Dict[str, Any] = {}
    stage: Optional[str] = "immediate"  # immediate, quick, detailed

class AnalysisResponse(BaseModel):
    original_response: Dict[str, Any]
    xai_enhanced: Dict[str, Any]
    module: str
    confidence: float
    visualization_data: Dict[str, Any]

class XAIAnalyzer:
    def __init__(self):
        self.keyword_patterns = self.load_keyword_patterns()
        self.module_detector = ModuleDetector()
        self.visualization_generator = VisualizationGenerator()
    
    def load_keyword_patterns(self) -> Dict[str, Dict]:
        """Load keyword patterns for different modules"""
        return {
            "M1": {
                "keywords": ["記憶", "忘記", "重複", "迷路", "時間混淆", "洗衣機", "瓦斯", "鑰匙", "錢包"],
                "intents": ["symptom_check", "warning_sign_inquiry"],
                "weight": 1.0
            },
            "M2": {
                "keywords": ["階段", "病程", "惡化", "進展", "早期", "中期", "晚期", "輕度", "中度", "重度"],
                "intents": ["stage_inquiry", "progression_check"],
                "weight": 1.0
            },
            "M3": {
                "keywords": ["行為", "精神", "妄想", "躁動", "憂鬱", "幻覺", "攻擊", "焦慮", "失眠"],
                "intents": ["behavioral_symptom", "psychological_symptom"],
                "weight": 1.0
            },
            "M4": {
                "keywords": ["照護", "任務", "日常", "醫療", "社交", "協助", "照顧", "陪伴"],
                "intents": ["care_guidance", "task_navigation"],
                "weight": 1.0
            }
        }
    
    async def analyze(self, user_input: str, bot_response: Dict) -> Dict[str, Any]:
        """Analyze user input and bot response to generate XAI data"""
        try:
            # 1. Extract keywords
            keywords = self.extract_keywords(user_input)
            
            # 2. Classify intent
            intent = await self.classify_intent(user_input, keywords)
            
            # 3. Calculate confidence
            confidence = await self.calculate_confidence(user_input, bot_response, intent)
            
            # 4. Generate reasoning path
            reasoning_path = self.generate_reasoning_path(keywords, intent, bot_response)
            
            return {
                "keywords": keywords,
                "intent": intent,
                "confidence": confidence,
                "reasoning": reasoning_path,
                "evidence": self.extract_evidence(bot_response)
            }
        except Exception as e:
            logger.error(f"Error in XAI analysis: {e}")
            return {
                "keywords": {},
                "intent": "unknown",
                "confidence": 0.5,
                "reasoning": [],
                "evidence": {}
            }
    
    def extract_keywords(self, user_input: str) -> Dict[str, float]:
        """Extract keywords from user input with importance scores"""
        keywords = {}
        input_lower = user_input.lower()
        
        for module, patterns in self.keyword_patterns.items():
            for keyword in patterns["keywords"]:
                if keyword in input_lower:
                    # Calculate importance based on frequency and position
                    count = input_lower.count(keyword)
                    position_score = 1.0 if input_lower.startswith(keyword) else 0.7
                    keywords[keyword] = count * position_score * patterns["weight"]
        
        return keywords
    
    async def classify_intent(self, user_input: str, keywords: Dict[str, float]) -> str:
        """Classify user intent based on input and keywords"""
        if not keywords:
            return "general_inquiry"
        
        # Simple intent classification based on keywords
        if any(k in ["記憶", "忘記", "重複"] for k in keywords.keys()):
            return "symptom_check"
        elif any(k in ["階段", "病程", "惡化"] for k in keywords.keys()):
            return "stage_inquiry"
        elif any(k in ["行為", "精神", "妄想"] for k in keywords.keys()):
            return "behavioral_symptom"
        elif any(k in ["照護", "協助", "照顧"] for k in keywords.keys()):
            return "care_guidance"
        else:
            return "general_inquiry"
    
    async def calculate_confidence(self, user_input: str, bot_response: Dict, intent: str) -> float:
        """Calculate confidence score for the analysis"""
        # Base confidence on response quality and intent clarity
        base_confidence = 0.7
        
        # Adjust based on response length and structure
        if "contents" in bot_response:
            response_quality = min(len(str(bot_response["contents"])) / 100, 1.0)
            base_confidence += response_quality * 0.2
        
        # Adjust based on intent clarity
        if intent != "general_inquiry":
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def generate_reasoning_path(self, keywords: Dict[str, float], intent: str, bot_response: Dict) -> list:
        """Generate reasoning path for XAI visualization"""
        steps = [
            {
                "step": 1,
                "label": "輸入分析",
                "description": f"分析使用者輸入，提取關鍵詞: {list(keywords.keys())}",
                "confidence": 0.9
            },
            {
                "step": 2,
                "label": "意圖分類",
                "description": f"識別使用者意圖: {intent}",
                "confidence": 0.8
            },
            {
                "step": 3,
                "label": "回應生成",
                "description": "基於分析結果生成回應",
                "confidence": 0.85
            }
        ]
        
        return steps
    
    def extract_evidence(self, bot_response: Dict) -> Dict[str, Any]:
        """Extract evidence from bot response for visualization"""
        evidence = {
            "response_type": bot_response.get("type", "unknown"),
            "has_flex_content": "contents" in bot_response,
            "response_length": len(str(bot_response))
        }
        
        if "contents" in bot_response:
            evidence["flex_type"] = bot_response["contents"].get("type", "unknown")
        
        return evidence

class ModuleDetector:
    def __init__(self):
        self.patterns = {
            "M1": {
                "keywords": ["記憶", "忘記", "重複", "迷路", "時間混淆", "洗衣機", "瓦斯", "鑰匙", "錢包"],
                "intents": ["symptom_check", "warning_sign_inquiry"]
            },
            "M2": {
                "keywords": ["階段", "病程", "惡化", "進展", "早期", "中期", "晚期", "輕度", "中度", "重度"],
                "intents": ["stage_inquiry", "progression_check"]
            },
            "M3": {
                "keywords": ["行為", "精神", "妄想", "躁動", "憂鬱", "幻覺", "攻擊", "焦慮", "失眠"],
                "intents": ["behavioral_symptom", "psychological_symptom"]
            },
            "M4": {
                "keywords": ["照護", "任務", "日常", "醫療", "社交", "協助", "照顧", "陪伴"],
                "intents": ["care_guidance", "task_navigation"]
            }
        }
    
    def detect_module(self, user_input: str, keywords: Dict[str, float], intent: str) -> str:
        """Detect which visualization module to use"""
        scores = {}
        
        for module, patterns in self.patterns.items():
            keyword_score = self.calculate_keyword_match(keywords, patterns["keywords"])
            intent_score = 1.0 if intent in patterns["intents"] else 0.0
            scores[module] = keyword_score * 0.6 + intent_score * 0.4
        
        # Return the module with highest score, default to M1 if no clear match
        best_module = max(scores, key=scores.get) if max(scores.values()) > 0.3 else "M1"
        logger.info(f"Module detection scores: {scores}, selected: {best_module}")
        return best_module
    
    def calculate_keyword_match(self, keywords: Dict[str, float], pattern_keywords: list) -> float:
        """Calculate keyword match score"""
        if not keywords:
            return 0.0
        
        matches = sum(1 for keyword in keywords.keys() if keyword in pattern_keywords)
        return min(matches / len(pattern_keywords), 1.0)

class VisualizationGenerator:
    def __init__(self):
        self.optimized_generator = OptimizedVisualizationGenerator()
        self.cache = VisualizationCache()
    
    def generate_visualization(self, module: str, xai_data: Dict[str, Any], stage: VisualizationStage = VisualizationStage.IMMEDIATE) -> Dict[str, Any]:
        """Generate optimized visualization data based on module type"""
        # 檢查快取
        cache_key = self.cache.get_cache_key(module, xai_data.get("keywords", {}), xai_data.get("confidence", 0.0))
        cached_result = self.cache.get(cache_key)
        
        if cached_result and stage == VisualizationStage.IMMEDIATE:
            logger.info(f"✅ Using cached visualization for {module}")
            return cached_result
        
        # 生成新的視覺化
        result = self.optimized_generator.generate_visualization(module, xai_data, stage)
        
        # 快取結果（僅快取即時視覺化）
        if stage == VisualizationStage.IMMEDIATE:
            self.cache.set(cache_key, result)
        
        return result
    
    def generate_m1_visualization(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate M1 warning signs comparison visualization"""
        return {
            "type": "comparison_card",
            "module": "M1",
            "title": "🚨 失智症警訊分析",
            "confidence_score": xai_data["confidence"],
            "evidence_highlights": [
                {
                    "text": keyword,
                    "importance": score,
                    "category": "warning_sign"
                }
                for keyword, score in xai_data["keywords"].items()
            ],
            "reasoning_path": {
                "steps": xai_data["reasoning"]
            },
            "comparison": {
                "normal_aging": self.extract_normal_aging_info(xai_data),
                "warning_signs": self.extract_warning_signs(xai_data)
            }
        }
    
    def generate_m2_visualization(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate M2 progression stage visualization"""
        return {
            "type": "progression_chart",
            "module": "M2",
            "title": "📊 病程階段評估",
            "confidence_score": xai_data["confidence"],
            "stage_indicators": self.extract_stage_indicators(xai_data),
            "progression_factors": list(xai_data["keywords"].keys())
        }
    
    def generate_m3_visualization(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate M3 BPSD symptoms visualization"""
        return {
            "type": "symptom_analysis",
            "module": "M3",
            "title": "🧠 BPSD 症狀分析",
            "confidence_score": xai_data["confidence"],
            "symptoms": list(xai_data["keywords"].keys()),
            "severity_indicators": self.calculate_severity(xai_data)
        }
    
    def generate_m4_visualization(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate M4 care navigation visualization"""
        return {
            "type": "care_navigation",
            "module": "M4",
            "title": "🏥 照護需求識別",
            "confidence_score": xai_data["confidence"],
            "care_needs": list(xai_data["keywords"].keys()),
            "priority_level": self.calculate_priority(xai_data)
        }
    
    def generate_default_visualization(self, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate default visualization for unknown modules"""
        return {
            "type": "general_analysis",
            "module": "general",
            "title": "📝 一般分析",
            "confidence_score": xai_data["confidence"],
            "key_points": list(xai_data["keywords"].keys())
        }
    
    def extract_normal_aging_info(self, xai_data: Dict[str, Any]) -> list:
        """Extract normal aging information for comparison"""
        return ["偶爾忘記名字", "偶爾放錯物品", "偶爾迷路"]
    
    def extract_warning_signs(self, xai_data: Dict[str, Any]) -> list:
        """Extract warning signs from analysis"""
        return list(xai_data["keywords"].keys())
    
    def extract_stage_indicators(self, xai_data: Dict[str, Any]) -> list:
        """Extract stage indicators for progression analysis"""
        return list(xai_data["keywords"].keys())
    
    def calculate_severity(self, xai_data: Dict[str, Any]) -> str:
        """Calculate symptom severity"""
        keyword_count = len(xai_data["keywords"])
        if keyword_count >= 3:
            return "high"
        elif keyword_count >= 1:
            return "medium"
        else:
            return "low"
    
    def calculate_priority(self, xai_data: Dict[str, Any]) -> str:
        """Calculate care priority level"""
        keyword_count = len(xai_data["keywords"])
        if keyword_count >= 2:
            return "high"
        elif keyword_count >= 1:
            return "medium"
        else:
            return "low"

class DementiaBotWrapper:
    def __init__(self):
        self.chatbot_api_url = "http://localhost:8008/analyze"  # Your existing chatbot API
        self.xai_analyzer = XAIAnalyzer()
        self.module_detector = ModuleDetector()
        self.visualization_generator = VisualizationGenerator()
    
    async def enhance_with_xai(self, user_input: str, user_id: str = "default_user", stage: str = "immediate") -> Dict[str, Any]:
        """Enhance chatbot response with XAI visualization"""
        try:
            # 1. Call original chatbot API
            original_response = await self.call_chatbot_api(user_input, user_id)
            
            # 2. Analyze with XAI
            xai_data = await self.xai_analyzer.analyze(user_input, original_response)
            
            # 3. Detect appropriate module
            module = self.module_detector.detect_module(
                user_input, 
                xai_data["keywords"], 
                xai_data["intent"]
            )
            
            # 4. Generate visualization data with progressive loading
            stage_mapping = {
                "immediate": VisualizationStage.IMMEDIATE,
                "quick": VisualizationStage.QUICK,
                "detailed": VisualizationStage.DETAILED
            }
            current_stage = stage_mapping.get(stage, VisualizationStage.IMMEDIATE)
            visualization = self.visualization_generator.generate_visualization(module, xai_data, original_response, current_stage)
            
            return {
                "original_response": original_response,
                "xai_enhanced": {
                    "module": module,
                    "visualization": visualization,
                    "confidence": xai_data["confidence"],
                    "reasoning_path": xai_data["reasoning"]
                }
            }
        except Exception as e:
            logger.error(f"Error in XAI enhancement: {e}")
            # Fallback to original response
            original_response = await self.call_chatbot_api(user_input, user_id)
            return {
                "original_response": original_response,
                "xai_enhanced": {
                    "module": "M1",
                    "visualization": {},
                    "confidence": 0.5,
                    "reasoning_path": []
                }
            }
    
    async def call_chatbot_api(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Call the original chatbot API"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.chatbot_api_url,
                    json={
                        "message": user_input,
                        "user_id": user_id
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error calling chatbot API: {e}")
            # Return fallback response
            return {
                "type": "text",
                "text": "抱歉，目前無法處理您的請求，請稍後再試。"
            }

# Initialize wrapper
wrapper = DementiaBotWrapper()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "XAI Wrapper Service",
        "version": "1.0.0",
        "features": ["M1-M4 visualization", "XAI analysis", "Module detection"]
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_with_xai(request: AnalysisRequest):
    """Main endpoint for XAI-enhanced analysis"""
    try:
        logger.info(f"Processing analysis request: {request.user_input[:50]}...")
        
        # Get enhanced response
        enhanced_response = await wrapper.enhance_with_xai(
            request.user_input, 
            request.user_id
        )
        
        # Prepare response
        response = AnalysisResponse(
            original_response=enhanced_response["original_response"],
            xai_enhanced=enhanced_response["xai_enhanced"],
            module=enhanced_response["xai_enhanced"]["module"],
            confidence=enhanced_response["xai_enhanced"]["confidence"],
            visualization_data=enhanced_response["xai_enhanced"]["visualization"]
        )
        
        logger.info(f"Analysis completed. Module: {response.module}, Confidence: {response.confidence}")
        return response
        
    except Exception as e:
        logger.error(f"Error in analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "XAI Wrapper Service",
        "version": "1.0.0",
        "description": "Enhanced wrapper for dementia chatbot API with XAI visualization",
        "endpoints": {
            "POST /analyze": "Analyze with XAI enhancement",
            "GET /health": "Health check",
            "GET /": "Service information"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009) 