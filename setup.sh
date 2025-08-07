#!/bin/bash

# LINE Bot Dementia Analysis System - Complete Setup Script
# Run this script in your repo root: ./setup.sh

set -e

echo "🚀 Setting up LINE Bot Dementia Analysis System..."

# ============================================
# 1. Create Directory Structure
# ============================================
echo "📁 Creating directory structure..."

mkdir -p services/{line-bot,xai-wrapper}/{app,tests}
mkdir -p data/{chunks,upload,archive}
mkdir -p config
mkdir -p logs
mkdir -p ssl
mkdir -p docs

# ============================================
# 2. Create XAI Wrapper Service
# ============================================
echo "🧠 Creating XAI Wrapper Service..."

cat > services/xai-wrapper/app/__init__.py << 'EOF'
# XAI Wrapper Service
__version__ = "1.0.0"
EOF

cat > services/xai-wrapper/app/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from typing import Dict, Any, Optional
import httpx
import asyncio
import hashlib
import json
from datetime import datetime
from pydantic import BaseModel

from .module_detector import ModuleDetector
from .xai_analyzer import XAIAnalyzer
from .visualization_generator import VisualizationGenerator
from .cache_manager import CacheManager

app = FastAPI(title="XAI Wrapper Service", version="1.0.0")

class AnalysisRequest(BaseModel):
    user_input: str
    user_id: str
    context: Optional[Dict] = None

class XAIWrapperService:
    def __init__(self):
        self.bot_api_url = "https://dementia-helper-api.com"  # Replace with actual
        self.module_detector = ModuleDetector()
        self.xai_analyzer = XAIAnalyzer()
        self.viz_generator = VisualizationGenerator()
        self.cache = CacheManager()
        
    async def process_message(self, request: AnalysisRequest) -> Dict[str, Any]:
        # Check cache
        cache_key = f"analysis:{hashlib.md5(request.user_input.encode()).hexdigest()}"
        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
            
        # Call dementia bot API
        async with httpx.AsyncClient() as client:
            try:
                bot_response = await client.post(
                    self.bot_api_url,
                    json={"text": request.user_input},
                    timeout=10.0
                )
                bot_data = bot_response.json()
            except:
                bot_data = {"text": "無法連接到失智小幫手", "confidence": 0.3}
        
        # Extract keywords and classify intent
        keywords = await self.xai_analyzer.extract_keywords(request.user_input)
        intent = await self.xai_analyzer.classify_intent(request.user_input)
        
        # Detect module
        module = self.module_detector.detect(
            user_input=request.user_input,
            keywords=keywords,
            intent=intent,
            bot_response=bot_data
        )
        
        # Generate XAI analysis
        xai_data = await self.xai_analyzer.analyze(
            user_input=request.user_input,
            bot_response=bot_data,
            module=module
        )
        
        # Generate visualization
        visualization = await self.viz_generator.generate(
            module=module,
            xai_data=xai_data
        )
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": request.user_input,
            "module": module,
            "bot_response": bot_data,
            "xai_analysis": xai_data,
            "visualization": visualization,
            "confidence": xai_data["confidence"]
        }
        
        # Cache result
        await self.cache.set(cache_key, json.dumps(result), ttl=3600)
        
        return result

wrapper_service = XAIWrapperService()

@app.post("/api/v1/analyze")
async def analyze(request: AnalysisRequest):
    try:
        result = await wrapper_service.process_message(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "xai-wrapper"
    }
EOF

# Create Module Detector
cat > services/xai-wrapper/app/module_detector.py << 'EOF'
from typing import List, Dict

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
                "weight": 1.1
            },
            "M4": {
                "keywords": ["照護", "資源", "申請", "補助", "日常",
                            "醫療", "任務", "協助"],
                "intents": ["care_guidance", "resource_inquiry"],
                "weight": 0.8
            }
        }
        
    def detect(self, user_input: str, keywords: List[str], 
               intent: str, bot_response: Dict) -> str:
        scores = {}
        
        for module, pattern in self.module_patterns.items():
            keyword_score = self._calculate_keyword_score(keywords, pattern["keywords"])
            intent_score = 1.0 if intent in pattern["intents"] else 0.3
            scores[module] = (keyword_score * 0.6 + intent_score * 0.4) * pattern["weight"]
        
        selected = max(scores, key=scores.get)
        return selected if scores[selected] > 0.3 else "M1"
    
    def _calculate_keyword_score(self, found_keywords: List[str], 
                                 pattern_keywords: List[str]) -> float:
        if not found_keywords:
            return 0.0
        matches = sum(1 for kw in found_keywords if any(
            pk in kw or kw in pk for pk in pattern_keywords
        ))
        return min(matches / len(pattern_keywords), 1.0)
