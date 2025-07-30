"""
Replit 部署版本的 LINE Bot
將此程式複製到你的 Replit 專案中
"""

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

# 從環境變數獲取設定
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# 初始化 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class M1M2M3AnalysisBot:
    """增強版失智症分析 Bot - Replit 版本"""
    
    def __init__(self):
        # M1+M2+M3 API 設定 - 指向你的本地 API
        # 注意：需要將 localhost 改為你的實際 IP 地址
        self.api_base_url = "http://YOUR_IP_HERE:8005"  # 請替換為實際 IP
        self.analysis_endpoint = f"{self.api_base_url}/comprehensive-analysis"
        
        # 如果本地 API 無法訪問，使用模擬模式
        self.use_simulation = True
        
        logger.info("🚀 Replit 版失智症分析 Bot 初始化完成")
    
    def analyze_symptoms(self, user_input: str) -> FlexSendMessage:
        """症狀分析函數"""
        
        try:
            if not self.use_simulation:
                # 嘗試連接本地 API
                response = requests.post(
                    self.analysis_endpoint,
                    json={"user_input": user_input},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_api_response(data)
            
            # 模擬模式 - 基於關鍵字的簡單分析
            return self._simulate_analysis(user_input)
            
        except Exception as e:
            logger.error(f"分析錯誤：{str(e)}")
            return self._simulate_analysis(user_input)
    
    def _simulate_analysis(self, user_input: str) -> FlexSendMessage:
        """模擬 M1+M2+M3 分析"""
        
        # 簡單的關鍵字匹配
        memory_keywords = ["忘記", "記憶", "健忘", "記不得"]
        paranoia_keywords = ["懷疑", "偷", "不信任", "害"]
        aggression_keywords = ["打人", "叫罵", "暴躁", "發脾氣"]
        sleep_keywords = ["睡不著", "失眠", "日夜顛倒", "不睡"]
        
        detected_symptoms = []
        suggestions = []
        
        # M1 記憶力檢測
        if any(keyword in user_input for keyword in memory_keywords):
            detected_symptoms.append("🚨 M1-01: 記憶力減退影響日常生活")
            suggestions.append("建議記錄忘記的事件模式")
        
        # M3 BPSD 檢測
        if any(keyword in user_input for keyword in paranoia_keywords):
            detected_symptoms.append("🧠 M3-01: 妄想症狀")
            suggestions.append("避免直接否定，提供安全感")
        
        if any(keyword in user_input for keyword in aggression_keywords):
            detected_symptoms.append("🧠 M3-03: 激動與攻擊行為")
            suggestions.append("保持冷靜，識別觸發因子")
        
        if any(keyword in user_input for keyword in sleep_keywords):
            detected_symptoms.append("🧠 M3-06: 睡眠障礙")
            suggestions.append("維持規律作息，增加白天光照")
        
        # 如果沒有匹配到，提供一般建議
        if not detected_symptoms:
            detected_symptoms.append("🔍 需要更詳細的症狀描述")
            suggestions.append("建議詳細記錄症狀並諮詢專業醫療人員")
        
        # 建立 Flex Message
        return FlexSendMessage(
            alt_text="失智症症狀分析結果",
            contents={
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "🧠 失智症症狀分析",
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
                            "text": "🔍 檢測結果",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#005073",
                            "margin": "md"
                        }
                    ] + [
                        {
                            "type": "text",
                            "text": symptom,
                            "size": "sm",
                            "margin": "xs",
                            "wrap": True
                        } for symptom in detected_symptoms
                    ] + [
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "💡 建議",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#005073",
                            "margin": "md"
                        }
                    ] + [
                        {
                            "type": "text",
                            "text": f"• {suggestion}",
                            "size": "xs",
                            "margin": "xs",
                            "wrap": True,
                            "color": "#666666"
                        } for suggestion in suggestions[:3]
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
    
    def _process_api_response(self, data: dict) -> FlexSendMessage:
        """處理 API 回應"""
        flex_message = data.get("flex_message")
        if flex_message:
            return FlexSendMessage(
                alt_text=flex_message.get("altText", "失智症分析結果"),
                contents=flex_message["contents"]
            )
        else:
            return self._simulate_analysis("一般症狀")

# 初始化分析機器人
analysis_bot = M1M2M3AnalysisBot()

@app.route("/webhook", methods=['POST'])
def webhook():
    """LINE Bot webhook"""
    
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理訊息"""
    
    user_message = event.message.text.strip()
    
    if len(user_message) < 3:
        reply_message = TextSendMessage(
            text="請描述更詳細的症狀，例如記憶力問題、行為改變等。"
        )
    else:
        reply_message = analysis_bot.analyze_symptoms(user_message)
    
    try:
        line_bot_api.reply_message(event.reply_token, reply_message)
    except LineBotApiError as e:
        logger.error(f"LINE Bot API 錯誤：{e}")

@app.route("/", methods=['GET'])
def index():
    return {
        "message": "失智症分析 LINE Bot - Replit 版本",
        "status": "running",
        "version": "3.0.0-replit"
    }

if __name__ == "__main__":
    print("🚀 啟動 Replit 版 LINE Bot...")
    app.run(host='0.0.0.0', port=3000)
