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


def create_smart_flex_message(user_input: str, analysis_result: Any) -> Dict:
    """智能創建適合的 Flex Message，根據用戶問題選配視覺模組"""
    
    # 提取分析結果
    if isinstance(analysis_result, dict):
        summary = analysis_result.get('comprehensive_summary', '分析完成')
        symptom_titles = analysis_result.get('symptom_titles', [])
        matched_codes = analysis_result.get('matched_codes', [])
        stage_detection = analysis_result.get('stage_detection', {})
    else:
        summary = getattr(analysis_result, 'comprehensive_summary', '分析完成')
        symptom_titles = getattr(analysis_result, 'symptom_titles', [])
        matched_codes = getattr(analysis_result, 'matched_codes', [])
        stage_detection = getattr(analysis_result, 'stage_detection', {})
    
    # 根據用戶輸入選擇適合的視覺模組
    user_input_lower = user_input.lower()
    
    # 分析用戶意圖 - 更精確的關鍵字判斷
    if any(word in user_input_lower for word in ['記憶', '忘記', '重複', '記不住', '記性']):
        component_type = "warning_sign"
        title = "記憶力警訊分析"
        color_theme = "warning"
        logger.info(f"[DEBUG] 選擇模組：記憶力警訊分析 (關鍵字: {[word for word in ['記憶', '忘記', '重複', '記不住', '記性'] if word in user_input_lower]})")
    elif any(word in user_input_lower for word in ['階段', '程度', '嚴重', '輕度', '中度', '重度']):
        component_type = "stage_description"
        title = "病程階段評估"
        color_theme = "info"
        logger.info(f"[DEBUG] 選擇模組：病程階段評估 (關鍵字: {[word for word in ['階段', '程度', '嚴重', '輕度', '中度', '重度'] if word in user_input_lower]})")
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
            {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
        ]
    elif component_type == "coping_strategy":
        body_contents = [
            {"type": "text", "text": "💡 照護建議：保持耐心、建立規律作息、善用輔助工具，並多與醫療團隊溝通。", "weight": "bold", "size": "md", "color": "#5cb85c", "wrap": True},
            {"type": "separator", "margin": "md"},
            {"type": "text", "text": f"📝 用戶描述：{user_input}", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
        ]
    elif component_type == "stage_description":
        body_contents = [
            {"type": "text", "text": "📊 病程階段評估：根據描述，可能處於失智症的某個階段，建議諮詢專業醫師。", "weight": "bold", "size": "md", "color": "#5bc0de", "wrap": True},
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
    
    # 添加症狀分析（如果有）
    if symptom_titles:
        symptom_contents = []
        for i, title in enumerate(symptom_titles[:2]):
            code = matched_codes[i] if i < len(matched_codes) else f"M1-{i+1:02d}"
            symptom_contents.append({
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
                        "text": f"代碼：{code} | 信心：MEDIUM",
                        "size": "xs",
                        "weight": "regular",
                        "color": "#dc3545",
                        "margin": "xs"
                    }
                ]
            })
        
        # 將症狀分析插入到 body 中
        flex_message["contents"]["body"]["contents"].extend(symptom_contents)
    
    # 添加階段分析（如果有）
    if stage_detection:
        stage_content = {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "📊 綜合評估",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#4ECDC4"
                },
                {
                    "type": "text",
                    "text": f"評估為{stage_detection.get('detected_stage', '')}階段，建議尋求專業醫療評估。",
                    "size": "sm",
                    "weight": "regular",
                    "wrap": True,
                    "margin": "xs"
                }
            ]
        }
        flex_message["contents"]["body"]["contents"].append(stage_content)
    
    # 確保 body 至少有基本內容
    if not flex_message["contents"]["body"]["contents"]:
        flex_message["contents"]["body"]["contents"].append({
            "type": "text",
            "text": "分析完成，請提供更多詳細資訊以獲得更好的建議。",
            "wrap": True,
            "margin": "md",
            "size": "sm",
            "weight": "regular",
            "color": "#666666"
        })
    
    return flex_message


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
            
            # 智能創建適合的 Flex Message
            logger.info("[DEBUG] 開始智能創建 Flex Message...")
            try:
                flex_message = create_smart_flex_message(user_input, result)
                logger.info("[DEBUG] 智能 Flex Message 創建成功")
                logger.info(f"[DEBUG] Flex Message altText: {flex_message['altText']}")
                logger.info(f"[DEBUG] Flex Message type: {flex_message['type']}")
                
            except Exception as flex_error:
                logger.warning(f"[DEBUG] 智能 Flex Message 創建失敗: {flex_error}")
                # 回退到簡單的 Flex Message
                flex_message = {
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
                                    "text": "分析完成，請提供更多詳細資訊以獲得更好的建議。",
                                    "wrap": True,
                                    "margin": "md",
                                    "size": "sm",
                                    "color": "#666666"
                                }
                            ]
                        }
                    }
                }
            
            logger.info("[DEBUG] Flex Message 創建完成，準備發送...")
            
            # 回覆 Flex Message
            try:
                logger.info("[DEBUG] 準備發送 Flex Message")
                logger.info(f"[DEBUG] Flex Message 類型: {type(flex_message)}")
                logger.info(f"[DEBUG] Flex Message altText: '{flex_message.get('altText', 'N/A')}'")
                logger.info(f"[DEBUG] Flex Message contents 類型: {type(flex_message.get('contents', 'N/A'))}")
                
                # 確保 altText 不為空且沒有前導空格
                if flex_message.get('altText'):
                    flex_message['altText'] = flex_message['altText'].strip()
                    # 移除所有多餘空格
                    flex_message['altText'] = ' '.join(flex_message['altText'].split())
                else:
                    flex_message['altText'] = "失智症分析結果"
                
                # 確保 contents 不為空
                if not flex_message.get('contents'):
                    logger.error("[DEBUG] Flex Message contents 為空")
                    raise Exception("Flex Message contents is empty")
                
                # 最終檢查
                logger.info(f"[DEBUG] 最終 altText: '{flex_message['altText']}'")
                logger.info(f"[DEBUG] 最終 contents 鍵: {list(flex_message['contents'].keys()) if isinstance(flex_message['contents'], dict) else '不是字典'}")
                
                # 檢查 reply token 是否有效
                if not event.reply_token or event.reply_token == "00000000000000000000000000000000":
                    logger.error("[DEBUG] Reply token 無效或過期")
                    return
                
                # 將 Flex Message 字典轉換為 SDK 對象
                from linebot.v3.messaging.models import FlexMessage, FlexBubble, FlexBox, FlexText, FlexButton, MessageAction, FlexSeparator

                def dict_to_flex_component(component):
                    if component['type'] == 'text':
                        return FlexText(
                            text=component['text'],
                            weight=component.get('weight', 'regular'),
                            size=component.get('size', 'md'),
                            color=component.get('color', '#000000'),
                            wrap=component.get('wrap', False),
                            margin=component.get('margin', None)
                        )
                    elif component['type'] == 'box':
                        return FlexBox(
                            layout=component['layout'],
                            contents=[dict_to_flex_component(c) for c in component['contents']],
                            margin=component.get('margin', None)
                        )
                    elif component['type'] == 'button':
                        action = component['action']
                        return FlexButton(
                            style=component.get('style', 'link'),
                            height=component.get('height', 'sm'),
                            action=MessageAction(
                                label=action['label'],
                                text=action['text']
                            ),
                            flex=component.get('flex', 0)
                        )
                    elif component['type'] == 'separator':
                        return FlexSeparator(margin=component.get('margin', None))
                    else:
                        raise ValueError(f"Unknown component type: {component['type']}")

                header = flex_message['contents'].get('header')
                body = flex_message['contents'].get('body')
                footer = flex_message['contents'].get('footer')

                bubble = FlexBubble(
                    size=flex_message['contents'].get('size', 'kilo'),
                    header=dict_to_flex_component(header) if header else None,
                    body=dict_to_flex_component(body) if body else None,
                    footer=dict_to_flex_component(footer) if footer else None
                )
                line_flex_message = FlexMessage(
                    alt_text=flex_message['altText'],
                    contents=bubble
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[line_flex_message]
                    )
                )
                logger.info(f"✅ 已回覆用戶 {user_id} Flex Message (SDK 對象)")
                
            except Exception as api_error:
                logger.error(f"❌ LINE API 連線錯誤: {api_error}")
                logger.error(f"❌ 錯誤詳情: {type(api_error).__name__}: {str(api_error)}")
                
                # 如果 Flex Message 失敗，嘗試發送純文字
                try:
                    # 檢查 reply token 是否仍然有效
                    if not event.reply_token or event.reply_token == "00000000000000000000000000000000":
                        logger.error("[DEBUG] Reply token 已過期，無法發送純文字回覆")
                        return
                    
                    # 提取摘要用於純文字回覆
                    if isinstance(result, dict):
                        summary = result.get('comprehensive_summary', '分析完成')
                    else:
                        summary = getattr(result, 'comprehensive_summary', '分析完成')
                    
                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text=summary)]
                        )
                    )
                    logger.info(f"✅ 已回覆用戶 {user_id} 純文字訊息（備用方案）")
                except Exception as text_error:
                    logger.error(f"❌ 純文字回覆也失敗: {text_error}")
                    # 如果連純文字都失敗，可能是 reply token 過期
                    if "Invalid reply token" in str(text_error):
                        logger.error("[DEBUG] Reply token 已過期，無法回覆用戶")
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
                # 修復屬性訪問錯誤
                total_chunks = len(getattr(integrated_engine, 'all_chunks', []))
                m1_chunks = len(getattr(integrated_engine, 'm1_chunks', []))
                m2_chunks = len(getattr(integrated_engine, 'm2_chunks', []))
                m3_chunks = len(getattr(integrated_engine, 'm3_chunks', []))
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
            "M1": "active" if integrated_engine and hasattr(integrated_engine, 'm1_chunks') and integrated_engine.m1_chunks else "inactive",
            "M2": "active" if integrated_engine and hasattr(integrated_engine, 'm2_chunks') and integrated_engine.m2_chunks else "inactive",
            "M3": "active" if integrated_engine and hasattr(integrated_engine, 'm3_chunks') and integrated_engine.m3_chunks else "inactive"
        }

        # 檢查優化狀態
        optimizations = {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "cache_stats": cache_manager.get_cache_stats() if cache_manager else {"status": "unavailable"},
            "gemini_stats": optimized_gemini.get_usage_stats() if optimized_gemini else {"status": "unavailable"},
            "cost_optimization": {
                "cache_hit_rate": 0.0,  # 簡化，避免方法不存在
                "estimated_savings": 0.0,  # 簡化，避免方法不存在
                "total_cost": 0.0  # 簡化，避免方法不存在
            }
        }

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "engine_info": engine_info,
            "modules_status": modules_status,
            "optimizations": optimizations
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


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
        return cache_manager.get_stats()
    return {"status": "unavailable"}


