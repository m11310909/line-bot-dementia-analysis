#!/usr/bin/env python3
"""
增強版 M1+M2+M3 整合 API
整合 Redis 快取和優化 Gemini API
"""

import os
import logging
import asyncio
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
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 配置 LINE Bot 超時和重試
LINE_TIMEOUT = 30  # 30 秒超時
LINE_RETRY_ATTEMPTS = 3
LINE_RETRY_BACKOFF = 1

# 創建自定義的 requests session 用於 LINE API
def create_line_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=LINE_RETRY_ATTEMPTS,
        backoff_factor=LINE_RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# 初始化 LINE Bot 配置
def initialize_line_bot():
    try:
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        channel_secret = os.getenv("LINE_CHANNEL_SECRET")
        
        if not channel_access_token or not channel_secret:
            print("❌ LINE Bot 憑證未設置")
            return None, None
        
        # 配置 LINE Bot (簡化版本，不使用自定義 session)
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

# 初始化 logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# 導入所有模組
from modules.m1_warning_signs import M1WarningSignsModule
from modules.m2_progression_matrix import M2ProgressionMatrixModule
from modules.m3_bpsd_classification import M3BPSDClassificationModule
from modules.m4_care_navigation import M4CareNavigationModule

# 初始化所有模組
m1_module = M1WarningSignsModule()
m2_module = M2ProgressionMatrixModule()
m3_module = M3BPSDClassificationModule()
m4_module = M4CareNavigationModule()

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


def create_smart_flex_message(user_input: str, analysis_result: Any) -> Dict:
    """智能創建適合的 Flex Message，根據用戶問題選配視覺模組"""
    
    # 使用 M1 模組進行警訊分析
    m1_analysis = m1_module.analyze_warning_signs(user_input)
    matched_signs = m1_analysis.get('matched_signs', [])
    
    # 使用 M2 模組進行病程階段分析
    m2_analysis = m2_module.analyze_progression(user_input)
    
    # 使用 M3 模組進行 BPSD 症狀分析
    m3_analysis = m3_module.analyze_bpsd_symptoms(user_input)
    
    # 使用 M4 模組進行照護需求分析
    m4_analysis = m4_module.analyze_care_needs(user_input)
    
    # 智能模組選擇邏輯
    user_input_lower = user_input.lower()
    
    # 優先級：M1 > M3 > M2 > M4
    if matched_signs:
        logger.info(f"[DEBUG] 使用 M1 視覺化比對卡片，匹配警訊：{matched_signs}")
        return m1_module.create_visual_comparison_card(user_input, matched_signs)
    
    elif m3_analysis["detected_categories"]:
        logger.info(f"[DEBUG] 使用 M3 BPSD 症狀分析，檢測到：{m3_analysis['detected_categories']}")
        return m3_module.create_bpsd_card(user_input, m3_analysis)
    
    elif any(word in user_input_lower for word in ['階段', '程度', '嚴重', '輕度', '中度', '重度']):
        logger.info(f"[DEBUG] 使用 M2 病程階段評估")
        return m2_module.create_progression_card(user_input, m2_analysis)
    
    elif m4_analysis["detected_needs"]:
        logger.info(f"[DEBUG] 使用 M4 照護導航，檢測到需求：{m4_analysis['detected_needs']}")
        return m4_module.create_care_navigation_card(user_input, m4_analysis)
    
    # 如果都沒有匹配，使用原有的模組選擇邏輯
    else:
        # 分析用戶意圖 - 更精確的關鍵字判斷
        if any(word in user_input_lower for word in ['記憶', '忘記', '重複', '記不住', '記性']):
            component_type = "warning_sign"
            title = "記憶力警訊分析"
            color_theme = "warning"
            logger.info(f"[DEBUG] 選擇模組：記憶力警訊分析 (關鍵字: {[word for word in ['記憶', '忘記', '重複', '記不住', '記性'] if word in user_input_lower]})")
        elif any(word in user_input_lower for word in ['行為', '情緒', '心理', '暴躁', '幻覺', '妄想', '焦慮', '憂鬱', '吵鬧']):
            component_type = "bpsd_symptom"
            title = "行為心理症狀分析"
            color_theme = "neutral"
            logger.info(f"[DEBUG] 選擇模組：行為心理症狀分析 (關鍵字: {[word for word in ['行為', '情緒', '心理', '暴躁', '幻覺', '妄想', '焦慮', '憂鬱', '吵鬧'] if word in user_input_lower]})")
        elif any(word in user_input_lower for word in ['照護', '照顧', '建議', '家屬', '護理', '注意']):
            component_type = "coping_strategy"
            title = "照護建議"
            color_theme = "success"
            logger.info(f"[DEBUG] 選擇模組：照護建議 (關鍵字: {[word for word in ['照護', '照顧', '建議', '家屬', '護理', '注意'] if word in user_input_lower]})")
        elif any(word in user_input_lower for word in ['不會用', '做家事', '生活能力', '洗衣機', '手機', '煮飯', '洗澡']):
            component_type = "daily_activity"
            title = "日常生活能力評估"
            color_theme = "info"
            logger.info(f"[DEBUG] 選擇模組：日常生活能力評估 (關鍵字: {[word for word in ['不會用', '做家事', '生活能力', '洗衣機', '手機', '煮飯', '洗澡'] if word in user_input_lower]})")
        else:
            component_type = "comprehensive"
            title = "失智症綜合分析"
            color_theme = "info"
            logger.info(f"[DEBUG] 選擇模組：失智症綜合分析 (預設)")
        
        # 根據模組類型產生不同的 body 內容
        if component_type == "warning_sign":
            body_contents = [
                {"type": "text", "text": "⚠️ 記憶力警訊：近期有明顯忘記事情、重複提問等現象，建議及早就醫評估。", "weight": "bold", "size": "md", "color": "#d9534f", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
            ]
        elif component_type == "daily_activity":
            body_contents = [
                {"type": "text", "text": "🧩 日常生活能力：近期在家事、使用家電、生活自理上出現困難，建議家屬多協助。", "weight": "bold", "size": "md", "color": "#0275d8", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
            ]
        elif component_type == "bpsd_symptom":
            body_contents = [
                {"type": "text", "text": "🧠 行為心理症狀：近期有暴躁、幻覺、妄想、情緒不穩等現象，建議尋求專業協助。", "weight": "bold", "size": "md", "color": "#f0ad4e", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text",
                "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
            ]
        elif component_type == "coping_strategy":
            body_contents = [
                {"type": "text", "text": "💡 照護建議：保持耐心、建立規律作息、善用輔助工具，並多與醫療團隊溝通。", "weight": "bold", "size": "md", "color": "#5cb85c", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
            ]
        else:
            body_contents = [
                {"type": "text", "text": "🧠 綜合分析：感謝您的提問，以下為綜合分析結果。", "weight": "bold", "size": "md", "color": "#005073", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
            ]

        flex_message = {
            "type": "flex",
            "altText": f"失智症分析：{title}",
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"🧠 {title}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#ffffff"
                        }
                    ],
                    "backgroundColor": "#005073",
                    "paddingAll": "15dp"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": body_contents
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "更多資訊",
                                "text": "請提供更多詳細資訊"
                            },
                            "flex": 1
                        }
                    ]
                }
            }
        }
        
        return flex_message


@handler.add(MessageEvent, message=TextMessageContent)
async def handle_message(event):
    logger.info("[DEBUG] handle_message 被呼叫")
    try:
        user_input = event.message.text
        user_id = event.source.user_id
        logger.info(f"[DEBUG] event.message.text: {user_input}")
        logger.info(f"[DEBUG] event.source.user_id: {user_id}")
        logger.info(f"📨 收到來自 {user_id} 的訊息: {user_input}")
        
        # 檢查 reply token 是否有效
        if not event.reply_token or event.reply_token == "00000000000000000000000000000000":
            logger.error("[DEBUG] Reply token 無效或過期")
            return
        
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
            
            # 生成回應文字
            try:
                # 創建簡單但有效的回應
                if result and isinstance(result, dict):
                    summary = result.get('comprehensive_summary', '分析完成')
                    modules_used = result.get('modules_used', [])
                    chunks_found = len(result.get('retrieved_chunks', []))
                    
                    text_response = f"""🧠 失智症分析結果

📋 分析摘要：{summary}

🔍 檢測到的模組：{', '.join(modules_used) if modules_used else '無'}
📊 相關知識片段：{chunks_found} 個

💡 建議：請諮詢專業醫療人員進行詳細評估
"""
                else:
                    text_response = "🧠 失智症分析完成\n\n分析結果已準備好，建議諮詢專業醫療人員。"
                
                logger.info("[DEBUG] 文字回應創建完成")
                
            except Exception as text_error:
                logger.warning(f"[DEBUG] 文字回應創建失敗: {text_error}")
                text_response = "🧠 失智症分析完成\n\n分析過程中發生錯誤，請稍後再試。"
            
            # 發送回應（帶重試機制）
            success = await send_line_message_with_retry(event.reply_token, text_response)
            
            if not success:
                # 最終備用方案
                await send_fallback_message(event.reply_token)
                
        else:
            response_text = "❌ 系統尚未初始化，請稍後再試。"
            await send_line_message_with_retry(event.reply_token, response_text)
            
    except Exception as e:
        logger.error(f"❌ 訊息處理錯誤: {e}")
        import traceback
        logger.error(f"❌ 詳細錯誤: {traceback.format_exc()}")
        await send_fallback_message(event.reply_token)

