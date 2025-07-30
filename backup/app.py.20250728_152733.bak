# 將上面完整的修復版程式碼貼到這裡
# app.py - 完整修復版 FlexComponent 系統
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List, Optional, Union
import uuid
import time
import json
import asyncio
from datetime import datetime
from enum import Enum
import logging
import socket

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== 數據模型 (已修復 Pydantic V2) =====
class ComponentType(str, Enum):
    COMPARISON_CARD = "comparison_card"
    CONFIDENCE_METER = "confidence_meter"
    XAI_BOX = "xai_box"
    INFO_BOX = "info_box"
    ACTION_CARD = "action_card"

class ChunkInput(BaseModel):
    type: str = Field(..., description="Chunk 類型")
    title: Optional[str] = Field(None, description="組件標題")
    content: Dict[str, Any] = Field(..., description="內容數據")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元數據")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="信心度")

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v):
        if v is not None and not 0 <= v <= 1:
            raise ValueError('信心度必須在 0-1 之間')
        return v

class XAIInput(BaseModel):
    explanation: str = Field(..., description="解釋文本")
    confidence_score: float = Field(..., ge=0, le=1, description="信心分數")
    feature_importance: Dict[str, float] = Field(default_factory=dict, description="特徵重要性")
    reasoning_steps: List[str] = Field(default_factory=list, description="推理步驟")
    uncertainty_factors: List[str] = Field(default_factory=list, description="不確定因素")

class ComponentRequest(BaseModel):
    chunks: List[ChunkInput] = Field(..., description="要處理的數據塊")
    xai_data: Optional[List[XAIInput]] = Field(None, description="XAI 解釋數據")
    options: Dict[str, Any] = Field(default_factory=dict, description="處理選項")

class ComponentOutput(BaseModel):
    type: str
    id: str
    title: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    xai_summary: Optional[str] = None

class ProcessingResult(BaseModel):
    success: bool
    components: List[ComponentOutput]
    errors: List[str] = Field(default_factory=list)
    processing_time: float
    metadata: Dict[str, Any]

