"""
最簡化的 Replit LINE Bot - 模擬 M1+M2+M3 功能
複製此代碼到你的 Replit 專案中，立即可用
"""

import os
import logging
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 應用
app = Flask(__name__)

# LINE Bot 設定（從 Replit Secrets 獲取）
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# 初始化 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def analyze_symptoms(user_input):
    """模擬 M1+M2+M3 症狀分析"""

    # 症狀關鍵字檢測
    symptoms_detected = []
    suggestions = []

    # M1 失智症警訊檢測
    memory_keywords = ["忘記", "記憶", "健忘", "記不得", "重複問"]
    thinking_keywords = ["混亂", "迷路", "找不到", "不認識"]

    if any(kw in user_input for kw in memory_keywords):
        symptoms_detected.append({
            "icon": "🚨",
            "code": "M1-01", 
            "title": "記憶力減退影響日常生活",
            "confidence": "HIGH"
        })
        suggestions.append("記錄忘記事件的模式和頻率")

    if any(kw in user_input for kw in thinking_keywords):
        symptoms_detected.append({
            "icon": "🚨",
            "code": "M1-02",
            "title": "無法勝任原本熟悉的事務", 
            "confidence": "MEDIUM"
        })
        suggestions.append("評估日常活動的獨立性")

    # M3 BPSD 行為心理症狀檢測
    paranoia_keywords = ["懷疑", "偷", "不信任", "害", "陷害"]
    aggression_keywords = ["打人", "叫罵", "暴躁", "發脾氣", "攻擊"]
    depression_keywords = ["憂鬱", "悲傷", "不想", "沒興趣", "低落"]
    sleep_keywords = ["睡不著", "失眠", "日夜顛倒", "不睡", "睡眠"]

    if any(kw in user_input for kw in paranoia_keywords):
        symptoms_detected.append({
            "icon": "🧠",
            "code": "M3-01",
            "title": "妄想症狀",
            "confidence": "HIGH"
        })
        suggestions.append("避免直接否定妄想，提供安全感")

    if any(kw in user_input for kw in aggression_keywords):
        symptoms_detected.append({
            "icon": "🧠", 
            "code": "M3-03",
            "title": "激動與攻擊行為",
            "confidence": "HIGH"
        })
        suggestions.append("保持冷靜，識別觸發因子")

    if any(kw in user_input for kw in depression_keywords):
        symptoms_detected.append({
            "icon": "🧠",
            "code": "M3-04", 
            "title": "憂鬱與焦慮",
            "confidence": "MEDIUM"
        })
        suggestions.append("提供情感支持，維持規律作息")

    if any(kw in user_input for kw in sleep_keywords):
        symptoms_detected.append({
            "icon": "🧠",
            "code": "M3-06",
            "title": "睡眠障礙與日夜顛倒", 
            "confidence": "HIGH"
        })
        suggestions.append("改善睡眠環境，增加白天光照")

    # 如果沒有檢測到特定症狀
    if not symptoms_detected:
        symptoms_detected.append({
            "icon": "🔍",
            "code": "GENERAL",
            "title": "需要更詳細的症狀描述",
            "confidence": "LOW"
        })
        suggestions.append("請提供更具體的行為或症狀描述")

    return symptoms_detected, suggestions

