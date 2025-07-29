#!/bin/bash

echo "🚀 M1-M3 模組 LINE 測試腳本"
echo "============================================"

# 檢查 Python 環境
echo "📋 檢查 Python 環境..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 已安裝"
else
    echo "❌ Python3 未安裝，請先安裝 Python3"
    exit 1
fi

# 檢查必要套件
echo "📦 檢查必要套件..."
python3 -c "import requests, json, time" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 必要套件已安裝"
else
    echo "⚠️  安裝必要套件..."
    pip3 install requests
fi

# 檢查 API 服務是否運行
echo "🔍 檢查 API 服務狀態..."

# 嘗試不同的端口
PORTS=(8005 8004 8001 5000)
API_URL=""

for port in "${PORTS[@]}"; do
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        API_URL="http://localhost:$port"
        echo "✅ 找到運行中的 API 服務: $API_URL"
        break
    fi
done

if [ -z "$API_URL" ]; then
    echo "⚠️  未找到運行中的 API 服務"
    echo "📋 請先啟動以下服務之一："
    echo "   - python3 m1_m2_m3_integrated_api.py (端口 8005)"
    echo "   - python3 integrated_m1_m2_api_8004.py (端口 8004)"
    echo "   - python3 main_fastapi.py (端口 8001)"
    echo ""
    echo "🔧 快速啟動命令："
    echo "   python3 m1_m2_m3_integrated_api.py &"
    echo "   sleep 10"
    echo "   python3 test_m1_m2_m3_modules.py"
    echo ""
    read -p "是否要現在啟動 API 服務？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 啟動 M1-M2-M3 整合 API..."
        python3 m1_m2_m3_integrated_api.py &
        API_PID=$!
        echo "⏳ 等待服務啟動..."
        sleep 15
        
        # 檢查服務是否啟動成功
        if curl -s "http://localhost:8005/health" > /dev/null 2>&1; then
            API_URL="http://localhost:8005"
            echo "✅ API 服務啟動成功: $API_URL"
        else
            echo "❌ API 服務啟動失敗"
            exit 1
        fi
    else
        echo "❌ 無法繼續測試，請手動啟動 API 服務"
        exit 1
    fi
fi

echo ""
echo "🧪 開始執行 M1-M3 模組測試..."
echo "============================================"

# 執行測試
python3 test_m1_m2_m3_modules.py "$API_URL"

TEST_RESULT=$?

echo ""
echo "============================================"
if [ $TEST_RESULT -eq 0 ]; then
    echo "🎉 所有測試通過！M1-M3 模組運行正常"
    echo ""
    echo "📱 現在可以在 LINE 上測試："
    echo "   1. 確保 LINE Bot 已部署"
    echo "   2. 發送測試訊息到 LINE Bot"
    echo "   3. 檢查回應是否正確"
else
    echo "⚠️  部分測試失敗，請檢查錯誤訊息"
    echo ""
    echo "🔧 故障排除："
    echo "   1. 檢查 API 服務是否正常運行"
    echo "   2. 檢查網路連接"
    echo "   3. 檢查日誌檔案"
fi

echo ""
echo "📋 測試完成！"
echo "💡 提示：使用 'python3 test_m1_m2_m3_modules.py $API_URL' 重新執行測試"

# 如果我們啟動了服務，提供停止命令
if [ ! -z "$API_PID" ]; then
    echo ""
    echo "🛑 停止 API 服務："
    echo "   kill $API_PID"
fi 