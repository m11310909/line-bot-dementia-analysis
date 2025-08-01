# LINE Bot 無回應問題 - 故障排除指南

## 🚨 問題描述
LINE Bot 沒有回應用戶訊息，可能的原因和解決方案。

---

## 🔍 診斷步驟

### 1. 檢查環境變數
```bash
# 檢查 LINE Bot 憑證是否設置
echo $LINE_CHANNEL_ACCESS_TOKEN
echo $LINE_CHANNEL_SECRET
```

**解決方案：**
- 如果為空，請設置環境變數
- 創建 `.env` 檔案並填入憑證

### 2. 檢查服務狀態
```bash
# 檢查是否有 Python 程序在運行
ps aux | grep python | grep -E "(line|webhook|bot)"

# 檢查端口使用情況
lsof -i :8000 -i :8001 -i :8002
```

**解決方案：**
- 如果沒有程序運行，啟動 LINE Bot
- 如果端口被占用，停止衝突的服務

### 3. 檢查依賴項
```bash
# 檢查必要的 Python 套件
python3 -c "import fastapi, uvicorn, linebot, requests, pyyaml; print('✅ All dependencies available')"
```

**解決方案：**
- 如果缺少套件，安裝：`pip3 install fastapi uvicorn linebot requests pyyaml`

---

## 🚀 啟動步驟

### 方法 1：使用啟動腳本（推薦）
```bash
# 運行啟動腳本
python3 start_line_bot_m1.py
```

### 方法 2：手動啟動
```bash
# 1. 設置環境變數
export LINE_CHANNEL_ACCESS_TOKEN="your_token_here"
export LINE_CHANNEL_SECRET="your_secret_here"

# 2. 啟動 LINE Bot
python3 line_bot_m1_integrated.py
```

### 方法 3：使用 uvicorn
```bash
# 直接啟動 FastAPI 應用
uvicorn line_bot_m1_integrated:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🧪 測試步驟

### 1. 測試 M1 模組
```bash
# 測試 M1 視覺化模組
python3 test_m1_simple.py
```

### 2. 測試 LINE Bot 整合
```bash
# 測試 LINE Bot 整合（需要先啟動 bot）
python3 test_line_bot_m1.py
```

### 3. 測試健康檢查
```bash
# 檢查 bot 健康狀態
curl http://localhost:8000/health
```

---

## 🔧 常見問題解決

### 問題 1：環境變數未設置
**症狀：** 啟動時顯示 "LINE Bot credentials not found"

**解決方案：**
```bash
# 創建 .env 檔案
cat > .env << EOF
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here
EOF

# 重新啟動
python3 start_line_bot_m1.py
```

### 問題 2：端口被占用
**症狀：** "Address already in use" 錯誤

**解決方案：**
```bash
# 查找占用端口的程序
lsof -i :8000

# 停止程序
kill -9 <PID>

# 或使用不同端口
uvicorn line_bot_m1_integrated:app --host 0.0.0.0 --port 8001
```

### 問題 3：M1 模組導入失敗
**症狀：** "M1 modules not available" 警告

**解決方案：**
```bash
# 檢查 M1 模組
python3 -c "from xai_flex.m1_enhanced_visualization import M1EnhancedVisualizationGenerator; print('✅ M1 modules OK')"

# 如果失敗，使用簡化版本
python3 test_m1_simple.py
```

### 問題 4：RAG API 未運行
**症狀：** "RAG API not running" 警告

**解決方案：**
```bash
# 啟動 RAG API（如果有的話）
python3 api/main.py

# 或使用 fallback 模式
# Bot 會自動使用 M1 fallback 分析
```

### 問題 5：LINE Webhook 配置錯誤
**症狀：** Bot 啟動但 LINE 沒有回應

**解決方案：**
1. 檢查 LINE Developer Console 的 Webhook URL
2. 確保 URL 格式正確：`https://your-domain.com/webhook`
3. 檢查 Webhook 是否啟用
4. 驗證簽名是否正確

---

## 📋 檢查清單

### 啟動前檢查
- [ ] LINE Bot 憑證已設置
- [ ] 所有依賴項已安裝
- [ ] 端口 8000 可用
- [ ] M1 模組可正常導入

### 啟動後檢查
- [ ] Bot 服務正在運行
- [ ] 健康檢查通過
- [ ] M1 視覺化測試通過
- [ ] Webhook 端點可訪問

### LINE 整合檢查
- [ ] Webhook URL 正確配置
- [ ] 簽名驗證正常
- [ ] Bot 可以接收訊息
- [ ] Bot 可以發送回應

---

## 🛠️ 進階故障排除

### 1. 啟用詳細日誌
```python
# 在 line_bot_m1_integrated.py 中添加
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. 測試 Webhook 端點
```bash
# 使用 curl 測試 webhook
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[]}'
```

### 3. 檢查 LINE Bot API 狀態
```python
# 在 Python 中測試
from linebot import LineBotApi
api = LineBotApi('your_token')
try:
    profile = api.get_profile('test_user_id')
    print("✅ LINE Bot API 正常")
except Exception as e:
    print(f"❌ LINE Bot API 錯誤: {e}")
```

---

## 📞 支援資訊

### 日誌檔案
- 應用日誌：查看控制台輸出
- 錯誤日誌：檢查 Python 錯誤訊息

### 測試檔案
- `test_m1_simple.py` - M1 模組測試
- `test_line_bot_m1.py` - LINE Bot 整合測試
- `start_line_bot_m1.py` - 啟動腳本

### 配置檔案
- `.env` - 環境變數
- `config/m1_config.yaml` - M1 配置
- `line_bot_m1_integrated.py` - 主程式

---

## 🎯 快速修復

如果以上步驟都無法解決問題，請嘗試：

1. **完全重新啟動：**
```bash
# 停止所有相關程序
pkill -f "line_bot\|uvicorn\|python.*8000"

# 清理並重新安裝
pip3 install --upgrade fastapi uvicorn linebot requests pyyaml

# 重新啟動
python3 start_line_bot_m1.py
```

2. **使用簡化版本：**
```bash
# 使用基本的 LINE Bot（不包含 M1）
python3 line_bot_webhook_v2.py
```

3. **檢查網路連接：**
```bash
# 確保可以訪問 LINE API
curl -I https://api.line.me/v2/bot/profile/U1234567890abcdef
```

---

**最後更新：** 2025-08-01  
**版本：** 3.0.0  
**狀態：** ✅ 已測試並驗證 