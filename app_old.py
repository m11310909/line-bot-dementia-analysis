# 修復 Pydantic V2 兼容性問題
# 將這部分程式碼替換你 app.py 中的 ChunkInput 類別

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, List, Optional, Union
import uuid
import time
import json
import asyncio
from datetime import datetime
from enum import Enum
import logging

# ===== 修復後的數據模型 =====
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

    @field_validator('confidence')
    @classmethod
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

# ===== 建立修復版本的完整 app.py =====
print("建立修復版本的 app.py...")

fixed_app_content = '''
# fixed_app.py - 修復版本的 FlexComponent 系統
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

# ===== 組件工廠 (簡化版，穩定可靠) =====
class StableComponentFactory:
    def __init__(self):
        self.type_mapping = {
            'comparison': ComponentType.COMPARISON_CARD,
            'confidence': ComponentType.CONFIDENCE_METER,
            'explanation': ComponentType.XAI_BOX,
            'info': ComponentType.INFO_BOX,
            'action': ComponentType.ACTION_CARD,
        }

        self.stats = {
            'total_processed': 0,
            'type_distribution': {t: 0 for t in ComponentType},
            'error_count': 0
        }

    async def create_component(self, chunk: ChunkInput, xai_data: Optional[XAIInput] = None) -> ComponentOutput:
        try:
            component_type = self._determine_type(chunk)
            component_data = self._format_data(chunk, component_type, xai_data)

            self.stats['total_processed'] += 1
            self.stats['type_distribution'][component_type] += 1

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
        if any(keyword in content_str for keyword in ['compare', 'vs', '比較']):
            return ComponentType.COMPARISON_CARD
        elif any(keyword in content_str for keyword in ['confidence', 'probability', '信心']):
            return ComponentType.CONFIDENCE_METER
        elif any(keyword in content_str for keyword in ['explanation', 'reasoning', '解釋']):
            return ComponentType.XAI_BOX
        elif any(keyword in content_str for keyword in ['action', 'todo', '行動']):
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
            base_data["comparison_data"] = chunk.content.get('options', chunk.content)
            base_data["layout"] = {"columns": 2, "highlight_differences": True}

        elif comp_type == ComponentType.CONFIDENCE_METER:
            confidence = chunk.confidence or (xai_data.confidence_score if xai_data else 0.5)
            base_data.update({
                "confidence_value": confidence,
                "confidence_level": self._get_confidence_level(confidence),
                "uncertainty_factors": xai_data.uncertainty_factors if xai_data else []
            })

        elif comp_type == ComponentType.XAI_BOX:
            base_data.update({
                "explanation": xai_data.explanation if xai_data else chunk.content.get('explanation', ''),
                "reasoning_steps": xai_data.reasoning_steps if xai_data else [],
                "feature_importance": self._format_feature_importance(xai_data)
            })

        elif comp_type == ComponentType.ACTION_CARD:
            actions = chunk.content.get('actions', [])
            if isinstance(chunk.content, list):
                actions = chunk.content
            base_data.update({
                "actions": actions,
                "priority": chunk.metadata.get('priority', 'medium')
            })

        return base_data

    def _get_confidence_level(self, confidence: float) -> str:
        if confidence >= 0.8: return "高"
        elif confidence >= 0.6: return "中"
        elif confidence >= 0.4: return "低"
        else: return "很低"

    def _format_feature_importance(self, xai_data: Optional[XAIInput]) -> List[Dict[str, Any]]:
        if not xai_data or not xai_data.feature_importance:
            return []

        return [
            {
                "feature": feature,
                "importance": importance,
                "impact": "正面" if importance > 0 else "負面"
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
            data={"error": error_msg, "fallback": True},
            metadata={"error": True, "created_at": datetime.now().isoformat()},
            created_at=datetime.now()
        )

    def get_stats(self) -> Dict[str, Any]:
        return self.stats.copy()

# ===== 端口檢查工具 =====
def find_available_port(start_port=8000, max_attempts=10):
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
    description="智能組件系統穩定版",
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
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/components", response_model=ProcessingResult)
async def create_components(request: ComponentRequest):
    processing_start = time.time()

    try:
        tasks = []
        for i, chunk in enumerate(request.chunks):
            xai_data = None
            if request.xai_data and i < len(request.xai_data):
                xai_data = request.xai_data[i]

            task = factory.create_component(chunk, xai_data)
            tasks.append(task)

        components = await asyncio.gather(*tasks, return_exceptions=True)

        successful_components = []
        errors = []

        for i, component in enumerate(components):
            if isinstance(component, Exception):
                errors.append(f"Chunk {i} 處理失敗: {str(component)}")
            else:
                successful_components.append(component)

        processing_time = time.time() - processing_start

        return ProcessingResult(
            success=len(errors) == 0,
            components=successful_components,
            errors=errors,
            processing_time=processing_time,
            metadata={
                "total_chunks": len(request.chunks),
                "successful_components": len(successful_components),
                "factory_stats": factory.get_stats(),
                "timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        logger.error(f"請求處理失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0",
        "uptime": time.time() - start_time,
        "factory_stats": factory.get_stats()
    }

@app.get("/api/stats")
async def get_stats():
    stats = factory.get_stats()
    stats.update({
        "uptime": time.time() - start_time,
        "server_status": "running",
        "last_updated": datetime.now().isoformat()
    })
    return stats

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlexComponent Stable Demo</title>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .component { border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; }
            button { background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; margin: 5px; }
            button:hover { background: #0056b3; }
            .stats { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FlexComponent Stable Demo</h1>
            <p>穩定版智能組件系統 - 修復所有已知問題</p>

            <div class="stats" id="stats"></div>

            <button onclick="runTest()">運行測試</button>
            <button onclick="getStats()">查看統計</button>

            <div id="results"></div>
        </div>

        <script>
        async function runTest() {
            document.getElementById('results').innerHTML = '<p>⏳ 處理中...</p>';

            const testData = {
                chunks: [
                    {
                        type: "comparison",
                        title: "穩定版測試",
                        content: {
                            options: {
                                "舊版本": {"穩定性": "中", "功能": "基礎"},
                                "新版本": {"穩定性": "高", "功能": "完整"}
                            }
                        },
                        confidence: 0.95
                    },
                    {
                        type: "confidence",
                        title: "系統信心度",
                        content: {"system": "stable"},
                        confidence: 0.98
                    }
                ]
            };

            try {
                const response = await axios.post('/api/components', testData);
                const result = response.data;

                let html = `<h2>✅ 測試結果</h2>
                           <p>成功: ${result.success}</p>
                           <p>組件數: ${result.components.length}</p>
                           <p>處理時間: ${(result.processing_time * 1000).toFixed(2)}ms</p>`;

                result.components.forEach(comp => {
                    html += `<div class="component">
                               <h3>${comp.title} (${comp.type})</h3>
                               <pre>${JSON.stringify(comp.data, null, 2)}</pre>
                             </div>`;
                });

                document.getElementById('results').innerHTML = html;
            } catch (error) {
                document.getElementById('results').innerHTML = 
                    '<p style="color: red;">❌ 測試失敗: ' + error.message + '</p>';
            }
        }

        async function getStats() {
            try {
                const response = await axios.get('/api/stats');
                const stats = response.data;

                document.getElementById('stats').innerHTML = `
                    <h3>📊 系統統計</h3>
                    <p>運行時間: ${(stats.uptime / 3600).toFixed(2)} 小時</p>
                    <p>總處理數: ${stats.total_processed}</p>
                    <p>錯誤數量: ${stats.error_count}</p>
                `;
            } catch (error) {
                console.error('統計獲取失敗:', error);
            }
        }

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

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=available_port,
        reload=False,
        access_log=True
    )
'''

# 將修復版本寫入文件
with open('app_fixed.py', 'w', encoding='utf-8') as f:
    f.write(fixed_app_content.strip())

print("✅ 修復版本已建立為 app_fixed.py")
print("")
print("🎯 現在執行以下步驟："
print("1. mv app.py app_old.py          # 備份舊版本")  
print("2. mv app_fixed.py app.py        # 使用修復版本")
print("3. python app.py                 # 啟動服務")
print("")
print("🔧 修復內容:")
print("• 將 @validator 改為 @field_validator (Pydantic V2)")
print("• 添加自動端口檢測功能")
print("• 簡化組件工廠，提高穩定性")
print("• 改善錯誤處理機制")