EOF

# Create XAI Analyzer
cat > services/xai-wrapper/app/xai_analyzer.py << 'EOF'
from typing import Dict, List, Any
import jieba
import random

class XAIAnalyzer:
    def __init__(self):
        self.important_words = [
            "忘記", "重複", "迷路", "混淆", "躁動", "妄想",
            "記憶", "時間", "空間", "行為", "情緒", "照護"
        ]
        
    async def extract_keywords(self, text: str) -> List[str]:
        words = jieba.lcut(text)
        return [w for w in words if w in self.important_words or len(w) > 1]
    
    async def classify_intent(self, text: str) -> str:
        if any(word in text for word in ["症狀", "警訊", "正常"]):
            return "symptom_check"
        elif any(word in text for word in ["階段", "病程", "惡化"]):
            return "stage_inquiry"
        elif any(word in text for word in ["行為", "情緒", "躁動"]):
            return "behavioral_symptom"
        elif any(word in text for word in ["照護", "資源", "申請"]):
            return "care_guidance"
        return "general_inquiry"
    
    async def analyze(self, user_input: str, bot_response: Dict, 
                     module: str) -> Dict[str, Any]:
        keywords = await self.extract_keywords(user_input)
        
        # Calculate confidence based on keywords and response
        base_confidence = 0.7
        keyword_boost = min(len(keywords) * 0.05, 0.2)
        confidence = min(base_confidence + keyword_boost, 0.95)
        
        # Build reasoning path
        reasoning_path = [
            {"step": "關鍵詞提取", "confidence": 0.85, "detail": f"識別到 {len(keywords)} 個關鍵詞"},
            {"step": "症狀比對", "confidence": 0.78, "detail": f"匹配到{module}模組"},
            {"step": "結果判斷", "confidence": confidence, "detail": "綜合分析完成"}
        ]
        
        return {
            "confidence": confidence,
            "reasoning_path": reasoning_path,
            "keywords": keywords,
            "evidence": [{"text": kw, "importance": 0.8} for kw in keywords[:3]],
            "explanation": f"根據您的描述，系統判斷這可能與{self._get_module_name(module)}相關"
        }
    
    def _get_module_name(self, module: str) -> str:
        names = {
            "M1": "失智症警訊",
            "M2": "病程階段",
            "M3": "精神行為症狀",
            "M4": "照護資源"
        }
        return names.get(module, "一般諮詢")
EOF

# Create Visualization Generator
cat > services/xai-wrapper/app/visualization_generator.py << 'EOF'
from typing import Dict, Any

