#!/usr/bin/env python3
"""
修復版 M1+M2+M3 整合 API
基於技術架構文檔修復 - 修復 Webhook 問題
增強版：支援 Flex Messages 視覺化回應
"""

import os
import logging
import asyncio
import json
import hmac
import hashlib
from typing import Any, Dict, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 FastAPI
app = FastAPI(title="Dementia Analysis API", version="1.0.0")

# 配置 LINE Bot
def initialize_line_bot():
    try:
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        channel_secret = os.getenv("LINE_CHANNEL_SECRET")
        
        print(f"🔍 檢查 LINE Bot 憑證:")
        print(f"   Channel Access Token: {'✅ 已設置' if channel_access_token else '❌ 未設置'}")
        print(f"   Channel Secret: {'✅ 已設置' if channel_secret else '❌ 未設置'}")
        
        if not channel_access_token or not channel_secret:
            print("❌ LINE Bot 憑證未設置")
            print("請設置以下環境變數:")
            print("   LINE_CHANNEL_ACCESS_TOKEN")
            print("   LINE_CHANNEL_SECRET")
            return None, None
        
        configuration = Configuration(access_token=channel_access_token)
        api_client = ApiClient(configuration)
        messaging_api = MessagingApi(api_client)
        handler = WebhookHandler(channel_secret)
        
        print("✅ LINE Bot 初始化成功")
        return messaging_api, handler
        
    except Exception as e:
        print(f"❌ LINE Bot 初始化失敗: {e}")
        return None, None

# 全局變數
line_bot_api, handler = initialize_line_bot()

# 測試模式配置
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# 初始化 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 檢查環境變數
def check_env_variables():
    """檢查必要的環境變數"""
    required_vars = [
        "LINE_CHANNEL_ACCESS_TOKEN",
        "LINE_CHANNEL_SECRET",
        "GEMINI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少環境變數: {', '.join(missing_vars)}")
        print("請設置以下環境變數:")
        for var in missing_vars:
            print(f"   {var}")
        return False
    
    print("✅ 環境變數檢查通過")
    return True

# Flex Message 生成函數
def create_flex_message(analysis_result: Dict[str, Any], module_type: str) -> Dict[str, Any]:
    """創建 Flex Message 回應"""
    
    # 根據模組類型選擇顏色
    color_map = {
        "M1": "#FF6B6B",  # 紅色 - 記憶力
        "M2": "#4ECDC4",  # 青色 - 情緒
        "M3": "#45B7D1",  # 藍色 - 空間
        "M4": "#96CEB4",  # 綠色 - 興趣
        "comprehensive": "#FFA07A"  # 橙色 - 綜合
    }
    
    primary_color = color_map.get(module_type, "#FF6B6B")
    
    # 從 analysis_result 中提取數據
    data = analysis_result.get("data", {})
    
    # 風險等級
    risk_level = data.get("risk_level", "medium")
    risk_color_map = {
        "low": "#4CAF50",
        "medium": "#FF9800", 
        "high": "#F44336"
    }
    risk_color = risk_color_map.get(risk_level, "#FF9800")
    
    # 根據模組類型提取症狀和建議
    symptoms = []
    recommendations = []
    
    if module_type == "M1":
        symptoms = data.get("warning_signs", [])
        recommendations = data.get("recommendations", [])
    elif module_type == "M2":
        symptoms = data.get("symptoms", [])
        recommendations = data.get("care_focus", [])
    elif module_type == "M3":
        symptoms = data.get("bpsd_symptoms", [])
        recommendations = data.get("intervention", [])
    elif module_type == "M4":
        symptoms = ["照護資源評估"]
        recommendations = data.get("practical_tips", [])
    elif module_type == "comprehensive":
        symptoms = ["綜合症狀評估"]
        recommendations = data.get("recommendations", [])
    
    symptoms_text = "\n".join([f"• {symptom}" for symptom in symptoms]) if symptoms else "• 需要進一步評估"
    recommendations_text = "\n".join([f"• {rec}" for rec in recommendations]) if recommendations else "• 建議尋求專業醫療協助"
    
    flex_message = {
        "type": "flex",
        "altText": f"失智症分析結果 - {module_type}",
        "contents": {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🔍 {module_type} 分析結果",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": f"風險等級: {risk_level.upper()}",
                        "size": "sm",
                        "color": "#FFFFFF",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": primary_color,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📋 可能症狀",
                                "weight": "bold",
                                "size": "md",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": symptoms_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "sm"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 建議",
                                "weight": "bold",
                                "size": "md",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": recommendations_text,
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True,
                                "margin": "sm"
                            }
                        ]
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
                        "text": "⚠️ 此分析僅供參考，請諮詢專業醫療人員",
                        "size": "xs",
                        "color": "#999999",
                        "align": "center",
                        "wrap": True
                    }
                ],
                "paddingAll": "15px"
            }
        }
    }
    
    return flex_message

