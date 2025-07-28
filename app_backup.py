# enhanced_app.py - 增強版組件系統
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional, Union
import uuid
import time
import json
import asyncio
from datetime import datetime
from enum import Enum
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== 增強版數據模型 =====
class ComponentType(str, Enum):
    COMPARISON_CARD = "comparison_card"
    CONFIDENCE_METER = "confidence_meter"
    XAI_BOX = "xai_box"
    INFO_BOX = "info_box"
    ACTION_CARD = "action_card"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ChunkInput(BaseModel):
    type: str = Field(..., description="Chunk 類型")
    title: Optional[str] = Field(None, description="組件標題")
    content: Dict[str, Any] = Field(..., description="內容數據")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元數據")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="信心度")

    @validator('confidence')
    def validate_confidence(cls, v):
        if v is not None and not 0 <= v <= 1:
            raise ValueError('信心度必須在 0-1 之間')
        return v

class XAIInput(BaseModel):
    """XAI 解釋數據"""
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

# ===== 增強版組件工廠 =====
class AdvancedComponentFactory:
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

        # 關鍵詞權重
        self.keyword_weights = {
            ComponentType.COMPARISON_CARD: {
                'vs': 3, 'versus': 3, 'compare': 3, 'comparison': 3,
                'option': 2, 'alternative': 2, '比較': 3, '對比': 3,
                'A vs B': 4, 'before_after': 2
            },
            ComponentType.CONFIDENCE_METER: {
                'confidence': 3, 'certainty': 2, 'probability': 3,
                'likelihood': 2, 'score': 1, '信心': 3, '確定性': 2,
                'accuracy': 2, 'precision': 2
            },
            ComponentType.XAI_BOX: {
                'explanation': 3, 'reasoning': 3, 'why': 2, 'because': 2,
                'factors': 2, 'analysis': 2, '解釋': 3, '原因': 2,
                'interpret': 2, 'understand': 2
            },
            ComponentType.ACTION_CARD: {
                'action': 3, 'todo': 3, 'task': 3, 'recommendation': 3,
                'next_step': 2, 'plan': 2, '行動': 3, '任務': 3,
                'implement': 2, 'execute': 2
            }
        }

        self.processing_stats = {
            'total_processed': 0,
            'type_distribution': {t: 0 for t in ComponentType},
            'error_count': 0
        }

    async def create_component(self, chunk: ChunkInput, xai_data: Optional[XAIInput] = None) -> ComponentOutput:
        """異步創建組件"""
        try:
            component_type = await self._determine_type_async(chunk)
            component_data = await self._format_data_async(chunk, component_type, xai_data)

            # 更新統計
            self.processing_stats['total_processed'] += 1
            self.processing_stats['type_distribution'][component_type] += 1

            return ComponentOutput(
                type=component_type.value,
                id=f"{component_type.value}_{str(uuid.uuid4())[:8]}",
                title=chunk.title or self._generate_default_title(component_type),
                data=component_data,
                metadata={
                    "created_at": datetime.now().isoformat(),
                    "original_type": chunk.type,
                    "has_confidence": chunk.confidence is not None,
                    "has_xai": xai_data is not None,
                    "inference_confidence": await self._calculate_inference_confidence(chunk, component_type)
                },
                created_at=datetime.now(),
                xai_summary=xai_data.explanation if xai_data else None
            )

        except Exception as e:
            self.processing_stats['error_count'] += 1
            logger.error(f"組件創建失敗: {e}")
            return await self._create_error_component(chunk, str(e))

    async def _determine_type_async(self, chunk: ChunkInput) -> ComponentType:
        """異步類型判斷"""
        # 直接映射
        chunk_type = chunk.type.lower().strip()
        if chunk_type in self.type_mapping:
            return self.type_mapping[chunk_type]

        # 智能推斷
        content_str = str(chunk.content).lower()
        title_str = (chunk.title or "").lower()
        metadata_str = str(chunk.metadata).lower()

        combined_text = f"{content_str} {title_str} {metadata_str}"

        # 計算各類型分數
        type_scores = {}
        for comp_type, keywords in self.keyword_weights.items():
            score = 0
            for keyword, weight in keywords.items():
                count = combined_text.count(keyword.lower())
                score += count * weight

            # 結構化分析加分
            score += await self._structural_analysis_async(chunk, comp_type)

            if score > 0:
                type_scores[comp_type] = score

        # 返回最高分數類型，否則默認 INFO_BOX
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            logger.info(f"推斷類型: {best_type} (分數: {type_scores[best_type]})")
            return best_type

        return ComponentType.INFO_BOX

    async def _structural_analysis_async(self, chunk: ChunkInput, comp_type: ComponentType) -> int:
        """異步結構化分析"""
        score = 0
        content = chunk.content

        if comp_type == ComponentType.COMPARISON_CARD:
            if isinstance(content, dict):
                if 'options' in content and len(content['options']) >= 2:
                    score += 5
                elif len(content) >= 2:
                    score += 3

        elif comp_type == ComponentType.CONFIDENCE_METER:
            if chunk.confidence is not None:
                score += 5
            if any(key in content for key in ['score', 'percentage', 'rate', 'accuracy']):
                score += 3

        elif comp_type == ComponentType.XAI_BOX:
            explanation_fields = ['explanation', 'reasoning', 'analysis', 'factors', 'why']
            for field in explanation_fields:
                if field in content:
                    score += 3

        elif comp_type == ComponentType.ACTION_CARD:
            if isinstance(content, dict) and 'actions' in content:
                if isinstance(content['actions'], list) and len(content['actions']) > 0:
                    score += 5
            if 'priority' in chunk.metadata:
                score += 2

        return score

    async def _format_data_async(self, chunk: ChunkInput, comp_type: ComponentType, xai_data: Optional[XAIInput]) -> Dict[str, Any]:
        """異步數據格式化"""
        base_data = {
            "title": chunk.title,
            "content": chunk.content,
            "confidence": chunk.confidence,
            "metadata": chunk.metadata
        }

        if comp_type == ComponentType.COMPARISON_CARD:
            base_data.update({
                "comparison_data": await self._format_comparison_data(chunk.content),
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
                "feature_importance": await self._format_feature_importance(xai_data),
                "confidence_score": xai_data.confidence_score if xai_data else chunk.confidence,
                "interactive": {
                    "expandable": True,
                    "show_details": True,
                    "highlight_key_factors": True
                }
            })

        elif comp_type == ComponentType.ACTION_CARD:
            actions = await self._extract_actions(chunk.content)
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

    async def _format_comparison_data(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """格式化比較數據"""
        if 'options' in content:
            return content['options']
        elif isinstance(content, dict) and len(content) >= 2:
            return content
        else:
            return {"項目": content}

    async def _format_feature_importance(self, xai_data: Optional[XAIInput]) -> List[Dict[str, Any]]:
        """格式化特徵重要性"""
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

    async def _extract_actions(self, content: Dict[str, Any]) -> List[str]:
        """提取行動項目"""
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
        """獲取信心度等級"""
        if confidence >= 0.8:
            return "高"
        elif confidence >= 0.6:
            return "中"
        elif confidence >= 0.4:
            return "低"
        else:
            return "很低"

    def _get_color_scheme(self, confidence: float) -> str:
        """獲取顏色方案"""
        if confidence >= 0.7:
            return "green"
        elif confidence >= 0.5:
            return "yellow"
        else:
            return "red"

    def _generate_default_title(self, comp_type: ComponentType) -> str:
        """生成默認標題"""
        titles = {
            ComponentType.COMPARISON_CARD: "比較分析",
            ComponentType.CONFIDENCE_METER: "信心度評估",
            ComponentType.XAI_BOX: "AI 解釋",
            ComponentType.INFO_BOX: "信息摘要",
            ComponentType.ACTION_CARD: "行動建議"
        }
        return titles.get(comp_type, "未命名組件")

    async def _calculate_inference_confidence(self, chunk: ChunkInput, comp_type: ComponentType) -> float:
        """計算推斷信心度"""
        # 簡化的信心度計算
        base_confidence = 0.5

        # 如果有明確的類型映射，信心度較高
        if chunk.type.lower() in self.type_mapping:
            base_confidence += 0.3

        # 根據關鍵詞匹配度調整
        content_str = str(chunk.content).lower()
        if comp_type in self.keyword_weights:
            keyword_matches = sum(
                1 for keyword in self.keyword_weights[comp_type].keys()
                if keyword.lower() in content_str
            )
            base_confidence += min(0.2, keyword_matches * 0.05)

        return min(1.0, base_confidence)

    async def _create_error_component(self, chunk: ChunkInput, error_msg: str) -> ComponentOutput:
        """創建錯誤組件"""
        return ComponentOutput(
            type=ComponentType.INFO_BOX.value,
            id=f"error_{str(uuid.uuid4())[:8]}",
            title="組件創建錯誤",
            data={
                "error": error_msg,
                "original_chunk": chunk.dict(),
                "fallback": True
            },
            metadata={
                "error": True,
                "created_at": datetime.now().isoformat()
            },
            created_at=datetime.now()
        )

    def get_stats(self) -> Dict[str, Any]:
        """獲取處理統計"""
        return self.processing_stats.copy()

# ===== FastAPI 應用 =====
app = FastAPI(
    title="FlexComponent System - Enhanced",
    description="智能組件系統增強版",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局實例
factory = AdvancedComponentFactory()
start_time = time.time()

# ===== API 路由 =====
@app.get("/")
async def root():
    return {
        "message": "FlexComponent System Enhanced - v2.0",
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
    """創建組件端點 - 增強版"""
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
        "version": "2.0.0",
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

# Demo 頁面
@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """增強版演示頁面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlexComponent Enhanced Demo</title>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .component { border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background: #fff; }
            .comparison { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .confidence { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
            .xai { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
            .action { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; }
            .info { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
            button { background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
            .stats { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FlexComponent Enhanced Demo</h1>
            <p>智能組件系統增強版 - 支援異步處理、XAI 整合、智能推斷</p>

            <div class="stats" id="stats"></div>

            <button onclick="runBasicDemo()">基礎演示</button>
            <button onclick="runAdvancedDemo()">高級演示 (含 XAI)</button>
            <button onclick="runStressTest()">壓力測試</button>
            <button onclick="getStats()">查看統計</button>

            <div id="results"></div>
        </div>

        <script>
        async function runBasicDemo() {
            showLoading();
            const testData = {
                chunks: [
                    {
                        type: "comparison",
                        title: "產品方案比較",
                        content: {
                            options: {
                                "標準版": {"價格": "$99", "功能": "基礎", "支援": "郵件"},
                                "專業版": {"價格": "$199", "功能": "完整", "支援": "24/7"}
                            }
                        },
                        confidence: 0.92
                    },
                    {
                        type: "confidence",
                        title: "預測準確度",
                        content: {"model": "RandomForest", "dataset": "customer_data"},
                        confidence: 0.78
                    },
                    {
                        type: "action",
                        title: "下週任務清單",
                        content: {
                            actions: [
                                "完成產品原型設計",
                                "安排用戶訪談",
                                "準備投資者簡報",
                                "優化系統性能"
                            ]
                        },
                        metadata: {"priority": "high"}
                    }
                ]
            };

            await executeRequest(testData);
        }

        async function runAdvancedDemo() {
            showLoading();
            const testData = {
                chunks: [
                    {
                        type: "explanation",
                        title: "市場策略分析",
                        content: {"strategy": "market_penetration"},
                        confidence: 0.85
                    }
                ],
                xai_data: [
                    {
                        explanation: "基於過去5年市場數據和競爭對手分析，建議採用滲透定價策略",
                        confidence_score: 0.85,
                        feature_importance: {
                            "市場規模": 0.35,
                            "競爭強度": 0.28,
                            "客戶需求": 0.22,
                            "成本結構": 0.15
                        },
                        reasoning_steps: [
                            "分析目標市場規模和增長潛力",
                            "評估主要競爭對手的定價策略",
                            "調研客戶價格敏感度",
                            "計算不同定價策略的預期回報"
                        ],
                        uncertainty_factors: ["市場波動", "競爭對手反應", "經濟環境變化"]
                    }
                ]
            };

            await executeRequest(testData);
        }

        async function runStressTest() {
            showLoading();
            const chunks = [];
            for (let i = 0; i < 10; i++) {
                chunks.push({
                    type: ["comparison", "confidence", "info", "action", "explanation"][i % 5],
                    title: `測試組件 ${i + 1}`,
                    content: {
                        test_data: `stress_test_${i}`,
                        value: Math.random()
                    },
                    confidence: Math.random()
                });
            }

            await executeRequest({chunks});
        }

        async function executeRequest(testData) {
            try {
                const startTime = Date.now();
                const response = await axios.post('/api/components', testData);
                const endTime = Date.now();

                displayResults(response.data, endTime - startTime);
            } catch (error) {
                document.getElementById('results').innerHTML = 
                    '<div style="color: red; padding: 20px;">❌ 請求失敗: ' + error.message + '</div>';
            }
        }

        function displayResults(data, clientTime) {
            const resultsDiv = document.getElementById('results');

            let html = `
                <h2>🎯 處理結果</h2>
                <div class="stats">
                    <strong>處理狀態:</strong> ${data.success ? '✅ 成功' : '❌ 失敗'}<br>
                    <strong>組件數量:</strong> ${data.components.length}<br>
                    <strong>錯誤數量:</strong> ${data.errors.length}<br>
                    <strong>服務器處理時間:</strong> ${(data.processing_time * 1000).toFixed(2)}ms<br>
                    <strong>客戶端時間:</strong> ${clientTime}ms<br>
                    <strong>總處理數:</strong> ${data.metadata.factory_stats?.total_processed || 'N/A'}
                </div>
            `;

            if (data.errors.length > 0) {
                html += `<div style="color: red; margin: 10px 0;"><h3>錯誤信息:</h3><ul>`;
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
                    <strong>運行時間:</strong> ${(stats.uptime / 3600).toFixed(2)} 小時<br>
                    <strong>總處理數:</strong> ${stats.total_processed}<br>
                    <strong>錯誤數量:</strong> ${stats.error_count}<br>
                    <strong>成功率:</strong> ${stats.total_processed > 0 ? 
                        ((stats.total_processed - stats.error_count) / stats.total_processed * 100).toFixed(1) : 0}%<br>
                    <strong>類型分佈:</strong><br>
                    ${Object.entries(stats.type_distribution).map(([type, count]) => 
                        `&nbsp;&nbsp;• ${type}: ${count}`
                    ).join('<br>')}
                `;
            } catch (error) {
                document.getElementById('stats').innerHTML = 
                    '<div style="color: red;">統計獲取失敗: ' + error.message + '</div>';
            }
        }

        function showLoading() {
            document.getElementById('results').innerHTML = 
                '<div style="text-align: center; padding: 40px;">⏳ 處理中...</div>';
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

    print("🚀 啟動 FlexComponent System Enhanced")
    print("📡 API: http://localhost:8000")
    print("📖 文檔: http://localhost:8000/docs")
    print("🎨 演示: http://localhost:8000/demo")
    print("📊 統計: http://localhost:8000/api/stats")
    print("❤️  健康檢查: http://localhost:8000/api/health")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        access_log=True
    )