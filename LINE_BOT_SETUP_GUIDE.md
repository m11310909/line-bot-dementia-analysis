# 🚀 LINE Bot 完整設定指南

## 📋 **問題診斷**

您遇到的問題是：**LINE Bot 沒有回應消息**

### 🔍 **根本原因**
1. **缺少 LINE 憑證**: 沒有設定 `LINE_CHANNEL_ACCESS_TOKEN` 和 `LINE_CHANNEL_SECRET`
2. **運行的是演示版本**: 當前運行的是 `enhanced_line_bot_demo.py`，這是演示模式
3. **需要真實的 Webhook 服務**: 需要運行 `updated_line_bot_webhook.py`

---

## 🛠️ **解決方案**

### **步驟 1: 獲取 LINE Bot 憑證**

1. **訪問 LINE Developers Console**
   ```
   https://developers.line.biz/console/
   ```

2. **創建新的 Provider 和 Channel**
   - 點擊 "Create Provider"
   - 創建新的 Messaging API Channel

3. **獲取憑證**
   - **Channel Access Token**: 在 Channel 設定中找到
   - **Channel Secret**: 在 Basic Settings 中找到

### **步驟 2: 設定環境變數**

創建 `.env` 文件：

```bash
# LINE Bot 憑證
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# API 設定
FLEX_API_URL=http://localhost:8000/demo/message
RAG_HEALTH_URL=http://localhost:8000/health
RAG_ANALYZE_URL=http://localhost:8000/demo/comprehensive
```

### **步驟 3: 啟動真實的 LINE Bot 服務**

```bash
# 停止演示版本
pkill -f "enhanced_line_bot_demo"

# 啟動真實的 LINE Bot Webhook 服務
python3 updated_line_bot_webhook.py
```

### **步驟 4: 設定 Webhook URL**

在 LINE Developers Console 中設定 Webhook URL：
```
https://your-domain.com/webhook
```

如果使用 ngrok 進行本地測試：
```bash
# 安裝 ngrok
brew install ngrok

# 啟動 ngrok
ngrok http 8000

# 使用提供的 URL 設定 Webhook
# 例如: https://abc123.ngrok.io/webhook
```

---

## 🔧 **快速修復腳本**

創建 `fix_line_bot.sh`:

```bash
#!/bin/bash

echo "🔧 LINE Bot 快速修復"

# 1. 停止所有相關進程
echo "📛 停止現有進程..."
pkill -f "enhanced_line_bot_demo"
pkill -f "updated_line_bot_webhook"
sleep 2

# 2. 檢查環境變數
echo "🔍 檢查 LINE 憑證..."
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "❌ LINE_CHANNEL_ACCESS_TOKEN 未設定"
    echo "請設定您的 LINE Bot 憑證"
    exit 1
fi

if [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "❌ LINE_CHANNEL_SECRET 未設定"
    echo "請設定您的 LINE Bot 憑證"
    exit 1
fi

echo "✅ LINE 憑證已設定"

# 3. 啟動 LINE Bot Webhook 服務
echo "🚀 啟動 LINE Bot Webhook 服務..."
python3 updated_line_bot_webhook.py &

# 4. 等待服務啟動
sleep 5

# 5. 測試服務
echo "🧪 測試服務..."
curl -s http://localhost:8000/health | head -c 100

echo "✅ LINE Bot 修復完成！"
```

---

## 📱 **測試方法**

### **方法 1: 使用 curl 測試**
```bash
# 測試健康檢查
curl http://localhost:8000/health

# 測試消息處理
curl -X POST http://localhost:8000/demo/message \
  -H "Content-Type: application/json" \
  -d '{"text": "媽媽最近常忘記關瓦斯", "user_id": "test_user"}'
```

### **方法 2: 使用 LINE 應用程式**
1. 掃描您的 LINE Bot QR Code
2. 發送測試消息
3. 檢查是否有回應

---

## 🚨 **常見問題**

### **Q1: LINE Bot 沒有回應**
- ✅ 檢查憑證是否正確設定
- ✅ 確認 Webhook URL 是否正確
- ✅ 檢查服務是否正在運行

### **Q2: 收到 "Invalid signature" 錯誤**
- ✅ 確認 Channel Secret 是否正確
- ✅ 檢查 Webhook URL 是否使用 HTTPS

### **Q3: 服務無法啟動**
- ✅ 檢查端口 8000 是否被佔用
- ✅ 確認 Python 環境是否正確
- ✅ 檢查依賴套件是否已安裝

---

## 📊 **系統狀態檢查**

```bash
# 檢查服務狀態
curl http://localhost:8000/health

# 檢查 LINE Bot 資訊
curl http://localhost:8000/info

# 檢查 RAG API 狀態
curl http://localhost:8000/rag-status
```

---

## 🎯 **下一步**

1. **設定 LINE 憑證**
2. **啟動真實的 Webhook 服務**
3. **設定 Webhook URL**
4. **測試 LINE Bot 功能**

完成這些步驟後，您的 LINE Bot 就能正常回應消息了！

---

## 📞 **需要幫助？**

如果遇到問題，請檢查：
- LINE Developers Console 設定
- 環境變數設定
- 服務日誌輸出
- 網路連接狀態 