#!/bin/bash

# === 設定 ===
LOCAL_PORT=3000
NGROK_LOG="ngrok.log"
API_PORTS=(4040 4041 4042)

echo "🚫 終止現有 ngrok..."
pkill ngrok
sleep 2

echo "🚀 啟動 ngrok 並導出至背景 log 檔..."
nohup ngrok http $LOCAL_PORT > $NGROK_LOG 2>&1 &

# 等待 ngrok 啟動
echo "⏳ 等待 ngrok 初始化..."
sleep 5

# 嘗試取得 ngrok public URL
for PORT in "${API_PORTS[@]}"; do
    NGROK_URL=$(curl -s http://localhost:$PORT/api/tunnels | grep -Eo 'https://[a-z0-9]+\.ngrok-free\.app' | head -n 1)
    if [ -n "$NGROK_URL" ]; then
        echo "✅ Ngrok Public URL:"
        echo "$NGROK_URL"
        exit 0
    fi
done

echo "❌ 無法擷取 ngrok public URL。請檢查 ngrok 是否成功啟動。"
exit 1 