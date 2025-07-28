#!/bin/bash

echo "🧪 測試增強版 LINE Bot"
echo ""

# 測試健康檢查
echo "📊 測試健康檢查："
curl -s http://localhost:5000/health | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'狀態：{data.get(\"status\")}')
    print(f'API 狀態：{data.get(\"api_status\")}')
    stats = data.get('stats', {})
    print(f'總請求：{stats.get(\"total_requests\", 0)}')
except:
    print('健康檢查失敗')
"

echo ""
echo "📋 測試基本資訊："
curl -s http://localhost:5000/ | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'版本：{data.get(\"version\")}')
    print(f'狀態：{data.get(\"status\")}')
    features = data.get('features', [])
    print('功能：')
    for feature in features:
        print(f'  - {feature}')
except:
    print('基本資訊測試失敗')
"

echo ""
echo "✅ 測試完成"
echo "💡 如果看到正常回應，表示 LINE Bot 運行正常"
