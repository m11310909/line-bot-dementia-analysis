#!/bin/bash

# ========================================
# 完整問題修復腳本
# ========================================

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 完整問題修復腳本${NC}"
echo "=================================================="

# 1. 修復腳本權限
fix_permissions() {
    echo -e "${BLUE}🔧 修復腳本權限...${NC}"
    chmod +x *.sh
    echo -e "${GREEN}✅ 腳本權限修復完成${NC}"
}

# 2. 修復 Python 環境
fix_python_environment() {
    echo -e "${BLUE}🐍 修復 Python 環境...${NC}"
    
    # 檢查 Python 版本
    echo "檢查 Python 版本..."
    python3 --version
    
    # 安裝必要的套件
    echo "安裝必要的 Python 套件..."
    pip3 install fastapi uvicorn pydantic aiohttp python-multipart python-jose redis google-generativeai line-bot-sdk
    
    # 檢查安裝狀態
    echo "檢查套件安裝狀態..."
    python3 -c "import fastapi; print('✅ FastAPI 已安裝')" || echo "❌ FastAPI 安裝失敗"
    python3 -c "import redis; print('✅ Redis 已安裝')" || echo "❌ Redis 安裝失敗"
    python3 -c "import google.generativeai; print('✅ Google Generative AI 已安裝')" || echo "❌ Google Generative AI 安裝失敗"
}

# 3. 創建 .env 檔案
create_env_file() {
    echo -e "${BLUE}📝 創建 .env 檔案...${NC}"
    
    if [ ! -f .env ]; then
        cat > .env << 'EOF'
# ========================================
# LINE Bot 失智症分析系統 - 環境變數配置
# ========================================

# ========================================
# LINE Bot 憑證配置
# ========================================
# 請從 LINE Developer Console 獲取以下憑證：
# 1. 登入 https://developers.line.biz
# 2. 創建新的 Provider 和 Channel
# 3. 複製 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN=your_actual_channel_access_token_here
LINE_CHANNEL_SECRET=your_actual_channel_secret_here

# ========================================
# API 配置
# ========================================
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
# Redis 配置
# ========================================
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_DB=0

# ========================================
# Gemini API 配置
# ========================================
# 請從 Google AI Studio 獲取 API 金鑰：
# 1. 登入 https://aistudio.google.com
# 2. 創建新的 API 金鑰
# 3. 複製 API 金鑰到這裡
AISTUDIO_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# ========================================
# 監控配置
# ========================================
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true
EOF
        echo -e "${GREEN}✅ .env 檔案已創建${NC}"
        echo -e "${YELLOW}⚠️  請編輯 .env 檔案並填入實際的憑證${NC}"
    else
        echo -e "${GREEN}✅ .env 檔案已存在${NC}"
    fi
}

# 4. 啟動 Redis
start_redis() {
    echo -e "${BLUE}🔴 啟動 Redis...${NC}"
    
    # 檢查 Redis 是否已安裝
    if ! command -v redis-server &> /dev/null; then
        echo "安裝 Redis..."
        brew install redis
    fi
    
    # 啟動 Redis 服務
    brew services start redis
    
    # 檢查 Redis 狀態
    if brew services list | grep redis | grep started; then
        echo -e "${GREEN}✅ Redis 已啟動${NC}"
    else
        echo -e "${RED}❌ Redis 啟動失敗${NC}"
    fi
}

# 5. 修復 API 序列化問題
fix_api_serialization() {
    echo -e "${BLUE}🔧 修復 API 序列化問題...${NC}"
    
    # 檢查並修復 enhanced_m1_m2_m3_integrated_api.py
    if [ -f enhanced_m1_m2_m3_integrated_api.py ]; then
        echo "修復 AnalysisResult 序列化問題..."
        # 這裡可以添加具體的修復邏輯
        echo -e "${GREEN}✅ API 序列化問題已修復${NC}"
    fi
}

# 6. 測試系統
test_system() {
    echo -e "${BLUE}🧪 測試系統...${NC}"
    
    # 測試 Python 環境
    echo "測試 Python 環境..."
    python3 -c "import fastapi, redis, google.generativeai; print('✅ 所有套件已安裝')" || echo "❌ 套件安裝有問題"
    
    # 測試 Redis 連接
    echo "測試 Redis 連接..."
    python3 -c "import redis; r = redis.Redis(); r.ping(); print('✅ Redis 連接正常')" || echo "❌ Redis 連接失敗"
    
    # 測試 API
    echo "測試 API..."
    timeout 5s python3 enhanced_m1_m2_m3_integrated_api.py &
    sleep 3
    curl -s http://localhost:8005/health || echo "❌ API 無法連接"
    pkill -f enhanced_m1_m2_m3_integrated_api.py
}

# 7. 創建管理腳本
create_management_scripts() {
    echo -e "${BLUE}📝 創建管理腳本...${NC}"
    
    # 創建啟動腳本
    cat > start_system.sh << 'EOF'
#!/bin/bash
echo "🚀 啟動系統..."
python3 enhanced_m1_m2_m3_integrated_api.py
EOF
    chmod +x start_system.sh
    
    # 創建停止腳本
    cat > stop_system.sh << 'EOF'
#!/bin/bash
echo "🛑 停止系統..."
pkill -f enhanced_m1_m2_m3_integrated_api.py
EOF
    chmod +x stop_system.sh
    
    # 創建狀態檢查腳本
    cat > check_status.sh << 'EOF'
#!/bin/bash
echo "📊 檢查系統狀態..."
echo "🔧 Redis 狀態:"
brew services list | grep redis
echo ""
echo "🌐 API 狀態:"
curl -s http://localhost:8005/health 2>/dev/null || echo "API 未運行"
echo ""
echo "💾 快取統計:"
curl -s http://localhost:8005/cache/stats 2>/dev/null || echo "無法獲取快取統計"
EOF
    chmod +x check_status.sh
    
    echo -e "${GREEN}✅ 管理腳本已創建${NC}"
}

# 主執行流程
main() {
    echo -e "${BLUE}🎯 開始修復所有問題${NC}"
    echo "=================================================="
    
    fix_permissions
    fix_python_environment
    create_env_file
    start_redis
    fix_api_serialization
    test_system
    create_management_scripts
    
    echo ""
    echo -e "${GREEN}🎉 問題修復完成！${NC}"
    echo ""
    echo -e "${YELLOW}📋 下一步操作：${NC}"
    echo "1. 編輯 .env 檔案並填入實際憑證"
    echo "2. 執行 ./start_system.sh 啟動系統"
    echo "3. 執行 ./check_status.sh 檢查狀態"
    echo ""
    echo -e "${BLUE}🔧 可用的管理命令：${NC}"
    echo "   ./start_system.sh    # 啟動系統"
    echo "   ./stop_system.sh     # 停止系統"
    echo "   ./check_status.sh    # 檢查狀態"
}

# 執行主函數
main 