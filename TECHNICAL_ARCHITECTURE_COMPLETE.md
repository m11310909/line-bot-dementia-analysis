# 🏗️ 技術架構與實作指南

## 1. 系統架構

### 1.1 整體架構圖
```
┌─────────────────────────────────────────────────────────────┐
│                         LINE Users                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    LINE Platform                            │
│  ┌──────────────┐        ┌──────────────┐                 │
│  │   Webhook    │        │     LIFF     │                 │
│  └──────┬───────┘        └──────┬───────┘                 │
└─────────┼────────────────────────┼─────────────────────────┘
          │                        │
          ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────────────────────────────────────────┐      │
│  │            LINE Bot Service (Port 8081)         │      │
│  │  ├── Webhook Handler                           │      │
│  │  ├── Message Processor                         │      │
│  │  └── Flex Message Builder                      │      │
│  └──────────────────┬──────────────────────────────┘      │
│                     │                                       │
│  ┌─────────────────▼──────────────────────────────┐      │
│  │         XAI Wrapper Service (Port 8005)        │      │
│  │  ├── Module Detector                           │      │
│  │  ├── XAI Analyzer                              │      │
│  │  └── Visualization Generator                    │      │
│  └──────────────────┬──────────────────────────────┘      │
└─────────────────────┼───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    External Services                        │
│  ┌─────────────────────────────────────────────────┐      │
│  │          失智小幫手 Chatbot API                  │      │
│  └─────────────────────────────────────────────────┘      │
│  ┌─────────────────────────────────────────────────┐      │
│  │              Gemini AI API                       │      │
│  └─────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │    Redis     │  │  PostgreSQL  │  │   FAISS      │    │
│  │   (Cache)    │  │  (Database)  │  │  (Vectors)   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 服務架構

```yaml
services:
  line-bot:
    container: line-bot:latest
    ports: [8081]
    dependencies: [xai-wrapper, redis]
    
  xai-wrapper:
    container: xai-wrapper:latest
    ports: [8005]
    dependencies: [redis, postgres]
    
  redis:
    container: redis:7-alpine
    ports: [6379]
    
  postgres:
    container: postgres:15-alpine
    ports: [5432]
    
  nginx:
    container: nginx:alpine
    ports: [80, 443]
    role: reverse-proxy
```

## 2. 核心模組實作

### 2.1 XAI Wrapper Service

```python
# services/xai-wrapper/app/main.py
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, Optional
import httpx
import asyncio
from datetime import datetime

app = FastAPI(title="XAI Wrapper Service")

