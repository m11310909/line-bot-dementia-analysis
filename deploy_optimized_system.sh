#!/bin/bash

# 優化系統部署腳本
# 整合 Redis 快取和優化 Gemini API

echo "🚀 優化系統部署腳本"
echo "=================================================="

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查必要工具
check_requirements() {
    echo -e "${BLUE}🔍 檢查必要工具...${NC}"
    
    # 檢查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安裝${NC}"
        exit 1
    fi
    
    # 檢查 pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 未安裝${NC}"
        exit 1
    fi
    
    # 檢查 curl
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}❌ curl 未安裝${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 必要工具檢查完成${NC}"
}

# 安裝依賴
install_dependencies() {
    echo -e "${BLUE}📦 安裝 Python 依賴...${NC}"
    
    # 安裝基本依賴
    pip3 install fastapi uvicorn pydantic aiohttp python-multipart python-jose redis google-generativeai
    
    # 檢查安裝結果
    python3 -c "import fastapi, redis, google.generativeai; print('✅ 依賴安裝成功')" 2>/dev/null || {
        echo -e "${RED}❌ 依賴安裝失敗${NC}"
        exit 1
    }
    
    echo -e "${GREEN}✅ 依賴安裝完成${NC}"
}

# 設置 Redis
setup_redis() {
    echo -e "${BLUE}🔧 設置 Redis...${NC}"
    
    # 檢查 Redis 是否已安裝
    if ! command -v redis-server &> /dev/null; then
        echo -e "${YELLOW}📦 安裝 Redis...${NC}"
        brew install redis
    fi
    
    # 啟動 Redis 服務
    if ! brew services list | grep redis | grep started &> /dev/null; then
        echo -e "${YELLOW}🚀 啟動 Redis 服務...${NC}"
        brew services start redis
        sleep 3
    fi
    
    # 測試 Redis 連接
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✅ Redis 服務正常運行${NC}"
    else
        echo -e "${RED}❌ Redis 服務啟動失敗${NC}"
        exit 1
    fi
}

# 設置環境變數
setup_environment() {
    echo -e "${BLUE}🔧 設置環境變數...${NC}"
    
    # 創建 .env 檔案
    if [ ! -f .env ]; then
        cat > .env << EOF
# LINE Bot 憑證配置
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

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
AISTUDIO_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=1000

# 監控配置
ENABLE_MONITORING=true
ENABLE_LOGGING=true
ENABLE_METRICS=true
EOF
        echo -e "${GREEN}✅ 環境變數檔案已創建 (.env)${NC}"
        echo -e "${YELLOW}⚠️  請編輯 .env 檔案填入實際的憑證${NC}"
    else
        echo -e "${GREEN}✅ 環境變數檔案已存在${NC}"
    fi
}

# 測試系統組件
test_components() {
    echo -e "${BLUE}🧪 測試系統組件...${NC}"
    
    # 測試 Redis 快取
    echo -e "${YELLOW}📊 測試 Redis 快取...${NC}"
    python3 redis_cache_manager.py
    
    # 測試優化 Gemini 客戶端
    echo -e "${YELLOW}🤖 測試優化 Gemini 客戶端...${NC}"
    python3 optimized_gemini_client.py
    
    echo -e "${GREEN}✅ 組件測試完成${NC}"
}

# 啟動優化 API
start_optimized_api() {
    echo -e "${BLUE}🚀 啟動優化 API...${NC}"
    
    # 檢查是否有其他 API 在運行
    if pgrep -f "enhanced_m1_m2_m3_integrated_api.py" > /dev/null; then
        echo -e "${YELLOW}🛑 停止現有 API...${NC}"
        pkill -f "enhanced_m1_m2_m3_integrated_api.py"
        sleep 2
    fi
    
    # 啟動優化 API
    echo -e "${YELLOW}🔧 啟動增強版 API...${NC}"
    python3 enhanced_m1_m2_m3_integrated_api.py &
    API_PID=$!
    
    # 等待 API 啟動
    echo -e "${YELLOW}⏳ 等待 API 啟動...${NC}"
    sleep 10
    
    # 測試 API 健康狀態
    if curl -s http://localhost:8005/health > /dev/null; then
        echo -e "${GREEN}✅ 優化 API 啟動成功${NC}"
        echo -e "${BLUE}📊 API 狀態:${NC}"
        curl -s http://localhost:8005/health | python3 -m json.tool
    else
        echo -e "${RED}❌ API 啟動失敗${NC}"
        exit 1
    fi
}

