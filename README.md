# 🚀 Dockerized LINE Bot Dementia Analysis System - Phase 2 Enhanced

## 🎯 **系統概述**
這是一個基於微服務架構的失智症照護 LINE Bot 系統，採用 Docker 容器化部署，支援 GPU 加速、XAI 視覺化、非線性導航和 ngrok 外部訪問，提供完整的智能分析和知識檢索功能。

## 🏗️ **系統架構**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LINE Bot      │    │  XAI Analysis   │    │   RAG Service   │
│   (Port 8081)   │◄──►│   (Port 8005)   │◄──►│   (Port 8006)   │
│   Non-linear    │    │   Enhanced      │    │   GPU Acceler.  │
│   Navigation    │    │   Visualization  │    │   Vector Search │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   ngrok Tunnel  │
│   (Port 5432)   │    │   (Port 6379)   │    │   (External)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 **快速開始**

### **前置需求**
- Docker 28.3.2+
- Docker Compose
- NVIDIA GPU (可選，用於 GPU 加速)
- ngrok (用於外部訪問)
- LINE Bot 憑證

### **Step 1: 克隆專案**
```bash
git clone <repository-url>
cd line-bot-dementia-analysis
```

### **Step 2: 設置環境變數**
```bash
cp env.example .env
# 編輯 .env 文件，填入您的 LINE Bot 憑證
```

### **Step 3: 部署系統**
```bash
chmod +x deploy.sh
./deploy.sh
```

### **Step 4: 設置 ngrok (可選)**
```bash
chmod +x ngrok-setup.sh
./ngrok-setup.sh
```

### **Step 5: 更新 LINE Developer Console**
1. 前往 [LINE Developer Console](https://developers.line.biz/)
2. 設置 Webhook URL: `https://your-ngrok-url.ngrok-free.app/webhook`
3. 啟用 Webhook

### **Step 6: 測試系統**
```bash
python test_phase2_features.py
```

## 🎯 **Phase 2 增強功能**

### **🚀 GPU 加速 RAG 系統**
- **FAISS GPU 向量搜尋**: 支援 GPU 加速的相似度搜尋
- **Sentence Transformers**: 多語言模型支援
- **自動降級**: GPU 不可用時自動使用 CPU
- **效能監控**: 即時處理時間和 GPU 使用率監控

### **📊 XAI 視覺化增強**
- **可解釋性路徑**: 詳細的決策過程說明
- **信心度雷達圖**: 各模組分析結果視覺化
- **特徵重要性**: 關鍵詞和症狀權重分析
- **模組使用統計**: 各模組使用頻率追蹤

### **🧭 四大模組非線性導航**
- **智能意圖檢測**: 自動識別用戶需求
- **動態模組推薦**: 基於上下文推薦相關模組
- **一鍵模組切換**: 無需重新輸入即可切換分析模組
- **個人化體驗**: 記住用戶偏好和歷史

### **💬 進階 Flex Message**
- **豐富視覺設計**: 彩色模組標識和圖標
- **互動按鈕**: 一鍵深入分析和知識檢索
- **動態內容**: 根據分析結果動態生成內容
- **錯誤處理**: 優雅的錯誤提示和恢復

## 📡 **服務端點**

### **LINE Bot Service (Port 8081)**
- `GET /` - 服務狀態
- `GET /health` - 健康檢查
- `POST /webhook` - LINE Bot webhook
- `GET /webhook-url` - 獲取 webhook URL

### **XAI Analysis Service (Port 8005)**
- `GET /` - 服務狀態
- `GET /health` - 健康檢查
- `POST /comprehensive-analysis` - 綜合分析
- `POST /analyze/{module}` - 單模組分析
- `GET /xai-features` - XAI 功能列表
- `GET /modules` - 模組列表

### **RAG Service (Port 8006)**
- `GET /` - 服務狀態
- `GET /health` - 健康檢查
- `POST /search` - GPU 加速知識搜尋
- `GET /gpu-status` - GPU 狀態檢查
- `GET /domains` - 知識領域列表
- `GET /knowledge/{domain}` - 特定領域知識

## 🌐 **ngrok 配置**

### **自動設置**
```bash
./ngrok-setup.sh
```

### **手動設置**
1. 啟動 ngrok: `ngrok http 8081`
2. 獲取 URL: `curl http://localhost:4040/api/tunnels`
3. 更新 .env: `EXTERNAL_URL=https://your-url.ngrok-free.app`

### **URL 檢索**
```bash
# 獲取當前 webhook URL
curl http://localhost:8081/webhook-url

# 檢查 ngrok 狀態
curl http://localhost:4040/api/tunnels
```

## 🛠️ **管理命令**

### **服務管理**
```bash
# 啟動所有服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 重啟特定服務
docker-compose restart line-bot

# 停止所有服務
docker-compose down

# 查看日誌
docker-compose logs -f [service-name]
```

### **功能測試**
```bash
# 測試 Phase 2 功能
python test_phase2_features.py

# 測試 GPU 加速
curl http://localhost:8006/gpu-status

# 測試 XAI 功能
curl http://localhost:8005/xai-features

# 測試知識搜尋
curl -X POST http://localhost:8006/search \
  -H "Content-Type: application/json" \
  -d '{"query": "失智症早期症狀", "use_gpu": true}'
```

## 🔧 **故障排除**

### **常見問題**
1. **GPU 不可用**: 系統會自動降級到 CPU 模式
2. **ngrok URL 變更**: 使用 `./ngrok-setup.sh` 自動更新
3. **服務啟動失敗**: 檢查 Docker 和端口衝突
4. **LINE Bot 無回應**: 檢查 webhook URL 和憑證

### **日誌查看**
```bash
# 查看所有日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f line-bot
docker-compose logs -f xai-analysis
docker-compose logs -f rag-service
```

### **健康檢查**
```bash
# 檢查所有服務健康狀態
curl http://localhost:8081/health
curl http://localhost:8005/health
curl http://localhost:8006/health
```

## 📊 **監控與運維**

### **效能監控**
- **GPU 使用率**: `curl http://localhost:8006/gpu-status`
- **處理時間**: 各 API 回應包含處理時間
- **服務狀態**: 健康檢查端點提供詳細狀態

### **日誌管理**
- **集中化日誌**: 所有服務日誌統一管理
- **錯誤追蹤**: 詳細的錯誤訊息和堆疊追蹤
- **效能分析**: 處理時間和資源使用統計

## 🔄 **升級指南**

### **從 Phase 1 升級到 Phase 2**
1. 備份現有配置: `cp .env .env.backup`
2. 更新代碼: `git pull origin main`
3. 重新部署: `./deploy.sh`
4. 測試功能: `python test_phase2_features.py`

### **功能對比**
| 功能 | Phase 1 | Phase 2 |
|------|---------|---------|
| GPU 加速 | ❌ | ✅ |
| XAI 視覺化 | 基礎 | 增強 |
| 非線性導航 | ❌ | ✅ |
| Flex Message | 基礎 | 進階 |
| 效能監控 | 基礎 | 詳細 |

## 🛠️ **開發指南**

### **本地開發**
```bash
# 克隆專案
git clone <repository-url>
cd line-bot-dementia-analysis

# 設置開發環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 啟動開發服務
python services/line-bot/main.py
python services/xai-analysis/main.py
python services/rag-service/main.py
```

### **API 開發**
- 使用 FastAPI 框架
- 支援 OpenAPI 文檔
- 自動生成 API 文檔: `http://localhost:8005/docs`

### **測試開發**
```bash
# 運行測試
python test_phase2_features.py

# 自定義測試
python -c "
import requests
response = requests.get('http://localhost:8005/health')
print(response.json())
"
```

## 🎯 **功能特色**

### **智能分析**
- **四大模組**: M1-M4 完整分析流程
- **XAI 可解釋性**: 詳細的決策過程說明
- **GPU 加速**: 高效能向量搜尋
- **多語言支援**: 中文和英文分析

### **用戶體驗**
- **非線性導航**: 智能模組推薦和切換
- **豐富視覺**: 彩色 Flex Message 設計
- **即時回應**: 優化的處理速度
- **錯誤恢復**: 優雅的錯誤處理

### **系統穩定性**
- **微服務架構**: 服務獨立，易於擴展
- **自動重啟**: 服務故障自動恢復
- **健康監控**: 即時狀態檢查
- **日誌管理**: 完整的錯誤追蹤

### **開發友好**
- **Docker 容器化**: 環境一致，部署簡單
- **API 文檔**: 自動生成的 OpenAPI 文檔
- **測試工具**: 完整的測試套件
- **監控工具**: 詳細的效能監控

## 📞 **支援**

### **技術支援**
- **GitHub Issues**: 報告問題和功能請求
- **文檔**: 詳細的 API 文檔和使用指南
- **測試**: 完整的測試套件和範例

### **社群**
- **開發者社群**: 分享經驗和最佳實踐
- **貢獻指南**: 歡迎提交 Pull Request
- **更新日誌**: 詳細的功能更新記錄

---

**🎉 Phase 2 升級完成！享受增強的 GPU 加速、XAI 視覺化和非線性導航功能！**

