# 建立 backend/main.py
echo "🚀 建立 backend/main.py..."
cat > backend/main.py << 'EOF'
"""
FlexComponent System - Pinecode 版本
整合所有功能的輕量級 FastAPI 應用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import uuid
import time
from datetime import datetime
import json

# ===== 數據模型 =====
class ChunkInput(BaseModel):
    type: str = Field(..., description="Chunk 類型")
    title: Optional[str] = Field(None, description="組件標題")
    content: Dict[str, Any] = Field(..., description="內容數據")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = Field(None, ge=0, le=1)

class ComponentRequest(BaseModel):
    chunks: List[ChunkInput] = Field(..., description="要處理的數據塊")

class ComponentOutput(BaseModel):
    type: str
    id: str
    title: str
    data: Dict[str, Any]
    metadata: Dict[str, Any]

class ProcessingResult(BaseModel):
    success: bool
    components: List[ComponentOutput]
    errors: List[str] = Field(default_factory=list)
    processing_time: float
    metadata: Dict[str, Any]

# ===== 組件工廠 =====
class SimpleComponentFactory:
    def __init__(self):
        self.type_mapping = {
            'comparison': 'comparison_card',
            'confidence': 'confidence_meter',
            'explanation': 'xai_box',
            'info': 'info_box',
            'action': 'action_card'
        }
    
    def create_component(self, chunk: ChunkInput) -> ComponentOutput:
        """創建組件"""
        component_type = self._determine_type(chunk)
        
        return ComponentOutput(
            type=component_type,
            id=f"{component_type}_{str(uuid.uuid4())[:8]}",
            title=chunk.title or "未命名組件",
            data=self._format_data(chunk, component_type),
            metadata={
                "created_at": datetime.now().isoformat(),
                "original_type": chunk.type,
                "has_confidence": chunk.confidence is not None
            }
        )
    
    def _determine_type(self, chunk: ChunkInput) -> str:
        """判斷組件類型"""
        chunk_type = chunk.type.lower()
        
        # 直接映射
        if chunk_type in self.type_mapping:
            return self.type_mapping[chunk_type]
        
        # 關鍵詞推斷
        content_str = str(chunk.content).lower()
        if any(keyword in content_str for keyword in ['compare', 'vs', '比較']):
            return 'comparison_card'
        elif any(keyword in content_str for keyword in ['confidence', 'probability', '信心']):
            return 'confidence_meter'
        elif any(keyword in content_str for keyword in ['explanation', 'reasoning', '解釋']):
            return 'xai_box'
        elif any(keyword in content_str for keyword in ['action', 'todo', '行動']):
            return 'action_card'
        else:
            return 'info_box'
    
    def _format_data(self, chunk: ChunkInput, component_type: str) -> Dict[str, Any]:
        """格式化數據"""
        base_data = {
            "title": chunk.title,
            "content": chunk.content,
            "confidence": chunk.confidence
        }
        
        if component_type == 'comparison_card':
            base_data.update({
                "comparison_data": chunk.content.get('options', chunk.content),
                "layout": {"columns": 2, "highlight_differences": True}
            })
        elif component_type == 'confidence_meter':
            confidence = chunk.confidence or 0.5
            base_data.update({
                "confidence_value": confidence,
                "confidence_level": self._get_confidence_level(confidence),
                "display": {"show_numeric": True, "show_bars": True}
            })
        elif component_type == 'action_card':
            actions = chunk.content.get('actions', [])
            if isinstance(chunk.content, list):
                actions = chunk.content
            base_data.update({
                "actions": actions,
                "priority": chunk.metadata.get('priority', 'medium')
            })
        
        return base_data
    
    def _get_confidence_level(self, confidence: float) -> str:
        if confidence >= 0.8:
            return "高"
        elif confidence >= 0.6:
            return "中"
        elif confidence >= 0.4:
            return "低"
        else:
            return "很低"

# ===== FastAPI 應用 =====
app = FastAPI(
    title="FlexComponent System - Pinecode Version",
    description="智能組件系統 - Pinecode 優化版",
    version="1.0.0"
)

# CORS 設置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 組件工廠實例
factory = SimpleComponentFactory()

# ===== API 路由 =====
@app.get("/")
async def root():
    """根路由"""
    return {
        "message": "FlexComponent System - Pinecode Version",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs"
    }

@app.post("/api/components", response_model=ProcessingResult)
async def create_components(request: ComponentRequest):
    """創建組件端點"""
    start_time = time.time()
    components = []
    errors = []
    
    try:
        for i, chunk in enumerate(request.chunks):
            try:
                component = factory.create_component(chunk)
                components.append(component)
            except Exception as e:
                errors.append(f"Chunk {i} error: {str(e)}")
        
        processing_time = time.time() - start_time
        
        return ProcessingResult(
            success=len(errors) == 0,
            components=components,
            errors=errors,
            processing_time=processing_time,
            metadata={
                "total_chunks": len(request.chunks),
                "successful_components": len(components),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-pinecode"
    }

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """演示頁面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FlexComponent Demo</title>
        <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .component { border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background: #fafafa; }
            .component h3 { color: #333; margin-top: 0; }
            button { background: #007bff; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px 5px; }
            button:hover { background: #0056b3; }
            .error { color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; }
            .success { color: #155724; background: #d4edda; padding: 10px; border-radius: 5px; }
            pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat { background: #e9ecef; padding: 10px; border-radius: 5px; text-align: center; flex: 1; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 FlexComponent System - Pinecode Demo</h1>
            <p>智能組件系統演示頁面，支援多種組件類型的動態生成</p>
            
            <div>
                <button onclick="runBasicDemo()">基礎演示</button>
                <button onclick="runAdvancedDemo()">進階演示</button>
                <button onclick="runPerformanceTest()">性能測試</button>
                <button onclick="clearResults()">清除結果</button>
            </div>
            
            <div id="stats" class="stats" style="display: none;">
                <div class="stat">
                    <strong id="componentCount">0</strong><br>
                    <small>組件數量</small>
                </div>
                <div class="stat">
                    <strong id="processingTime">0ms</strong><br>
                    <small>處理時間</small>
                </div>
                <div class="stat">
                    <strong id="successRate">0%</strong><br>
                    <small>成功率</small>
                </div>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
        async function runBasicDemo() {
            const testData = {
                chunks: [
                    {
                        type: "comparison",
                        title: "方案比較分析",
                        content: {
                            options: {
                                "方案A": {"價格": "$100", "效果": "高", "風險": "低"},
                                "方案B": {"價格": "$80", "效果": "中", "風險": "中"},
                                "方案C": {"價格": "$60", "效果": "低", "風險": "高"}
                            }
                        },
                        confidence: 0.85
                    },
                    {
                        type: "confidence",
                        title: "預測信心度",
                        content: {"prediction": "成功機率評估", "details": "基於歷史數據分析"},
                        confidence: 0.75
                    }
                ]
            };
            
            await sendRequest(testData, '基礎演示');
        }
        
        async function runAdvancedDemo() {
            const testData = {
                chunks: [
                    {
                        type: "explanation",
                        title: "AI 決策解釋",
                        content: {
                            reasoning: "基於多因子分析模型",
                            factors: ["歷史表現", "市場趨勢", "風險評估"],
                            conclusion: "建議採用混合策略"
                        },
                        confidence: 0.92
                    },
                    {
                        type: "action",
                        title: "建議行動項目",
                        content: {
                            actions: [
                                "立即執行風險評估",
                                "3天內完成方案比較",
                                "1週內制定實施計劃"
                            ]
                        },
                        metadata: {"priority": "high"}
                    },
                    {
                        type: "info",
                        title: "重要資訊",
                        content: {
                            message: "系統運行正常",
                            details: "所有模組已啟動並正常運行",
                            timestamp: new Date().toISOString()
                        }
                    }
                ]
            };
            
            await sendRequest(testData, '進階演示');
        }
        
        async function runPerformanceTest() {
            const chunks = [];
            for (let i = 0; i < 10; i++) {
                chunks.push({
                    type: ["comparison", "confidence", "explanation", "action", "info"][i % 5],
                    title: `測試組件 ${i + 1}`,
                    content: {
                        test_data: `性能測試數據 ${i + 1}`,
                        value: Math.random()
                    },
                    confidence: Math.random()
                });
            }
            
            await sendRequest({chunks}, '性能測試');
        }
        
        async function sendRequest(testData, demoType) {
            const resultsDiv = document.getElementById('results');
            const statsDiv = document.getElementById('stats');
            
            resultsDiv.innerHTML = '<p>⏳ 處理中...</p>';
            
            try {
                const startTime = Date.now();
                const response = await axios.post('/api/components', testData);
                const endTime = Date.now();
                const clientTime = endTime - startTime;
                
                // 更新統計信息
                document.getElementById('componentCount').textContent = response.data.components.length;
                document.getElementById('processingTime').textContent = Math.round(response.data.processing_time * 1000) + 'ms';
                document.getElementById('successRate').textContent = response.data.success ? '100%' : '部分成功';
                statsDiv.style.display = 'flex';
                
                // 顯示結果
                let html = `<div class="success">✅ ${demoType}完成！處理時間: ${Math.round(response.data.processing_time * 1000)}ms (服務端) + ${clientTime}ms (網路)</div>`;
                
                if (response.data.errors.length > 0) {
                    html += '<div class="error">⚠️ 錯誤: ' + response.data.errors.join(', ') + '</div>';
                }
                
                html += '<h2>🎨 生成的組件:</h2>';
                html += response.data.components.map((comp, index) => 
                    `<div class="component">
                        <h3>${comp.title} <small>(${comp.type})</small></h3>
                        <p><strong>ID:</strong> ${comp.id}</p>
                        <p><strong>創建時間:</strong> ${comp.metadata.created_at}</p>
                        <details>
                            <summary>📊 組件數據</summary>
                            <pre>${JSON.stringify(comp.data, null, 2)}</pre>
                        </details>
                    </div>`
                ).join('');
                
                resultsDiv.innerHTML = html;
                
            } catch (error) {
                console.error('Error:', error);
                resultsDiv.innerHTML = `<div class="error">❌ 請求失敗: ${error.message}</div>`;
                statsDiv.style.display = 'none';
            }
        }
        
        function clearResults() {
            document.getElementById('results').innerHTML = '';
            document.getElementById('stats').style.display = 'none';
        }
        </script>
    </body>
    </html>
    """

# ===== 主程序 =====
if __name__ == "__main__":
    import uvicorn
    print("🚀 啟動 FlexComponent System - Pinecode Version")
    print("📡 API: http://localhost:8000")
    print("📖 文檔: http://localhost:8000/docs")
    print("🎨 演示: http://localhost:8000/demo")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=False
    )
EOF
