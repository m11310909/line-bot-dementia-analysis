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

@app.get("/")
def root():
    return {
        "message": "LINE Bot 失智症分析系統 - 完整版",
        "status": "running",
        "features": ["接收訊息 ✅", "分析功能 ✅", "Flex Message ✅", "LINE 回覆 ✅"],
        "ready_to_reply": bool(LINE_TOKEN),
        "ai_ready": bool(GEMINI_KEY)
    }

@app.get("/health")
def health():
    return {"status": "healthy", "webhook": "connected", "line_api": bool(LINE_TOKEN)}

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
                    print(f"🔄 Reply Token: {reply_token}")
                    
                    # 分析並回覆
                    await process_and_reply(user_text, reply_token)
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Webhook 錯誤: {e}")
        return {"status": "ok"}

async def process_and_reply(text: str, reply_token: str):
    """處理訊息並回覆"""
    try:
        # 特殊指令處理
        if text.lower() in ['hello', 'hi', '你好', 'help', '幫助']:
            reply_message = create_help_message()
        else:
            # 失智症分析
            analysis = analyze_dementia_symptoms(text)
            reply_message = create_analysis_flex_message(text, analysis)
        
        # 發送回覆
        if LINE_TOKEN:
            await send_line_reply(reply_token, reply_message)
            print("✅ 回覆已發送")
        else:
            print("⚠️ LINE_TOKEN 未設定，無法發送回覆")
            
    except Exception as e:
        print(f"❌ 處理錯誤: {e}")

def analyze_dementia_symptoms(text: str) -> dict:
    """失智症症狀分析"""
    categories = {
        'M1-01': {
            'name': '記憶力減退影響生活',
            'keywords': ['忘記', '記不住', '重複問', '健忘', '記憶'],
            'normal_aging': '偶爾忘記約會或朋友名字，但能夠自己想起來',
            'warning': '頻繁忘記重要資訊，影響日常生活功能'
        },
        'M1-02': {
            'name': '計劃事情或解決問題有困難',
            'keywords': ['計劃', '安排', '困難', '不會', '想不出'],
            'normal_aging': '偶爾需要幫助操作微波爐設定',
            'warning': '無法制定和執行計劃，處理數字有困難'
        },
        'M1-03': {
            'name': '無法勝任原本熟悉的事務',
            'keywords': ['熟悉', '不會用', '做不到', '操作', '家電'],
            'normal_aging': '偶爾需要幫助記錄電視節目',
            'warning': '無法完成原本熟悉的工作或家務'
        },
        'M1-04': {
            'name': '對時間地點感到混淆',
            'keywords': ['迷路', '時間', '地點', '混淆', '不知道在哪'],
            'normal_aging': '偶爾忘記今天是星期幾',
            'warning': '在熟悉的地方迷路，不知道時間、日期或季節'
        },
        'M1-08': {
            'name': '判斷力變差或減弱',
            'keywords': ['判斷', '決定', '奇怪', '不合理'],
            'normal_aging': '偶爾做出不好的決定',
            'warning': '判斷力明顯變差，容易受騙或做出不當決定'
        },
        'M1-10': {
            'name': '情緒和個性的改變',
            'keywords': ['脾氣', '個性', '改變', '易怒', '憂鬱'],
            'normal_aging': '當打破常規時會感到易怒',
            'warning': '個性明顯改變，變得困惑、多疑、憂鬱或易怒'
        }
    }
    
    # 分析文本匹配最佳類別
    best_match = None
    max_score = 0
    
    for category_id, info in categories.items():
        score = sum(1 for keyword in info['keywords'] if keyword in text)
        if score > max_score:
            max_score = score
            best_match = category_id
    
    if not best_match:
        best_match = 'M1-01'  # 預設分類
        max_score = 0.3
    
    return {
        'category': best_match,
        'category_name': categories[best_match]['name'],
        'confidence': min(max_score * 0.3 + 0.4, 0.9),
        'normal_aging': categories[best_match]['normal_aging'],
        'warning_sign': categories[best_match]['warning'],
        'recommendations': [
            '持續觀察症狀變化頻率',
            '記錄具體發生的情況',
            '如症狀持續建議諮詢醫師'
        ]
    }

def create_help_message():
    """創建幫助訊息"""
    return {
        "type": "text",
        "text": """🤖 失智症早期警訊分析助手

📝 使用方法：
直接描述觀察到的行為，例如：
- 媽媽最近常重複問同樣的問題
- 爸爸忘記回家的路
- 奶奶不會用原本熟悉的家電

🎯 分析範圍：
本系統可分析失智症十大警訊：
- M1-01: 記憶力減退影響生活
- M1-02: 計劃事情或解決問題有困難
- M1-03: 無法勝任原本熟悉的事務
- M1-04: 對時間地點感到混淆
- M1-05: 視覺影像和空間關係問題
- M1-06: 言語表達或書寫困難
- M1-07: 物品擺放錯亂
- M1-08: 判斷力變差或減弱
- M1-09: 從工作或社交活動中退出
- M1-10: 情緒和個性的改變

⚠️ 重要提醒：
此分析僅供參考，如有疑慮請諮詢專業醫師進行詳細評估。"""
    }

def create_analysis_flex_message(user_input: str, analysis: dict):
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
                        "text": "🧠 失智症警訊分析",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": f"{confidence_emoji} 信心度: {analysis['confidence']:.0%}",
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
                        "text": user_input[:150] + ("..." if len(user_input) > 150 else ""),
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

async def send_line_reply(reply_token: str, message: dict):
    """發送 LINE 回覆訊息"""
    if not LINE_TOKEN:
        print("❌ LINE_TOKEN 未設定")
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
            print("✅ LINE 回覆發送成功")
        else:
            print(f"❌ LINE 回覆失敗: {response.status_code}, {response.text}")
            
    except Exception as e:
        print(f"❌ 發送回覆錯誤: {e}")

@app.get("/test-analysis")
def test_analysis():
    """測試分析功能"""
    test_cases = [
        "媽媽最近常重複問同樣的問題",
        "爸爸不會用原本熟悉的洗衣機", 
        "奶奶經常迷路找不到回家的路",
        "爺爺的脾氣變得很暴躁"
    ]
    
    results = []
    for case in test_cases:
        analysis = analyze_dementia_symptoms(case)
        results.append({
            "input": case,
            "analysis": analysis
        })
    
    return {"test_results": results}

if __name__ == "__main__":
    print("🚀 啟動完整版 LINE Bot 失智症分析服務")
    print("✅ 功能: 接收訊息 + 分析 + Flex Message 回覆")
    uvicorn.run(app, host="0.0.0.0", port=8000)
