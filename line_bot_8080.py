from flask import Flask, request, jsonify
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)

# Get credentials from Replit Secrets
ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

print(f"🔑 ACCESS_TOKEN: {'✅ Found' if ACCESS_TOKEN else '❌ Missing'}")
print(f"🔑 CHANNEL_SECRET: {'✅ Found' if CHANNEL_SECRET else '❌ Missing'}")

if ACCESS_TOKEN and CHANNEL_SECRET:
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    handler = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def home():
    return "🤖 LINE Bot with Advanced Components - Ready on Port 8080! 📱"

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "port": 8080}), 200

@app.route('/callback', methods=['POST'])
def callback():
    try:
        print("✅ Webhook received from LINE!")
        
        if not ACCESS_TOKEN or not CHANNEL_SECRET:
            print("❌ Missing credentials")
            return jsonify({"error": "Missing credentials"}), 500
        
        # Get signature and body
        signature = request.headers.get('X-Line-Signature', '')
        body = request.get_data(as_text=True)
        
        # Handle webhook
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("❌ Invalid signature")
            return jsonify({"error": "Invalid signature"}), 400
            
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"❌ Callback error: {e}")
        return jsonify({"error": str(e)}), 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_message = event.message.text
        print(f"📝 User message: {user_message}")
        
        # Create comprehensive flex message with ALL 7 components
        flex_content = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": "🧠 失智症警訊分析系統",
                    "weight": "bold",
                    "color": "#ffffff",
                    "size": "lg"
                }],
                "backgroundColor": "#FF6B6B",
                "paddingAll": "lg"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"📝 您的描述：{user_message}",
                        "wrap": True,
                        "weight": "bold",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⚠️ 警訊對比卡片 (comparison_card)",
                                "weight": "bold",
                                "color": "#FF6B6B"
                            },
                            {
                                "type": "text",
                                "text": "✅ 正常老化：偶爾忘記約會或朋友名字",
                                "size": "sm",
                                "color": "#28a745"
                            },
                            {
                                "type": "text",
                                "text": "🚨 失智警訊：重複問相同問題，忘記剛說過的話",
                                "size": "sm",
                                "color": "#dc3545"
                            }
                        ],
                        "backgroundColor": "#FFF3F3",
                        "cornerRadius": "md",
                        "paddingAll": "md",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📊 信心度量表 (confidence_meter): 85%",
                                "weight": "bold",
                                "color": "#007bff"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "filler"
                                    }
                                ],
                                "backgroundColor": "#007bff",
                                "height": "8px",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": "#F0F8FF",
                        "cornerRadius": "md",
                        "paddingAll": "md",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡 XAI解釋盒 (xai_box)",
                                "weight": "bold",
                                "color": "#4ECDC4"
                            },
                            {
                                "type": "text",
                                "text": "AI分析：重複詢問相同問題是短期記憶受損的典型表現，符合失智症M1-01警訊特徵。",
                                "size": "sm",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": "#F0FFFF",
                        "cornerRadius": "md",
                        "paddingAll": "md",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "ℹ️ 資訊盒 (info_box)",
                                "weight": "bold",
                                "color": "#17a2b8"
                            },
                            {
                                "type": "text",
                                "text": "📋 警訊類型：M1-01 記憶力減退\n🏥 建議科別：神經內科\n⏰ 觀察期：持續2週以上",
                                "size": "sm",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": "#E7F3FF",
                        "cornerRadius": "md",
                        "paddingAll": "md",
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🚨 警告盒 (warning_box)",
                                "weight": "bold",
                                "color": "#dc3545",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": "⚠️ 重要提醒：如症狀持續，請盡快諮詢專業醫師",
                                "size": "xs",
                                "color": "#dc3545"
                            }
                        ],
                        "backgroundColor": "#FFE6E6",
                        "cornerRadius": "sm",
                        "paddingAll": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "🎯 行動卡片 (action_card)",
                        "weight": "bold",
                        "color": "#28a745",
                        "size": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "📅 建立時間軸追蹤 (timeline_list)",
                            "text": "時間軸追蹤"
                        },
                        "style": "primary",
                        "color": "#28a745"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🔍 查看更多警訊",
                            "text": "更多警訊"
                        },
                        "style": "secondary",
                        "margin": "sm"
                    }
                ],
                "spacing": "sm"
            }
        }
        
        # Send comprehensive flex message
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text=f"失智症警訊分析：{user_message}",
                contents=flex_content
            )
        )
        
        print("✅ 包含所有7個組件的Flex訊息已發送!")
        
    except Exception as e:
        print(f"❌ Message handling error: {e}")
        # Fallback text message
        if ACCESS_TOKEN:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"收到訊息：{user_message}\n系統正在處理中...")
            )

if __name__ == '__main__':
    print("🚀 啟動 LINE Bot - 包含所有7個進階組件")
    print("📱 Port: 8080")
    print("🎯 組件：comparison_card, confidence_meter, xai_box, info_box, action_card, timeline_list, warning_box")
    app.run(host='0.0.0.0', port=8080, debug=False)
