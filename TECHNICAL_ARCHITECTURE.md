# 🏗️ LINE Bot Dementia Analysis System - Technical Architecture

## 1. System Overview

### 1.1 Architecture Diagram
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

## 2. Core Services

### 2.1 LINE Bot Service (Port 8081)
- **Purpose**: Handle LINE webhook events and send responses
- **Key Components**:
  - Webhook Handler
  - Message Processor
  - Flex Message Builder
- **Dependencies**: XAI Wrapper Service, Redis

### 2.2 XAI Wrapper Service (Port 8005)
- **Purpose**: Analyze user input and generate explanations
- **Key Components**:
  - Module Detector (M1-M4)
  - XAI Analyzer
  - Visualization Generator
  - Cache Manager
- **Dependencies**: Redis, PostgreSQL, External APIs

### 2.3 Data Services
- **Redis**: Caching and session management
- **PostgreSQL**: User interactions and analytics
- **FAISS**: Vector similarity search

## 3. Module System

### 3.1 Module Detection Logic
```python
MODULE_PATTERNS = {
    "M1": {
        "keywords": ["記憶", "忘記", "重複", "迷路", "時間混淆"],
        "intents": ["symptom_check", "memory_concern"],
        "weight": 1.0
    },
    "M2": {
        "keywords": ["階段", "病程", "早期", "中期", "晚期"],
        "intents": ["stage_inquiry", "progression_check"],
        "weight": 0.9
    },
    "M3": {
        "keywords": ["躁動", "妄想", "憂鬱", "幻覺", "攻擊"],
        "intents": ["behavioral_symptom", "psychological_symptom"],
        "weight": 1.1
    },
    "M4": {
        "keywords": ["照護", "資源", "申請", "補助", "日常"],
        "intents": ["care_guidance", "resource_inquiry"],
        "weight": 0.8
    }
}
```

### 3.2 Module Functions
- **M1**: Warning Signs Detection (警訊比對)
- **M2**: Disease Progression (病程評估)
- **M3**: BPSD Symptoms (行為症狀)
- **M4**: Care Navigation (任務導航)

## 4. User Workflow

### 4.1 Message Processing Flow
```mermaid
graph TD
    A[User Input] --> B[LINE Webhook]
    B --> C[XAI Analysis]
    C --> D[Module Detection]
    D --> E[Generate Response]
    E --> F[Send Flex Message]
    F --> G[User Receives]
```

### 4.2 XAI Analysis Process
1. **Keyword Extraction**: Use jieba for Chinese text processing
2. **Intent Classification**: Determine user's primary intent
3. **Module Selection**: Score-based module detection
4. **Confidence Calculation**: Based on keywords and patterns
5. **Visualization Generation**: Create appropriate Flex Message
6. **Response Assembly**: Combine all components

## 5. API Endpoints

### 5.1 LINE Bot Webhook
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
```

### 5.2 XAI Analysis API
```yaml
POST /api/v1/analyze
Body:
  user_input: string
  user_id: string
  context: object (optional)
Response:
  module: string
  confidence: float
  visualization: object
  xai_analysis: object
```

## 6. Database Schema

### 6.1 User Interactions
```sql
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
```

### 6.2 Analysis Cache
```sql
CREATE TABLE analysis_cache (
    id SERIAL PRIMARY KEY,
    input_hash VARCHAR(64) UNIQUE NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);
```

## 7. Deployment Configuration

### 7.1 Docker Compose Services
```yaml
services:
  line-bot:
    build: ./services/line-bot
    ports: ["8081:8081"]
    environment:
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET}
    
  xai-wrapper:
    build: ./services/xai-wrapper
    ports: ["8005:8005"]
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://admin:${DB_PASSWORD}@postgres:5432/dementia_db
    
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    
  postgres:
    image: postgres:15-alpine
    ports: ["5432:5432"]
    environment:
      - POSTGRES_DB=dementia_db
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=${DB_PASSWORD}
```

### 7.2 Environment Variables
```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
LIFF_ID=your_liff_id

# API Keys
GEMINI_API_KEY=your_gemini_api_key
BOT_API_URL=https://dementia-helper-api.com

# Database
DB_PASSWORD=secure_password_here
```

## 8. Monitoring & Logging

### 8.1 Key Metrics
- Response Time (target: < 3 seconds)
- Confidence Score (target: > 60%)
- Error Rate (target: < 5%)
- Module Accuracy (target: > 90%)

### 8.2 Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8005/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 9. Security Considerations

### 9.1 LINE Signature Verification
```python
def verify_line_signature(body: str, signature: str, secret: str) -> bool:
    hash = hmac.new(
        secret.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).digest()
    calculated_signature = base64.b64encode(hash).decode('utf-8')
    return calculated_signature == signature
```

### 9.2 Rate Limiting
```python
@limiter.limit("30 per minute")
async def webhook(request: Request):
    # Handle webhook
    pass
```

## 10. Testing Strategy

### 10.1 Unit Tests
```python
def test_m1_detection():
    detector = ModuleDetector()
    result = detector.detect(
        user_input="媽媽最近常忘記吃藥",
        keywords=["忘記", "吃藥"],
        intent="symptom_check"
    )
    assert result == "M1"
```

### 10.2 Integration Tests
```python
async def test_full_flow():
    response = await client.post(
        "http://localhost:8005/api/v1/analyze",
        json={"user_input": "媽媽常常重複問同樣的問題", "user_id": "test_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["module"] == "M1"
    assert data["confidence"] > 0.6
```

## 11. Performance Optimization

### 11.1 Caching Strategy
```python
CACHE_CONFIG = {
    "analysis_results": {"ttl": 3600, "max_size": 1000},
    "user_sessions": {"ttl": 86400, "max_size": 500},
    "module_templates": {"ttl": 604800, "max_size": 100}
}
```

### 11.2 Parallel Processing
```python
async def parallel_api_calls(user_input: str):
    tasks = [
        call_dementia_bot_api(user_input),
        call_gemini_api(user_input),
        analyze_keywords(user_input)
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## 12. Deployment Checklist

- [ ] Environment variables configured
- [ ] Docker images built successfully
- [ ] Database initialized
- [ ] Redis connection tested
- [ ] LINE webhook verified
- [ ] ngrok tunnel established
- [ ] Health check endpoints working
- [ ] Logging system operational
- [ ] Monitoring system active
- [ ] Backup strategy implemented

## 13. User Experience Flow

### 13.1 Typical User Journey
1. **Discovery**: User notices concerning behavior
2. **Input**: Describes symptoms via LINE
3. **Analysis**: AI processes and categorizes
4. **Response**: Receives Flex Message with analysis
5. **Action**: Follows recommendations
6. **Follow-up**: Continues monitoring

### 13.2 Success Metrics
- Response time < 3 seconds
- User satisfaction > 80%
- Action completion rate > 60%
- Return usage rate > 40%

This architecture ensures:
- ✅ Scalable microservices design
- ✅ Robust error handling
- ✅ Comprehensive monitoring
- ✅ Secure data handling
- ✅ Fast response times
- ✅ User-friendly experience
