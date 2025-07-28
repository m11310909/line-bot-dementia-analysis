# ========================================
# 🚀 LINE Bot M1+M2+M3 全自動升級腳本
# ========================================

echo "🚀 開始 LINE Bot 全自動升級到 M1+M2+M3 系統"
echo "⏰ 預估時間：5-10 分鐘"
echo ""

# ========================================
# 步驟 1：環境檢查和備份
# ========================================
echo "============================================"
echo "📋 步驟 1：環境檢查和備份"
echo "============================================"

# 檢查新 API 是否運行
echo "🔍 檢查 M1+M2+M3 API 狀態..."
if ! curl -s http://localhost:8005/health > /dev/null; then
    echo "❌ M1+M2+M3 API 未運行，請先啟動"
    echo "💡 執行：bash final_fix_script.sh"
    exit 1
fi
echo "✅ M1+M2+M3 API 運行正常"

# 備份現有 LINE Bot 文件
echo "💾 備份現有 LINE Bot 文件..."
BACKUP_DIR="linebot_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 查找並備份可能的 LINE Bot 文件
for file in *.py; do
    if [ -f "$file" ]; then
        if grep -q "line.*bot\|webhook\|flex" "$file" 2>/dev/null; then
            echo "📄 備份：$file"
            cp "$file" "$BACKUP_DIR/"
        fi
    fi
done

echo "✅ 備份完成：$BACKUP_DIR"

# ========================================
# 步驟 2：建立增強版 LINE Bot
# ========================================
echo ""
echo "============================================"
echo "📋 步驟 2：建立增強版 LINE Bot"
echo "============================================"

echo "🔧 建立增強版 LINE Bot 代碼..."

cat > enhanced_line_bot.py << 'LINEBOT_CODE'
import os
import sys
import json
import logging
import requests
from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
)

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LINE Bot 設定
app = Flask(__name__)

# 從環境變數獲取設定（請設定你的實際值）
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', 'your_channel_secret_here')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'your_access_token_here')

