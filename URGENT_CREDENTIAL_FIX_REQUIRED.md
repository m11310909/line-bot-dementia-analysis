# 🚨 緊急：需要更新真實 LINE 憑證

## ❌ **問題狀況**

您的 `.env` 檔案仍然使用**占位符文字**，不是真實憑證：

```
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here
```

因此持續出現簽名錯誤：
```
❌ Invalid LINE signature: <InvalidSignatureError [Invalid signature. signature=CbwNQtbVK5MRuzAVKNzb0u3xjf66knJONbNLUBmrXKI=]>
```

## 🔧 **立即修復步驟**

### **步驟 1：取得真實 LINE 憑證**

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 選擇您的 Messaging API Channel
3. 在 **「Basic settings」** 頁面找到：
   - **Channel secret** (複製此值)
4. 在 **「Messaging API」** 頁面找到：
   - **Channel access token** (如果沒有，點擊 "Issue" 建立)

### **步驟 2：更新 .env 檔案**

**⚠️ 重要**：用您的**真實憑證**替換以下內容：

```bash
# 編輯 .env 檔案
nano .env

# 或使用其他編輯器
code .env
```

**更新為**：
```env
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=您的真實Channel_Access_Token
LINE_CHANNEL_SECRET=您的真實Channel_Secret

# 其他配置保持不變...
```

### **步驟 3：重新啟動服務**

```bash
# 重新啟動以載入新憑證
docker-compose down
docker-compose up -d
```

## 📝 **憑證格式範例**

**正確格式**：
```env
LINE_CHANNEL_ACCESS_TOKEN=aBc123XyZ789...（很長的字串）
LINE_CHANNEL_SECRET=1a2b3c4d5e6f7g8h9i0j...（32位字串）
```

**❌ 錯誤格式**（目前狀況）：
```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here
```

## 🎯 **完成後**

更新憑證並重啟服務後，我會幫您驗證配置是否正確。

**您的 Bot 將能夠**：
- ✅ 正確驗證 LINE 簽名
- ✅ 成功接收和處理訊息
- ✅ 回覆失智症分析結果

---

**💡 提示**：憑證是敏感資訊，請妥善保管，不要分享給他人。