class XAIWrapperService:
    def __init__(self):
        self.bot_api = DementiaBotClient()
        self.xai_analyzer = XAIAnalyzer()
        self.module_detector = ModuleDetector()
        self.viz_generator = VisualizationGenerator()
        self.cache = RedisCache()
        
    async def process_message(self, 
                              user_input: str, 
                              user_id: str,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        主要處理流程
        """
        # 1. 檢查快取
        cache_key = f"analysis:{hashlib.md5(user_input.encode()).hexdigest()}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # 2. 平行呼叫 APIs
        tasks = [
            self.bot_api.get_response(user_input),
            self.xai_analyzer.extract_keywords(user_input),
            self.xai_analyzer.classify_intent(user_input)
        ]
        bot_response, keywords, intent = await asyncio.gather(*tasks)
        
        # 3. 判斷模組
        module = self.module_detector.detect(
            user_input=user_input,
            keywords=keywords,
            intent=intent,
            bot_response=bot_response
        )
        
        # 4. 生成 XAI 資料
        xai_data = await self.xai_analyzer.analyze(
            user_input=user_input,
            bot_response=bot_response,
            module=module
        )
        
        # 5. 生成視覺化
        visualization = await self.viz_generator.generate(
            module=module,
            xai_data=xai_data
        )
        
        # 6. 組裝結果
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "module": module,
            "bot_response": bot_response,
            "xai_analysis": xai_data,
            "visualization": visualization,
            "confidence": xai_data["confidence"]
        }
        
        # 7. 快取結果
        await self.cache.set(cache_key, result, ttl=3600)
        
        return result
```

### 2.2 Module Detector

```python
# services/xai-wrapper/app/module_detector.py
from typing import List, Dict, Tuple
import numpy as np

class ModuleDetector:
    def __init__(self):
        self.module_patterns = {
            "M1": {
                "keywords": ["記憶", "忘記", "重複", "迷路", "時間混淆", 
                            "忘記吃藥", "記不住", "想不起來"],
                "intents": ["symptom_check", "memory_concern"],
                "weight": 1.0
            },
            "M2": {
                "keywords": ["階段", "病程", "早期", "中期", "晚期", 
                            "惡化", "進展", "變嚴重"],
                "intents": ["stage_inquiry", "progression_check"],
                "weight": 0.9
            },
            "M3": {
                "keywords": ["躁動", "妄想", "憂鬱", "幻覺", "攻擊",
                            "遊走", "不安", "情緒", "行為"],
                "intents": ["behavioral_symptom", "psychological_symptom"],
                "weight": 1.1  # 優先處理行為問題
            },
            "M4": {
                "keywords": ["照護", "資源", "申請", "補助", "日常",
                            "醫療", "任務", "協助"],
                "intents": ["care_guidance", "resource_inquiry"],
                "weight": 0.8
            }
        }
        
    def detect(self, 
               user_input: str, 
               keywords: List[str], 
               intent: str,
               bot_response: Dict) -> str:
        """
        判斷應使用的模組
        """
        scores = {}
        
        for module, pattern in self.module_patterns.items():
            # 關鍵詞匹配分數
            keyword_score = self._calculate_keyword_score(
                keywords, 
                pattern["keywords"]
            )
            
            # 意圖匹配分數
            intent_score = 1.0 if intent in pattern["intents"] else 0.3
            
            # 回應內容相關性
            response_score = self._analyze_response_relevance(
                bot_response.get("text", ""),
                pattern["keywords"]
            )
            
            # 加權總分
            total_score = (
                keyword_score * 0.4 + 
                intent_score * 0.3 + 
                response_score * 0.3
            ) * pattern["weight"]
            
            scores[module] = total_score
        
        # 選擇最高分模組
        selected = max(scores, key=scores.get)
        
        # 如果分數太低，預設使用 M1
        if scores[selected] < 0.3:
            return "M1"
            
        return selected
```

### 2.3 XAI Analyzer

```python
# services/xai-wrapper/app/xai_analyzer.py
from typing import Dict, List, Any
import jieba
import numpy as np

class XAIAnalyzer:
    def __init__(self):
        self.confidence_calculator = ConfidenceCalculator()
        self.reasoning_builder = ReasoningPathBuilder()
        
    async def analyze(self, 
                     user_input: str,
                     bot_response: Dict,
                     module: str) -> Dict[str, Any]:
        """
        執行 XAI 分析
        """
        # 1. 計算信心度
        confidence = await self.confidence_calculator.calculate(
            user_input=user_input,
            bot_response=bot_response,
            module=module
        )
        
        # 2. 建立推理路徑
        reasoning_path = self.reasoning_builder.build(
            user_input=user_input,
            module=module,
            confidence=confidence
        )
        
        # 3. 提取證據
        evidence = self._extract_evidence(user_input, bot_response)
        
        # 4. 生成解釋
        explanation = self._generate_explanation(
            module=module,
            confidence=confidence,
            evidence=evidence
        )
        
        return {
            "confidence": confidence,
            "reasoning_path": reasoning_path,
            "evidence": evidence,
            "explanation": explanation,
            "module_specific_data": self._get_module_data(module, evidence)
        }
    
    def _extract_evidence(self, 
                         user_input: str, 
                         bot_response: Dict) -> List[Dict]:
        """
        提取關鍵證據
        """
        # 使用 jieba 分詞
        words = jieba.cut(user_input)
        
        # 標記重要詞彙
        evidence = []
        importance_words = ["忘記", "重複", "迷路", "混淆", "躁動", "妄想"]
        
        for word in words:
            if word in importance_words:
                evidence.append({
                    "text": word,
                    "type": "keyword",
                    "importance": 0.8
                })
        
        return evidence
```

### 2.4 Visualization Generator

```python
# services/xai-wrapper/app/visualization_generator.py
from typing import Dict, Any
import json

class VisualizationGenerator:
    def __init__(self):
        self.flex_builder = FlexMessageBuilder()
        self.module_templates = self._load_templates()
        
    async def generate(self, 
                      module: str, 
                      xai_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成視覺化資料
        """
        if module == "M1":
            return await self._generate_m1_visualization(xai_data)
        elif module == "M2":
            return await self._generate_m2_visualization(xai_data)
        elif module == "M3":
            return await self._generate_m3_visualization(xai_data)
        elif module == "M4":
            return await self._generate_m4_visualization(xai_data)
        else:
            return await self._generate_default_visualization(xai_data)
    
    async def _generate_m1_visualization(self, xai_data: Dict) -> Dict:
        """
        M1 警訊比對視覺化
        """
        return {
            "flex_message": {
                "type": "comparison_card",
                "confidence_bar": {
                    "value": xai_data["confidence"],
                    "color": self._get_confidence_color(xai_data["confidence"])
                },
                "reasoning_path": {
                    "steps": [
                        {
                            "label": "關鍵詞",
                            "confidence": xai_data["reasoning_path"][0]["score"]
                        },
                        {
                            "label": "症狀比對",
                            "confidence": xai_data["reasoning_path"][1]["score"]
                        },
                        {
                            "label": "警訊判斷",
                            "confidence": xai_data["confidence"]
                        }
                    ]
                },
                "comparison": {
                    "normal": {
                        "title": "正常老化",
                        "items": ["偶爾忘記", "提醒後想起"],
                        "color": "#4CAF50"
                    },
                    "warning": {
                        "title": "失智警訊",
                        "items": ["影響生活", "重複發問"],
                        "color": "#FF9800"
                    }
                }
            },
            "liff_data": {
                "detailed_analysis": xai_data["explanation"],
                "similar_cases": await self._get_similar_cases(xai_data),
                "recommended_actions": self._get_recommendations(xai_data)
            }
        }
```

## 3. 資料庫架構

### 3.1 PostgreSQL Schema

```sql
-- 使用者互動記錄
CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_text TEXT NOT NULL,
    selected_module VARCHAR(10),
    confidence_score FLOAT,
    response_data JSONB,
    feedback_score INTEGER
);

