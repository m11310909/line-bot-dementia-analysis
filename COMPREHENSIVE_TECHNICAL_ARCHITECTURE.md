# 🏗️ **完整技術架構與流程統整**

## 📋 **目錄**
1. [系統概述](#系統概述)
2. [整體架構](#整體架構)
3. [核心工作流程](#核心工作流程)
4. [技術組件詳解](#技術組件詳解)
5. [模組架構](#模組架構)
6. [XAI 整合](#xai-整合)
7. [視覺化系統](#視覺化系統)
8. [監控與警報](#監控與警報)
9. [部署架構](#部署架構)
10. [效能優化](#效能優化)

---

## 🎯 **系統概述**

### **📱 產品定位**
智能失智症照護 LINE Bot 系統，整合 BoN-MAV、SHAP、LIME 等先進 AI 技術，為失智症患者和照護者提供專業、可信、可解釋的分析服務。

### **🎯 核心價值**
- **專業性**: 基於醫學專業知識的失智症分析
- **可信度**: 多引擎驗證和多面向評估
- **可解釋性**: 詳細的分析推理過程
- **易用性**: 直觀的視覺化界面

---

## 🏗️ **整體架構**

### **📊 系統架構圖**
```
┌─────────────────────────────────────────────────────────────────┐
│                        📱 LINE 用戶端                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🔗 Webhook 接收層                           │
│  • LINE Bot Webhook (Port 8081)                               │
│  • 簽名驗證和安全性檢查                                        │
│  • 訊息路由和負載均衡                                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🤖 失智小幫手核心分析                       │
│  • 專業失智症分析引擎                                          │
│  • 多面向症狀評估                                              │
│  • 統一回答標準                                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 核心分析引擎                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   M1 模組   │  │   M2 模組   │  │   M3 模組   │           │
│  │ 警訊徵兆分析 │  │ 病程進展評估 │  │ 行為症狀分析 │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │   M4 模組   │  │  XAI 分析   │  │  RAG 檢索   │           │
│  │ 照護資源導航 │  │ 視覺化引擎  │  │ 知識庫搜尋  │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🤖 AI 引擎層                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Gemini API │  │ OpenAI API  │  │ 第三方 API  │           │
│  │ Google AI   │  │ GPT-3.5     │  │ 失智小幫手  │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    📊 XAI 分析層                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ BoN-MAV     │  │   SHAP      │  │   LIME      │           │
│  │ 多候選答案   │  │ 特徵重要度   │  │ 局部解釋    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    📊 資料處理層                               │
│  • JSON 資料提取和結構化                                       │
│  • 快取管理 (Redis)                                           │
│  • 向量搜尋 (FAISS GPU)                                       │
│  • 資料庫存儲 (PostgreSQL)                                     │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🎨 視覺化回應層                             │
│  • M1-M4 模組視覺化                                           │
│  • Flex Message 生成                                           │
│  • 互動按鈕設計                                               │
│  • LIFF 整合                                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    📤 回應發送層                               │
│  • LINE Bot API 整合                                          │
│  • 錯誤處理和重試機制                                          │
│  • 效能監控和日誌記錄                                          │
└─────────────────────────────────────────────────────────────────┘
```

### **🔧 微服務架構**
```yaml
# docker-compose.yml
version: '3.8'
services:
  line-bot:
    build: ./services/line-bot
    ports:
      - "8081:8081"
    environment:
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET}
    depends_on:
      - redis
      - postgres
  
  xai-analysis:
    build: ./services/xai-analysis
    ports:
      - "8005:8005"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  rag-service:
    build: ./services/rag-service
    ports:
      - "8006:8006"
    environment:
      - REDIS_HOST=redis
      - POSTGRES_HOST=postgres
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=dementia_analysis
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
```

---

## 🔄 **核心工作流程**

### **📱 完整工作流程圖**
```
📱 用戶發送訊息到 LINE Bot
    ↓
🔗 Webhook 接收並驗證訊息
    ↓
🤖 失智小幫手 (Dementia Assistant) 核心分析
    ↓
🧠 基於失智小幫手回答的後續處理
    ↓
📊 XAI 引擎分析失智小幫手的回答
    ↓
📋 生成結構化的分析結果
    ↓
🎨 創建豐富的 Flex Message
    ↓
📤 發送回應給用戶
```

### **🧠 智能分析流程**
```
1. 用戶輸入預處理
   ↓
2. 失智小幫手核心分析
   ↓
3. 模組選擇 (基於失智小幫手分析)
   ↓
4. BoN-MAV 多候選答案驗證
   ↓
5. SHAP 特徵重要度分析
   ↓
6. LIME 局部解釋分析
   ↓
7. 結果整合和衝突解決
   ↓
8. 視覺化內容生成
   ↓
9. Flex Message 創建
   ↓
10. 回應發送
```

### **📊 資料處理流程**
```
原始輸入 → 文字清理 → 特徵提取 → 向量化 → 相似度搜尋 → 知識檢索 → 結構化 → 快取 → 回應生成
    ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓       ↓
  驗證    標準化    TF-IDF   FAISS   GPU加速  RAG系統  JSON格式  Redis    Flex UI
```

---

## 🔧 **技術組件詳解**

### **🤖 失智小幫手核心分析**
```python
async def call_dementia_assistant(user_message: str) -> Dict[str, Any]:
    """調用失智小幫手進行核心分析"""
    
    dementia_prompt = f"""
你是一個專業的失智症照護助手「失智小幫手」。
請分析以下用戶描述，並提供：

1. 失智症警訊分析
2. 專業建議
3. 關懷提醒
4. 後續行動建議
5. 嚴重程度評估
6. 建議就醫時機

用戶描述：{user_message}

請用繁體中文回答，並提供結構化的分析結果。
"""
    
    # 調用失智小幫手 API
    response = requests.post(
        "https://api.dementia-assistant.com/analyze",
        json={
            "prompt": dementia_prompt,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        },
        timeout=30
    )
    
    return response.json()
```

### **🔄 基於失智小幫手回答的後續處理**
```python
async def process_dementia_assistant_response(assistant_response: Dict) -> Dict[str, Any]:
    """基於失智小幫手回答進行後續處理"""
    
    # 提取失智小幫手的回答
    dementia_analysis = assistant_response.get("analysis", "")
    recommendations = assistant_response.get("recommendations", [])
    warnings = assistant_response.get("warnings", [])
    severity = assistant_response.get("severity", "unknown")
    
    # 步驟 4.1: 模組選擇 (基於失智小幫手的分析)
    selected_module = select_module_based_on_assistant_response(dementia_analysis)
    
    # 步驟 4.2: BoN-MAV 驗證 (驗證失智小幫手的回答)
    bon_mav_result = await validate_assistant_response_with_bon_mav(dementia_analysis)
    
    # 步驟 4.3: SHAP 特徵分析 (分析失智小幫手回答的特徵)
    shap_result = analyze_assistant_response_features(dementia_analysis)
    
    # 步驟 4.4: LIME 局部解釋 (解釋失智小幫手的推理過程)
    lime_result = explain_assistant_reasoning(dementia_analysis)
    
    return {
        "original_assistant_response": assistant_response,
        "selected_module": selected_module,
        "bon_mav_validation": bon_mav_result,
        "shap_analysis": shap_result,
        "lime_explanation": lime_result
    }
```

---

## 🧩 **模組架構**

### **🚨 M1 模組：警訊徵兆分析**
```python
class M1WarningSignsModule:
    """M1 模組：失智症十大警訊比對"""
    
    def __init__(self):
        self.warning_signs = self._load_warning_signs()
    
    def analyze_warning_signs(self, user_input: str) -> Dict:
        """分析用戶輸入，識別失智症警訊"""
        # 關鍵詞匹配分析
        # 警訊徵兆識別
        # 嚴重程度評估
        # 行動建議生成
        pass
    
    def create_visual_comparison_card(self, user_input: str, matched_signs: List[str]) -> Dict:
        """創建視覺化比對卡片"""
        # 正常老化 vs 失智症警訊對比
        # 嚴重程度評估
        # 行動建議生成
        pass
```

### **📈 M2 模組：病程進展評估**
```python
class M2ProgressionMatrixModule:
    """M2 模組：病程階段評估矩陣"""
    
    def __init__(self):
        self.stages = self._load_progression_stages()
    
    def analyze_progression(self, user_input: str) -> Dict:
        """分析用戶輸入，評估可能的病程階段"""
        # 用戶症狀描述分析
        # 關鍵詞匹配和權重計算
        # 病程階段判定
        # 症狀特徵識別
        # 照護重點建議
        pass
    
    def create_progression_card(self, user_input: str, stage_analysis: Dict) -> Dict:
        """創建病程進展視覺化卡片"""
        # 階段性症狀和照護重點
        # 症狀特徵視覺化
        # 照護重點動態生成
        pass
```

### **🧠 M3 模組：行為心理症狀分析**
```python
class M3BPSDClassificationModule:
    """M3 模組：行為心理症狀分類 (BPSD)"""
    
    def __init__(self):
        self.bpsd_symptoms = self._load_bpsd_symptoms()
    
    def analyze_bpsd_symptoms(self, user_input: str) -> Dict:
        """分析行為和心理症狀"""
        # 行為症狀描述分析
        # BPSD 分類識別
        # 觸發因素分析
        # 干預措施建議
        # 嚴重程度評估
        pass
    
    def create_bpsd_card(self, user_input: str, bpsd_analysis: Dict) -> Dict:
        """創建 BPSD 視覺化卡片"""
        # 五大 BPSD 分類
        # 症狀觸發因素分析
        # 專業干預建議
        pass
```

### **🏥 M4 模組：照護資源導航**
```python
class M4CareNavigationModule:
    """M4 模組：照護資源導航系統"""
    
    def __init__(self):
        self.care_resources = self._load_care_resources()
    
    def analyze_care_tasks(self, user_input: str) -> Dict:
        """分析照護需求，推薦適合的資源"""
        # 用戶需求分析
        # 資源類別匹配
        # 具體資源推薦
        # 聯絡資訊提供
        # 實用技巧建議
        pass
    
    def create_care_navigation_card(self, user_input: str, care_analysis: Dict) -> Dict:
        """創建照護資源導航卡片"""
        # 五大資源類別
        # 專業聯絡資訊
        # 實用照護技巧
        pass
```

---

## 🧠 **XAI 整合**

### **🏆 BoN-MAV 方法**
```python
class BoNMAV:
    """Best of N - Multi-Aspect Verification"""
    
    def __init__(self, n_candidates: int = 5):
        self.n_candidates = n_candidates
        self.aspects = {
            "medical_accuracy": "醫療準確性",
            "safety": "安全性",
            "feasibility": "可行性",
            "emotional_appropriateness": "情感適當性"
        }
    
    async def generate_best_answer(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """生成最佳答案並進行多面向驗證"""
        # 步驟 1: 生成多個候選答案
        candidates = await self._generate_candidates(user_input, context)
        
        # 步驟 2: 對每個候選答案進行多面向驗證
        verified_candidates = []
        for candidate in candidates:
            verification = await self._verify_aspects(candidate, context)
            verified_candidates.append({
                "answer": candidate,
                "verification": verification,
                "overall_score": self._calculate_comprehensive_score(candidate, verification, context)
            })
        
        # 步驟 3: 選擇最佳答案
        best_candidate = max(verified_candidates, key=lambda x: x["overall_score"])
        
        return {
            "best_answer": best_candidate["answer"],
            "verification_results": best_candidate["verification"],
            "overall_score": best_candidate["overall_score"],
            "selection_reason": self._get_selection_reason(best_candidate),
            "all_candidates": verified_candidates
        }
```

### **🔍 SHAP 特徵重要度分析**
```python
class SHAPAnalyzer:
    """SHAP 特徵重要度分析器"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.explainer = None
        self.feature_names = []
    
    def analyze_feature_importance(self, text: str) -> Dict[str, Any]:
        """分析文本的特徵重要度"""
        # 特徵提取
        X = self.vectorizer.transform([text])
        
        # 生成 SHAP 值
        shap_values = self.explainer.shap_values(X)
        
        # 提取特徵重要度
        feature_importance = {}
        for i, feature_name in enumerate(self.feature_names):
            if X[0, i] > 0:  # 只考慮文本中出現的特徵
                feature_importance[feature_name] = float(shap_values[0, i])
        
        return {
            "feature_importance": dict(sorted_features[:10]),
            "shap_values": shap_values.tolist(),
            "base_value": float(self.explainer.expected_value),
            "prediction": self.model.predict(X)[0]
        }
```

### **🎯 LIME 局部解釋分析**
```python
class LIMEAnalyzer:
    """LIME 局部解釋分析器"""
    
    def __init__(self):
        self.explainer = LimeTextExplainer(class_names=['正常', '輕度', '中度', '重度'])
    
    def analyze_local_importance(self, text: str, model) -> Dict[str, Any]:
        """分析文本的局部特徵重要度"""
        # 創建預測函數
        def predict_proba(texts):
            return np.array([[0.1, 0.3, 0.4, 0.2]])
        
        # 生成 LIME 解釋
        exp = self.explainer.explain_instance(
            text, 
            predict_proba, 
            num_features=10,
            num_samples=100
        )
        
        return {
            "feature_importance": feature_importance,
            "predicted_class": exp.predicted_class,
            "confidence": exp.score,
            "explanation": exp.as_list()
        }
```

---

## 🎨 **視覺化系統**

### **📱 M1-M4 視覺化模組**
```python
def create_comprehensive_visualization(analysis_result: Dict) -> Dict:
    """創建完整的視覺化界面"""
    
    # 根據分析結果選擇模組
    selected_module = analysis_result.get("selected_module", "M1")
    
    # 記錄指標
    metrics_tracker.record_metrics(analysis_result)
    
    # 檢查警報
    alerts = metrics_tracker.check_threshold_alerts()
    for alert in alerts:
        await alert_system.send_alert(alert)
    
    # 獲取引用來源
    citation_text = citation_manager.get_citation_text(
        analysis_result.get("source_keys", ["dsm5", "taiwan_dementia"])
    )
    analysis_result["sources"] = citation_text
    
    # 創建對應模組的視覺化
    if selected_module == "M1":
        return create_m1_visualization(analysis_result)
    elif selected_module == "M2":
        return create_m2_visualization(analysis_result)
    elif selected_module == "M3":
        return create_m3_visualization(analysis_result)
    elif selected_module == "M4":
        return create_m4_visualization(analysis_result)
    else:
        return create_m1_visualization(analysis_result)  # 預設
```

### **🎨 視覺化特色**
- **M1 模組**: 警訊分析卡片，風險等級指示
- **M2 模組**: 進展階段圖表，症狀特徵展示
- **M3 模組**: 症狀熱力圖，干預建議
- **M4 模組**: 資源分類導航，聯絡資訊

---

## 📊 **監控與警報**

### **🔍 關鍵指標追蹤**
```python
class MetricsTracker:
    """指標追蹤系統"""
    
    def __init__(self):
        self.metrics = {
            "auc": [],
            "recall_at_k": [],
            "user_satisfaction": [],
            "physician_diff": [],
            "response_time": [],
            "error_rate": []
        }
    
    def record_metrics(self, analysis_result: Dict):
        """記錄分析指標"""
        self.metrics["auc"].append(analysis_result.get("auc", 0))
        self.metrics["recall_at_k"].append(analysis_result.get("recall_at_k", 0))
        self.metrics["user_satisfaction"].append(analysis_result.get("user_satisfaction", 0))
        self.metrics["physician_diff"].append(analysis_result.get("physician_diff", 0))
        self.metrics["response_time"].append(analysis_result.get("response_time", 0))
        self.metrics["error_rate"].append(analysis_result.get("error_rate", 0))
    
    def check_threshold_alerts(self) -> List[Dict]:
        """檢查閾值警報"""
        alerts = []
        
        # AUC 閾值檢查
        avg_auc = np.mean(self.metrics["auc"])
        if avg_auc < 0.8:
            alerts.append({
                "type": "warning",
                "message": f"AUC 指標過低: {avg_auc:.3f}",
                "severity": "medium",
                "recipients": ["devops", "clinical_consultant"]
            })
        
        # 用戶滿意度閾值檢查
        avg_satisfaction = np.mean(self.metrics["user_satisfaction"])
        if avg_satisfaction < 4.0:
            alerts.append({
                "type": "warning",
                "message": f"用戶滿意度過低: {avg_satisfaction:.1f}/5.0",
                "severity": "high",
                "recipients": ["devops", "clinical_consultant", "product_manager"]
            })
        
        return alerts
```

### **🚨 自動警報系統**
```python
class AlertSystem:
    """自動警報系統"""
    
    def __init__(self):
        self.thresholds = {
            "auc_min": 0.8,
            "recall_at_k_min": 0.75,
            "user_satisfaction_min": 4.0,
            "physician_diff_max": 0.2,
            "response_time_max": 5.0,
            "error_rate_max": 0.05
        }
    
    async def send_alert(self, alert: Dict):
        """發送警報"""
        recipients = alert.get("recipients", [])
        
        for recipient in recipients:
            if recipient == "devops":
                await self.send_devops_alert(alert)
            elif recipient == "clinical_consultant":
                await self.send_clinical_alert(alert)
            elif recipient == "product_manager":
                await self.send_product_alert(alert)
            elif recipient == "medical_director":
                await self.send_medical_director_alert(alert)
```

---

## 🚀 **部署架構**

### **📦 容器化部署**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  line-bot:
    build: ./services/line-bot
    ports:
      - "8081:8081"
    environment:
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - LINE_CHANNEL_SECRET=${LINE_CHANNEL_SECRET}
    depends_on:
      - redis
      - postgres
    restart: unless-stopped
  
  xai-analysis:
    build: ./services/xai-analysis
    ports:
      - "8005:8005"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
  
  rag-service:
    build: ./services/rag-service
    ports:
      - "8006:8006"
    environment:
      - REDIS_HOST=redis
      - POSTGRES_HOST=postgres
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
  
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=dementia_analysis
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

### **🔧 CI/CD 流程**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚡ **效能優化**

### **📊 快取策略**
```python
# Redis 快取配置
CACHE_CONFIG = {
    "analysis_results": {
        "ttl": 3600,  # 1 小時
        "prefix": "analysis:"
    },
    "user_sessions": {
        "ttl": 86400,  # 24 小時
        "prefix": "session:"
    },
    "knowledge_cache": {
        "ttl": 604800,  # 7 天
        "prefix": "knowledge:"
    }
}
```

### **🚀 GPU 加速**
```python
def perform_vector_search(query: str, top_k: int = 5) -> List[Dict]:
    """GPU 加速向量搜尋"""
    # GPU 加速向量搜尋
    if torch.cuda.is_available():
        embeddings = model.encode(query, device='cuda')
    else:
        embeddings = model.encode(query, device='cpu')
    
    # FAISS GPU 搜尋
    if faiss.get_num_gpus() > 0:
        index = faiss.IndexFlatIP(768)
        index = faiss.index_cpu_to_gpu(index, 0)
    else:
        index = faiss.IndexFlatIP(768)
    
    return search_results
```

### **📈 效能指標**
- **回應時間**: 目標 < 3 秒
- **系統可用性**: 目標 > 99.9%
- **錯誤率**: 目標 < 0.1%
- **並發處理能力**: 目標 100+ 同時在線

---

## 📚 **引用來源管理**

### **🔗 專業標準**
```python
class CitationManager:
    """引用來源管理系統"""
    
    def __init__(self):
        self.sources = {
            "dsm5": {
                "title": "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition",
                "author": "American Psychiatric Association",
                "year": "2013",
                "url": "https://doi.org/10.1176/appi.books.9780890425596"
            },
            "taiwan_dementia": {
                "title": "台灣失智症協會照護指南",
                "author": "台灣失智症協會",
                "year": "2023",
                "url": "https://www.tada2002.org.tw/"
            },
            "who_dementia": {
                "title": "WHO Guidelines on Risk Reduction of Cognitive Decline and Dementia",
                "author": "World Health Organization",
                "year": "2019",
                "url": "https://www.who.int/publications/i/item/risk-reduction-of-cognitive-decline-and-dementia"
            }
        }
    
    def get_citation_text(self, source_keys: List[str]) -> str:
        """獲取引用文字"""
        citations = []
        for key in source_keys:
            if key in self.sources:
                source = self.sources[key]
                citations.append(f"{source['author']} ({source['year']})")
        
        if citations:
            return f"基於: {', '.join(citations)}"
        else:
            return "基於 DSM-5 診斷標準和台灣失智症協會指南"
```

---

## 📈 **預期效果**

### **✅ 技術優勢**
- **多引擎 AI**: Gemini、OpenAI、第三方 API 整合
- **XAI 可解釋性**: BoN-MAV、SHAP、LIME 深度分析
- **高效能架構**: GPU 加速、Redis 快取、微服務設計
- **安全可靠**: 完整的安全機制和隱私保護

### **📊 效能指標**
- **業務指標**: DAU 1000+、MAU 5000+、留存率 > 60%
- **技術指標**: 回應時間 < 3 秒、可用性 > 99.9%、錯誤率 < 0.1%
- **AI 指標**: 分析準確率 > 85%、模組選擇準確率 > 90%

### **🎯 用戶價值**
- **專業分析**: 基於醫學專業知識的失智症分析
- **視覺化體驗**: 豐富的圖表和互動元素
- **即時回應**: 快速的分析和建議
- **持續支持**: 提供後續行動建議和專業諮詢

---

*這個完整的技術架構與流程統整，涵蓋了從系統概述到具體實現的每個環節，為 LINE Bot 失智症分析系統提供了全面的技術藍圖和實施指南。* 