def create_analysis_flex_message(user_input, symptoms, suggestions):
    """建立分析結果的 Flex Message"""

    # 建立症狀內容
    symptom_contents = []
    for symptom in symptoms[:3]:  # 最多顯示 3 個症狀
        confidence_color = {
            "HIGH": "#28a745",
            "MEDIUM": "#ffc107", 
            "LOW": "#dc3545"
        }.get(symptom["confidence"], "#6c757d")

        symptom_contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"{symptom['icon']} {symptom['title']}",
                    "size": "sm",
                    "weight": "bold",
                    "color": "#005073",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": f"代碼：{symptom['code']} | 信心：{symptom['confidence']}",
                    "size": "xs",
                    "color": confidence_color,
                    "margin": "xs"
                }
            ]
        })

    # 建立建議內容
    suggestion_contents = []
    for suggestion in suggestions[:3]:  # 最多顯示 3 個建議
        suggestion_contents.append({
            "type": "text",
            "text": f"• {suggestion}",
            "size": "xs",
            "margin": "xs",
            "wrap": True,
            "color": "#666666"
        })

    return FlexSendMessage(
        alt_text=f"失智症症狀分析：檢測到 {len(symptoms)} 項症狀",
        contents={
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "🧠 M1+M2+M3 症狀分析",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                }],
                "backgroundColor": "#005073",
                "paddingAll": "15dp"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📝 症狀描述",
                        "weight": "bold",
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": user_input,
                        "size": "sm",
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"🔍 檢測結果 ({len(symptoms)} 項)",
                        "weight": "bold", 
                        "size": "sm",
                        "color": "#005073",
                        "margin": "md"
                    }
                ] + symptom_contents + [
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "💡 專業建議",
                        "weight": "bold",
                        "size": "sm", 
                        "color": "#005073",
                        "margin": "md"
                    }
                ] + suggestion_contents + [
                    {
                        "type": "text",
                        "text": "• 建議諮詢專業醫療人員進行詳細評估",
                        "size": "xs",
                        "margin": "sm",
                        "wrap": True,
                        "color": "#666666"
                    }
                ],
                "paddingAll": "15dp"
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "更多資訊",
                            "text": "請告訴我更多症狀資訊"
                        },
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm", 
                        "action": {
                            "type": "uri",
                            "label": "專業諮詢",
                            "uri": "https://www.tada2002.org.tw/"
                        },
                        "flex": 1,
                        "margin": "sm"
                    }
                ],
                "paddingAll": "15dp"
            }
        }
    )

@app.route("/webhook", methods=['POST'])
def webhook():
    """LINE Bot webhook 端點"""

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理使用者訊息"""

    user_message = event.message.text.strip()

    # 特殊指令
    if user_message.lower() in ['health', '健康檢查', 'status']:
        reply_message = TextSendMessage(
            text="✅ 系統運行正常\n🧠 M1+M2+M3 模擬模式\n📊 支援症狀分析功能"
        )
    elif user_message.lower() in ['help', '幫助', '使用說明']:
        reply_message = TextSendMessage(
            text="""🧠 失智症症狀分析 Bot 使用說明

📝 使用方式：
直接描述觀察到的症狀或行為

🔍 支援檢測：
• M1 失智症警訊（記憶、思考問題）
• M3 BPSD 行為心理症狀（妄想、激動、憂鬱、睡眠等）

💡 範例：
「媽媽常忘記關瓦斯爐」
「爸爸懷疑有人偷他的東西」
「奶奶睡眠日夜顛倒」

🏥 提醒：此為初步篩檢，請諮詢專業醫療人員"""
        )
    elif len(user_message) < 3:
        reply_message = TextSendMessage(
            text="請描述更詳細的症狀，例如：\n• 記憶力問題\n• 行為改變\n• 情緒變化\n• 睡眠問題\n\n輸入「幫助」查看使用說明"
        )
    else:
        # 進行症狀分析
        symptoms, suggestions = analyze_symptoms(user_message)
        reply_message = create_analysis_flex_message(user_message, symptoms, suggestions)

        # 記錄分析結果
        logger.info(f"症狀分析 - 輸入長度：{len(user_message)}，檢測症狀：{len(symptoms)}")

    try:
        line_bot_api.reply_message(event.reply_token, reply_message)
    except LineBotApiError as e:
        logger.error(f"LINE Bot API 錯誤：{e}")

@app.route("/", methods=['GET'])
def index():
    """首頁"""
    return {
        "message": "失智症分析 LINE Bot - Replit 版本",
        "version": "3.0.0-replit-simple",
        "status": "running",
        "features": [
            "M1: 失智症十大警訊識別", 
            "M3: BPSD 行為心理症狀分析",
            "智能關鍵字檢測",
            "專業建議生成"
        ],
        "supported_symptoms": [
            "記憶力減退", "思考混亂", "妄想症狀", 
            "激動攻擊", "憂鬱焦慮", "睡眠障礙"
        ]
    }

@app.route("/health", methods=['GET'])
def health():
    """健康檢查"""
    return {
        "status": "healthy",
        "mode": "simulation",
        "line_bot_configured": bool(LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN)
    }

if __name__ == "__main__":
    if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
        print("⚠️  請在 Replit Secrets 中設定：")
        print("   LINE_CHANNEL_SECRET")
        print("   LINE_CHANNEL_ACCESS_TOKEN")
    else:
        print("✅ LINE Bot 設定完成")

    print("🚀 啟動 Replit LINE Bot...")
    app.run(host='0.0.0.0', port=3000)