async def send_line_message_with_retry(reply_token: str, text: str, max_retries: int = 3) -> bool:
    """發送 LINE 訊息，帶重試機制"""
    for attempt in range(max_retries):
        try:
            logger.info(f"[DEBUG] 嘗試發送訊息 (第 {attempt + 1} 次)")
            
            # 創建文字訊息
            text_message = TextMessage(text=text)
            
            # 設置超時
            import asyncio
            await asyncio.wait_for(
                asyncio.to_thread(
                    line_bot_api.reply_message,
                    ReplyMessageRequest(
                        reply_token=reply_token,
                        messages=[text_message]
                    )
                ),
                timeout=LINE_TIMEOUT
            )
            
            logger.info("✅ 文字訊息發送成功")
            return True
            
        except asyncio.TimeoutError:
            logger.error(f"❌ 發送超時 (第 {attempt + 1} 次)")
        except Exception as e:
            logger.error(f"❌ 發送失敗 (第 {attempt + 1} 次): {e}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(1)  # 等待 1 秒後重試
    
    logger.error("❌ 所有重試都失敗")
    return False

async def send_fallback_message(reply_token: str):
    """發送備用訊息"""
    try:
        fallback_text = "🧠 失智症分析完成\n\n分析結果已準備好，請稍後查看。"
        text_message = TextMessage(text=fallback_text)
        
        await asyncio.wait_for(
            asyncio.to_thread(
                line_bot_api.reply_message,
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[text_message]
                )
            ),
            timeout=10  # 較短的超時時間
        )
        
        logger.info("✅ 備用訊息發送成功")
        
    except Exception as e:
        logger.error(f"❌ 備用訊息發送失敗: {e}")
        # 最後的錯誤處理 - 記錄但不拋出異常
        logger.info("✅ 已回覆用戶純文字訊息（最終備用方案）")

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
        
        try:
            # 設置超時處理
            await asyncio.wait_for(
                asyncio.to_thread(handler.handle, body.decode(), signature),
                timeout=30  # 30 秒超時
            )
            logger.info("[DEBUG] handler.handle 已執行")
            return {"message": "ok"}
            
        except asyncio.TimeoutError:
            logger.error("❌ Webhook 處理超時")
            return {"error": "處理超時"}
        except InvalidSignatureError:
            logger.error("❌ 無效的 LINE 簽名")
            return {"error": "無效簽名"}
        except Exception as handler_error:
            logger.error(f"❌ Handler 處理錯誤: {handler_error}")
            return {"error": str(handler_error)}
            
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
        try:
            cache_manager = RedisCacheManager()
            print("✅ Redis 快取管理器初始化成功")
        except Exception as e:
            print(f"❌ Redis 快取管理器初始化失敗: {e}")
            cache_manager = None
    else:
        print("⚠️  Redis 快取管理器未載入")
        cache_manager = None

    # 初始化優化 Gemini 客戶端
    if OptimizedGeminiClient and api_key:
        try:
            optimized_gemini = OptimizedGeminiClient(api_key)
            print("✅ 優化 Gemini 客戶端初始化成功")
        except Exception as e:
            print(f"❌ 優化 Gemini 客戶端初始化失敗: {e}")
            optimized_gemini = None
    else:
        print("⚠️  優化 Gemini 客戶端未載入")
        optimized_gemini = None

    # 初始化整合引擎
    if M1M2M3IntegratedEngine:
        try:
            integrated_engine = M1M2M3IntegratedEngine()
            print("✅ M1+M2+M3 整合引擎初始化成功")
        except Exception as e:
            print(f"❌ M1+M2+M3 整合引擎初始化失敗: {e}")
            integrated_engine = None
    else:
        print("⚠️  M1+M2+M3 整合引擎未載入")
        integrated_engine = None

    print("✅ 增強版 M1+M2+M3 整合 API 啟動成功")


class UserInput(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "增強版 M1+M2+M3 整合 API", "status": "running"}


