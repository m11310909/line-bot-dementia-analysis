from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
import os
import asyncio

app = FastAPI(title="LINE Bot 失智症分析系統", version="1.0")

# 環境變數
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

@app.get("/")
def root():
    return {
        "message": "LINE Bot 失智症分析系統",
        "status": "✅ 運行中",
        "features": ["Webhook 接收", "失智症分析", "Flex Message"],
        "line_token": "✅ 已設定" if LINE_TOKEN else "❌ 未設定",
        "webhook_url": "請設定為: /webhook"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "ready": True}

@app.post("/webhook")
async def webhook(request: Request):
    """LINE Bot Webhook 端點"""
    try:
        print("=" * 50)
        print("📨 收到 LINE Webhook 請求")
        
        # 讀取請求內容
        body = await request.body()
        webhook_data = json.loads(body.decode('utf-8'))
        
        events = webhook_data.get('events', [])
        print(f"🎯 處理 {len(events)} 個事件")
        
        # 處理每個事件
        for event in events:
            event_type = event.get('type', 'unknown')
            print(f"📋 事件類型: {event_type}")
            
            if event_type == 'message':
                message = event.get('message', {})
                if message.get('type') == 'text':
                    user_text = message.get('text', '').strip()
                    reply_token = event.get('replyToken', '')
                    
                    print(f"👤 使用者訊息: '{user_text}'")
                    print(f"🔄 Reply Token: {reply_token}")
                    
                    # 處理訊息
                    await process_message(user_text, reply_token)
        
        print("✅ Webhook 處理完成")
        print("=" * 50)
        
        # 必須回傳 200
        return JSONResponse(
            status_code=200,
            content={"status": "ok", "message": "processed"}
        )
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": str(e)}
        )

async def process_message(text: str, reply_token: str):
    """處理使用者訊息"""
    try:
        # 分析訊息類型
        if text.lower() in ['hello', 'hi', '你好', 'help', '幫助']:
            print("📋 回應: 幫助訊息")
            response = create_help_response()
        else:
            print("🧠 執行失智症分析...")
            analysis = analyze_symptoms(text)
            response = create_analysis_response(text, analysis)
            print(f"📊 分析結果: {analysis['category']} (信心度: {analysis['confidence']:.0%})")
        
        # 如果有 LINE_TOKEN，發送回覆
        if LINE_TOKEN and reply_token:
            await send_real_reply(reply_token, response)
        else:
            print("⚠️ 無法發送回覆 (TOKEN 或 reply_token 缺失)")
            
    except Exception as e:
        print(f"❌ 訊息處理錯誤: {e}")

def analyze_symptoms(text: str) -> dict:
    """失智症症狀分析"""
    # 定義警訊類別和關鍵字
    categories = {
        'M1-01': {
            'name': '記憶力減退影響生活',
            'keywords': ['忘記', '記不住', '重複問', '健忘', '記憶'],
            'normal': '偶爾忘記約會或朋友名字，但能夠自己想起來',
            'warning': '頻繁忘記重要資訊，影響日常生活功能'
        },
        'M1-02': {
            'name': '計劃事情或解決問題有困難',
            'keywords': ['計劃', '安排', '困難', '不會', '想不出'],
            'normal': '偶爾需要幫助操作微波爐設定',
            'warning': '無法制定和執行計劃，處理數字有困難'
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
        },
        'M1-10': {
            'name': '情緒和個性的改變',
            'keywords': ['脾氣', '個性', '改變', '易怒', '憂鬱'],
            'normal': '當打破常規時會感到易怒',
            'warning': '個性明顯改變，變得困惑、多疑、憂鬱或易怒'
        }
    }
    
    # 分析匹配度
    best_match = 'M1-01'
    max_score = 0
    
    for category_id, info in categories.items():
        score = sum(1 for keyword in info['keywords'] if keyword in text)
        if score > max_score:
            max_score = score
            best_match = category_id
    
    # 計算信心度
    confidence = min(max_score * 0.25 + 0.5, 0.9) if max_score > 0 else 0.6
    
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

🎯 分析範圍：
本系統可分析失智症十大警訊：
- M1-01: 記憶力減退影響生活
- M1-02: 計劃事情或解決問題有困難
- M1-03: 無法勝任原本熟悉的事務
- M1-04: 對時間地點感到混淆
- M1-10: 情緒和個性的改變

⚠️ 重要提醒：
此分析僅供參考，如有疑慮請諮詢專業醫師進行詳細評估。"""
    }

def create_analysis_response(user_input: str, analysis: dict):
    """創建分析結果的 Flex Message"""
    confidence_emoji = "🟢" if analysis['confidence'] > 0.7 else "🟡" if analysis['confidence'] > 0.4 else "🔴"
    
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
                        "color": "#666666",
                        "margin": "sm"
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
                        "text": user_input[:100] + ("..." if len(user_input) > 100 else ""),
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
                    }
                ] + [
                    {
                        "type": "text",
                        "text": f"{i+1}. {rec}",
                        "wrap": True,
                        "size": "sm",
                        "color": "#333333",
                        "margin": "sm"
                    } for i, rec in enumerate(analysis['recommendations'])
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

async def send_real_reply(reply_token: str, message: dict):
    """發送 LINE 回覆 (模擬)"""
    print(f"📤 模擬發送 LINE 回覆 (Token: {reply_token[:20]}...)")
    print(f"📝 訊息類型: {message['type']}")
    # 這裡可以加入實際的 LINE API 調用
    print("✅ 回覆發送完成 (模擬)")

if __name__ == "__main__":
    print("🚀 啟動 LINE Bot 失智症分析系統")
    print("✅ 功能: Webhook + 分析 + Flex Message")
    print(f"🔑 LINE Token: {'已設定' if LINE_TOKEN else '未設定'}")
    uvicorn.run(app, host="0.0.0.0", port=8000)

# 在檔案末尾加入真實的 LINE API 調用
import httpx

async def send_real_reply(reply_token: str, message: dict):
    """發送真實的 LINE 回覆"""
    if not LINE_TOKEN:
        print("⚠️ LINE_TOKEN 未設定，無法發送回覆")
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
            print("✅ LINE 回覆發送成功！")
        else:
            print(f"❌ LINE 回覆失敗: {response.status_code}, {response.text}")
            
    except Exception as e:
        print(f"❌ 發送回覆錯誤: {e}")

# 替換 send_real_reply 函數調用
# 將 await send_real_reply(reply_token, response) 
# 改為 await send_real_reply(reply_token, response)
