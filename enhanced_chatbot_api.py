#!/usr/bin/env python3
"""
增強版失智小助手 Chatbot API
支援 M1-M4 模組分析
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
import os
from datetime import datetime

app = FastAPI(
    title="增強版失智小助手 Chatbot API",
    description="支援 M1-M4 模組的失智症分析服務",
    version="2.0.0"
)

class ChatbotRequest(BaseModel):
    message: str
    user_id: str = "line_user"

class ChatbotResponse(BaseModel):
    type: str = "flex"
    altText: str = "失智症分析結果"
    contents: Dict[str, Any]

# M1 警訊關鍵詞
M1_WARNING_SIGNS = {
    "M1-01": ["忘記", "記憶", "記不住", "想不起", "重複問"],
    "M1-02": ["不會用", "忘記關", "操作", "使用", "功能"],
    "M1-03": ["迷路", "找不到", "方向", "空間", "位置"],
    "M1-04": ["說不出", "找不到詞", "表達困難", "語言", "溝通"],
    "M1-05": ["判斷力", "決定", "選擇", "邏輯", "判斷"]
}

# M2 病程階段關鍵詞
M2_STAGES = {
    "輕度": ["輕度", "初期", "剛開始", "記憶力", "忘記", "語言"],
    "中度": ["中度", "中期", "明顯", "迷路", "不會用", "暴躁"],
    "重度": ["重度", "晚期", "嚴重", "完全", "不認識", "臥床"]
}

# M3 BPSD 症狀關鍵詞
M3_BPSD_SYMPTOMS = {
    "妄想": ["妄想", "懷疑", "被害", "被偷", "被騙"],
    "幻覺": ["幻覺", "看到", "聽到", "不存在", "幻象"],
    "憂鬱": ["憂鬱", "沮喪", "悲觀", "無望", "自責"],
    "焦慮": ["焦慮", "緊張", "擔心", "不安", "恐懼"],
    "易怒": ["易怒", "暴躁", "生氣", "激動", "攻擊"]
}

# M4 照護需求關鍵詞
M4_CARE_NEEDS = {
    "醫療": ["醫生", "醫院", "治療", "藥物", "檢查"],
    "照護": ["照顧", "護理", "協助", "幫助", "支持"],
    "安全": ["安全", "防護", "跌倒", "走失", "意外"],
    "環境": ["環境", "居家", "改造", "設備", "設施"],
    "社會": ["社會", "資源", "補助", "服務", "團體"]
}

def analyze_m1_warning_signs(text: str) -> Dict[str, Any]:
    """M1 警訊分析"""
    text_lower = text.lower()
    detected_signs = []
    
    for sign_id, keywords in M1_WARNING_SIGNS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_signs.append(sign_id)
                break
    
    return {
        "module": "M1",
        "detected_signs": detected_signs,
        "count": len(detected_signs),
        "analysis": f"檢測到 {len(detected_signs)} 個警訊"
    }

def analyze_m2_progression(text: str) -> Dict[str, Any]:
    """M2 病程階段分析"""
    text_lower = text.lower()
    detected_stage = "輕度"  # 預設
    
    for stage, keywords in M2_STAGES.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_stage = stage
                break
    
    return {
        "module": "M2",
        "detected_stage": detected_stage,
        "analysis": f"評估病程階段：{detected_stage}"
    }

def analyze_m3_bpsd(text: str) -> Dict[str, Any]:
    """M3 BPSD 症狀分析"""
    text_lower = text.lower()
    detected_symptoms = []
    
    for symptom, keywords in M3_BPSD_SYMPTOMS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_symptoms.append(symptom)
                break
    
    return {
        "module": "M3",
        "detected_symptoms": detected_symptoms,
        "count": len(detected_symptoms),
        "analysis": f"檢測到 {len(detected_symptoms)} 個 BPSD 症狀"
    }

def analyze_m4_care_needs(text: str) -> Dict[str, Any]:
    """M4 照護需求分析"""
    text_lower = text.lower()
    detected_needs = []
    
    for need, keywords in M4_CARE_NEEDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_needs.append(need)
                break
    
    return {
        "module": "M4",
        "detected_needs": detected_needs,
        "count": len(detected_needs),
        "analysis": f"識別 {len(detected_needs)} 個照護需求"
    }

def create_m1_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建 M1 警訊 Flex Message"""
    signs_text = "\n• ".join(analysis["detected_signs"]) if analysis["detected_signs"] else "未檢測到明顯警訊"
    
    return {
        "type": "flex",
        "altText": "M1 警訊分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🚨 M1 警訊分析",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#E74C3C"
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
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 檢測到的警訊：\n• {signs_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#E74C3C" if analysis["detected_signs"] else "#27AE60"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：及早發現，及早介入",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ]
            }
        }
    }