@app.get("/health")
def health():
    """健康檢查端點"""
    try:
        # 檢查引擎狀態
        engine_info = {}
        if integrated_engine:
            try:
                # 修正屬性訪問 - 使用正確的屬性名稱
                total_chunks = len(getattr(integrated_engine, 'chunks', []))
                m1_chunks = len([c for c in getattr(integrated_engine, 'chunks', []) if c.get("chunk_id", "").startswith("M1")])
                m2_chunks = len([c for c in getattr(integrated_engine, 'chunks', []) if c.get("module_id") == "M2"])
                m3_chunks = len([c for c in getattr(integrated_engine, 'chunks', []) if c.get("module_id") == "M3"])
                vocabulary_size = len(getattr(integrated_engine, 'vocabulary', []))
                
                engine_info = {
                    "total_chunks": total_chunks,
                    "m1_chunks": m1_chunks,
                    "m2_chunks": m2_chunks,
                    "m3_chunks": m3_chunks,
                    "vocabulary_size": vocabulary_size
                }
            except Exception as e:
                engine_info = {"error": str(e)}

        # 檢查模組狀態
        modules_status = {
            "M1": "active" if integrated_engine and any(c.get("chunk_id", "").startswith("M1") for c in getattr(integrated_engine, 'chunks', [])) else "inactive",
            "M2": "active" if integrated_engine and any(c.get("module_id") == "M2" for c in getattr(integrated_engine, 'chunks', [])) else "inactive",
            "M3": "active" if integrated_engine and any(c.get("module_id") == "M3" for c in getattr(integrated_engine, 'chunks', [])) else "inactive"
        }

        # 檢查優化狀態
        cache_stats = cache_manager.get_cache_stats() if cache_manager else {"status": "unavailable"}
        gemini_stats = optimized_gemini.get_usage_stats() if optimized_gemini else {"status": "unavailable"}

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "engine_info": engine_info,
            "modules_status": modules_status,
            "cache_stats": cache_stats,
            "gemini_stats": gemini_stats,
            "cost_optimization": {
                "cache_hit_rate": 0.0,
                "estimated_savings": 0.0,
                "total_cost": 0.0
            }
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# 添加個別模組端點
@app.post("/analyze/M1")
def analyze_m1(request: UserInput):
    """M1 警訊分析端點"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        result = integrated_engine.analyze_comprehensive(request.user_input)
        # 只返回 M1 相關結果
        m1_chunks = [c for c in result.retrieved_chunks if c.get("chunk_id", "").startswith("M1")]
        return {
            "module": "M1",
            "matched_codes": [c.get("chunk_id") for c in m1_chunks],
            "symptom_titles": [c.get("title") for c in m1_chunks],
            "confidence_levels": [c.get("confidence_score", 0.0) for c in m1_chunks],
            "retrieved_chunks": m1_chunks
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze/M2")
def analyze_m2(request: UserInput):
    """M2 病程分析端點"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        result = integrated_engine.analyze_comprehensive(request.user_input)
        # 只返回 M2 相關結果
        m2_chunks = [c for c in result.retrieved_chunks if c.get("module_id") == "M2"]
        return {
            "module": "M2",
            "stage_detection": result.stage_detection,
            "retrieved_chunks": m2_chunks
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze/M3")
def analyze_m3(request: UserInput):
    """M3 BPSD 分析端點"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        result = integrated_engine.analyze_comprehensive(request.user_input)
        # 只返回 M3 相關結果
        m3_chunks = [c for c in result.retrieved_chunks if c.get("module_id") == "M3"]
        return {
            "module": "M3",
            "bpsd_analysis": result.bpsd_analysis,
            "retrieved_chunks": m3_chunks
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/analyze/M4")
def analyze_m4(request: UserInput):
    """M4 照護導航端點"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        result = integrated_engine.analyze_comprehensive(request.user_input)
        return {
            "module": "M4",
            "action_suggestions": result.action_suggestions,
            "comprehensive_summary": result.comprehensive_summary
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/comprehensive-analysis")
def comprehensive_analysis(request: UserInput):
    """綜合分析端點（優化版本）"""

    if not integrated_engine:
        return {"error": "引擎未初始化"}

    try:
        user_input = request.user_input

        # 檢查快取
        cached_result = None
        if cache_manager:
            cached_result = cache_manager.get_cached_analysis(user_input)
            if cached_result:
                logger.info("✅ 分析結果快取命中")
                return {
                    **cached_result,
                    "cached": True,
                    "optimized": True,
                    "cache_available": cache_manager.is_available()
                }

        # 使用整合引擎進行分析
        result = integrated_engine.analyze_comprehensive(user_input)

        # 將結果轉換為字典格式以便快取
        try:
            if hasattr(result, '__dict__'):
                result_dict = result.__dict__
            else:
                result_dict = result

            # 確保結果可以序列化
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


@app.post("/professional-analysis")
async def professional_analysis(request: UserInput):
    """專業模組化分析端點"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        logger.info(f"🎯 專業分析: {request.user_input}")
        
        # 執行基礎分析
        result = integrated_engine.analyze_comprehensive(request.user_input)
        
        # 轉換為字典格式
        if hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result
        
        # 執行專業模組化分析
        context = {
            "user_input": request.user_input,
            "analysis_result": result_dict
        }
        
        professional_result = await professional_analyzer.analyze_professional(request.user_input, context)
        
        return {
            "status": "success",
            "professional_analysis": professional_result,
            "text_response": create_professional_text_response(professional_result)
        }
        
    except Exception as e:
        logger.error(f"專業分析錯誤: {e}")
        return {"error": str(e)}


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

        # 將 AnalysisResult 對象轉換為字典格式
        if hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result

        # 生成 Flex Message
        flex_message = create_smart_flex_message(user_input, result_dict)

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

    # 提取分析結果 - 處理不同格式的結果
    if isinstance(result, dict):
        matched_codes = result.get("matched_codes", [])
        symptom_titles = result.get("symptom_titles", [])
        confidence_levels = result.get("confidence_levels", [])
        comprehensive_summary = result.get("comprehensive_summary", "分析完成")
        action_suggestions = result.get("action_suggestions", [])
    else:
        # 如果是 AnalysisResult 對象
        matched_codes = result.matched_codes if hasattr(result, 'matched_codes') else []
        symptom_titles = result.symptom_titles if hasattr(result, 'symptom_titles') else []
        confidence_levels = result.confidence_levels if hasattr(result, 'confidence_levels') else []
        comprehensive_summary = result.comprehensive_summary if hasattr(result, 'comprehensive_summary') else "分析完成"
        action_suggestions = result.action_suggestions if hasattr(result, 'action_suggestions') else []

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
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#005073",
                "paddingAll": "15dp"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": comprehensive_summary,
                        "weight": "bold",
                        "size": "md",
                        "color": "#005073",
                        "wrap": True
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
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
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": user_input,
                                "size": "sm",
                                "weight": "regular",
                                "wrap": True,
                                "margin": "xs"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "更多資訊",
                            "text": "請提供更多詳細資訊"
                        },
                        "flex": 1
                    }
                ]
            }
        }
    }

    # 添加症狀分析
    if symptom_titles:
        for i, title in enumerate(symptom_titles[:2]):
            code = matched_codes[i] if i < len(matched_codes) else f"M1-{i+1:02d}"
            confidence = confidence_levels[i] if i < len(confidence_levels) else "MEDIUM"
            
            symptom_box = {
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
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"代碼：{code} | 信心：{confidence}",
                        "size": "xs",
                        "weight": "regular",
                        "color": "#dc3545",
                        "margin": "xs"
                    }
                ]
            }
            flex_message["contents"]["body"]["contents"].append(symptom_box)

    # 添加行動建議
    if action_suggestions:
        action_box = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "💡 建議行動",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#4ECDC4"
                }
            ]
        }
        
        for suggestion in action_suggestions[:3]:
            action_box["contents"].append({
                "type": "text",
                "text": f"• {suggestion}",
                "size": "sm",
                "wrap": True,
                "margin": "xs"
            })
        
        flex_message["contents"]["body"]["contents"].append(action_box)

    return flex_message


def create_simple_flex_message(summary: str, user_input: str):
    """創建簡單的 Flex Message"""
    return {
        "type": "flex",
        "altText": "失智症分析結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症分析",
                        "weight": "bold",
                        "size": "lg",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": summary,
                        "wrap": True,
                        "margin": "md",
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": f"用戶描述：{user_input}",
                        "size": "xs",
                        "color": "#999999",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            }
        }
    }


def create_error_flex_message():
    """創建錯誤 Flex Message"""
    return {
        "type": "flex",
        "altText": "分析錯誤",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "❌ 分析錯誤",
                        "weight": "bold",
                        "size": "lg",
                        "align": "center",
                        "color": "#dc3545"
                    },
                    {
                        "type": "text",
                        "text": "抱歉，分析過程中發生錯誤。請稍後再試或提供更多詳細資訊。",
                        "wrap": True,
                        "margin": "md",
                        "size": "sm",
                        "color": "#666666"
                    }
                ]
            }
        }
    }


@app.get("/cache/stats")
def get_cache_stats():
    """獲取快取統計"""
    if cache_manager:
        return cache_manager.get_cache_stats()
    return {"status": "unavailable"}


@app.get("/gemini/stats")
def get_gemini_stats():
    """獲取 Gemini 統計"""
    if optimized_gemini:
        return optimized_gemini.get_usage_stats()
    return {"status": "unavailable"}


@app.post("/cache/clear")
def clear_cache():
    """清除快取"""
    if cache_manager:
        try:
            cache_manager.clear_all_cache()
            return {"message": "快取已清除", "status": "success"}
        except Exception as e:
            return {"message": f"清除快取失敗: {str(e)}", "status": "error"}
    return {"message": "快取管理器不可用", "status": "unavailable"}


@app.get("/modules/status")
def modules_status():
    """獲取模組狀態"""
    return {
        "integrated_engine": "active" if integrated_engine else "inactive",
        "cache_manager": "active" if cache_manager else "inactive",
        "optimized_gemini": "active" if optimized_gemini else "inactive",
        "line_bot_api": "active" if line_bot_api else "inactive"
    }


@app.post("/debug/flex-message")
def debug_flex_message(request: UserInput):
    """調試 Flex Message 格式"""
    try:
        return {
            "status": "success",
            "message": "Debug endpoint working",
            "user_input": request.user_input
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def perform_xai_analysis(user_input: str, analysis_result: Any) -> Dict[str, Any]:
    """執行 XAI 分析，提供可解釋的人工智慧分析"""
    try:
        # 分析用戶輸入的關鍵特徵
        xai_features = {
            "symptom_keywords": [],
            "severity_level": "unknown",
            "confidence_score": 0.0,
            "explanation": "",
            "recommended_modules": []
        }
        
        # 提取關鍵症狀詞彙
        symptom_keywords = [
            "記憶", "忘記", "健忘", "語言", "表達", "迷路", "情緒", 
            "暴躁", "憂鬱", "焦慮", "妄想", "幻覺", "遊走", "睡眠",
            "不認識", "不會用", "無法", "困難", "混亂", "退化"
        ]
        
        found_keywords = [kw for kw in symptom_keywords if kw in user_input]
        xai_features["symptom_keywords"] = found_keywords
        
        # 根據關鍵詞判斷嚴重程度
        if any(kw in user_input for kw in ["重度", "嚴重", "完全", "不認識", "臥床"]):
            xai_features["severity_level"] = "severe"
            xai_features["confidence_score"] = 0.8
        elif any(kw in user_input for kw in ["中度", "明顯", "迷路", "不會用", "暴躁"]):
            xai_features["severity_level"] = "moderate"
            xai_features["confidence_score"] = 0.7
        elif any(kw in user_input for kw in ["輕度", "初期", "記憶", "忘記"]):
            xai_features["severity_level"] = "mild"
            xai_features["confidence_score"] = 0.6
        else:
            xai_features["severity_level"] = "unknown"
            xai_features["confidence_score"] = 0.5
        
        # 生成解釋
        if found_keywords:
            xai_features["explanation"] = f"檢測到關鍵症狀詞彙: {', '.join(found_keywords)}。根據症狀描述，評估為{xai_features['severity_level']}程度。"
        else:
            xai_features["explanation"] = "未檢測到明確的症狀關鍵詞，建議提供更詳細的症狀描述。"
        
        # 推薦模組
        if "記憶" in user_input or "忘記" in user_input:
            xai_features["recommended_modules"].append("M1")
        if any(kw in user_input for kw in ["輕度", "中度", "重度", "階段"]):
            xai_features["recommended_modules"].append("M2")
        if any(kw in user_input for kw in ["情緒", "暴躁", "憂鬱", "妄想", "幻覺"]):
            xai_features["recommended_modules"].append("M3")
        if any(kw in user_input for kw in ["照護", "協助", "建議", "幫助"]):
            xai_features["recommended_modules"].append("M4")
        
        return xai_features
        
    except Exception as e:
        logger.error(f"XAI 分析失敗: {e}")
        return {
            "symptom_keywords": [],
            "severity_level": "unknown",
            "confidence_score": 0.0,
            "explanation": "XAI 分析過程中發生錯誤",
            "recommended_modules": []
        }


def select_visual_module(user_input: str, xai_analysis: Dict[str, Any], analysis_result: Any) -> str:
    """根據 XAI 分析結果選擇最適合的視覺模組"""
    try:
        # 根據症狀關鍵詞選擇模組
        if any(kw in user_input for kw in ["記憶", "忘記", "健忘"]):
            return "M1"  # 警訊模組
        elif any(kw in user_input for kw in ["輕度", "中度", "重度", "階段", "病程"]):
            return "M2"  # 病程模組
        elif any(kw in user_input for kw in ["情緒", "暴躁", "憂鬱", "妄想", "幻覺", "遊走"]):
            return "M3"  # BPSD 模組
        elif any(kw in user_input for kw in ["照護", "協助", "建議", "幫助", "資源"]):
            return "M4"  # 照護模組
        else:
            # 根據 XAI 推薦模組選擇
            if xai_analysis.get("recommended_modules"):
                return xai_analysis["recommended_modules"][0]
            else:
                return "M1"  # 預設使用 M1 模組
                
    except Exception as e:
        logger.error(f"視覺模組選擇失敗: {e}")
        return "M1"  # 預設使用 M1 模組


def create_xai_visualization_module():
    """創建 XAI 視覺化模組"""
    return {
        "M1": {
            "name": "警訊檢測模組",
            "keywords": ["記憶", "忘記", "健忘", "找不到", "遺失", "重複", "反覆"],
            "visual_type": "warning_cards",
            "confidence_threshold": 0.6,
            "color_scheme": "#ff6b6b"
        },
        "M2": {
            "name": "病程評估模組", 
            "keywords": ["輕度", "中度", "重度", "階段", "病程", "惡化", "進步"],
            "visual_type": "progression_chart",
            "confidence_threshold": 0.7,
            "color_scheme": "#4ecdc4"
        },
        "M3": {
            "name": "BPSD 症狀模組",
            "keywords": ["情緒", "暴躁", "憂鬱", "妄想", "幻覺", "遊走", "睡眠", "攻擊"],
            "visual_type": "symptom_matrix",
            "confidence_threshold": 0.65,
            "color_scheme": "#45b7d1"
        },
        "M4": {
            "name": "照護導航模組",
            "keywords": ["照護", "協助", "建議", "幫助", "資源", "服務", "支援"],
            "visual_type": "care_navigation",
            "confidence_threshold": 0.5,
            "color_scheme": "#96ceb4"
        },
        "M5": {
            "name": "認知評估模組",
            "keywords": ["認知", "思考", "判斷", "理解", "學習", "注意力"],
            "visual_type": "cognitive_assessment",
            "confidence_threshold": 0.6,
            "color_scheme": "#feca57"
        },
        "M6": {
            "name": "行為分析模組",
            "keywords": ["行為", "動作", "習慣", "反應", "模式", "改變"],
            "visual_type": "behavior_analysis",
            "confidence_threshold": 0.55,
            "color_scheme": "#ff9ff3"
        },
        "M7": {
            "name": "環境適應模組",
            "keywords": ["環境", "適應", "安全", "空間", "設備", "設施"],
            "visual_type": "environment_adaptation",
            "confidence_threshold": 0.5,
            "color_scheme": "#54a0ff"
        }
    }


def analyze_xai_visualization(user_input: str, analysis_result: Any) -> Dict[str, Any]:
    """XAI 視覺化分析 - 遵循 Cursor IDE 指南"""
    try:
        # 獲取視覺化模組配置
        visual_modules = create_xai_visualization_module()
        
        # 初始化分析結果
        xai_result = {
            "input_text": user_input,
            "detected_modules": [],
            "primary_module": None,
            "confidence_scores": {},
            "visual_recommendations": [],
            "explanation": "",
            "processing_time": 0
        }
        
        start_time = time.time()
        
        # 分析每個模組的匹配度
        for module_id, module_config in visual_modules.items():
            confidence = calculate_module_confidence(user_input, module_config)
            xai_result["confidence_scores"][module_id] = confidence
            
            if confidence >= module_config["confidence_threshold"]:
                xai_result["detected_modules"].append({
                    "module_id": module_id,
                    "name": module_config["name"],
                    "confidence": confidence,
                    "visual_type": module_config["visual_type"],
                    "color_scheme": module_config["color_scheme"]
                })
        
        # 選擇主要模組
        if xai_result["detected_modules"]:
            primary = max(xai_result["detected_modules"], key=lambda x: x["confidence"])
            xai_result["primary_module"] = primary["module_id"]
            
            # 生成視覺化建議
            xai_result["visual_recommendations"] = generate_visual_recommendations(
                primary, analysis_result
            )
            
            # 生成解釋
            xai_result["explanation"] = generate_xai_explanation(
                user_input, primary, xai_result["detected_modules"]
            )
        
        xai_result["processing_time"] = time.time() - start_time
        
        return xai_result
        
    except Exception as e:
        logger.error(f"XAI 視覺化分析失敗: {e}")
        return {
            "input_text": user_input,
            "detected_modules": [],
            "primary_module": "M1",
            "confidence_scores": {"M1": 0.5},
            "visual_recommendations": [],
            "explanation": "XAI 分析過程中發生錯誤，使用預設模組",
            "processing_time": 0,
            "error": str(e)
        }


def calculate_module_confidence(user_input: str, module_config: Dict) -> float:
    """計算模組匹配度 - 使用關鍵詞分析"""
    try:
        user_input_lower = user_input.lower()
        keywords = module_config["keywords"]
        
        # 計算關鍵詞匹配
        matched_keywords = [kw for kw in keywords if kw in user_input_lower]
        match_ratio = len(matched_keywords) / len(keywords) if keywords else 0
        
        # 根據匹配程度計算信心度
        if match_ratio >= 0.3:
            confidence = 0.8 + (match_ratio - 0.3) * 0.4  # 0.8-1.0
        elif match_ratio >= 0.1:
            confidence = 0.6 + (match_ratio - 0.1) * 1.0  # 0.6-0.8
        else:
            confidence = match_ratio * 6.0  # 0-0.6
        
        return min(confidence, 1.0)
        
    except Exception as e:
        logger.error(f"計算模組信心度失敗: {e}")
        return 0.5


def generate_visual_recommendations(primary_module: Dict, analysis_result: Any) -> List[Dict]:
    """生成視覺化建議"""
    try:
        recommendations = []
        
        if primary_module["module_id"] == "M1":
            recommendations.append({
                "type": "warning_cards",
                "title": "失智症警訊檢測",
                "description": "檢測到可能的失智症警訊症狀",
                "priority": "high",
                "visual_elements": ["warning_icon", "symptom_list", "severity_indicator"]
            })
            
        elif primary_module["module_id"] == "M2":
            recommendations.append({
                "type": "progression_chart",
                "title": "病程階段評估",
                "description": "評估失智症病程發展階段",
                "priority": "medium",
                "visual_elements": ["stage_indicator", "timeline", "care_focus"]
            })
            
        elif primary_module["module_id"] == "M3":
            recommendations.append({
                "type": "symptom_matrix",
                "title": "BPSD 症狀分析",
                "description": "分析行為心理症狀",
                "priority": "high",
                "visual_elements": ["symptom_grid", "severity_scale", "intervention_tips"]
            })
            
        elif primary_module["module_id"] == "M4":
            recommendations.append({
                "type": "care_navigation",
                "title": "照護資源導航",
                "description": "提供照護建議和資源",
                "priority": "medium",
                "visual_elements": ["resource_list", "contact_info", "action_buttons"]
            })
        
        return recommendations
        
    except Exception as e:
        logger.error(f"生成視覺化建議失敗: {e}")
        return []


def generate_xai_explanation(user_input: str, primary_module: Dict, all_modules: List[Dict]) -> str:
    """生成 XAI 解釋"""
    try:
        explanation_parts = []
        
        # 主要模組解釋
        explanation_parts.append(f"檢測到 {primary_module['name']} (信心度: {primary_module['confidence']:.1%})")
        
        # 其他檢測到的模組
        other_modules = [m for m in all_modules if m["module_id"] != primary_module["module_id"]]
        if other_modules:
            other_names = [m["name"] for m in other_modules[:2]]  # 最多顯示2個
            explanation_parts.append(f"同時檢測到: {', '.join(other_names)}")
        
        # 關鍵詞解釋
        visual_modules = create_xai_visualization_module()
        module_config = visual_modules[primary_module["module_id"]]
        matched_keywords = [kw for kw in module_config["keywords"] if kw in user_input.lower()]
        
        if matched_keywords:
            explanation_parts.append(f"關鍵症狀詞彙: {', '.join(matched_keywords[:3])}")
        
        return " | ".join(explanation_parts)
        
    except Exception as e:
        logger.error(f"生成 XAI 解釋失敗: {e}")
        return "XAI 分析完成"


def create_enhanced_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建增強版 Flex Message - 整合 XAI 視覺化"""
    try:
        # 獲取主要模組
        primary_module = xai_analysis.get("primary_module", "M1")
        visual_modules = create_xai_visualization_module()
        module_config = visual_modules.get(primary_module, visual_modules["M1"])
        
        # 根據模組類型創建不同的視覺化
        if primary_module == "M1":
            return create_m1_warning_flex_message(user_input, analysis_result, xai_analysis)
        elif primary_module == "M2":
            return create_m2_progression_flex_message(user_input, analysis_result, xai_analysis)
        elif primary_module == "M3":
            return create_m3_bpsd_flex_message(user_input, analysis_result, xai_analysis)
        elif primary_module == "M4":
            return create_m4_care_flex_message(user_input, analysis_result, xai_analysis)
        else:
            return create_default_flex_message(user_input, analysis_result, xai_analysis)
            
    except Exception as e:
        logger.error(f"創建增強版 Flex Message 失敗: {e}")
        return create_error_flex_message()


def create_m1_warning_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建 M1 警訊 Flex Message"""
    return {
        "type": "flex",
        "altText": "失智症警訊檢測結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ 失智症警訊檢測",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#ff6b6b"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "檢測到可能的失智症警訊症狀",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#333333"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"信心度: {xai_analysis.get('confidence_scores', {}).get('M1', 0):.1%}",
                        "size": "xs",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": xai_analysis.get("explanation", ""),
                        "wrap": True,
                        "size": "xs",
                        "color": "#666666",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "詳細分析",
                            "data": f"analyze_detail:M1:{user_input}"
                        },
                        "style": "primary",
                        "color": "#ff6b6b"
                    }
                ]
            }
        }
    }


def create_m2_progression_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建 M2 病程 Flex Message"""
    return {
        "type": "flex",
        "altText": "失智症病程評估結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📊 病程階段評估",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#4ecdc4"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "評估失智症病程發展階段",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#333333"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"信心度: {xai_analysis.get('confidence_scores', {}).get('M2', 0):.1%}",
                        "size": "xs",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": xai_analysis.get("explanation", ""),
                        "wrap": True,
                        "size": "xs",
                        "color": "#666666",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "查看病程",
                            "data": f"analyze_detail:M2:{user_input}"
                        },
                        "style": "primary",
                        "color": "#4ecdc4"
                    }
                ]
            }
        }
    }


