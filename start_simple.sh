#!/bin/bash

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 啟動系統${NC}"
echo "=================================================="

# 檢查 Python 環境
echo -e "${BLUE}🐍 檢查 Python 環境...${NC}"
python3 -c "import fastapi, redis, google.generativeai; print('✅ 所有套件已安裝')" || {
    echo -e "${RED}❌ 缺少必要套件，正在安裝...${NC}"
    pip3 install fastapi uvicorn pydantic aiohttp python-multipart python-jose redis google-generativeai line-bot-sdk
}

# 啟動 Redis
echo -e "${BLUE}🔴 啟動 Redis...${NC}"
brew services start redis
sleep 2

# 檢查 Redis 狀態
if brew services list | grep redis | grep started > /dev/null; then
    echo -e "${GREEN}✅ Redis 已啟動${NC}"
else
    echo -e "${RED}❌ Redis 啟動失敗${NC}"
    exit 1
fi

# 檢查 .env 檔案
echo -e "${BLUE}📝 檢查 .env 檔案...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env 檔案不存在${NC}"
    echo "請先執行 ./verify_credentials_simple.sh 創建 .env 檔案"
    exit 1
fi

# 啟動 API
echo -e "${BLUE}🌐 啟動 API...${NC}"
python3 enhanced_m1_m2_m3_integrated_api.py 