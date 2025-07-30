#!/bin/bash

# ========================================
# 憑證驗證和修復腳本
# ========================================

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔐 憑證驗證和修復腳本${NC}"
echo "=================================================="

# 檢查 .env 檔案
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env 檔案不存在${NC}"
    echo "正在創建 .env 檔案..."
    
    cat > .env << 'EOF'
# ========================================
# LINE Bot 失智症分析系統 - 環境變數配置
# ========================================

# ========================================
# LINE Bot 憑證配置
# ========================================
# 請從 LINE Developer Console 獲取以下憑證：
# 1. 登入 https://developers.line.biz/
# 2. 選擇您的 Channel
# 3. 在 Messaging API 設定中複製憑證

# LINE Channel Access Token (必須設置)
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here

# LINE Channel Secret (必須設置)
LINE_CHANNEL_SECRET=your_channel_secret_here

# ========================================
# API 配置
# ========================================
# RAG API 端點配置
FLEX_API_URL=http://localhost:8005/comprehensive-analysis
RAG_HEALTH_URL=http://localhost:8005/health
RAG_ANALYZE_URL=http://localhost:8005/comprehensive-analysis

# ========================================
# 生產環境配置
# ========================================
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG_MODE=false

# ========================================
# Redis 快取配置
# ========================================
# Redis 連接配置
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# ========================================
# Gemini API 配置
# ========================================
# 請從 Google AI Studio 獲取 API 金鑰：
# 1. 登入 https://aistudio.google.com/
# 2. 創建新的 API 金鑰
# 3. 複製金鑰到下方

# Gemini API 金鑰 (必須設置)
AISTUDIO_API_KEY=your_gemini_api_key_here

# Gemini 模型配置
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# ========================================
# 監控配置
# ========================================
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true

# ========================================
# Webhook 配置
# ========================================
# 生產環境 webhook URL (部署後更新)
WEBHOOK_URL=https://your-domain.com/webhook

# ========================================
# 安全配置
# ========================================
# 請設置強密碼用於生產環境
ADMIN_PASSWORD=your_admin_password_here

# ========================================
# 效能配置
# ========================================
# 快取 TTL 設置 (秒)
CACHE_TTL_ANALYSIS=1800
CACHE_TTL_FLEX_MESSAGE=3600
CACHE_TTL_USER_SESSION=7200

# API 速率限制
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_REQUESTS_PER_HOUR=1000

# ========================================
# 開發環境配置 (可選)
# ========================================
# 開發模式設置
DEV_MODE=false
DEV_LOG_LEVEL=DEBUG

# 測試配置
TEST_MODE=false
TEST_API_KEY=test_key_here

# ========================================
# 備註說明
# ========================================
# 1. 請將所有 "your_xxx_here" 替換為實際的憑證
# 2. 生產環境請使用強密碼
# 3. 定期更新 API 金鑰
# 4. 監控 API 使用量以避免超額費用
EOF

    echo -e "${GREEN}✅ .env 檔案已創建${NC}"
    echo -e "${YELLOW}⚠️  請編輯 .env 檔案填入實際的憑證${NC}"
    echo ""
    echo "�� 需要設置的憑證："
    echo "   1. LINE_CHANNEL_ACCESS_TOKEN"
    echo "   2. LINE_CHANNEL_SECRET"
    echo "   3. AISTUDIO_API_KEY"
    echo ""
    echo "�� 獲取憑證的網址："
    echo "   LINE Bot: https://developers.line.biz/"
    echo "   Gemini API: https://aistudio.google.com/"
    echo ""
    exit 1
fi

# 載入環境變數
source .env

echo -e "${BLUE}�� 檢查憑證設置狀態...${NC}"
echo ""

# 檢查 LINE Bot 憑證
echo -e "${BLUE}🔍 檢查 LINE Bot 憑證...${NC}"

if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_channel_access_token_here" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo -e "${RED}❌ LINE_CHANNEL_ACCESS_TOKEN 未設置或仍為預設值${NC}"
    LINE_TOKEN_STATUS=false
else
    echo -e "${GREEN}✅ LINE_CHANNEL_ACCESS_TOKEN 已設置${NC}"
    LINE_TOKEN_STATUS=true
fi