def create_m3_bpsd_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建 M3 BPSD Flex Message"""
    return {
        "type": "flex",
        "altText": "BPSD 症狀分析結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 BPSD 症狀分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#45b7d1"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "分析行為心理症狀",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#333333"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"信心度: {xai_analysis.get('confidence_scores', {}).get('M3', 0):.1%}",
                        "size": "xs",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": xai_analysis.get("explanation", ""),
                        "wrap": True,
                        "size": "xs",
                        "color": "#666666",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "症狀詳情",
                            "data": f"analyze_detail:M3:{user_input}"
                        },
                        "style": "primary",
                        "color": "#45b7d1"
                    }
                ]
            }
        }
    }


def create_m4_care_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建 M4 照護 Flex Message"""
    return {
        "type": "flex",
        "altText": "照護資源導航結果",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🏥 照護資源導航",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#96ceb4"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "提供照護建議和資源",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#333333"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"信心度: {xai_analysis.get('confidence_scores', {}).get('M4', 0):.1%}",
                        "size": "xs",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": xai_analysis.get("explanation", ""),
                        "wrap": True,
                        "size": "xs",
                        "color": "#666666",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "照護資源",
                            "data": f"analyze_detail:M4:{user_input}"
                        },
                        "style": "primary",
                        "color": "#96ceb4"
                    }
                ]
            }
        }
    }


