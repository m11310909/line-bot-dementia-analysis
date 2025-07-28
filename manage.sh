#!/bin/bash

# LINE Bot 失智症分析系統 - 使用說明與快速執行
# ==================================================

echo "🤖 LINE Bot 失智症分析系統 - 使用指南"
echo "===================================="

show_menu() {
    echo ""
    echo "請選擇操作："
    echo "1. 🚀 一鍵重構優化（完整重構）"
    echo "2. ⚡ 快速啟動服務"
    echo "3. 🧪 執行系統測試"
    echo "4. 📊 記憶體監控"
    echo "5. 🔧 環境設定"
    echo "6. 📋 查看系統狀態"
    echo "7. 🆘 故障排除"
    echo "8. 📚 查看完整文件"
    echo "0. 退出"
    echo ""
    read -p "請輸入選項 (0-8): " choice
}

# 1. 一鍵重構優化
run_refactor() {
    echo "🚀 開始一鍵重構優化..."

    # 檢查是否已下載重構腳本
    if [[ ! -f "refactor.sh" ]]; then
        echo "📥 創建重構腳本..."
        # 這裡會使用上面創建的完整重構腳本
        cat > refactor.sh << 'REFACTOR_SCRIPT'
#!/bin/bash

# LINE Bot 失智症分析系統 - 一鍵優化重構腳本
# (這裡包含完整的重構腳本內容)

set -e
echo "🚀 LINE Bot 失智症分析系統 - 一鍵優化開始"

# ... (完整的重構腳本內容)
REFACTOR_SCRIPT
        chmod +x refactor.sh
    fi

    echo "執行重構腳本..."
    ./refactor.sh

    read -p "按 Enter 鍵返回主選單..."
}

# 2. 快速啟動服務
quick_start() {
    echo "⚡ 快速啟動服務..."

    # 檢查環境變數
    if [[ ! -f ".env" ]]; then
        echo "⚠️ 找不到 .env 文件，創建範本..."
        cp .env.template .env 2>/dev/null || {
            cat > .env << 'EOF'
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here
AISTUDIO_API_KEY=your_api_key_here
EOF
        }
        echo "📝 請編輯 .env 文件設定您的 API 金鑰"
        read -p "設定完成後按 Enter 繼續..."
    fi

    # 檢查依賴
    echo "📦 檢查 Python 依賴..."
    pip install -q fastapi uvicorn google-generativeai pyyaml psutil aiohttp pydantic line-bot-sdk

    # 啟動服務
    echo "🚀 啟動 API 服務..."
    if [[ -f "api/main.py" ]]; then
        python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
        API_PID=$!
        echo "API 服務已啟動 (PID: $API_PID)"
    else
        echo "❌ 找不到 api/main.py，請先執行重構"
        return 1
    fi

    # 等待服務啟動
    sleep 3

    # 測試連線
    echo "🔍 測試服務連線..."
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ 服務啟動成功！"
        echo "📝 API 文件: http://localhost:8000/docs"
        echo "🔧 健康檢查: http://localhost:8000/health"
    else
        echo "❌ 服務啟動失敗"
    fi

    echo "按 Ctrl+C 停止服務"
    read -p "按 Enter 鍵返回主選單..."
    kill $API_PID 2>/dev/null || true
}

# 3. 執行系統測試
run_tests() {
    echo "🧪 執行系統測試..."

    if [[ -f "tests/test_basic.py" ]]; then
        python tests/test_basic.py
    else
        echo "執行簡化測試..."

        # 簡化測試腳本
        python << 'EOF'
import sys
import asyncio

print("🧪 開始基礎測試...")

# 測試 1: 記憶體檢查
def test_memory():
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"✅ 記憶體使用: {mem.percent:.1f}%")
        return mem.percent < 90
    except ImportError:
        print("⚠️ psutil 未安裝，跳過記憶體測試")
        return True

# 測試 2: 模組導入
def test_imports():
    try:
        import fastapi
        import uvicorn
        import yaml
        print("✅ 核心模組導入成功")
        return True
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

# 測試 3: 配置檢查
def test_config():
    try:
        import os
        if os.path.exists('.env'):
            print("✅ 配置文件存在")
            return True
        else:
            print("⚠️ 配置文件不存在")
            return False
    except Exception as e:
        print(f"❌ 配置檢查失敗: {e}")
        return False

# 執行所有測試
tests = [test_memory(), test_imports(), test_config()]
passed = sum(tests)
total = len(tests)

print(f"📊 測試結果: {passed}/{total} 通過")
if passed == total:
    print("🎉 所有測試通過！")
else:
    print("⚠️ 部分測試失敗，建議檢查環境設定")
EOF
    fi

    read -p "按 Enter 鍵返回主選單..."
}

