#!/usr/bin/env python3
"""
增強版 M1+M2+M3 整合 API
整合 Redis 快取和優化 Gemini API
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn

# 初始化 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# line-bot-sdk v3 imports
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage, FlexMessage

# 引入優化模組
try:
    from redis_cache_manager import RedisCacheManager, cache_result
    from optimized_gemini_client import OptimizedGeminiClient
except ImportError as e:
    print(f"⚠️  優化模組導入失敗: {e}")
    RedisCacheManager = None
    OptimizedGeminiClient = None

# 引入整合引擎
try:
    from m1_m2_m3_integrated_rag import M1M2M3IntegratedEngine
except ImportError:
    print("⚠️  整合引擎模組未找到")
    M1M2M3IntegratedEngine = None

# 初始化 LINE Bot v3
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

# FastAPI 應用
app = FastAPI()

# 全域引擎和優化組件
integrated_engine = None
cache_manager = None
optimized_gemini = None


# 檢查環境變數
def check_env_variables():
    """檢查環境變數"""
    print("🔍 檢查環境變數...")

    # 檢查 .env 檔案
    if not os.path.exists(".env"):
        print("❌ .env 檔案不存在")
        return False

    # 檢查關鍵環境變數
    env_vars = {
        "LINE_CHANNEL_ACCESS_TOKEN": os.getenv("LINE_CHANNEL_ACCESS_TOKEN"),
        "LINE_CHANNEL_SECRET": os.getenv("LINE_CHANNEL_SECRET"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    }

    for var_name, var_value in env_vars.items():
        if not var_value or var_value.startswith("your_actual_"):
            print(f"❌ {var_name} 未正確設置")
        else:
            print(f"✅ {var_name} 已設置")

    return True


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    logger.info("[DEBUG] handle_message 被呼叫")
    try:
        user_input = event.message.text
        user_id = event.source.user_id
        logger.info(f"[DEBUG] event.message.text: {user_input}")
        logger.info(f"[DEBUG] event.source.user_id: {user_id}")
        logger.info(f"📨 收到來自 {user_id} 的訊息: {user_input}")
        
        if integrated_engine:
            logger.info("[DEBUG] integrated_engine 可用，開始分析...")
            
            # 檢查快取
            cached_result = None
            if cache_manager:
                cached_result = cache_manager.get_cached_analysis(user_input)
                if cached_result:
                    logger.info("[DEBUG] 快取命中，使用快取結果")
                    result = cached_result
                else:
                    logger.info("[DEBUG] 快取未命中，進行新分析")
                    result = integrated_engine.analyze_comprehensive(user_input)
                    # 快取新結果
                    try:
                        cache_manager.cache_analysis_result(user_input, result)
                        logger.info("[DEBUG] 新分析結果已快取")
                    except Exception as cache_error:
                        logger.warning(f"[DEBUG] 快取失敗: {cache_error}")
            else:
                logger.info("[DEBUG] 無快取管理器，直接分析")
                result = integrated_engine.analyze_comprehensive(user_input)
            
            logger.info(f"[DEBUG] 分析結果類型: {type(result)}")
            
            # 完全安全地提取分析結果
            try:
                if hasattr(result, 'comprehensive_summary'):
                    summary = result.comprehensive_summary
                    logger.info("[DEBUG] 使用 result.comprehensive_summary")
                elif hasattr(result, '__dict__'):
                    if 'comprehensive_summary' in result.__dict__:
                        summary = result.__dict__['comprehensive_summary']
                        logger.info("[DEBUG] 使用 result.__dict__['comprehensive_summary']")
                    else:
                        summary = str(result)
                        logger.info("[DEBUG] 使用 str(result)")
                else:
                    summary = str(result)
                    logger.info("[DEBUG] 使用 str(result) 作為備用")
            except Exception as extract_error:
                logger.error(f"[DEBUG] 提取分析結果時發生錯誤: {extract_error}")
                summary = "分析完成，但無法提取詳細結果"
            
            logger.info(f"[DEBUG] 最終摘要: {summary}")
            logger.info("[DEBUG] 開始創建 Flex Message...")
            
            # 創建符合 LINE Bot API v3 格式的 Flex Message
            from linebot.v3.messaging.models import (
                FlexBubble,
                FlexBox,
                FlexText,
                FlexButton,
                MessageAction,
                FlexSeparator
            )
            
            # 創建 Flex Message 內容
            bubble = FlexBubble(
                size="kilo",
                header=FlexBox(
                    layout="vertical",
                    contents=[
                        FlexText(
                            text="🧠 失智症分析結果",
                            weight="bold",
                            size="lg",
                            color="#ffffff"
                        )
                    ],
                    background_color="#005073"
                ),
                body=FlexBox(
                    layout="vertical",
                    contents=[
                        FlexText(
                            text="分析完成",
                            size="md",
                            color="#005073",
                            wrap=True
                        ),
                        FlexText(
                            text=summary,
                            size="sm",
                            wrap=True,
                            margin="md"
                        )
                    ]
                ),
                footer=FlexBox(
                    layout="horizontal",
                    contents=[
                        FlexButton(
                            style="primary",
                            height="sm",
                            action=MessageAction(
                                label="更多資訊",
                                text="請提供更多詳細資訊"
                            ),
                            flex=1
                        )
                    ]
                )
            )
            
            flex_message = FlexMessage(
                alt_text="失智症分析結果",
                contents=bubble
            )
            
            logger.info("[DEBUG] Flex Message 創建完成，準備發送...")
            
            # 檢查 reply token
            if not event.reply_token:
                logger.error("[DEBUG] Reply token 為空")
                return
            
            # 檢查 reply token 是否為 "00000000000000000000000000000000"
            if event.reply_token == "00000000000000000000000000000000":
                logger.error("[DEBUG] Reply token 無效")
                return
            
            # 回覆 Flex Message（加入超時處理）
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[flex_message]
                    )
                )
                logger.info(f"✅ 已回覆用戶 {user_id} Flex Message")
            except Exception as api_error:
                logger.error(f"❌ LINE API 連線錯誤: {api_error}")
                # 如果 Flex Message 失敗，嘗試發送純文字
                try:
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=summary)]
                        )
                    )
                    logger.info(f"✅ 已回覆用戶 {user_id} 純文字訊息（備用方案）")
                except Exception as text_error:
                    logger.error(f"❌ 純文字回覆也失敗: {text_error}")
        else:
            response_text = "❌ 系統尚未初始化，請稍後再試。"
            # 回覆純文字訊息
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=response_text)]
                    )
                )
                logger.info(f"✅ 已回覆用戶 {user_id} 純文字訊息")
            except Exception as e:
                logger.error(f"❌ 系統訊息回覆失敗: {e}")
    except Exception as e:
        logger.error(f"❌ 訊息處理錯誤: {e}")
        import traceback
        logger.error(f"❌ 詳細錯誤: {traceback.format_exc()}")
        try:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="抱歉，處理您的訊息時發生錯誤。")]
                )
            )
        except Exception as e2:
            logger.error(f"❌ 回覆用戶時發生錯誤: {e2}")

@app.post("/webhook")
async def webhook(request: Request):
    logger.info("[DEBUG] /webhook endpoint 被呼叫")
    try:
        body = await request.body()
        signature = request.headers.get("X-Line-Signature")
        logger.info(f"[DEBUG] X-Line-Signature: {signature}")
        logger.info(f"[DEBUG] webhook body: {body[:200]}")
        if not signature:
            logger.error("[DEBUG] 缺少 X-Line-Signature")
            return {"error": "缺少 X-Line-Signature"}
        handler.handle(body.decode(), signature)
        logger.info("[DEBUG] handler.handle 已執行")
        return {"message": "ok"}
    except Exception as e:
        logger.error(f"❌ Webhook 處理錯誤: {e}")
        return {"error": str(e)}


@app.on_event("startup")
async def startup():
    global integrated_engine, cache_manager, optimized_gemini, line_bot_api, handler
    print("🚀 啟動增強版 M1+M2+M3 整合引擎...")

    # 檢查環境變數
    check_env_variables()

    api_key = os.getenv("GEMINI_API_KEY")

    # 初始化 LINE Bot
    if line_bot_api:
        print("✅ LINE Bot 初始化成功")
    else:
        print("⚠️  LINE Bot 模組未載入")

    # 初始化快取管理器
    if RedisCacheManager:
        cache_manager = RedisCacheManager()
        if cache_manager.is_available():
            print("✅ Redis 快取管理器初始化成功")
        else:
            print("⚠️  Redis 快取不可用，將使用記憶體快取")
    else:
        print("⚠️  Redis 快取管理器未載入")

    # 初始化優化 Gemini 客戶端
    if OptimizedGeminiClient:
        optimized_gemini = OptimizedGeminiClient(api_key)
        print("✅ 優化 Gemini 客戶端初始化成功")
    else:
        print("⚠️  優化 Gemini 客戶端未載入")

    # 初始化整合引擎
    if M1M2M3IntegratedEngine:
        integrated_engine = M1M2M3IntegratedEngine(api_key)
        print("✅ M1+M2+M3 整合引擎初始化成功")
    else:
        print("❌ 整合引擎無法載入")
        return

    print("✅ 增強版 M1+M2+M3 整合 API 啟動成功")


class UserInput(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {
        "message": "增強版 M1+M2+M3 整合 RAG API",
        "version": "4.0.0",
        "features": [
            "🚨 M1: 失智症十大警訊識別",
            "🏥 M2: 病程階段分析",
            "🧠 M3: BPSD 行為心理症狀分析",
            "🔍 智能語義檢索",
            "📊 多重信心度評估",
            "🎯 綜合分析報告",
            "⚡ Redis 快取優化",
            "💰 Gemini API 成本優化",
        ],
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "optimized_gemini": optimized_gemini is not None,
            "cache_stats": cache_manager.get_cache_stats() if cache_manager else None,
        },
        "total_chunks": len(integrated_engine.chunks) if integrated_engine else 0,
    }


@app.get("/health")
def health():
    if not integrated_engine:
        return {"status": "error", "message": "引擎未初始化"}

    # 統計模組分布
    m1_chunks = [
        c for c in integrated_engine.chunks if c.get("chunk_id", "").startswith("M1")
    ]
    m2_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M2"]
    m3_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M3"]

    # 獲取快取統計
    cache_stats = None
    if cache_manager:
        cache_stats = cache_manager.get_cache_stats()

    # 獲取 Gemini 使用統計
    gemini_stats = None
    if optimized_gemini:
        gemini_stats = optimized_gemini.get_usage_stats()

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_info": {
            "total_chunks": len(integrated_engine.chunks),
            "m1_chunks": len(m1_chunks),
            "m2_chunks": len(m2_chunks),
            "m3_chunks": len(m3_chunks),
            "vocabulary_size": len(integrated_engine.vocabulary),
        },
        "modules_status": {
            "M1": "active" if m1_chunks else "inactive",
            "M2": "active" if m2_chunks else "inactive",
            "M3": "active" if m3_chunks else "inactive",
        },
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "cache_stats": cache_stats,
            "gemini_stats": gemini_stats,
        },
    }


@app.post("/comprehensive-analysis")
def comprehensive_analysis(request: UserInput):
    """M1+M2+M3 綜合分析端點（優化版本）"""

    if not integrated_engine:
        return {"error": "引擎未初始化"}

    try:
        user_input = request.user_input

        # 檢查快取
        cached_result = None
        if cache_manager:
            cached_result = cache_manager.get_cached_analysis(user_input)
            if cached_result:
                logger.info("✅ 快取命中，直接返回結果")
                return {**cached_result, "cached": True, "optimized": True}

        # 使用整合引擎進行綜合分析
        result = integrated_engine.analyze_comprehensive(user_input)

        # 將結果轉換為字典格式
        if hasattr(result, "__dict__"):
            result_dict = result.__dict__
        else:
            result_dict = result

        # 確保結果是可序列化的
        try:
            # 嘗試序列化測試
            import json

            json.dumps(result_dict)
        except (TypeError, ValueError):
            # 如果無法序列化，轉換為字符串
            result_dict = {"result": str(result), "type": type(result).__name__}

        # 快取結果
        if cache_manager:
            try:
                cache_manager.cache_analysis_result(user_input, result_dict)
                logger.info("💾 分析結果已快取")
            except Exception as cache_error:
                logger.warning(f"⚠️  快取失敗: {cache_error}")

        return {
            **result_dict,
            "cached": False,
            "optimized": True,
            "cache_available": cache_manager.is_available() if cache_manager else False,
        }

    except Exception as e:
        logger.error(f"❌ 綜合分析錯誤: {e}")
        return {"error": f"分析過程中發生錯誤: {str(e)}"}


@app.post("/m1-flex")
def analyze_with_flex(request: UserInput):
    """M1 Flex Message 分析端點（優化版本）"""

    if not integrated_engine:
        return {"error": "引擎未初始化"}

    try:
        user_input = request.user_input

        # 檢查快取
        cached_flex = None
        if cache_manager:
            cached_flex = cache_manager.get_cached_flex_message(user_input)
            if cached_flex:
                logger.info("✅ Flex Message 快取命中")
                return {"flex_message": cached_flex, "cached": True, "optimized": True}

        # 使用整合引擎進行分析
        result = integrated_engine.analyze_comprehensive(user_input)

        # 生成 Flex Message
        flex_message = create_comprehensive_flex_message(result, user_input)

        # 快取 Flex Message
        if cache_manager:
            cache_manager.cache_flex_message(user_input, flex_message)
            logger.info("💾 Flex Message 已快取")

        return {
            "flex_message": flex_message,
            "comprehensive_analysis": result,
            "cached": False,
            "optimized": True,
            "cache_available": cache_manager.is_available() if cache_manager else False,
        }

    except Exception as e:
        logger.error(f"❌ Flex Message 生成錯誤: {e}")
        return {"flex_message": create_error_flex_message()}


def create_comprehensive_flex_message(result, user_input: str) -> Dict:
    """創建綜合分析 Flex Message（優化版本）"""

    # 提取分析結果
    matched_codes = result.get("matched_codes", [])
    symptom_titles = result.get("symptom_titles", [])
    confidence_levels = result.get("confidence_levels", [])
    comprehensive_summary = result.get("comprehensive_summary", "分析完成")
    action_suggestions = result.get("action_suggestions", [])

    # 生成主要標題
    main_title = "失智症綜合分析"
    if symptom_titles:
        main_title = f"失智症綜合分析：{symptom_titles[0]}"

    # 生成 Flex Message
    flex_message = {
        "type": "flex",
        "altText": main_title,
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 M1+M2+M3 綜合分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                    }
                ],
                "backgroundColor": "#005073",
                "paddingAll": "15dp",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": main_title,
                        "weight": "bold",
                        "size": "md",
                        "color": "#005073",
                        "wrap": True,
                    },
                    {"type": "separator", "margin": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📝 症狀描述",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#666666",
                            },
                            {
                                "type": "text",
                                "text": user_input,
                                "size": "sm",
                                "wrap": True,
                                "margin": "xs",
                            },
                        ],
                    },
                ],
                "paddingAll": "15dp",
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "詳細說明",
                            "text": "請詳細說明相關資訊",
                        },
                        "flex": 1,
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "專業諮詢",
                            "uri": "https://www.tada2002.org.tw/",
                        },
                        "flex": 1,
                        "margin": "sm",
                    },
                ],
                "paddingAll": "15dp",
            },
        },
    }

    # 添加分析結果到 body
    body_contents = flex_message["contents"]["body"]["contents"]

    # 添加檢測到的症狀
    for i, (code, title, confidence) in enumerate(
        zip(matched_codes, symptom_titles, confidence_levels)
    ):
        confidence_color = "#dc3545" if confidence == "low" else "#28a745"
        body_contents.append(
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🚨 {title}",
                        "size": "sm",
                        "weight": "bold",
                        "color": "#005073",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"代碼：{code} | 信心：{confidence.upper()}",
                        "size": "xs",
                        "color": confidence_color,
                        "margin": "xs",
                    },
                ],
            }
        )

    # 添加綜合評估
    body_contents.append(
        {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "📊 綜合評估",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#005073",
                },
                {
                    "type": "text",
                    "text": comprehensive_summary,
                    "size": "xs",
                    "wrap": True,
                    "margin": "xs",
                    "color": "#666666",
                },
            ],
        }
    )

    # 添加建議行動
    if action_suggestions:
        body_contents.append(
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 建議行動",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#005073",
                    },
                    {
                        "type": "text",
                        "text": "；".join(action_suggestions),
                        "size": "xs",
                        "wrap": True,
                        "margin": "xs",
                        "color": "#666666",
                    },
                ],
            }
        )

    return flex_message


def create_error_flex_message():
    """創建錯誤 Flex Message"""
    return {
        "type": "flex",
        "altText": "分析錯誤",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "❌ 分析錯誤",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                    }
                ],
                "backgroundColor": "#dc3545",
                "paddingAll": "15dp",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "抱歉，分析過程中發生錯誤",
                        "size": "md",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": "請稍後再試或聯繫客服",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                    },
                ],
                "paddingAll": "15dp",
            },
        },
    }


@app.get("/cache/stats")
def get_cache_stats():
    """獲取快取統計"""
    if not cache_manager:
        return {"error": "快取管理器未初始化"}

    return cache_manager.get_cache_stats()


@app.get("/gemini/stats")
def get_gemini_stats():
    """獲取 Gemini API 統計"""
    if not optimized_gemini:
        return {"error": "優化 Gemini 客戶端未初始化"}

    return optimized_gemini.get_usage_stats()


@app.post("/cache/clear")
def clear_cache():
    """清除快取"""
    if not cache_manager:
        return {"error": "快取管理器未初始化"}

    success = cache_manager.clear_all_cache()
    return {"success": success, "message": "快取已清除" if success else "清除快取失敗"}


@app.get("/modules/status")
def modules_status():
    """模組狀態檢查"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}

    # 檢查各模組狀態
    m1_chunks = [
        c for c in integrated_engine.chunks if c.get("chunk_id", "").startswith("M1")
    ]
    m2_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M2"]
    m3_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M3"]

    return {
        "modules": {
            "M1": {
                "status": "active" if m1_chunks else "inactive",
                "chunks_count": len(m1_chunks),
                "description": "失智症警訊檢測",
            },
            "M2": {
                "status": "active" if m2_chunks else "inactive",
                "chunks_count": len(m2_chunks),
                "description": "病程階段分析",
            },
            "M3": {
                "status": "active" if m3_chunks else "inactive",
                "chunks_count": len(m3_chunks),
                "description": "BPSD 行為心理症狀",
            },
        },
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "optimized_gemini": optimized_gemini is not None,
        },
        "total_chunks": len(integrated_engine.chunks),
    }


if __name__ == "__main__":
    print("🚀 啟動增強版 M1+M2+M3 整合 RAG API...")
    print("📋 功能：")
    print("   🚨 M1: 失智症十大警訊識別")
    print("   🏥 M2: 病程階段分析")
    print("   🧠 M3: BPSD 行為心理症狀分析")
    print("   🔍 智能語義檢索")
    print("   📊 多重信心度評估")
    print("   🎯 綜合分析報告")
    print("   ⚡ Redis 快取優化")
    print("   💰 Gemini API 成本優化")

    uvicorn.run(app, host="0.0.0.0", port=8005)
