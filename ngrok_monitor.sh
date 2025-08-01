#!/bin/bash

echo "📺 ngrok 實時監控"
echo "按 Ctrl+C 退出"
echo "=================="

while true; do
    clear
    echo "📊 ngrok 監控面板 - $(date)"
    echo "=============================="
    
    # 進程狀態
    if pgrep -f "ngrok" > /dev/null; then
        ngrok_pid=$(pgrep -f "ngrok")
        echo "✅ ngrok 運行中 (PID: $ngrok_pid)"
        
        # 進程運行時間
        if command -v ps &> /dev/null; then
            runtime=$(ps -o etime= -p $ngrok_pid 2>/dev/null | tr -d ' ')
            echo "⏱️  運行時間: $runtime"
        fi
    else
        echo "❌ ngrok 未運行"
    fi
    
    echo ""
    
    # API 狀態和隧道信息
    api_found=false
    for port in 4040 4041 4042; do
        if curl -s "http://localhost:$port/api/tunnels" > /dev/null 2>&1; then
            echo "🌐 ngrok API (端口 $port):"
            api_found=true
            
            if command -v jq &> /dev/null; then
                # 使用 jq 解析詳細信息
                tunnels_info=$(curl -s "http://localhost:$port/api/tunnels" | jq -r '
                    .tunnels[] | 
                    "  📡 \(.name):\n    Public: \(.public_url)\n    Local:  \(.config.addr)\n    Requests: \(.metrics.http.count // 0)"
                ')
                if [ -n "$tunnels_info" ]; then
                    echo "$tunnels_info"
                else
                    echo "  📭 無活動隧道"
                fi
            else
                # 簡單解析
                public_urls=$(curl -s "http://localhost:$port/api/tunnels" | grep -o 'https://[^"]*\.ngrok[^"]*')
                if [ -n "$public_urls" ]; then
                    echo "  📡 Public URLs:"
                    echo "$public_urls" | sed 's/^/    /'
                else
                    echo "  📭 無活動隧道"
                fi
            fi
            break
        fi
    done
    
    if [ "$api_found" = false ]; then
        echo "❌ ngrok API 不可用"
    fi
    
    echo ""
    
    # 保存的 URL 狀態
    if [ -f "ngrok_url.txt" ]; then
        saved_url=$(cat ngrok_url.txt)
        echo "📋 保存的 URL: $saved_url"
        
        # 快速可達性測試
        if timeout 3 curl -s "$saved_url" > /dev/null 2>&1; then
            echo "✅ URL 可達"
        else
            echo "❌ URL 不可達或響應慢"
        fi
    fi
    
    echo ""
    
    # 最新日誌
    if [ -f "ngrok.log" ]; then
        echo "📝 最新日誌:"
        tail -3 ngrok.log | sed 's/^/  /'
    fi
    
    # 刷新間隔
    sleep 5
done 