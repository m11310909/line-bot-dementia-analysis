#!/bin/bash

# LINE Bot 生產環境配置腳本
# 設置 LINE Bot 憑證和生產環境配置

echo "🚀 LINE Bot 生產環境配置"
echo "=================================================="

# 檢查必要工具
check_requirements() {
    echo "🔍 檢查必要工具..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安裝"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        echo "❌ curl 未安裝"
        exit 1
    fi
    
    echo "✅ 必要工具檢查完成"
}

# 設置環境變數
setup_environment() {
    echo "🔧 設置環境變數..."
    
    # 創建 .env 檔案
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

    echo "✅ 環境變數檔案已創建 (.env)"
    echo "⚠️  請編輯 .env 檔案填入實際的憑證"
}

# 驗證憑證
validate_credentials() {
    echo "🔐 驗證 LINE Bot 憑證..."
    
    if [ -f .env ]; then
        source .env
        
        if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_channel_access_token_here" ]; then
            echo "❌ 請設置 LINE_CHANNEL_ACCESS_TOKEN"
            return 1
        fi
        
        if [ "$LINE_CHANNEL_SECRET" = "your_channel_secret_here" ]; then
            echo "❌ 請設置 LINE_CHANNEL_SECRET"
            return 1
        fi
        
        echo "✅ 憑證格式正確"
        return 0
    else
        echo "❌ .env 檔案不存在"
        return 1
    fi
}

# 測試 LINE Bot 連接
test_line_bot_connection() {
    echo "🧪 測試 LINE Bot 連接..."
    
    if validate_credentials; then
        source .env
        
        # 測試 Channel Access Token
        response=$(curl -s -H "Authorization: Bearer $LINE_CHANNEL_ACCESS_TOKEN" \
            "https://api.line.me/v2/bot/profile/U1234567890abcdef" 2>/dev/null)
        
        if echo "$response" | grep -q "error"; then
            echo "❌ Channel Access Token 無效"
            return 1
        else
            echo "✅ Channel Access Token 有效"
        fi
        
        echo "✅ LINE Bot 連接測試通過"
        return 0
    else
        echo "❌ 憑證驗證失敗"
        return 1
    fi
}

# 設置 webhook URL
setup_webhook() {
    echo "🔗 設置 webhook URL..."
    
    if validate_credentials; then
        source .env
        
        # 獲取公開 URL（這裡需要根據實際部署環境調整）
        PUBLIC_URL="https://your-domain.com"
        WEBHOOK_URL="$PUBLIC_URL/webhook"
        
        echo "📋 Webhook URL: $WEBHOOK_URL"
        echo "⚠️  請在 LINE Developer Console 設置 webhook URL"
        echo "🔗 設置步驟："
        echo "   1. 登入 LINE Developer Console"
        echo "   2. 選擇您的 Channel"
        echo "   3. 在 Messaging API 設定中"
        echo "   4. 設置 Webhook URL: $WEBHOOK_URL"
        echo "   5. 啟用 Use webhook"
        
        return 0
    else
        echo "❌ 無法設置 webhook，憑證無效"
        return 1
    fi
}

