#!/bin/bash
# ============================================================================
# LINE Bot ngrok 隧道自動設置腳本 (增強版)
# 支持多服務端口和自動 webhook 更新
# ============================================================================

# === 配置區 ===
WEBHOOK_SERVICE_PORT=3000  # LINE Bot webhook 服務端口 (修正為 3000)
API_SERVICE_PORT=8000      # API 服務端口
NGROK_LOG="ngrok.log"
NGROK_URL_FILE="ngrok_url.txt"
ENV_FILE=".env"
WEBHOOK_PATH="/webhook"   # LINE Bot webhook 路徑 (修正為 /webhook)

# ngrok API 端口範圍
NGROK_API_PORTS=(4040 4041 4042 4043 4044)

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# === 函數定義 ===
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 檢查必要工具
check_dependencies() {
    log_info "檢查必要工具..."
    
    if ! command -v ngrok &> /dev/null; then
        log_error "ngrok 未安裝。請先安裝 ngrok: https://ngrok.com/download"
        exit 1
    fi
    
    if ! command -v curl &> /dev/null; then
        log_error "curl 未安裝。請安裝 curl"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log_warning "jq 未安裝，將使用 grep 解析 JSON (建議安裝 jq 獲得更好的支持)"
    fi
    
    log_success "工具檢查完成"
}

