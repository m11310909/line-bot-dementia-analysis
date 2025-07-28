from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime
from m1_m2_integrated_rag import M1M2RAGEngine

# FastAPI 應用
app = FastAPI(
    title="M1+M2 整合 RAG API",
    description="支援失智症警訊(M1) + 病程階段分析(M2)",
    version="2.1.0"
)

# 全域引擎
integrated_engine = None

@app.on_event("startup")
async def startup():
    global integrated_engine
    print("🚀 啟動 M1+M2 整合引擎...")
    
    api_key = os.getenv('AISTUDIO_API_KEY')
    integrated_engine = M1M2RAGEngine(api_key)
    
    print("✅ M1+M2 整合 API 啟動成功")

class UserInput(BaseModel):
    user_input: str

@app.get("/")
def root():
    return {
        "message": "M1+M2 整合 RAG API",
        "version": "2.1.0",
        "features": [
            "🚨 M1: 失智症十大警訊識別",
            "🏥 M2: 病程階段分析",
            "🔍 智能語義檢索",
            "📊 信心度評估"
        ],
        "modules": {
            "M1": "失智症警訊檢測",
            "M2": "病程階段分析"
        },
        "total_chunks": len(integrated_engine.chunks) if integrated_engine else 0
    }

@app.get("/health")
def health():
    if not integrated_engine:
        return {"status": "error", "message": "引擎未初始化"}
    
    # 統計模組分布
    m1_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M1"]
    m2_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M2"]
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_info": {
            "total_chunks": len(integrated_engine.chunks),
            "m1_chunks": len(m1_chunks),
            "m2_chunks": len(m2_chunks),
            "vocabulary_size": len(integrated_engine.vocabulary)
        },
        "capabilities": [
            "warning_sign_detection",
            "stage_analysis", 
            "semantic_search",
            "confidence_scoring"
        ]
    }

@app.post("/m1-flex")
def analyze_with_flex(request: UserInput):
    """主要分析端點 - 整合 M1+M2 功能"""
    
    if not integrated_engine:
        return {"error": "引擎未初始化"}
    
    try:
        # 使用整合引擎進行分析
        result = integrated_engine.analyze_with_stage_detection(request.user_input)
        
        # 生成增強版 Flex Message
        flex_message = create_enhanced_flex_message(result, request.user_input)
        
        return {
            "flex_message": flex_message,
            "analysis_data": result,
            "enhanced": True,
            "version": "2.1.0",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "flex_message": create_error_flex_message(),
            "enhanced": False
        }

@app.post("/api/v1/analyze")
def detailed_analysis(request: UserInput):
    """詳細分析端點 - 返回完整分析資料"""
    
    if not integrated_engine:
        raise HTTPException(status_code=503, detail="引擎未初始化")
    
    try:
        result = integrated_engine.analyze_with_stage_detection(request.user_input)
        
        return {
            "query": request.user_input,
            "analysis": result,
            "modules_used": get_modules_used(result),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_modules_used(result):
    """分析使用了哪些模組"""
    retrieved_chunks = result.get("retrieved_chunks", [])
    modules = {}
    
    for chunk in retrieved_chunks:
        module_id = chunk.get("module_id", "unknown")
        if module_id not in modules:
            modules[module_id] = {
                "count": 0,
                "avg_similarity": 0,
                "chunks": []
            }
        
        modules[module_id]["count"] += 1
        modules[module_id]["chunks"].append({
            "chunk_id": chunk.get("chunk_id"),
            "title": chunk.get("title"),
            "similarity": chunk.get("similarity_score", 0)
        })
    
    # 計算平均相似度
    for module_id, info in modules.items():
        if info["chunks"]:
            avg_sim = sum(c["similarity"] for c in info["chunks"]) / len(info["chunks"])
            info["avg_similarity"] = round(avg_sim, 4)
    
    return modules

def create_enhanced_flex_message(result, user_input):
    """創建增強版 Flex Message（包含 M1+M2 資訊）"""
    
    # 基本資訊
    warning_code = result.get("matched_warning_code", "M1-GENERAL")
    symptom_title = result.get("symptom_title", "需要關注的症狀")
    confidence = result.get("confidence_level", "medium")
    
    # M2 階段資訊
    stage_info = result.get("stage_detection", {})
    detected_stage = stage_info.get("detected_stage", "需要評估")
    stage_confidence = stage_info.get("confidence", 0)
    
    # 信心度顏色
    confidence_colors = {
        "high": "#28a745",
        "medium": "#ffc107", 
        "low": "#dc3545"
    }
    confidence_color = confidence_colors.get(confidence, "#6c757d")
    
    return {
        "type": "flex",
        "altText": f"失智症分析：{symptom_title}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "🧠 M1+M2 整合分析",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                }],
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
                                "text": user_input,
                                "size": "sm",
                                "wrap": True,
                                "margin": "xs"
                            }
                        ]
                    },
                    
                    # M1 警訊分析
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"🚨 警訊識別：{warning_code}",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#dc3545"
                            },
                            {
                                "type": "text",
                                "text": f"信心程度：{confidence.upper()}",
                                "size": "xs",
                                "color": confidence_color,
                                "margin": "xs"
                            }
                        ]
                    },
                    
                    # M2 階段分析（如果有）
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"🏥 病程階段：{detected_stage}",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#007bff"
                            },
                            {
                                "type": "text",
                                "text": f"階段信心：{stage_confidence:.2f}",
                                "size": "xs",
                                "color": "#666666",
                                "margin": "xs"
                            }
                        ]
                    } if stage_info else {
                        "type": "text",
                        "text": "🔍 未檢測到明確階段特徵",
                        "size": "xs",
                        "color": "#999999",
                        "margin": "md"
                    },
                    
                    # 建議行動
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
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
                                "text": result.get("action_suggestion", "建議諮詢專業醫療人員進行評估"),
                                "size": "xs",
                                "wrap": True,
                                "margin": "xs",
                                "color": "#666666"
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
                            "label": "了解更多",
                            "text": f"請告訴我更多關於{detected_stage}失智症的資訊"
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

def create_error_flex_message():
    """錯誤時的 Flex Message"""
    return {
        "type": "flex",
        "altText": "系統暫時無法分析",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "😅 分析服務暫時無法使用，請稍後再試。",
                    "wrap": True,
                    "size": "md"
                }]
            }
        }
    }

@app.get("/test")
def test_endpoint():
    """測試端點"""
    return {
        "message": "M1+M2 整合 API 測試",
        "engine_ready": integrated_engine is not None,
        "version": "2.1.0"
    }

if __name__ == "__main__":
    print("🚀 啟動 M1+M2 整合 RAG API...")
    print("📋 功能：")
    print("   🚨 M1: 失智症警訊識別")
    print("   🏥 M2: 病程階段分析")
    print("   🔍 智能語義檢索")
    print("   📊 信心度評估")
    
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")

