#!/usr/bin/env python3
"""
Dockerized LINE Bot Webhook Service with Non-linear Navigation
Enhanced for microservices architecture
"""

import os
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextSendMessage,
    FlexSendMessage,
    TextMessage,
    FollowEvent,
    UnfollowEvent,
    PostbackEvent,
    MessageEvent,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
XAI_API_URL = os.getenv("XAI_API_URL", "http://xai-wrapper:8005")
RAG_API_URL = os.getenv("RAG_API_URL", "http://xai-wrapper:8005")
EXTERNAL_URL = os.getenv("EXTERNAL_URL", "http://localhost:8081")
LIFF_ID = os.getenv("LIFF_ID")
LIFF_PLACEHOLDER_URL = os.getenv("LIFF_PLACEHOLDER_URL")

# Initialize LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Create FastAPI app
app = FastAPI(
    title="LINE Bot Webhook Service - Non-linear Navigation",
    description=("Microservices-based LINE Bot with non-linear module navigation"),
    version="3.0.0",
)

# User session management
user_sessions = {}

# 移除複雜的 M1 模組導入
# from visualization.modules.m1_visualization import M1VisualizationProcessor

# 移除 M1 處理器初始化
# m1_processor = M1VisualizationProcessor()


# 添加簡單的 M1 功能
def _get_liff_url() -> str:
    if LIFF_ID:
        return f"line://app/{LIFF_ID}"
    if LIFF_PLACEHOLDER_URL:
        return LIFF_PLACEHOLDER_URL
    # 最低保護：回退到 EXTERNAL_URL（若非 https 僅作占位）
    return EXTERNAL_URL


def create_simple_m1_response(
    user_text: str, full_text_id: Optional[str] = None
) -> FlexSendMessage:
    """創建簡單的 M1 回應"""

    # 簡單的症狀檢測
    symptoms = {}
    if "忘記" in user_text or "記憶" in user_text:
        symptoms["記憶力"] = 3
    if "迷路" in user_text or "方向" in user_text:
        symptoms["定向力"] = 4
    if "說話" in user_text or "語言" in user_text:
        symptoms["語言能力"] = 2

    # 簡單的風險評估
    risk_factors = {}
    if "年紀" in user_text or "年齡" in user_text:
        risk_factors["年齡"] = 0.7

    # 計算警訊等級
    warning_level = 1
    if symptoms:
        avg_severity = sum(symptoms.values()) / len(symptoms)
        if avg_severity > 3:
            warning_level = 4
        elif avg_severity > 2:
            warning_level = 3
        else:
            warning_level = 2

    # 基礎 Confidence（P0：規則/預設）
    # 規則：以症狀數與平均強度粗估；否則預設 70%
    if symptoms:
        confidence_val = min(95, int(60 + 10 * len(symptoms)))
    else:
        confidence_val = 70

    # 生成警訊訊息
    warning_messages = {
        1: "目前症狀輕微，建議定期觀察",
        2: "需要關注症狀變化，建議諮詢醫生",
        3: "症狀明顯，建議盡快就醫檢查",
        4: "症狀嚴重，建議立即就醫",
        5: "症狀非常嚴重，建議緊急就醫",
    }
    warning_message = warning_messages.get(warning_level, warning_messages[1])

    # 創建簡單的 Flex Message
    contents = []

    # 警訊指示器 + 信心度
    warning_colors = {
        1: "#4CAF50",
        2: "#8BC34A",
        3: "#FFC107",
        4: "#FF9800",
        5: "#F44336",
    }
    warning_icons = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🟠", 5: "🔴"}

    contents.append(
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "md",
            "backgroundColor": warning_colors.get(warning_level, "#4CAF50"),
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "contents": [
                {
                    "type": "text",
                    "text": warning_icons.get(warning_level, "🟢"),
                    "size": "lg",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "flex": 1,
                    "contents": [
                        {
                            "type": "text",
                            "text": f"警訊等級 {warning_level}",
                            "weight": "bold",
                            "color": "#FFFFFF",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": warning_message,
                            "color": "#FFFFFF",
                            "size": "xs",
                            "wrap": True,
                        },
                        {
                            "type": "text",
                            "text": f"AI 信心度：{confidence_val}%",
                            "color": "#E6F4EA",
                            "size": "xs",
                            "margin": "sm",
                        },
                    ],
                },
            ],
        }
    )

    # 症狀列表
    if symptoms:
        contents.append({"type": "separator", "margin": "lg"})
        symptoms_box = {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "檢測到的症狀",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#333333",
                }
            ],
        }

        for symptom, severity in symptoms.items():
            severity_text = (
                "輕微" if severity <= 2 else "中等" if severity <= 3 else "嚴重"
            )
            symptoms_box["contents"].append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": symptom,
                            "size": "sm",
                            "color": "#333333",
                            "flex": 1,
                        },
                        {
                            "type": "text",
                            "text": f"{severity_text} ({severity}/5)",
                            "size": "sm",
                            "color": "#666666",
                        },
                    ],
                }
            )

        contents.append(symptoms_box)

    # 行動列（符合 P0：深入分析 / 看原文 / 開啟 LIFF）
    contents.append({"type": "separator", "margin": "lg"})
    contents.append(
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "margin": "lg",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "🔍 深入分析",
                        "data": "view=frame36&page=1",
                        "displayText": "深入分析",
                    },
                    "style": "primary",
                    "color": "#1DB446",
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "📝 看原文",
                        "data": (f"view=original&ref={full_text_id or 'latest'}"),
                        "displayText": "看原文",
                    },
                    "style": "secondary",
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "🔗 開啟 LIFF",
                        "uri": _get_liff_url(),
                    },
                    "style": "secondary",
                },
            ],
        }
    )

    return FlexSendMessage(
        alt_text="失智症警訊徵兆檢測結果",
        contents={
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": contents,
            },
        },
    )