-- 分析結果快取
CREATE TABLE analysis_cache (
    id SERIAL PRIMARY KEY,
    input_hash VARCHAR(64) UNIQUE NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);

-- 模組效能指標
CREATE TABLE module_metrics (
    id SERIAL PRIMARY KEY,
    module_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    avg_confidence FLOAT,
    avg_response_time FLOAT,
    satisfaction_score FLOAT,
    UNIQUE(module_id, date)
);

-- 索引優化
CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);
CREATE INDEX idx_analysis_cache_expires ON analysis_cache(expires_at);
CREATE INDEX idx_module_metrics_date ON module_metrics(date);
```

### 3.2 Redis 快取策略

```python
# Cache Configuration
CACHE_CONFIG = {
    "analysis_results": {
        "prefix": "analysis:",
        "ttl": 3600,  # 1 hour
        "max_size": 1000
    },
    "user_sessions": {
        "prefix": "session:",
        "ttl": 86400,  # 24 hours
        "max_size": 500
    },
    "module_templates": {
        "prefix": "template:",
        "ttl": 604800,  # 7 days
        "max_size": 100
    },
    "api_responses": {
        "prefix": "api:",
        "ttl": 300,  # 5 minutes
        "max_size": 200
    }
}
```

## 4. API 端點規格

### 4.1 LINE Bot Webhook

```yaml
POST /webhook
Headers:
  X-Line-Signature: <signature>
