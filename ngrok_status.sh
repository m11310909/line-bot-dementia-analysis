#!/bin/bash

NGROK_URL_FILE="ngrok_url.txt"
NGROK_LOG="ngrok.log"

echo "📊 ngrok 隧道狀態檢查"
echo "======================"

# 檢查 ngrok 進程
echo "🔍 進程狀態:"
if pgrep -f "ngrok" > /dev/null; then
    ngrok_pid=$(pgrep -f "ngrok")
    echo "  ✅ ngrok 正在運行 (PID: $ngrok_pid)"
else
    echo "  ❌ ngrok 未運行"
    exit 1
fi

# 檢查 API 是否可用
echo ""
echo "🌐 API 狀態:"
api_available=false
for port in 4040 4041 4042; do
    if curl -s "http://localhost:$port/api/tunnels" > /dev/null 2>&1; then
        echo "  ✅ ngrok API 可用 (端口 $port)"
        api_available=true
        
        # 獲取隧道信息
        if command -v jq &> /dev/null; then
            tunnels=$(curl -s "http://localhost:$port/api/tunnels" | jq -r '.tunnels[] | "\(.name): \(.public_url) -> \(.config.addr)"')
            if [ -n "$tunnels" ]; then
                echo "  📡 活動隧道:"
                echo "$tunnels" | sed 's/^/    /'
            fi
        else
            echo "  💡 安裝 jq 以獲得詳細隧道信息"
        fi
        break
    fi
done

if [ "$api_available" = false ]; then
    echo "  ❌ ngrok API 不可用"
fi

# 檢查保存的 URL
echo ""
echo "📁 URL 文件:"
if [ -f "$NGROK_URL_FILE" ]; then
    saved_url=$(cat "$NGROK_URL_FILE")
    echo "  📋 保存的 URL: $saved_url"
    
    # 測試 URL 可達性
    if curl -s --max-time 5 "$saved_url" > /dev/null; then
        echo "  ✅ URL 可達"
    else
        echo "  ❌ URL 不可達"
    fi
else
    echo "  ❌ URL 文件不存在"
fi

# 檢查日誌
echo ""
echo "📝 最新日誌 (最後 5 行):"
if [ -f "$NGROK_LOG" ]; then
    tail -5 "$NGROK_LOG" | sed 's/^/  /'
else
    echo "  ❌ 日誌文件不存在"
fi 