from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
import os
import httpx

app = FastAPI(title="LINE Bot 失智症分析系統", version="1.0")

# 環境變數
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

@app.get("/")
def root():
    return {
        "message": "LINE Bot 失智症分析系統",
        "status": "✅ 運行中",
        "line_token": "✅ 已設定" if LINE_TOKEN else "❌ 未設定",
        "real_reply": "✅ 啟用" if LINE_TOKEN else "❌ 需要 TOKEN"
    }

@app.post("/webhook")
async def webhook(request: Request):
    try:
        print("=" * 50)
        print("📨 收到 LINE Webhook 請求")
        
        body = await request.body()
        webhook_data = json.loads(body.decode('utf-8'))
        
        events = webhook_data.get('events', [])
        print(f"🎯 處理 {len(events)} 個事件")
        
        for event in events:
            if event.get('type') == 'message':
                message = event.get('message', {})
                if message.get('type') == 'text':
                    user_text = message.get('text', '').strip()
                    reply_token = event.get('replyToken', '')
                    
                    print(f"👤 使用者訊息: '{user_text}'")
                    print(f"🔄 Reply Token: {reply_token}")
                    
                    # 處理訊息並發送真實回覆
                    await process_and_send_real_reply(user_text, reply_token)
        
        print("✅ Webhook 處理完成")
        print("=" * 50)
        
        return JSONResponse(status_code=200, content={"status": "ok"})
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return JSONResponse(status_code=200, content={"status": "ok"})

async def process_and_send_real_reply(text: str, reply_token: str):
    """處理訊息並發送真實回覆"""
    try:
        # 分析訊息
        if text.lower() in ['hello', 'hi', '你好', 'help', '幫助']:
            print("📋 生成幫助訊息")
            response = create_help_response()
        else:
            print("🧠 執行失智症分析...")
            analysis = analyze_symptoms(text)
            response = create_flex_message(text, analysis)
            print(f"📊 分析結果: {analysis['category']} (信心度: {analysis['confidence']:.0%})")
        
        # 發送真實回覆
        if LINE_TOKEN and reply_token:
            success = await send_line_reply(reply_token, response)
            if success:
                print("🎉 真實回覆發送成功！用戶已收到訊息")
            else:
                print("❌ 真實回覆發送失敗")
        else:
            print("⚠️ 無法發送回覆：LINE_TOKEN 或 reply_token 缺失")
            
    except Exception as e:
        print(f"❌ 處理錯誤: {e}")

def analyze_symptoms(text: str) -> dict:
    """失智症症狀分析"""
    categories = {
        'M1-01': {
            'name': '記憶力減退影響生活',
            'keywords': ['忘記', '記不住', '重複問', '健忘', '記憶'],
            'normal': '偶爾忘記約會或朋友名字，但能夠自己想起來',
            'warning': '頻繁忘記重要資訊，影響日常生活功能'
        },
        'M1-03': {
            'name': '無法勝任原本熟悉的事務',
            'keywords': ['熟悉', '不會用', '做不到', '操作', '家電'],
            'normal': '偶爾需要幫助記錄電視節目',
            'warning': '無法完成原本熟悉的工作或家務'
        },
        'M1-04': {
            'name': '對時間地點感到混淆',
            'keywords': ['迷路', '時間', '地點', '混淆', '不知道在哪'],
            'normal': '偶爾忘記今天是星期幾',
            'warning': '在熟悉的地方迷路，不知道時間、日期或季節'
        }
    }
    
    # 分析匹配
    best_match = 'M1-01'
    max_score = 0
    
    for category_id, info in categories.items():
        score = sum(1 for keyword in info['keywords'] if keyword in text)
        if score > max_score:
            max_score = score
            best_match = category_id
    
    confidence = min(max_score * 0.25 + 0.5, 0.9) if max_score > 0 else 0.75
    category_info = categories[best_match]
    
    return {
        'category': best_match,
        'category_name': category_info['name'],
        'confidence': confidence,
        'normal_aging': category_info['normal'],
        'warning_sign': category_info['warning'],
        'recommendations': [
            '持續觀察症狀變化的頻率和嚴重度',
            '記錄具體發生的時間和情況',
            '如症狀持續或加重，建議諮詢神經內科醫師'
        ]
    }

def create_help_response():
    """創建幫助回應"""
    return {
        "type": "text",
        "text": """🤖 失智症早期警訊分析助手

📝 使用方法：
直接描述觀察到的行為變化，例如：
- 媽媽最近常重複問同樣的問題
- 爸爸忘記回家的路
- 奶奶不會用原本熟悉的家電

🎯 本系統可分析失智症十大警訊並提供專業建議

⚠️ 重要提醒：此分析僅供參考，請諮詢專業醫師"""
    }

def create_flex_message(user_input: str, analysis: dict):
    """創建 Flex Message"""
    confidence_emoji = "🟢" if analysis['confidence'] > 0.7 else "🟡"
    
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
                        "text": "🧠 失智症警訊分析結果",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": f"{confidence_emoji} 分析信心度: {analysis['confidence']:.0%}",
                        "size": "sm",
                        "color": "#666666"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
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
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": f"⚠️ 警訊類別: {analysis['category']}",
                        "weight": "bold",
                        "color": "#FF5551",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": analysis['category_name'],
                        "wrap": True,
                        "color": "#FF5551",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "✅ 正常老化現象",
                        "weight": "bold",
                        "color": "#00B900",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": analysis['normal_aging'],
                        "wrap": True,
                        "color": "#00B900",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "🔍 警訊特徵",
                        "weight": "bold",
                        "color": "#FF5551",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": analysis['warning_sign'],
                        "wrap": True,
                        "color": "#FF5551",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "💡 建議事項",
                        "weight": "bold",
                        "color": "#1DB446",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "1. " + analysis['recommendations'][0],
                        "wrap": True,
                        "size": "sm",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": "2. " + analysis['recommendations'][1],
                        "wrap": True,
                        "size": "sm",
                        "margin": "sm"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ 此分析僅供參考，如有疑慮請諮詢專業醫師",
                        "wrap": True,
                        "color": "#888888",
                        "size": "xs",
                        "margin": "md"
                    }
                ]
            }
        }
    }

async def send_line_reply(reply_token: str, message: dict) -> bool:
    """發送 LINE 回覆"""
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
            print("✅ LINE API 回覆成功")
            return True
        else:
            print(f"❌ LINE API 失敗: {response.status_code}")
            print(f"錯誤詳情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 發送錯誤: {e}")
        return False

if __name__ == "__main__":
    print("🚀 啟動真實回覆版 LINE Bot")
    print(f"🔑 LINE Token: {'已設定' if LINE_TOKEN else '❌ 未設定'}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
