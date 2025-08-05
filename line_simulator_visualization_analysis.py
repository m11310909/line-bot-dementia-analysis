#!/usr/bin/env python3
"""
LINE Simulator 視覺化模組分析腳本
分析失智小幫手4個模組的回應格式，為視覺化優化提供數據
"""

import requests
import json
import time
from typing import Dict, List, Any
from datetime import datetime

class LineSimulatorVisualizationAnalyzer:
    """LINE Simulator 視覺化分析器"""
    
    def __init__(self, base_url: str = "http://localhost:8008"):
        self.base_url = base_url
        self.test_messages = {
            "M1": [
                "媽媽忘記關瓦斯",
                "爸爸不會用洗衣機", 
                "奶奶忘記吃藥",
                "爺爺走失過",
                "媽媽最近常重複問同樣的問題"
            ],
            "M2": [
                "媽媽輕度失智",
                "爸爸中度失智",
                "奶奶重度失智",
                "爺爺病程進展",
                "媽媽記憶力退化"
            ],
            "M3": [
                "爺爺有妄想症狀",
                "爸爸有攻擊行為",
                "奶奶有躁動不安",
                "媽媽有幻覺",
                "爺爺晚上不睡覺"
            ],
            "M4": [
                "需要醫療協助",
                "需要照護資源",
                "需要社會支持",
                "需要經濟協助",
                "需要專業諮詢"
            ]
        }
        
    def test_module_responses(self) -> Dict[str, List[Dict]]:
        """測試各模組的回應格式"""
        results = {}
        
        for module, messages in self.test_messages.items():
            print(f"\n🧪 測試 {module} 模組回應格式...")
            module_results = []
            
            for i, message in enumerate(messages, 1):
                print(f"  📝 測試 {i}/{len(messages)}: {message}")
                
                try:
                    # 測試智能分析
                    response = self.analyze_message(message)
                    module_results.append({
                        "message": message,
                        "response": response,
                        "format_analysis": self.analyze_response_format(response)
                    })
                    
                    # 測試特定模組
                    specific_response = self.analyze_specific_module(message, module.lower())
                    module_results.append({
                        "message": message,
                        "response": specific_response,
                        "format_analysis": self.analyze_response_format(specific_response),
                        "module_specific": True
                    })
                    
                except Exception as e:
                    print(f"    ❌ 錯誤: {e}")
                    
            results[module] = module_results
            
        return results
    
    def analyze_message(self, message: str) -> Dict:
        """智能分析訊息"""
        url = f"{self.base_url}/analyze"
        payload = {
            "message": message,
            "user_id": "simulator_test"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def analyze_specific_module(self, message: str, module: str) -> Dict:
        """分析特定模組"""
        url = f"{self.base_url}/analyze/{module}"
        payload = {
            "message": message,
            "user_id": "simulator_test"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def analyze_response_format(self, response: Dict) -> Dict:
        """分析回應格式"""
        analysis = {
            "response_type": "unknown",
            "has_flex_message": False,
            "has_text": False,
            "has_visualization": False,
            "content_structure": {},
            "key_elements": []
        }
        
        if "type" in response:
            analysis["response_type"] = response["type"]
            
            if response["type"] == "flex":
                analysis["has_flex_message"] = True
                analysis["content_structure"] = self.analyze_flex_structure(response.get("contents", {}))
                analysis["key_elements"] = self.extract_flex_elements(response.get("contents", {}))
                
            elif response["type"] == "text":
                analysis["has_text"] = True
                analysis["content_structure"] = {"text": response.get("text", "")}
                analysis["key_elements"] = self.extract_text_elements(response.get("text", ""))
        
        return analysis
    
    def analyze_flex_structure(self, contents: Dict) -> Dict:
        """分析 Flex Message 結構"""
        structure = {
            "type": contents.get("type", ""),
            "size": contents.get("size", ""),
            "has_header": False,
            "has_body": False,
            "has_footer": False,
            "header_content": {},
            "body_content": {},
            "footer_content": {}
        }
        
        if "header" in contents:
            structure["has_header"] = True
            structure["header_content"] = contents["header"]
            
        if "body" in contents:
            structure["has_body"] = True
            structure["body_content"] = contents["body"]
            
        if "footer" in contents:
            structure["has_footer"] = True
            structure["footer_content"] = contents["footer"]
            
        return structure
    
    def extract_flex_elements(self, contents: Dict) -> List[str]:
        """提取 Flex Message 關鍵元素"""
        elements = []
        
        def extract_text_elements(obj):
            if isinstance(obj, dict):
                if "text" in obj:
                    elements.append(obj["text"])
                for value in obj.values():
                    extract_text_elements(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_text_elements(item)
        
        extract_text_elements(contents)
        return elements
    
    def extract_text_elements(self, text: str) -> List[str]:
        """提取文字回應關鍵元素"""
        elements = []
        
        # 提取表情符號
        import re
        emojis = re.findall(r'[🚨📊🧠🏥📝🔍✅❌⚠️💡]', text)
        elements.extend(emojis)
        
        # 提取關鍵詞
        keywords = ["警訊", "症狀", "階段", "照護", "建議", "分析", "檢測", "評估"]
        for keyword in keywords:
            if keyword in text:
                elements.append(keyword)
                
        return elements
    
    def generate_visualization_recommendations(self, results: Dict) -> Dict:
        """生成視覺化優化建議"""
        recommendations = {
            "M1": {
                "current_format": "flex_message",
                "optimization_suggestions": [],
                "visual_elements": [],
                "interaction_patterns": []
            },
            "M2": {
                "current_format": "flex_message", 
                "optimization_suggestions": [],
                "visual_elements": [],
                "interaction_patterns": []
            },
            "M3": {
                "current_format": "flex_message",
                "optimization_suggestions": [],
                "visual_elements": [],
                "interaction_patterns": []
            },
            "M4": {
                "current_format": "flex_message",
                "optimization_suggestions": [],
                "visual_elements": [],
                "interaction_patterns": []
            }
        }
        
        for module, responses in results.items():
            print(f"\n📊 分析 {module} 模組視覺化優化建議...")
            
            # 分析回應格式
            flex_count = 0
            text_count = 0
            common_elements = []
            
            for response_data in responses:
                analysis = response_data["format_analysis"]
                
                if analysis["has_flex_message"]:
                    flex_count += 1
                if analysis["has_text"]:
                    text_count += 1
                    
                common_elements.extend(analysis["key_elements"])
            
            # 生成優化建議
            if module == "M1":
                recommendations[module]["optimization_suggestions"] = [
                    "🚨 警訊等級視覺化",
                    "📊 症狀嚴重程度圖表",
                    "⏰ 時間軸症狀追蹤",
                    "🎯 風險評估儀表板"
                ]
                recommendations[module]["visual_elements"] = [
                    "警報燈號系統",
                    "症狀檢查清單",
                    "風險等級指示器",
                    "緊急聯絡按鈕"
                ]
                
            elif module == "M2":
                recommendations[module]["optimization_suggestions"] = [
                    "📈 病程進展圖表",
                    "🎯 階段評估儀表板",
                    "📊 認知功能雷達圖",
                    "⏳ 預後時間軸"
                ]
                recommendations[module]["visual_elements"] = [
                    "進度條顯示",
                    "階段標籤系統",
                    "功能評估量表",
                    "趨勢預測圖"
                ]
                
            elif module == "M3":
                recommendations[module]["optimization_suggestions"] = [
                    "🧠 症狀分類圖表",
                    "📊 行為頻率統計",
                    "🎯 症狀嚴重度評估",
                    "💊 藥物反應追蹤"
                ]
                recommendations[module]["visual_elements"] = [
                    "症狀圖標系統",
                    "頻率統計圖",
                    "嚴重度指示器",
                    "治療效果追蹤"
                ]
                
            elif module == "M4":
                recommendations[module]["optimization_suggestions"] = [
                    "🏥 資源地圖視覺化",
                    "📞 聯絡資訊卡片",
                    "💰 費用估算工具",
                    "📅 預約排程系統"
                ]
                recommendations[module]["visual_elements"] = [
                    "資源分類標籤",
                    "聯絡按鈕系統",
                    "費用計算器",
                    "預約日曆"
                ]
            
            # 分析互動模式
            recommendations[module]["interaction_patterns"] = [
                "點擊展開詳細資訊",
                "滑動查看多個選項",
                "長按顯示操作選單",
                "搖晃重新整理內容"
            ]
        
        return recommendations
    
    def create_visualization_prototypes(self, recommendations: Dict) -> Dict:
        """創建視覺化原型設計"""
        prototypes = {}
        
        for module, rec in recommendations.items():
            print(f"\n🎨 創建 {module} 視覺化原型...")
            
            if module == "M1":
                prototypes[module] = {
                    "name": "警訊監控儀表板",
                    "layout": "vertical_carousel",
                    "components": [
                        {
                            "type": "header",
                            "content": "🚨 警訊分析",
                            "style": "warning_red"
                        },
                        {
                            "type": "alert_level",
                            "content": "高風險",
                            "style": "danger"
                        },
                        {
                            "type": "symptom_list",
                            "content": ["忘記關瓦斯", "重複問問題"],
                            "style": "checklist"
                        },
                        {
                            "type": "action_buttons",
                            "content": ["立即諮詢", "記錄症狀", "緊急聯絡"],
                            "style": "primary"
                        }
                    ]
                }
                
            elif module == "M2":
                prototypes[module] = {
                    "name": "病程階段評估",
                    "layout": "horizontal_progress",
                    "components": [
                        {
                            "type": "header",
                            "content": "📊 病程階段",
                            "style": "info_blue"
                        },
                        {
                            "type": "progress_bar",
                            "content": "中度失智",
                            "progress": 60,
                            "style": "gradient"
                        },
                        {
                            "type": "stage_indicators",
                            "content": ["輕度", "中度", "重度"],
                            "current": 1,
                            "style": "dots"
                        },
                        {
                            "type": "assessment_chart",
                            "content": "認知功能評估",
                            "style": "radar"
                        }
                    ]
                }
                
            elif module == "M3":
                prototypes[module] = {
                    "name": "BPSD 症狀分析",
                    "layout": "grid_cards",
                    "components": [
                        {
                            "type": "header",
                            "content": "🧠 BPSD 症狀",
                            "style": "purple"
                        },
                        {
                            "type": "symptom_cards",
                            "content": [
                                {"symptom": "妄想", "severity": "高", "frequency": "經常"},
                                {"symptom": "攻擊行為", "severity": "中", "frequency": "偶爾"}
                            ],
                            "style": "cards"
                        },
                        {
                            "type": "treatment_suggestions",
                            "content": ["藥物治療", "行為療法", "環境調整"],
                            "style": "tags"
                        }
                    ]
                }
                
            elif module == "M4":
                prototypes[module] = {
                    "name": "照護資源導航",
                    "layout": "vertical_list",
                    "components": [
                        {
                            "type": "header",
                            "content": "🏥 照護需求",
                            "style": "medical_blue"
                        },
                        {
                            "type": "resource_categories",
                            "content": [
                                {"category": "醫療", "icon": "🏥", "count": 5},
                                {"category": "照護", "icon": "👨‍⚕️", "count": 3},
                                {"category": "社會支持", "icon": "🤝", "count": 4}
                            ],
                            "style": "category_cards"
                        },
                        {
                            "type": "contact_buttons",
                            "content": ["立即諮詢", "預約服務", "查看詳情"],
                            "style": "action_buttons"
                        }
                    ]
                }
        
        return prototypes
    
    def run_analysis(self):
        """執行完整分析"""
        print("🚀 開始 LINE Simulator 視覺化模組分析...")
        print("=" * 60)
        
        # 測試各模組回應
        results = self.test_module_responses()
        
        # 生成優化建議
        recommendations = self.generate_visualization_recommendations(results)
        
        # 創建視覺化原型
        prototypes = self.create_visualization_prototypes(recommendations)
        
        # 生成分析報告
        self.generate_analysis_report(results, recommendations, prototypes)
        
        print("\n✅ 分析完成!")
        return {
            "results": results,
            "recommendations": recommendations,
            "prototypes": prototypes
        }
    
    def generate_analysis_report(self, results: Dict, recommendations: Dict, prototypes: Dict):
        """生成分析報告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": sum(len(responses) for responses in results.values()),
                "modules_analyzed": list(results.keys()),
                "response_formats": self.analyze_response_formats(results)
            },
            "module_analysis": {},
            "visualization_recommendations": recommendations,
            "prototype_designs": prototypes
        }
        
        # 詳細模組分析
        for module, responses in results.items():
            report["module_analysis"][module] = {
                "test_count": len(responses),
                "flex_message_count": sum(1 for r in responses if r["format_analysis"]["has_flex_message"]),
                "text_response_count": sum(1 for r in responses if r["format_analysis"]["has_text"]),
                "common_elements": self.get_common_elements(responses),
                "response_structure": self.analyze_module_structure(responses)
            }
        
        # 保存報告
        with open("visualization_analysis_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 分析報告已保存: visualization_analysis_report.json")
        
        # 打印摘要
        self.print_analysis_summary(report)
    
    def analyze_response_formats(self, results: Dict) -> Dict:
        """分析回應格式統計"""
        formats = {"flex": 0, "text": 0, "mixed": 0}
        
        for responses in results.values():
            for response in responses:
                analysis = response["format_analysis"]
                if analysis["has_flex_message"] and analysis["has_text"]:
                    formats["mixed"] += 1
                elif analysis["has_flex_message"]:
                    formats["flex"] += 1
                elif analysis["has_text"]:
                    formats["text"] += 1
        
        return formats
    
    def get_common_elements(self, responses: List[Dict]) -> List[str]:
        """獲取常見元素"""
        all_elements = []
        for response in responses:
            all_elements.extend(response["format_analysis"]["key_elements"])
        
        # 統計頻率
        from collections import Counter
        element_counts = Counter(all_elements)
        return [element for element, count in element_counts.most_common(5)]
    
    def analyze_module_structure(self, responses: List[Dict]) -> Dict:
        """分析模組結構"""
        structures = {
            "has_header": 0,
            "has_body": 0,
            "has_footer": 0,
            "common_layouts": []
        }
        
        for response in responses:
            if "content_structure" in response["format_analysis"]:
                structure = response["format_analysis"]["content_structure"]
                if structure.get("has_header"):
                    structures["has_header"] += 1
                if structure.get("has_body"):
                    structures["has_body"] += 1
                if structure.get("has_footer"):
                    structures["has_footer"] += 1
        
        return structures
    
    def print_analysis_summary(self, report: Dict):
        """打印分析摘要"""
        print("\n📋 視覺化模組分析摘要")
        print("=" * 50)
        
        summary = report["summary"]
        print(f"📊 總測試數: {summary['total_tests']}")
        print(f"🎯 分析模組: {', '.join(summary['modules_analyzed'])}")
        print(f"📱 回應格式: {summary['response_formats']}")
        
        print("\n🎨 視覺化優化建議:")
        for module, rec in report["visualization_recommendations"].items():
            print(f"  {module}: {len(rec['optimization_suggestions'])} 項建議")
            for suggestion in rec['optimization_suggestions'][:2]:
                print(f"    • {suggestion}")

if __name__ == "__main__":
    analyzer = LineSimulatorVisualizationAnalyzer()
    results = analyzer.run_analysis() 