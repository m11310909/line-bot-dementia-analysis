#!/usr/bin/env python3
"""
Simple Backend API for LINE Bot
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Simple LINE Bot Backend API",
    description="Backend API for LINE Bot dementia analysis",
    version="1.0.0"
)

# Pydantic models
class MessageRequest(BaseModel):
    text: str
    user_id: str = "demo_user"

def create_simple_flex_message(text: str) -> Dict[str, Any]:
    """Create a simple Flex Message for testing"""
    return {
        "type": "flex",
        "altText": f"失智照護分析：{text}",
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
                        "text": "AI 分析結果",
                        "size": "lg",
                        "weight": "bold",
                        "color": "#212121"
                    },
                    {
                        "type": "text",
                        "text": "記憶力評估",
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
                        "text": "AI 信心度 85%",
                        "size": "xs",
                        "color": "#666666",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#F0F0F0",
                        "height": 8,
                        "cornerRadius": 4,
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#4CAF50",
                                "width": "85%",
                                "cornerRadius": 4,
                                "contents": []
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#E8F5E9",
                                "cornerRadius": 8,
                                "paddingAll": "16px",
                                "margin": "sm",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "👴",
                                                "size": "lg",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": "正常老化",
                                                "size": "sm",
                                                "weight": "bold",
                                                "color": "#212121",
                                                "flex": 1,
                                                "margin": "sm"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": "偶爾忘記但能回想起來",
                                        "size": "xs",
                                        "color": "#666666",
                                        "wrap": True,
                                        "margin": "sm"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#FFF3E0",
                                "cornerRadius": 8,
                                "paddingAll": "16px",
                                "margin": "sm",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "⚠️",
                                                "size": "lg",
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": "失智警訊",
                                                "size": "sm",
                                                "weight": "bold",
                                                "color": "#212121",
                                                "flex": 1,
                                                "margin": "sm"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "text",
                                        "text": "經常忘記且無法回想",
                                        "size": "xs",
                                        "color": "#666666",
                                        "wrap": True,
                                        "margin": "sm"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": "💡 觀察到記憶力相關症狀，建議進一步評估",
                        "size": "sm",
                        "color": "#2196F3",
                        "wrap": True,
                        "margin": "md"
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
                            "label": "查看詳細分析",
                            "data": "m1_detail"
                        },
                        "style": "primary",
                        "height": 44,
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
        "message": "Simple LINE Bot Backend API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mode": "simple",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/demo/message")
def demo_message(request: MessageRequest):
    """Demo message endpoint"""
    logger.info(f"👤 Demo message from {request.user_id}: {request.text}")
    return create_simple_flex_message(request.text)

@app.post("/demo/comprehensive")
def comprehensive_analysis(request: MessageRequest):
    """Comprehensive analysis endpoint"""
    logger.info(f"🔍 Comprehensive analysis for {request.user_id}: {request.text}")
    return {
        "status": "success",
        "user_input": request.text,
        "analysis_results": {
            "m1": create_simple_flex_message(request.text)
        }
    }

@app.post("/test")
def test_endpoint():
    """Test endpoint"""
    return {
        "status": "success",
        "message": "Backend API is working"
    }

if __name__ == "__main__":
    print("🚀 Starting Simple LINE Bot Backend API...")
    print("🌐 Access demo at: http://localhost:8000/demo")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 