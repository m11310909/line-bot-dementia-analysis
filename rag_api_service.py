"""
RAG API Service for M1-M4 Analysis
Provides the expected API endpoints on port 8005
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG API Service",
    description="M1-M4 Analysis RAG API Service",
    version="2.0.0"
)

# Pydantic models
class AnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class AnalysisResponse(BaseModel):
    success: bool
    analysis: Dict[str, Any]
    confidence: float
    summary: str
    timestamp: str

def create_analysis_flex_message(analysis_result: Dict, user_input: str, analysis_data_encoded: str = None) -> Dict:
    """Create flex message for analysis results"""
    
    # Get primary symptom
    primary_symptom = analysis_result["symptom_titles"][0] if analysis_result["symptom_titles"] else "未檢測到症狀"
    confidence = analysis_result["confidence_levels"][0] if analysis_result["confidence_levels"] else "medium"
    
    # Confidence color mapping
    confidence_colors = {
        "high": "#4CAF50",
        "medium": "#2196F3", 
        "low": "#FF9800"
    }
    confidence_color = confidence_colors.get(confidence, "#666666")
    
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#F8F9FA",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "text",
                    "text": "AI 智慧分析",
                    "size": "sm",
                    "color": "#666666"
                },
                {
                    "type": "text",
                    "text": "失智症警訊分析",
                    "size": "xl",
                    "weight": "bold",
                    "color": "#212121",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": datetime.now().strftime("%Y/%m/%d %p%I:%M"),
                    "size": "xs",
                    "color": "#999999"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "paddingAll": "16px",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 症狀描述",
                            "size": "sm",
                            "weight": "bold",
                            "color": "#666666"
                        },
                        {
                            "type": "text",
                            "text": user_input,
                            "size": "sm",
                            "wrap": True,
                            "margin": "xs"
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 分析結果",
                            "size": "sm",
                            "weight": "bold",
                            "color": "#666666"
                        },
                        {
                            "type": "text",
                            "text": primary_symptom,
                            "size": "sm",
                            "weight": "bold",
                            "color": confidence_color,
                            "margin": "xs"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 綜合評估",
                            "size": "sm",
                            "weight": "bold",
                            "color": "#666666"
                        },
                        {
                            "type": "text",
                            "text": analysis_result["comprehensive_summary"],
                            "size": "sm",
                            "wrap": True,
                            "margin": "xs",
                            "color": "#666666"
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#F8F9FA",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "查看詳細報告",
                        "uri": f"https://d6ad4bf748cd.ngrok-free.app/index.html?analysis={analysis_data_encoded}" if analysis_data_encoded else "https://d6ad4bf748cd.ngrok-free.app/index.html"
                    },
                    "style": "primary",
                    "color": "#2196F3"
                }
            ]
        }
    }

# Sample analysis data
SAMPLE_ANALYSIS_DATA = {
    "M1": {
        "matched_items": [
            {
                "id": "M1-01",
                "name": "記憶力減退",
                "normal_aging": "偶爾忘記鑰匙放哪裡",
                "dementia_warning": "忘記剛吃過飯、重複問同樣問題",
                "confidence": 0.85
            }
        ],
        "confidence": 0.85,
        "summary": "檢測到記憶力減退症狀，建議及早就醫評估"
    },
    "M2": {
        "matched_items": [
            {
                "stage": "middle",
                "progress": 65,
                "name": "中期階段",
                "description": "明顯記憶力減退，需要協助處理日常事務"
            }
        ],
        "confidence": 0.78,
        "summary": "根據症狀分析，患者目前處於中期階段，需要適當的照護協助"
    },
    "M3": {
        "matched_items": [
            {
                "id": "M3-01",
                "name": "躁動不安",
                "category": "躁動不安",
                "confidence": 0.85,
                "description": "患者表現出明顯的躁動和不安情緒"
            }
        ],
        "confidence": 0.82,
        "summary": "檢測到躁動不安症狀，建議專業醫療評估"
    },
    "M4": {
        "matched_items": [
            {
                "id": "M4-01",
                "title": "藥物管理",
                "description": "協助患者按時服藥，確保藥物安全",
                "priority": "high",
                "icon": "💊"
            }
        ],
        "confidence": 0.75,
        "summary": "根據患者狀況，建議優先處理藥物管理任務"
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "RAG API Service",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "GET /health": "Health check",
            "POST /comprehensive-analysis": "Comprehensive analysis",
            "POST /m1-flex": "M1 flex message",
            "GET /modules/status": "Module status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "RAG API",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "M1": "active",
            "M2": "active", 
            "M3": "active",
            "M4": "active"
        }
    }

@app.post("/comprehensive-analysis")
async def comprehensive_analysis(request: AnalysisRequest):
    """Comprehensive analysis endpoint"""
    try:
        user_input = request.text.lower()
        
        # Simple keyword-based analysis
        analysis_result = {
            "success": True,
            "matched_codes": [],
            "symptom_titles": [],
            "confidence_levels": [],
            "comprehensive_summary": "",
            "action_suggestions": [],
            "modules_used": []
        }
        
        # Enhanced keyword-based analysis with more comprehensive detection
        symptoms_detected = []
        
        # M1: Memory Warning Signs
        memory_keywords = ["記憶", "忘記", "健忘", "重複", "同樣", "剛吃過", "約會", "日期", "事件"]
        if any(word in user_input for word in memory_keywords):
            analysis_result["matched_codes"].append("M1-01")
            analysis_result["symptom_titles"].append("記憶力減退")
            analysis_result["confidence_levels"].append("high")
            analysis_result["modules_used"].append("M1")
            symptoms_detected.append("記憶力減退")
        
        # M1: Daily Living Activities
        daily_keywords = ["熟悉", "工作", "迷路", "預算", "管理", "洗衣機", "煮飯", "瓦斯", "關門"]
        if any(word in user_input for word in daily_keywords):
            analysis_result["matched_codes"].append("M1-02")
            analysis_result["symptom_titles"].append("日常生活能力下降")
            analysis_result["confidence_levels"].append("high")
            analysis_result["modules_used"].append("M1")
            symptoms_detected.append("日常生活能力下降")
        
        # M1: Language Problems
        language_keywords = ["語言", "表達", "用詞", "混亂", "對話", "說話", "詞彙", "理解"]
        if any(word in user_input for word in language_keywords):
            analysis_result["matched_codes"].append("M1-03")
            analysis_result["symptom_titles"].append("語言表達困難")
            analysis_result["confidence_levels"].append("medium")
            analysis_result["modules_used"].append("M1")
            symptoms_detected.append("語言表達困難")
        
        # M2: Progression Stages
        stage_keywords = ["階段", "進展", "早期", "中期", "晚期", "惡化", "加重", "嚴重"]
        if any(word in user_input for word in stage_keywords):
            analysis_result["matched_codes"].append("M2-01")
            analysis_result["symptom_titles"].append("病程進展評估")
            analysis_result["confidence_levels"].append("medium")
            analysis_result["modules_used"].append("M2")
            symptoms_detected.append("病程進展評估")
        
        # M3: BPSD Symptoms - Agitation
        agitation_keywords = ["躁動", "不安", "激動", "煩躁", "易怒", "攻擊", "暴力", "衝動"]
        if any(word in user_input for word in agitation_keywords):
            analysis_result["matched_codes"].append("M3-01")
            analysis_result["symptom_titles"].append("躁動不安")
            analysis_result["confidence_levels"].append("medium")
            analysis_result["modules_used"].append("M3")
            symptoms_detected.append("躁動不安")
        
        # M3: BPSD Symptoms - Depression
        depression_keywords = ["憂鬱", "情緒低落", "悲傷", "無助", "絕望", "哭泣", "悲觀", "自責"]
        if any(word in user_input for word in depression_keywords):
            analysis_result["matched_codes"].append("M3-02")
            analysis_result["symptom_titles"].append("憂鬱情緒")
            analysis_result["confidence_levels"].append("medium")
            analysis_result["modules_used"].append("M3")
            symptoms_detected.append("憂鬱情緒")
        
        # M3: BPSD Symptoms - Hallucination
        hallucination_keywords = ["看到", "聽到", "幻覺", "不存在", "有人", "聲音", "影像", "幻聽", "幻視"]
        if any(word in user_input for word in hallucination_keywords):
            analysis_result["matched_codes"].append("M3-03")
            analysis_result["symptom_titles"].append("幻覺症狀")
            analysis_result["confidence_levels"].append("high")
            analysis_result["modules_used"].append("M3")
            symptoms_detected.append("幻覺症狀")
        
        # M3: BPSD Symptoms - Delusion
        delusion_keywords = ["妄想", "懷疑", "被害", "被偷", "被騙", "監視", "跟蹤", "陰謀"]
        if any(word in user_input for word in delusion_keywords):
            analysis_result["matched_codes"].append("M3-04")
            analysis_result["symptom_titles"].append("妄想症狀")
            analysis_result["confidence_levels"].append("high")
            analysis_result["modules_used"].append("M3")
            symptoms_detected.append("妄想症狀")
        
        # M4: Care Tasks
        care_keywords = ["照顧", "照護", "協助", "幫助", "洗澡", "穿衣", "進食", "服藥", "安全"]
        if any(word in user_input for word in care_keywords):
            analysis_result["matched_codes"].append("M4-01")
            analysis_result["symptom_titles"].append("照護任務")
            analysis_result["confidence_levels"].append("high")
            analysis_result["modules_used"].append("M4")
            symptoms_detected.append("照護任務")
        
        # Generate specific summary based on detected symptoms
        if symptoms_detected:
            if len(symptoms_detected) == 1:
                symptom = symptoms_detected[0]
                if "記憶力減退" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}症狀，可能為失智症警訊，建議及早就醫進行認知功能評估"
                    analysis_result["action_suggestions"] = ["建議及早就醫評估", "進行認知功能測試", "尋求神經科醫師協助"]
                elif "日常生活能力下降" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，影響日常生活功能，建議評估照護需求"
                    analysis_result["action_suggestions"] = ["評估照護需求", "尋求社工協助", "考慮居家照護服務"]
                elif "語言表達困難" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，可能影響溝通能力，建議語言治療評估"
                    analysis_result["action_suggestions"] = ["語言治療評估", "改善溝通方式", "尋求專業協助"]
                elif "躁動不安" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，可能為BPSD症狀，建議精神科評估"
                    analysis_result["action_suggestions"] = ["精神科評估", "行為治療", "藥物治療考慮"]
                elif "憂鬱情緒" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，可能合併憂鬱症，建議心理評估"
                    analysis_result["action_suggestions"] = ["心理評估", "憂鬱症篩檢", "心理治療考慮"]
                elif "幻覺症狀" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，需要立即醫療評估，可能有安全風險"
                    analysis_result["action_suggestions"] = ["立即醫療評估", "安全環境評估", "24小時照護考慮"]
                elif "妄想症狀" in symptom:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，需要精神科評估，可能有被害妄想"
                    analysis_result["action_suggestions"] = ["精神科評估", "安全評估", "藥物治療考慮"]
                elif "照護任務" in symptom:
                    analysis_result["comprehensive_summary"] = f"需要{symptom}協助，建議評估照護需求並制定照護計劃"
                    analysis_result["action_suggestions"] = ["制定照護計劃", "尋求照護資源", "家屬支持團體"]
                else:
                    analysis_result["comprehensive_summary"] = f"檢測到{symptom}，建議專業醫療評估"
                    analysis_result["action_suggestions"] = ["建議及早就醫評估", "尋求專業醫療協助"]
            else:
                # Multiple symptoms detected
                analysis_result["comprehensive_summary"] = f"檢測到多項症狀：{', '.join(symptoms_detected)}，建議綜合醫療評估"
                analysis_result["action_suggestions"] = ["綜合醫療評估", "多專科會診", "制定治療計劃"]
        else:
            analysis_result["comprehensive_summary"] = "未檢測到明顯症狀，建議持續觀察並定期健康檢查"
            analysis_result["action_suggestions"] = ["持續觀察", "定期健康檢查", "注意症狀變化"]
        
        # Encode analysis data for LIFF URL
        import urllib.parse
        analysis_data_encoded = urllib.parse.quote(json.dumps(analysis_result, ensure_ascii=False))
        
        # Create flex message for webhook compatibility
        flex_message = create_analysis_flex_message(analysis_result, request.text, analysis_data_encoded)
        
        # Return format expected by webhook
        return {
            "type": "flex",
            "altText": "失智症警訊分析結果",
            "contents": flex_message,
            "analysis_data": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/m1-flex")
async def m1_flex_analysis(request: AnalysisRequest):
    """M1 flex message analysis (backward compatibility)"""
    try:
        # Use the same analysis logic as comprehensive
        result = await comprehensive_analysis(request)
        
        # Add M1-specific formatting
        result["module"] = "M1"
        result["flex_message"] = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#F8F9FA",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "AI 智慧分析",
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": "記憶力評估分析",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#212121",
                        "margin": "sm"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": result["comprehensive_summary"],
                        "size": "sm",
                        "wrap": True
                    }
                ]
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"M1 flex analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/modules/status")
async def modules_status():
    """Module status endpoint"""
    return {
        "modules": {
            "M1": {
                "status": "active",
                "confidence": 0.85,
                "matched_items_count": 1
            },
            "M2": {
                "status": "active", 
                "confidence": 0.78,
                "matched_items_count": 1
            },
            "M3": {
                "status": "active",
                "confidence": 0.82,
                "matched_items_count": 1
            },
            "M4": {
                "status": "active",
                "confidence": 0.75,
                "matched_items_count": 1
            }
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/cache/stats")
async def cache_stats():
    """Cache statistics endpoint"""
    return {
        "cache_hits": 0,
        "cache_misses": 0,
        "cache_size": 0,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🚀 Starting RAG API Service on port 8005...")
    print("📍 Service URL: http://localhost:8005")
    print("📊 Health Check: http://localhost:8005/health")
    print("🔍 API Docs: http://localhost:8005/docs")
    print("")
    
    uvicorn.run(
        "rag_api_service:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    ) 