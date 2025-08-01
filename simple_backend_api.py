#!/usr/bin/env python3
"""
Enhanced Backend API for LINE Bot with Dynamic Analysis
"""

import os
import logging
import re
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Enhanced LINE Bot Backend API",
    description="Backend API for LINE Bot dementia analysis with dynamic responses",
    version="2.0.0"
)

# Pydantic models
class MessageRequest(BaseModel):
    text: str
    user_id: str = "demo_user"

def analyze_user_input(text: str) -> Dict[str, Any]:
    """Analyze user input and determine the type of question"""
    text_lower = text.lower()
    
    # Memory-related keywords
    memory_keywords = ['忘記', '記憶', '記不住', '想不起來', '失憶', '健忘']
    # Care-related keywords  
    care_keywords = ['照顧', '照護', '護理', '如何', '怎麼辦', '方法', '建議']
    # Symptom-related keywords
    symptom_keywords = ['症狀', '表現', '行為', '異常', '問題', '狀況']
    # Stage-related keywords
    stage_keywords = ['階段', '程度', '嚴重', '輕微', '中度', '重度']
    
    # Determine analysis type
    if any(keyword in text_lower for keyword in memory_keywords):
        return {
            "type": "memory_analysis",
            "confidence": 0.85,
            "warning_level": "moderate",
            "symptoms": ["記憶力下降", "經常忘記日常事務"],
            "recommendations": ["建議進行認知功能評估", "保持規律作息", "使用備忘錄"]
        }
    elif any(keyword in text_lower for keyword in care_keywords):
        return {
            "type": "care_guidance", 
            "confidence": 0.90,
            "focus_areas": ["日常生活照顧", "安全防護", "情緒支持"],
            "recommendations": ["建立規律作息", "確保居家安全", "保持耐心溝通"]
        }
    elif any(keyword in text_lower for keyword in symptom_keywords):
        return {
            "type": "symptom_assessment",
            "confidence": 0.80,
            "symptoms": ["行為改變", "情緒波動", "認知功能下降"],
            "interventions": ["行為治療", "環境調整", "藥物治療"]
        }
    elif any(keyword in text_lower for keyword in stage_keywords):
        return {
            "type": "stage_evaluation",
            "confidence": 0.75,
            "current_stage": "需要進一步評估",
            "care_focus": ["症狀管理", "生活品質", "家屬支持"]
        }
    else:
        # Default general analysis
        return {
            "type": "general_consultation",
            "confidence": 0.70,
            "message": "建議諮詢專業醫師進行詳細評估",
            "next_steps": ["認知功能測試", "影像學檢查", "專科醫師診斷"]
        }

