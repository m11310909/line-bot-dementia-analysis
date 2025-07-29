from flask import Flask, request, jsonify
import os
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)

# Get credentials from Replit Secrets (environment variables)
ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

print(f"🔑 ACCESS_TOKEN: {'✅ Found' if ACCESS_TOKEN else '❌ Missing'}")
print(f"🔑 CHANNEL_SECRET: {'✅ Found' if CHANNEL_SECRET else '❌ Missing'}")

if not ACCESS_TOKEN or not CHANNEL_SECRET:
    print("❌ Missing LINE credentials in Replit Secrets!")
    print("💡 Please add LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET to Replit Secrets")
    exit(1)

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def home():
    return "🤖 Working Flex Bot - Ready! 📱"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/callback', methods=['POST'])
def callback():
    try:
        # Get X-Line-Signature header value
        signature = request.headers.get('X-Line-Signature', '')
        
        # Get request body as text
        body = request.get_data(as_text=True)
        print(f"✅ Callback received from LINE")
        
        # Handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print("❌ Invalid signature")
            return jsonify({"error": "Invalid signature"}), 400
        except Exception as e:
            print(f"❌ Handler error: {e}")
            return jsonify({"error": str(e)}), 500
            
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        print(f"❌ Callback error: {e}")
        return jsonify({"error": str(e)}), 500

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        user_message = event.message.text
        print(f"📝 User message: {user_message}")
        
        # Create comprehensive flex message with ALL components
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
                        "margin": "md",
                        "weight": "bold"
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
                                "color": "#FF6B6B",
                                "size": "md"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "✅ 正常老化：偶爾忘記約會或朋友名字",
                                        "size": "sm",
                                        "color": "#28a745",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "text", 
                                        "text": "🚨 失智警訊：重複問相同問題，忘記剛說過的話",
                                        "size": "sm",
                                        "color": "#dc3545",
                                        "margin": "sm"
                                    }
                                ]
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
                                "text": "📊 信心度量表 (confidence_meter)",
                                "weight": "bold",
                                "color": "#007bff"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "AI 分析信心度：",
                                        "size": "sm",
                                        "flex": 0
                                    },
                                    {
                                        "type": "text",
                                        "text": "85%",
                                        "size": "sm",
                                        "weight": "bold",
                                        "color": "#007bff",
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [{"type": "filler"}],
                                        "backgroundColor": "#007bff",
                                        "height": "8px",
                                        "flex": 85
                                    },
                                    {
                                        "type": "box", 
                                        "layout": "baseline",
                                        "contents": [{"type": "filler"}],
                                        "backgroundColor": "#E0E0E0",
                                        "height": "8px",
                                        "flex": 15
                                    }
                                ],
                                "spacing": "none",
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
                                "text": "AI 分析依據：重複詢問相同問題是短期記憶受損的典型表現，符合失智症早期警訊 M1-01「記憶力減退影響生活」的特徵。建議進行專業評估。",
                                "size": "sm",
                                "wrap": True,
                                "margin": "sm"
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
                                "text": "📋 相關資訊：失智症十大警訊 M1-01\n🏥 建議科別：神經內科、精神科\n⏰ 觀察期間：持續2週以上",
                                "size": "sm",
                                "wrap": True,
                                "margin": "sm"
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
                        "type": "text",
                        "text": "🎯 行動卡片 (action_card)",
                        "weight": "bold",
                        "color": "#28a745",
                        "size": "sm"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "📅 建立追蹤時間軸",
                            "text": "時間軸追蹤"
                        },
                        "style": "primary",
                        "color": "#28a745"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message", 
                            "label": "🚨 查看更多警訊",
                            "text": "更多警訊"
                        },
                        "style": "secondary",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "💡 獲得專業建議",
                            "text": "專業建議"
                        },
                        "style": "secondary",
                        "margin": "sm"
                    }
                ],
                "spacing": "sm",
                "paddingAll": "md",
                "backgroundColor": "#F8F9FA"
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
        
        print("✅ 完整Flex訊息已發送 - 包含所有進階組件!")
        
    except LineBotApiError as e:
        print(f"❌ LINE API Error: {e}")
        # Fallback message
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"收到您的訊息：{user_message}\n系統正在處理中...")
        )
    except Exception as e:
        print(f"❌ Message handling error: {e}")

if __name__ == '__main__':
    print("🚀 啟動完整組件展示 LINE Bot...")
    print("📱 Webhook: /callback")
    print("🎯 包含所有7個進階組件")
    app.run(host='0.0.0.0', port=5001, debug=True)