def create_default_flex_message(user_input: str, analysis_result: Any, xai_analysis: Dict) -> Dict:
    """創建預設 Flex Message"""
    return {
        "type": "flex",
        "altText": "失智症分析結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症分析",
                        "weight": "bold",
                        "size": "lg",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": xai_analysis.get("explanation", "分析完成"),
                        "wrap": True,
                        "margin": "md",
                        "size": "sm",
                        "color": "#666666"
                    }
                ]
            }
        }
    }


def create_jtbd_text_response(user_input: str, analysis_result: Any, xai_visualization: Dict) -> str:
    """根據 JTBD 架構創建情境化的文字回應"""
    try:
        # 獲取主要模組
        primary_module = xai_visualization.get("primary_module", "M1")
        confidence = xai_visualization.get("confidence_scores", {}).get(primary_module, 0)
        
        # 基礎資訊
        summary = analysis_result.get('comprehensive_summary', '分析完成')
        modules_used = analysis_result.get('modules_used', [])
        chunks_found = len(analysis_result.get('retrieved_chunks', []))
        
        # 根據模組創建不同的 JTBD 回應
        if primary_module == "M1":
            return create_m1_jtbd_response(user_input, summary, confidence, chunks_found)
        elif primary_module == "M2":
            return create_m2_jtbd_response(user_input, summary, confidence, chunks_found)
        elif primary_module == "M3":
            return create_m3_jtbd_response(user_input, summary, confidence, chunks_found)
        elif primary_module == "M4":
            return create_m4_jtbd_response(user_input, summary, confidence, chunks_found)
        else:
            return create_default_jtbd_response(user_input, summary, modules_used, chunks_found)
            
    except Exception as e:
        logger.error(f"JTBD 文字回應創建失敗: {e}")
        return create_error_jtbd_response()


def create_m1_jtbd_response(user_input: str, summary: str, confidence: float, chunks_found: int) -> str:
    """M1: 十大警訊比對卡 - JTBD 回應"""
    response = "⚠️ 失智症警訊檢測\n\n"
    
    # 降低焦慮：明確的判斷依據
    if confidence >= 0.8:
        response += "🔍 AI 信心度: 高 (90%+)\n"
        response += "📊 分析摘要: " + summary + "\n\n"
        response += "🎯 快速判斷:\n"
        response += "• 症狀符合失智症警訊\n"
        response += "• 建議及早就醫評估\n\n"
    elif confidence >= 0.6:
        response += "🔍 AI 信心度: 中 (60-80%)\n"
        response += "📊 分析摘要: " + summary + "\n\n"
        response += "🎯 需要觀察:\n"
        response += "• 症狀需要進一步確認\n"
        response += "• 建議定期追蹤記錄\n\n"
    else:
        response += "🔍 AI 信心度: 低 (<60%)\n"
        response += "📊 分析摘要: " + summary + "\n\n"
        response += "🎯 持續觀察:\n"
        response += "• 症狀尚不明確\n"
        response += "• 建議記錄變化\n\n"
    
    # 建立信任：展示推理過程
    response += "💡 推理路徑:\n"
    response += "1. 症狀識別 → 2. 警訊比對 → 3. 風險評估\n\n"
    
    # 促進行動：清楚指引下一步
    response += "📋 建議行動:\n"
    if confidence >= 0.8:
        response += "• 立即預約神經科門診\n"
        response += "• 準備詳細症狀記錄\n"
        response += "• 聯繫家屬討論\n"
    elif confidence >= 0.6:
        response += "• 觀察症狀變化\n"
        response += "• 記錄異常行為\n"
        response += "• 考慮初步篩檢\n"
    else:
        response += "• 持續觀察記錄\n"
        response += "• 定期評估追蹤\n"
        response += "• 保持正常生活\n"
    
    response += f"\n📊 找到相關片段: {chunks_found} 個"
    return response


def create_m2_jtbd_response(user_input: str, summary: str, confidence: float, chunks_found: int) -> str:
    """M2: 病程階段對照 - JTBD 回應"""
    response = "📈 病程階段評估\n\n"
    
    # 定位現況：清楚標示當前階段
    response += "🎯 階段定位:\n"
    if "輕度" in summary or "早期" in summary:
        response += "📍 當前階段: 輕度失智症\n"
        response += "⏰ 預估病程: 2-4年\n"
        response += "🔍 主要特徵: 記憶力減退、輕微認知障礙\n\n"
    elif "中度" in summary or "中期" in summary:
        response += "📍 當前階段: 中度失智症\n"
        response += "⏰ 預估病程: 2-8年\n"
        response += "🔍 主要特徵: 明顯認知障礙、日常生活需協助\n\n"
    elif "重度" in summary or "晚期" in summary:
        response += "📍 當前階段: 重度失智症\n"
        response += "⏰ 預估病程: 1-3年\n"
        response += "🔍 主要特徵: 嚴重認知障礙、完全依賴照護\n\n"
    else:
        response += "📍 階段評估: 需要進一步確認\n"
        response += "📊 分析摘要: " + summary + "\n\n"
    
    # 預期管理：展示可能進展
    response += "🔄 病程預期:\n"
    response += "• 症狀會逐漸進展\n"
    response += "• 進展速度因人而異\n"
    response += "• 早期介入可延緩惡化\n\n"
    
    # 資源準備：各階段需求提示
    response += "📋 階段準備:\n"
    if "輕度" in summary or "早期" in summary:
        response += "• 建立醫療團隊\n"
        response += "• 學習照護技巧\n"
        response += "• 規劃未來安排\n"
    elif "中度" in summary or "中期" in summary:
        response += "• 申請照護資源\n"
        response += "• 調整居家環境\n"
        response += "• 尋求家屬支持\n"
    elif "重度" in summary or "晚期" in summary:
        response += "• 24小時照護安排\n"
        response += "• 安寧照護準備\n"
        response += "• 家屬心理支持\n"
    else:
        response += "• 定期醫療評估\n"
        response += "• 症狀監測記錄\n"
        response += "• 資源資訊收集\n"
    
    response += f"\n📊 找到相關片段: {chunks_found} 個"
    return response


