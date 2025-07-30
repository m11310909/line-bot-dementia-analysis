#!/bin/bash

# 生產環境啟動腳本

echo "🚀 啟動 LINE Bot 生產環境服務..."

# 載入環境變數
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 檢查必要配置
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "❌ 缺少 LINE Bot 憑證"
    echo "請設置 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET"
    exit 1
fi

if [ -z "$AISTUDIO_API_KEY" ]; then
    echo "❌ 缺少 Gemini API 金鑰"
    echo "請設置 AISTUDIO_API_KEY"
    exit 1
fi

# 啟動 RAG API
echo "🔧 啟動 RAG API..."
python3 m1_m2_m3_integrated_api.py &
RAG_PID=$!

# 等待 RAG API 啟動
sleep 5

# 檢查 RAG API 健康狀態
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ RAG API 啟動成功"
else
    echo "❌ RAG API 啟動失敗"
    exit 1
fi

# 啟動 LINE Bot Webhook
echo "🤖 啟動 LINE Bot Webhook..."
python3 updated_line_bot_webhook.py &
WEBHOOK_PID=$!

echo "✅ 生產環境服務啟動完成"
echo "📊 服務狀態："
echo "   RAG API: http://localhost:8005"
echo "   Webhook: 運行中"
echo "   PID: RAG($RAG_PID), Webhook($WEBHOOK_PID)"

# 等待中斷信號
trap "echo '🛑 停止服務...'; kill $RAG_PID $WEBHOOK_PID; exit" INT TERM
wait
