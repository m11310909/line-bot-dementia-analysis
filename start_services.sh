#!/bin/bash

echo "🚀 啟動 LINE Bot 服務..."
echo "========================"

# 停止現有服務
echo "🛑 停止現有服務..."
pkill -f "simple_backend_api.py" 2>/dev/null
pkill -f "updated_line_bot_webhook.py" 2>/dev/null
sleep 2

# 激活虛擬環境
echo "🔧 激活虛擬環境..."
source venv/bin/activate

# 載入環境變數
echo "📋 載入環境變數..."
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ 環境變數已載入"
else
    echo "❌ .env 文件不存在"
    exit 1
fi

# 啟動後端 API
echo "🌐 啟動後端 API (端口 8000)..."
python3 simple_backend_api.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ 後端 API 已啟動 (PID: $BACKEND_PID)"

# 等待後端啟動
sleep 3

# 測試後端
echo "🧪 測試後端 API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 後端 API 正常運行"
else
    echo "❌ 後端 API 啟動失敗"
    exit 1
fi

# 啟動 LINE Bot webhook
echo "📱 啟動 LINE Bot webhook (端口 3000)..."
python3 updated_line_bot_webhook.py > webhook.log 2>&1 &
WEBHOOK_PID=$!
echo "✅ LINE Bot webhook 已啟動 (PID: $WEBHOOK_PID)"

# 等待 webhook 啟動
sleep 3

# 測試 webhook
echo "🧪 測試 LINE Bot webhook..."
if curl -s http://localhost:3000/health > /dev/null; then
    echo "✅ LINE Bot webhook 正常運行"
else
    echo "❌ LINE Bot webhook 啟動失敗"
    exit 1
fi

echo ""
echo "🎉 所有服務已啟動！"
echo "=================="
echo "📊 服務狀態:"
echo "  • 後端 API: http://localhost:8000 (PID: $BACKEND_PID)"
echo "  • LINE Bot: http://localhost:3000 (PID: $WEBHOOK_PID)"
echo "  • ngrok: https://a0f19f466cf1.ngrok-free.app"
echo ""
echo "🔧 管理命令:"
echo "  • 查看日誌: tail -f backend.log webhook.log"
echo "  • 停止服務: ./stop_services.sh"
echo "  • 重啟服務: ./restart_services.sh"
echo ""
echo "📱 LINE Bot 測試:"
echo "  在 LINE 中發送消息到您的 Bot" 