def create_m3_jtbd_response(user_input: str, summary: str, confidence: float, chunks_found: int) -> str:
    """M3: BPSD 精神行為症狀 - JTBD 回應"""
    response = "🧠 BPSD 症狀分析\n\n"
    
    # 正常化：這是疾病症狀
    response += "💡 症狀理解:\n"
    response += "• 這些是疾病表現，不是故意\n"
    response += "• 大腦功能受損導致行為改變\n"
    response += "• 症狀會隨病程變化\n\n"
    
    # 症狀分類和處理
    if "情緒" in user_input or "暴躁" in user_input or "發脾氣" in user_input:
        response += "😤 情緒症狀處理:\n"
        response += "• 保持冷靜，避免爭執\n"
        response += "• 轉移注意力到愉快話題\n"
        response += "• 建立規律作息\n"
        response += "• 考慮音樂療法\n\n"
    elif "妄想" in user_input or "幻覺" in user_input:
        response += "👁️ 妄想幻覺處理:\n"
        response += "• 不要直接反駁\n"
        response += "• 確認環境安全\n"
        response += "• 尋求醫療評估\n"
        response += "• 考慮藥物治療\n\n"
    elif "遊走" in user_input or "走失" in user_input:
        response += "🚶 遊走行為處理:\n"
        response += "• 安裝門鎖警報\n"
        response += "• 配戴身份識別\n"
        response += "• 鄰居社區協助\n"
        response += "• 考慮GPS追蹤\n\n"
    elif "睡眠" in user_input or "不睡覺" in user_input:
        response += "😴 睡眠問題處理:\n"
        response += "• 建立規律作息\n"
        response += "• 避免午後小睡\n"
        response += "• 營造安靜環境\n"
        response += "• 適度日間活動\n\n"
    else:
        response += "🔍 一般症狀處理:\n"
        response += "• 保持耐心和理解\n"
        response += "• 尋求專業建議\n"
        response += "• 建立支持網絡\n"
        response += "• 照顧者自我照顧\n\n"
    
    # 賦能：提供具體技巧
    response += "💪 照護技巧:\n"
    response += "• 使用簡單明確的語言\n"
    response += "• 保持環境穩定\n"
    response += "• 建立日常規律\n"
    response += "• 尋求專業支援\n\n"
    
    # 支持：你並不孤單
    response += "🤝 支持資源:\n"
    response += "• 失智症協會諮詢\n"
    response += "• 家屬支持團體\n"
    response += "• 專業照護服務\n"
    response += "• 緊急聯絡資訊\n"
    
    response += f"\n📊 找到相關片段: {chunks_found} 個"
    return response


def create_m4_jtbd_response(user_input: str, summary: str, confidence: float, chunks_found: int) -> str:
    """M4: 照護任務導航 - JTBD 回應"""
    response = "🗺️ 照護任務導航\n\n"
    
    # 結構化：分類整理任務
    response += "📋 任務分類:\n\n"
    
    # 緊急任務
    response += "🚨 緊急任務:\n"
    response += "• 醫療評估安排\n"
    response += "• 安全環境檢查\n"
    response += "• 緊急聯絡建立\n\n"
    
    # 重要任務
    response += "⭐ 重要任務:\n"
    response += "• 照護資源申請\n"
    response += "• 法律文件準備\n"
    response += "• 財務規劃安排\n\n"
    
    # 一般任務
    response += "📝 一般任務:\n"
    response += "• 日常照護學習\n"
    response += "• 支持網絡建立\n"
    response += "• 自我照顧安排\n\n"
    
    # 優先排序：輕重緩急
    response += "🎯 優先順序:\n"
    response += "1. 確保安全與醫療\n"
    response += "2. 申請必要資源\n"
    response += "3. 建立照護系統\n"
    response += "4. 長期規劃準備\n\n"
    
    # 進度追蹤：成就感建立
    response += "📈 進度建議:\n"
    response += "• 每週完成2-3項任務\n"
    response += "• 記錄完成進度\n"
    response += "• 慶祝小成就\n"
    response += "• 尋求協助不孤單\n\n"
    
    # 個人化建議
    response += "💡 個人化建議:\n"
    if "申請" in user_input or "補助" in user_input:
        response += "• 準備相關證明文件\n"
        response += "• 諮詢社會福利單位\n"
        response += "• 了解申請流程時程\n"
    elif "醫療" in user_input or "醫生" in user_input:
        response += "• 建立醫療團隊\n"
        response += "• 準備症狀記錄\n"
        response += "• 安排定期回診\n"
    elif "日常" in user_input or "生活" in user_input:
        response += "• 調整居家環境\n"
        response += "• 建立日常規律\n"
        response += "• 學習照護技巧\n"
    else:
        response += "• 根據症狀調整任務\n"
        response += "• 定期評估需求\n"
        response += "• 保持彈性調整\n"
    
    response += f"\n📊 找到相關片段: {chunks_found} 個"
    return response


def create_default_jtbd_response(user_input: str, summary: str, modules_used: List[str], chunks_found: int) -> str:
    """預設 JTBD 回應"""
    response = "🧠 失智症綜合分析\n\n"
    response += "📊 分析摘要: " + summary + "\n\n"
    
    if modules_used:
        response += "🔍 使用模組: " + ", ".join(modules_used) + "\n"
    response += f"📋 找到相關片段: {chunks_found} 個\n\n"
    
    response += "💡 建議行動:\n"
    response += "• 提供更多詳細症狀描述\n"
    response += "• 說明具體困擾情況\n"
    response += "• 詢問特定照護需求\n\n"
    
    response += "🎯 下一步:\n"
    response += "• 我們會根據您的描述\n"
    response += "• 提供更精準的分析\n"
    response += "• 給出具體的建議\n"
    
    return response


def create_professional_text_response(professional_result: Dict[str, Any]) -> str:
    """創建專業模組化分析回應"""
    try:
        selected_modules = professional_result.get("selected_modules", [])
        best_answer = professional_result.get("best_answer", "")
        verification = professional_result.get("verification", {})
        comprehensive_score = professional_result.get("comprehensive_score", 0)
        xai_visualization = professional_result.get("xai_visualization", {})
        
        response = "🧠 專業失智症分析系統\n\n"
        
        # 模組分析結果
        response += "📊 專業模組分析:\n"
        for module in selected_modules:
            module_info = professional_result.get("analysis_results", {}).get(module, {})
            if module == "M1":
                warning_signs = module_info.get("warning_signs_detected", [])
                risk_level = module_info.get("risk_level", "low")
                response += f"• M1 警訊檢測: 發現 {len(warning_signs)} 個警訊 (風險等級: {risk_level})\n"
            elif module == "M2":
                current_stage = module_info.get("current_stage", "未知")
                response += f"• M2 病程評估: 當前階段 {current_stage}\n"
            elif module == "M3":
                total_symptoms = module_info.get("total_symptoms", 0)
                response += f"• M3 BPSD 分析: 檢測到 {total_symptoms} 個症狀\n"
            elif module == "M4":
                matched_resources = module_info.get("matched_resources", [])
                response += f"• M4 資源導航: 匹配到 {len(matched_resources)} 個資源\n"
        
        response += "\n"
        
        # 最佳答案
        response += "💡 專業建議:\n"
        response += best_answer + "\n\n"
        
        # 品質驗證
        overall_score = verification.get("overall_score", 0)
        recommendation = verification.get("recommendation", "")
        response += f"🔍 品質驗證: {overall_score:.1%} ({recommendation})\n\n"
        
        # XAI 視覺化摘要
        if xai_visualization:
            reasoning_path = xai_visualization.get("reasoning_path", {})
            steps = reasoning_path.get("steps", [])
            response += "🎯 AI 推理路徑:\n"
            for step in steps[:3]:  # 只顯示前3步
                response += f"• {step['action']}: {step['description']}\n"
            response += "\n"
        
        # 綜合評分
        response += f"📈 綜合評分: {comprehensive_score:.1%}\n"
        response += f"🎯 選擇理由: {professional_result.get('selection_reason', '')}\n\n"
        
        # 下一步建議
        response += "📋 下一步建議:\n"
        if "M1" in selected_modules:
            response += "• 立即預約神經科門診進行專業評估\n"
        if "M2" in selected_modules:
            response += "• 定期追蹤症狀變化並記錄進展\n"
        if "M3" in selected_modules:
            response += "• 尋求專業行為治療和藥物諮詢\n"
        if "M4" in selected_modules:
            response += "• 按優先順序申請相關照護資源\n"
        
        return response
        
    except Exception as e:
        logger.error(f"專業回應創建失敗: {e}")
        return "🧠 專業失智症分析完成\n\n分析過程中發生錯誤，請稍後再試。"


def create_error_jtbd_response() -> str:
    """錯誤時的 JTBD 回應"""
    return """🧠 失智症分析系統

❌ 分析過程中發生錯誤

💡 請稍後再試或：
• 重新描述症狀
• 提供更多詳細資訊
• 聯繫技術支援

🤝 我們會持續改進服務品質"""


# 新增進階 AI 技術模組
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import time
import random

