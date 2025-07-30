#!/bin/bash

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}📊 系統狀態檢查${NC}"
echo "=================================================="

# 檢查 Python 環境
echo -e "${BLUE}🐍 檢查 Python 環境...${NC}"
python3 --version
python3 -c "import fastapi; print('✅ FastAPI 已安裝')" || echo "❌ FastAPI 未安裝"
python3 -c "import redis; print('✅ Redis 已安裝')" || echo "❌ Redis 未安裝"
python3 -c "import google.generativeai; print('✅ Google Generative AI 已安裝')" || echo "❌ Google Generative AI 未安裝"

echo ""

# 檢查 Redis 狀態
echo -e "${BLUE}🔴 檢查 Redis 狀態...${NC}"
if brew services list | grep redis | grep started > /dev/null; then
    echo -e "${GREEN}✅ Redis 正在運行${NC}"
else
    echo -e "${RED}❌ Redis 未運行${NC}"
    echo "啟動 Redis..."
    brew services start redis
fi

echo ""

# 檢查 API 狀態
echo -e "${BLUE}🌐 檢查 API 狀態...${NC}"
if curl -s http://localhost:8005/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API 正在運行${NC}"
    echo "API 回應："
    curl -s http://localhost:8005/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8005/health
else
    echo -e "${RED}❌ API 未運行${NC}"
    echo "啟動 API..."
    python3 enhanced_m1_m2_m3_integrated_api.py &
    sleep 3
    if curl -s http://localhost:8005/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API 啟動成功${NC}"
    else
        echo -e "${RED}❌ API 啟動失敗${NC}"
    fi
fi

echo ""

# 檢查 .env 檔案
echo -e "${BLUE}📝 檢查 .env 檔案...${NC}"
if [ -f .env ]; then
    echo -e "${GREEN}✅ .env 檔案存在${NC}"
    source .env
    if [ "$LINE_CHANNEL_ACCESS_TOKEN" != "your_actual_channel_access_token_here" ] && [ -n "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
        echo -e "${GREEN}✅ LINE Bot 憑證已設置${NC}"
    else
        echo -e "${RED}❌ LINE Bot 憑證未設置${NC}"
    fi
    if [ "$AISTUDIO_API_KEY" != "your_actual_gemini_api_key_here" ] && [ -n "$AISTUDIO_API_KEY" ]; then
        echo -e "${GREEN}✅ Gemini API 憑證已設置${NC}"
    else
        echo -e "${RED}❌ Gemini API 憑證未設置${NC}"
    fi
else
    echo -e "${RED}❌ .env 檔案不存在${NC}"
fi

echo ""
echo -e "${GREEN}✅ 系統狀態檢查完成${NC}" 