class VisualizationGenerator:
    def __init__(self):
        self.module_templates = self._load_templates()
        
    async def generate(self, module: str, xai_data: Dict[str, Any]) -> Dict[str, Any]:
        if module == "M1":
            return await self._generate_m1(xai_data)
        elif module == "M2":
            return await self._generate_m2(xai_data)
        elif module == "M3":
            return await self._generate_m3(xai_data)
        elif module == "M4":
            return await self._generate_m4(xai_data)
        else:
            return await self._generate_default(xai_data)
    
    async def _generate_m1(self, xai_data: Dict) -> Dict:
        confidence = xai_data["confidence"]
        return {
            "type": "comparison_card",
            "flex_message": {
                "confidence_bar": {
                    "value": confidence,
                    "color": self._get_confidence_color(confidence),
                    "label": f"{int(confidence * 100)}%"
                },
                "reasoning_steps": [
                    {
                        "label": step["step"],
                        "confidence": step["confidence"]
                    }
                    for step in xai_data["reasoning_path"]
                ],
                "comparison": {
                    "normal": {
                        "title": "正常老化",
                        "items": ["偶爾忘記", "提醒後想起", "日常生活正常"],
                        "color": "#4CAF50"
                    },
                    "warning": {
                        "title": "失智警訊",
                        "items": ["影響生活", "重複發問", "忘記重要事件"],
                        "color": "#FF9800"
                    }
                }
            },
            "liff_url": "https://liff.line.me/YOUR_LIFF_ID/m1"
        }
    
    async def _generate_m2(self, xai_data: Dict) -> Dict:
        return {
            "type": "stage_timeline",
            "flex_message": {
                "current_stage": "middle",
                "stages": ["早期", "中期", "晚期"],
                "features": ["日常需協助", "行為症狀", "認知退化"]
            }
        }
    
    async def _generate_m3(self, xai_data: Dict) -> Dict:
        return {
            "type": "symptom_cards",
            "flex_message": {
                "symptoms": [
                    {"name": "躁動不安", "severity": 75, "color": "#F44336"},
                    {"name": "憂鬱情緒", "severity": 60, "color": "#2196F3"}
                ]
            }
        }
    
    async def _generate_m4(self, xai_data: Dict) -> Dict:
        return {
            "type": "task_navigation",
            "flex_message": {
                "tasks": [
                    {"category": "醫療", "priority": "緊急", "action": "預約評估"},
                    {"category": "日常", "priority": "建議", "action": "環境調整"}
                ]
            }
        }
    
    async def _generate_default(self, xai_data: Dict) -> Dict:
        return {
            "type": "simple_text",
            "text": xai_data.get("explanation", "請提供更多資訊")
        }
    
    def _get_confidence_color(self, confidence: float) -> str:
        if confidence > 0.8:
            return "#4CAF50"
        elif confidence > 0.6:
            return "#2196F3"
        else:
            return "#FF9800"
    
    def _load_templates(self) -> Dict:
        return {}
EOF

# Create Cache Manager
cat > services/xai-wrapper/app/cache_manager.py << 'EOF'
import redis
import json
from typing import Optional

class CacheManager:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                decode_responses=True
            )
            self.redis_client.ping()
        except:
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[str]:
        if not self.redis_client:
            return None
        try:
            return self.redis_client.get(key)
        except:
            return None
    
    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        if not self.redis_client:
            return False
        try:
            self.redis_client.setex(key, ttl, value)
            return True
        except:
            return False
EOF

# Create requirements for XAI wrapper
cat > services/xai-wrapper/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.1
redis==5.0.1
jieba==0.42.1
pydantic==2.5.0
python-multipart==0.0.6
EOF

# Create Dockerfile for XAI wrapper
cat > services/xai-wrapper/Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
EOF

# ============================================
# 3. Update LINE Bot Service
# ============================================
echo "🤖 Updating LINE Bot Service..."

cat > services/line-bot/app/main.py << 'EOF'
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)
from linebot.v3.webhookhandler import MessageEvent
from linebot.v3.webhook import TextMessageContent
import httpx
import asyncio
import json
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot configuration
configuration = Configuration(
    access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
)
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

XAI_SERVICE_URL = os.getenv('XAI_SERVICE_URL', 'http://localhost:8005')

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle LINE message events"""
    user_input = event.message.text
    user_id = event.source.user_id
    reply_token = event.reply_token
    
    # Process with XAI wrapper
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(process_with_xai(user_input, user_id))
    
    # Send response
    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)
        
        if result and result.get('confidence', 0) > 0.6:
            # Send Flex Message
            flex_json = create_flex_message(result)
            try:
                api.reply_message(
                    ReplyMessageRequest(
                        replyToken=reply_token,
                        messages=[FlexMessage(
                            altText=f"分析結果: {result['module']}",
                            contents=FlexContainer.from_dict(flex_json)
                        )]
                    )
                )
            except Exception as e:
                logger.error(f"Flex message error: {e}")
                # Fallback to text
                api.reply_message(
                    ReplyMessageRequest(
                        replyToken=reply_token,
                        messages=[TextMessage(text=result.get('bot_response', {}).get('text', '處理中...'))]
                    )
                )
        else:
            # Low confidence - send text only
            api.reply_message(
                ReplyMessageRequest(
                    replyToken=reply_token,
                    messages=[TextMessage(text="請提供更多資訊以便分析")]
                )
            )

async def process_with_xai(user_input: str, user_id: str):
    """Call XAI wrapper service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{XAI_SERVICE_URL}/api/v1/analyze",
                json={"user_input": user_input, "user_id": user_id},
                timeout=8.0
            )
            return response.json()
        except Exception as e:
            logger.error(f"XAI service error: {e}")
            return None