# 創建生產環境配置檔案
create_production_config() {
    echo "📁 創建生產環境配置..."
    
    # 創建 production_config.py
    cat > production_config.py << 'EOF'
"""
生產環境配置檔案
"""

import os
from typing import Optional

class ProductionConfig:
    """生產環境配置類別"""
    
    # LINE Bot 配置
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
    LINE_CHANNEL_SECRET: str = os.getenv('LINE_CHANNEL_SECRET', '')
    
    # API 配置
    FLEX_API_URL: str = os.getenv('FLEX_API_URL', 'http://localhost:8005/comprehensive-analysis')
    RAG_HEALTH_URL: str = os.getenv('RAG_HEALTH_URL', 'http://localhost:8005/health')
    RAG_ANALYZE_URL: str = os.getenv('RAG_ANALYZE_URL', 'http://localhost:8005/comprehensive-analysis')
    
    # 環境配置
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'production')
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Redis 配置
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379')
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD')
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # Gemini API 配置
    AISTUDIO_API_KEY: str = os.getenv('AISTUDIO_API_KEY', '')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    GEMINI_MAX_TOKENS: int = int(os.getenv('GEMINI_MAX_TOKENS', '1000'))
    
    # 監控配置
    ENABLE_MONITORING: bool = os.getenv('ENABLE_MONITORING', 'true').lower() == 'true'
    ENABLE_LOGGING: bool = os.getenv('ENABLE_LOGGING', 'true').lower() == 'true'
    ENABLE_METRICS: bool = os.getenv('ENABLE_METRICS', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """驗證配置是否完整"""
        required_fields = [
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_CHANNEL_SECRET',
            'AISTUDIO_API_KEY'
        ]
        
        for field in required_fields:
            if not getattr(cls, field):
                print(f"❌ 缺少必要配置: {field}")
                return False
        
        return True
    
    @classmethod
    def get_webhook_url(cls) -> str:
        """獲取 webhook URL"""
        # 這裡需要根據實際部署環境調整
        return "https://your-domain.com/webhook"

# 全域配置實例
config = ProductionConfig()
EOF

    echo "✅ 生產環境配置檔案已創建 (production_config.py)"
}

# 創建啟動腳本
create_startup_script() {
    echo "🚀 創建啟動腳本..."
    
    cat > start_production.sh << 'EOF'
#!/bin/bash

# 生產環境啟動腳本

echo "🚀 啟動 LINE Bot 生產環境服務..."

# 載入環境變數
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# 檢查必要配置
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "❌ 缺少 LINE Bot 憑證"
    echo "請設置 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_CHANNEL_SECRET"
    exit 1
fi

if [ -z "$AISTUDIO_API_KEY" ]; then
    echo "❌ 缺少 Gemini API 金鑰"
    echo "請設置 AISTUDIO_API_KEY"
    exit 1
fi

# 啟動 RAG API
echo "🔧 啟動 RAG API..."
python3 m1_m2_m3_integrated_api.py &
RAG_PID=$!

# 等待 RAG API 啟動
sleep 5

# 檢查 RAG API 健康狀態
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ RAG API 啟動成功"
else
    echo "❌ RAG API 啟動失敗"
    exit 1
fi

# 啟動 LINE Bot Webhook
echo "🤖 啟動 LINE Bot Webhook..."
python3 updated_line_bot_webhook.py &
WEBHOOK_PID=$!

echo "✅ 生產環境服務啟動完成"
echo "📊 服務狀態："
echo "   RAG API: http://localhost:8005"
echo "   Webhook: 運行中"
echo "   PID: RAG($RAG_PID), Webhook($WEBHOOK_PID)"

# 等待中斷信號
trap "echo '🛑 停止服務...'; kill $RAG_PID $WEBHOOK_PID; exit" INT TERM
wait
EOF

    chmod +x start_production.sh
    echo "✅ 啟動腳本已創建 (start_production.sh)"
}

# 主執行流程
main() {
    echo "🎯 開始 LINE Bot 生產環境配置"
    echo "=================================================="
    
    check_requirements
    setup_environment
    create_production_config
    create_startup_script
    
    echo ""
    echo "📋 配置完成！下一步："
    echo "1. 編輯 .env 檔案填入實際憑證"
    echo "2. 在 LINE Developer Console 設置 webhook URL"
    echo "3. 執行 ./start_production.sh 啟動服務"
    echo ""
    echo "🔧 配置檔案："
    echo "   - .env: 環境變數配置"
    echo "   - production_config.py: 生產環境配置"
    echo "   - start_production.sh: 啟動腳本"
    echo ""
    echo "✅ LINE Bot 生產環境配置完成！"
}

# 執行主流程
main "$@"
