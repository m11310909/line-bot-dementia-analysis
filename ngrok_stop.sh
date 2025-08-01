#!/bin/bash

echo "🛑 停止 ngrok 隧道..."

# 檢查是否有 ngrok 進程運行
if ! pgrep -f "ngrok" > /dev/null; then
    echo "✅ ngrok 未運行"
    exit 0
fi

# 獲取進程 ID
ngrok_pids=$(pgrep -f "ngrok")
echo "📋 找到 ngrok 進程: $ngrok_pids"

# 優雅關閉
echo "🔄 嘗試優雅關閉..."
pkill -TERM ngrok
sleep 3

# 檢查是否還有進程運行
if pgrep -f "ngrok" > /dev/null; then
    echo "⚡ 強制終止..."
    pkill -KILL ngrok
    sleep 1
fi

# 最終檢查
if pgrep -f "ngrok" > /dev/null; then
    echo "❌ 部分 ngrok 進程仍在運行"
    echo "請手動終止: kill -9 $(pgrep -f ngrok)"
else
    echo "✅ 所有 ngrok 進程已停止"
fi

# 清理文件
echo "🧹 清理臨時文件..."
rm -f ngrok.log
echo "✅ 清理完成" 