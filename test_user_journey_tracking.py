#!/usr/bin/env python3
"""
使用者歷程追蹤測試腳本
測試完整對話記錄與分析、個人化病程追蹤、智能提醒與預警、照護計畫建議
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

class UserJourneyTracker:
    """使用者歷程追蹤器"""
    
    def __init__(self, base_url: str = "http://localhost:8008"):
        self.base_url = base_url
        self.user_sessions = {}
        self.conversation_history = {}
        self.care_plans = {}
        
    def start_user_session(self, user_id: str) -> Dict[str, Any]:
        """開始使用者會話"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "user_id": user_id,
                "start_time": datetime.now(),
                "conversation_count": 0,
                "modules_used": [],
                "symptoms_detected": [],
                "care_needs": [],
                "last_interaction": None,
                "session_duration": 0
            }
            self.conversation_history[user_id] = []
            self.care_plans[user_id] = {
                "current_plan": None,
                "recommendations": [],
                "alerts": [],
                "progress_tracking": {}
            }
        
        return self.user_sessions[user_id]
    
    def log_conversation(self, user_id: str, message: str, response: Dict[str, Any]) -> None:
        """記錄對話"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # 分析回應中的模組
        module_detected = self._extract_module_from_response(response)
        
        # 記錄對話
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "bot_response": response,
            "module_detected": module_detected,
            "response_type": response.get("type", "unknown"),
            "confidence": self._extract_confidence(response)
        }
        
        self.conversation_history[user_id].append(conversation_entry)
        
        # 更新會話統計
        if user_id in self.user_sessions:
            self.user_sessions[user_id]["conversation_count"] += 1
            self.user_sessions[user_id]["last_interaction"] = datetime.now()
            if module_detected not in self.user_sessions[user_id]["modules_used"]:
                self.user_sessions[user_id]["modules_used"].append(module_detected)
    
    def _extract_module_from_response(self, response: Dict[str, Any]) -> str:
        """從回應中提取模組"""
        alt_text = response.get("altText", "")
        if "M1" in alt_text or "警訊分析" in alt_text:
            return "M1"
        elif "M2" in alt_text or "病程階段" in alt_text:
            return "M2"
        elif "M3" in alt_text or "BPSD" in alt_text:
            return "M3"
        elif "M4" in alt_text or "照護需求" in alt_text:
            return "M4"
        else:
            return "Unknown"
    
    def _extract_confidence(self, response: Dict[str, Any]) -> float:
        """從回應中提取信心度"""
        # 這裡可以根據實際的回應格式提取信心度
        return 0.8  # 預設值
    
    def analyze_user_journey(self, user_id: str) -> Dict[str, Any]:
        """分析使用者歷程"""
        if user_id not in self.conversation_history:
            return {"error": "No conversation history found"}
        
        conversations = self.conversation_history[user_id]
        session = self.user_sessions.get(user_id, {})
        
        # 分析模組使用模式
        module_usage = {}
        for conv in conversations:
            module = conv.get("module_detected", "Unknown")
            module_usage[module] = module_usage.get(module, 0) + 1
        
        # 分析對話主題
        topics = []
        for conv in conversations:
            message = conv.get("user_message", "").lower()
            if any(word in message for word in ["忘記", "記憶", "記不住"]):
                topics.append("記憶問題")
            elif any(word in message for word in ["妄想", "幻覺", "攻擊"]):
                topics.append("行為症狀")
            elif any(word in message for word in ["醫療", "醫生", "治療"]):
                topics.append("醫療需求")
            elif any(word in message for word in ["照顧", "協助", "幫助"]):
                topics.append("照護需求")
        
        # 計算會話持續時間
        if conversations:
            first_time = datetime.fromisoformat(conversations[0]["timestamp"])
            last_time = datetime.fromisoformat(conversations[-1]["timestamp"])
            session_duration = (last_time - first_time).total_seconds() / 60  # 分鐘
        else:
            session_duration = 0
        
        return {
            "user_id": user_id,
            "total_conversations": len(conversations),
            "session_duration_minutes": session_duration,
            "module_usage": module_usage,
            "topics_discussed": list(set(topics)),
            "most_used_module": max(module_usage.items(), key=lambda x: x[1])[0] if module_usage else "None",
            "conversation_flow": [conv["module_detected"] for conv in conversations],
            "average_confidence": sum(conv.get("confidence", 0) for conv in conversations) / len(conversations) if conversations else 0
        }
    
    def generate_care_plan(self, user_id: str) -> Dict[str, Any]:
        """生成照護計畫"""
        journey_analysis = self.analyze_user_journey(user_id)
        
        recommendations = []
        alerts = []
        
        # 根據模組使用情況生成建議
        module_usage = journey_analysis.get("module_usage", {})
        
        if module_usage.get("M1", 0) > 0:
            recommendations.append({
                "type": "warning",
                "title": "警訊監控",
                "description": "檢測到失智症警訊，建議定期監控症狀變化",
                "priority": "high"
            })
        
        if module_usage.get("M3", 0) > 0:
            recommendations.append({
                "type": "behavior",
                "title": "行為症狀管理",
                "description": "發現行為心理症狀，建議尋求專業醫療協助",
                "priority": "high"
            })
            alerts.append({
                "type": "urgent",
                "message": "檢測到行為症狀，建議立即諮詢精神科醫師",
                "timestamp": datetime.now().isoformat()
            })
        
        if module_usage.get("M4", 0) > 0:
            recommendations.append({
                "type": "care",
                "title": "照護資源",
                "description": "需要照護協助，建議聯繫相關社會資源",
                "priority": "medium"
            })
        
        # 根據對話頻率生成提醒
        total_conversations = journey_analysis.get("total_conversations", 0)
        if total_conversations > 5:
            recommendations.append({
                "type": "monitoring",
                "title": "定期追蹤",
                "description": "您已多次諮詢，建議建立定期追蹤機制",
                "priority": "medium"
            })
        
        return {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "recommendations": recommendations,
            "alerts": alerts,
            "next_follow_up": (datetime.now() + timedelta(days=7)).isoformat(),
            "care_plan_summary": {
                "total_recommendations": len(recommendations),
                "urgent_alerts": len([alert for alert in alerts if alert["type"] == "urgent"]),
                "priority_level": "high" if any(rec["priority"] == "high" for rec in recommendations) else "medium"
            }
        }
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """獲取使用者進度追蹤"""
        if user_id not in self.conversation_history:
            return {"error": "No user data found"}
        
        conversations = self.conversation_history[user_id]
        if not conversations:
            return {"error": "No conversations found"}
        
        # 分析進度
        first_conversation = conversations[0]
        latest_conversation = conversations[-1]
        
        # 計算模組進展
        module_progress = {}
        for i, conv in enumerate(conversations):
            module = conv.get("module_detected", "Unknown")
            if module not in module_progress:
                module_progress[module] = {"first_mention": i, "total_mentions": 0}
            module_progress[module]["total_mentions"] += 1
        
        return {
            "user_id": user_id,
            "first_interaction": first_conversation["timestamp"],
            "latest_interaction": latest_conversation["timestamp"],
            "total_interactions": len(conversations),
            "module_progress": module_progress,
            "engagement_level": self._calculate_engagement_level(conversations),
            "progress_summary": {
                "has_warning_signs": any(conv["module_detected"] == "M1" for conv in conversations),
                "has_behavioral_symptoms": any(conv["module_detected"] == "M3" for conv in conversations),
                "seeking_care": any(conv["module_detected"] == "M4" for conv in conversations),
                "consistent_engagement": len(conversations) > 3
            }
        }
    
    def _calculate_engagement_level(self, conversations: List[Dict]) -> str:
        """計算參與度等級"""
        if len(conversations) >= 5:
            return "high"
        elif len(conversations) >= 3:
            return "medium"
        else:
            return "low"

def test_user_journey_tracking():
    """測試使用者歷程追蹤功能"""
    
    base_url = "http://localhost:8008"
    tracker = UserJourneyTracker(base_url)
    
    print("🧪 使用者歷程追蹤測試")
    print("=" * 60)
    print("🎯 測試目標:")
    print("   • 完整對話記錄與分析")
    print("   • 個人化病程追蹤")
    print("   • 智能提醒與預警")
    print("   • 照護計畫建議")
    print("=" * 60)
    
    # 測試案例
    test_users = [
        {
            "user_id": "user_001",
            "name": "張媽媽的照護者",
            "conversations": [
                "媽媽忘記關瓦斯",
                "媽媽最近常重複問同樣的問題",
                "需要醫療協助",
                "媽媽中度失智",
                "爺爺有妄想症狀"
            ]
        },
        {
            "user_id": "user_002", 
            "name": "李爺爺的家人",
            "conversations": [
                "爺爺有妄想症狀",
                "需要照護資源",
                "爺爺有攻擊行為",
                "需要醫療協助",
                "爺爺晚上不睡覺"
            ]
        },
        {
            "user_id": "user_003",
            "name": "王奶奶的照護者",
            "conversations": [
                "奶奶有躁動不安",
                "需要社會支持",
                "奶奶忘記吃藥",
                "需要經濟協助"
            ]
        }
    ]
    
    for test_user in test_users:
        print(f"\n👤 測試使用者: {test_user['name']} ({test_user['user_id']})")
        print("-" * 50)
        
        # 開始使用者會話
        session = tracker.start_user_session(test_user["user_id"])
        print(f"✅ 開始會話: {session['start_time']}")
        
        # 模擬對話
        for i, message in enumerate(test_user["conversations"], 1):
            print(f"\n💬 對話 {i}: {message}")
            
            try:
                # 發送請求
                response = requests.post(
                    f"{base_url}/analyze",
                    json={"message": message, "user_id": test_user["user_id"]},
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 記錄對話
                    tracker.log_conversation(test_user["user_id"], message, data)
                    
                    # 顯示回應摘要
                    alt_text = data.get("altText", "")
                    print(f"   🤖 回應: {alt_text[:50]}...")
                    
                else:
                    print(f"   ❌ 請求失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 測試失敗: {str(e)}")
            
            time.sleep(0.5)
        
        # 分析使用者歷程
        print(f"\n📊 使用者歷程分析:")
        journey_analysis = tracker.analyze_user_journey(test_user["user_id"])
        
        print(f"   總對話數: {journey_analysis['total_conversations']}")
        print(f"   會話時長: {journey_analysis['session_duration_minutes']:.1f} 分鐘")
        print(f"   模組使用: {journey_analysis['module_usage']}")
        print(f"   討論主題: {journey_analysis['topics_discussed']}")
        print(f"   主要模組: {journey_analysis['most_used_module']}")
        print(f"   對話流程: {' → '.join(journey_analysis['conversation_flow'])}")
        print(f"   平均信心度: {journey_analysis['average_confidence']:.2f}")
        
        # 生成照護計畫
        print(f"\n🏥 照護計畫建議:")
        care_plan = tracker.generate_care_plan(test_user["user_id"])
        
        print(f"   建議數量: {care_plan['care_plan_summary']['total_recommendations']}")
        print(f"   緊急警報: {care_plan['care_plan_summary']['urgent_alerts']}")
        print(f"   優先等級: {care_plan['care_plan_summary']['priority_level']}")
        
        for rec in care_plan["recommendations"]:
            print(f"   📋 {rec['title']}: {rec['description']} (優先級: {rec['priority']})")
        
        for alert in care_plan["alerts"]:
            print(f"   ⚠️  {alert['message']}")
        
        # 獲取進度追蹤
        print(f"\n📈 進度追蹤:")
        progress = tracker.get_user_progress(test_user["user_id"])
        
        print(f"   首次互動: {progress['first_interaction']}")
        print(f"   最新互動: {progress['latest_interaction']}")
        print(f"   參與等級: {progress['engagement_level']}")
        
        progress_summary = progress["progress_summary"]
        print(f"   進度摘要:")
        print(f"     • 有警訊症狀: {'是' if progress_summary['has_warning_signs'] else '否'}")
        print(f"     • 有行為症狀: {'是' if progress_summary['has_behavioral_symptoms'] else '否'}")
        print(f"     • 尋求照護: {'是' if progress_summary['seeking_care'] else '否'}")
        print(f"     • 持續參與: {'是' if progress_summary['consistent_engagement'] else '否'}")

def test_personalized_tracking():
    """測試個人化追蹤功能"""
    
    print("\n🎯 個人化追蹤測試")
    print("=" * 50)
    
    base_url = "http://localhost:8008"
    tracker = UserJourneyTracker(base_url)
    
    # 模擬長期使用者
    long_term_user = "user_long_term"
    tracker.start_user_session(long_term_user)
    
    # 模擬多個時間點的對話
    conversations_over_time = [
        {"time": "2025-08-01", "message": "媽媽忘記關瓦斯"},
        {"time": "2025-08-02", "message": "媽媽中度失智"},
        {"time": "2025-08-03", "message": "爺爺有妄想症狀"},
        {"time": "2025-08-04", "message": "需要醫療協助"},
        {"time": "2025-08-05", "message": "媽媽最近常重複問同樣的問題"}
    ]
    
    print(f"📅 模擬長期使用者 ({long_term_user}) 的對話歷程:")
    
    for conv in conversations_over_time:
        print(f"\n📅 {conv['time']}: {conv['message']}")
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json={"message": conv["message"], "user_id": long_term_user},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                tracker.log_conversation(long_term_user, conv["message"], data)
                
                alt_text = data.get("altText", "")
                print(f"   🤖 回應: {alt_text[:50]}...")
                
        except Exception as e:
            print(f"   ❌ 測試失敗: {str(e)}")
        
        time.sleep(0.3)
    
    # 分析長期趨勢
    print(f"\n📊 長期趨勢分析:")
    journey_analysis = tracker.analyze_user_journey(long_term_user)
    care_plan = tracker.generate_care_plan(long_term_user)
    progress = tracker.get_user_progress(long_term_user)
    
    print(f"   總對話數: {journey_analysis['total_conversations']}")
    print(f"   模組使用模式: {journey_analysis['module_usage']}")
    print(f"   照護建議: {len(care_plan['recommendations'])} 項")
    print(f"   參與等級: {progress['engagement_level']}")

def test_intelligent_alerts():
    """測試智能提醒與預警功能"""
    
    print("\n🚨 智能提醒與預警測試")
    print("=" * 50)
    
    base_url = "http://localhost:8008"
    tracker = UserJourneyTracker(base_url)
    
    # 模擬緊急情況
    emergency_user = "user_emergency"
    tracker.start_user_session(emergency_user)
    
    emergency_conversations = [
        "爺爺有攻擊行為",
        "爺爺有妄想症狀",
        "需要立即醫療協助",
        "爺爺晚上不睡覺到處走動"
    ]
    
    print(f"🚨 模擬緊急情況使用者 ({emergency_user}):")
    
    for i, message in enumerate(emergency_conversations, 1):
        print(f"\n🚨 緊急對話 {i}: {message}")
        
        try:
            response = requests.post(
                f"{base_url}/analyze",
                json={"message": message, "user_id": emergency_user},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                tracker.log_conversation(emergency_user, message, data)
                
                alt_text = data.get("altText", "")
                print(f"   🤖 回應: {alt_text[:50]}...")
                
        except Exception as e:
            print(f"   ❌ 測試失敗: {str(e)}")
        
        time.sleep(0.3)
    
    # 生成緊急照護計畫
    print(f"\n🚨 緊急照護計畫:")
    care_plan = tracker.generate_care_plan(emergency_user)
    
    for alert in care_plan["alerts"]:
        print(f"   ⚠️  {alert['message']}")
    
    for rec in care_plan["recommendations"]:
        if rec["priority"] == "high":
            print(f"   🔴 高優先級: {rec['title']} - {rec['description']}")

if __name__ == "__main__":
    print("🚀 開始使用者歷程追蹤測試...")
    
    # 檢查服務狀態
    try:
        response = requests.get("http://localhost:8008/health", timeout=5)
        if response.status_code == 200:
            print("✅ Chatbot API 服務正常")
        else:
            print("❌ Chatbot API 服務異常")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Chatbot API 服務無法連接: {e}")
        print("💡 請確保 Chatbot API 正在運行 (port 8008)")
        sys.exit(1)
    
    # 執行測試
    test_user_journey_tracking()
    test_personalized_tracking()
    test_intelligent_alerts()
    
    print("\n✅ 測試完成!")
    print("\n📋 測試總結:")
    print("   • 完整對話記錄與分析")
    print("   • 個人化病程追蹤")
    print("   • 智能提醒與預警")
    print("   • 照護計畫建議")
    print("   • 長期趨勢分析")
    print("   • 緊急情況處理") 