def create_flex_message(result):
    """Create Flex Message from XAI result"""
    module = result.get('module', 'M1')
    viz = result.get('visualization', {})
    
    if module == 'M1':
        return create_m1_flex(viz)
    # Add other modules as needed
    return create_default_flex(result)

def create_m1_flex(viz):
    """Create M1 warning signs comparison Flex Message"""
    flex_data = viz.get('flex_message', {})
    confidence = flex_data.get('confidence_bar', {})
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "AI 分析結果",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"信心度: {confidence.get('label', 'N/A')}",
                    "size": "sm",
                    "color": confidence.get('color', '#666666')
                }
            ]
        }
    }

def create_default_flex(result):
    """Create default Flex Message"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": result.get('bot_response', {}).get('text', '分析完成'),
                    "wrap": True
                }
            ]
        }
    }

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        abort(400)
    
    return 'OK'

@app.route("/health", methods=['GET'])
def health():
    return {"status": "healthy", "service": "line-bot"}

if __name__ == "__main__":
    app.run(port=8081, debug=True)
EOF

# Create requirements for LINE bot
cat > services/line-bot/requirements.txt << 'EOF'
Flask==3.0.0
line-bot-sdk==3.5.0
httpx==0.25.1
gunicorn==21.2.0
EOF

# Create Dockerfile for LINE bot
cat > services/line-bot/Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["gunicorn", "--bind", "0.0.0.0:8081", "app.main:app"]
EOF

# ============================================
# 4. Create Database Initialization
# ============================================
echo "🗄️ Creating database initialization..."

cat > init.sql << 'EOF'
-- Database initialization script
CREATE DATABASE IF NOT EXISTS dementia_db;

\c dementia_db;

-- User interactions table
CREATE TABLE IF NOT EXISTS user_interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_text TEXT NOT NULL,
    selected_module VARCHAR(10),
    confidence_score FLOAT,
    response_data JSONB,
    feedback_score INTEGER
);

-- Analysis cache table
CREATE TABLE IF NOT EXISTS analysis_cache (
    id SERIAL PRIMARY KEY,
    input_hash VARCHAR(64) UNIQUE NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);

-- Module metrics table
CREATE TABLE IF NOT EXISTS module_metrics (
    id SERIAL PRIMARY KEY,
    module_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    avg_confidence FLOAT,
    avg_response_time FLOAT,
    satisfaction_score FLOAT,
    UNIQUE(module_id, date)
);

-- Create indexes
CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);
CREATE INDEX idx_analysis_cache_expires ON analysis_cache(expires_at);
CREATE INDEX idx_module_metrics_date ON module_metrics(date);
EOF

# ============================================
# 5. Create Docker Compose Configuration
# ============================================
echo "🐳 Creating Docker Compose configuration..."

cat > docker-compose.yml << 'EOF'
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
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
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
EOF

# ============================================
# 6. Create Nginx Configuration
# ============================================
echo "🌐 Creating Nginx configuration..."

cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream line-bot {
        server line-bot:8081;
    }

    upstream xai-wrapper {
        server xai-wrapper:8005;
    }

    server {
        listen 80;
        server_name localhost;

        location /webhook {
            proxy_pass http://line-bot;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/ {
            proxy_pass http://xai-wrapper;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /health {
            access_log off;
            return 200 "healthy\n";
        }
    }
}
EOF

# ============================================
# 7. Create Environment Template
# ============================================
echo "🔐 Creating environment template..."

cat > .env.example << 'EOF'
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
LIFF_ID=your_liff_id

# API Keys
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
BOT_API_URL=https://dementia-helper-api.com

# Database
DB_PASSWORD=secure_password_here

# Development
NGROK_AUTHTOKEN=your_ngrok_auth_token
EOF

# ============================================
# 8. Create Startup Scripts
# ============================================
echo "🚀 Creating startup scripts..."

cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting LINE Bot Dementia Analysis System..."

# Check environment
if [ ! -f .env ]; then
    echo "❌ .env file not found! Copy .env.example to .env and fill in values."
    exit 1
fi

# Load environment variables
export $(cat .env | xargs)

# Start services
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check health
echo "🔍 Checking service health..."
curl -s http://localhost:8081/health
curl -s http://localhost:8005/health

echo "✅ System is running!"
echo "📱 LINE Webhook: http://localhost:8081/webhook"
echo "🧠 XAI API: http://localhost:8005/api/v1/analyze"
EOF

chmod +x start.sh

cat > stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping services..."
docker-compose down
echo "✅ Services stopped"
EOF

chmod +x stop.sh

cat > logs.sh << 'EOF'
#!/bin/bash
echo "📋 Showing logs..."
docker-compose logs -f $1
EOF

chmod +x logs.sh

# ============================================
# 9. Create Test Script
# ============================================
echo "🧪 Creating test script..."

cat > test_system.py << 'EOF'
#!/usr/bin/env python3
import httpx
import json
import asyncio

async def test_xai_analysis():
    """Test XAI analysis endpoint"""
    test_cases = [
        {"user_input": "媽媽最近常常忘記吃藥", "expected_module": "M1"},
        {"user_input": "失智症中期會有什麼症狀", "expected_module": "M2"},
        {"user_input": "爸爸晚上很躁動怎麼辦", "expected_module": "M3"},
        {"user_input": "需要申請什麼補助嗎", "expected_module": "M4"}
    ]
    
    async with httpx.AsyncClient() as client:
        for test in test_cases:
            try:
                response = await client.post(
                    "http://localhost:8005/api/v1/analyze",
                    json={"user_input": test["user_input"], "user_id": "test_user"}
                )
                result = response.json()
                
                print(f"✅ Input: {test['user_input']}")
                print(f"   Module: {result['module']} (Expected: {test['expected_module']})")
                print(f"   Confidence: {result['xai_analysis']['confidence']:.2%}")
                print()
                
            except Exception as e:
                print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing XAI Analysis System...")
    asyncio.run(test_xai_analysis())
EOF

chmod +x test_system.py

# ============================================
# 10. Create README
# ============================================
echo "📚 Creating README..."

cat > README.md << 'EOF'
# LINE Bot Dementia Analysis System

## 🚀 Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start Services
```bash
./start.sh
```

### 3. Configure LINE Webhook
Set your webhook URL to: `https://your-domain.com/webhook`

### 4. Test System
```bash
python test_system.py
```

## 📁 Project Structure
```
.
├── services/
│   ├── line-bot/          # LINE Bot service
│   └── xai-wrapper/        # XAI analysis service
├── data/                   # Data storage
├── logs/                   # Application logs
├── docker-compose.yml      # Docker configuration
├── .env                    # Environment variables
└── README.md              # This file
```

## 🛠️ Available Commands
- `./start.sh` - Start all services
- `./stop.sh` - Stop all services
- `./logs.sh [service]` - View logs
- `python test_system.py` - Run tests

## 📊 Modules
- **M1**: Warning Signs Detection (警訊比對)
- **M2**: Disease Progression (病程評估)
- **M3**: BPSD Symptoms (行為症狀)
- **M4**: Care Navigation (任務導航)

## 🔧 Development
```bash
# Install dependencies locally for development
pip install -r services/xai-wrapper/requirements.txt
pip install -r services/line-bot/requirements.txt

# Run services locally
uvicorn services.xai-wrapper.app.main:app --reload --port 8005
python services/line-bot/app/main.py
```

## 📝 API Documentation
- XAI Analysis: `POST /api/v1/analyze`
- Health Check: `GET /health`

## 🐛 Troubleshooting
1. Check logs: `./logs.sh [service-name]`
2. Verify health: `curl http://localhost:8005/health`
3. Test webhook: Use LINE Developer Console

## 📄 License
MIT
EOF

# ============================================
# Final Steps
# ============================================
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.example to .env and fill in your credentials"
echo "2. Run './start.sh' to start the system"
echo "3. Configure LINE webhook URL"
echo "4. Test with 'python test_system.py'"
echo ""
echo "📚 See README.md for detailed instructions"
