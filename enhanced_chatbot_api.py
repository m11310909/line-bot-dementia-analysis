#!/usr/bin/env python3
"""
增強版失智小助手 Chatbot API
支援 M1-M4 模組分析 + XAI 視覺化
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import json
import os
from datetime import datetime
import re

app = FastAPI(
    title="增強版失智小助手 Chatbot API",
    description="支援 M1-M4 模組的失智症分析服務 + XAI 視覺化",
    version="3.0.0"
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
    """M1 警訊分析 + XAI 推理路徑"""
    text_lower = text.lower()
    detected_signs = []
    reasoning_steps = []
    confidence_scores = []
    
    # XAI 推理路徑分析
    for sign_id, keywords in M1_WARNING_SIGNS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_signs.append(sign_id)
                reasoning_steps.append(f"檢測到關鍵詞 '{keyword}' → {sign_id}")
                confidence_scores.append(0.85)  # 基於關鍵詞匹配的信心度
                break
    
    # 計算整體信心度
    overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
    
    # 生成人性化文字回覆
    if detected_signs:
        if len(detected_signs) >= 3:
            chatbot_reply = f"⚠️ 我注意到您描述的情況中包含了多個失智症警訊。這些症狀確實需要特別關注，建議您盡快安排專業醫療評估。同時，請確保居家環境的安全，避免可能的危險情況。"
        elif len(detected_signs) == 2:
            chatbot_reply = f"🔍 根據您的描述，我檢測到了一些值得注意的警訊。建議您密切觀察這些症狀的變化，並考慮諮詢專業醫師進行進一步評估。"
        else:
            chatbot_reply = f"📝 您提到的情況確實值得關注。雖然目前只檢測到一個警訊，但建議您持續觀察，如果症狀持續或加重，請及時尋求專業協助。"
    else:
        chatbot_reply = f"💡 感謝您的分享。雖然目前沒有檢測到明顯的警訊，但如果您對家人的狀況有任何疑慮，建議您持續觀察並在需要時尋求專業建議。"
    
    return {
        "module": "M1",
        "detected_signs": detected_signs,
        "count": len(detected_signs),
        "analysis": f"檢測到 {len(detected_signs)} 個警訊",
        "chatbot_reply": chatbot_reply,
        "xai_data": {
            "reasoning_steps": reasoning_steps,
            "confidence_score": overall_confidence,
            "feature_importance": {sign: score for sign, score in zip(detected_signs, confidence_scores)},
            "uncertainty_factors": ["症狀描述可能不完整", "需要專業評估確認"] if detected_signs else []
        }
    }

def analyze_m2_progression(text: str) -> Dict[str, Any]:
    """M2 病程階段分析 + XAI 視覺化"""
    text_lower = text.lower()
    detected_stage = "輕度"  # 預設
    reasoning_steps = []
    confidence_score = 0.7
    
    # XAI 推理路徑
    for stage, keywords in M2_STAGES.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_stage = stage
                reasoning_steps.append(f"檢測到關鍵詞 '{keyword}' → 判斷為{stage}階段")
                confidence_score = 0.8 if stage == "中度" else 0.7
                break
    
    # 生成人性化文字回覆
    stage_replies = {
        "輕度": "🟢 根據您的描述，目前可能處於輕度階段。這個階段最重要的是早期介入和適當的照護安排。建議您建立規律的生活作息，並開始規劃長期的照護計畫。",
        "中度": "🟡 您描述的情況符合中度階段的特徵。這個階段需要更多的照護支持，建議您尋求專業的照護服務，並考慮申請相關的社會福利資源。",
        "重度": "🔴 您提到的症狀可能屬於重度階段。這個階段需要全天候的專業照護，建議您立即聯繫專業醫療團隊，並考慮機構照護的選項。"
    }
    
    chatbot_reply = stage_replies.get(detected_stage, "💡 感謝您的分享。建議您諮詢專業醫師進行詳細評估，以確定最適合的照護方案。")
    
    return {
        "module": "M2",
        "detected_stage": detected_stage,
        "analysis": f"評估病程階段：{detected_stage}",
        "chatbot_reply": chatbot_reply,
        "xai_data": {
            "reasoning_steps": reasoning_steps,
            "confidence_score": confidence_score,
            "feature_importance": {"stage_keywords": 0.8, "symptom_patterns": 0.6},
            "uncertainty_factors": ["症狀描述有限", "建議專業評估"]
        }
    }

def analyze_m3_bpsd(text: str) -> Dict[str, Any]:
    """M3 BPSD 症狀分析 + XAI 視覺化"""
    text_lower = text.lower()
    detected_symptoms = []
    reasoning_steps = []
    confidence_scores = []
    
    # XAI 推理路徑
    for symptom, keywords in M3_BPSD_SYMPTOMS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_symptoms.append(symptom)
                reasoning_steps.append(f"檢測到關鍵詞 '{keyword}' → {symptom}症狀")
                confidence_scores.append(0.85)
                break
    
    overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
    
    # 生成人性化文字回覆
    if detected_symptoms:
        if len(detected_symptoms) >= 3:
            chatbot_reply = f"⚠️ 我注意到您描述的行為症狀比較複雜。這些症狀可能對照護者造成很大壓力，建議您尋求專業的精神科醫師協助，並考慮藥物治療的可能性。"
        elif len(detected_symptoms) == 2:
            chatbot_reply = f"🔍 您提到的行為症狀確實需要關注。建議您記錄這些症狀的發生頻率和觸發因素，這將有助於醫師制定更精準的治療方案。"
        else:
            chatbot_reply = f"📝 您描述的行為症狀值得注意。建議您觀察症狀的變化，並在下次就醫時詳細告知醫師，以便調整治療策略。"
    else:
        chatbot_reply = f"💡 感謝您的分享。雖然目前沒有檢測到明顯的行為症狀，但如果您有任何疑慮，建議您諮詢專業醫師進行評估。"
    
    return {
        "module": "M3",
        "detected_symptoms": detected_symptoms,
        "analysis": f"檢測到 {len(detected_symptoms)} 種 BPSD 症狀",
        "chatbot_reply": chatbot_reply,
        "xai_data": {
            "reasoning_steps": reasoning_steps,
            "confidence_score": overall_confidence,
            "feature_importance": {symptom: score for symptom, score in zip(detected_symptoms, confidence_scores)},
            "uncertainty_factors": ["行為描述需要更詳細", "建議專業精神科評估"]
        }
    }

def analyze_m4_care_needs(text: str) -> Dict[str, Any]:
    """M4 照護需求分析 + XAI 視覺化"""
    text_lower = text.lower()
    detected_needs = []
    reasoning_steps = []
    confidence_scores = []
    
    # XAI 推理路徑
    for need_type, keywords in M4_CARE_NEEDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_needs.append(need_type)
                reasoning_steps.append(f"檢測到關鍵詞 '{keyword}' → {need_type}需求")
                confidence_scores.append(0.85)
                break
    
    overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
    
    # 生成人性化文字回覆
    if detected_needs:
        if len(detected_needs) >= 3:
            chatbot_reply = f"🏥 根據您的描述，我建議您尋求多方面的專業協助。這些需求可以通過醫療團隊、社會工作者和照護機構的協調來解決。建議您聯繫當地的長照管理中心尋求協助。"
        elif len(detected_needs) == 2:
            chatbot_reply = f"💼 您提到的需求確實需要專業支持。建議您先諮詢醫師了解醫療需求，同時可以聯繫社會福利機構了解可用的資源和服務。"
        else:
            chatbot_reply = f"📋 您描述的需求我們可以協助您找到合適的資源。建議您先諮詢專業醫師，他們可以為您轉介相關的服務機構。"
    else:
        chatbot_reply = f"💡 感謝您的分享。如果您有任何照護相關的需求或疑問，歡迎隨時詢問，我會協助您找到合適的資源和建議。"
    
    return {
        "module": "M4",
        "detected_needs": detected_needs,
        "analysis": f"識別出 {len(detected_needs)} 項照護需求",
        "chatbot_reply": chatbot_reply,
        "xai_data": {
            "reasoning_steps": reasoning_steps,
            "confidence_score": overall_confidence,
            "feature_importance": {need: score for need, score in zip(detected_needs, confidence_scores)},
            "uncertainty_factors": ["需求描述需要更詳細", "建議專業評估"]
        }
    }

def create_enhanced_m1_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建增強版 M1 警訊 Flex Message + XAI 視覺化"""
    
    # 根據檢測到的警訊數量決定顏色
    warning_count = len(analysis.get("detected_signs", []))
    if warning_count >= 3:
        header_color = "#E74C3C"  # 紅色 - 高風險
        severity_text = "高風險"
    elif warning_count >= 1:
        header_color = "#F39C12"  # 橙色 - 中風險
        severity_text = "中風險"
    else:
        header_color = "#27AE60"  # 綠色 - 低風險
        severity_text = "低風險"
    
    signs_text = "\n• ".join(analysis["detected_signs"]) if analysis["detected_signs"] else "未檢測到明顯警訊"
    
    # XAI 數據
    xai_data = analysis.get("xai_data", {})
    confidence_score = xai_data.get("confidence_score", 0.5)
    reasoning_steps = xai_data.get("reasoning_steps", [])
    
    # 創建信心度視覺化
    confidence_percentage = int(confidence_score * 100)
    confidence_color = "#4CAF50" if confidence_score >= 0.8 else "#FF9800" if confidence_score >= 0.6 else "#F44336"
    
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🚨",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M1 警訊分析",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的失智症警訊評估",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊 風險評估",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": severity_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
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
                        "color": header_color if analysis["detected_signs"] else "#27AE60"
                    },
                    {
                        "type": "separator"
                    },
                    # XAI 信心度視覺化
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 AI 信心度",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}%",
                                "color": confidence_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#F0F0F0",
                        "height": "8px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": confidence_color,
                                "width": f"{confidence_percentage}%",
                                "contents": []
                            }
                        ]
                    },
                    # XAI 推理路徑（簡化版）
                    {
                        "type": "text",
                        "text": "🧠 推理路徑：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": " → ".join(reasoning_steps[:3]) if reasoning_steps else "基於症狀關鍵詞分析",
                        "size": "xs",
                        "color": "#666666",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    # 失智小幫手文字回覆
                    {
                        "type": "text",
                        "text": "💬 失智小幫手：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md",
                        "color": "#2E86AB"
                    },
                    {
                        "type": "text",
                        "text": analysis.get("chatbot_reply", "感謝您的分享，建議您諮詢專業醫師進行評估。"),
                        "size": "sm",
                        "color": "#2E86AB",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
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
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m2_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建增強版 M2 病程階段 Flex Message + XAI 視覺化"""
    
    stage = analysis.get("detected_stage", "輕度")
    stage_colors = {
        "輕度": {"header": "#27AE60", "progress": "#27AE60", "text": "早期階段"},
        "中度": {"header": "#F39C12", "progress": "#F39C12", "text": "中期階段"},
        "重度": {"header": "#E74C3C", "progress": "#E74C3C", "text": "晚期階段"}
    }
    
    color_info = stage_colors.get(stage, stage_colors["輕度"])
    
    # XAI 數據
    xai_data = analysis.get("xai_data", {})
    confidence_score = xai_data.get("confidence_score", 0.7)
    reasoning_steps = xai_data.get("reasoning_steps", [])
    
    # 創建信心度視覺化
    confidence_percentage = int(confidence_score * 100)
    confidence_color = "#4CAF50" if confidence_score >= 0.8 else "#FF9800" if confidence_score >= 0.6 else "#F44336"
    
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M2 病程階段",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的病程評估",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": color_info["header"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📈 階段評估",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": color_info["text"],
                                "color": color_info["header"],
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
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
                    # XAI 信心度視覺化
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 AI 信心度",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}%",
                                "color": confidence_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#F0F0F0",
                        "height": "8px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": confidence_color,
                                "width": f"{confidence_percentage}%",
                                "contents": []
                            }
                        ]
                    },
                    # XAI 推理路徑
                    {
                        "type": "text",
                        "text": "🧠 推理路徑：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": " → ".join(reasoning_steps[:3]) if reasoning_steps else "基於症狀模式分析",
                        "size": "xs",
                        "color": "#666666",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    # 失智小幫手文字回覆
                    {
                        "type": "text",
                        "text": "💬 失智小幫手：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md",
                        "color": "#2E86AB"
                    },
                    {
                        "type": "text",
                        "text": analysis.get("chatbot_reply", "感謝您的分享，建議您諮詢專業醫師進行評估。"),
                        "size": "sm",
                        "color": "#2E86AB",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：定期追蹤病程變化",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m3_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建增強版 M3 BPSD 症狀 Flex Message + XAI 視覺化"""
    
    symptoms = analysis.get("detected_symptoms", [])
    symptom_count = len(symptoms)
    
    # 根據症狀數量決定顏色
    if symptom_count >= 3:
        header_color = "#E74C3C"  # 紅色 - 多種症狀
        severity_text = "多種症狀"
    elif symptom_count >= 1:
        header_color = "#F39C12"  # 橙色 - 單一症狀
        severity_text = "單一症狀"
    else:
        header_color = "#27AE60"  # 綠色 - 無明顯症狀
        severity_text = "無明顯症狀"
    
    symptoms_text = "\n• ".join(symptoms) if symptoms else "未檢測到明顯 BPSD 症狀"
    
    # XAI 數據
    xai_data = analysis.get("xai_data", {})
    confidence_score = xai_data.get("confidence_score", 0.5)
    reasoning_steps = xai_data.get("reasoning_steps", [])
    
    # 創建信心度視覺化
    confidence_percentage = int(confidence_score * 100)
    confidence_color = "#4CAF50" if confidence_score >= 0.8 else "#FF9800" if confidence_score >= 0.6 else "#F44336"
    
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🧠",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M3 BPSD 症狀",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的行為心理症狀分析",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 症狀評估",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": severity_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
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
                        "color": header_color if symptoms else "#27AE60"
                    },
                    {
                        "type": "separator"
                    },
                    # XAI 信心度視覺化
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 AI 信心度",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}%",
                                "color": confidence_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#F0F0F0",
                        "height": "8px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": confidence_color,
                                "width": f"{confidence_percentage}%",
                                "contents": []
                            }
                        ]
                    },
                    # XAI 推理路徑
                    {
                        "type": "text",
                        "text": "🧠 推理路徑：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": " → ".join(reasoning_steps[:3]) if reasoning_steps else "基於行為描述分析",
                        "size": "xs",
                        "color": "#666666",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    # 失智小幫手文字回覆
                    {
                        "type": "text",
                        "text": "💬 失智小幫手：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md",
                        "color": "#2E86AB"
                    },
                    {
                        "type": "text",
                        "text": analysis.get("chatbot_reply", "感謝您的分享，建議您諮詢專業醫師進行評估。"),
                        "size": "sm",
                        "color": "#2E86AB",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：尋求專業精神科評估",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }

def create_enhanced_m4_flex_message(analysis: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """創建增強版 M4 照護需求 Flex Message + XAI 視覺化"""
    
    needs = analysis.get("detected_needs", [])
    needs_count = len(needs)
    
    # 根據需求數量決定顏色
    if needs_count >= 3:
        header_color = "#3498DB"  # 藍色 - 多種需求
        priority_text = "高優先級"
    elif needs_count >= 1:
        header_color = "#9B59B6"  # 紫色 - 單一需求
        priority_text = "中優先級"
    else:
        header_color = "#27AE60"  # 綠色 - 無明顯需求
        priority_text = "低優先級"
    
    needs_text = "\n• ".join(needs) if needs else "未檢測到明顯照護需求"
    
    # XAI 數據
    xai_data = analysis.get("xai_data", {})
    confidence_score = xai_data.get("confidence_score", 0.5)
    reasoning_steps = xai_data.get("reasoning_steps", [])
    
    # 創建信心度視覺化
    confidence_percentage = int(confidence_score * 100)
    confidence_color = "#4CAF50" if confidence_score >= 0.8 else "#FF9800" if confidence_score >= 0.6 else "#F44336"
    
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
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🏥",
                                "size": "lg",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "M4 照護需求",
                                        "weight": "bold",
                                        "color": "#ffffff",
                                        "size": "lg"
                                    },
                                    {
                                        "type": "text",
                                        "text": "AI 驅動的照護需求識別",
                                        "color": "#ffffff",
                                        "size": "xs",
                                        "opacity": 0.8
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": header_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📋 需求評估",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": priority_text,
                                "color": header_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
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
                        "text": f"📍 識別的需求：\n• {needs_text}",
                        "wrap": True,
                        "size": "sm",
                        "color": header_color if needs else "#27AE60"
                    },
                    {
                        "type": "separator"
                    },
                    # XAI 信心度視覺化
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎯 AI 信心度",
                                "weight": "bold",
                                "size": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{confidence_percentage}%",
                                "color": confidence_color,
                                "weight": "bold",
                                "size": "sm",
                                "align": "end"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "backgroundColor": "#F0F0F0",
                        "height": "8px",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": confidence_color,
                                "width": f"{confidence_percentage}%",
                                "contents": []
                            }
                        ]
                    },
                    # XAI 推理路徑
                    {
                        "type": "text",
                        "text": "🧠 推理路徑：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": " → ".join(reasoning_steps[:3]) if reasoning_steps else "基於需求描述分析",
                        "size": "xs",
                        "color": "#666666",
                        "wrap": True
                    },
                    {
                        "type": "separator"
                    },
                    # 失智小幫手文字回覆
                    {
                        "type": "text",
                        "text": "💬 失智小幫手：",
                        "weight": "bold",
                        "size": "sm",
                        "margin": "md",
                        "color": "#2E86AB"
                    },
                    {
                        "type": "text",
                        "text": analysis.get("chatbot_reply", "感謝您的分享，建議您諮詢專業醫師進行評估。"),
                        "size": "sm",
                        "color": "#2E86AB",
                        "wrap": True
                    }
                ],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議：聯繫相關照護資源",
                        "size": "xs",
                        "color": "#666666",
                        "align": "center"
                    }
                ],
                "paddingAll": "15px"
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
        "version": "3.0.0",
        "description": "支援 M1-M4 模組的失智症分析服務 + XAI 視覺化",
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
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
        "modules": ["M1", "M2", "M3", "M4"],
        "features": [
            "M1 警訊分析",
            "M2 病程階段評估", 
            "M3 BPSD 症狀分析",
            "M4 照護需求識別",
            "增強版 Flex Message 回應",
            "XAI 信心度評估",
            "XAI 推理路徑視覺化"
        ]
    }