class NonLinearNavigationEngine:
    """Enhanced navigation engine for non-linear module access"""

    def __init__(self):
        self.modules = {
            "M1": {
                "name": "警訊徵兆分析",
                "description": "分析失智症早期警訊徵兆",
                "keywords": ["記憶", "忘記", "迷路", "語言", "判斷"],
                "color": "#FF6B6B",
            },
            "M2": {
                "name": "病程進展評估",
                "description": "評估失智症病程進展階段",
                "keywords": ["早期", "中期", "晚期", "進展", "階段"],
                "color": "#4ECDC4",
            },
            "M3": {
                "name": "行為症狀分析",
                "description": "分析行為和心理症狀",
                "keywords": ["妄想", "幻覺", "激動", "憂鬱", "焦慮"],
                "color": "#45B7D1",
            },
            "M4": {
                "name": "照護資源導航",
                "description": "推薦適合的照護資源",
                "keywords": ["醫生", "醫院", "照護", "資源", "補助"],
                "color": "#96CEB4",
            },
        }
        self.navigation_history = {}

    def detect_user_intent(self, text: str, user_id: str) -> Dict[str, Any]:
        """Detect user intent and suggest relevant modules"""
        detected_modules = []
        confidence_scores = {}

        for module_id, module_info in self.modules.items():
            score = 0
            for keyword in module_info["keywords"]:
                if keyword in text:
                    score += 1

            if score > 0:
                confidence = score / len(module_info["keywords"])
                detected_modules.append(module_id)
                confidence_scores[module_id] = confidence

        return {
            "detected_modules": detected_modules,
            "confidence_scores": confidence_scores,
            "suggested_modules": self._get_suggested_modules(user_id, detected_modules),
        }

    def _get_suggested_modules(
        self, user_id: str, detected_modules: List[str]
    ) -> List[str]:
        """Get suggested modules based on history and current detection"""
        if not detected_modules:
            return ["M1", "M4"]

        # Suggest related modules
        related_modules = {
            "M1": ["M2", "M4"],
            "M2": ["M1", "M3"],
            "M3": ["M2", "M4"],
            "M4": ["M1", "M3"],
        }

        suggestions = []
        for module in detected_modules:
            if module in related_modules:
                suggestions.extend(related_modules[module])

        return list(set(suggestions))[:2]


