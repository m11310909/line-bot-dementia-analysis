#!/bin/bash

echo "🧪 開始 API 整合測試..."

# 啟動 Mock Server (背景執行)
cd ../mocks && node mock-server.js &
SERVER_PID=$!

# 等待 server 啟動
sleep 2

echo -e "\n📡 測試 M1 API:"
curl -s -X POST http://localhost:3001/api/v1/m1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "我媽最近一整天都在找東西，她說人家偷了"}' | jq '.'

echo -e "\n📡 測試 M2 API:"
curl -s -X POST http://localhost:3001/api/v1/m2/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "晚上會起來走動，白天嗜睡，有時認不得家人"}' | jq '.'

echo -e "\n📡 測試錯誤處理:"
curl -s -X POST http://localhost:3001/api/v1/m1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "短"}' | jq '.'

echo -e "\n🏥 健康檢查:"
curl -s http://localhost:3001/api/health | jq '.'

# 停止 Mock Server
kill $SERVER_PID
echo -e "\n✅ 測試完成"