# 測試 API 功能
test_api_functionality() {
    echo -e "${BLUE}🧪 測試 API 功能...${NC}"
    
    # 測試基本分析
    echo -e "${YELLOW}📝 測試基本分析...${NC}"
    curl -X POST "http://localhost:8005/comprehensive-analysis" \
        -H "Content-Type: application/json" \
        -d '{"user_input": "我媽媽最近常常忘記事情"}' \
        -s | python3 -m json.tool
    
    # 測試快取功能
    echo -e "${YELLOW}💾 測試快取功能...${NC}"
    curl -X POST "http://localhost:8005/comprehensive-analysis" \
        -H "Content-Type: application/json" \
        -d '{"user_input": "我媽媽最近常常忘記事情"}' \
        -s | python3 -c "import sys, json; data=json.load(sys.stdin); print('✅ 快取命中' if data.get('cached') else '❌ 快取未命中')"
    
    # 檢查快取統計
    echo -e "${YELLOW}📊 檢查快取統計...${NC}"
    curl -s http://localhost:8005/cache/stats | python3 -m json.tool
    
    echo -e "${GREEN}✅ API 功能測試完成${NC}"
}

# 顯示系統狀態
show_system_status() {
    echo -e "${BLUE}📊 系統狀態...${NC}"
    
    echo -e "${YELLOW}🔧 服務狀態:${NC}"
    echo "  - Redis: $(brew services list | grep redis | awk '{print $2}')"
    echo "  - API: $(curl -s http://localhost:8005/health | python3 -c "import sys, json; data=json.load(sys.stdin); print('運行中' if data.get('status') == 'healthy' else '停止')" 2>/dev/null || echo '停止')"
    
    echo -e "${YELLOW}📈 效能指標:${NC}"
    if curl -s http://localhost:8005/cache/stats > /dev/null; then
        CACHE_STATS=$(curl -s http://localhost:8005/cache/stats)
        echo "  - 快取命中率: $(echo $CACHE_STATS | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'{data.get(\"hit_rate\", 0)}/{data.get(\"hit_rate\", 0) + data.get(\"miss_rate\", 0)}')" 2>/dev/null || echo 'N/A')"
        echo "  - 記憶體使用: $(echo $CACHE_STATS | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('memory_usage', 'N/A'))" 2>/dev/null || echo 'N/A')"
    fi
    
    echo -e "${YELLOW}🔗 API 端點:${NC}"
    echo "  - 健康檢查: http://localhost:8005/health"
    echo "  - 綜合分析: http://localhost:8005/comprehensive-analysis"
    echo "  - 快取統計: http://localhost:8005/cache/stats"
    echo "  - Gemini 統計: http://localhost:8005/gemini/stats"
}

# 創建管理腳本
create_management_scripts() {
    echo -e "${BLUE}📁 創建管理腳本...${NC}"
    
    # 啟動腳本
    cat > start_optimized_system.sh << 'EOF'
#!/bin/bash
echo "🚀 啟動優化系統..."
python3 enhanced_m1_m2_m3_integrated_api.py
EOF
    chmod +x start_optimized_system.sh
    
    # 停止腳本
    cat > stop_optimized_system.sh << 'EOF'
#!/bin/bash
echo "🛑 停止優化系統..."
pkill -f "enhanced_m1_m2_m3_integrated_api.py"
echo "✅ 系統已停止"
EOF
    chmod +x stop_optimized_system.sh
    
    # 重啟腳本
    cat > restart_optimized_system.sh << 'EOF'
#!/bin/bash
echo "🔄 重啟優化系統..."
./stop_optimized_system.sh
sleep 2
./start_optimized_system.sh
EOF
    chmod +x restart_optimized_system.sh
    
    # 狀態檢查腳本
    cat > check_system_status.sh << 'EOF'
#!/bin/bash
echo "📊 系統狀態檢查..."
echo "🔧 Redis 狀態:"
brew services list | grep redis
echo ""
echo "🌐 API 狀態:"
curl -s http://localhost:8005/health | python3 -m json.tool 2>/dev/null || echo "API 未運行"
echo ""
echo "💾 快取統計:"
curl -s http://localhost:8005/cache/stats | python3 -m json.tool 2>/dev/null || echo "無法獲取快取統計"
EOF
    chmod +x check_system_status.sh
    
    echo -e "${GREEN}✅ 管理腳本已創建${NC}"
}

# 主執行流程
main() {
    echo -e "${BLUE}🎯 開始優化系統部署${NC}"
    echo "=================================================="
    
    check_requirements
    install_dependencies
    setup_redis
    setup_environment
    test_components
    start_optimized_api
    test_api_functionality
    create_management_scripts
    show_system_status
    
    echo ""
    echo -e "${GREEN}🎉 優化系統部署完成！${NC}"
    echo ""
    echo -e "${YELLOW}📋 下一步：${NC}"
    echo "1. 編輯 .env 檔案填入實際憑證"
    echo "2. 使用 ./start_optimized_system.sh 啟動系統"
    echo "3. 使用 ./check_system_status.sh 檢查狀態"
    echo "4. 使用 ./stop_optimized_system.sh 停止系統"
    echo ""
    echo -e "${BLUE}🔧 管理腳本：${NC}"
    echo "  - start_optimized_system.sh: 啟動系統"
    echo "  - stop_optimized_system.sh: 停止系統"
    echo "  - restart_optimized_system.sh: 重啟系統"
    echo "  - check_system_status.sh: 檢查狀態"
    echo ""
    echo -e "${GREEN}✅ 優化系統已準備就緒！${NC}"
}

# 執行主流程
main "$@" 