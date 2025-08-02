#!/usr/bin/env python3
"""
簡單的失智小助手 Chatbot API
提供基本的失智症分析功能
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import os
from datetime import datetime

app = FastAPI(
    title="失智小助手 Chatbot API",
    description="提供失智症分析服務的簡單 API",
    version="1.0.0"
)

class ChatbotRequest(BaseModel):
    message: str
    user_id: str = "line_user"

class ChatbotResponse(BaseModel):
    type: str = "flex"
    altText: str = "失智症分析結果"
    contents: Dict[str, Any]

# 失智症關鍵詞分析
DEMENTIA_KEYWORDS = {
    "記憶力": ["忘記", "記憶", "重複", "記不住", "想不起"],
    "語言": ["說不出", "找不到詞", "表達困難", "語言"],
    "空間": ["迷路", "找不到", "方向", "空間"],
    "判斷": ["判斷力", "決定", "選擇", "邏輯"],
    "情緒": ["易怒", "焦慮", "憂鬱", "情緒變化"],
    "日常": ["不會用", "忘記關", "操作", "日常生活"]
}

def analyze_dementia_symptoms(text: str) -> Dict[str, Any]:
    """分析文本中的失智症症狀"""
    text_lower = text.lower()
    detected_symptoms = []
    confidence = 0.0
    
    for category, keywords in DEMENTIA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_symptoms.append(category)
                confidence += 0.2
                break
    
    return {
        "detected_symptoms": detected_symptoms,
        "confidence": min(confidence, 1.0),
        "analysis": f"檢測到 {len(detected_symptoms)} 個可能的症狀類別"
    }

def create_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建 Flex Message 格式的回應"""
    
    symptoms_text = "\n• ".join(analysis["detected_symptoms"]) if analysis["detected_symptoms"] else "未檢測到明顯症狀"
    confidence_percent = int(analysis["confidence"] * 100)
    
    return {
        "type": "flex",
        "altText": "失智症分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症症狀分析",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#27AE60"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"📝 您的描述：\n{original_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 分析結果：\n{analysis['analysis']}",
                        "wrap": True,
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"📊 信心度：{confidence_percent}%",
                        "size": "sm",
                        "color": "#27AE60"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 檢測到的症狀類別：\n• {symptoms_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#E74C3C" if analysis["detected_symptoms"] else "#27AE60"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：如有疑慮請諮詢專業醫師",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ]
            }
        }
    }

@app.get("/")
async def root():
    """API 根端點"""
    return {
        "service": "失智小助手 Chatbot API",
        "version": "1.0.0",
        "description": "提供失智症症狀分析服務",
        "endpoints": {
            "POST /analyze": "分析用戶輸入",
            "GET /health": "健康檢查"
        }
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "service": "失智小助手 Chatbot API",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "症狀關鍵詞分析",
            "信心度評估",
            "Flex Message 回應"
        ]
    }

@app.post("/analyze")
async def analyze_message(request: ChatbotRequest):
    """分析用戶訊息"""
    try:
        # 分析症狀
        analysis = analyze_dementia_symptoms(request.message)
        
        # 創建 Flex Message
        flex_message = create_flex_message(analysis, request.message)
        
        return flex_message
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

@app.post("/simple")
async def simple_analyze(request: ChatbotRequest):
    """簡單文字回應（備用格式）"""
    try:
        analysis = analyze_dementia_symptoms(request.message)
        
        return {
            "message": f"分析結果：{analysis['analysis']}，信心度：{int(analysis['confidence'] * 100)}%",
            "confidence": analysis["confidence"],
            "symptoms": analysis["detected_symptoms"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("CHATBOT_PORT", "8007"))
    uvicorn.run(app, host="0.0.0.0", port=port) 