# ===== 組件工廠 (穩定版) =====
class StableComponentFactory:
    def __init__(self):
        self.type_mapping = {
            'comparison': ComponentType.COMPARISON_CARD,
            'confidence': ComponentType.CONFIDENCE_METER,
            'explanation': ComponentType.XAI_BOX,
            'info': ComponentType.INFO_BOX,
            'action': ComponentType.ACTION_CARD,
            # 別名
            'compare': ComponentType.COMPARISON_CARD,
            'vs': ComponentType.COMPARISON_CARD,
            'cert': ComponentType.CONFIDENCE_METER,
            'probability': ComponentType.CONFIDENCE_METER,
            'xai': ComponentType.XAI_BOX,
            'explain': ComponentType.XAI_BOX,
            'reasoning': ComponentType.XAI_BOX,
            'information': ComponentType.INFO_BOX,
            'general': ComponentType.INFO_BOX,
            'todo': ComponentType.ACTION_CARD,
            'tasks': ComponentType.ACTION_CARD,
        }

        self.stats = {
            'total_processed': 0,
            'type_distribution': {t.value: 0 for t in ComponentType},
            'error_count': 0
        }

    async def create_component(self, chunk: ChunkInput, xai_data: Optional[XAIInput] = None) -> ComponentOutput:
        try:
            component_type = self._determine_type(chunk)
            component_data = self._format_data(chunk, component_type, xai_data)

            self.stats['total_processed'] += 1
            self.stats['type_distribution'][component_type.value] += 1

            return ComponentOutput(
                type=component_type.value,
                id=f"{component_type.value}_{str(uuid.uuid4())[:8]}",
                title=chunk.title or self._get_default_title(component_type),
                data=component_data,
                metadata={
                    "created_at": datetime.now().isoformat(),
                    "original_type": chunk.type,
                    "has_confidence": chunk.confidence is not None,
                    "has_xai": xai_data is not None
                },
                created_at=datetime.now(),
                xai_summary=xai_data.explanation if xai_data else None
            )

        except Exception as e:
            self.stats['error_count'] += 1
            logger.error(f"組件創建失敗: {e}")
            return self._create_error_component(chunk, str(e))

    def _determine_type(self, chunk: ChunkInput) -> ComponentType:
        chunk_type = chunk.type.lower().strip()

        # 直接映射
        if chunk_type in self.type_mapping:
            return self.type_mapping[chunk_type]

        # 關鍵詞推斷
        content_str = str(chunk.content).lower()
        title_str = (chunk.title or "").lower()
        combined_text = f"{content_str} {title_str}"

        if any(keyword in combined_text for keyword in ['compare', 'vs', '比較', 'versus', 'option']):
            return ComponentType.COMPARISON_CARD
        elif any(keyword in combined_text for keyword in ['confidence', 'probability', '信心', 'certainty']):
            return ComponentType.CONFIDENCE_METER
        elif any(keyword in combined_text for keyword in ['explanation', 'reasoning', '解釋', 'why', 'because']):
            return ComponentType.XAI_BOX
        elif any(keyword in combined_text for keyword in ['action', 'todo', '行動', 'task', 'recommendation']):
            return ComponentType.ACTION_CARD
        else:
            return ComponentType.INFO_BOX

    def _format_data(self, chunk: ChunkInput, comp_type: ComponentType, xai_data: Optional[XAIInput]) -> Dict[str, Any]:
        base_data = {
            "title": chunk.title,
            "content": chunk.content,
            "confidence": chunk.confidence,
            "metadata": chunk.metadata
        }

        if comp_type == ComponentType.COMPARISON_CARD:
            base_data.update({
                "comparison_data": chunk.content.get('options', chunk.content),
                "layout": {
                    "columns": 2,
                    "highlight_differences": True,
                    "show_confidence": chunk.confidence is not None
                }
            })

        elif comp_type == ComponentType.CONFIDENCE_METER:
            confidence = chunk.confidence or (xai_data.confidence_score if xai_data else 0.5)
            base_data.update({
                "confidence_value": confidence,
                "confidence_level": self._get_confidence_level(confidence),
                "uncertainty_factors": xai_data.uncertainty_factors if xai_data else [],
                "display": {
                    "show_numeric": True,
                    "show_bars": True,
                    "color_scheme": self._get_color_scheme(confidence)
                }
            })

        elif comp_type == ComponentType.XAI_BOX:
            base_data.update({
                "explanation": xai_data.explanation if xai_data else chunk.content.get('explanation', ''),
                "reasoning_steps": xai_data.reasoning_steps if xai_data else [],
                "feature_importance": self._format_feature_importance(xai_data),
                "confidence_score": xai_data.confidence_score if xai_data else chunk.confidence,
                "interactive": {
                    "expandable": True,
                    "show_details": True,
                    "highlight_key_factors": True
                }
            })

        elif comp_type == ComponentType.ACTION_CARD:
            actions = self._extract_actions(chunk.content)
            base_data.update({
                "actions": actions,
                "priority": chunk.metadata.get('priority', 'medium'),
                "deadline": chunk.metadata.get('deadline'),
                "progress": chunk.metadata.get('progress', 0),
                "interactive": {
                    "clickable": True,
                    "show_progress": True,
                    "enable_feedback": True
                }
            })

        return base_data

    def _extract_actions(self, content: Dict[str, Any]) -> List[str]:
        if isinstance(content, dict):
            if 'actions' in content and isinstance(content['actions'], list):
                return content['actions']
            elif 'tasks' in content and isinstance(content['tasks'], list):
                return content['tasks']
            elif 'recommendations' in content and isinstance(content['recommendations'], list):
                return content['recommendations']
        elif isinstance(content, list):
            return [str(item) for item in content]

        return [str(content)]

    def _get_confidence_level(self, confidence: float) -> str:
        if confidence >= 0.8: return "高"
        elif confidence >= 0.6: return "中"
        elif confidence >= 0.4: return "低"
        else: return "很低"

    def _get_color_scheme(self, confidence: float) -> str:
        if confidence >= 0.7: return "green"
        elif confidence >= 0.5: return "yellow"
        else: return "red"

    def _format_feature_importance(self, xai_data: Optional[XAIInput]) -> List[Dict[str, Any]]:
        if not xai_data or not xai_data.feature_importance:
            return []

        return [
            {
                "feature": feature,
                "importance": importance,
                "impact": "正面" if importance > 0 else "負面",
                "abs_importance": abs(importance)
            }
            for feature, importance in sorted(
                xai_data.feature_importance.items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )
        ]

    def _get_default_title(self, comp_type: ComponentType) -> str:
        titles = {
            ComponentType.COMPARISON_CARD: "比較分析",
            ComponentType.CONFIDENCE_METER: "信心度評估",
            ComponentType.XAI_BOX: "AI 解釋",
            ComponentType.INFO_BOX: "信息摘要",
            ComponentType.ACTION_CARD: "行動建議"
        }
        return titles.get(comp_type, "未命名組件")

    def _create_error_component(self, chunk: ChunkInput, error_msg: str) -> ComponentOutput:
        return ComponentOutput(
            type=ComponentType.INFO_BOX.value,
            id=f"error_{str(uuid.uuid4())[:8]}",
            title="組件創建錯誤",
            data={
                "error": error_msg,
                "original_chunk": chunk.dict() if hasattr(chunk, 'dict') else str(chunk),
                "fallback": True
            },
            metadata={"error": True, "created_at": datetime.now().isoformat()},
            created_at=datetime.now()
        )

    def get_stats(self) -> Dict[str, Any]:
        return self.stats.copy()