def create_m2_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建 M2 病程階段 Flex Message"""
    stage_colors = {
        "輕度": "#F39C12",
        "中度": "#E67E22", 
        "重度": "#C0392B"
    }
    
    return {
        "type": "flex",
        "altText": "M2 病程階段分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📊 M2 病程階段",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "lg"
                    }
                ],
                "backgroundColor": stage_colors.get(analysis["detected_stage"], "#95A5A6")
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
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🎯 評估階段：{analysis['detected_stage']}",
                        "size": "sm",
                        "color": stage_colors.get(analysis["detected_stage"], "#95A5A6")
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：根據階段調整照護策略",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ]
            }
        }
    }

def create_m3_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建 M3 BPSD 症狀 Flex Message"""
    symptoms_text = "\n• ".join(analysis["detected_symptoms"]) if analysis["detected_symptoms"] else "未檢測到明顯 BPSD 症狀"
    
    return {
        "type": "flex",
        "altText": "M3 BPSD 症狀分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 M3 BPSD 症狀",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#9B59B6"
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
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 檢測到的症狀：\n• {symptoms_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#9B59B6" if analysis["detected_symptoms"] else "#27AE60"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：尋求專業醫療協助",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ]
            }
        }
    }

def create_m4_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建 M4 照護需求 Flex Message"""
    needs_text = "\n• ".join(analysis["detected_needs"]) if analysis["detected_needs"] else "未識別特定照護需求"
    
    return {
        "type": "flex",
        "altText": "M4 照護需求分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🏥 M4 照護需求",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "lg"
                    }
                ],
                "backgroundColor": "#3498DB"
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
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"🎯 識別的需求：\n• {needs_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#3498DB" if analysis["detected_needs"] else "#27AE60"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：尋求相關資源協助",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ]
            }
        }
    }

def analyze_comprehensive(text: str) -> Dict[str, Any]:
    """綜合分析所有模組"""
    m1_analysis = analyze_m1_warning_signs(text)
    m2_analysis = analyze_m2_progression(text)
    m3_analysis = analyze_m3_bpsd(text)
    m4_analysis = analyze_m4_care_needs(text)
    
    return {
        "M1": m1_analysis,
        "M2": m2_analysis,
        "M3": m3_analysis,
        "M4": m4_analysis
    }

@app.get("/")
async def root():
    """API 根端點"""
    return {
        "service": "增強版失智小助手 Chatbot API",
        "version": "2.0.0",
        "description": "支援 M1-M4 模組的失智症分析服務",
        "modules": ["M1", "M2", "M3", "M4"],
        "endpoints": {
            "POST /analyze": "綜合分析",
            "POST /analyze/m1": "M1 警訊分析",
            "POST /analyze/m2": "M2 病程分析", 
            "POST /analyze/m3": "M3 BPSD 分析",
            "POST /analyze/m4": "M4 照護需求分析",
            "GET /health": "健康檢查"
        }
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "service": "增強版失智小助手 Chatbot API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "modules": ["M1", "M2", "M3", "M4"],
        "features": [
            "M1 警訊分析",
            "M2 病程階段評估", 
            "M3 BPSD 症狀分析",
            "M4 照護需求識別",
            "Flex Message 回應"
        ]
    }

@app.post("/analyze")
async def analyze_message(request: ChatbotRequest):
    """綜合分析用戶訊息"""
    try:
        # 綜合分析
        comprehensive_analysis = analyze_comprehensive(request.message)
        
        # 根據分析結果選擇最適合的模組回應
        if comprehensive_analysis["M1"]["detected_signs"]:
            return create_m1_flex_message(comprehensive_analysis["M1"], request.message)
        elif comprehensive_analysis["M3"]["detected_symptoms"]:
            return create_m3_flex_message(comprehensive_analysis["M3"], request.message)
        elif comprehensive_analysis["M4"]["detected_needs"]:
            return create_m4_flex_message(comprehensive_analysis["M4"], request.message)
        else:
            return create_m2_flex_message(comprehensive_analysis["M2"], request.message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

@app.post("/analyze/m1")
async def analyze_m1(request: ChatbotRequest):
    """M1 警訊分析"""
    try:
        analysis = analyze_m1_warning_signs(request.message)
        return create_m1_flex_message(analysis, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M1 分析失敗：{str(e)}")

@app.post("/analyze/m2")
async def analyze_m2(request: ChatbotRequest):
    """M2 病程階段分析"""
    try:
        analysis = analyze_m2_progression(request.message)
        return create_m2_flex_message(analysis, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M2 分析失敗：{str(e)}")

@app.post("/analyze/m3")
async def analyze_m3(request: ChatbotRequest):
    """M3 BPSD 症狀分析"""
    try:
        analysis = analyze_m3_bpsd(request.message)
        return create_m3_flex_message(analysis, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M3 分析失敗：{str(e)}")

@app.post("/analyze/m4")
async def analyze_m4(request: ChatbotRequest):
    """M4 照護需求分析"""
    try:
        analysis = analyze_m4_care_needs(request.message)
        return create_m4_flex_message(analysis, request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M4 分析失敗：{str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("ENHANCED_CHATBOT_PORT", "8008"))
    uvicorn.run(app, host="0.0.0.0", port=port) 