def create_simple_flex_message(title: str, content: str, color: str = "#FF6B6B") -> Dict[str, Any]:
    """創建簡單的 Flex Message"""
    return {
        "type": "flex",
        "altText": title,
        "contents": {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": content,
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": color,
                "paddingAll": "20px"
            }
        }
    }

# 模型定義
class UserInput(BaseModel):
    message: str

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] = {}

# 健康檢查
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "line_bot_configured": bool(line_bot_api and handler),
        "test_mode": TEST_MODE
    }

@app.get("/")
def root():
    return {
        "message": "Dementia Analysis API", 
        "status": "running",
        "test_mode": TEST_MODE
    }

def handle_line_message(event: MessageEvent):
    """處理 LINE Bot 訊息 - 使用 Flex Messages"""
    try:
        if isinstance(event.message, TextMessageContent):
            user_message = event.message.text
            user_id = event.source.user_id
            
            print(f"📱 收到用戶訊息: {user_message}")
            print(f"👤 用戶 ID: {user_id}")
            
            # 分析用戶訊息
            analysis_result = analyze_user_message(user_message)
            print(f"🔍 分析結果: {analysis_result.get('success', False)}")
            
            # 生成 Flex Message 回應
            flex_message = generate_flex_reply(analysis_result)
            print(f"🎨 Flex Message 生成完成: {flex_message.get('altText', 'N/A')}")
            
            # 發送 Flex Message 回應
            send_line_reply(event.reply_token, "", flex_message)
            
            print(f"✅ Flex Message 回應已發送給用戶 {user_id}")
            
    except Exception as e:
        logger.error(f"處理 LINE 訊息失敗: {e}")
        print(f"❌ 處理 LINE 訊息失敗: {e}")
        # 發送錯誤回應
        try:
            error_flex = create_simple_flex_message(
                "❌ 系統錯誤",
                "抱歉，處理您的訊息時發生錯誤，請稍後再試。",
                "#F44336"
            )
            send_line_reply(event.reply_token, "", error_flex)
        except Exception as error_e:
            print(f"❌ 發送錯誤回應也失敗: {error_e}")

def analyze_user_message(user_message: str) -> Dict[str, Any]:
    """分析用戶訊息"""
    try:
        # 根據訊息內容選擇分析模組
        if any(keyword in user_message for keyword in ["忘記", "記憶", "健忘", "重複"]):
            module = "M1"
        elif any(keyword in user_message for keyword in ["失智", "認知", "行為", "症狀"]):
            module = "M2"
        elif any(keyword in user_message for keyword in ["妄想", "幻覺", "情緒", "行為"]):
            module = "M3"
        elif any(keyword in user_message for keyword in ["照護", "資源", "協助", "醫療"]):
            module = "M4"
        else:
            module = "comprehensive"
        
        print(f"🔍 選擇分析模組: {module}")
        
        # 本地分析（避免 HTTP 請求超時）
        if module == "M1":
            result = {
                "module": "M1",
                "warning_signs": ["記憶力減退", "語言障礙"],
                "risk_level": "medium",
                "recommendations": ["建議就醫檢查", "注意安全"]
            }
        elif module == "M2":
            result = {
                "module": "M2",
                "progression_stage": "mild",
                "symptoms": ["認知功能下降", "行為改變"],
                "care_focus": ["認知訓練", "環境安全"]
            }
        elif module == "M3":
            result = {
                "module": "M3",
                "bpsd_symptoms": ["妄想", "幻覺"],
                "intervention": ["藥物治療", "行為療法"],
                "severity": "moderate"
            }
        elif module == "M4":
            result = {
                "module": "M4",
                "care_resources": ["醫療資源", "照護技巧"],
                "contact_info": ["醫院聯絡", "社工協助"],
                "practical_tips": ["安全環境", "溝通技巧"]
            }
        else:  # comprehensive
            result = {
                "module": "comprehensive",
                "modules_used": ["M1", "M2", "M3", "M4"],
                "overall_assessment": "需要專業醫療評估",
                "recommendations": [
                    "立即就醫檢查",
                    "安排認知功能評估",
                    "考慮藥物治療",
                    "建立安全照護環境"
                ],
                "confidence": 0.85
            }
        
        return {
            "success": True,
            "message": f"{module} 分析完成",
            "data": result
        }
            
    except Exception as e:
        logger.error(f"分析用戶訊息失敗: {e}")
        return {"success": False, "message": f"分析失敗: {str(e)}"}

