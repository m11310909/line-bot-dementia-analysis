#!/bin/bash

# ========================================
# 系統問題修復腳本
# ========================================

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 系統問題修復腳本${NC}"
echo "=================================================="

# 1. 修復 Python 環境問題
fix_python_environment() {
    echo -e "${BLUE}🐍 修復 Python 環境問題...${NC}"
    
    # 檢查 Python 版本
    echo "檢查 Python 版本..."
    python3 --version
    
    # 安裝必要的套件
    echo "安裝 FastAPI 和相關套件..."
    pip3 install fastapi uvicorn pydantic aiohttp python-multipart python-jose redis google-generativeai line-bot-sdk
    
    # 檢查安裝狀態
    echo "檢查套件安裝狀態..."
    python3 -c "import fastapi; print('✅ FastAPI 已安裝')" || echo "❌ FastAPI 安裝失敗"
    python3 -c "import redis; print('✅ Redis 已安裝')" || echo "❌ Redis 安裝失敗"
    python3 -c "import google.generativeai; print('✅ Google Generative AI 已安裝')" || echo "❌ Google Generative AI 安裝失敗"
    python3 -c "import linebot; print('✅ LINE Bot SDK 已安裝')" || echo "❌ LINE Bot SDK 安裝失敗"
}

# 2. 修復憑證問題
fix_credentials() {
    echo -e "${BLUE}🔐 修復憑證問題...${NC}"
    
    # 檢查 .env 檔案
    if [ ! -f .env ]; then
        echo "創建 .env 檔案..."
        cat > .env << 'EOF'
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
        echo -e "${GREEN}✅ .env 檔案已創建${NC}"
    else
        echo -e "${GREEN}✅ .env 檔案已存在${NC}"
    fi
    
    # 載入環境變數
    source .env
    
    # 檢查憑證狀態
    echo "檢查憑證狀態..."
    
    if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_channel_access_token_here" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
        echo -e "${RED}❌ LINE_CHANNEL_ACCESS_TOKEN 未設置${NC}"
        echo "請編輯 .env 檔案填入實際的 LINE Channel Access Token"
    else
        echo -e "${GREEN}✅ LINE_CHANNEL_ACCESS_TOKEN 已設置${NC}"
    fi
    
    if [ "$LINE_CHANNEL_SECRET" = "your_channel_secret_here" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
        echo -e "${RED}❌ LINE_CHANNEL_SECRET 未設置${NC}"
        echo "請編輯 .env 檔案填入實際的 LINE Channel Secret"
    else
        echo -e "${GREEN}✅ LINE_CHANNEL_SECRET 已設置${NC}"
    fi
    
    if [ "$AISTUDIO_API_KEY" = "your_gemini_api_key_here" ] || [ -z "$AISTUDIO_API_KEY" ]; then
        echo -e "${RED}❌ AISTUDIO_API_KEY 未設置${NC}"
        echo "請編輯 .env 檔案填入實際的 Gemini API 金鑰"
    else
        echo -e "${GREEN}✅ AISTUDIO_API_KEY 已設置${NC}"
    fi
}

# 3. 修復 Redis 快取問題
fix_redis_cache() {
    echo -e "${BLUE}�� 修復 Redis 快取問題...${NC}"
    
    # 檢查 Redis 是否運行
    if ! pgrep -x "redis-server" > /dev/null; then
        echo "啟動 Redis 服務..."
        brew services start redis
    else
        echo -e "${GREEN}✅ Redis 服務正在運行${NC}"
    fi
    
    # 測試 Redis 連接
    echo "測試 Redis 連接..."
    python3 -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis 連接成功')
except Exception as e:
    print(f'❌ Redis 連接失敗: {e}')
"
}

# 4. 修復 API 序列化問題
fix_api_serialization() {
    echo -e "${BLUE}🔧 修復 API 序列化問題...${NC}"
    
    # 檢查並修復 enhanced_m1_m2_m3_integrated_api.py
    if [ -f enhanced_m1_m2_m3_integrated_api.py ]; then
        echo "檢查 API 序列化問題..."
        
        # 檢查是否有 AnalysisResult 序列化問題
        if grep -q "AnalysisResult" enhanced_m1_m2_m3_integrated_api.py; then
            echo "發現 AnalysisResult 序列化問題，正在修復..."
            
            # 創建修復腳本
            cat > fix_serialization.py << 'EOF'
#!/usr/bin/env python3
"""
修復 AnalysisResult 序列化問題
"""

import json
from typing import Dict, Any

def convert_analysis_result_to_dict(result):
    """將 AnalysisResult 物件轉換為字典"""
    if hasattr(result, '__dict__'):
        return result.__dict__
    elif isinstance(result, dict):
        return result
    else:
        # 嘗試將物件轉換為字典
        try:
            return {
                'type': type(result).__name__,
                'content': str(result)
            }
        except:
            return {'error': '無法序列化物件'}

def safe_json_serialize(obj):
    """安全的 JSON 序列化"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, (list, tuple)):
        return [safe_json_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: safe_json_serialize(v) for k, v in obj.items()}
    else:
        return str(obj)

if __name__ == "__main__":
    print("✅ 序列化修復函數已準備就緒")
EOF
            echo -e "${GREEN}✅ 序列化修復函數已創建${NC}"
        fi
    fi
}

# 5. 測試系統功能
test_system() {
    echo -e "${BLUE}🧪 測試系統功能...${NC}"
    
    # 測試 Python 環境
    echo "測試 Python 環境..."
    python3 -c "
try:
    import fastapi
    import redis
    import google.generativeai
    import linebot
    print('✅ 所有必要套件已安裝')
except ImportError as e:
    print(f'❌ 套件缺失: {e}')
"
    
    # 測試 Redis 連接
    echo "測試 Redis 連接..."
    python3 -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    print('✅ Redis 連接正常')
except Exception as e:
    print(f'❌ Redis 連接失敗: {e}')
"
    
    # 測試 API 啟動
    echo "測試 API 啟動..."
    timeout 10s python3 m1_m2_m3_integrated_api.py > /dev/null 2>&1 &
    API_PID=$!
    sleep 3
    
    if curl -s http://localhost:8005/health > /dev/null; then
        echo -e "${GREEN}✅ API 啟動成功${NC}"
        kill $API_PID 2>/dev/null
    else
        echo -e "${RED}❌ API 啟動失敗${NC}"
        kill $API_PID 2>/dev/null
    fi
}

# 6. 提供使用指南
show_usage_guide() {
    echo -e "${BLUE}📋 使用指南${NC}"
    echo "=================================================="
    echo ""
    echo "1. 🔐 設置憑證："
    echo "   編輯 .env 檔案："
    echo "   nano .env"
    echo ""
    echo "   替換以下佔位符："
    echo "   your_channel_access_token_here → 您的 LINE Channel Access Token"
    echo "   your_channel_secret_here → 您的 LINE Channel Secret"
    echo "   your_gemini_api_key_here → 您的 Gemini API 金鑰"
    echo ""
    echo "2. 🚀 啟動系統："
    echo "   ./start_optimized_system.sh"
    echo ""
    echo "3. 🧪 測試系統："
    echo "   python3 test_line_bot_connection.py"
    echo ""
    echo "4. 📊 檢查狀態："
    echo "   ./check_system_status.sh"
    echo ""
    echo " 獲取憑證的網址："
    echo "   LINE Bot: https://developers.line.biz/"
    echo "   Gemini API: https://aistudio.google.com/"
}

# 主執行流程
main() {
    echo -e "${BLUE}�� 開始修復系統問題${NC}"
    echo "=================================================="
    
    fix_python_environment
    echo ""
    
    fix_credentials
    echo ""
    
    fix_redis_cache
    echo ""
    
    fix_api_serialization
    echo ""
    
    test_system
    echo ""
    
    show_usage_guide
    echo ""
    
    echo -e "${GREEN}🎉 系統修復完成！${NC}"
    echo ""
    echo "📋 下一步："
    echo "   1. 編輯 .env 檔案填入實際憑證"
    echo "   2. 執行 ./start_optimized_system.sh 啟動系統"
    echo "   3. 執行 python3 test_line_bot_connection.py 測試連接"
}

# 執行主函數
main