Body:
  events:
    - type: message
      message:
        type: text
        text: "媽媽最近常忘記吃藥"
      replyToken: <token>
      source:
        userId: <user_id>
Response:
  status: 200
  body: "OK"
```

### 4.2 XAI Analysis API

```yaml
POST /api/v1/analyze
Headers:
  Content-Type: application/json
Body:
  user_input: string
  user_id: string
  context: object (optional)
Response:
  module: string
  confidence: float
  visualization: object
  bot_response: object
  xai_analysis: object
```

### 4.3 Health Check

```yaml
GET /health
Response:
  status: "healthy"
  services:
    line_bot: boolean
    xai_wrapper: boolean
    redis: boolean
    postgres: boolean
  timestamp: ISO8601
```

## 5. 部署配置

### 5.1 Docker Compose

```yaml
version: '3.8'

services:
  line-bot:
    build: ./services/line-bot
    ports:
      - "8081:8081"
    environment:
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET}
      - XAI_SERVICE_URL=http://xai-wrapper:8005
    depends_on:
      xai-wrapper:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - dementia-network

  xai-wrapper:
    build: ./services/xai-wrapper
    ports:
      - "8005:8005"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - BOT_API_URL=${BOT_API_URL}
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://admin:${DB_PASSWORD}@postgres:5432/dementia_db
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8005/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - dementia-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped
    networks:
      - dementia-network

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=dementia_db
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "admin", "-d", "dementia_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - dementia-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - line-bot
      - xai-wrapper
    restart: unless-stopped
    networks:
      - dementia-network

networks:
  dementia-network:
    driver: bridge

volumes:
  redis_data:
  postgres_data:
```

### 5.2 環境變數

```bash
# .env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
GEMINI_API_KEY=your_gemini_api_key
BOT_API_URL=https://dementia-helper-api.com
DB_PASSWORD=secure_password_here
NGROK_AUTHTOKEN=your_ngrok_auth_token
LIFF_ID=your_liff_id
```

## 6. 監控與日誌

### 6.1 監控指標

```python
# Metrics to track
METRICS = {
    "response_time": {
        "unit": "seconds",
        "threshold": 3.0,
        "alert": True
    },
    "confidence_score": {
        "unit": "percentage",
        "threshold": 0.6,
        "alert": False
    },
    "error_rate": {
        "unit": "percentage",
        "threshold": 0.05,
        "alert": True
    },
    "module_accuracy": {
        "unit": "percentage",
        "threshold": 0.9,
        "alert": True
    }
}
```

### 6.2 日誌配置

```python
# Logging configuration
import logging
from logging.handlers import RotatingFileHandler

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "msg": "%(message)s"}'
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json"
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    }
}
```

## 7. 安全配置

### 7.1 LINE 簽名驗證

```python
import hmac
import hashlib
import base64

def verify_line_signature(body: str, signature: str, secret: str) -> bool:
    """
    驗證 LINE 請求簽名
    """
    hash = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    calculated_signature = base64.b64encode(hash).decode('utf-8')
    return calculated_signature == signature
```

### 7.2 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@app.post("/webhook")
@limiter.limit("30 per minute")
async def webhook(request: Request):
    # Handle webhook
    pass
```

## 8. 測試策略

### 8.1 單元測試

```python
# tests/test_module_detector.py
import pytest
from services.xai_wrapper.app.module_detector import ModuleDetector

def test_m1_detection():
    detector = ModuleDetector()
    result = detector.detect(
        user_input="媽媽最近常忘記吃藥",
        keywords=["忘記", "吃藥"],
        intent="symptom_check",
        bot_response={"text": "這可能是記憶力問題"}
    )
    assert result == "M1"
```

### 8.2 整合測試

