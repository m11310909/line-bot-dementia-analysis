# 🤖 失智小助手chatbot API 整合指南

## 📋 配置步驟

### 1. 設置環境變數

在 `.env` 文件中添加以下配置：

```bash
# 失智小助手chatbot API 配置
CHATBOT_API_URL=https://your-chatbot-api-endpoint.com/analyze
CHATBOT_API_KEY=your-api-key-here
USE_CHATBOT_API=true

# 原有 RAG API 配置（備用）
FLEX_API_URL=http://localhost:8005/comprehensive-analysis
RAG_HEALTH_URL=http://localhost:8005/health
```

### 2. API 格式要求

您的 chatbot API 需要支援以下格式：

#### 請求格式：
```json
{
  "message": "用戶輸入的文字",
  "user_id": "line_user"
}
```

#### 回應格式（選項1 - Flex Message）：
```json
{
  "type": "flex",
  "altText": "失智症分析結果",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "分析結果",
          "weight": "bold"
        }
      ]
    }
  }
}
```

#### 回應格式（選項2 - 簡單文字）：
```json
{
  "message": "分析結果文字",
  "confidence": 0.85
}
```

### 3. 切換 API

#### 使用 Chatbot API：
```bash
export USE_CHATBOT_API=true
export CHATBOT_API_URL=https://your-api.com/analyze
```

#### 使用原有 RAG API：
```bash
export USE_CHATBOT_API=false
```

### 4. 測試配置

```bash
# 測試 chatbot API
curl -X POST https://your-api.com/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"message": "爸爸不會用洗衣機", "user_id": "test_user"}'
```

## 🔧 故障排除

### 常見問題：

1. **API 連接失敗**
   - 檢查 `CHATBOT_API_URL` 是否正確
   - 確認 API 端點是否可訪問

2. **認證錯誤**
   - 檢查 `CHATBOT_API_KEY` 是否正確
   - 確認 API 金鑰格式

3. **回應格式錯誤**
   - 確保 API 回應符合預期格式
   - 檢查 JSON 結構是否正確

### 日誌檢查：
```bash
# 查看 webhook 日誌
tail -f logs/webhook.log

# 查看 API 調用日誌
grep "Calling chatbot API" logs/webhook.log
```

## 📊 監控

### 健康檢查端點：
```bash
curl https://your-ngrok-url.ngrok-free.app/health
```

### API 狀態檢查：
```bash
curl https://your-ngrok-url.ngrok-free.app/rag-status
```

## 🎯 使用範例

### 啟動系統：
```bash
# 使用 chatbot API
USE_CHATBOT_API=true python3 updated_line_bot_webhook.py

# 使用原有 RAG API
USE_CHATBOT_API=false python3 updated_line_bot_webhook.py
```

### 測試訊息：
發送以下訊息到 LINE Bot：
- `爸爸不會用洗衣機`
- `媽媽最近常忘記關瓦斯`
- `爺爺在熟悉地方迷路`

---
**最後更新**: 2025-08-02
**狀態**: 準備就緒 🚀 