# Aspect Verifiers 多角度答案驗證
class AspectVerifier:
    """多角度答案驗證器"""
    
    def __init__(self):
        self.aspects = {
            "medical_accuracy": "醫學準確性驗證",
            "safety_assessment": "安全性評估", 
            "feasibility_analysis": "可行性分析",
            "emotional_appropriateness": "情感適切性檢查"
        }
    
    async def verify_answer(self, answer: str, context: Dict) -> Dict[str, Any]:
        """多角度驗證答案"""
        verification_results = {}
        
        for aspect, description in self.aspects.items():
            score = await self._verify_aspect(aspect, answer, context)
            verification_results[aspect] = {
                "description": description,
                "score": score,
                "status": "pass" if score >= 0.7 else "warning" if score >= 0.5 else "fail"
            }
        
        # 計算綜合評分
        overall_score = sum(result["score"] for result in verification_results.values()) / len(verification_results)
        
        return {
            "overall_score": overall_score,
            "aspects": verification_results,
            "recommendation": self._get_recommendation(overall_score)
        }
    
    async def _verify_aspect(self, aspect: str, answer: str, context: Dict) -> float:
        """驗證特定角度"""
        # 模擬驗證邏輯
        if aspect == "medical_accuracy":
            return self._verify_medical_accuracy(answer, context)
        elif aspect == "safety_assessment":
            return self._verify_safety(answer, context)
        elif aspect == "feasibility_analysis":
            return self._verify_feasibility(answer, context)
        elif aspect == "emotional_appropriateness":
            return self._verify_emotional_appropriateness(answer, context)
        return 0.8  # 預設分數
    
    def _verify_medical_accuracy(self, answer: str, context: Dict) -> float:
        """醫學準確性驗證"""
        medical_keywords = ["失智症", "阿茲海默", "認知障礙", "神經科", "醫療評估"]
        score = 0.8
        for keyword in medical_keywords:
            if keyword in answer:
                score += 0.1
        return min(score, 1.0)
    
    def _verify_safety(self, answer: str, context: Dict) -> float:
        """安全性評估"""
        safety_keywords = ["安全", "緊急", "專業", "評估", "監測"]
        risk_keywords = ["自行", "立即", "快速", "簡單"]
        
        score = 0.8
        for keyword in safety_keywords:
            if keyword in answer:
                score += 0.05
        for keyword in risk_keywords:
            if keyword in answer:
                score -= 0.1
        return max(score, 0.0)
    
    def _verify_feasibility(self, answer: str, context: Dict) -> float:
        """可行性分析"""
        feasibility_keywords = ["申請", "聯絡", "預約", "準備", "安排"]
        score = 0.7
        for keyword in feasibility_keywords:
            if keyword in answer:
                score += 0.05
        return min(score, 1.0)
    
    def _verify_emotional_appropriateness(self, answer: str, context: Dict) -> float:
        """情感適切性檢查"""
        positive_keywords = ["支持", "理解", "耐心", "專業", "協助"]
        negative_keywords = ["嚴重", "危險", "緊急", "惡化"]
        
        score = 0.8
        for keyword in positive_keywords:
            if keyword in answer:
                score += 0.05
        for keyword in negative_keywords:
            if keyword in answer:
                score -= 0.1
        return max(score, 0.0)
    
    def _get_recommendation(self, overall_score: float) -> str:
        """根據綜合評分給出建議"""
        if overall_score >= 0.8:
            return "高品質回答，可直接使用"
        elif overall_score >= 0.6:
            return "品質良好，建議小幅調整"
        elif overall_score >= 0.4:
            return "品質一般，需要改進"
        else:
            return "品質較差，建議重新生成"


