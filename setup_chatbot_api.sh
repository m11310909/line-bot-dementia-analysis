#!/bin/bash

# 設置失智小助手 Chatbot API 配置

echo "🤖 設置失智小助手 Chatbot API 配置"
echo "=================================="

# 設置環境變數
export CHATBOT_API_URL="http://localhost:8007/analyze"
export CHATBOT_API_KEY=""
export USE_CHATBOT_API="true"

echo "✅ 環境變數已設置："
echo "   CHATBOT_API_URL: $CHATBOT_API_URL"
echo "   USE_CHATBOT_API: $USE_CHATBOT_API"

# 測試 chatbot API
echo ""
echo "🧪 測試 Chatbot API..."
curl -s http://localhost:8007/health | jq .

echo ""
echo "🎯 測試分析功能..."
curl -X POST http://localhost:8007/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "爸爸不會用洗衣機", "user_id": "test_user"}' \
  | jq . | head -20

echo ""
echo "🚀 現在可以啟動 webhook 服務："
echo "   python3 updated_line_bot_webhook.py"
echo ""
echo "💡 或者使用環境變數啟動："
echo "   USE_CHATBOT_API=true python3 updated_line_bot_webhook.py" 