@app.post("/analyze")
async def analyze_message(request: ChatbotRequest) -> ChatbotResponse:
    """智能分析訊息並自動選擇最適合的模組"""
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="訊息不能為空")
        
        # 計算各模組的匹配分數
        module_scores = {}
        
        # M1 警訊分析分數
        m1_analysis = analyze_m1_warning_signs(message)
        module_scores["M1"] = len(m1_analysis["detected_signs"]) / 5.0  # 標準化分數
        
        # M2 病程階段分數
        m2_analysis = analyze_m2_progression(message)
        stage_weights = {"輕度": 0.3, "中度": 0.6, "重度": 0.9}
        module_scores["M2"] = stage_weights.get(m2_analysis["detected_stage"], 0.3)
        
        # M3 BPSD 症狀分數
        m3_analysis = analyze_m3_bpsd(message)
        module_scores["M3"] = len(m3_analysis["detected_symptoms"]) / 5.0
        
        # M4 照護需求分數 - 提高權重
        m4_analysis = analyze_m4_care_needs(message)
        module_scores["M4"] = len(m4_analysis["detected_needs"]) / 3.0  # 提高 M4 權重
        
        # 特殊處理：如果明確提到醫療、照護等關鍵詞，優先選擇 M4
        care_keywords = ["醫療", "醫生", "醫院", "治療", "照護", "照顧", "協助", "幫助", "支持", "資源", "服務"]
        if any(keyword in message for keyword in care_keywords):
            module_scores["M4"] += 0.5  # 額外加分
        
        # 選擇分數最高的模組
        selected_module = max(module_scores, key=module_scores.get)
        
        # 根據選擇的模組創建回應
        if selected_module == "M1":
            flex_message = create_enhanced_m1_flex_message(m1_analysis, message)
        elif selected_module == "M2":
            flex_message = create_enhanced_m2_flex_message(m2_analysis, message)
        elif selected_module == "M3":
            flex_message = create_enhanced_m3_flex_message(m3_analysis, message)
        elif selected_module == "M4":
            flex_message = create_enhanced_m4_flex_message(m4_analysis, message)
        else:
            # 預設使用 M1
            flex_message = create_enhanced_m1_flex_message(m1_analysis, message)
        
        return ChatbotResponse(**flex_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

@app.post("/analyze/m1")
async def analyze_m1(request: ChatbotRequest) -> ChatbotResponse:
    """M1 警訊分析"""
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="訊息不能為空")
        
        analysis = analyze_m1_warning_signs(message)
        flex_message = create_enhanced_m1_flex_message(analysis, message)
        
        return ChatbotResponse(**flex_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M1 分析失敗：{str(e)}")

@app.post("/analyze/m2")
async def analyze_m2(request: ChatbotRequest) -> ChatbotResponse:
    """M2 病程階段分析"""
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="訊息不能為空")
        
        analysis = analyze_m2_progression(message)
        flex_message = create_enhanced_m2_flex_message(analysis, message)
        
        return ChatbotResponse(**flex_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M2 分析失敗：{str(e)}")

@app.post("/analyze/m3")
async def analyze_m3(request: ChatbotRequest) -> ChatbotResponse:
    """M3 BPSD 症狀分析"""
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="訊息不能為空")
        
        analysis = analyze_m3_bpsd(message)
        flex_message = create_enhanced_m3_flex_message(analysis, message)
        
        return ChatbotResponse(**flex_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M3 分析失敗：{str(e)}")

@app.post("/analyze/m4")
async def analyze_m4(request: ChatbotRequest) -> ChatbotResponse:
    """M4 照護需求分析"""
    try:
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="訊息不能為空")
        
        analysis = analyze_m4_care_needs(message)
        flex_message = create_enhanced_m4_flex_message(analysis, message)
        
        return ChatbotResponse(**flex_message)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"M4 分析失敗：{str(e)}")

@app.get("/xai-info")
async def get_xai_info():
    """獲取 XAI 系統資訊"""
    return {
        "xai_features": {
            "confidence_scoring": "動態信心度評估系統",
            "reasoning_paths": "AI 推理路徑視覺化",
            "feature_importance": "關鍵特徵重要性分析",
            "uncertainty_factors": "不確定性因素識別",
            "visual_indicators": "信心度進度條和顏色編碼"
        },
        "modules": {
            "M1": {
                "description": "十大警訊比對卡",
                "xai_components": ["關鍵詞標記", "症狀分類", "警訊判斷", "信心度評估"]
            },
            "M2": {
                "description": "病程階段對照",
                "xai_components": ["症狀吻合度", "階段特徵符合度", "進展合理性"]
            },
            "M3": {
                "description": "BPSD 症狀分類",
                "xai_components": ["行為模式識別", "症狀嚴重度評估", "處理方案建議"]
            },
            "M4": {
                "description": "照護需求識別",
                "xai_components": ["需求分類", "優先級評估", "資源連結建議"]
            }
        },
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("ENHANCED_CHATBOT_PORT", "8008"))
    uvicorn.run(app, host="0.0.0.0", port=port) 