```python
# tests/test_integration.py
import httpx
import pytest

@pytest.mark.asyncio
async def test_full_flow():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8005/api/v1/analyze",
            json={
                "user_input": "媽媽常常重複問同樣的問題",
                "user_id": "test_user"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["module"] == "M1"
        assert data["confidence"] > 0.6
```

## 9. 效能優化

### 9.1 快取策略

```python
class CacheManager:
    def __init__(self):
        self.redis = redis.Redis(
            connection_pool=redis.ConnectionPool(
                max_connections=50,
                decode_responses=True
            )
        )
    
    async def get_or_compute(self, key: str, compute_func, ttl: int = 3600):
        """
        快取或計算
        """
        # 嘗試從快取取得
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # 計算結果
        result = await compute_func()
        
        # 存入快取
        await self.redis.setex(
            key, 
            ttl, 
            json.dumps(result)
        )
        
        return result
```

### 9.2 並行處理

```python
async def parallel_api_calls(user_input: str):
    """
    平行呼叫多個 API
    """
    tasks = [
        call_dementia_bot_api(user_input),
        call_gemini_api(user_input),
        analyze_keywords(user_input)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 處理錯誤
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Task {i} failed: {result}")
            results[i] = None
    
    return results
```

## 10. 部署檢查清單

- [ ] 環境變數設置完成
- [ ] Docker images 建置成功
- [ ] 資料庫初始化完成
- [ ] Redis 連線測試通過
- [ ] LINE Webhook 驗證成功
- [ ] ngrok 隧道建立
- [ ] Health check 端點正常
- [ ] 日誌系統運作正常
- [ ] 監控系統啟動
- [ ] 備份策略實施

# 🚀 使用者工作流程與體驗旅程

## 1. 使用者旅程地圖

### 1.1 整體流程圖
```mermaid
journey
    title 失智症照護者使用旅程
    section 發現問題
      觀察異常行為: 3: 照護者
      產生擔憂: 2: 照護者
      尋求協助: 4: 照護者
    section 初次互動
      開啟 LINE: 5: 照護者
      輸入症狀描述: 4: 照護者
      等待回應: 3: 照護者
    section AI 分析
      接收快速摘要: 5: AI
      查看信心度: 4: AI
      理解推理過程: 4: AI
    section 深入了解
      點擊詳細分析: 4: 照護者
      閱讀完整報告: 4: 照護者
      獲得行動建議: 5: 照護者
    section 採取行動
      預約就醫: 5: 照護者
      調整照護: 4: 照護者
      持續追蹤: 4: 照護者
```

## 2. 詳細使用流程

### 2.1 Flow 1: 症狀評估流程 (M1)

```yaml
觸發場景: 家人出現記憶問題
使用者目標: 判斷是否需要就醫

步驟:
  1. 開啟 LINE:
     - 時間: 1秒
     - 動作: 點擊失智小幫手對話
     
  2. 描述症狀:
     - 時間: 30秒
     - 輸入: "媽媽最近常常忘記吃藥，剛說過的話馬上就忘記"
     - 心理: 焦慮、擔心
     
  3. AI 即時回應:
     - 時間: 2秒內
     - 顯示: Flex Message
     - 內容:
       - AI 信心度: 82%
       - 推理路徑: 關鍵詞→症狀比對→警訊判斷
       - 對比卡片: 正常老化 vs 失智警訊
       
  4. 查看詳細分析:
     - 時間: 用戶決定
     - 動作: 點擊 "查看完整分析報告"
     - 跳轉: LIFF 頁面
     
  5. 獲得指引:
     - 內容: 
       - 完整十大警訊對照
       - 建議就醫科別
       - 準備就醫資料清單
       
預期結果: 使用者明確知道下一步行動
```

### 2.2 Flow 2: 病程了解流程 (M2)

