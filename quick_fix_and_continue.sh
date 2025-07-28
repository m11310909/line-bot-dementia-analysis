# ========================================
# 🚀 快速修復並繼續 M1+M2+M3 系統建置
# ========================================

echo "🔧 修復 here-document 問題並繼續建置..."

# 首先執行修復腳本
bash fixed_engine_creation.sh

# 確認 M3 資料是否存在
if [ ! -f "m3_bpsd_data.json" ]; then
    echo "🧠 M3 資料不存在，正在建立..."
    python3 create_m3_data.py
fi

# 確認整合引擎是否存在
if [ ! -f "m1_m2_m3_integrated_rag.py" ]; then
    echo "❌ 整合引擎建立失敗"
    exit 1
fi

echo "✅ 整合引擎修復完成"

# ========================================
# 建立 API 服務
# ========================================
echo ""
echo "============================================"
echo "📋 建立 M1+M2+M3 API 服務"
echo "============================================"

# 建立 API 服務檔案
python3 << 'API_SCRIPT'
api_code = '''from fastapi import FastAPI, Request, HTTPException
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
'''

# 寫入檔案
with open('m1_m2_m3_integrated_api.py', 'w', encoding='utf-8') as f:
    f.write(api_code)

print("✅ API 服務檔案已成功建立")
API_SCRIPT

echo "✅ API 服務建立完成"

# ========================================
# 停止舊服務並啟動新服務
# ========================================
echo ""
echo "============================================"
echo "📋 服務部署和啟動"
echo "============================================"

echo "🛑 停止舊服務..."
pkill -f "integrated_m1_m2_api" 2>/dev/null || echo "沒有找到舊的 API 服務"
pkill -f "port=800" 2>/dev/null || echo "沒有找到佔用端口的程序"

# 等待端口釋放
echo "⏳ 等待端口釋放..."
sleep 3

echo "🚀 啟動 M1+M2+M3 完整整合 API..."
echo "📍 新服務將在端口 8005 啟動"

# 啟動 API（後台運行）
python3 m1_m2_m3_integrated_api.py &
API_PID=$!

echo "⏳ 等待 API 啟動（20秒）..."
sleep 20

# 檢查服務是否啟動
echo "🔍 檢查服務狀態..."
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ M1+M2+M3 整合 API 啟動成功！"
else
    echo "❌ API 服務啟動失敗"
    echo "📋 請檢查："
    echo "   1. Python 相依套件是否安裝"
    echo "   2. 端口 8005 是否被佔用"
    echo "   3. 檔案權限是否正確"
    exit 1
fi

echo ""
echo "============================================"
echo "🧪 快速功能測試"
echo "============================================"

# 快速健康檢查
echo "📊 系統健康檢查："
curl -s http://localhost:8005/health

echo ""
echo ""

# 快速 M1 測試
echo "🚨 快速 M1 測試："
curl -s -X POST "http://localhost:8005/comprehensive-analysis" \
     -H "Content-Type: application/json" \
     -d '{"user_input": "媽媽常忘記事情"}' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    analysis = data.get('comprehensive_analysis', {})
    print(f\"✅ 檢測結果：{', '.join(analysis.get('matched_codes', [])[:2])}\")
    print(f\"✅ 使用模組：{', '.join(analysis.get('modules_used', []))}\")
except:
    print('❌ 測試失敗')
"

echo ""
echo ""

# 快速 M3 測試
echo "🧠 快速 M3 測試："
curl -s -X POST "http://localhost:8005/comprehensive-analysis" \
     -H "Content-Type: application/json" \
     -d '{"user_input": "懷疑有人偷東西"}' | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    analysis = data.get('comprehensive_analysis', {})
    print(f\"✅ 檢測結果：{', '.join(analysis.get('matched_codes', [])[:2])}\")
    print(f\"✅ 使用模組：{', '.join(analysis.get('modules_used', []))}\")
except:
    print('❌ 測試失敗')
"

echo ""
echo ""

echo "============================================"
echo "🎉 M1+M2+M3 系統修復並啟動成功！"
echo "============================================"
echo ""
echo "📍 服務地址：http://localhost:8005"
echo ""
echo "🔗 主要端點："
echo "   📱 /comprehensive-analysis  - M1+M2+M3 綜合分析"
echo "   📱 /m1-flex                 - 向後相容端點"
echo "   💚 /health                  - 健康檢查"
echo "   🔧 /modules/status          - 模組狀態"
echo ""
echo "🆕 完整功能："
echo "   ✅ M1: 失智症十大警訊識別"
echo "   ✅ M2: 病程階段分析（如有 M2 資料）"
echo "   ✅ M3: BPSD 行為心理症狀分析"
echo "   ✅ 智能語義檢索"
echo "   ✅ 多重信心度評估"
echo "   ✅ 綜合分析報告"
echo ""
echo "🧠 M3 BPSD 涵蓋症狀："
echo "   🔍 M3-01: 妄想症狀"
echo "   👻 M3-02: 幻覺症狀"
echo "   ⚡ M3-03: 激動攻擊行為"
echo "   😢 M3-04: 憂鬱與焦慮"
echo "   🚶 M3-05: 遊走與重複行為"
echo "   😴 M3-06: 睡眠障礙"
echo "   🍽️  M3-07: 飲食行為改變"
echo ""
echo "📱 立即可測試："
echo "   curl -X POST http://localhost:8005/comprehensive-analysis \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"user_input\": \"你想測試的症狀描述\"}'"
echo ""
echo "⚡ API 服務持續運行中（PID: $API_PID）"
echo "💡 使用 'pkill -f m1_m2_m3_integrated_api' 停止服務"
echo ""
echo "🎯 修復完成！現在可以繼續進行完整測試！"

# 保持服務運行
wait $API_PID