# 初始化 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class M1M2M3AnalysisBot:
    """增強版失智症分析 Bot"""

    def __init__(self):
        # 新的 M1+M2+M3 API 設定
        self.api_base_url = "http://localhost:8005"
        self.analysis_endpoint = f"{self.api_base_url}/comprehensive-analysis"
        self.health_endpoint = f"{self.api_base_url}/health"
        self.fallback_endpoint = f"{self.api_base_url}/m1-flex"

        # 統計資料
        self.stats = {
            "total_requests": 0,
            "successful_analysis": 0,
            "m1_detections": 0,
            "m3_detections": 0,
            "cross_module_detections": 0
        }

        logger.info("🚀 增強版失智症分析 Bot 初始化完成")

    def analyze_symptoms(self, user_input: str, user_id: str = None) -> FlexSendMessage:
        """主要症狀分析函數"""
        self.stats["total_requests"] += 1

        try:
            # 記錄使用者輸入（去敏化）
            logger.info(f"分析請求 - 長度：{len(user_input)}，用戶：{user_id[:8] if user_id else 'unknown'}")

            # 發送分析請求
            response = requests.post(
                self.analysis_endpoint,
                json={"user_input": user_input},
                timeout=30,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                return self._process_successful_response(response.json(), user_input)
            else:
                logger.warning(f"API 錯誤：{response.status_code}")
                return self._try_fallback_api(user_input)

        except requests.exceptions.Timeout:
            logger.error("API 請求超時")
            return self._create_timeout_message()
        except requests.exceptions.ConnectionError:
            logger.error("API 連接失敗")
            return self._create_connection_error_message()
        except Exception as e:
            logger.error(f"分析錯誤：{str(e)}")
            return self._create_general_error_message()

    def _process_successful_response(self, data: dict, user_input: str) -> FlexSendMessage:
        """處理成功的 API 回應"""

        # 檢查是否有錯誤
        if "error" in data:
            logger.error(f"API 返回錯誤：{data['error']}")
            return self._create_general_error_message()

        # 更新統計資料
        self.stats["successful_analysis"] += 1
        self._update_detection_stats(data)

        # 記錄分析結果
        self._log_analysis_result(data, user_input)

        # 提取並返回 Flex Message
        flex_message = data.get("flex_message")
        if flex_message:
            return FlexSendMessage(
                alt_text=flex_message.get("altText", "失智症分析結果"),
                contents=flex_message["contents"]
            )
        else:
            logger.warning("Flex Message 生成失敗")
            return self._create_general_error_message()

    def _try_fallback_api(self, user_input: str) -> FlexSendMessage:
        """嘗試使用備用 API"""
        try:
            logger.info("嘗試使用備用 API")
            response = requests.post(
                self.fallback_endpoint,
                json={"user_input": user_input},
                timeout=15
            )

            if response.status_code == 200:
                return self._process_successful_response(response.json(), user_input)
            else:
                return self._create_general_error_message()

        except Exception as e:
            logger.error(f"備用 API 也失敗：{str(e)}")
            return self._create_general_error_message()

    def _update_detection_stats(self, data: dict):
        """更新檢測統計"""
        analysis = data.get("comprehensive_analysis", {})
        modules_used = analysis.get("modules_used", [])

        if "M1" in modules_used:
            self.stats["m1_detections"] += 1
        if "M3" in modules_used:
            self.stats["m3_detections"] += 1
        if len(modules_used) > 1:
            self.stats["cross_module_detections"] += 1

    def _log_analysis_result(self, data: dict, user_input: str):
        """記錄分析結果"""
        analysis = data.get("comprehensive_analysis", {})

        log_data = {
            "input_length": len(user_input),
            "matched_codes": analysis.get("matched_codes", []),
            "modules_used": analysis.get("modules_used", []),
            "total_findings": analysis.get("total_findings", 0),
            "has_bpsd": analysis.get("bpsd_analysis") is not None,
            "has_stage": analysis.get("stage_detection") is not None,
            "api_version": data.get("version", "unknown"),
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"分析完成：{json.dumps(log_data, ensure_ascii=False)}")

    def check_api_health(self) -> bool:
        """檢查 API 健康狀態"""
        try:
            response = requests.get(self.health_endpoint, timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                is_healthy = health_data.get("status") == "healthy"
                if is_healthy:
                    logger.info("API 健康檢查通過")
                return is_healthy
            return False
        except Exception as e:
            logger.error(f"健康檢查失敗：{str(e)}")
            return False

    def get_stats(self) -> dict:
        """獲取統計資料"""
        return self.stats.copy()

    def _create_timeout_message(self) -> FlexSendMessage:
        """創建超時訊息"""
        return FlexSendMessage(
            alt_text="分析請求超時",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "⏰ 分析請求超時\n\n請稍後再試，或嘗試簡化症狀描述。",
                        "wrap": True,
                        "size": "md",
                        "color": "#666666"
                    }]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "message",
                            "label": "重新嘗試",
                            "text": "請幫我分析症狀"
                        }
                    }]
                }
            }
        )

    def _create_connection_error_message(self) -> FlexSendMessage:
        """創建連接錯誤訊息"""
        return FlexSendMessage(
            alt_text="服務暫時無法使用",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "🔧 分析服務暫時維護中\n\n請稍後再試，造成不便敬請見諒。",
                        "wrap": True,
                        "size": "md",
                        "color": "#666666"
                    }]
                }
            }
        )

    def _create_general_error_message(self) -> FlexSendMessage:
        """創建一般錯誤訊息"""
        return FlexSendMessage(
            alt_text="系統暫時無法分析",
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "😅 系統暫時無法分析\n\n請稍後再試，或聯繫客服協助。",
                        "wrap": True,
                        "size": "md",
                        "color": "#666666"
                    }]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "secondary",
                            "action": {
                                "type": "message",
                                "label": "重試",
                                "text": "重新分析"
                            },
                            "flex": 1
                        },
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "客服",
                                "uri": "https://www.tada2002.org.tw/"
                            },
                            "flex": 1,
                            "margin": "sm"
                        }
                    ]
                }
            }
        )

# 初始化分析機器人
analysis_bot = M1M2M3AnalysisBot()

@app.route("/callback", methods=['POST'])
def callback():
    """LINE Bot webhook 回調函數"""

    # 獲取 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']

    # 獲取請求主體為文本
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 webhook 主體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理文字訊息"""

    user_message = event.message.text.strip()
    user_id = event.source.user_id if hasattr(event.source, 'user_id') else None

    # 記錄收到的訊息
    logger.info(f"收到訊息：{len(user_message)} 字符")

    # 特殊命令處理
    if user_message.lower() in ['health', '健康檢查']:
        if analysis_bot.check_api_health():
            reply_message = TextSendMessage(text="✅ 系統運行正常")
        else:
            reply_message = TextSendMessage(text="❌ 系統維護中")

    elif user_message.lower() in ['stats', '統計']:
        stats = analysis_bot.get_stats()
        stats_text = f"""📊 系統統計：
