#!/bin/bash

# 自動化系統修復腳本
# 解決常見的系統問題

set -e  # 遇到錯誤時退出

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查是否為 root 用戶
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "以 root 用戶運行可能不安全"
    fi
}

# 創建必要的目錄
create_directories() {
    log_info "創建必要的目錄..."
    
    directories=(
        "logs"
        "temp"
        "backup"
        "data"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_success "創建目錄: $dir"
        else
            log_info "目錄已存在: $dir"
        fi
    done
}

# 檢查和殺死佔用端口的進程
kill_port_processes() {
    local ports=(8000 5000 3000)
    
    log_info "檢查端口佔用情況..."
    
    for port in "${ports[@]}"; do
        local pid=$(lsof -ti:$port 2>/dev/null || true)
        
        if [ ! -z "$pid" ]; then
            log_warning "端口 $port 被進程 $pid 佔用"
            
            # 嘗試優雅終止
            log_info "嘗試優雅終止進程 $pid..."
            kill -TERM "$pid" 2>/dev/null || true
            sleep 3
            
            # 檢查進程是否還在運行
            if kill -0 "$pid" 2>/dev/null; then
                log_warning "優雅終止失敗，強制終止進程 $pid"
                kill -KILL "$pid" 2>/dev/null || true
            fi
            
            log_success "端口 $port 已釋放"
        else
            log_info "端口 $port 可用"
        fi
    done
}

# 清理舊的日誌文件
cleanup_logs() {
    log_info "清理舊的日誌文件..."
    
    # 刪除7天前的日誌文件
    find logs/ -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
    
    # 清理大於10MB的日誌文件
    find logs/ -name "*.log" -type f -size +10M -exec truncate -s 0 {} \; 2>/dev/null || true
    
    log_success "日誌清理完成"
}

# 檢查並修復虛擬環境
fix_virtual_environment() {
    log_info "檢查虛擬環境..."
    
    if [ -d "venv" ]; then
        log_info "發現虛擬環境"
        
        # 激活虛擬環境
        source venv/bin/activate 2>/dev/null || {
            log_warning "虛擬環境激活失敗，嘗試重建..."
            rm -rf venv
            python3 -m venv venv
            source venv/bin/activate
            log_success "虛擬環境重建完成"
        }
        
        # 檢查 pip
        if ! command -v pip &> /dev/null; then
            log_warning "pip 不可用，嘗試修復..."
            python -m ensurepip --upgrade
        fi
        
        # 升級關鍵包
        log_info "升級關鍵包..."
        pip install --upgrade pip setuptools wheel
        
        # 檢查 requirements.txt
        if [ -f "requirements.txt" ]; then
            log_info "安裝依賴..."
            pip install -r requirements.txt
        fi
        
        log_success "虛擬環境檢查完成"
    else
        log_warning "未發現虛擬環境，創建新的..."
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
        
        log_success "虛擬環境創建完成"
    fi
}

# 檢查 Python 進程
check_python_processes() {
    log_info "檢查 Python 進程..."
    
    local python_processes=$(ps aux | grep python | grep -v grep | wc -l)
    log_info "發現 $python_processes 個 Python 進程"
    
    # 檢查是否有殭屍進程 (macOS 兼容)
    local zombie_processes=$(ps aux | awk '{print $8}' | grep -c Z 2>/dev/null || echo "0")
    if [ "$zombie_processes" -gt 0 ] 2>/dev/null; then
        log_warning "發現 $zombie_processes 個殭屍進程"
        # 嘗試清理殭屍進程
        pkill -f "python.*line_bot" 2>/dev/null || true
        sleep 2
    fi
}

# 檢查系統資源
check_system_resources() {
    log_info "檢查系統資源..."
    
    # 檢查內存使用 (macOS 兼容)
    if command -v vm_stat &> /dev/null; then
        # macOS 內存檢查
        local memory_info=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
        local total_memory=$(sysctl -n hw.memsize 2>/dev/null || echo "8589934592")
        local free_memory=$((memory_info * 4096))
        local used_memory=$((total_memory - free_memory))
        local memory_usage=$(echo "scale=1; $used_memory * 100 / $total_memory" | bc 2>/dev/null || echo "0")
        log_info "內存使用率: ${memory_usage}%"
        
        if (( $(echo "$memory_usage > 80" | bc -l 2>/dev/null || echo "0") )); then
            log_warning "內存使用率過高: ${memory_usage}%"
        fi
    else
        # Linux 內存檢查
        local memory_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}' 2>/dev/null || echo "0")
        log_info "內存使用率: ${memory_usage}%"
        
        if (( $(echo "$memory_usage > 80" | bc -l 2>/dev/null || echo "0") )); then
            log_warning "內存使用率過高: ${memory_usage}%"
            # 清理緩存 (僅 Linux)
            sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || true
        fi
    fi
    
    # 檢查磁盤空間
    local disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//' 2>/dev/null || echo "0")
    log_info "磁盤使用率: ${disk_usage}%"
    
    if [ "$disk_usage" -gt 90 ]; then
        log_warning "磁盤空間不足: ${disk_usage}%"
        # 清理臨時文件
        rm -rf /tmp/* 2>/dev/null || true
        rm -rf temp/* 2>/dev/null || true
    fi
}

# 修復文件權限
fix_file_permissions() {
    log_info "修復文件權限..."
    
    # 修復腳本執行權限
    find . -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true
    
    # 修復 Python 文件權限
    find . -name "*.py" -type f -exec chmod 644 {} \; 2>/dev/null || true
    
    # 修復目錄權限
    find . -type d -exec chmod 755 {} \; 2>/dev/null || true
    
    # 修復日誌目錄權限
    chmod -R 755 logs/ 2>/dev/null || true
    
    log_success "文件權限修復完成"
}

# 驗證系統狀態
validate_system() {
    log_info "驗證系統狀態..."
    
    local errors=0
    
    # 檢查關鍵目錄
    if [ ! -d "logs" ]; then
        log_error "logs 目錄不存在"
        ((errors++))
    fi
    
    # 檢查 Python 環境
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 不可用"
        ((errors++))
    fi
    
    # 檢查虛擬環境
    if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
        log_error "虛擬環境損壞"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        log_success "系統狀態驗證通過"
        return 0
    else
        log_error "發現 $errors 個問題"
        return 1
    fi
}

# 生成修復報告
generate_repair_report() {
    local report_file="logs/repair_report_$(date +%Y%m%d_%H%M%S).txt"
    
    log_info "生成修復報告: $report_file"
    
    cat > "$report_file" << EOF
系統修復報告
==============
修復時間: $(date)
修復腳本版本: 1.0

修復項目:
- 創建必要目錄
- 清理端口佔用
- 清理舊日誌文件
- 修復虛擬環境
- 檢查系統資源
- 修復文件權限

系統狀態:
- Python 版本: $(python3 --version 2>/dev/null || echo "未安裝")
- 磁盤使用: $(df / | tail -1 | awk '{print $5}')
- 內存使用: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')
- 運行進程: $(ps aux | grep python | grep -v grep | wc -l) 個 Python 進程

修復結果: $([ $? -eq 0 ] && echo "成功" || echo "部分失敗")
EOF

    log_success "修復報告已生成: $report_file"
}

# 主修復流程
main_repair() {
    log_info "開始系統自動修復..."
    echo "=================================="
    
    check_root
    create_directories
    kill_port_processes
    cleanup_logs
    fix_virtual_environment
    check_python_processes
    check_system_resources
    fix_file_permissions
    
    if validate_system; then
        log_success "系統修復完成！"
        generate_repair_report
        return 0
    else
        log_error "系統修復部分失敗，請檢查報告"
        generate_repair_report
        return 1
    fi
}

# 快速修復模式
quick_repair() {
    log_info "執行快速修復..."
    
    kill_port_processes
    create_directories
    cleanup_logs
    
    log_success "快速修復完成"
}

# 深度修復模式
deep_repair() {
    log_info "執行深度修復..."
    
    main_repair
    
    # 額外的深度修復步驟
    log_info "執行深度清理..."
    
    # 清理 Python 緩存
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # 重建虛擬環境
    if [ -d "venv" ]; then
        log_info "重建虛擬環境..."
        rm -rf venv
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
        fi
    fi
    
    log_success "深度修復完成"
}

# 顯示幫助信息
show_help() {
    cat << EOF
系統自動修復腳本

用法: $0 [選項]

選項:
    --quick     執行快速修復（端口清理、目錄創建、日誌清理）
    --deep      執行深度修復（包含虛擬環境重建）
    --check     僅檢查系統狀態，不執行修復
    --help      顯示此幫助信息

示例:
    $0                  # 執行標準修復
    $0 --quick          # 快速修復
    $0 --deep           # 深度修復
    $0 --check          # 檢查系統狀態
EOF
}

# 僅檢查模式
check_only() {
    log_info "檢查系統狀態..."
    
    check_python_processes
    check_system_resources
    validate_system
    
    log_info "系統檢查完成"
}

# 參數處理
case "${1:-}" in
    --quick)
        quick_repair
        ;;
    --deep)
        deep_repair
        ;;
    --check)
        check_only
        ;;
    --help|-h)
        show_help
        ;;
    "")
        main_repair
        ;;
    *)
        log_error "未知參數: $1"
        show_help
        exit 1
        ;;
esac

exit $? 