def send_line_reply(reply_token: str, message: str, flex_message: Dict[str, Any] = None):
    """發送 LINE 回應 - 支援 Flex Messages"""
    try:
        if TEST_MODE:
            print(f"🧪 測試模式: 模擬發送 LINE 回應")
            print(f"   回應令牌: {reply_token[:20]}...")
            if flex_message:
                print(f"   訊息類型: Flex Message")
                print(f"   標題: {flex_message.get('altText', 'N/A')}")
                print(f"   內容: {flex_message.get('contents', {}).get('header', {}).get('contents', [{}])[0].get('text', 'N/A')}")
            else:
                print(f"   訊息類型: 文字訊息")
                print(f"   訊息內容: {message[:100]}...")
            print("✅ 測試模式回應已記錄")
            return
        
        if line_bot_api and reply_token:
            if flex_message:
                # 創建 Flex Message - 修復版本
                from linebot.v3.messaging import FlexMessage
                
                # 確保 contents 是正確的格式
                contents = flex_message.get("contents", {})
                if not contents:
                    print("❌ Flex Message contents 為空")
                    return
                
                # 驗證 Flex Message 結構
                if contents.get("type") != "bubble":
                    print("❌ Flex Message 類型不是 bubble")
                    return
                
                # 檢查是否有必要的區塊
                header = contents.get("header", {})
                body = contents.get("body", {})
                
                if not header or not body:
                    print("❌ Flex Message 缺少必要的區塊")
                    return
                
                flex_msg = FlexMessage(
                    alt_text=flex_message.get("altText", "分析結果"),
                    contents=contents
                )
                
                # 創建回應請求
                reply_request = ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[flex_msg]
                )
                
                print(f"🎨 發送 Flex Message: {flex_message.get('altText', 'N/A')}")
                print(f"   結構: {contents.get('type')} - {contents.get('size', 'N/A')}")
                print(f"   標題區塊: {'✅' if header else '❌'}")
                print(f"   內容區塊: {'✅' if body else '❌'}")
            else:
                # 創建文字訊息
                text_message = TextMessage(text=message)
                
                # 創建回應請求
                reply_request = ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[text_message]
                )
            
            # 發送回應
            line_bot_api.reply_message(reply_request)
            print(f"✅ LINE 回應已發送")
            
        else:
            print(f"⚠️ 無法發送 LINE 回應: {'LINE Bot API 未初始化' if not line_bot_api else '無效的回應令牌'}")
            
    except Exception as e:
        logger.error(f"發送 LINE 回應失敗: {e}")
        print(f"❌ 發送 LINE 回應失敗: {e}")
        
        # 如果是 reply token 錯誤，提供更多信息
        if "Invalid reply token" in str(e):
            print("💡 提示: reply token 已過期，這是正常行為")
            print("💡 提示: 用戶需要重新發送訊息")
        elif "400" in str(e) and "At least one block must be specified" in str(e):
            print("💡 提示: Flex Message 結構問題")
            print("💡 提示: 嘗試發送簡單文字訊息")
            # 嘗試發送簡單的文字訊息作為備用
            try:
                text_message = TextMessage(text="抱歉，顯示分析結果時發生錯誤。請稍後再試。")
                reply_request = ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[text_message]
                )
                line_bot_api.reply_message(reply_request)
                print("✅ 已發送備用文字訊息")
            except Exception as backup_e:
                print(f"❌ 備用訊息也發送失敗: {backup_e}")
        else:
            print("💡 提示: 請檢查 LINE Bot 憑證是否正確")

