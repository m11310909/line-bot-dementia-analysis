# 第三方 API 失智症小幫手1 配置指南

## 🎯 概述

本專案已更新為支援第三方 API 作為主要的對話回答引擎。系統會按以下優先順序選擇 API：

1. **第三方 API 失智症小幫手1** (優先)
2. 內部 Chatbot API (備用)
3. RAG API (最後備用)

## ⚠️ 重要提醒

### ChatGPT GPT 配置問題
如果您要使用 ChatGPT 的 GPT 作為第三方 API，需要：

1. **使用 OpenAI API**：不能直接調用 ChatGPT 網頁界面
2. **正確的 API 端點**：需要使用 OpenAI 的官方 API
3. **API Key**：需要有效的 OpenAI API Key

## ⚙️ 配置步驟

### 1. 環境變數設定

在 `.env` 文件中添加以下配置：

```bash
# 第三方 API 失智症小幫手1 配置 (主要對話引擎)
# 選項 A: OpenAI API (推薦)
THIRD_PARTY_API_URL=https://api.openai.com/v1/chat/completions
THIRD_PARTY_API_KEY=your_openai_api_key_here
USE_THIRD_PARTY_API=true
THIRD_PARTY_API_NAME=OpenAI ChatGPT

# 選項 B: 其他第三方 API
# THIRD_PARTY_API_URL=https://your-api-endpoint.com/chat
# THIRD_PARTY_API_KEY=your_api_key_here
# USE_THIRD_PARTY_API=true
# THIRD_PARTY_API_NAME=您的API名稱

# 內部 API 配置 (備用)
CHATBOT_API_URL=http://localhost:8008/analyze
USE_CHATBOT_API=false
```

### 2. OpenAI API 配置 (推薦)

如果您要使用 ChatGPT，請：

1. **註冊 OpenAI 帳號**：https://platform.openai.com/
2. **獲取 API Key**：在 OpenAI 平台生成 API Key
3. **設定環境變數**：
   ```bash
   THIRD_PARTY_API_URL=https://api.openai.com/v1/chat/completions
   THIRD_PARTY_API_KEY=sk-your-openai-api-key-here
   ```

### 3. API 回應格式要求

第三方 API 需要支援以下格式之一：

#### 格式 A: Flex Message (推薦)
```json
{
    "type": "flex",
    "altText": "失智症分析結果",
    "contents": {
        "type": "bubble",
        "size": "kilo",
        "header": {...},
        "body": {...}
    }
}
```

#### 格式 B: 純文字
```json
{
    "text": "分析結果文字內容"
}
```

### 4. API 請求格式

系統會向第三方 API 發送以下格式的請求：

```json
{
    "message": "用戶輸入的訊息",
    "user_id": "line_user"
}
```

## 🔧 故障排除

### 常見問題

1. **405 Method Not Allowed**
   - 原因：API URL 不是正確的端點
   - 解決：使用正確的 API 端點，不是網頁界面

2. **401 Unauthorized**
   - 原因：API Key 無效或未設定
   - 解決：檢查 API Key 是否正確

3. **404 Not Found**
   - 原因：API URL 錯誤
   - 解決：確認 API 端點是否正確

### 測試方法

運行測試腳本：
```bash
python3 test_third_party_api.py
```

## 📝 範例配置

### OpenAI API 配置範例
```bash
# .env 文件
THIRD_PARTY_API_URL=https://api.openai.com/v1/chat/completions
THIRD_PARTY_API_KEY=sk-1234567890abcdef1234567890abcdef1234567890abcdef
USE_THIRD_PARTY_API=true
THIRD_PARTY_API_NAME=OpenAI ChatGPT
```

### 自定義 API 配置範例
```bash
# .env 文件
THIRD_PARTY_API_URL=https://your-api-server.com/api/chat
THIRD_PARTY_API_KEY=your-custom-api-key
USE_THIRD_PARTY_API=true
THIRD_PARTY_API_NAME=自定義失智症API
```

## 🚀 下一步

1. 設定正確的 API 端點和 Key
2. 運行測試腳本驗證連接
3. 啟動 LINE Bot 服務
4. 測試完整的對話流程 