# 讀取環境變數
load_env() {
    log_info "讀取環境變數..."
    
    if [ ! -f "$ENV_FILE" ]; then
        log_warning ".env 文件不存在，創建默認配置"
        cat > "$ENV_FILE" << EOF
# LINE Bot 配置
LINE_CHANNEL_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=YOUR_CHANNEL_SECRET
WEBHOOK_URL=
EOF
    fi
    
    # 讀取 LINE Channel Access Token
    LINE_CHANNEL_TOKEN=$(grep 'LINE_CHANNEL_ACCESS_TOKEN=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    
    if [ -z "$LINE_CHANNEL_TOKEN" ] || [ "$LINE_CHANNEL_TOKEN" = "YOUR_CHANNEL_ACCESS_TOKEN" ]; then
        log_error "LINE_CHANNEL_ACCESS_TOKEN 未設置"
        log_info "請在 $ENV_FILE 中設置正確的 LINE_CHANNEL_ACCESS_TOKEN"
        exit 1
    fi
    
    log_success "環境變數讀取完成"
}

# 停止舊的 ngrok 進程
stop_old_ngrok() {
    log_info "終止舊的 ngrok 進程..."
    
    # 嘗試優雅關閉
    pkill -TERM ngrok
    sleep 2
    
    # 強制終止剩餘進程
    pkill -KILL ngrok 2>/dev/null
    
    # 清理舊的日誌文件
    rm -f "$NGROK_LOG"
    
    log_success "舊進程清理完成"
}

# 檢查服務狀態
check_services() {
    log_info "檢查本地服務狀態..."
    
    local services_running=true
    
    # 檢查 webhook 服務
    if curl -s "http://localhost:$WEBHOOK_SERVICE_PORT/health" > /dev/null; then
        log_success "Webhook 服務 (端口 $WEBHOOK_SERVICE_PORT) 正常運行"
    else
        log_warning "Webhook 服務 (端口 $WEBHOOK_SERVICE_PORT) 未運行"
        services_running=false
    fi
    
    # 檢查 API 服務
    if curl -s "http://localhost:$API_SERVICE_PORT/health" > /dev/null; then
        log_success "API 服務 (端口 $API_SERVICE_PORT) 正常運行"
    else
        log_warning "API 服務 (端口 $API_SERVICE_PORT) 未運行"
        services_running=false
    fi
    
    if [ "$services_running" = false ]; then
        log_warning "部分服務未運行，建議先執行 ./start_services.sh"
        read -p "是否繼續設置 ngrok? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 啟動 ngrok
start_ngrok() {
    log_info "啟動 ngrok 隧道 (端口 $WEBHOOK_SERVICE_PORT)..."
    
    # 使用背景進程啟動 ngrok
    nohup ngrok http $WEBHOOK_SERVICE_PORT --log=stdout > "$NGROK_LOG" 2>&1 &
    local ngrok_pid=$!
    
    log_info "ngrok 進程 ID: $ngrok_pid"
    log_info "等待 ngrok 初始化..."
    
    # 等待 ngrok 啟動
    local max_attempts=20
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        sleep 1
        if grep -q "started tunnel" "$NGROK_LOG" 2>/dev/null; then
            log_success "ngrok 隧道已建立"
            return 0
        fi
        
        if grep -q "failed to start tunnel" "$NGROK_LOG" 2>/dev/null; then
            log_error "ngrok 啟動失敗"
            cat "$NGROK_LOG"
            return 1
        fi
        
        ((attempt++))
        echo -n "."
    done
    
    echo
    log_error "ngrok 啟動超時"
    return 1
}

# 獲取 ngrok public URL
get_ngrok_url() {
    log_info "獲取 ngrok public URL..."
    
    local ngrok_url=""
    
    # 嘗試不同的 API 端口
    for port in "${NGROK_API_PORTS[@]}"; do
        log_info "嘗試端口 $port..."
        
        if command -v jq &> /dev/null; then
            # 使用 jq 解析 JSON
            ngrok_url=$(curl -s "http://localhost:$port/api/tunnels" 2>/dev/null | \
                       jq -r '.tunnels[] | select(.config.addr | contains("'$WEBHOOK_SERVICE_PORT'")) | .public_url' 2>/dev/null | \
                       grep "https://" | head -n 1)
        else
            # 使用 grep 解析 JSON
            ngrok_url=$(curl -s "http://localhost:$port/api/tunnels" 2>/dev/null | \
                       grep -Eo 'https://[a-z0-9-]+\.ngrok-free\.app' | head -n 1)
        fi
        
        if [ -n "$ngrok_url" ]; then
            log_success "從端口 $port 獲取到 URL: $ngrok_url"
            break
        fi
    done
    
    if [ -z "$ngrok_url" ]; then
        log_error "無法獲取 ngrok public URL"
        log_info "請檢查 ngrok 日誌:"
        cat "$NGROK_LOG"
        return 1
    fi
    
    echo "$ngrok_url"
}

# 保存 URL 到文件
save_url() {
    local url=$1
    
    log_info "保存 URL 到文件..."
    
    echo "$url" > "$NGROK_URL_FILE"
    log_success "已保存到 $NGROK_URL_FILE"
    
    # 更新 .env 文件
    if grep -q "^WEBHOOK_URL=" "$ENV_FILE"; then
        # macOS 和 Linux 兼容的 sed 命令
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s|^WEBHOOK_URL=.*|WEBHOOK_URL=$url|" "$ENV_FILE"
        else
            sed -i "s|^WEBHOOK_URL=.*|WEBHOOK_URL=$url|" "$ENV_FILE"
        fi
    else
        echo "WEBHOOK_URL=$url" >> "$ENV_FILE"
    fi
    
    log_success "已更新 $ENV_FILE 中的 WEBHOOK_URL"
}

# 更新 LINE Bot webhook
update_line_webhook() {
    local base_url=$1
    local full_webhook_url="${base_url}${WEBHOOK_PATH}"
    
    log_info "更新 LINE Bot webhook URL..."
    log_info "目標 URL: $full_webhook_url"
    
    # 更新 webhook endpoint
    local response=$(curl -s -X PUT "https://api.line.me/v2/bot/channel/webhook/endpoint" \
        -H "Authorization: Bearer $LINE_CHANNEL_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"endpoint\":\"$full_webhook_url\"}" \
        -w "HTTP_STATUS:%{http_code}")
    
    local http_status=$(echo "$response" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
    local body=$(echo "$response" | sed 's/HTTP_STATUS:[0-9]*$//')
    
    if [ "$http_status" = "200" ]; then
        log_success "LINE webhook 更新成功"
        
        # 啟用 webhook
        log_info "啟用 webhook..."
        local enable_response=$(curl -s -X PUT "https://api.line.me/v2/bot/channel/webhook/test" \
            -H "Authorization: Bearer $LINE_CHANNEL_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"endpoint\":\"$full_webhook_url\"}" \
            -w "HTTP_STATUS:%{http_code}")
        
        local enable_status=$(echo "$enable_response" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
        
        if [ "$enable_status" = "200" ]; then
            log_success "Webhook 測試成功"
        else
            log_warning "Webhook 測試失敗 (狀態碼: $enable_status)"
        fi
        
    else
        log_error "LINE webhook 更新失敗 (狀態碼: $http_status)"
        log_error "響應: $body"
        return 1
    fi
}

# 顯示結果摘要
show_summary() {
    local ngrok_url=$1
    
    echo
    echo "============================================"
    echo "🎉 ngrok 設置完成！"
    echo "============================================"
    echo
    echo "📡 ngrok 資訊:"
    echo "  • Public URL: $ngrok_url"
    echo "  • Local Port: $WEBHOOK_SERVICE_PORT"
    echo "  • Webhook Path: $WEBHOOK_PATH"
    echo "  • Full Webhook URL: ${ngrok_url}${WEBHOOK_PATH}"
    echo
    echo "📁 文件更新:"
    echo "  • URL 已保存到: $NGROK_URL_FILE"
    echo "  • 環境變數已更新: $ENV_FILE"
    echo
    echo "🔧 管理命令:"
    echo "  • 查看 ngrok 狀態: curl http://localhost:4040/api/tunnels"
    echo "  • 查看 ngrok 日誌: tail -f $NGROK_LOG"
    echo "  • 停止 ngrok: pkill ngrok"
    echo
    echo "🧪 測試命令:"
    echo "  • 測試 webhook: curl -X POST ${ngrok_url}${WEBHOOK_PATH}"
    echo "  • 檢查服務狀態: ./status.sh"
    echo
}

# 主要執行流程
main() {
    echo "============================================"
    echo "🚀 LINE Bot ngrok 隧道設置"
    echo "============================================"
    echo
    
    # 執行各個步驟
    check_dependencies
    load_env
    check_services
    stop_old_ngrok
    
    if ! start_ngrok; then
        exit 1
    fi
    
    local ngrok_url
    if ! ngrok_url=$(get_ngrok_url); then
        exit 1
    fi
    
    save_url "$ngrok_url"
    
    if ! update_line_webhook "$ngrok_url"; then
        log_warning "LINE webhook 更新失敗，但 ngrok 隧道已建立"
        log_info "您可以手動在 LINE Developers Console 中更新 webhook URL:"
        log_info "${ngrok_url}${WEBHOOK_PATH}"
    fi
    
    show_summary "$ngrok_url"
}

# 執行主函數
main "$@" 