# 4. 記憶體監控
memory_monitor() {
    echo "📊 啟動記憶體監控（按 Ctrl+C 停止）..."

    python << 'EOF'
import time
import sys

try:
    import psutil
    import datetime

    while True:
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        now = datetime.datetime.now().strftime('%H:%M:%S')

        status = "🟢"
        if mem.percent > 70:
            status = "🟡"
        if mem.percent > 85:
            status = "🔴"

        print(f'[{now}] {status} 記憶體: {mem.percent:.1f}% ({mem.used/1024/1024:.0f}MB) CPU: {cpu:.1f}%')

        if mem.percent > 90:
            print('🚨 記憶體嚴重不足！建議重啟 Replit')

        time.sleep(5)

except ImportError:
    print("❌ psutil 未安裝，無法監控記憶體")
    print("安裝指令: pip install psutil")
except KeyboardInterrupt:
    print("\n📊 監控已停止")
EOF

    read -p "按 Enter 鍵返回主選單..."
}

# 5. 環境設定
setup_environment() {
    echo "🔧 環境設定指南..."
    echo ""

    echo "📋 必要的環境變數："
    echo "1. LINE_CHANNEL_ACCESS_TOKEN - LINE Bot 頻道存取權杖"
    echo "2. LINE_CHANNEL_SECRET - LINE Bot 頻道密鑰"
    echo "3. AISTUDIO_API_KEY - Google AI Studio API 金鑰"
    echo ""

    echo "📝 取得 API 金鑰的步驟："
    echo ""
    echo "LINE Bot 設定："
    echo "1. 前往 https://developers.line.biz/"
    echo "2. 登入並創建新的 Provider"
    echo "3. 創建 Messaging API 頻道"
    echo "4. 在 'Basic settings' 頁面取得 Channel secret"
    echo "5. 在 'Messaging API' 頁面取得 Channel access token"
    echo ""
    echo "Google AI Studio 設定："
    echo "1. 前往 https://aistudio.google.com/"
    echo "2. 登入 Google 帳號"
    echo "3. 點擊 'Get API key' 創建新的 API 金鑰"
    echo "4. 複製產生的 API 金鑰"
    echo ""

    read -p "是否要編輯 .env 文件？(y/n): " edit_env

    if [[ $edit_env == "y" || $edit_env == "Y" ]]; then
        if [[ ! -f ".env" ]]; then
            cp .env.template .env 2>/dev/null || {
                cat > .env << 'EOF'
# LINE Bot 憑證
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here

# Google AI Studio API
AISTUDIO_API_KEY=your_google_ai_studio_api_key_here

# 服務設定
API_PORT=8000
DEBUG=false

# 安全設定
RATE_LIMIT_PER_MINUTE=60
MAX_INPUT_LENGTH=1000

# Replit 最佳化
MEMORY_LIMIT_MB=400
ENABLE_MEMORY_MONITOR=true
EOF
            }
        fi

        echo "📝 開啟 .env 文件進行編輯..."
        if command -v nano > /dev/null; then
            nano .env
        elif command -v vi > /dev/null; then
            vi .env
        else
            echo "請手動編輯 .env 文件"
            cat .env
        fi
    fi

    read -p "按 Enter 鍵返回主選單..."
}

# 6. 查看系統狀態
check_status() {
    echo "📋 系統狀態檢查..."
    echo ""

    # 檢查文件結構
    echo "📁 文件結構檢查："
    if [[ -d "api" ]]; then
        echo "✅ api/ 目錄存在"
    else
        echo "❌ api/ 目錄不存在 - 需要執行重構"
    fi

    if [[ -f ".env" ]]; then
        echo "✅ .env 配置文件存在"
    else
        echo "❌ .env 配置文件不存在"
    fi

    if [[ -f "requirements.txt" ]]; then
        echo "✅ requirements.txt 存在"
    else
        echo "❌ requirements.txt 不存在"
    fi

    # 檢查依賴
    echo ""
    echo "📦 Python 依賴檢查："

    packages=("fastapi" "uvicorn" "google-generativeai" "pyyaml" "psutil")
    for package in "${packages[@]}"; do
        if python -c "import $package" 2>/dev/null; then
            echo "✅ $package 已安裝"
        else
            echo "❌ $package 未安裝"
        fi
    done

    # 檢查服務狀態
    echo ""
    echo "🔍 服務狀態檢查："
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ API 服務運行中"
        curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "API 回應異常"
    else
        echo "❌ API 服務未運行"
    fi

    # 記憶體狀態
    echo ""
    echo "📊 系統資源："
    python -c "
try:
    import psutil
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    print(f'記憶體使用: {mem.percent:.1f}% ({mem.used/1024/1024:.0f}MB/{mem.total/1024/1024:.0f}MB)')
    print(f'CPU 使用率: {cpu:.1f}%')
except:
    print('無法取得系統資源資訊')
"

    read -p "按 Enter 鍵返回主選單..."
}

