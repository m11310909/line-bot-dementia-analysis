LINE Bot Dementia Warning Analysis System
完整的失智症早期警訊分析系統，使用 Google Gemini AI 和 LINE Bot 為家庭照顧者提供專業的行為評估服務。

🏗️ 系統架構
使用者訊息 → LINE Bot → Webhook (8002) → M1 Flex API (8001) → Google Gemini → 分析結果
     ↑                                                                      ↓
LINE App ←─── Flex Message ←─── JSON 回應 ←─── AI 分析 ←──────────────────────┘
📦 檔案結構
line-bot-dementia-analysis/
├── requirements.txt           # Python 套件需求
├── .env.template             # 環境變數範本
├── setup.py                  # 安裝腳本
├── m1_flex_api.py           # Google Gemini 分析服務 (Port 8001)
├── line_bot_webhook.py      # LINE Bot 整合服務 (Port 8002)
├── start_flex.bat/.sh       # M1 Flex API 啟動腳本
├── start_webhook.bat/.sh    # Webhook 啟動腳本
└── README.md                # 說明文件
🚀 快速開始
1. 安裝與設定
bash
# 1. 執行安裝腳本
python setup.py

# 2. 設定環境變數
cp .env.template .env
# 編輯 .env 檔案，填入你的 API 金鑰
2. 設定環境變數
編輯 .env 檔案：

bash
# LINE Bot 憑證
LINE_CHANNEL_ACCESS_TOKEN=你的_LINE_頻道_存取_權杖
LINE_CHANNEL_SECRET=你的_LINE_頻道_密鑰

# Google AI Studio API 金鑰  
AISTUDIO_API_KEY=你的_Google_AI_Studio_API_金鑰

# 可選：API 端點
FLEX_API_URL=http://localhost:8001/m1-flex
如何取得 API 金鑰：
LINE Bot 憑證: LINE Developers Console
Google AI Studio API: AI Studio
3. 啟動服務（3 個終端）
方法 A：使用啟動腳本
Windows:

bash
# 終端 1: M1 Flex API
start_flex.bat

# 終端 2: LINE Bot Webhook  
start_webhook.bat
Unix/Mac:

bash
# 終端 1: M1 Flex API
./start_flex.sh

# 終端 2: LINE Bot Webhook
./start_webhook.sh
方法 B：手動啟動
bash
# 終端 1: M1 Flex API (Google Gemini 分析)
python m1_flex_api.py

# 終端 2: LINE Bot Webhook (LINE 整合)
python line_bot_webhook.py

# 終端 3: Ngrok 隧道 (讓 LINE 可以連到你的服務)
ngrok http 8002
4. 設定 LINE Bot Webhook
啟動 ngrok 後，複製 https URL（例如：https://abc123.ngrok.io）
到 LINE Developers Console
選擇你的 Bot → Messaging API
設定 Webhook URL: https://abc123.ngrok.io/webhook
啟用 "Use webhook"
點擊 "Verify" 確認連線成功
🧪 測試系統
1. 檢查服務狀態
bash
# 測試 M1 Flex API
curl http://localhost:8001/health

# 測試 LINE Bot Webhook
curl http://localhost:8002/health
2. 測試分析功能
bash
# 直接測試 Gemini 分析
curl -X POST http://localhost:8001/m1-flex \
  -H "Content-Type: application/json" \
  -d '{"user_input": "媽媽最近常重複問同樣的問題"}'
3. 測試 LINE Bot
掃描 LINE Developers Console 中的 QR Code 加 Bot 為好友
發送訊息測試：
help - 顯示使用說明
媽媽最近常忘記關瓦斯 - 分析失智症警訊
爸爸重複問同樣問題 - 另一個測試範例
🔧 系統功能
失智症十大警訊分析
系統可以分析以下 10 種早期警訊：

M1-01: 記憶力減退影響生活
M1-02: 計劃事情或解決問題有困難
M1-03: 無法勝任原本熟悉的事務
M1-04: 對時間地點感到混淆
M1-05: 有困難理解視覺影像和空間關係
M1-06: 言語表達或書寫出現困難
M1-07: 東西擺放錯亂且失去回頭尋找的能力
M1-08: 判斷力變差或減弱
M1-09: 從工作或社交活動中退出
M1-10: 情緒和個性的改變
Flex Message 回應格式
每個分析結果包含：

🔸 使用者描述: 總結使用者的輸入
✅ 正常老化: 對應的正常老化現象
⚠️ 失智警訊: 需要注意的失智症徵象
🔁 建議行動: 具體的後續建議
🔗 更多資訊: 連結到專業資源
🛠️ 故障排除
常見問題
1. "Missing AISTUDIO_API_KEY"
解決方法: 到 Google AI Studio 申請 API 金鑰並設定到環境變數

2. "Missing LINE Bot credentials"
解決方法: 到 LINE Developers 建立 Bot 並取得憑證

3. "Cannot connect to Flex API"
檢查:

M1 Flex API 是否在 port 8001 運行
防火牆是否阻擋 localhost:8001
查看 M1 Flex API 終端的錯誤訊息
4. "Invalid LINE signature"
檢查:

LINE_CHANNEL_SECRET 是否正確設定
Webhook URL 是否為 https://your-ngrok.ngrok.io/webhook
確保使用 https（不是 http）的 ngrok URL
5. Bot 沒有回應
除錯步驟:

檢查三個終端都有在運行
個別測試每個組件
確認 ngrok 隧道還在運作
驗證 LINE Bot webhook 設定
記錄檔分析
尋找這些記錄訊息：

✅ Google AI configured - Gemini 設定成功
✅ LINE Bot API initialized - LINE Bot 設定成功
📨 Webhook request received - LINE 正在呼叫你的 webhook
✅ Webhook processed successfully - 訊息處理成功
❌ Invalid LINE signature - 檢查你的頻道密鑰
🔍 開發與除錯
API 端點
M1 Flex API (Port 8001):

POST /m1-flex - 主要分析端點
GET /health - 健康檢查
GET /docs - API 文件
POST /test - 測試端點
LINE Bot Webhook (Port 8002):

POST /webhook - LINE webhook 端點
GET /health - 健康檢查
GET /info - Bot 資訊
POST /test-webhook - 測試端點
手動測試 Webhook
bash
# 測試 webhook（替換為你的 ngrok URL）
curl -X POST https://your-ngrok-url.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -H "X-Line-Signature: test" \
  -d '{"events":[]}'
📈 擴充功能
系統設計為模組化，可以輕鬆擴充：

多語言支援: 加入英文、日文等語言分析
更多評估模組: 擴充到 M2-M9 其他評估類型
資料庫整合: 儲存使用者互動記錄
進階分析: 加入趨勢分析和個人化建議
網頁介面: 建立管理後台
📄 授權
此專案僅供教育和研究用途。請諮詢專業醫師進行正式的失智症評估。

🆘 支援
如果遇到問題：

檢查 故障排除 章節
查看終端的錯誤訊息
確認所有環境變數都正確設定
驗證 API 金鑰是否有效
⚠️ 重要提醒: 此系統僅供參考，不可取代專業醫療診斷。如有疑慮請諮詢神經內科或記憶門診專業醫師。