@app.get("/gemini/stats")
def get_gemini_stats():
    """獲取 Gemini 統計"""
    if optimized_gemini:
        return optimized_gemini.get_stats()
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
        # 創建測試 Flex Message
        test_flex = create_smart_flex_message(request.user_input, {
            'comprehensive_summary': '測試分析結果',
            'symptom_titles': ['記憶力減退'],
            'matched_codes': ['M1-01'],
            'stage_detection': {'detected_stage': '輕度'}
        })
        
        # 詳細調試信息
        debug_info = {
            "original_flex": test_flex,
            "altText": test_flex.get('altText'),
            "altText_length": len(test_flex.get('altText', '')),
            "altText_stripped": test_flex.get('altText', '').strip(),
            "contents_type": type(test_flex.get('contents')),
            "contents_keys": list(test_flex.get('contents', {}).keys()) if isinstance(test_flex.get('contents'), dict) else 'not_dict',
            "flex_type": test_flex.get('type'),
            "user_input": request.user_input
        }
        
        # 測試 LINE Bot SDK 對象創建
        try:
            from linebot.v3.messaging.models import FlexMessage
            line_flex = FlexMessage(
                alt_text=test_flex['altText'],
                contents=test_flex['contents']
            )
            debug_info["sdk_object_created"] = True
            debug_info["sdk_alt_text"] = line_flex.alt_text
            debug_info["sdk_contents_type"] = type(line_flex.contents)
        except Exception as sdk_error:
            debug_info["sdk_object_created"] = False
            debug_info["sdk_error"] = str(sdk_error)
        
        return {
            "status": "success",
            "debug_info": debug_info,
            "test_flex_message": test_flex
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
    