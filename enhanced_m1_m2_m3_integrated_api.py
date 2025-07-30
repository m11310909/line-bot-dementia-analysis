#!/usr/bin/env python3
"""
增強版 M1+M2+M3 整合 API
整合 Redis 快取和優化 Gemini API
"""

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

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

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 應用
app = FastAPI(
    title="增強版 M1+M2+M3 整合 RAG API",
    description="支援失智症警訊(M1) + 病程階段(M2) + BPSD行為心理症狀(M3) + Redis快取 + 優化Gemini",
    version="4.0.0"
)

# 全域引擎和優化組件
integrated_engine = None
cache_manager = None
optimized_gemini = None

@app.on_event("startup")
async def startup():
    global integrated_engine, cache_manager, optimized_gemini
    print("🚀 啟動增強版 M1+M2+M3 整合引擎...")

    api_key = os.getenv('AISTUDIO_API_KEY')

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
            "💰 Gemini API 成本優化"
        ],
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "optimized_gemini": optimized_gemini is not None,
            "cache_stats": cache_manager.get_cache_stats() if cache_manager else None
        },
        "total_chunks": len(integrated_engine.chunks) if integrated_engine else 0
    }

@app.get("/health")
def health():
    if not integrated_engine:
        return {"status": "error", "message": "引擎未初始化"}

    # 統計模組分布
    m1_chunks = [c for c in integrated_engine.chunks if c.get("chunk_id", "").startswith("M1")]
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
            "vocabulary_size": len(integrated_engine.vocabulary)
        },
        "modules_status": {
            "M1": "active" if m1_chunks else "inactive",
            "M2": "active" if m2_chunks else "inactive", 
            "M3": "active" if m3_chunks else "inactive"
        },
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "cache_stats": cache_stats,
            "gemini_stats": gemini_stats
        }
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
                return {
                    **cached_result,
                    "cached": True,
                    "optimized": True
                }

        # 使用整合引擎進行綜合分析
        result = integrated_engine.analyze_comprehensive(user_input)
        
        # 將結果轉換為字典格式
        if hasattr(result, '__dict__'):
            result_dict = result.__dict__
        else:
            result_dict = result
        
        # 快取結果
        if cache_manager:
            cache_manager.cache_analysis_result(user_input, result_dict)
            logger.info("💾 分析結果已快取")

        return {
            **result_dict,
            "cached": False,
            "optimized": True,
            "cache_available": cache_manager.is_available() if cache_manager else False
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
                return {
                    "flex_message": cached_flex,
                    "cached": True,
                    "optimized": True
                }

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
            "cache_available": cache_manager.is_available() if cache_manager else False
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
                        "text": main_title,
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
                                "wrap": True,
                                "margin": "xs"
                            }
                        ]
                    }
                ],
                "paddingAll": "15dp"
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
                            "text": "請詳細說明相關資訊"
                        },
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "uri",
                            "label": "專業諮詢",
                            "uri": "https://www.tada2002.org.tw/"
                        },
                        "flex": 1,
                        "margin": "sm"
                    }
                ],
                "paddingAll": "15dp"
            }
        }
    }
    
    # 添加分析結果到 body
    body_contents = flex_message["contents"]["body"]["contents"]
    
    # 添加檢測到的症狀
    for i, (code, title, confidence) in enumerate(zip(matched_codes, symptom_titles, confidence_levels)):
        confidence_color = "#dc3545" if confidence == "low" else "#28a745"
        body_contents.append({
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
                    "text": f"代碼：{code} | 信心：{confidence.upper()}",
                    "size": "xs",
                    "color": confidence_color,
                    "margin": "xs"
                }
            ]
        })
    
    # 添加綜合評估
    body_contents.append({
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "contents": [
            {
                "type": "text",
                "text": "📊 綜合評估",
                "weight": "bold",
                "size": "sm",
                "color": "#005073"
            },
            {
                "type": "text",
                "text": comprehensive_summary,
                "size": "xs",
                "wrap": True,
                "margin": "xs",
                "color": "#666666"
            }
        ]
    })
    
    # 添加建議行動
    if action_suggestions:
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "💡 建議行動",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#005073"
                },
                {
                    "type": "text",
                    "text": "；".join(action_suggestions),
                    "size": "xs",
                    "wrap": True,
                    "margin": "xs",
                    "color": "#666666"
                }
            ]
        })
    
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
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#dc3545",
                "paddingAll": "15dp"
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
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": "請稍後再試或聯繫客服",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md"
                    }
                ],
                "paddingAll": "15dp"
            }
        }
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
    m1_chunks = [c for c in integrated_engine.chunks if c.get("chunk_id", "").startswith("M1")]
    m2_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M2"]
    m3_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M3"]
    
    return {
        "modules": {
            "M1": {
                "status": "active" if m1_chunks else "inactive",
                "chunks_count": len(m1_chunks),
                "description": "失智症警訊檢測"
            },
            "M2": {
                "status": "active" if m2_chunks else "inactive",
                "chunks_count": len(m2_chunks),
                "description": "病程階段分析"
            },
            "M3": {
                "status": "active" if m3_chunks else "inactive",
                "chunks_count": len(m3_chunks),
                "description": "BPSD 行為心理症狀"
            }
        },
        "optimizations": {
            "redis_cache": cache_manager.is_available() if cache_manager else False,
            "optimized_gemini": optimized_gemini is not None
        },
        "total_chunks": len(integrated_engine.chunks)
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