# ===== 端口檢查工具 =====
def find_available_port(start_port=8000, max_attempts=10):
    """找到可用端口"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

# ===== FastAPI 應用 =====
app = FastAPI(
    title="FlexComponent System - Stable Version",
    description="智能組件系統穩定版 - 修復所有已知問題",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

factory = StableComponentFactory()
start_time = time.time()

@app.get("/")
async def root():
    return {
        "message": "FlexComponent System - Stable v2.1",
        "status": "running",
        "uptime": time.time() - start_time,
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "create_components": "/api/components",
            "health": "/api/health",
            "stats": "/api/stats",
            "docs": "/docs",
            "demo": "/demo"
        }
    }

@app.post("/api/components", response_model=ProcessingResult)
async def create_components(request: ComponentRequest, background_tasks: BackgroundTasks):
    """創建組件端點"""
    processing_start = time.time()

    try:
        logger.info(f"處理請求: {len(request.chunks)} 個 chunks")

        # 並行處理組件
        tasks = []
        for i, chunk in enumerate(request.chunks):
            xai_data = None
            if request.xai_data and i < len(request.xai_data):
                xai_data = request.xai_data[i]

            task = factory.create_component(chunk, xai_data)
            tasks.append(task)

        # 等待所有任務完成
        components = await asyncio.gather(*tasks, return_exceptions=True)

        # 處理結果
        successful_components = []
        errors = []

        for i, component in enumerate(components):
            if isinstance(component, Exception):
                errors.append(f"Chunk {i} 處理失敗: {str(component)}")
            else:
                successful_components.append(component)

        processing_time = time.time() - processing_start

        # 背景任務：記錄處理日誌
        background_tasks.add_task(
            log_processing_result, 
            len(successful_components), 
            len(errors), 
            processing_time
        )

        return ProcessingResult(
            success=len(errors) == 0,
            components=successful_components,
            errors=errors,
            processing_time=processing_time,
            metadata={
                "total_chunks": len(request.chunks),
                "successful_components": len(successful_components),
                "failed_components": len(errors),
                "timestamp": datetime.now().isoformat(),
                "parallel_processing": True,
                "factory_stats": factory.get_stats()
            }
        )

    except Exception as e:
        logger.error(f"請求處理失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0",
        "uptime": time.time() - start_time,
        "factory_stats": factory.get_stats()
    }

@app.get("/api/stats")
async def get_stats():
    """獲取統計信息"""
    stats = factory.get_stats()
    stats.update({
        "uptime": time.time() - start_time,
        "server_status": "running",
        "last_updated": datetime.now().isoformat()
    })
    return stats

# 背景任務
async def log_processing_result(success_count: int, error_count: int, processing_time: float):
    """記錄處理結果"""
    logger.info(f"處理完成: 成功 {success_count}, 失敗 {error_count}, 耗時 {processing_time:.3f}s")

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """穩定版演示頁面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlexComponent Stable Demo</title>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .component { border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background: #fff; }
            .comparison { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .confidence { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
            .xai { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
            .action { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; }
            .info { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
            button { background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
            .stats { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; max-height: 300px; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FlexComponent Stable Demo</h1>
            <p>穩定版智能組件系統 - 修復所有已知問題，支援 Pydantic V2</p>

            <div class="stats" id="stats"></div>

            <button onclick="runBasicTest()">基礎測試</button>
            <button onclick="runAdvancedTest()">高級測試 (含 XAI)</button>
            <button onclick="runStressTest()">壓力測試</button>
            <button onclick="getStats()">查看統計</button>
            <button onclick="clearResults()">清除結果</button>

            <div id="results"></div>
        </div>

        <script>
        async function runBasicTest() {
            showLoading('運行基礎測試...');

            const testData = {
                chunks: [
                    {
                        type: "comparison",
                        title: "產品方案比較",
                        content: {
                            options: {
                                "基礎版": {"價格": "$99", "功能": "基礎", "支援": "郵件"},
                                "專業版": {"價格": "$199", "功能": "完整", "支援": "24/7"}
                            }
                        },
                        confidence: 0.92
                    },
                    {
                        type: "confidence",
                        title: "系統信心度",
                        content: {"system": "stable_version"},
                        confidence: 0.98
                    },
                    {
                        type: "action",
                        title: "測試任務清單",
                        content: {
                            actions: [
                                "驗證 API 功能",
                                "測試組件渲染",
                                "檢查錯誤處理",
                                "確認穩定性"
                            ]
                        },
                        metadata: {"priority": "high"}
                    }
                ]
            };

            await executeRequest(testData, '基礎測試');
        }

        async function runAdvancedTest() {
            showLoading('運行高級測試 (含 XAI)...');

            const testData = {
                chunks: [
                    {
                        type: "explanation",
                        title: "智能推薦系統分析",
                        content: {"recommendation": "market_strategy"},
                        confidence: 0.87
                    }
                ],
                xai_data: [
                    {
                        explanation: "基於用戶行為數據和市場趨勢，建議採用個性化推薦策略",
                        confidence_score: 0.87,
                        feature_importance: {
                            "用戶歷史行為": 0.35,
                            "市場趨勢": 0.28,
                            "競品分析": 0.20,
                            "季節因素": 0.17
                        },
                        reasoning_steps: [
                            "收集並分析用戶歷史行為數據",
                            "評估當前市場趨勢和需求",
                            "分析競爭對手策略和定位",
                            "考慮季節性因素對策略的影響"
                        ],
                        uncertainty_factors: ["市場波動性", "用戶偏好變化", "技術限制"]
                    }
                ]
            };

            await executeRequest(testData, '高級測試 (XAI)');
        }

        async function runStressTest() {
            showLoading('運行壓力測試 (10個組件)...');

            const chunks = [];
            const types = ["comparison", "confidence", "info", "action", "explanation"];

            for (let i = 0; i < 10; i++) {
                chunks.push({
                    type: types[i % 5],
                    title: `壓力測試組件 ${i + 1}`,
                    content: {
                        test_id: i,
                        test_data: `stress_test_data_${i}`,
                        random_value: Math.random()
                    },
                    confidence: Math.random(),
                    metadata: {
                        batch: "stress_test",
                        priority: ["high", "medium", "low"][i % 3]
                    }
                });
            }

            await executeRequest({chunks}, '壓力測試');
        }

        async function executeRequest(testData, testName) {
            try {
                const startTime = Date.now();
                const response = await axios.post('/api/components', testData);
                const endTime = Date.now();

                displayResults(response.data, endTime - startTime, testName);
            } catch (error) {
                showError('請求失敗: ' + error.message);
            }
        }

        function displayResults(data, clientTime, testName) {
            const resultsDiv = document.getElementById('results');

            let statusClass = data.success ? 'success' : 'error';
            let statusIcon = data.success ? '✅' : '❌';

            let html = `
                <div class="status ${statusClass}">
                    <h2>${statusIcon} ${testName} 結果</h2>
                    <p><strong>處理狀態:</strong> ${data.success ? '成功' : '失敗'}</p>
                    <p><strong>組件數量:</strong> ${data.components.length}</p>
                    <p><strong>錯誤數量:</strong> ${data.errors.length}</p>
                    <p><strong>服務器處理時間:</strong> ${(data.processing_time * 1000).toFixed(2)}ms</p>
                    <p><strong>客戶端時間:</strong> ${clientTime}ms</p>
                    <p><strong>總處理數:</strong> ${data.metadata.factory_stats?.total_processed || 'N/A'}</p>
                </div>
            `;

            if (data.errors.length > 0) {
                html += `<div class="error"><h3>錯誤信息:</h3><ul>`;
                data.errors.forEach(error => {
                    html += `<li>${error}</li>`;
                });
                html += `</ul></div>`;
            }

            html += `<h3>🎨 生成的組件:</h3>`;

            data.components.forEach((comp, index) => {
                const typeClass = comp.type.replace('_', '');
                html += `
                    <div class="component ${typeClass}">
                        <h4>${comp.title} (${comp.type})</h4>
                        <p><strong>ID:</strong> ${comp.id}</p>
                        <p><strong>創建時間:</strong> ${comp.created_at}</p>
                        ${comp.xai_summary ? `<p><strong>AI解釋:</strong> ${comp.xai_summary}</p>` : ''}

                        <details>
                            <summary>詳細數據</summary>
                            <pre>${JSON.stringify(comp.data, null, 2)}</pre>
                        </details>

                        <details>
                            <summary>元數據</summary>
                            <pre>${JSON.stringify(comp.metadata, null, 2)}</pre>
                        </details>
                    </div>
                `;
            });

            resultsDiv.innerHTML = html;
        }

        async function getStats() {
            try {
                const response = await axios.get('/api/stats');
                const stats = response.data;

                document.getElementById('stats').innerHTML = `
                    <h3>📊 系統統計</h3>
                    <p><strong>運行時間:</strong> ${(stats.uptime / 3600).toFixed(2)} 小時</p>
                    <p><strong>總處理數:</strong> ${stats.total_processed}</p>
                    <p><strong>錯誤數量:</strong> ${stats.error_count}</p>
                    <p><strong>成功率:</strong> ${stats.total_processed > 0 ? 
                        ((stats.total_processed - stats.error_count) / stats.total_processed * 100).toFixed(1) : 0}%</p>
                    <p><strong>類型分佈:</strong></p>
                    <ul>
                        ${Object.entries(stats.type_distribution).map(([type, count]) => 
                            `<li>${type}: ${count}</li>`
                        ).join('')}
                    </ul>
                `;
            } catch (error) {
                showError('統計獲取失敗: ' + error.message);
            }
        }

        function showLoading(message) {
            document.getElementById('results').innerHTML = 
                `<div style="text-align: center; padding: 40px;">⏳ ${message}</div>`;
        }

        function showError(message) {
            document.getElementById('results').innerHTML = 
                `<div class="error">❌ ${message}</div>`;
        }

        function clearResults() {
            document.getElementById('results').innerHTML = '';
        }

        // 頁面載入時獲取統計
        window.onload = function() {
            getStats();
        };
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn

    # 自動找到可用端口
    available_port = find_available_port()
    if not available_port:
        print("❌ 找不到可用端口 (8000-8009)")
        exit(1)

    print(f"🚀 啟動 FlexComponent System Stable")
    print(f"📡 API: http://localhost:{available_port}")
    print(f"📖 文檔: http://localhost:{available_port}/docs")
    print(f"🎨 演示: http://localhost:{available_port}/demo")
    print(f"📊 統計: http://localhost:{available_port}/api/stats")
    print(f"❤️  健康檢查: http://localhost:{available_port}/api/health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=available_port,
        reload=False,
        access_log=True
    )