```yaml
觸發場景: 已確診，想了解病程
使用者目標: 預期管理和資源準備

步驟:
  1. 詢問階段:
     - 輸入: "失智症中期會有什麼症狀？"
     
  2. AI 階段評估:
     - 顯示: 階段時間軸
     - 標記: 當前可能階段
     - 列出: 階段特徵
     
  3. 深入了解:
     - 查看: 詳細症狀矩陣
     - 了解: 照護重點變化
     - 準備: 未來需求
     
預期結果: 使用者對未來有心理準備
```

### 2.3 Flow 3: 行為處理流程 (M3)

```yaml
觸發場景: 出現困擾行為症狀
使用者目標: 獲得立即可用的處理方法

步驟:
  1. 描述行為:
     - 輸入: "爸爸最近晚上都很躁動，一直想出門"
     
  2. AI 症狀分類:
     - 顯示: BPSD 分類卡片
     - 標記: 躁動不安 75%
     - 提供: 立即建議
     
  3. 查看處理建議:
     - 環境調整技巧
     - 溝通方式建議
     - 何時需要醫療介入
     
預期結果: 照護者能立即嘗試建議方法
```

### 2.4 Flow 4: 任務管理流程 (M4)

```yaml
觸發場景: 不知道該做什麼
使用者目標: 有條理地處理照護事務

步驟:
  1. 尋求指引:
     - 輸入: "確診失智症後該做什麼？"
     
  2. AI 任務導航:
     - 顯示: 優先級任務列表
     - 分類: 醫療/日常/社交
     - 標記: 緊急/建議/可選
     
  3. 追蹤進度:
     - 查看: 整體完成度
     - 設定: 提醒事項
     - 獲得: 資源連結
     
預期結果: 照護者有明確的行動清單
```

## 3. 介面互動細節

### 3.1 LINE 聊天介面

```
使用者體驗要素:
  輸入:
    - 支援語音轉文字
    - 常用詞快速回覆
    - 歷史記錄參考
    
  等待:
    - 顯示輸入中指示
    - 3秒內必須回應
    - 處理中動畫
    
  接收:
    - Flex Message 呈現
    - 視覺層次清晰
    - 可點擊互動元素
```

### 3.2 Flex Message 互動

```yaml
視覺層級:
  Level 1 - 立即可見:
    - 模組標題 (記憶力評估)
    - AI 信心度 (82%)
    - 核心結論 (可能為失智警訊)
    
  Level 2 - 稍微瀏覽:
    - 推理路徑
    - 對比資訊
    - 關鍵證據
    
  Level 3 - 主動探索:
    - 詳細分析按鈕
    - 相關資源連結
    - 回饋選項

互動元素:
  按鈕:
    - 主要 CTA: "查看完整分析"
    - 次要選項: "不準確" / "很有幫助"
    
  Carousel (M3):
    - 左右滑動查看不同症狀
    - 每張卡片獨立互動
```

### 3.3 LIFF 頁面體驗

```yaml
載入優化:
  - 骨架屏顯示
  - 漸進式內容載入
  - 關鍵資訊優先

導航設計:
  頂部:
    - 返回聊天室
    - 當前模組標示
    
  內容區:
    - 摘要卡片
    - 詳細分析
    - 視覺化圖表
    - 行動建議
    
  底部:
    - 相關資源
    - 聯絡專業協助

無障礙設計:
  - 字體大小可調
  - 高對比模式
  - 語音朗讀支援
```

## 4. 關鍵決策點

### 4.1 信任建構節點

```mermaid
graph TD
    A[使用者輸入] -->|2秒內| B[快速回應]
    B --> C{信心度判斷}
    C -->|>80%| D[顯示完整分析]
    C -->|60-80%| E[顯示分析+提醒]
    C -->|<60%| F[建議人工諮詢]
    D --> G[展示推理過程]
    E --> G
    G --> H[使用者信任建立]
```

### 4.2 降級策略

