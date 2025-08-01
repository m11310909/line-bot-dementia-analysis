# 🔗 LINE Bot Webhook URL 設定指南

## ✅ **系統狀態確認**

您的 LINE Bot 系統已經完全正常運行：

- **API 服務**: ✅ 運行在 `http://localhost:8000`
- **Webhook 服務**: ✅ 運行在 `http://localhost:3000`
- **ngrok 隧道**: ✅ 已建立
- **LINE 憑證**: ✅ 已載入

---

## 🌐 **Webhook URL 設定**

### **您的 Webhook URL**
```
https://95ac71549b46.ngrok-free.app/webhook
```

### **設定步驟**

1. **訪問 LINE Developers Console**
   ```
   https://developers.line.biz/console/
   ```

2. **選擇您的 Bot Channel**
   - 點擊您的 Messaging API Channel

3. **設定 Webhook URL**
   - 在 "Messaging API" 設定頁面
   - 找到 "Webhook URL" 欄位
   - 輸入: `https://95ac71549b46.ngrok-free.app/webhook`
   - 點擊 "Update" 或 "Save"

4. **啟用 Webhook**
   - 確保 "Use webhook" 選項已開啟
   - 點擊 "Verify" 按鈕測試連接

---

## 🧪 **測試 LINE Bot**

### **方法 1: 使用 LINE 應用程式**
1. 掃描您的 LINE Bot QR Code
2. 發送測試消息: "媽媽最近常忘記關瓦斯"
3. 檢查是否收到分析結果

### **方法 2: 檢查 Webhook 日誌**
```bash
# 監控 webhook 服務日誌
tail -f logs/webhook.log
```

---

## 🔧 **故障排除**

### **如果 LINE Bot 仍然沒有回應**

1. **檢查 Webhook URL 是否正確**
   - 確認 URL: `https://95ac71549b46.ngrok-free.app/webhook`
   - 在 LINE Developers Console 中重新設定

2. **檢查 ngrok 狀態**
   ```bash
   curl -s http://localhost:4040/api/tunnels
   ```

3. **檢查服務狀態**
   ```bash
   # API 服務
   curl http://localhost:8000/health
   
   # Webhook 服務
   curl http://localhost:3000/health
   ```

4. **重新啟動服務**
   ```bash
   # 停止所有服務
   pkill -f "enhanced_line_bot_demo"
   pkill -f "updated_line_bot_webhook"
   pkill ngrok
   
   # 重新啟動
   source .env
   export FLEX_API_URL=http://localhost:8000/demo/message
   export RAG_HEALTH_URL=http://localhost:8000/health
   export RAG_ANALYZE_URL=http://localhost:8000/demo/comprehensive
   
   python3 enhanced_line_bot_demo.py &
   python3 updated_line_bot_webhook.py &
   ngrok http 3000 > /dev/null 2>&1 &
   ```

---

## 📊 **系統監控**

### **健康檢查端點**
```bash
# API 服務健康檢查
curl http://localhost:8000/health

# Webhook 服務健康檢查
curl http://localhost:3000/health

# Bot 資訊
curl http://localhost:3000/info
```

### **日誌監控**
```bash
# 查看 webhook 日誌
tail -f logs/webhook.log

# 查看 API 日誌
tail -f logs/api.log
```

---

## 🚨 **常見問題**

### **Q1: Webhook URL 驗證失敗**
- ✅ 確認 ngrok 正在運行
- ✅ 確認 webhook 服務在端口 3000
- ✅ 確認 URL 格式正確

### **Q2: LINE Bot 收到消息但沒有回應**
- ✅ 檢查 API 服務是否正常
- ✅ 檢查 LINE 憑證是否正確
- ✅ 檢查 webhook 處理邏輯

### **Q3: ngrok URL 變更**
- 每次重啟 ngrok 都會產生新的 URL
- 需要重新在 LINE Developers Console 中設定

---

## 🎯 **下一步**

1. **設定 Webhook URL**: 使用提供的 URL 在 LINE Developers Console 中設定
2. **測試 Bot**: 在 LINE 應用程式中發送消息
3. **監控日誌**: 觀察 webhook 處理過程
4. **驗證功能**: 確認分析結果正常顯示

---

## 📞 **需要幫助？**

如果仍然遇到問題，請檢查：
- LINE Developers Console 設定
- ngrok 隧道狀態
- 服務日誌輸出
- 網路連接狀態

**您的 LINE Bot 現在應該可以正常回應消息了！** 🎉 