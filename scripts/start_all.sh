#!/bin/bash

echo "🚀 啟動失智症分析系統"
echo "======================"

# 檢查環境變數
if [[ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]]; then
    echo "⚠️ 警告: LINE_CHANNEL_ACCESS_TOKEN 未設定"
fi

if [[ -z "$AISTUDIO_API_KEY" ]]; then
    echo "⚠️ 警告: AISTUDIO_API_KEY 未設定"
fi

# 記憶體檢查
python -c "
try:
    import psutil
    mem = psutil.virtual_memory()
    print(f'📊 啟動前記憶體使用: {mem.percent:.1f}%')
    if mem.percent > 70:
        print('⚠️ 記憶體使用偏高，建議重啟 Replit')
except ImportError:
    print('📊 記憶體監控模組未安裝')
" 2>/dev/null || echo "📊 無法檢查記憶體使用"

# 安裝依賴（如果需要）
if [[ -f "requirements.txt" ]]; then
    echo "📦 檢查依賴套件..."
    pip install -r requirements.txt --quiet
fi

# 啟動 API 服務
echo "🚀 啟動 API 服務..."
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# 等待服務啟動
sleep 3

# 健康檢查
echo "🔍 執行健康檢查..."
curl -s http://localhost:8000/health 2>/dev/null | python -m json.tool 2>/dev/null || echo "健康檢查: API 服務可能尚未完全啟動"

echo "✅ 系統啟動完成"
echo "📝 API 文件: http://localhost:8000/docs"
echo "🔧 管理介面: http://localhost:8000"

# 等待中斷信號
trap "echo '🛑 正在關閉服務...'; kill $API_PID 2>/dev/null; exit" INT TERM
wait $API_PID
