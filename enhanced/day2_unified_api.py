    # day2_unified_api.py
    """
    Day 2: 統一 API 與完整系統整合
    保留現有 LINE Bot + M1 Flex API，加入 RAG 增強功能
    """

    from fastapi import FastAPI, HTTPException, Request
    from pydantic import BaseModel
    from typing import Dict, List, Optional
    import uvicorn
    import os
    from datetime import datetime
    import json

    # 導入 Day 1 的增強引擎
    from day1_m1_rag_integration import EnhancedM1RAGEngine

    # ===== Pydantic 模型定義 =====

    class UserInput(BaseModel):
        user_input: str
        analysis_mode: str = "enhanced"  # "enhanced" 或 "classic"
        return_format: str = "flex"      # "flex" 或 "json"

    class RAGQuery(BaseModel):
        query: str
        module_filter: Optional[str] = "M1"
        k: int = 3

    class FlexMessageResponse(BaseModel):
        flex_message: Dict
        analysis_data: Dict
        metadata: Dict

    # ===== FastAPI 應用程式初始化 =====

    app = FastAPI(
        title="Enhanced M1 RAG API",
        description="整合 LINE Bot + RAG 的失智症警訊分析系統",
        version="2.0.0"
    )

    # 全域變數
    enhanced_engine = None

    @app.on_event("startup")
    async def startup_event():
        """應用程式啟動時初始化"""
        global enhanced_engine

        api_key = os.getenv('AISTUDIO_API_KEY')
        if not api_key:
            print("警告：未設定 AISTUDIO_API_KEY")
            return

        try:
            enhanced_engine = EnhancedM1RAGEngine(api_key)
            print("✅ Enhanced M1 RAG 引擎初始化完成")
        except Exception as e:
            print(f"❌ 引擎初始化失敗：{e}")

    # ===== 保留現有的 M1 Flex API 端點 =====

    @app.post("/m1-flex")
    async def m1_flex_classic(request: UserInput):
        """
        保留原有的 M1 Flex API，但加入 RAG 增強
        完全向後相容你的現有 LINE Bot
        """
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        try:
            # 使用增強版分析（包含 RAG 檢索）
            analysis_result = enhanced_engine.analyze_with_enhanced_context(request.user_input)

            # 生成 Flex Message（保留你現有的格式）
            flex_message = generate_enhanced_flex_message(analysis_result)

            return {
                "flex_message": flex_message,
                "analysis_data": analysis_result,
                "enhanced": True,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            # 保留原有的錯誤處理機制
            return generate_error_flex_message(str(e))

    # ===== 新增的 RAG API 端點 =====

    @app.post("/api/v1/analyze")
    async def unified_analyze(request: RAGQuery):
        """
        統一的分析端點
        支援 RAG 檢索 + AI 分析
        """
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        try:
            # RAG 分析
            analysis_result = enhanced_engine.analyze_with_enhanced_context(request.query)

            # 檢索資訊
            chunks = enhanced_engine.retrieve_relevant_chunks(request.query, k=request.k)

            return {
                "analysis": analysis_result,
                "retrieved_chunks": chunks,
                "query": request.query,
                "module_filter": request.module_filter,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"分析失敗：{str(e)}")

    @app.post("/api/v1/flex-message")
    async def generate_flex_only(request: UserInput):
        """
        純 Flex Message 生成端點
        用於從分析結果生成視覺化卡片
        """
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        try:
            # 分析
            analysis_result = enhanced_engine.analyze_with_enhanced_context(request.user_input)

            # 生成 Flex Message
            flex_message = generate_enhanced_flex_message(analysis_result)

            return FlexMessageResponse(
                flex_message=flex_message,
                analysis_data=analysis_result,
                metadata={
                    "generation_time": datetime.now().isoformat(),
                    "rag_enhanced": analysis_result.get("rag_enhanced", False),
                    "chunks_used": analysis_result.get("total_chunks_used", 0)
                }
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Flex Message 生成失敗：{str(e)}")

    @app.get("/api/v1/search")
    async def search_chunks(
        q: str,
        k: int = 5,
        format: str = "json"
    ):
        """
        純檢索端點
        只做檢索，不做 AI 分析
        """
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        try:
            chunks = enhanced_engine.retrieve_relevant_chunks(q, k=k)

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
        保留你現有的視覺設計，加入 RAG 資訊
        """

        # 基本資訊提取
        warning_code = analysis_data.get("matched_warning_code", "M1-GENERAL")
        symptom_title = analysis_data.get("symptom_title", "需要關注的症狀")
        user_behavior = analysis_data.get("user_behavior_summary", "描述的情況")
        normal_behavior = analysis_data.get("normal_behavior", "正常老化的表現")
        dementia_indicator = analysis_data.get("dementia_indicator", "需要注意的警訊")
        action_suggestion = analysis_data.get("action_suggestion", "建議諮詢專業人員")
        confidence = analysis_data.get("confidence_level", "medium")

        # RAG 增強資訊
        rag_enhanced = analysis_data.get("rag_enhanced", False)
        chunks_used = analysis_data.get("total_chunks_used", 0)

        # 信心程度顏色映射
        confidence_colors = {
            "high": "#28a745",    # 綠色
            "medium": "#ffc107",  # 黃色  
            "low": "#dc3545"      # 紅色
        }

        confidence_color = confidence_colors.get(confidence, "#6c757d")

        # 生成 Flex Message（保留你的設計風格）
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

                        # RAG 增強資訊（新增）
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"🔍 分析資訊 {'(RAG增強)' if rag_enhanced else ''}",
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
                                            "text": f"信心程度: {confidence.upper()}",
                                            "size": "xs",
                                            "color": confidence_color,
                                            "weight": "bold",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": f"參考資料: {chunks_used}項",
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
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        }

    # ===== 保留現有的 LINE Bot Webhook 端點 =====

    @app.post("/webhook")
    async def line_webhook(request: Request):
        """
        LINE Bot Webhook 端點
        保留你現有的 LINE Bot 整合邏輯
        """
        body = await request.body()

        try:
            # 這裡保留你現有的 LINE Bot 處理邏輯
            # 包括簽章驗證、事件解析等

            # 示例：基本事件處理
            events = json.loads(body.decode('utf-8')).get('events', [])

            for event in events:
                if event['type'] == 'message' and event['message']['type'] == 'text':
                    user_message = event['message']['text']

                    # 呼叫增強版 M1 分析
                    analysis_response = await m1_flex_classic(
                        UserInput(user_input=user_message)
                    )

                    # 這裡加入你的 LINE Bot 回應邏輯
                    # line_bot_api.reply_message(...)

            return {"status": "success"}

        except Exception as e:
            print(f"Webhook 處理錯誤：{e}")
            return {"status": "error", "message": str(e)}

    # ===== 健康檢查與監控端點 =====

    @app.get("/health")
    async def health_check():
        """系統健康檢查"""
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        # 檢查各組件狀態
        chunks_count = len(enhanced_engine.chunks)
        index_ready = enhanced_engine.index is not None

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "rag_engine": "ready",
                "vector_index": "ready" if index_ready else "not_ready",
                "chunks_loaded": chunks_count,
                "gemini_api": "configured" if os.getenv('AISTUDIO_API_KEY') else "not_configured"
            },
            "endpoints": {
                "m1_flex_classic": "/m1-flex",
                "unified_analyze": "/api/v1/analyze", 
                "flex_generation": "/api/v1/flex-message",
                "search_only": "/api/v1/search",
                "line_webhook": "/webhook"
            },
            "version": "2.0.0"
        }

    @app.get("/api/v1/stats")
    async def get_statistics():
        """取得系統統計資訊"""
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        # 統計 chunks 資訊
        chunk_types = {}
        for chunk in enhanced_engine.chunks:
            chunk_type = chunk.get('chunk_type', 'unknown')
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1

        return {
            "total_chunks": len(enhanced_engine.chunks),
            "chunk_distribution": chunk_types,
            "modules_available": ["M1"],
            "features": {
                "rag_retrieval": True,
                "ai_analysis": True, 
                "flex_message": True,
                "line_bot_integration": True
            },
            "timestamp": datetime.now().isoformat()
        }

    # ===== 開發與測試端點 =====

    @app.get("/api/v1/test")
    async def test_system():
        """系統功能測試端點"""
        if not enhanced_engine:
            raise HTTPException(status_code=503, detail="引擎未初始化")

        test_cases = [
            "媽媽最近常忘記關瓦斯",
            "爸爸開車時會迷路",
            "奶奶重複問同樣的問題"
        ]

        results = []
        for test_input in test_cases:
            try:
                # 測試檢索
                chunks = enhanced_engine.retrieve_relevant_chunks(test_input, k=2)

                # 測試分析（簡化版，避免過多 API 呼叫）
                result = {
                    "input": test_input,
                    "chunks_retrieved": len(chunks),
                    "top_match": chunks[0]['title'] if chunks else "無匹配",
                    "similarity_score": chunks[0]['similarity_score'] if chunks else 0,
                    "status": "success"
                }
                results.append(result)

            except Exception as e:
                results.append({
                    "input": test_input,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "test_results": results,
            "overall_status": "healthy" if all(r['status'] == 'success' for r in results) else "degraded",
            "timestamp": datetime.now().isoformat()
        }

    # ===== 主程式執行 =====

    if __name__ == "__main__":
        print("🚀 啟動增強版 M1 RAG API 伺服器...")
        print("📋 功能清單：")
        print("   ✅ 保留原有 M1 Flex API (/m1-flex)")
        print("   ✅ 新增統一分析 API (/api/v1/analyze)")  
        print("   ✅ RAG 檢索增強")
        print("   ✅ LINE Bot Webhook 支援")
        print("   ✅ Flex Message 生成")
        print("   ✅ 系統監控與測試")
        print("\n📖 API 文件：http://localhost:8001/docs")
        print("🔍 健康檢查：http://localhost:8001/health")

        # 檢查必要的環境變數
        if not os.getenv('AISTUDIO_API_KEY'):
            print("\n⚠️  警告：請設定 AISTUDIO_API_KEY 環境變數")

        # 啟動伺服器（port 8001 符合你的現有架構）
        uvicorn.run(
            "day2_unified_api:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info"
        )