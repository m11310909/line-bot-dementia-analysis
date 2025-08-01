#!/bin/bash

echo "🔧 LINE Bot 快速修復"
echo "===================="

# 1. 停止所有相關進程
echo "📛 停止現有進程..."
pkill -f "enhanced_line_bot_demo"
pkill -f "updated_line_bot_webhook"
pkill -f "line_bot_demo"
sleep 2

# 2. 檢查環境變數
echo "🔍 檢查 LINE 憑證..."
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "❌ LINE_CHANNEL_ACCESS_TOKEN 未設定"
    echo "請設定您的 LINE Bot 憑證"
    echo ""
    echo "設定方法："
    echo "1. 訪問 https://developers.line.biz/console/"
    echo "2. 創建 Messaging API Channel"
    echo "3. 獲取 Channel Access Token 和 Channel Secret"
    echo "4. 設定環境變數："
    echo "   export LINE_CHANNEL_ACCESS_TOKEN=your_token_here"
    echo "   export LINE_CHANNEL_SECRET=your_secret_here"
    exit 1
fi

if [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "❌ LINE_CHANNEL_SECRET 未設定"
    echo "請設定您的 LINE Bot 憑證"
    exit 1
fi

echo "✅ LINE 憑證已設定"

# 3. 檢查端口是否被佔用
echo "🔍 檢查端口 8000..."
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 8000 已被佔用，正在清理..."
    lsof -ti:8000 | xargs kill -9
    sleep 2
fi

# 4. 啟動 LINE Bot Webhook 服務
echo "🚀 啟動 LINE Bot Webhook 服務..."
python3 updated_line_bot_webhook.py &
WEBHOOK_PID=$!

# 5. 等待服務啟動
echo "⏳ 等待服務啟動..."
sleep 5

# 6. 測試服務
echo "🧪 測試服務..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 服務啟動成功！"
    echo ""
    echo "📱 下一步："
    echo "1. 設定 Webhook URL: https://your-domain.com/webhook"
    echo "2. 或使用 ngrok 進行本地測試："
    echo "   ngrok http 8000"
    echo ""
    echo "🔗 服務資訊："
    curl -s http://localhost:8000/info | python3 -m json.tool 2>/dev/null || echo "無法獲取服務資訊"
else
    echo "❌ 服務啟動失敗"
    echo "請檢查錯誤日誌"
    kill $WEBHOOK_PID 2>/dev/null
    exit 1
fi

echo ""
echo "✅ LINE Bot 修復完成！"
echo "PID: $WEBHOOK_PID" 