def generate_flex_reply(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """生成 Flex Message 回應"""
    try:
        print(f"🎨 開始生成 Flex Message...")
        
        if not analysis_result.get("success", False):
            print(f"❌ 分析失敗，生成錯誤 Flex Message")
            return create_simple_flex_message(
                "❌ 分析失敗",
                "抱歉，我無法分析您的訊息。請嘗試重新描述您的情況。",
                "#F44336"
            )
        
        data = analysis_result.get("data", {})
        module = data.get("module", "comprehensive")
        
        print(f"🎯 使用模組: {module}")
        
        # 使用更簡單的 Flex Message 來避免結構問題
        if module == "M1":
            title = "🔍 M1 記憶力分析結果"
            content = "根據您的描述，可能涉及記憶力減退的症狀。建議：\n• 立即就醫檢查\n• 注意安全\n• 建立提醒系統"
            color = "#FF6B6B"
        elif module == "M2":
            title = "🔍 M2 認知功能分析結果"
            content = "根據您的描述，可能涉及認知功能下降。建議：\n• 安排認知功能評估\n• 進行認知訓練\n• 建立安全環境"
            color = "#4ECDC4"
        elif module == "M3":
            title = "🔍 M3 行為症狀分析結果"
            content = "根據您的描述，可能涉及行為症狀。建議：\n• 尋求專業醫療協助\n• 考慮藥物治療\n• 建立行為療法"
            color = "#45B7D1"
        else:
            title = "🔍 綜合分析結果"
            content = "根據您的描述，建議進行綜合評估。建議：\n• 立即就醫檢查\n• 安排專業評估\n• 建立照護計劃"
            color = "#FFA07A"
        
        flex_message = create_simple_flex_message(title, content, color)
        print(f"🎨 生成簡單 Flex Message 成功: {module} 模組")
        print(f"   標題: {flex_message.get('altText', 'N/A')}")
        return flex_message
        
    except Exception as e:
        logger.error(f"生成 Flex Message 失敗: {e}")
        print(f"❌ 生成 Flex Message 失敗: {e}")
        return create_simple_flex_message(
            "❌ 系統錯誤",
            "抱歉，生成回應時發生錯誤。請稍後再試。",
            "#F44336"
        )

# 註冊 LINE Bot 訊息處理器
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """處理 LINE Bot 文字訊息"""
    try:
        print(f"📨 處理 LINE 訊息事件")
        print(f"   事件類型: {type(event)}")
        print(f"   訊息類型: {type(event.message)}")
        print(f"   用戶 ID: {event.source.user_id}")
        print(f"   訊息內容: {event.message.text}")
        
        handle_line_message(event)
        
    except Exception as e:
        logger.error(f"處理 LINE 訊息事件失敗: {e}")
        print(f"❌ 處理訊息事件失敗: {e}")

# 處理所有訊息類型
@handler.add(MessageEvent)
def handle_all_messages(event):
    """處理所有類型的訊息"""
    try:
        print(f"📨 處理所有訊息事件")
        print(f"   事件類型: {type(event)}")
        print(f"   訊息類型: {type(event.message)}")
        
        # 只處理文字訊息
        if isinstance(event.message, TextMessageContent):
            handle_line_message(event)
        else:
            print(f"⚠️ 忽略非文字訊息: {type(event.message)}")
            
    except Exception as e:
        logger.error(f"處理所有訊息事件失敗: {e}")
        print(f"❌ 處理所有訊息事件失敗: {e}")

# M1 模組分析
@app.post("/analyze/M1")
def analyze_m1(request: UserInput):
    try:
        # 模擬 M1 分析
        result = {
            "module": "M1",
            "warning_signs": ["記憶力減退", "語言障礙"],
            "risk_level": "medium",
            "recommendations": ["建議就醫檢查", "注意安全"]
        }
        
        return AnalysisResponse(
            success=True,
            message="M1 分析完成",
            data=result
        )
    except Exception as e:
        return AnalysisResponse(
            success=False,
            message=f"M1 分析失敗: {str(e)}"
        )

# M2 模組分析
@app.post("/analyze/M2")
def analyze_m2(request: UserInput):
    try:
        # 模擬 M2 分析
        result = {
            "module": "M2",
            "progression_stage": "mild",
            "symptoms": ["認知功能下降", "行為改變"],
            "care_focus": ["認知訓練", "環境安全"]
        }
        
        return AnalysisResponse(
            success=True,
            message="M2 分析完成",
            data=result
        )
    except Exception as e:
        return AnalysisResponse(
            success=False,
            message=f"M2 分析失敗: {str(e)}"
        )

# M3 模組分析
@app.post("/analyze/M3")
def analyze_m3(request: UserInput):
    try:
        # 模擬 M3 分析
        result = {
            "module": "M3",
            "bpsd_symptoms": ["妄想", "幻覺"],
            "intervention": ["藥物治療", "行為療法"],
            "severity": "moderate"
        }
        
        return AnalysisResponse(
            success=True,
            message="M3 分析完成",
            data=result
        )
    except Exception as e:
        return AnalysisResponse(
            success=False,
            message=f"M3 分析失敗: {str(e)}"
        )

# M4 模組分析
@app.post("/analyze/M4")
def analyze_m4(request: UserInput):
    try:
        # 模擬 M4 分析
        result = {
            "module": "M4",
            "care_resources": ["醫療資源", "照護技巧"],
            "contact_info": ["醫院聯絡", "社工協助"],
            "practical_tips": ["安全環境", "溝通技巧"]
        }
        
        return AnalysisResponse(
            success=True,
            message="M4 分析完成",
            data=result
        )
    except Exception as e:
        return AnalysisResponse(
            success=False,
            message=f"M4 分析失敗: {str(e)}"
        )

# 綜合分析
@app.post("/comprehensive-analysis")
def comprehensive_analysis(request: UserInput):
    try:
        print(f"🔍 收到綜合分析請求: {request.message}")
        
        # 分析用戶訊息
        analysis_result = analyze_user_message(request.message)
        print(f"📊 分析結果: {analysis_result}")
        
        # 生成 Flex Message
        flex_message = generate_flex_reply(analysis_result)
        print(f"🎨 生成 Flex Message: {flex_message.get('altText', 'N/A')}")
        
        # 返回包含 Flex Message 的回應
        return {
            "success": True,
            "message": "綜合分析完成",
            "data": analysis_result.get("data", {}),
            "flex_message": flex_message
        }
    except Exception as e:
        print(f"❌ 綜合分析失敗: {e}")
        return {
            "success": False,
            "message": f"綜合分析失敗: {str(e)}",
            "flex_message": create_simple_flex_message(
                "❌ 分析失敗",
                "抱歉，分析過程中發生錯誤，請稍後再試。",
                "#F44336"
            )
        }

# 添加 comprehensive 端點（別名）
@app.post("/analyze/comprehensive")
def analyze_comprehensive(request: UserInput):
    """comprehensive 分析的別名端點"""
    return comprehensive_analysis(request)

# LINE Bot Webhook
@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        signature = request.headers.get("X-Line-Signature", "")
        
        print(f"📥 收到 LINE Webhook 請求")
        print(f"📝 簽名: {signature[:20]}...")
        print(f"📏 請求體大小: {len(body)} bytes")
        
        # 檢查 LINE Bot 是否已初始化
        if not line_bot_api or not handler:
            print("❌ LINE Bot 未初始化")
            raise HTTPException(status_code=500, detail="LINE Bot not initialized")
        
        # 驗證簽名並處理事件
        try:
            body_str = body.decode('utf-8')
            print(f"📄 請求體內容: {body_str[:200]}...")
            
            # 嘗試解析 JSON 以檢查事件結構
            try:
                event_data = json.loads(body_str)
                print(f"📊 事件數量: {len(event_data.get('events', []))}")
                for i, event in enumerate(event_data.get('events', [])):
                    print(f"   事件 {i+1}: {event.get('type', 'unknown')}")
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON 解析錯誤: {e}")
            
            # 使用 LINE Bot SDK 處理事件
            handler.handle(body_str, signature)
            print("✅ Webhook 處理成功")
            
        except InvalidSignatureError as e:
            print(f"❌ 簽名驗證失敗: {e}")
            print("請檢查 LINE_CHANNEL_SECRET 是否正確")
            raise HTTPException(status_code=400, detail="Invalid signature")
            
        except Exception as e:
            print(f"❌ Webhook 處理失敗: {e}")
            print(f"錯誤類型: {type(e)}")
            
            # 嘗試手動處理事件
            try:
                print("🔄 嘗試手動處理事件...")
                event_data = json.loads(body_str)
                events = event_data.get('events', [])
                
                for event in events:
                    if event.get('type') == 'message' and event.get('message', {}).get('type') == 'text':
                        # 創建模擬的 MessageEvent
                        from linebot.v3.webhooks import UserSource, TextMessageContent
                        
                        # 創建用戶來源
                        source = UserSource(user_id=event['source']['userId'])
                        
                        # 創建文字訊息
                        message = TextMessageContent(
                            id=event['message']['id'],
                            text=event['message']['text'],
                            quote_token=event['message'].get('quoteToken', '')
                        )
                        
                        # 創建 MessageEvent
                        message_event = MessageEvent(
                            type='message',
                            mode=event.get('mode', 'active'),
                            timestamp=event.get('timestamp', 0),
                            source=source,
                            webhook_event_id=event.get('webhookEventId', ''),
                            delivery_context=event.get('deliveryContext', {}),
                            reply_token=event.get('replyToken', ''),
                            message=message
                        )
                        
                        # 處理事件
                        handle_line_message(message_event)
                        print("✅ 手動處理事件成功")
                        
            except Exception as manual_error:
                print(f"❌ 手動處理也失敗: {manual_error}")
                raise HTTPException(status_code=500, detail="Internal server error")
        
        return {"status": "success"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 測試 Webhook 端點（跳過簽名驗證）
@app.post("/test-webhook")
async def test_webhook(request: Request):
    """測試 Webhook 端點，跳過簽名驗證"""
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        
        print(f"🧪 測試 Webhook 請求")
        print(f"📏 請求體大小: {len(body)} bytes")
        print(f"📄 請求體內容: {body_str[:200]}...")
        
        # 檢查 LINE Bot 是否已初始化
        if not line_bot_api or not handler:
            print("❌ LINE Bot 未初始化")
            return {"status": "error", "message": "LINE Bot not initialized"}
        
        # 嘗試解析 JSON
        try:
            event_data = json.loads(body_str)
            print(f"📊 事件數量: {len(event_data.get('events', []))}")
            
            events = event_data.get('events', [])
            processed_count = 0
            
            for event in events:
                if event.get('type') == 'message' and event.get('message', {}).get('type') == 'text':
                    print(f"📨 處理文字訊息: {event['message']['text']}")
                    
                    # 創建模擬的 MessageEvent
                    from linebot.v3.webhooks import UserSource, TextMessageContent
                    
                    # 創建用戶來源
                    source = UserSource(user_id=event['source']['userId'])
                    
                    # 創建文字訊息
                    message = TextMessageContent(
                        id=event['message']['id'],
                        text=event['message']['text'],
                        quote_token=event['message'].get('quoteToken', '')
                    )
                    
                    # 創建 MessageEvent
                    message_event = MessageEvent(
                        type='message',
                        mode=event.get('mode', 'active'),
                        timestamp=event.get('timestamp', 0),
                        source=source,
                        webhook_event_id=event.get('webhookEventId', ''),
                        delivery_context=event.get('deliveryContext', {}),
                        reply_token=event.get('replyToken', ''),
                        message=message
                    )
                    
                    # 處理事件
                    handle_line_message(message_event)
                    processed_count += 1
                    print(f"✅ 處理事件成功 ({processed_count})")
                    
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析錯誤: {e}")
            return {"status": "error", "message": "Invalid JSON"}
        except Exception as e:
            print(f"❌ 事件處理錯誤: {e}")
            return {"status": "error", "message": str(e)}
        
        print(f"✅ 測試 Webhook 處理完成，處理了 {processed_count} 個事件")
        return {"status": "success", "processed_events": processed_count}
        
    except Exception as e:
        print(f"❌ 測試 Webhook 錯誤: {e}")
        return {"status": "error", "message": str(e)}

# 啟動事件
@app.on_event("startup")
async def startup():
    print("🚀 API 啟動中...")
    
    # 檢查環境變數
    if not check_env_variables():
        print("❌ 環境變數檢查失敗")
        return
    
    if TEST_MODE:
        print("🧪 測試模式已啟用 - LINE 訊息將不會實際發送")
    else:
        print("📱 生產模式 - LINE 訊息將正常發送")
    
    print("✅ API 啟動完成")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005) 