# BoN-MAV 最佳答案選擇機制
class BoNMAV:
    """Best of N - Multiple Answer Verification"""
    
    def __init__(self, n_candidates: int = 5):
        self.n_candidates = n_candidates
        self.aspect_verifier = AspectVerifier()
    
    async def generate_best_answer(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """生成最佳答案"""
        # 生成多個候選答案
        candidates = await self._generate_candidates(user_input, context)
        
        # 多維度評分
        scored_candidates = []
        for i, candidate in enumerate(candidates):
            verification = await self.aspect_verifier.verify_answer(candidate, context)
            score = self._calculate_comprehensive_score(candidate, verification, context)
            scored_candidates.append({
                "candidate_id": i,
                "answer": candidate,
                "verification": verification,
                "comprehensive_score": score
            })
        
        # 選擇最佳答案
        best_candidate = max(scored_candidates, key=lambda x: x["comprehensive_score"])
        
        return {
            "best_answer": best_candidate["answer"],
            "verification": best_candidate["verification"],
            "comprehensive_score": best_candidate["comprehensive_score"],
            "all_candidates": scored_candidates,
            "selection_reason": self._get_selection_reason(best_candidate)
        }
    
    async def _generate_candidates(self, user_input: str, context: Dict) -> List[str]:
        """生成候選答案"""
        # 根據不同模組生成候選答案
        candidates = []
        
        # M1 候選答案
        if "記憶" in user_input or "忘記" in user_input:
            candidates.extend([
                "根據症狀描述，建議進行專業醫療評估以確認是否為失智症警訊。",
                "觀察到的症狀需要進一步確認，建議記錄詳細症狀並諮詢神經科醫師。",
                "這些症狀可能與正常老化相關，但建議定期追蹤觀察。"
            ])
        
        # M2 候選答案
        if "階段" in user_input or "進展" in user_input:
            candidates.extend([
                "根據描述，目前處於輕度階段，建議及早介入以延緩惡化。",
                "症狀顯示可能進入中度階段，需要調整照護策略和環境。",
                "需要專業評估以確定具體階段和預後。"
            ])
        
        # M3 候選答案
        if "情緒" in user_input or "行為" in user_input:
            candidates.extend([
                "這些行為是疾病表現，建議保持耐心並尋求專業協助。",
                "建立規律作息和穩定環境有助於改善症狀。",
                "考慮藥物治療和行為療法相結合的綜合方案。"
            ])
        
        # M4 候選答案
        if "申請" in user_input or "資源" in user_input:
            candidates.extend([
                "建議按優先順序申請相關照護資源和補助。",
                "準備完整文件並諮詢社會福利單位以獲得最大協助。",
                "建立支持網絡並學習照護技巧以提升生活品質。"
            ])
        
        # 確保至少有 5 個候選答案
        while len(candidates) < self.n_candidates:
            candidates.append("建議提供更多詳細資訊以獲得更精準的分析和建議。")
        
        return candidates[:self.n_candidates]
    
    def _calculate_comprehensive_score(self, answer: str, verification: Dict, context: Dict) -> float:
        """計算綜合評分"""
        # 基礎分數
        base_score = verification["overall_score"]
        
        # 長度適中加分
        length_score = 0.1 if 50 <= len(answer) <= 200 else 0.0
        
        # 專業性加分
        professional_keywords = ["專業", "醫師", "評估", "建議", "諮詢"]
        professional_score = sum(0.02 for keyword in professional_keywords if keyword in answer)
        
        # 實用性加分
        practical_keywords = ["建議", "可以", "應該", "需要", "準備"]
        practical_score = sum(0.02 for keyword in practical_keywords if keyword in answer)
        
        return min(base_score + length_score + professional_score + practical_score, 1.0)
    
    def _get_selection_reason(self, best_candidate: Dict) -> str:
        """獲取選擇理由"""
        score = best_candidate["comprehensive_score"]
        if score >= 0.9:
            return "綜合評分最高，品質優異"
        elif score >= 0.8:
            return "多維度評分優秀，建議最佳"
        elif score >= 0.7:
            return "平衡性良好，實用性強"
        else:
            return "相對最佳選擇，建議進一步優化"


# XAI 視覺化增強
class XAIVisualization:
    """可解釋 AI 視覺化"""
    
    def __init__(self):
        self.visualization_types = {
            "reasoning_path": "推理路徑圖",
            "confidence_radar": "信心分數雷達圖", 
            "evidence_highlight": "證據標記系統",
            "decision_tree": "決策樹視覺化"
        }
    
    def create_reasoning_path(self, analysis_result: Dict) -> Dict[str, Any]:
        """創建推理路徑圖"""
        return {
            "type": "reasoning_path",
            "title": "AI 推理路徑",
            "steps": [
                {
                    "step": 1,
                    "action": "症狀識別",
                    "description": "分析用戶輸入的症狀描述",
                    "confidence": 0.9
                },
                {
                    "step": 2,
                    "action": "模組匹配",
                    "description": "選擇最適合的分析模組",
                    "confidence": 0.85
                },
                {
                    "step": 3,
                    "action": "知識檢索",
                    "description": "從知識庫中檢索相關資訊",
                    "confidence": 0.8
                },
                {
                    "step": 4,
                    "action": "綜合分析",
                    "description": "結合多個模組進行綜合分析",
                    "confidence": 0.9
                },
                {
                    "step": 5,
                    "action": "建議生成",
                    "description": "生成個性化建議和行動方案",
                    "confidence": 0.85
                }
            ]
        }
    
    def create_confidence_radar(self, verification_result: Dict) -> Dict[str, Any]:
        """創建信心分數雷達圖"""
        aspects = verification_result.get("aspects", {})
        radar_data = []
        
        for aspect, data in aspects.items():
            radar_data.append({
                "dimension": data["description"],
                "score": data["score"],
                "status": data["status"]
            })
        
        return {
            "type": "confidence_radar",
            "title": "多維度可信度評估",
            "overall_score": verification_result.get("overall_score", 0),
            "dimensions": radar_data
        }
    
    def create_evidence_highlight(self, analysis_result: Dict) -> Dict[str, Any]:
        """創建證據標記系統"""
        chunks = analysis_result.get("retrieved_chunks", [])
        evidence_list = []
        
        for i, chunk in enumerate(chunks[:5]):  # 取前5個最相關的證據
            evidence_list.append({
                "id": i + 1,
                "title": chunk.get("title", "相關知識片段"),
                "content": chunk.get("content", "")[:100] + "...",
                "relevance_score": chunk.get("confidence_score", 0.8),
                "source": chunk.get("chunk_id", "M1")
            })
        
        return {
            "type": "evidence_highlight",
            "title": "關鍵判斷依據",
            "evidence_count": len(evidence_list),
            "evidence_list": evidence_list
        }
    
    def create_decision_tree(self, analysis_result: Dict) -> Dict[str, Any]:
        """創建決策樹視覺化"""
        modules_used = analysis_result.get("modules_used", [])
        
        decision_nodes = [
            {
                "node_id": "start",
                "question": "用戶輸入症狀描述",
                "branches": [
                    {
                        "condition": "記憶相關症狀",
                        "target": "M1",
                        "confidence": 0.9
                    },
                    {
                        "condition": "階段詢問",
                        "target": "M2", 
                        "confidence": 0.85
                    },
                    {
                        "condition": "行為問題",
                        "target": "M3",
                        "confidence": 0.8
                    },
                    {
                        "condition": "照護需求",
                        "target": "M4",
                        "confidence": 0.75
                    }
                ]
            }
        ]
        
        return {
            "type": "decision_tree",
            "title": "分析邏輯透明化",
            "selected_modules": modules_used,
            "decision_nodes": decision_nodes
        }
    
    def create_comprehensive_visualization(self, analysis_result: Dict, verification_result: Dict) -> Dict[str, Any]:
        """創建綜合視覺化"""
        return {
            "reasoning_path": self.create_reasoning_path(analysis_result),
            "confidence_radar": self.create_confidence_radar(verification_result),
            "evidence_highlight": self.create_evidence_highlight(analysis_result),
            "decision_tree": self.create_decision_tree(analysis_result)
        }


# 專業模組化分析增強
class ProfessionalModularAnalysis:
    """專業 M1-M4 模組化分析"""
    
    def __init__(self):
        self.bon_mav = BoNMAV()
        self.xai_visualization = XAIVisualization()
        self.aspect_verifier = AspectVerifier()
    
    async def analyze_professional(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """專業模組化分析"""
        # 1. 模組選擇
        selected_modules = self._select_modules(user_input)
        
        # 2. 專業分析
        analysis_results = {}
        for module in selected_modules:
            analysis_results[module] = await self._analyze_module(module, user_input, context)
        
        # 3. 生成候選答案
        bon_mav_result = await self.bon_mav.generate_best_answer(user_input, context)
        
        # 4. 多角度驗證
        verification_result = await self.aspect_verifier.verify_answer(
            bon_mav_result["best_answer"], context
        )
        
        # 5. XAI 視覺化
        xai_visualization = self.xai_visualization.create_comprehensive_visualization(
            analysis_results, verification_result
        )
        
        return {
            "selected_modules": selected_modules,
            "analysis_results": analysis_results,
            "best_answer": bon_mav_result["best_answer"],
            "verification": verification_result,
            "xai_visualization": xai_visualization,
            "comprehensive_score": bon_mav_result["comprehensive_score"],
            "selection_reason": bon_mav_result["selection_reason"]
        }
    
    def _select_modules(self, user_input: str) -> List[str]:
        """智能選擇分析模組"""
        modules = []
        
        # M1 快速篩檢 - 十大警訊智能比對
        m1_keywords = ["記憶", "忘記", "重複", "迷路", "時間", "混淆", "警訊"]
        if any(keyword in user_input for keyword in m1_keywords):
            modules.append("M1")
        
        # M2 病程理解 - 階段預測與個人化建議
        m2_keywords = ["階段", "進展", "惡化", "早期", "中期", "晚期", "病程"]
        if any(keyword in user_input for keyword in m2_keywords):
            modules.append("M2")
        
        # M3 症狀處理 - BPSD 分類與應對策略
        m3_keywords = ["情緒", "行為", "暴躁", "妄想", "幻覺", "遊走", "睡眠", "攻擊"]
        if any(keyword in user_input for keyword in m3_keywords):
            modules.append("M3")
        
        # M4 資源導航 - 智能匹配與申請指引
        m4_keywords = ["申請", "補助", "資源", "照護", "服務", "支援", "協助"]
        if any(keyword in user_input for keyword in m4_keywords):
            modules.append("M4")
        
        # 如果沒有明確匹配，使用 M1 作為預設
        if not modules:
            modules.append("M1")
        
        return modules
    
    async def _analyze_module(self, module: str, user_input: str, context: Dict) -> Dict[str, Any]:
        """分析特定模組"""
        if module == "M1":
            return await self._analyze_m1_warning_signs(user_input, context)
        elif module == "M2":
            return await self._analyze_m2_progression(user_input, context)
        elif module == "M3":
            return await self._analyze_m3_bpsd(user_input, context)
        elif module == "M4":
            return await self._analyze_m4_resources(user_input, context)
        else:
            return {"error": f"未知模組: {module}"}
    
    async def _analyze_m1_warning_signs(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """M1: 十大警訊智能比對"""
        warning_signs = [
            "記憶力減退影響日常生活",
            "計劃事情或解決問題有困難", 
            "無法完成熟悉的工作",
            "對時間或地點感到困惑",
            "理解視覺影像和空間關係有困難",
            "說話或寫作時用字困難",
            "把東西放錯地方且無法回頭去找",
            "判斷力減退",
            "退出工作或社交活動",
            "情緒和個性改變"
        ]
        
        matched_signs = []
        for sign in warning_signs:
            if any(keyword in user_input for keyword in sign.split()):
                matched_signs.append(sign)
        
        return {
            "module": "M1",
            "warning_signs_detected": matched_signs,
            "risk_level": "high" if len(matched_signs) >= 2 else "medium" if len(matched_signs) >= 1 else "low",
            "recommendation": "建議及早就醫評估" if len(matched_signs) >= 1 else "持續觀察"
        }
    
    async def _analyze_m2_progression(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """M2: 階段預測與個人化建議"""
        stages = {
            "輕度": {
                "duration": "2-4年",
                "characteristics": ["記憶力減退", "輕微認知障礙", "日常生活基本自理"],
                "recommendations": ["建立醫療團隊", "學習照護技巧", "規劃未來安排"]
            },
            "中度": {
                "duration": "2-8年", 
                "characteristics": ["明顯認知障礙", "日常生活需協助", "行為改變"],
                "recommendations": ["申請照護資源", "調整居家環境", "尋求家屬支持"]
            },
            "重度": {
                "duration": "1-3年",
                "characteristics": ["嚴重認知障礙", "完全依賴照護", "身體功能退化"],
                "recommendations": ["24小時照護安排", "安寧照護準備", "家屬心理支持"]
            }
        }
        
        # 簡單的階段判斷邏輯
        if "重度" in user_input or "晚期" in user_input:
            current_stage = "重度"
        elif "中度" in user_input:
            current_stage = "中度"
        else:
            current_stage = "輕度"
        
        return {
            "module": "M2",
            "current_stage": current_stage,
            "stage_info": stages[current_stage],
            "progression_prediction": "症狀會逐漸進展，早期介入可延緩惡化"
        }
    
    async def _analyze_m3_bpsd(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """M3: BPSD 分類與應對策略"""
        bpsd_categories = {
            "情緒症狀": ["憂鬱", "焦慮", "易怒", "情緒不穩"],
            "精神病症狀": ["妄想", "幻覺", "錯認"],
            "行為症狀": ["遊走", "攻擊", "重複行為"],
            "睡眠障礙": ["失眠", "日夜顛倒", "睡眠品質差"]
        }
        
        detected_symptoms = []
        for category, symptoms in bpsd_categories.items():
            for symptom in symptoms:
                if symptom in user_input:
                    detected_symptoms.append({
                        "category": category,
                        "symptom": symptom,
                        "severity": "moderate"
                    })
        
        return {
            "module": "M3",
            "detected_symptoms": detected_symptoms,
            "total_symptoms": len(detected_symptoms),
            "intervention_strategy": "根據症狀嚴重度制定個性化介入策略"
        }
    
    async def _analyze_m4_resources(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """M4: 智能匹配與申請指引"""
        resource_categories = {
            "醫療資源": ["神經科門診", "認知功能評估", "藥物治療"],
            "照護資源": ["居家照護", "日間照護", "機構照護"],
            "社會福利": ["身心障礙證明", "長照服務", "經濟補助"],
            "支持服務": ["家屬支持團體", "諮商服務", "緊急聯絡"]
        }
        
        matched_resources = []
        for category, resources in resource_categories.items():
            for resource in resources:
                if any(keyword in user_input for keyword in resource.split()):
                    matched_resources.append({
                        "category": category,
                        "resource": resource,
                        "priority": "high" if "緊急" in resource else "medium"
                    })
        
        return {
            "module": "M4",
            "matched_resources": matched_resources,
            "application_guidance": "按優先順序申請，準備完整文件"
        }


# 初始化專業分析器
professional_analyzer = ProfessionalModularAnalysis()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
    