```yaml
場景 1 - API 延遲:
  條件: 回應時間 > 3秒
  動作: 
    - 顯示預設回應
    - 標記 "AI 處理中"
    - 提供基本建議

場景 2 - 低信心度:
  條件: 信心度 < 60%
  動作:
    - 純文字回應
    - 建議人工諮詢
    - 提供緊急聯絡

場景 3 - Flex 失敗:
  條件: Flex Message 錯誤
  動作:
    - 降級為文字訊息
    - 保留核心資訊
    - 簡化互動選項
```

## 5. 使用者回饋循環

### 5.1 即時回饋

```yaml
觸發時機:
  - 每次 AI 回應後
  - LIFF 頁面底部
  
回饋選項:
  快速評分:
    - 👍 有幫助
    - 👎 不準確
    
  詳細回饋:
    - 哪裡不準確
    - 需要什麼資訊
    - 使用體驗問題
```

### 5.2 追蹤指標

```yaml
使用者行為:
  - 點擊率: Flex → LIFF
  - 停留時間: LIFF 頁面
  - 完成率: 建議行動
  
滿意度:
  - 回饋評分
  - 重複使用率
  - 推薦意願
  
效果評估:
  - 就醫轉換率
  - 照護改善度
  - 壓力減輕程度
```

## 6. 個人化體驗

### 6.1 學習使用者偏好

```python
user_preferences = {
    "detail_level": "progressive",  # minimal, moderate, detailed
    "visual_preference": "high",    # text, balanced, visual
    "language_style": "caring",     # formal, casual, caring
    "reminder_frequency": "daily"   # none, weekly, daily
}
```

### 6.2 情境感知調整

```yaml
時間感知:
  深夜 (22:00-06:00):
    - 簡化資訊
    - 緊急選項優先
    - 降低視覺刺激
    
  白天 (09:00-17:00):
    - 完整功能
    - 詳細分析
    - 資源連結
    
使用頻率:
  新使用者:
    - 引導教學
    - 簡單案例
    - 鼓勵探索
    
  常用使用者:
    - 快速路徑
    - 進階功能
    - 歷史參考
```

## 7. 緊急情況處理

### 7.1 危機識別

```yaml
觸發條件:
  - 關鍵詞: "自殺", "傷害", "攻擊"
  - 情緒指標: 極度焦慮、恐慌
  - 行為描述: 暴力、自傷

立即回應:
  1. 優先顯示:
     - 緊急聯絡電話
     - 24小時專線
     - 最近醫院
     
  2. 簡化選項:
     - 立即撥打 119
     - 聯絡家醫
     - 心理諮詢
     
  3. 持續支援:
     - 保持對話
     - 提供安撫
     - 記錄狀況
```

## 8. 多語言支援

### 8.1 語言切換

```yaml
支援語言:
  - 繁體中文 (預設)
  - 簡體中文
  - 英文
  - 印尼文 (外籍看護)
  
切換方式:
  - 自動偵測
  - 手動選擇
  - 記憶偏好
```

## 9. 離線功能

### 9.1 基礎快取

```yaml
離線可用:
  - 最近查詢結果
  - 基本照護指南
  - 緊急聯絡資訊
  - 常見問題解答
  
同步策略:
  - WiFi 自動更新
  - 手動重新整理
  - 背景同步
```

## 10. 成功案例流程

### 案例：王太太的使用經驗

```
Day 1 - 初次發現
時間: 晚上 8:30
輸入: "先生今天又忘記我是誰"
回應: M1 警訊比對 → 建議就醫
行動: 預約神經內科

Day 7 - 確診後
輸入: "醫生說是輕度失智"
回應: M2 病程說明 → 階段指引
行動: 了解未來準備

Day 30 - 行為問題
輸入: "半夜一直要出門"
回應: M3 症狀處理 → 環境調整
結果: 症狀改善

Day 60 - 資源需求
輸入: "需要申請什麼補助"
回應: M4 任務導航 → 資源清單
成果: 成功申請長照資源
```

這個使用者工作流程確保：
- ✅ 快速獲得幫助（3秒內）
- ✅ 容易理解（視覺化）
- ✅ 可以信任（透明推理）
- ✅ 能夠行動（具體建議）
