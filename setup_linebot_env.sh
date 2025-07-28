#!/bin/bash

echo "🔧 LINE Bot 環境設定"
echo ""

# 檢查必要的 Python 套件
echo "📦 檢查 Python 套件..."
python3 -c "import flask, requests, linebot" 2>/dev/null || {
    echo "⚠️  缺少必要套件，正在安裝..."
    pip3 install flask requests line-bot-sdk
}
echo "✅ Python 套件檢查完成"

# 建立環境變數設定檔
cat > .env << 'ENV_FILE'
# LINE Bot 環境變數設定
# 請將下面的值替換為你的實際 LINE Bot 設定

# LINE Channel Secret
LINE_CHANNEL_SECRET=your_channel_secret_here

# LINE Channel Access Token  
LINE_CHANNEL_ACCESS_TOKEN=your_access_token_here

# M1+M2+M3 API 設定
API_BASE_URL=http://localhost:8005
ANALYSIS_ENDPOINT=http://localhost:8005/comprehensive-analysis

# 日誌設定
LOG_LEVEL=INFO
ENV_FILE

echo "📄 環境變數設定檔已建立：.env"
echo ""
echo "🔧 請編輯 .env 檔案，設定你的 LINE Bot 參數："
echo "   1. LINE_CHANNEL_SECRET"
echo "   2. LINE_CHANNEL_ACCESS_TOKEN"
echo ""
echo "💡 或執行以下命令直接設定："
echo "   export LINE_CHANNEL_SECRET='your_actual_secret'"
echo "   export LINE_CHANNEL_ACCESS_TOKEN='your_actual_token'"