總請求：{stats['total_requests']}
成功分析：{stats['successful_analysis']}
M1 檢測：{stats['m1_detections']}
M3 檢測：{stats['m3_detections']}
跨模組：{stats['cross_module_detections']}"""
        reply_message = TextSendMessage(text=stats_text)

    elif len(user_message) < 3:
        # 訊息太短
        reply_message = TextSendMessage(
            text="請描述更詳細的症狀，例如：\n• 記憶力問題\n• 行為改變\n• 情緒變化\n\n這樣我才能提供準確的分析。"
        )

    else:
        # 進行症狀分析
        reply_message = analysis_bot.analyze_symptoms(user_message, user_id)

    # 回復訊息
    try:
        line_bot_api.reply_message(event.reply_token, reply_message)
    except LineBotApiError as e:
        logger.error(f"LINE Bot API 錯誤：{e}")

@app.route("/health", methods=['GET'])
def health_check():
    """健康檢查端點"""
    api_healthy = analysis_bot.check_api_health()
    stats = analysis_bot.get_stats()

    return {
        "status": "healthy" if api_healthy else "degraded",
        "api_status": "healthy" if api_healthy else "unhealthy",
        "stats": stats,
        "timestamp": datetime.now().isoformat()
    }

@app.route("/", methods=['GET'])
def index():
    """首頁"""
    return {
        "message": "增強版失智症分析 LINE Bot",
        "version": "3.0.0",
        "features": [
            "M1: 失智症十大警訊識別",
            "M3: BPSD 行為心理症狀分析",
            "跨模組整合分析",
            "智能綜合評估",
            "個人化管理建議"
        ],
        "api_endpoint": analysis_bot.analysis_endpoint,
        "status": "healthy" if analysis_bot.check_api_health() else "degraded"
    }

if __name__ == "__main__":
    # 檢查環境變數
    if LINE_CHANNEL_SECRET == 'your_channel_secret_here' or LINE_CHANNEL_ACCESS_TOKEN == 'your_access_token_here':
        print("⚠️  請設定 LINE Bot 環境變數：")
        print("export LINE_CHANNEL_SECRET='your_actual_secret'")
        print("export LINE_CHANNEL_ACCESS_TOKEN='your_actual_token'")
        print("\n💡 或直接在代碼中修改設定值")

    # 啟動檢查
    if analysis_bot.check_api_health():
        print("✅ M1+M2+M3 API 連接正常")
        print("🚀 啟動增強版 LINE Bot...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ M1+M2+M3 API 連接失敗")
        print("💡 請確認 API 服務運行在 http://localhost:8005")
LINEBOT_CODE

echo "✅ 增強版 LINE Bot 建立完成"

# ========================================
# 步驟 3：建立環境設定腳本
# ========================================
echo ""
echo "============================================"
echo "📋 步驟 3：建立環境設定和部署腳本"
echo "============================================"

# 建立環境設定腳本
cat > setup_linebot_env.sh << 'ENV_SCRIPT'
#!/bin/bash

echo "🔧 LINE Bot 環境設定"
echo ""

# 檢查必要的 Python 套件
echo "📦 檢查 Python 套件..."
python3 -c "import flask, requests, linebot" 2>/dev/null || {
    echo "⚠️  缺少必要套件，正在安裝..."
    pip3 install flask requests line-bot-sdk
}
echo "✅ Python 套件檢查完成"

# 建立環境變數設定檔
cat > .env << 'ENV_FILE'
# LINE Bot 環境變數設定
# 請將下面的值替換為你的實際 LINE Bot 設定

# LINE Channel Secret
LINE_CHANNEL_SECRET=your_channel_secret_here

# LINE Channel Access Token  
LINE_CHANNEL_ACCESS_TOKEN=your_access_token_here

# M1+M2+M3 API 設定
API_BASE_URL=http://localhost:8005
ANALYSIS_ENDPOINT=http://localhost:8005/comprehensive-analysis

# 日誌設定
LOG_LEVEL=INFO
ENV_FILE

echo "📄 環境變數設定檔已建立：.env"
echo ""
echo "🔧 請編輯 .env 檔案，設定你的 LINE Bot 參數："
echo "   1. LINE_CHANNEL_SECRET"
echo "   2. LINE_CHANNEL_ACCESS_TOKEN"
echo ""
echo "💡 或執行以下命令直接設定："
echo "   export LINE_CHANNEL_SECRET='your_actual_secret'"
echo "   export LINE_CHANNEL_ACCESS_TOKEN='your_actual_token'"
ENV_SCRIPT

chmod +x setup_linebot_env.sh

# 建立部署腳本
cat > deploy_linebot.sh << 'DEPLOY_SCRIPT'
#!/bin/bash

echo "🚀 部署增強版 LINE Bot"
echo ""

# 載入環境變數
if [ -f .env ]; then
    echo "📄 載入環境變數..."
    set -a
    source .env
    set +a
fi

# 檢查 M1+M2+M3 API
echo "🔍 檢查 M1+M2+M3 API..."
if curl -s http://localhost:8005/health > /dev/null; then
    echo "✅ M1+M2+M3 API 運行正常"
else
    echo "❌ M1+M2+M3 API 未運行"
    echo "💡 請先啟動：bash final_fix_script.sh"
    exit 1
fi

# 檢查環境變數
if [ "$LINE_CHANNEL_SECRET" = "your_channel_secret_here" ] || [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "⚠️  LINE_CHANNEL_SECRET 未設定"
    echo "💡 請設定環境變數或編輯 .env 檔案"
    exit 1
fi

if [ "$LINE_CHANNEL_ACCESS_TOKEN" = "your_access_token_here" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "⚠️  LINE_CHANNEL_ACCESS_TOKEN 未設定"
    echo "💡 請設定環境變數或編輯 .env 檔案"
    exit 1
fi

# 停止可能運行的舊版本
echo "🛑 停止舊版 LINE Bot..."
pkill -f "enhanced_line_bot" 2>/dev/null || echo "沒有找到舊版本"

# 啟動新版本
echo "🚀 啟動增強版 LINE Bot..."
echo "📍 服務將運行在 http://localhost:5000"
echo "📱 Webhook URL: http://your-domain.com/callback"
echo ""

python3 enhanced_line_bot.py
DEPLOY_SCRIPT

chmod +x deploy_linebot.sh

# 建立測試腳本
cat > test_linebot.sh << 'TEST_SCRIPT'
#!/bin/bash

echo "🧪 測試增強版 LINE Bot"
echo ""

# 測試健康檢查
echo "📊 測試健康檢查："
curl -s http://localhost:5000/health | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'狀態：{data.get(\"status\")}')
    print(f'API 狀態：{data.get(\"api_status\")}')
    stats = data.get('stats', {})
    print(f'總請求：{stats.get(\"total_requests\", 0)}')
except:
    print('健康檢查失敗')
"

echo ""
echo "📋 測試基本資訊："
curl -s http://localhost:5000/ | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'版本：{data.get(\"version\")}')
    print(f'狀態：{data.get(\"status\")}')
    features = data.get('features', [])
    print('功能：')
    for feature in features:
        print(f'  - {feature}')
except:
    print('基本資訊測試失敗')
"

echo ""
echo "✅ 測試完成"
echo "💡 如果看到正常回應，表示 LINE Bot 運行正常"
TEST_SCRIPT

chmod +x test_linebot.sh

echo "✅ 部署腳本建立完成"

# ========================================
# 步驟 4：執行環境設定
# ========================================
echo ""
echo "============================================"
echo "📋 步驟 4：執行環境設定"
echo "============================================"

# 執行環境設定
./setup_linebot_env.sh

# ========================================
# 步驟 5：顯示完成資訊和後續步驟
# ========================================
echo ""
echo "============================================"
echo "🎉 LINE Bot 全自動升級完成！"
echo "============================================"
echo ""
echo "📁 建立的檔案："
echo "   ✅ enhanced_line_bot.py     - 增強版 LINE Bot 主程式"
echo "   ✅ setup_linebot_env.sh     - 環境設定腳本"
echo "   ✅ deploy_linebot.sh        - 部署腳本"
echo "   ✅ test_linebot.sh          - 測試腳本"
echo "   ✅ .env                     - 環境變數設定檔"
echo "   📁 $BACKUP_DIR              - 原始檔案備份"
echo ""
echo "🔧 下一步操作："
echo ""
echo "1️⃣  設定 LINE Bot 參數："
echo "   編輯 .env 檔案或執行："
echo "   export LINE_CHANNEL_SECRET='your_actual_secret'"
echo "   export LINE_CHANNEL_ACCESS_TOKEN='your_actual_token'"
echo ""
echo "2️⃣  部署 LINE Bot："
echo "   ./deploy_linebot.sh"
echo ""
echo "3️⃣  測試功能："
echo "   ./test_linebot.sh"
echo ""
echo "🆕 新功能特色："
echo "   ✅ M1: 失智症十大警訊識別"
echo "   ✅ M3: BPSD 行為心理症狀分析（7大類）"
echo "   ✅ 跨模組整合分析"
echo "   ✅ 智能綜合評估"
echo "   ✅ 個人化管理建議"
echo "   ✅ 增強版 Flex Message"
echo "   ✅ 自動錯誤處理和降級"
echo "   ✅ 詳細統計和監控"
echo ""
echo "📱 LINE Bot 服務資訊："
echo "   🔗 本地地址：http://localhost:5000"
echo "   📍 Webhook：http://your-domain.com/callback"
echo "   💚 健康檢查：http://localhost:5000/health"
echo ""
echo "🎯 升級完成！你的 LINE Bot 現在具備業界最先進的失智症分析功能！"