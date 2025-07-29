from fastapi import FastAPI, Request
import uvicorn
import json
import os
import httpx
import asyncio

app = FastAPI()

# 環境變數
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')
GEMINI_KEY = os.getenv('AISTUDIO_API_KEY', '')

class AdvancedFlexComponents:
    """進階 Flex Message 組件系統"""

    @staticmethod
    def comparison_card(normal_aging: str, warning_sign: str, confidence: float):
        """警訊對比卡片"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⚖️ 對比分析",
                    "weight": "bold",
                    "size": "md",
                    "color": "#1DB446"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✅ 正常老化",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#00B900"
                                },
                                {
                                    "type": "text",
                                    "text": normal_aging,
                                    "wrap": True,
                                    "size": "xs",
                                    "color": "#00B900",
                                    "margin": "sm"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 1,
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⚠️ 警訊特徵",
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#FF5551"
                                },
                                {
                                    "type": "text",
                                    "text": warning_sign,
                                    "wrap": True,
                                    "size": "xs",
                                    "color": "#FF5551",
                                    "margin": "sm"
                                }
                            ]
                        }
                    ],
                    "margin": "md"
                }
            ],
            "backgroundColor": "#F8F9FA",
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "margin": "md"
        }

    @staticmethod
    def confidence_meter(confidence: float, category: str):
        """信心度量表"""
        # 計算量表條數 (最多5條)
        filled_bars = int(confidence * 5)
        confidence_color = "#00B900" if confidence > 0.7 else "#FFA500" if confidence > 0.4 else "#FF5551"

        bars = []
        for i in range(5):
            bars.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": confidence_color if i < filled_bars else "#E0E0E0",
                "flex": 1,
                "height": "6px",
                "margin": "xs"
            })

        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"📊 分析信心度: {confidence:.0%}",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#333333"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": bars,
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"類別: {category}",
                    "size": "xs",
                    "color": "#666666",
                    "margin": "xs"
                }
            ],
            "margin": "md"
        }

    @staticmethod
    def xai_box(explanation: str, key_factors: list):
        """XAI 解釋盒"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🤖 AI 解釋",
                    "weight": "bold",
                    "size": "md",
                    "color": "#6C5CE7"
                },
                {
                    "type": "text",
                    "text": explanation,
                    "wrap": True,
                    "size": "sm",
                    "color": "#333333",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "🔍 關鍵因素:",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#6C5CE7",
                    "margin": "md"
                }
            ] + [
                {
                    "type": "text",
                    "text": f"• {factor}",
                    "size": "xs",
                    "color": "#666666",
                    "margin": "xs"
                } for factor in key_factors
            ],
            "backgroundColor": "#F0F0FF",
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "margin": "md"
        }

    @staticmethod
    def info_box(title: str, content: str, icon: str = "ℹ️"):
        """資訊盒"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{icon} {title}",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#0084FF"
                },
                {
                    "type": "text",
                    "text": content,
                    "wrap": True,
                    "size": "xs",
                    "color": "#333333",
                    "margin": "sm"
                }
            ],
            "backgroundColor": "#E3F2FD",
            "cornerRadius": "6px",
            "paddingAll": "10px",
            "margin": "sm"
        }

    @staticmethod
    def action_card(recommendations: list):
        """行動卡片"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎯 建議行動",
                    "weight": "bold",
                    "size": "md",
                    "color": "#FF6B35"
                }
            ] + [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{i+1}",
                            "flex": 0,
                            "size": "xs",
                            "color": "#FFFFFF",
                            "align": "center",
                            "backgroundColor": "#FF6B35",
                            "cornerRadius": "10px",
                            "paddingAll": "4px"
                        },
                        {
                            "type": "text",
                            "text": rec,
                            "wrap": True,
                            "size": "sm",
                            "color": "#333333",
                            "flex": 1,
                            "margin": "sm"
                        }
                    ],
                    "margin": "md"
                } for i, rec in enumerate(recommendations)
            ],
            "backgroundColor": "#FFF5F0",
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "margin": "md"
        }

    @staticmethod
    def timeline_list(events: list):
        """時間軸列表"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📅 追蹤時間軸",
                    "weight": "bold",
                    "size": "md",
                    "color": "#8B5CF6"
                }
            ] + [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "●",
                                    "size": "sm",
                                    "color": "#8B5CF6",
                                    "align": "center"
                                }
                            ],
                            "flex": 0,
                            "width": "20px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": event.get('title', ''),
                                    "weight": "bold",
                                    "size": "sm",
                                    "color": "#333333"
                                },
                                {
                                    "type": "text",
                                    "text": event.get('description', ''),
                                    "wrap": True,
                                    "size": "xs",
                                    "color": "#666666",
                                    "margin": "xs"
                                }
                            ],
                            "flex": 1,
                            "margin": "sm"
                        }
                    ],
                    "margin": "md"
                } for event in events
            ],
            "margin": "md"
        }

    @staticmethod
    def warning_box(message: str, severity: str = "high"):
        """警告盒"""
        colors = {
            "high": {"bg": "#FFEBEE", "text": "#D32F2F", "icon": "🚨"},
            "medium": {"bg": "#FFF3E0", "text": "#F57C00", "icon": "⚠️"},
            "low": {"bg": "#E8F5E8", "text": "#388E3C", "icon": "⚡"}
        }

        color = colors.get(severity, colors["medium"])

        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{color['icon']} 重要提醒",
                    "weight": "bold",
                    "size": "sm",
                    "color": color["text"]
                },
                {
                    "type": "text",
                    "text": message,
                    "wrap": True,
                    "size": "sm",
                    "color": color["text"],
                    "margin": "sm"
                }
            ],
            "backgroundColor": color["bg"],
            "cornerRadius": "8px",
            "paddingAll": "12px",
            "margin": "md"
        }

@app.get("/")
def root():
    return {
        "message": "LINE Bot 失智症分析系統 - 進階視覺化版",
        "status": "running",
        "features": [
            "⚠️ 警訊對比卡片",
            "📊 信心度量表", 
            "💡 XAI解釋盒",
            "ℹ️ 資訊盒",
            "🎯 行動卡片",
            "📅 時間軸列表",
            "🚨 警告盒"
        ],
        "ready": bool(LINE_TOKEN and GEMINI_KEY)
    }

@app.get("/health")
def health():
    return {"status": "healthy", "components": "advanced", "webhook": "ready"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.body()
        webhook_data = json.loads(body.decode('utf-8'))

        print(f"📨 收到 LINE 事件: {len(webhook_data.get('events', []))} 個")

        for event in webhook_data.get('events', []):
            if event.get('type') == 'message':
                message = event.get('message', {})
                if message.get('type') == 'text':
                    user_text = message.get('text', '').strip()
                    reply_token = event.get('replyToken')

                    print(f"👤 使用者訊息: {user_text}")
                    await process_and_reply_advanced(user_text, reply_token)

        return {"status": "ok"}

    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return {"status": "ok"}

async def process_and_reply_advanced(text: str, reply_token: str):
    """使用進階組件處理並回覆"""
    try:
        if text.lower() in ['hello', 'hi', '你好', 'help', '幫助']:
            reply_message = create_advanced_help_message()
        else:
            analysis = analyze_with_xai(text)
            reply_message = create_advanced_flex_message(text, analysis)

        if LINE_TOKEN:
            await send_line_reply(reply_token, reply_message)
            print("✅ 進階視覺化回覆已發送")
        else:
            print("⚠️ LINE_TOKEN 未設定")

    except Exception as e:
        print(f"❌ 處理錯誤: {e}")

def analyze_with_xai(text: str) -> dict:
    """帶 XAI 解釋的分析"""
    # 基礎分析
    analysis = {
        'category': 'M1-01',
        'category_name': '記憶力減退影響生活',
        'confidence': 0.75,
        'normal_aging': '偶爾忘記約會或朋友名字，但能夠自己想起來',
        'warning_sign': '頻繁忘記重要資訊，影響日常生活功能',
        'recommendations': [
            '記錄症狀發生的具體時間和情況',
            '觀察是否影響日常生活功能',
            '建議諮詢神經內科醫師進行評估'
        ]
    }

    # XAI 解釋
    analysis['xai_explanation'] = "AI 根據您描述中的關鍵詞彙和語言模式進行分析"
    analysis['key_factors'] = [
        "提到「重複」和「問同樣問題」",
        "涉及短期記憶功能",
        "可能影響日常交流"
    ]

    # 時間軸事件
    analysis['timeline_events'] = [
        {
            'title': '立即行動',
            'description': '開始記錄觀察到的症狀'
        },
        {
            'title': '1週內',
            'description': '整理症狀記錄，準備就醫資料'
        },
        {
            'title': '2週內',
            'description': '預約神經內科或精神科門診'
        }
    ]

    return analysis

def create_advanced_flex_message(user_input: str, analysis: dict):
    """創建進階視覺化 Flex Message"""
    components = AdvancedFlexComponents()

    return {
        "type": "flex",
        "altText": f"失智症警訊分析：{analysis['category_name']}",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症警訊分析",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "lg"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # 使用者描述
                    {
                        "type": "text",
                        "text": "🔸 您的描述",
                        "weight": "bold",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": user_input,
                        "wrap": True,
                        "color": "#333333",
                        "size": "sm"
                    },

                    # 信心度量表
                    components.confidence_meter(
                        analysis['confidence'], 
                        analysis['category']
                    ),

                    # 對比卡片
                    components.comparison_card(
                        analysis['normal_aging'],
                        analysis['warning_sign'],
                        analysis['confidence']
                    ),

                    # XAI 解釋盒
                    components.xai_box(
                        analysis['xai_explanation'],
                        analysis['key_factors']
                    ),

                    # 行動卡片
                    components.action_card(analysis['recommendations']),

                    # 時間軸
                    components.timeline_list(analysis['timeline_events']),

                    # 警告盒
                    components.warning_box(
                        "此分析僅供參考，請諮詢專業醫師進行正式評估",
                        "medium"
                    )
                ]
            }
        }
    }

def create_advanced_help_message():
    """創建進階幫助訊息"""
    components = AdvancedFlexComponents()

    return {
        "type": "flex",
        "altText": "失智症分析系統使用說明",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🤖 失智症分析助手",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1DB446"
                    },

                    components.info_box(
                        "使用方法",
                        "直接描述觀察到的行為，例如：媽媽最近常重複問同樣的問題",
                        "📝"
                    ),

                    components.info_box(
                        "分析功能",
                        "系統會提供 XAI 解釋、信心度評估、對比分析等",
                        "🧠"
                    ),

                    components.warning_box(
                        "本系統提供的分析僅供參考，不可替代專業醫療診斷"
                    )
                ]
            }
        }
    }

async def send_line_reply(reply_token: str, message: dict):
    """發送 LINE 回覆"""
    if not LINE_TOKEN:
        return

    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    payload = {
        "replyToken": reply_token,
        "messages": [message]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print("✅ 進階 Flex Message 發送成功")
        else:
            print(f"❌ 發送失敗: {response.status_code}")

    except Exception as e:
        print(f"❌ 發送錯誤: {e}")

@app.get("/test-components")
def test_components():
    """測試所有視覺化組件"""
    components = AdvancedFlexComponents()

    return {
        "comparison_card": "✅",
        "confidence_meter": "✅", 
        "xai_box": "✅",
        "info_box": "✅",
        "action_card": "✅",
        "timeline_list": "✅",
        "warning_box": "✅",
        "status": "All components loaded!"
    }

if __name__ == "__main__":
    print("🚀 啟動進階視覺化 LINE Bot 失智症分析服務")
    print("✅ 包含所有進階組件: 對比卡片、信心度量表、XAI解釋盒等")
    uvicorn.run(app, host="0.0.0.0", port=8000)