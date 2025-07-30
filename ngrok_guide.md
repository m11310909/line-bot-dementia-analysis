# 🌐 ngrok Webhook 設置指南

## 步驟 1: 安裝 ngrok

### 方法 1: 使用 Homebrew (推薦)
```bash
brew install ngrok
```

### 方法 2: 手動下載
1. 前往 [ngrok.com](https://ngrok.com/)
2. 註冊免費帳號
3. 下載並安裝 ngrok

## 步驟 2: 啟動 API

確保您的 API 正在運行：
```bash
python3 enhanced_m1_m2_m3_integrated_api.py
```

## 步驟 3: 啟動 ngrok

在新的終端視窗中執行：
```bash
ngrok http 8005
```

## 步驟 4: 獲取 Webhook URL

ngrok 啟動後會顯示類似這樣的資訊：
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8005
```

您的 Webhook URL 就是：
```
https://abc123.ngrok.io/webhook
```

## 步驟 5: 設定 LINE Bot Webhook

1. 登入 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Channel
3. 進入 "Messaging API" 設定
4. 在 "Webhook URL" 欄位填入：`https://abc123.ngrok.io/webhook`
5. 開啟 "Use webhook" 選項
6. 點擊 "Verify" 按鈕測試連接

## 自動化設置

使用我們提供的腳本：
```bash
python3 setup_ngrok.py
```

## 注意事項

- ⚠️ **免費版 ngrok 每次重啟都會改變 URL**
- ⚠️ **需要重新設定 LINE Bot Webhook URL**
- 💡 **建議使用固定網域或付費版 ngrok**
- 🔒 **正式環境請使用 HTTPS**

## 測試 Webhook

設定完成後，您可以：
1. 掃描 LINE Bot QR Code
2. 發送訊息給 Bot
3. 檢查 API 日誌是否收到訊息

## 故障排除

### 問題 1: ngrok 無法啟動
```bash
# 檢查 ngrok 是否已安裝
ngrok version

# 重新安裝
brew reinstall ngrok
```

### 問題 2: API 端口被佔用
```bash
# 使用我們的腳本解決
python3 quick_fix_port.py
```

### 問題 3: LINE Bot 無法連接
- 確保 Webhook URL 正確
- 確保 API 正在運行
- 檢查 ngrok 是否正常運作 