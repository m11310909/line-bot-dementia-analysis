#!/bin/bash

NGROK_URL_FILE="ngrok_url.txt"

echo "🧪 ngrok 隧道測試"
echo "=================="

# 檢查 URL 文件
if [ ! -f "$NGROK_URL_FILE" ]; then
    echo "❌ URL 文件不存在: $NGROK_URL_FILE"
    echo "請先運行 ./setup_ngrok_enhanced.sh"
    exit 1
fi

NGROK_URL=$(cat "$NGROK_URL_FILE")
echo "📋 測試 URL: $NGROK_URL"

# 基本連通性測試
echo ""
echo "🔗 基本連通性測試:"
if curl -s --max-time 10 "$NGROK_URL" > /dev/null; then
    echo "✅ 基本連通性正常"
else
    echo "❌ 基本連通性失敗"
    exit 1
fi

# 健康檢查端點測試
echo ""
echo "🏥 健康檢查測試:"
health_url="${NGROK_URL}/health"
health_response=$(curl -s --max-time 10 "$health_url")

if [ $? -eq 0 ]; then
    echo "✅ 健康檢查端點可達"
    if command -v jq &> /dev/null; then
        echo "$health_response" | jq . 2>/dev/null || echo "響應: $health_response"
    else
        echo "響應: $health_response"
    fi
else
    echo "❌ 健康檢查端點不可達"
fi

# LINE webhook 端點測試
echo ""
echo "📱 LINE webhook 端點測試:"
webhook_url="${NGROK_URL}/webhook"
webhook_response=$(curl -s -X POST --max-time 10 \
    -H "Content-Type: application/json" \
    -d '{"events":[]}' \
    "$webhook_url")

if [ $? -eq 0 ]; then
    echo "✅ Webhook 端點可達"
    echo "響應: $webhook_response"
else
    echo "❌ Webhook 端點測試失敗"
fi

# 響應時間測試
echo ""
echo "⏱️  響應時間測試:"
response_time=$(curl -o /dev/null -s -w "%{time_total}" --max-time 10 "$NGROK_URL")
if [ $? -eq 0 ]; then
    echo "⚡ 響應時間: ${response_time}s"
    
    # 評估響應時間
    if (( $(echo "$response_time < 1.0" | bc -l 2>/dev/null) )); then
        echo "✅ 響應時間良好"
    elif (( $(echo "$response_time < 3.0" | bc -l 2>/dev/null) )); then
        echo "⚠️  響應時間一般"
    else
        echo "🐌 響應時間較慢"
    fi
else
    echo "❌ 響應時間測試失敗"
fi

echo ""
echo "🎉 測試完成!" 