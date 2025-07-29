#!/bin/bash

echo "🧪 開始 API 整合測試..."

# 啟動 Mock Server（背景執行）
cd ../mocks && node mock-server.js &
SERVER_PID=$!
cd ../tests

# 等待 server 啟動
sleep 2

# 判斷是否有 jq
if command -v jq &> /dev/null; then
  JQ="jq"
  echo "✅ 偵測到 jq，將以美化格式顯示 JSON"
else
  JQ="cat"
  echo "⚠️ 未安裝 jq，將直接輸出原始 JSON（無格式化）"
fi

echo -e "\n📡 測試 M1 API:"
curl -s -X POST http://localhost:3001/api/v1/m1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "我媽最近一整天都在找東西，她說人家偷了"}' | $JQ

echo -e "\n📡 測試 M2 API:"
curl -s -X POST http://localhost:3001/api/v1/m2/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "晚上會起來走動，白天嗜睡，有時認不得家人"}' | $JQ

echo -e "\n📡 測試錯誤處理:"
curl -s -X POST http://localhost:3001/api/v1/m1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "短"}' | $JQ

echo -e "\n🏥 健康檢查:"
curl -s http://localhost:3001/api/health | $JQ

# 關閉 Mock Server
if kill $SERVER_PID 2>/dev/null; then
  echo -e "\n🛑 Mock Server 已停止"
else
  echo -e "\n⚠️ 無法關閉 Mock Server，可能已被手動終止"
fi

echo -e "\n✅ 測試完成"
