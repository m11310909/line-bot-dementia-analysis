"""
使用者回饋收集整合系統
階段四任務 7.3：使用者回饋收集整合
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import json
import os
from datetime import datetime
import uuid

class FeedbackType(str, Enum):
    RATING = "rating"
    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    BOOLEAN = "boolean"

class FeedbackPoint(str, Enum):
    AFTER_AI_RESPONSE = "after_ai_response"
    AFTER_VISUAL_EXPLANATION = "after_visual_explanation"
    SESSION_END = "session_end"
    ERROR_ENCOUNTERED = "error_encountered"
    MODULE_SWITCH = "module_switch"

class FeedbackCollector:
    """整合使用者回饋到對話流程"""
    
    FEEDBACK_POINTS = {
        FeedbackPoint.AFTER_AI_RESPONSE: {
            'message': '這個資訊對您有幫助嗎？',
            'type': FeedbackType.MULTIPLE_CHOICE,
            'options': ['很有幫助', '還可以', '看不懂'],
            'follow_up': {
                '很有幫助': None,
                '還可以': '哪個部分需要更清楚說明？',
                '看不懂': '我換個方式說明'
            },
            'collect_details': False,
            'trigger_condition': 'confidence > 0.7'
        },
        FeedbackPoint.AFTER_VISUAL_EXPLANATION: {
            'message': '圖表說明清楚嗎？',
            'type': FeedbackType.MULTIPLE_CHOICE,
            'options': ['清楚', '太複雜', '需要文字說明'],
            'follow_up': {
                '清楚': None,
                '太複雜': '您希望簡化哪個部分？',
                '需要文字說明': '我提供文字版本'
            },
            'collect_details': True,
            'trigger_condition': 'visual_explanation_shown'
        },
        FeedbackPoint.SESSION_END: {
            'message': '整體使用體驗評分',
            'type': FeedbackType.RATING,
            'scale': 5,
            'optional_comment': True,
            'follow_up': {
                '1-2': '請告訴我們如何改善',
                '3': '有什麼建議嗎？',
                '4-5': '謝謝您的回饋！'
            },
            'trigger_condition': 'session_duration > 5_minutes'
        },
        FeedbackPoint.ERROR_ENCOUNTERED: {
            'message': '遇到問題了嗎？',
            'type': FeedbackType.BOOLEAN,
            'options': ['是', '否'],
            'follow_up': {
                '是': '請描述遇到的問題',
                '否': '謝謝您的確認'
            },
            'collect_details': True,
            'trigger_condition': 'error_occurred'
        },
        FeedbackPoint.MODULE_SWITCH: {
            'message': '模組切換順利嗎？',
            'type': FeedbackType.MULTIPLE_CHOICE,
            'options': ['順利', '有點困難', '找不到'],
            'follow_up': {
                '順利': None,
                '有點困難': '哪個部分需要改善？',
                '找不到': '我提供更清楚的指引'
            },
            'collect_details': False,
            'trigger_condition': 'module_switched'
        }
    }
    
    def __init__(self, storage_path: str = "feedback_data"):
        self.storage_path = storage_path
        self.feedback_history = []
        self.session_data = {}
        
        # 確保儲存目錄存在
        os.makedirs(storage_path, exist_ok=True)
    
    def should_collect_feedback(self, feedback_point: str, context: dict = None) -> bool:
        """判斷是否應該收集回饋"""
        
        if feedback_point not in self.FEEDBACK_POINTS:
            return False
        
        feedback_config = self.FEEDBACK_POINTS[feedback_point]
        trigger_condition = feedback_config.get('trigger_condition', 'always')
        
        # 簡單的條件判斷
        if trigger_condition == 'always':
            return True
        elif trigger_condition == 'confidence > 0.7':
            confidence = context.get('confidence', 0.0) if context else 0.0
            return confidence > 0.7
        elif trigger_condition == 'visual_explanation_shown':
            return context.get('visual_shown', False) if context else False
        elif trigger_condition == 'session_duration > 5_minutes':
            session_duration = context.get('session_duration', 0) if context else 0
            return session_duration > 300  # 5 分鐘 = 300 秒
        elif trigger_condition == 'error_occurred':
            return context.get('error_occurred', False) if context else False
        elif trigger_condition == 'module_switched':
            return context.get('module_switched', False) if context else False
        
        return True
    
    def insert_feedback_request(self, feedback_point: str, context: dict = None) -> Dict[str, Any]:
        """在對話適當時機插入回饋請求"""
        
        if not self.should_collect_feedback(feedback_point, context):
            return None
        
        feedback_config = self.FEEDBACK_POINTS[feedback_point]
        
        # 生成回饋請求
        feedback_request = {
            "id": str(uuid.uuid4()),
            "type": feedback_point,
            "message": feedback_config['message'],
            "feedback_type": feedback_config['type'],
            "options": feedback_config.get('options', []),
            "scale": feedback_config.get('scale', 5),
            "optional_comment": feedback_config.get('optional_comment', False),
            "follow_up": feedback_config.get('follow_up', {}),
            "collect_details": feedback_config.get('collect_details', False),
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }
        
        # 生成 Flex Message
        flex_message = self._create_feedback_flex_message(feedback_request)
        feedback_request["flex_message"] = flex_message
        
        return feedback_request
    
    def _create_feedback_flex_message(self, feedback_request: dict) -> Dict[str, Any]:
        """創建回饋收集的 Flex Message"""
        
        feedback_type = feedback_request["feedback_type"]
        message = feedback_request["message"]
        
        if feedback_type == FeedbackType.RATING:
            return self._create_rating_flex_message(message, feedback_request["scale"])
        elif feedback_type == FeedbackType.MULTIPLE_CHOICE:
            return self._create_multiple_choice_flex_message(message, feedback_request["options"])
        elif feedback_type == FeedbackType.BOOLEAN:
            return self._create_boolean_flex_message(message, feedback_request["options"])
        else:
            return self._create_text_feedback_flex_message(message)
    
    def _create_rating_flex_message(self, message: str, scale: int) -> Dict[str, Any]:
        """創建評分回饋 Flex Message"""
        
        rating_buttons = []
        for i in range(1, scale + 1):
            rating_buttons.append({
                "type": "action",
                "action": {
                    "type": "message",
                    "label": str(i),
                    "text": f"評分：{i}分"
                }
            })
        
        return {
            "type": "flex",
            "altText": message,
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 回饋收集",
                            "weight": "bold",
                            "color": "#4A90E2",
                            "size": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": message,
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": rating_buttons
                        }
                    ]
                }
            }
        }
    
    def _create_multiple_choice_flex_message(self, message: str, options: List[str]) -> Dict[str, Any]:
        """創建多選回饋 Flex Message"""
        
        choice_buttons = []
        for option in options:
            choice_buttons.append({
                "type": "action",
                "action": {
                    "type": "message",
                    "label": option,
                    "text": f"回饋：{option}"
                }
            })
        
        return {
            "type": "flex",
            "altText": message,
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 回饋收集",
                            "weight": "bold",
                            "color": "#4A90E2",
                            "size": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": message,
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": choice_buttons[:3]  # 最多顯示 3 個選項
                        }
                    ]
                }
            }
        }
    
    def _create_boolean_flex_message(self, message: str, options: List[str]) -> Dict[str, Any]:
        """創建布林回饋 Flex Message"""
        
        return {
            "type": "flex",
            "altText": message,
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 回饋收集",
                            "weight": "bold",
                            "color": "#4A90E2",
                            "size": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": message,
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "action",
                                    "action": {
                                        "type": "message",
                                        "label": options[0],
                                        "text": f"回饋：{options[0]}"
                                    }
                                },
                                {
                                    "type": "action",
                                    "action": {
                                        "type": "message",
                                        "label": options[1],
                                        "text": f"回饋：{options[1]}"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    
    def _create_text_feedback_flex_message(self, message: str) -> Dict[str, Any]:
        """創建文字回饋 Flex Message"""
        
        return {
            "type": "flex",
            "altText": message,
            "contents": {
                "type": "bubble",
                "size": "kilo",
                "header": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 回饋收集",
                            "weight": "bold",
                            "color": "#4A90E2",
                            "size": "sm"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": message,
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666"
                        }
                    ]
                }
            }
        }
    
    def process_feedback_response(self, feedback_id: str, response: str, user_id: str = None) -> Dict[str, Any]:
        """處理使用者回饋回應"""
        
        # 記錄回饋
        feedback_record = {
            "feedback_id": feedback_id,
            "user_id": user_id,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
        self.feedback_history.append(feedback_record)
        
        # 儲存到檔案
        self._save_feedback(feedback_record)
        
        # 分析回饋並生成後續行動
        follow_up_action = self._analyze_feedback_response(feedback_id, response)
        
        return {
            "feedback_processed": True,
            "follow_up_action": follow_up_action,
            "feedback_record": feedback_record
        }
    
    def _analyze_feedback_response(self, feedback_id: str, response: str) -> Dict[str, Any]:
        """分析回饋回應並生成後續行動"""
        
        # 這裡可以實作更複雜的回饋分析邏輯
        if "很有幫助" in response or "清楚" in response:
            return {
                "action": "positive_feedback",
                "message": "謝謝您的回饋！",
                "next_step": "continue_conversation"
            }
        elif "還可以" in response or "有點困難" in response:
            return {
                "action": "neutral_feedback",
                "message": "我們會持續改善，謝謝您的建議！",
                "next_step": "offer_improvement"
            }
        elif "看不懂" in response or "太複雜" in response:
            return {
                "action": "negative_feedback",
                "message": "我換個方式說明",
                "next_step": "simplify_explanation"
            }
        else:
            return {
                "action": "general_feedback",
                "message": "謝謝您的回饋！",
                "next_step": "continue_conversation"
            }
    
    def _save_feedback(self, feedback_record: dict):
        """儲存回饋到檔案"""
        
        filename = f"{self.storage_path}/feedback_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(json.dumps(feedback_record, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"儲存回饋失敗: {e}")
    
    def get_feedback_stats(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """獲取回饋統計"""
        
        # 讀取回饋檔案
        feedback_data = []
        for filename in os.listdir(self.storage_path):
            if filename.startswith("feedback_") and filename.endswith(".jsonl"):
                filepath = os.path.join(self.storage_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                feedback_data.append(json.loads(line.strip()))
                except Exception as e:
                    print(f"讀取回饋檔案失敗 {filename}: {e}")
        
        # 計算統計
        total_feedback = len(feedback_data)
        positive_feedback = len([f for f in feedback_data if "很有幫助" in f.get("response", "")])
        negative_feedback = len([f for f in feedback_data if "看不懂" in f.get("response", "")])
        
        return {
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "negative_feedback": negative_feedback,
            "neutral_feedback": total_feedback - positive_feedback - negative_feedback,
            "satisfaction_rate": positive_feedback / total_feedback if total_feedback > 0 else 0.0
        }

# 使用範例
def example_usage():
    """回饋收集系統使用範例"""
    
    # 創建回饋收集器
    collector = FeedbackCollector()
    
    # 模擬上下文
    context = {
        "confidence": 0.8,
        "visual_shown": True,
        "session_duration": 600,  # 10 分鐘
        "module_switched": True
    }
    
    # 測試回饋請求
    feedback_request = collector.insert_feedback_request(
        FeedbackPoint.AFTER_AI_RESPONSE,
        context
    )
    
    if feedback_request:
        print("回饋請求:", feedback_request)
        
        # 模擬處理回饋回應
        result = collector.process_feedback_response(
            feedback_request["id"],
            "很有幫助",
            "user123"
        )
        
        print("回饋處理結果:", result)
    
    # 獲取統計
    stats = collector.get_feedback_stats()
    print("回饋統計:", stats)
    
    return feedback_request

if __name__ == "__main__":
    example_usage() 