def create_dynamic_flex_message(text: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Create a dynamic Flex Message based on analysis results"""
    
    analysis_type = analysis.get("type", "general")
    
    if analysis_type == "memory_analysis":
        return {
            "type": "flex",
            "altText": f"記憶力分析：{text}",
            "contents": {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🧠 記憶力分析",
                            "size": "lg",
                            "weight": "bold",
                            "color": "#212121"
                        },
                        {
                            "type": "text",
                            "text": f"AI 信心度 {analysis.get('confidence', 0.8) * 100:.0f}%",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F5F5F5",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⚠️ 觀察到記憶力相關症狀",
                            "size": "sm",
                            "color": "#FF9800",
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "📋 建議進行認知功能評估",
                            "size": "sm",
                            "color": "#2196F3",
                            "wrap": True,
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "💡 保持規律作息，使用備忘錄",
                            "size": "sm",
                            "color": "#4CAF50",
                            "wrap": True,
                            "margin": "sm"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看詳細評估",
                                "data": "memory_detail"
                            },
                            "style": "primary",
                            "color": "#2196F3",
                            "margin": "sm"
                        }
                    ]
                }
            }
        }
    
    elif analysis_type == "care_guidance":
        return {
            "type": "flex",
            "altText": f"照護指導：{text}",
            "contents": {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏥 照護指導",
                            "size": "lg",
                            "weight": "bold",
                            "color": "#212121"
                        },
                        {
                            "type": "text",
                            "text": f"AI 信心度 {analysis.get('confidence', 0.9) * 100:.0f}%",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F5F5F5",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📅 建立規律作息時間表",
                            "size": "sm",
                            "color": "#2196F3",
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "🏠 確保居家環境安全",
                            "size": "sm",
                            "color": "#4CAF50",
                            "wrap": True,
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "💬 保持耐心溝通態度",
                            "size": "sm",
                            "color": "#FF9800",
                            "wrap": True,
                            "margin": "sm"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看照護技巧",
                                "data": "care_tips"
                            },
                            "style": "primary",
                            "color": "#2196F3",
                            "margin": "sm"
                        }
                    ]
                }
            }
        }
    
    elif analysis_type == "symptom_assessment":
        return {
            "type": "flex",
            "altText": f"症狀評估：{text}",
            "contents": {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 症狀評估",
                            "size": "lg",
                            "weight": "bold",
                            "color": "#212121"
                        },
                        {
                            "type": "text",
                            "text": f"AI 信心度 {analysis.get('confidence', 0.8) * 100:.0f}%",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F5F5F5",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📊 行為改變評估",
                            "size": "sm",
                            "color": "#2196F3",
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "💊 可能需要藥物治療",
                            "size": "sm",
                            "color": "#FF9800",
                            "wrap": True,
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "🏠 環境調整建議",
                            "size": "sm",
                            "color": "#4CAF50",
                            "wrap": True,
                            "margin": "sm"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "查看治療方案",
                                "data": "treatment_plan"
                            },
                            "style": "primary",
                            "color": "#2196F3",
                            "margin": "sm"
                        }
                    ]
                }
            }
        }
    
    else:
        # Default general consultation
        return {
            "type": "flex",
            "altText": f"失智症諮詢：{text}",
            "contents": {
                "type": "bubble",
                "size": "mega",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "text",
                            "text": "👨‍⚕️ 專業諮詢",
                            "size": "lg",
                            "weight": "bold",
                            "color": "#212121"
                        },
                        {
                            "type": "text",
                            "text": f"AI 信心度 {analysis.get('confidence', 0.7) * 100:.0f}%",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#F5F5F5",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🏥 建議諮詢專業醫師",
                            "size": "sm",
                            "color": "#2196F3",
                            "wrap": True,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "📋 進行詳細認知功能測試",
                            "size": "sm",
                            "color": "#4CAF50",
                            "wrap": True,
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": "🔬 可能需要影像學檢查",
                            "size": "sm",
                            "color": "#FF9800",
                            "wrap": True,
                            "margin": "sm"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FFFFFF",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "預約醫師諮詢",
                                "data": "book_consultation"
                            },
                            "style": "primary",
                            "color": "#2196F3",
                            "margin": "sm"
                        }
                    ]
                }
            }
        }

@app.get("/")
def root():
    return {
        "message": "Enhanced LINE Bot Backend API",
        "version": "2.0.0",
        "status": "running",
        "features": ["Dynamic Analysis", "Smart Responses", "Flex Messages"]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mode": "enhanced",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/demo/message")
def demo_message(request: MessageRequest):
    """Enhanced demo message endpoint with dynamic analysis"""
    logger.info(f"👤 Demo message from {request.user_id}: {request.text}")
    
    # Analyze user input
    analysis = analyze_user_input(request.text)
    logger.info(f"🔍 Analysis result: {analysis['type']}")
    
    # Create dynamic Flex Message
    flex_message = create_dynamic_flex_message(request.text, analysis)
    
    return flex_message

@app.post("/demo/comprehensive")
def comprehensive_analysis(request: MessageRequest):
    """Comprehensive analysis endpoint"""
    logger.info(f"🔍 Comprehensive analysis for {request.user_id}: {request.text}")
    
    analysis = analyze_user_input(request.text)
    flex_message = create_dynamic_flex_message(request.text, analysis)
    
    return {
        "status": "success",
        "user_input": request.text,
        "analysis": analysis,
        "flex_message": flex_message
    }

@app.post("/test")
def test_endpoint():
    """Test endpoint"""
    return {
        "status": "success",
        "message": "Enhanced Backend API is working",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    print("🚀 Starting Enhanced LINE Bot Backend API...")
    print("🌐 Access demo at: http://localhost:8000/demo")
    print("✨ Features: Dynamic Analysis, Smart Responses")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 