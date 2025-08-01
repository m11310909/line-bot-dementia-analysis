#!/bin/bash

echo "🔍 LINE Bot 系統狀態檢查"
echo "========================"

# 檢查進程
echo "📊 進程狀態:"
backend_running=false
webhook_running=false

if pgrep -f "simple_backend_api.py" > /dev/null; then
    backend_pid=$(pgrep -f "simple_backend_api.py")
    echo "  ✅ 後端 API 運行中 (PID: $backend_pid)"
    backend_running=true
else
    echo "  ❌ 後端 API 未運行"
fi

if pgrep -f "updated_line_bot_webhook.py" > /dev/null; then
    webhook_pid=$(pgrep -f "updated_line_bot_webhook.py")
    echo "  ✅ LINE Bot webhook 運行中 (PID: $webhook_pid)"
    webhook_running=true
else
    echo "  ❌ LINE Bot webhook 未運行"
fi

if pgrep -f "ngrok" > /dev/null; then
    ngrok_pid=$(pgrep -f "ngrok")
    echo "  ✅ ngrok 隧道運行中 (PID: $ngrok_pid)"
else
    echo "  ❌ ngrok 隧道未運行"
fi

echo ""

# 檢查端口
echo "🌐 端口狀態:"
if lsof -i :8000 > /dev/null 2>&1; then
    echo "  ✅ 端口 8000 (後端 API) 正在監聽"
else
    echo "  ❌ 端口 8000 (後端 API) 未監聽"
fi

if lsof -i :3000 > /dev/null 2>&1; then
    echo "  ✅ 端口 3000 (LINE Bot) 正在監聽"
else
    echo "  ❌ 端口 3000 (LINE Bot) 未監聽"
fi

echo ""

# 檢查服務健康狀態
echo "🏥 服務健康檢查:"

if [ "$backend_running" = true ]; then
    backend_health=$(curl -s http://localhost:8000/health 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "  ✅ 後端 API 健康檢查通過"
        echo "     $(echo $backend_health | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2, ensure_ascii=False))" 2>/dev/null | head -3)"
    else
        echo "  ❌ 後端 API 健康檢查失敗"
    fi
else
    echo "  ⚠️  後端 API 未運行，跳過健康檢查"
fi

if [ "$webhook_running" = true ]; then
    webhook_health=$(curl -s http://localhost:3000/health 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "  ✅ LINE Bot webhook 健康檢查通過"
        status=$(echo $webhook_health | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status', 'unknown'))" 2>/dev/null)
        line_bot_status=$(echo $webhook_health | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('services', {}).get('line_bot', {}).get('status', 'unknown'))" 2>/dev/null)
        rag_api_status=$(echo $webhook_health | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('services', {}).get('rag_api', {}).get('status', 'unknown'))" 2>/dev/null)
        echo "     整體狀態: $status"
        echo "     LINE Bot: $line_bot_status"
        echo "     RAG API: $rag_api_status"
    else
        echo "  ❌ LINE Bot webhook 健康檢查失敗"
    fi
else
    echo "  ⚠️  LINE Bot webhook 未運行，跳過健康檢查"
fi

echo ""

# 檢查 ngrok 隧道
echo "📡 ngrok 隧道狀態:"
if [ -f "ngrok_url.txt" ]; then
    ngrok_url=$(cat ngrok_url.txt)
    echo "  📋 保存的 URL: $ngrok_url"
    
    # 測試隧道可達性
    if curl -s --max-time 5 "$ngrok_url" > /dev/null; then
        echo "  ✅ ngrok 隧道可達"
        
        # 測試 webhook 端點
        webhook_response=$(curl -s --max-time 5 "$ngrok_url/webhook" 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "  ✅ webhook 端點可達"
        else
            echo "  ❌ webhook 端點不可達"
        fi
    else
        echo "  ❌ ngrok 隧道不可達"
    fi
else
    echo "  ❌ ngrok URL 文件不存在"
fi

echo ""

# 檢查環境變數
echo "🔧 環境變數檢查:"
if [ -f ".env" ]; then
    echo "  ✅ .env 文件存在"
    
    # 檢查關鍵變數
    if grep -q "LINE_CHANNEL_ACCESS_TOKEN" .env; then
        echo "  ✅ LINE_CHANNEL_ACCESS_TOKEN 已設置"
    else
        echo "  ❌ LINE_CHANNEL_ACCESS_TOKEN 未設置"
    fi
    
    if grep -q "LINE_CHANNEL_SECRET" .env; then
        echo "  ✅ LINE_CHANNEL_SECRET 已設置"
    else
        echo "  ❌ LINE_CHANNEL_SECRET 未設置"
    fi
    
    if grep -q "FLEX_API_URL.*8000" .env; then
        echo "  ✅ FLEX_API_URL 指向正確端口 (8000)"
    else
        echo "  ❌ FLEX_API_URL 可能指向錯誤端口"
    fi
else
    echo "  ❌ .env 文件不存在"
fi

echo ""

# 總結
echo "📋 系統總結:"
if [ "$backend_running" = true ] && [ "$webhook_running" = true ]; then
    echo "  🎉 所有核心服務正在運行"
    echo "  📱 LINE Bot 應該可以正常回應消息"
else
    echo "  ⚠️  部分服務未運行，請檢查並重啟"
fi

echo ""
echo "🔧 管理命令:"
echo "  ./start_services.sh    - 啟動所有服務"
echo "  ./stop_services.sh     - 停止所有服務"
echo "  ./restart_services.sh  - 重啟所有服務"
echo "  ./ngrok_status.sh      - 檢查 ngrok 狀態"
echo "  tail -f backend.log    - 查看後端日誌"
echo "  tail -f webhook.log    - 查看 webhook 日誌" 