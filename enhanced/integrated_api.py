# enhanced/integrated_api.py
"""
整合版 M1 API - 結合 RAG 引擎與現有 MVP 系統
完全向後相容，增強功能
"""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import os
from datetime import datetime
import json

# 導入我們的輕量級 RAG 引擎
from lightweight_rag_for_replit import LightweightRAGEngine

# ===== 資料模型定義 =====

class UserInput(BaseModel):
    user_input: str
    analysis_mode: str = "enhanced"  # "enhanced" 或 "classic"
    return_format: str = "flex"      # "flex" 或 "json"

class AnalysisResponse(BaseModel):
    flex_message: Dict
    analysis_data: Dict
    enhanced: bool
    timestamp: str
    rag_info: Optional[Dict] = None

# ===== FastAPI 應用程式 =====

app = FastAPI(
    title="Enhanced M1 RAG API",
    description="整合 RAG 的失智症警訊分析系統",
    version="2.0.0"
)

# 全域變數
rag_engine = None

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時初始化 RAG 引擎"""
    global rag_engine

    api_key = os.getenv('AISTUDIO_API_KEY')
    if not api_key:
        print("⚠️  未設定 AISTUDIO_API_KEY，將使用規則分析")

    try:
        rag_engine = LightweightRAGEngine(api_key)
        print("✅ Enhanced M1 RAG API 啟動成功")
    except Exception as e:
        print(f"❌ RAG 引擎初始化失敗：{e}")
        rag_engine = None

# ===== 保持向後相容的原有端點 =====

@app.post("/m1-flex")
async def m1_flex_enhanced(request: UserInput):
    """
    增強版 M1 Flex API
    保持與現有 LINE Bot 的完全相容性
    """
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG 引擎未初始化")

    try:
        # 使用增強版 RAG 分析
        analysis_result = rag_engine.analyze_with_lightweight_rag(request.user_input)

        # 生成增強版 Flex Message
        flex_message = generate_enhanced_flex_message(analysis_result)

        # 組裝回應（保持原有格式）
        response = {
            "flex_message": flex_message,
            "analysis_data": analysis_result,
            "enhanced": True,
            "timestamp": datetime.now().isoformat(),
            "rag_info": {
                "chunks_used": analysis_result.get("total_chunks_used", 0),
                "analysis_method": analysis_result.get("analysis_method", "unknown"),
                "top_similarity": analysis_result.get("similarity_scores", [0])[0] if analysis_result.get("similarity_scores") else 0
            }
        }

        return response

    except Exception as e:
        print(f"分析錯誤: {e}")
        return generate_error_flex_message(str(e))

# ===== 新增的增強功能端點 =====

@app.post("/api/v1/analyze")
async def enhanced_analyze(request: UserInput):
    """
    新的統一分析端點
    提供更詳細的分析結果
    """
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG 引擎未初始化")

    try:
        # RAG 分析
        analysis_result = rag_engine.analyze_with_lightweight_rag(request.user_input)

        # 檢索詳情
        retrieved_chunks = analysis_result.get("retrieved_chunks", [])

        return {
            "analysis": analysis_result,
            "retrieved_chunks": retrieved_chunks,
            "query": request.user_input,
            "analysis_mode": request.analysis_mode,
            "timestamp": datetime.now().isoformat(),
            "engine_info": {
                "type": "lightweight_rag",
                "version": "2.0.0",
                "chunks_available": len(rag_engine.chunks),
                "vocabulary_size": len(rag_engine.vocabulary)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

@app.get("/api/v1/search")
async def search_only(q: str, k: int = 3):
    """
    純檢索端點
    只做檢索，不做 AI 分析
    """
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG 引擎未初始化")

    try:
        chunks = rag_engine.retrieve_relevant_chunks(q, k=k)

        return {
            "query": q,
            "chunks": chunks,
            "total_results": len(chunks),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"檢索失敗：{str(e)}")

# ===== Flex Message 生成器（增強版） =====

def generate_enhanced_flex_message(analysis_data: Dict) -> Dict:
    """
    生成增強版 Flex Message
    基於你現有的設計，加入 RAG 資訊
    """

    # 提取分析結果
    warning_code = analysis_data.get("matched_warning_code", "M1-GENERAL")
    symptom_title = analysis_data.get("symptom_title", "需要關注的症狀")
    user_behavior = analysis_data.get("user_behavior_summary", "描述的情況")
    normal_behavior = analysis_data.get("normal_behavior", "正常老化的表現")
    dementia_indicator = analysis_data.get("dementia_indicator", "需要注意的警訊")
    action_suggestion = analysis_data.get("action_suggestion", "建議諮詢專業人員")
    confidence = analysis_data.get("confidence_level", "medium")

    # RAG 增強資訊
    chunks_used = analysis_data.get("total_chunks_used", 0)
    analysis_method = analysis_data.get("analysis_method", "rule_based")
    similarity_scores = analysis_data.get("similarity_scores", [])
    top_similarity = similarity_scores[0] if similarity_scores else 0

    # 信心程度顏色
    confidence_colors = {
        "high": "#28a745",    # 綠色
        "medium": "#ffc107",  # 黃色
        "low": "#dc3545"      # 紅色
    }
    confidence_color = confidence_colors.get(confidence, "#6c757d")

    # 生成 Flex Message（保持你的設計風格）
    flex_message = {
        "type": "flex",
        "altText": f"失智症警訊分析：{symptom_title}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症警訊分析",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#ffffff"
                    },
                    {
                        "type": "text",
                        "text": warning_code,
                        "size": "sm",
                        "color": "#ffffff",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": "#005073",
                "paddingAll": "15dp"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # 症狀標題
                    {
                        "type": "text",
                        "text": symptom_title,
                        "weight": "bold",
                        "size": "md",
                        "color": "#005073",
                        "wrap": True
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },

                    # 使用者描述
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📝 您的描述",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": user_behavior,
                                "size": "sm",
                                "wrap": True,
                                "margin": "xs"
                            }
                        ]
                    },

                    # 正常 vs 警訊對比
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✅ 正常老化",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#28a745"
                            },
                            {
                                "type": "text",
                                "text": normal_behavior,
                                "size": "xs",
                                "wrap": True,
                                "margin": "xs",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "⚠️ 失智警訊",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#dc3545",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": dementia_indicator,
                                "size": "xs",
                                "wrap": True,
                                "margin": "xs",
                                "color": "#666666"
                            }
                        ]
                    },

                    # RAG 增強資訊（新增特色）
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔍 AI 分析資訊",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#666666"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"信心: {confidence.upper()}",
                                        "size": "xs",
                                        "color": confidence_color,
                                        "weight": "bold",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": f"資料: {chunks_used}項",
                                        "size": "xs",
                                        "color": "#666666",
                                        "align": "end",
                                        "flex": 1
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "xs",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"方法: {analysis_method}",
                                        "size": "xs",
                                        "color": "#666666",
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": f"匹配: {top_similarity:.2f}",
                                        "size": "xs",
                                        "color": "#666666",
                                        "align": "end",
                                        "flex": 1
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "paddingAll": "15dp"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
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
                        "text": action_suggestion,
                        "size": "xs",
                        "wrap": True,
                        "margin": "xs",
                        "color": "#666666"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "了解更多",
                                    "text": f"請告訴我更多關於{symptom_title}的資訊"
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
                        ]
                    }
                ],
                "paddingAll": "15dp"
            }
        }
    }

    return flex_message

def generate_error_flex_message(error_message: str) -> Dict:
    """生成錯誤回應的 Flex Message"""
    return {
        "flex_message": {
            "type": "flex",
            "altText": "系統暫時無法分析",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "😅 系統暫時無法分析",
                            "weight": "bold",
                            "size": "md",
                            "color": "#dc3545"
                        },
                        {
                            "type": "text",
                            "text": "請稍後再試，或直接諮詢專業醫療人員。",
                            "size": "sm",
                            "wrap": True,
                            "margin": "md",
                            "color": "#666666"
                        }
                    ]
                }
            }
        },
        "analysis_data": {
            "error": error_message,
            "matched_warning_code": "ERROR",
            "symptom_title": "系統錯誤"
        },
        "enhanced": False,
        "timestamp": datetime.now().isoformat()
    }

# ===== 健康檢查與監控 =====

@app.get("/health")
async def health_check():
    """系統健康檢查"""
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG 引擎未初始化")

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "rag_engine": "ready",
            "chunks_loaded": len(rag_engine.chunks),
            "vocabulary_size": len(rag_engine.vocabulary),
            "gemini_available": rag_engine.gemini_available
        },
        "endpoints": {
            "classic_compatible": "/m1-flex",
            "enhanced_analysis": "/api/v1/analyze",
            "search_only": "/api/v1/search"
        },
        "version": "2.0.0"
    }

@app.get("/api/v1/test")
async def test_system():
    """系統測試端點"""
    if not rag_engine:
        raise HTTPException(status_code=503, detail="RAG 引擎未初始化")

    test_input = "媽媽常忘記關瓦斯"

    try:
        # 測試完整分析流程
        result = rag_engine.analyze_with_lightweight_rag(test_input)

        return {
            "test_input": test_input,
            "analysis_success": True,
            "warning_code": result.get("matched_warning_code"),
            "confidence": result.get("confidence_level"),
            "chunks_used": result.get("total_chunks_used", 0),
            "analysis_method": result.get("analysis_method"),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "test_input": test_input,
            "analysis_success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# ===== 主程式執行 =====

if __name__ == "__main__":
    print("🚀 啟動增強版 M1 RAG API 伺服器...")
    print("📋 功能特色：")
    print("   ✅ 100% 向後相容原有 /m1-flex API")
    print("   ✅ 新增 RAG 增強分析功能")
    print("   ✅ 智能檢索與相似度匹配")
    print("   ✅ 增強版 Flex Message 顯示")
    print("   ✅ 完整的系統監控")

    print(f"\n📖 API 文件: http://localhost:8002/docs")
    print(f"🔍 健康檢查: http://localhost:8002/health")
    print(f"🧪 系統測試: http://localhost:8002/api/v1/test")

    # 檢查環境
    if not os.getenv('AISTUDIO_API_KEY'):
        print("\n⚠️  提醒：未設定 AISTUDIO_API_KEY，將使用規則分析")
        print("   可以正常運作，但 AI 分析功能會受限")

    # 啟動服務（使用新的 port 8002 避免衝突）
    uvicorn.run(
        "integrated_api:app",
        host="0.0.0.0",
        port=8002,  # 新 port，與現有服務並行
        reload=True,
        log_level="info"
    )