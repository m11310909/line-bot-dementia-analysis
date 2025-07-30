#!/bin/bash

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔐 憑證驗證腳本${NC}"
echo "=================================================="

# 檢查 .env 檔案
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env 檔案不存在${NC}"
    echo "正在創建 .env 檔案..."
    
    cat > .env << 'EOF'
# LINE Bot 憑證配置
LINE_CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token_here
LINE_CHANNEL_SECRET=your_actual_channel_secret_here

# API 配置
FLEX_API_URL=http://localhost:8005/comprehensive-analysis
RAG_HEALTH_URL=http://localhost:8005/health
RAG_ANALYZE_URL=http://localhost:8005/comprehensive-analysis

# 生產環境配置
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG_MODE=false

# Redis 配置
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# Gemini API 配置
AISTUDIO_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# 監控配置
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true
EOF
    
    echo -e "${GREEN}✅ .env 檔案已創建${NC}"
    echo -e "${YELLOW}⚠️  請編輯 .env 檔案並填入實際的憑證${NC}"
else
    echo -e "${GREEN}✅ .env 檔案已存在${NC}"
fi

# 載入環境變數
source .env

echo ""
echo -e "${BLUE}📋 當前憑證狀態...${NC}"

# 檢查 LINE Bot 憑證
echo -e "${BLUE}🔍 檢查 LINE Bot 憑證...${NC}"
if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_actual_channel_access_token_here" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo -e "${RED}❌ LINE_CHANNEL_ACCESS_TOKEN 未設置${NC}"
else
    echo -e "${GREEN}✅ LINE_CHANNEL_ACCESS_TOKEN 已設置${NC}"
fi

if [ "$LINE_CHANNEL_SECRET" = "your_actual_channel_secret_here" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo -e "${RED}❌ LINE_CHANNEL_SECRET 未設置${NC}"
else
    echo -e "${GREEN}✅ LINE_CHANNEL_SECRET 已設置${NC}"
fi

# 檢查 Gemini API 憑證
echo -e "${BLUE}🔍 檢查 Gemini API 憑證...${NC}"
if [ "$AISTUDIO_API_KEY" = "your_actual_gemini_api_key_here" ] || [ -z "$AISTUDIO_API_KEY" ]; then
    echo -e "${RED}❌ AISTUDIO_API_KEY 未設置${NC}"
else
    echo -e "${GREEN}✅ AISTUDIO_API_KEY 已設置${NC}"
fi

echo ""
echo -e "${YELLOW}📋 憑證設置指南：${NC}"
echo "1. LINE Bot 憑證："
echo "   - 登入 https://developers.line.biz"
echo "   - 創建 Provider 和 Channel"
echo "   - 複製 Channel Access Token 和 Channel Secret"
echo ""
echo "2. Gemini API 憑證："
echo "   - 登入 https://aistudio.google.com"
echo "   - 創建 API 金鑰"
echo "   - 複製 API 金鑰"
echo ""
echo "3. 編輯 .env 檔案："
echo "   - 將實際憑證填入對應欄位"
echo "   - 保存檔案"
echo ""
echo -e "${GREEN}✅ 憑證驗證完成${NC}" 