# Initialize navigation engine
navigation_engine = NonLinearNavigationEngine()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LINE Bot Webhook Service - Non-linear Navigation",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "external_url": EXTERNAL_URL,
        "webhook_url": f"{EXTERNAL_URL}/webhook",
        "services": {
            "xai_analysis": XAI_API_URL,
            "rag_service": RAG_API_URL,
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        xai_response = requests.get(f"{XAI_API_URL}/health", timeout=5)
        rag_response = requests.get(f"{RAG_API_URL}/health", timeout=5)

        return {
            "status": "healthy",
            "service": "line-bot",
            "version": "3.0.0",
            "xai_service": (
                "healthy" if xai_response.status_code == 200 else "unhealthy"
            ),
            "rag_service": (
                "healthy" if rag_response.status_code == 200 else "unhealthy"
            ),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


@app.get("/webhook")
async def webhook_get():
    """Handle GET requests to webhook endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "message": "LINE Bot Webhook is running",
            "status": "active",
            "note": "This endpoint only accepts POST requests from LINE",
            "webhook_url": "POST /webhook",
            "health_check": "GET /health",
            "bot_info": "GET /info",
        },
    )


@app.post("/webhook")
async def webhook(request: Request):
    """LINE Bot webhook endpoint"""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), signature)
        logger.info("✅ Webhook processed successfully")
    except InvalidSignatureError as e:
        logger.error(f"❌ Invalid LINE signature: {e}")
        # Return 200 OK even for invalid signature to prevent LINE retries
        return JSONResponse(
            content={
                "status": "ok",
                "note": "Invalid signature ignored",
            }
        )
    except Exception as e:
        logger.error(f"❌ Webhook processing error: {e}")
        # Return 200 OK to prevent LINE from retrying
        return JSONResponse(content={"status": "ok", "note": "Error processed"})

    return JSONResponse(content={"status": "ok"})


@app.get("/webhook-url")
async def get_webhook_url():
    """Get current webhook URL for LINE Developer Console"""
    return {
        "webhook_url": f"{EXTERNAL_URL}/webhook",
        "external_url": EXTERNAL_URL,
        "note": "Update this URL in LINE Developer Console",
    }


def create_error_flex_message(error_msg: str) -> FlexSendMessage:
    """Create error flex message"""
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "❌ 系統暫時無法使用",
                    "weight": "bold",
                    "color": "#FF0000",
                    "size": "lg",
                },
                {
                    "type": "text",
                    "text": error_msg,
                    "color": "#666666",
                    "size": "sm",
                    "margin": "md",
                },
            ],
        },
    }
    return FlexSendMessage(alt_text="系統錯誤", contents=flex_message)


async def call_xai_analysis(text: str, user_id: str) -> Dict[str, Any]:
    """Call XAI analysis service"""
    try:
        response = requests.post(
            f"{XAI_API_URL}/comprehensive-analysis",
            json={
                "text": text,
                "user_id": user_id,
                "include_visualization": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"XAI analysis failed: {e}")
        return {"success": False, "error": str(e)}


async def call_rag_service(query: str) -> Dict[str, Any]:
    """Call RAG service"""
    try:
        response = requests.post(
            f"{RAG_API_URL}/search",
            json={
                "query": query,
                "top_k": 3,
                "threshold": 0.5,
                "use_gpu": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"RAG search failed: {e}")
        return {"success": False, "error": str(e)}


def call_xai_analysis_sync(text: str, user_id: str) -> Dict[str, Any]:
    """Call XAI analysis service (synchronous version)"""
    try:
        response = requests.post(
            f"{XAI_API_URL}/comprehensive-analysis",
            json={
                "text": text,
                "user_id": user_id,
                "include_visualization": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"XAI analysis failed: {e}")
        return {"success": False, "error": str(e)}


def call_rag_service_sync(query: str) -> Dict[str, Any]:
    """Call RAG service (synchronous version)"""
    try:
        response = requests.post(
            f"{RAG_API_URL}/search",
            json={
                "query": query,
                "top_k": 3,
                "threshold": 0.5,
                "use_gpu": True,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"RAG search failed: {e}")
        return {"success": False, "error": str(e)}


def create_analysis_flex_message(
    analysis_result: Dict[str, Any], user_text: str
) -> FlexSendMessage:
    """Create enhanced analysis flex message"""
    try:
        # modules_used 可用於未來顯示（目前未使用）
        _ = analysis_result.get("modules_used", [])
        confidence = analysis_result.get("confidence", 0)
        summary = analysis_result.get("summary", "")

        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 智能分析結果",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#1DB446",
                    },
                    {
                        "type": "text",
                        "text": (
                            f"您的描述：{user_text[:50]}"
                            f"{'...' if len(user_text) > 50 else ''}"
                        ),
                        "color": "#666666",
                        "size": "sm",
                        "margin": "md",
                    },
                    {
                        "type": "text",
                        "text": f"分析摘要：{summary}",
                        "color": "#333333",
                        "size": "sm",
                        "margin": "md",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"可信度：{confidence:.1%}",
                        "color": "#666666",
                        "size": "xs",
                        "margin": "md",
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "🔍 深入分析",
                            "data": "view=frame36&page=1",
                        },
                        "style": "primary",
                        "color": "#1DB446",
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "📚 知識檢索",
                            "data": "knowledge_search",
                        },
                        "style": "secondary",
                        "margin": "sm",
                    },
                ],
            },
        }

        return FlexSendMessage(alt_text="智能分析結果", contents=flex_message)

    except Exception as e:
        logger.error(f"Failed to create analysis flex message: {e}")
        return create_error_flex_message("分析結果顯示失敗")


def create_navigation_flex_message(
    user_id: str, detected_intent: Dict[str, Any]
) -> FlexSendMessage:
    """Create navigation flex message for non-linear module access"""
    try:
        detected_modules = detected_intent.get("detected_modules", [])
        suggested_modules = detected_intent.get("suggested_modules", [])

        action_buttons = []
        for module_id in detected_modules + suggested_modules:
            module_info = navigation_engine.modules.get(module_id, {})
            action_buttons.append(
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": module_info.get("name", module_id),
                        "data": f"analyze_{module_id}",
                    },
                    "style": (
                        "primary" if module_id in detected_modules else "secondary"
                    ),
                    "color": module_info.get("color", "#666666"),
                    "margin": "xs",
                }
            )

        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧭 智能導航",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#1DB446",
                    },
                    {
                        "type": "text",
                        "text": "根據您的描述，我們為您推薦以下分析模組：",
                        "color": "#666666",
                        "size": "sm",
                        "margin": "md",
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": action_buttons,
            },
        }

        return FlexSendMessage(alt_text="智能導航", contents=flex_message)

    except Exception as e:
        logger.error(f"Failed to create navigation flex message: {e}")
        return create_error_flex_message("導航功能暫時無法使用")


def create_welcome_flex_message() -> FlexSendMessage:
    """Create welcome flex message with non-linear navigation"""
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 失智症照護智能助手",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#1DB446",
                },
                {
                    "type": "text",
                    "text": "歡迎使用！我是您的失智症照護智能助手，可以為您提供：",
                    "color": "#666666",
                    "size": "sm",
                    "margin": "md",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔍 警訊徵兆分析",
                            "color": "#FF6B6B",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": "📊 病程進展評估",
                            "color": "#4ECDC4",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": "🧠 行為症狀分析",
                            "color": "#45B7D1",
                            "size": "sm",
                        },
                        {
                            "type": "text",
                            "text": "🏥 照護資源導航",
                            "color": "#96CEB4",
                            "size": "sm",
                        },
                    ],
                    "margin": "md",
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "開始分析",
                        "data": "start_analysis",
                    },
                    "style": "primary",
                    "color": "#1DB446",
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "知識檢索",
                        "data": "knowledge_search",
                    },
                    "style": "secondary",
                    "margin": "sm",
                },
            ],
        },
    }

    return FlexSendMessage(alt_text="歡迎使用失智症照護智能助手", contents=flex_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle text messages with non-linear navigation"""
    try:
        user_id = event.source.user_id
        user_text = event.message.text

        logger.info(f"📝 Received message from {user_id}: {user_text[:50]}...")

        # 儲存原文供「看原文」使用
        full_text_id = str(int(datetime.now().timestamp()))
        user_sessions[user_id] = {
            "full_text_id": full_text_id,
            "full_text": user_text,
            "ts": datetime.now().isoformat(),
        }

        # Detect user intent
        intent = navigation_engine.detect_user_intent(user_text, user_id)

        # If specific modules detected, perform analysis
        if intent["detected_modules"]:
            # 檢查是否為 M1 相關查詢
            if "M1" in intent["detected_modules"] or any(
                keyword in user_text
                for keyword in ["忘記", "記憶", "健忘", "失憶", "迷路", "混淆"]
            ):
                # 使用簡單的 M1 處理器
                flex_message = create_simple_m1_response(
                    user_text, full_text_id=full_text_id
                )
                line_bot_api.reply_message(event.reply_token, flex_message)
                logger.info("✅ M1 視覺化分析完成")
                return

            # Perform comprehensive analysis (原有邏輯)
            analysis_result = call_xai_analysis_sync(user_text, user_id)

            if analysis_result.get("success"):
                flex_message = create_analysis_flex_message(analysis_result, user_text)
                line_bot_api.reply_message(event.reply_token, flex_message)
                logger.info(f"✅ Analysis completed for {user_id}")
            else:
                # 如果 XAI 服務失敗，嘗試使用簡單的 M1 處理器
                flex_message = create_simple_m1_response(
                    user_text, full_text_id=full_text_id
                )
                line_bot_api.reply_message(event.reply_token, flex_message)
                logger.info("✅ M1 視覺化分析完成（XAI 服務備用）")
        else:
            # Show navigation menu
            flex_message = create_navigation_flex_message(user_id, intent)
            line_bot_api.reply_message(event.reply_token, flex_message)
            logger.info(f"✅ Navigation menu sent to {user_id}")

    except Exception as e:
        logger.error(f"❌ Text message handling failed: {e}")
        # 發生錯誤時，嘗試使用簡單的 M1 處理器作為備用
        try:
            # 注意：此處 user_text 定義於 try 作用域之上
            flex_message = create_simple_m1_response(user_text)
            line_bot_api.reply_message(event.reply_token, flex_message)
            logger.info("✅ M1 視覺化分析完成（錯誤處理備用）")
        except Exception as backup_error:
            logger.error(f"❌ M1 備用處理也失敗: {backup_error}")
            # 發送簡單的錯誤訊息
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，處理您的訊息時遇到問題。請稍後再試。"),
            )


@handler.add(PostbackEvent)
def handle_postback(event):
    """Handle postback events for non-linear navigation"""
    try:
        user_id = event.source.user_id
        postback_data = event.postback.data

        logger.info(f"🔘 Received postback from {user_id}: {postback_data}")

        if postback_data == "start_analysis":
            flex_message = create_navigation_flex_message(
                user_id,
                {"detected_modules": [], "suggested_modules": ["M1", "M4"]},
            )
            line_bot_api.reply_message(event.reply_token, flex_message)

        elif postback_data.startswith("analyze_"):
            module_id = postback_data.replace("analyze_", "")

            # Perform single module analysis
            analysis_result = call_xai_analysis_sync(
                f"請分析{module_id}相關內容", user_id
            )

            if analysis_result.get("success"):
                flex_message = create_analysis_flex_message(
                    analysis_result, f"{module_id}分析"
                )
                line_bot_api.reply_message(event.reply_token, flex_message)
            else:
                error_message = create_error_flex_message("模組分析失敗")
                line_bot_api.reply_message(event.reply_token, error_message)

        elif postback_data == "knowledge_search":
            # Perform knowledge search
            rag_result = call_rag_service_sync("失智症照護知識")

            if rag_result.get("success") and rag_result.get("results"):
                knowledge_text = "📚 相關知識：\n\n"
                for result in rag_result["results"][:3]:
                    snippet = result["content"][:100]
                    knowledge_text += f"• {result['title']}: {snippet}...\n\n"

                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=knowledge_text)
                )
            else:
                error_message = create_error_flex_message("知識檢索失敗")
                line_bot_api.reply_message(event.reply_token, error_message)

        elif postback_data.startswith("view=original"):
            # 回覆完整原文（若存在）
            session = user_sessions.get(user_id, {})
            full_text = session.get("full_text") or "（找不到原始訊息內容）"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=full_text)
            )

        elif postback_data.startswith("view=frame36"):
            # 預留：回覆 Frame36 Page1 入口（P1 具體實作）
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="已切換至深入分析（XAI 報告）— 即將提供詳細內容"),
            )

        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="請選擇您需要的功能")
            )

    except Exception as e:
        logger.error(f"❌ Postback handling failed: {e}")
        error_message = create_error_flex_message("功能處理失敗")
        line_bot_api.reply_message(event.reply_token, error_message)


@handler.add(FollowEvent)
def handle_follow(event):
    """Handle follow events"""
    try:
        user_id = event.source.user_id
        logger.info(f"👋 New user followed: {user_id}")

        welcome_message = create_welcome_flex_message()
        line_bot_api.reply_message(event.reply_token, welcome_message)

    except Exception as e:
        logger.error(f"❌ Follow event handling failed: {e}")


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    """Handle unfollow events"""
    try:
        user_id = event.source.user_id
        logger.info(f"👋 User unfollowed: {user_id}")

        # Clean up user session
        if user_id in user_sessions:
            del user_sessions[user_id]

    except Exception as e:
        logger.error(f"❌ Unfollow event handling failed: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081)
