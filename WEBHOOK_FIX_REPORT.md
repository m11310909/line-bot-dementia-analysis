# LINE Bot Webhook 修復報告

## 問題診斷

根據終端輸出，發現以下問題：

### 1. 簽名驗證失敗
```
❌ 簽名驗證失敗
ERROR:__main__:Webhook error: 400: Invalid signature
```

### 2. 事件解析錯誤
```
❌ Webhook 處理失敗: 4 validation errors for UnknownEvent
timestamp
  field required (type=value_error.missing)
mode
  field required (type=value_error.missing)
webhookEventId
  field required (type=value_error.missing)
deliveryContext
  field required (type=value_error.missing)
```

### 3. 未知事件類型
```
INFO:linebot:Unknown event type. type=message
```

## 修復措施

### 1. 改進簽名驗證
- 添加詳細的簽名驗證日誌
- 檢查 LINE_CHANNEL_SECRET 是否正確設置
- 添加簽名驗證錯誤處理

### 2. 增強事件處理
- 添加 JSON 解析檢查
- 實現手動事件處理作為備用方案
- 改進錯誤處理和日誌記錄

### 3. 多層次事件處理
- 添加通用訊息處理器
- 支持多種事件類型
- 改進事件類型檢測

## 修復後的代碼改進

### 1. 環境變數檢查
```python
def initialize_line_bot():
    try:
        channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        channel_secret = os.getenv("LINE_CHANNEL_SECRET")
        
        print(f"🔍 檢查 LINE Bot 憑證:")
        print(f"   Channel Access Token: {'✅ 已設置' if channel_access_token else '❌ 未設置'}")
        print(f"   Channel Secret: {'✅ 已設置' if channel_secret else '❌ 未設置'}")
```

### 2. 改進的 Webhook 處理
```python
@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        signature = request.headers.get("X-Line-Signature", "")
        
        # 檢查 LINE Bot 是否已初始化
        if not line_bot_api or not handler:
            print("❌ LINE Bot 未初始化")
            raise HTTPException(status_code=500, detail="LINE Bot not initialized")
        
        # 驗證簽名並處理事件
        try:
            body_str = body.decode('utf-8')
            
            # 嘗試解析 JSON 以檢查事件結構
            try:
                event_data = json.loads(body_str)
                print(f"📊 事件數量: {len(event_data.get('events', []))}")
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON 解析錯誤: {e}")
            
            handler.handle(body_str, signature)
            print("✅ Webhook 處理成功")
            
        except InvalidSignatureError as e:
            print(f"❌ 簽名驗證失敗: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")
            
        except Exception as e:
            print(f"❌ Webhook 處理失敗: {e}")
            # 嘗試手動處理事件
            # ... 手動處理邏輯
```

### 3. 多層次事件處理器
```python
# 處理文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """處理 LINE Bot 文字訊息"""
    try:
        print(f"📨 處理 LINE 訊息事件")
        handle_line_message(event)
    except Exception as e:
        logger.error(f"處理 LINE 訊息事件失敗: {e}")

# 處理所有訊息類型
@handler.add(MessageEvent)
def handle_all_messages(event):
    """處理所有類型的訊息"""
    try:
        if isinstance(event.message, TextMessageContent):
            handle_line_message(event)
        else:
            print(f"⚠️ 忽略非文字訊息: {type(event.message)}")
    except Exception as e:
        logger.error(f"處理所有訊息事件失敗: {e}")
```

## 測試工具

### 1. 配置測試
```bash
python3 test_line_bot_config.py
```

### 2. 簽名驗證測試
```bash
python3 test_webhook_signature.py
```

### 3. Webhook 端點測試
```bash
python3 test_webhook_endpoint.py
```

## 使用步驟

### 1. 檢查環境變數
```bash
python3 test_line_bot_config.py
```

### 2. 啟動修復後的 API
```bash
python3 enhanced_m1_m2_m3_integrated_api_fixed.py
```

### 3. 測試 Webhook
```bash
python3 test_webhook_endpoint.py
```

### 4. 檢查 ngrok 狀態
確保 ngrok 正在運行並轉發到正確的端口：
```bash
ngrok http 8005
```

## 預期結果

修復後應該看到：
- ✅ LINE Bot 初始化成功
- ✅ 環境變數檢查通過
- ✅ API 啟動完成
- ✅ Webhook 處理成功
- ✅ 簽名驗證通過

## 故障排除

### 如果仍然有簽名驗證失敗：
1. 檢查 LINE_CHANNEL_SECRET 是否正確
2. 確認 ngrok URL 是否正確設置在 LINE Developer Console
3. 檢查 webhook URL 是否為 HTTPS

### 如果事件解析仍然失敗：
1. 檢查 LINE Bot SDK 版本
2. 確認事件格式是否符合最新標準
3. 查看手動處理是否成功

## 總結

這些修復措施應該解決：
- 簽名驗證失敗問題
- 事件解析錯誤
- 未知事件類型問題
- 提供更好的錯誤診斷和日誌記錄

修復後的系統應該能夠正常處理 LINE Bot webhook 請求並回應用戶訊息。 