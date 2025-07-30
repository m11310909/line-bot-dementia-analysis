from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# 引入整合引擎
try:
    from m1_m2_m3_integrated_rag import M1M2M3IntegratedEngine
except ImportError:
    print("⚠️  整合引擎模組未找到")
    M1M2M3IntegratedEngine = None

# FastAPI 應用
app = FastAPI(
    title="M1+M2+M3 完整整合 RAG API",
    description="支援失智症警訊(M1) + 病程階段(M2) + BPSD行為心理症狀(M3)",
    version="3.0.0"
)

# 全域引擎
integrated_engine = None

@app.on_event("startup")
async def startup():
    global integrated_engine
    print("🚀 啟動 M1+M2+M3 完整整合引擎...")

    api_key = os.getenv('AISTUDIO_API_KEY')

    if M1M2M3IntegratedEngine:
        integrated_engine = M1M2M3IntegratedEngine(api_key)
    else:
        print("❌ 整合引擎無法載入")
        return

    print("✅ M1+M2+M3 完整整合 API 啟動成功")

class UserInput(BaseModel):
    user_input: str

@app.get("/")
def root():
    return {
        "message": "M1+M2+M3 完整整合 RAG API",
        "version": "3.0.0",
        "features": [
            "🚨 M1: 失智症十大警訊識別",
            "🏥 M2: 病程階段分析",
            "🧠 M3: BPSD 行為心理症狀分析",
            "🔍 智能語義檢索",
            "📊 多重信心度評估",
            "🎯 綜合分析報告"
        ],
        "modules": {
            "M1": "失智症警訊檢測",
            "M2": "病程階段分析",
            "M3": "BPSD 行為心理症狀"
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
        }
    }

@app.post("/comprehensive-analysis")
def comprehensive_analysis(request: UserInput):
    """M1+M2+M3 綜合分析端點"""

    if not integrated_engine:
        return {"error": "引擎未初始化"}

    try:
        # 使用整合引擎進行綜合分析
        result = integrated_engine.analyze_comprehensive(request.user_input)

        # 生成增強版 Flex Message
        flex_message = create_comprehensive_flex_message(result, request.user_input)

        return {
            "flex_message": flex_message,
            "comprehensive_analysis": {
                "matched_codes": result.matched_codes,
                "symptom_titles": result.symptom_titles,
                "confidence_levels": result.confidence_levels,
                "modules_used": result.modules_used,
                "bpsd_analysis": result.bpsd_analysis,
                "stage_detection": result.stage_detection,
                "comprehensive_summary": result.comprehensive_summary,
                "action_suggestions": result.action_suggestions,
                "total_findings": len(result.matched_codes)
            },
            "retrieved_chunks": result.retrieved_chunks,
            "enhanced": True,
            "version": "3.0.0",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "error": str(e),
            "flex_message": create_error_flex_message(),
            "enhanced": False
        }

@app.post("/m1-flex")  
def analyze_with_flex(request: UserInput):
    """向後相容的端點"""
    return comprehensive_analysis(request)

def create_comprehensive_flex_message(result, user_input: str) -> Dict:
    """創建綜合 Flex Message"""

    primary_title = result.symptom_titles[0] if result.symptom_titles else "綜合分析結果"
    primary_code = result.matched_codes[0] if result.matched_codes else "COMPREHENSIVE"

    # 模組圖標
    module_icons = {"M1": "🚨", "M2": "🏥", "M3": "🧠"}

    # 建立內容
    body_contents = [
        {
            "type": "text",
            "text": primary_title,
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
    ]

    # 添加檢測結果
    for i, (code, title, confidence) in enumerate(zip(
        result.matched_codes[:3],  # 最多顯示 3 個
        result.symptom_titles[:3],
        result.confidence_levels[:3]
    )):
        module_prefix = code.split("-")[0]
        icon = module_icons.get(module_prefix, "🔍")

        confidence_colors = {
            "high": "#28a745",
            "medium": "#ffc107", 
            "low": "#dc3545"
        }
        confidence_color = confidence_colors.get(confidence, "#6c757d")

        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"{icon} {title}",
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

    # 添加綜合摘要
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
                "text": result.comprehensive_summary,
                "size": "xs",
                "wrap": True,
                "margin": "xs",
                "color": "#666666"
            }
        ]
    })

    # 添加建議
    if result.action_suggestions:
        suggestion_text = "；".join(result.action_suggestions[:2])
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
                    "text": suggestion_text,
                    "size": "xs",
                    "wrap": True,
                    "margin": "xs",
                    "color": "#666666"
                }
            ]
        })

    return {
        "type": "flex",
        "altText": f"失智症綜合分析：{primary_title}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "🧠 M1+M2+M3 綜合分析",
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
                "contents": body_contents,
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
                            "text": f"請詳細說明{primary_code}的相關資訊"
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
    """錯誤 Flex Message"""
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

@app.get("/modules/status")
def modules_status():
    """模組狀態檢查"""
    if not integrated_engine:
        return {"error": "引擎未初始化"}

    m1_chunks = [c for c in integrated_engine.chunks if c.get("chunk_id", "").startswith("M1")]
    m2_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M2"]
    m3_chunks = [c for c in integrated_engine.chunks if c.get("module_id") == "M3"]

    return {
        "modules": {
            "M1": {
                "name": "失智症十大警訊",
                "status": "active" if m1_chunks else "inactive",
                "chunks": len(m1_chunks),
                "features": ["記憶力檢測", "日常功能評估", "認知警訊識別"]
            },
            "M2": {
                "name": "病程階段分析",
                "status": "active" if m2_chunks else "inactive", 
                "chunks": len(m2_chunks),
                "features": ["輕度評估", "中度評估", "重度評估"]
            },
            "M3": {
                "name": "BPSD 行為心理症狀",
                "status": "active" if m3_chunks else "inactive",
                "chunks": len(m3_chunks),
                "features": ["妄想檢測", "幻覺分析", "激動行為", "憂鬱焦慮", "睡眠障礙", "飲食行為"]
            }
        },
        "total_capabilities": len(m1_chunks) + len(m2_chunks) + len(m3_chunks),
        "integration_level": "full" if all([m1_chunks, m2_chunks, m3_chunks]) else "partial"
    }

if __name__ == "__main__":
    print("🚀 啟動 M1+M2+M3 完整整合 RAG API...")
    print("📋 功能：")
    print("   🚨 M1: 失智症十大警訊識別")
    print("   🏥 M2: 病程階段分析")
    print("   🧠 M3: BPSD 行為心理症狀分析")
    print("   🔍 智能語義檢索")
    print("   📊 多重信心度評估")
    print("   🎯 綜合分析報告")

    uvicorn.run(app, host="0.0.0.0", port=8005, log_level="info")
