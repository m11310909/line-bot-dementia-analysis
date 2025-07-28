#!/bin/bash

echo "🚀 部署增強版 LINE Bot"
echo ""

# 載入環境變數
if [ -f .env ]; then
    echo "📄 載入環境變數..."
    set -a
    source .env
    set +a
fi

# 檢查 M1+M2+M3 API
echo "🔍 檢查 M1+M2+M3 API..."
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ M1+M2+M3 API 運行正常"
else
    echo "❌ M1+M2+M3 API 未運行"
    echo "💡 請先啟動：bash final_fix_script.sh"
    exit 1
fi

# 檢查環境變數
if [ "$LINE_CHANNEL_SECRET" = "your_channel_secret_here" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "⚠️  LINE_CHANNEL_SECRET 未設定"
    echo "💡 請設定環境變數或編輯 .env 檔案"
    exit 1
fi

if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_access_token_here" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "⚠️  LINE_CHANNEL_ACCESS_TOKEN 未設定"
    echo "💡 請設定環境變數或編輯 .env 檔案"
    exit 1
fi

# 停止可能運行的舊版本
echo "🛑 停止舊版 LINE Bot..."
pkill -f "enhanced_line_bot" 2>/dev/null || echo "沒有找到舊版本"

# 啟動新版本
echo "🚀 啟動增強版 LINE Bot..."
echo "📍 服務將運行在 http://localhost:5000"
echo "📱 Webhook URL: http://your-domain.com/callback"
echo ""

python3 enhanced_line_bot.py
