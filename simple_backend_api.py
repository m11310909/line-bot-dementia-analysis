#!/usr/bin/env python3
"""
Enhanced Backend API for LINE Bot with M1-M4 Modules
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
    title="Enhanced LINE Bot Backend API with M1-M4 Modules",
    description="Backend API for LINE Bot dementia analysis with M1-M4 module integration",
    version="3.0.0"
)

# Pydantic models
class MessageRequest(BaseModel):
    text: str
    user_id: str = "demo_user"

def analyze_user_input(text: str) -> Dict[str, Any]:
    """Analyze user input and determine appropriate module response"""
    text_lower = text.lower()
    
    # M1 - Memory Analysis (Warning Signs)
    memory_keywords = ["忘記", "記憶", "記不住", "想不起來", "失憶", "健忘", "瓦斯", "關門", "鑰匙"]
    if any(keyword in text_lower for keyword in memory_keywords):
        return create_m1_memory_analysis_flex_message(text)
    
    # M2 - Disease Progression (Stage Assessment)
    progression_keywords = ["階段", "病程", "發展", "進展", "程度", "嚴重", "輕度", "中度", "重度"]
    if any(keyword in text_lower for keyword in progression_keywords):
        return create_m2_progression_flex_message(text)
    
    # M3 - BPSD Classification (Behavioral Symptoms)
    bpsd_keywords = ["躁動", "憂鬱", "幻覺", "妄想", "行為", "精神", "情緒", "不安", "攻擊"]
    if any(keyword in text_lower for keyword in bpsd_keywords):
        return create_m3_bpsd_flex_message(text)
    
    # M4 - Care Navigation (Task Management)
    care_keywords = ["照顧", "照護", "護理", "如何", "怎麼辦", "方法", "建議", "任務", "安排"]
    if any(keyword in text_lower for keyword in care_keywords):
        return create_m4_care_navigation_flex_message(text)
    
    # Default to M1 General Consultation
    return create_m1_general_consultation_flex_message(text)

def create_m1_memory_analysis_flex_message(text: str) -> Dict[str, Any]:
    """M1 Module: Memory Analysis and Warning Signs"""
    return {
        "type": "flex",
        "altText": f"記憶力分析：{text}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 記憶力分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "認知功能評估",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#4CAF50",
                "paddingAll": 16
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"分析內容：{text}",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ 警訊指標",
                                "weight": "bold",
                                "size": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "• 短期記憶力下降",
                                "size": "sm",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 日常生活能力減退",
                                "size": "sm",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 判斷力與定向感異常",
                                "size": "sm",
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
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "AI 信心度",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "85%",
                                "size": "sm",
                                "color": "#4CAF50",
                                "align": "end"
                            }
                        ]
                    }
                ],
                "paddingAll": 16
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "查看詳細分析",
                            "data": "m1_detailed_analysis"
                        },
                        "style": "primary",
                        "color": "#4CAF50",
                        "margin": "sm"
                    }
                ]
            }
        }
    }

def create_m2_progression_flex_message(text: str) -> Dict[str, Any]:
    """M2 Module: Disease Progression Stage Assessment"""
    return {
        "type": "flex",
        "altText": f"病程階段評估：{text}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📊 病程階段評估",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "疾病發展階段分析",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#FF9800",
                "paddingAll": 16
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"評估內容：{text}",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "早期",
                                        "size": "sm",
                                        "color": "#4CAF50",
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "●",
                                        "size": "lg",
                                        "color": "#4CAF50",
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "━━━",
                                "color": "#E0E0E0",
                                "align": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "中期",
                                        "size": "sm",
                                        "color": "#FF9800",
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "○",
                                        "size": "lg",
                                        "color": "#FF9800",
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "━━━",
                                "color": "#E0E0E0",
                                "align": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "晚期",
                                        "size": "sm",
                                        "color": "#F44336",
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "○",
                                        "size": "lg",
                                        "color": "#F44336",
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "當前階段：早期",
                                "weight": "bold",
                                "size": "sm",
                                "color": "#4CAF50"
                            },
                            {
                                "type": "text",
                                "text": "主要症狀：記憶力下降、判斷力減退",
                                "size": "sm",
                                "color": "#666666",
                                "margin": "xs"
                            }
                        ]
                    }
                ],
                "paddingAll": 16
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "查看完整病程",
                            "data": "m2_full_progression"
                        },
                        "style": "primary",
                        "color": "#FF9800",
                        "margin": "sm"
                    }
                ]
            }
        }
    }

def create_m3_bpsd_flex_message(text: str) -> Dict[str, Any]:
    """M3 Module: BPSD Classification and Intervention"""
    return {
        "type": "flex",
        "altText": f"BPSD 行為分類：{text}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔥 BPSD 行為分類",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "精神行為症狀分析",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#FF5722",
                "paddingAll": 16
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"分析內容：{text}",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "症狀分類",
                                "weight": "bold",
                                "size": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "🔥 躁動",
                                                "size": "sm",
                                                "color": "#FF5722"
                                            }
                                        ],
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "💙 憂鬱",
                                                "size": "sm",
                                                "color": "#607D8B"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
                                "margin": "xs"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "💜 幻覺",
                                                "size": "sm",
                                                "color": "#9C27B0"
                                            }
                                        ],
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "💗 妄想",
                                                "size": "sm",
                                                "color": "#E91E63"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
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
                        "contents": [
                            {
                                "type": "text",
                                "text": "建議處理方式",
                                "weight": "bold",
                                "size": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "• 環境調整：減少刺激源",
                                "size": "sm",
                                "color": "#4CAF50",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 行為介入：建立規律作息",
                                "size": "sm",
                                "color": "#2196F3",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 藥物治療：諮詢醫師",
                                "size": "sm",
                                "color": "#FF9800",
                                "margin": "xs"
                            }
                        ]
                    }
                ],
                "paddingAll": 16
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "查看詳細分類",
                            "data": "m3_detailed_bpsd"
                        },
                        "style": "primary",
                        "color": "#FF5722",
                        "margin": "sm"
                    }
                ]
            }
        }
    }

def create_m4_care_navigation_flex_message(text: str) -> Dict[str, Any]:
    """M4 Module: Care Navigation and Task Management"""
    return {
        "type": "flex",
        "altText": f"照護導航：{text}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🗺️ 照護導航",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "任務地圖與照顧指引",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#2196F3",
                "paddingAll": 16
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"查詢內容：{text}",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "今日照護任務",
                                "weight": "bold",
                                "size": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "🏥 醫療",
                                                "size": "sm",
                                                "color": "#F44336"
                                            },
                                            {
                                                "type": "text",
                                                "text": "回診預約",
                                                "size": "xs",
                                                "color": "#666666"
                                            }
                                        ],
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "🏠 日常",
                                                "size": "sm",
                                                "color": "#4CAF50"
                                            },
                                            {
                                                "type": "text",
                                                "text": "藥物管理",
                                                "size": "xs",
                                                "color": "#666666"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
                                "margin": "xs"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "🛡️ 安全",
                                                "size": "sm",
                                                "color": "#FF9800"
                                            },
                                            {
                                                "type": "text",
                                                "text": "環境檢查",
                                                "size": "xs",
                                                "color": "#666666"
                                            }
                                        ],
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "👥 社交",
                                                "size": "sm",
                                                "color": "#2196F3"
                                            },
                                            {
                                                "type": "text",
                                                "text": "活動安排",
                                                "size": "xs",
                                                "color": "#666666"
                                            }
                                        ],
                                        "flex": 1
                                    }
                                ],
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
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "完成度",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "33%",
                                "size": "sm",
                                "color": "#2196F3",
                                "align": "end"
                            }
                        ]
                    }
                ],
                "paddingAll": 16
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "查看完整任務地圖",
                            "data": "m4_full_tasks"
                        },
                        "style": "primary",
                        "color": "#2196F3",
                        "margin": "sm"
                    }
                ]
            }
        }
    }

def create_m1_general_consultation_flex_message(text: str) -> Dict[str, Any]:
    """M1 Module: General Consultation"""
    return {
        "type": "flex",
        "altText": f"專業諮詢：{text}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "👨‍⚕️ 專業諮詢",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": "失智症照護建議",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": "#607D8B",
                "paddingAll": 16
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"您的問題：{text}",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "建議諮詢方向",
                                "weight": "bold",
                                "size": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "• 神經科醫師：專業診斷",
                                "size": "sm",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 精神科醫師：行為治療",
                                "size": "sm",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 社工師：資源連結",
                                "size": "sm",
                                "margin": "xs"
                            },
                            {
                                "type": "text",
                                "text": "• 照護專員：實務指導",
                                "size": "sm",
                                "margin": "xs"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💡 建議：及早診斷，早期介入",
                        "size": "sm",
                        "color": "#607D8B",
                        "weight": "bold"
                    }
                ],
                "paddingAll": 16
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "預約醫師諮詢",
                            "data": "book_consultation"
                        },
                        "style": "primary",
                        "color": "#607D8B",
                        "margin": "sm"
                    }
                ]
            }
        }
    }

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Enhanced LINE Bot Backend API",
        "version": "3.0.0",
        "modules": ["M1-Memory", "M2-Progression", "M3-BPSD", "M4-Care"],
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "enhanced",
        "modules": {
            "m1_memory": "active",
            "m2_progression": "active", 
            "m3_bpsd": "active",
            "m4_care": "active"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/demo/message")
async def demo_message(request: MessageRequest):
    """Enhanced demo message endpoint with M1-M4 module support"""
    logger.info(f"👤 Demo message from {request.user_id}: {request.text}")
    
    # Analyze user input and generate appropriate response
    response = analyze_user_input(request.text)
    
    return response

@app.post("/demo/comprehensive")
async def comprehensive_analysis(request: MessageRequest):
    """Comprehensive analysis endpoint"""
    logger.info(f"🔍 Comprehensive analysis for {request.user_id}: {request.text}")
    
    # For comprehensive analysis, return M1 response as default
    return create_m1_memory_analysis_flex_message(request.text)

@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"message": "Enhanced Backend API is running with M1-M4 modules!"}

@app.get("/info")
async def info_endpoint():
    """Information endpoint"""
    return {
        "service": "Enhanced LINE Bot Backend API",
        "version": "3.0.0",
        "modules": {
            "M1": "Memory Analysis & Warning Signs",
            "M2": "Disease Progression Assessment", 
            "M3": "BPSD Classification & Intervention",
            "M4": "Care Navigation & Task Management"
        },
        "features": [
            "Dynamic response based on user input",
            "Flex Message generation for each module",
            "Comprehensive dementia care support",
            "XAI integration with confidence scoring"
        ]
    }

if __name__ == "__main__":
    print("🚀 Starting Enhanced LINE Bot Backend API with M1-M4 Modules...")
    print("🌐 Access demo at: http://localhost:8000/demo")
    print("📊 Modules: M1-Memory, M2-Progression, M3-BPSD, M4-Care")
    
    uvicorn.run(
        "simple_backend_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 