if [ "$LINE_CHANNEL_SECRET" = "your_channel_secret_here" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo -e "${RED}❌ LINE_CHANNEL_SECRET 未設置或仍為預設值${NC}"
    LINE_SECRET_STATUS=false
else
    echo -e "${GREEN}✅ LINE_CHANNEL_SECRET 已設置${NC}"
    LINE_SECRET_STATUS=true
fi

# 檢查 Gemini API 憑證
echo ""
echo -e "${BLUE}🔍 檢查 Gemini API 憑證...${NC}"

if [ "$AISTUDIO_API_KEY" = "your_gemini_api_key_here" ] || [ -z "$AISTUDIO_API_KEY" ]; then
    echo -e "${RED}❌ AISTUDIO_API_KEY 未設置或仍為預設值${NC}"
    GEMINI_STATUS=false
else
    echo -e "${GREEN}✅ AISTUDIO_API_KEY 已設置${NC}"
    GEMINI_STATUS=true
fi

# 顯示 .env 檔案內容（隱藏敏感資訊）
echo ""
echo -e "${BLUE}�� .env 檔案內容檢查...${NC}"
echo "=================================================="

# 顯示非敏感配置
grep -E "^(ENVIRONMENT|LOG_LEVEL|DEBUG_MODE|REDIS_URL|GEMINI_MODEL|ENABLE_)" .env | while read line; do
    echo "   $line"
done

# 顯示憑證狀態（隱藏實際值）
echo ""
echo -e "${YELLOW}🔐 憑證狀態（隱藏實際值）：${NC}"
if [ "$LINE_TOKEN_STATUS" = true ]; then
    echo "   LINE_CHANNEL_ACCESS_TOKEN=***已設置***"
else
    echo "   LINE_CHANNEL_ACCESS_TOKEN=❌ 未設置"
fi

if [ "$LINE_SECRET_STATUS" = true ]; then
    echo "   LINE_CHANNEL_SECRET=***已設置***"
else
    echo "   LINE_CHANNEL_SECRET=❌ 未設置"
fi

if [ "$GEMINI_STATUS" = true ]; then
    echo "   AISTUDIO_API_KEY=***已設置***"
else
    echo "   AISTUDIO_API_KEY=❌ 未設置"
fi

# 提供修正指南
echo ""
echo -e "${BLUE}🔧 修正指南${NC}"
echo "=================================================="

if [ "$LINE_TOKEN_STATUS" = false ] || [ "$LINE_SECRET_STATUS" = false ] || [ "$GEMINI_STATUS" = false ]; then
    echo -e "${YELLOW}⚠️  發現憑證問題，請按照以下步驟修正：${NC}"
    echo ""
    echo "1. 📝 編輯 .env 檔案："
    echo "   nano .env"
    echo "   或"
    echo "   code .env"
    echo ""
    echo "2. �� 替換以下佔位符："
    echo "   your_channel_access_token_here → 您的 LINE Channel Access Token"
    echo "   your_channel_secret_here → 您的 LINE Channel Secret"
    echo "   your_gemini_api_key_here → 您的 Gemini API 金鑰"
    echo ""
    echo "3. �� 儲存檔案"
    echo ""
    echo "4. 🔄 重新執行此腳本驗證"
    echo ""
    echo "�� 獲取憑證的網址："
    echo "   LINE Bot: https://developers.line.biz/"
    echo "   Gemini API: https://aistudio.google.com/"
    echo ""
    echo "�� 範例 .env 檔案內容："
    echo "   LINE_CHANNEL_ACCESS_TOKEN=U1234567890abcdef1234567890abcdef"
    echo "   LINE_CHANNEL_SECRET=abcdef1234567890abcdef1234567890ab"
    echo "   AISTUDIO_API_KEY=AIzaSyC1234567890abcdef1234567890abcdef"
else
    echo -e "${GREEN}🎉 所有憑證已正確設置！${NC}"
    echo ""
    echo "✅ 可以執行以下命令啟動系統："
    echo "   ./start_optimized_system.sh"
    echo "   ./start_production.sh"
    echo ""
    echo "�� 測試憑證有效性："
    echo "   python3 test_line_bot_connection.py"
fi

echo ""
echo -e "${BLUE}📊 總結${NC}"
echo "=================================================="
echo "LINE Bot 憑證: $([ "$LINE_TOKEN_STATUS" = true ] && [ "$LINE_SECRET_STATUS" = true ] && echo "✅ 完整" || echo "❌ 不完整")"
echo "Gemini API 憑證: $([ "$GEMINI_STATUS" = true ] && echo "✅ 完整" || echo "❌ 不完整")"

if [ "$LINE_TOKEN_STATUS" = true ] && [ "$LINE_SECRET_STATUS" = true ] && [ "$GEMINI_STATUS" = true ]; then
    echo ""
    echo -e "${GREEN}🎯 所有憑證已設置完成！${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ 請先完成憑證設置${NC}"
    exit 1
fi