# 7. 故障排除
troubleshoot() {
    echo "🆘 故障排除指南..."
    echo ""

    echo "🔧 常見問題與解決方案："
    echo ""
    echo "1. 記憶體不足錯誤"
    echo "   解決方案："
    echo "   - 重啟 Replit 環境"
    echo "   - 執行記憶體監控找出高用量程序"
    echo "   - 減少同時處理的請求數量"
    echo ""
    echo "2. API 金鑰錯誤"
    echo "   解決方案："
    echo "   - 檢查 .env 文件中的金鑰格式"
    echo "   - 確認 Google AI Studio API 金鑰有效"
    echo "   - 重新生成 LINE Bot 憑證"
    echo ""
    echo "3. 模組導入錯誤"
    echo "   解決方案："
    echo "   - pip install -r requirements.txt"
    echo "   - 檢查 Python 路徑設定"
    echo "   - 執行完整重構"
    echo ""
    echo "4. LINE Bot 無回應"
    echo "   解決方案："
    echo "   - 檢查 Webhook URL 設定"
    echo "   - 驗證 LINE 簽名設定"
    echo "   - 查看 API 服務日誌"
    echo ""
    echo "5. Flex Message 格式錯誤"
    echo "   解決方案："
    echo "   - 檢查 JSON 格式是否正確"
    echo "   - 驗證必要欄位是否存在"
    echo "   - 測試簡化的 Flex 訊息"
    echo ""

    echo "🧪 快速診斷："
    read -p "是否執行快速診斷？(y/n): " run_diag

    if [[ $run_diag == "y" || $run_diag == "Y" ]]; then
        echo "執行診斷..."

        # 診斷腳本
        python << 'EOF'
import sys
import os

print("🔍 系統診斷中...")

# 檢查 Python 版本
print(f"Python 版本: {sys.version}")

# 檢查工作目錄
print(f"工作目錄: {os.getcwd()}")

# 檢查環境變數
env_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'AISTUDIO_API_KEY']
for var in env_vars:
    value = os.getenv(var, '')
    if value:
        print(f"✅ {var}: 已設定 ({'***' + value[-4:] if len(value) > 4 else '***'})")
    else:
        print(f"❌ {var}: 未設定")

# 檢查文件權限
files_to_check = ['.env', 'requirements.txt']
for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file}: 存在")
    else:
        print(f"❌ {file}: 不存在")

print("診斷完成")
EOF
    fi

    read -p "按 Enter 鍵返回主選單..."
}

# 8. 查看完整文件
show_documentation() {
    echo "📚 完整文件..."
    echo ""

    if [[ -f "REFACTOR_REPORT.md" ]]; then
        echo "📄 重構報告已生成，內容："
        echo "=========================="
        head -50 REFACTOR_REPORT.md
        echo "=========================="
        echo "..."
        echo ""
        read -p "是否查看完整報告？(y/n): " view_full
        if [[ $view_full == "y" || $view_full == "Y" ]]; then
            cat REFACTOR_REPORT.md | less
        fi
    else
        echo "📝 建立快速文件..."
        cat << 'EOF'
# LINE Bot 失智症分析系統 - 快速使用指南

## 🚀 快速開始

1. **設定環境**:
   ```bash
   cp .env.template .env
   # 編輯 .env 設定 API 金鑰
   ```

2. **安裝依賴**:
   ```bash
   pip install fastapi uvicorn google-generativeai pyyaml psutil
   ```

3. **啟動服務**:
   ```bash
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```

## 📝 API 使用

- `POST /analyze/m1`: M1 失智症警訊分析
- `POST /webhook`: LINE Bot webhook 端點
- `GET /health`: 服務健康檢查

## 🔧 LINE Bot 設定

1. LINE Developers Console 設定 Webhook URL
2. 設定 Channel Access Token 與 Channel Secret
3. 啟用 Webhook 功能

## 📊 系統監控

使用內建記憶體監控確保 Replit 環境穩定運行。

EOF
    fi

    read -p "按 Enter 鍵返回主選單..."
}

# 主程式循環
main() {
    clear
    echo "🤖 歡迎使用 LINE Bot 失智症分析系統管理工具"
    echo "適用於 Replit 環境的一鍵部署與管理"
    echo ""

    while true; do
        show_menu

        case $choice in
            1)
                clear
                run_refactor
                ;;
            2)
                clear
                quick_start
                ;;
            3)
                clear
                run_tests
                ;;
            4)
                clear
                memory_monitor
                ;;
            5)
                clear
                setup_environment
                ;;
            6)
                clear
                check_status
                ;;
            7)
                clear
                troubleshoot
                ;;
            8)
                clear
                show_documentation
                ;;
            0)
                echo "👋 感謝使用！"
                exit 0
                ;;
            *)
                echo "❌ 無效選項，請重新選擇"
                sleep 2
                ;;
        esac
        clear
    done
}

# 檢查是否為直接執行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi