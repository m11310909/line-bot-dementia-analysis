# 🚀 Dockerized LINE Bot Dementia Analysis System

## 🎯 **系統概述**

這是一個基於微服務架構的失智症照護 LINE Bot 系統，採用 Docker 容器化部署，支援 ngrok 外部訪問，提供完整的 XAI 分析和 RAG 知識檢索功能。

## 🏗️ **系統架構**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LINE Bot      │    │  XAI Analysis   │    │   RAG Service   │
│   (Port 8081)   │◄──►│   (Port 8005)   │◄──►│   (Port 8006)   │
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
發送測試訊息：`爸爸不會用洗衣機`

## 📊 **服務端點**

| 服務 | 端點 | 描述 |
|------|------|------|
| LINE Bot | `http://localhost:8081` | Webhook 服務 |
| XAI Analysis | `http://localhost:8005` | 智能分析服務 |
| RAG Service | `http://localhost:8006` | 知識檢索服務 |
| PostgreSQL | `localhost:5432` | 資料庫 |
| Redis | `localhost:6379` | 快取服務 |
| ngrok | `https://xxx.ngrok-free.app` | 外部訪問 |

## 🌐 **ngrok 配置**

### **自動設置**
```bash
./ngrok-setup.sh
```

### **手動設置**
```bash
# 啟動 ngrok
ngrok http 8081

# 更新 .env 文件
EXTERNAL_URL=https://your-ngrok-url.ngrok-free.app

# 重啟 LINE Bot 服務
docker-compose restart line-bot
```

### **獲取 Webhook URL**
```bash
curl http://localhost:8081/webhook-url
```

## 🛠️ **管理命令**

### **查看服務狀態**
```bash
docker-compose ps
```

### **查看日誌**
```bash
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f line-bot
docker-compose logs -f xai-analysis
docker-compose logs -f rag-service

# 查看 ngrok 日誌
tail -f ngrok.log
```

### **重啟服務**
```bash
# 重啟所有服務
docker-compose restart

# 重啟特定服務
docker-compose restart line-bot
```

### **更新服務**
```bash
docker-compose up --build -d
```

### **停止服務**
```bash
docker-compose down
```

### **ngrok 管理**
```bash
# 停止 ngrok
pkill ngrok

# 重新設置 ngrok
./ngrok-setup.sh
```

## 🔧 **故障排除**

### **常見問題**

#### **1. 服務無法啟動**
```bash
# 檢查 Docker 是否運行
docker info

# 檢查端口是否被佔用
lsof -i :8081
lsof -i :8005
lsof -i :8006
```

#### **2. LINE Bot 無回應**
- 檢查 `.env` 文件中的憑證
- 確認 Webhook URL 設置正確
- 查看 LINE Bot 服務日誌
- 確認 ngrok URL 是否正確

#### **3. ngrok 連接問題**
```bash
# 檢查 ngrok 狀態
curl http://localhost:4040/api/tunnels

# 重新啟動 ngrok
./ngrok-setup.sh

# 檢查 ngrok 日誌
tail -f ngrok.log
```

#### **4. 分析服務錯誤**
```bash
# 檢查 XAI Analysis 服務
curl http://localhost:8005/health

# 檢查 RAG Service
curl http://localhost:8006/health
```

## 📈 **監控與維護**

### **健康檢查**
```bash
# 檢查所有服務健康狀態
curl http://localhost:8081/health
curl http://localhost:8005/health
curl http://localhost:8006/health

# 檢查 ngrok 狀態
curl http://localhost:4040/api/tunnels
```

### **效能監控**
```bash
# 查看容器資源使用
docker stats

# 查看服務日誌
docker-compose logs --tail=100

# 查看 ngrok 日誌
tail -f ngrok.log
```

## 🔄 **升級指南**

### **更新服務**
```bash
# 拉取最新代碼
git pull

# 重新構建並啟動服務
docker-compose up --build -d

# 重新設置 ngrok
./ngrok-setup.sh
```

### **資料備份**
```bash
# 備份 PostgreSQL 資料
docker-compose exec postgres pg_dump -U admin dementia_analysis > backup.sql

# 備份 Redis 資料
docker-compose exec redis redis-cli BGSAVE
```

## 📚 **開發指南**

### **本地開發**
```bash
# 啟動開發環境
docker-compose -f docker-compose.dev.yml up -d

# 查看開發日誌
docker-compose logs -f
```

### **添加新功能**
1. 在對應服務目錄中修改代碼
2. 重新構建服務：`docker-compose build [service-name]`
3. 重啟服務：`docker-compose restart [service-name]`

## 🎯 **功能特色**

- ✅ **微服務架構**：服務獨立部署，易於擴展
- ✅ **Docker 容器化**：環境一致，部署簡單
- ✅ **ngrok 支援**：外部訪問，LINE Bot 整合
- ✅ **XAI 分析**：可解釋的 AI 分析結果
- ✅ **RAG 知識檢索**：智能知識庫查詢
- ✅ **LINE Bot 整合**：完整的聊天機器人功能
- ✅ **健康監控**：自動健康檢查和日誌記錄
- ✅ **自動重啟**：服務故障自動恢復

## 📞 **支援**

如有問題，請檢查：
1. Docker 服務狀態
2. 環境變數設置
3. 服務日誌
4. 網路連接
5. ngrok 連接狀態

---

**版本**: 3.0.0  
**架構**: 微服務 + Docker + ngrok  
**狀態**: 生產就緒 