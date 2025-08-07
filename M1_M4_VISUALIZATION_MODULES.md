# 🎨 **M1-M4 視覺化模組完整設計**

## 📋 **模組概述**

基於您提供的 M1 警訊分析界面，我將為 M1-M4 四大模組設計完整的視覺化界面，並整合關鍵指標和自動化功能。

---

## 🚨 **M1 模組：警訊分析 (Warning Analysis)**

### **📱 界面設計**
```python
def create_m1_visualization(analysis_result: Dict) -> Dict:
    """創建 M1 警訊分析視覺化界面"""
    
    return {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🚨 警訊分析",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "icon",
                            "url": "https://example.com/siren-icon.png",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": f"{analysis_result['risk_level']}風險",
                            "size": "sm",
                            "color": "#ffffff"
                        }
                    ]
                }
            ],
            "backgroundColor": "#FF6B6B"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # AI 信心度
                create_ai_confidence_section(analysis_result),
                
                # AI 分析摘要
                create_ai_summary_section(analysis_result),
                
                # 失智警訊卡片
                create_warning_cards_section(analysis_result),
                
                # 指標和來源
                create_metrics_and_sources_section(analysis_result)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "深入瞭解",
                        "data": "action=m1_details"
                    },
                    "style": "primary",
                    "color": "#FF6B6B"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "儲存分析報告",
                        "data": "action=save_report"
                    },
                    "style": "secondary"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "分享給家人",
                        "data": "action=share_family"
                    },
                    "style": "secondary"
                }
            ]
        }
    }

def create_ai_confidence_section(analysis_result: Dict) -> Dict:
    """創建 AI 信心度區塊"""
    confidence = analysis_result.get("confidence", 0.85)
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "🤖 AI信心度",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "width": f"{confidence * 100}%",
                        "height": "8px",
                        "backgroundColor": "#4ECDC4"
                    }
                ],
                "backgroundColor": "#f0f0f0",
                "cornerRadius": "4px"
            },
            {
                "type": "text",
                "text": f"{confidence:.0%}",
                "size": "xs",
                "align": "end"
            }
        ],
        "margin": "sm"
    }

def create_ai_summary_section(analysis_result: Dict) -> Dict:
    """創建 AI 分析摘要區塊"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "icon",
                        "url": "https://example.com/doctor-icon.png",
                        "size": "sm"
                    },
                    {
                        "type": "text",
                        "text": "AI分析摘要",
                        "weight": "bold",
                        "size": "sm"
                    }
                ]
            },
            {
                "type": "text",
                "text": analysis_result.get("summary", ""),
                "wrap": True,
                "margin": "sm"
            },
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "查看AI分析判准報告",
                    "data": "action=view_ai_report"
                },
                "style": "link",
                "height": "sm"
            }
        ],
        "margin": "sm"
    }

def create_warning_cards_section(analysis_result: Dict) -> Dict:
    """創建失智警訊卡片區塊"""
    warnings = analysis_result.get("warnings", [])
    
    warning_cards = []
    for warning in warnings[:2]:  # 顯示前兩個警訊
        warning_cards.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "icon",
                            "url": warning.get("icon", ""),
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": warning.get("title", ""),
                            "weight": "bold",
                            "size": "sm"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": warning.get("description", ""),
                    "size": "xs",
                    "wrap": True,
                    "margin": "sm"
                }
            ],
            "backgroundColor": "#fff5f5",
            "cornerRadius": "8px",
            "paddingAll": "sm",
            "margin": "xs"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "!! 失智警訊",
                "weight": "bold",
                "size": "md",
                "color": "#FF6B6B"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": warning_cards
            }
        ],
        "margin": "sm"
    }

def create_metrics_and_sources_section(analysis_result: Dict) -> Dict:
    """創建指標和來源區塊"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            # 指標區塊
            {
                "type": "text",
                "text": "📊 分析指標",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"AUC: {analysis_result.get('auc', 0.85):.3f}",
                        "size": "xs",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"Recall@K: {analysis_result.get('recall_at_k', 0.78):.2f}",
                        "size": "xs",
                        "flex": 1
                    }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"用戶滿意度: {analysis_result.get('user_satisfaction', 4.2):.1f}/5.0",
                        "size": "xs",
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"醫師覆核差異: {analysis_result.get('physician_diff', 0.12):.2f}",
                        "size": "xs",
                        "flex": 1
                    }
                ]
            },
            
            # 來源區塊
            {
                "type": "text",
                "text": "📚 引用來源",
                "weight": "bold",
                "size": "sm",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": analysis_result.get("sources", "基於 DSM-5 診斷標準和台灣失智症協會指南"),
                "size": "xs",
                "wrap": True,
                "color": "#666666"
            }
        ],
        "margin": "sm"
    }
```

---

## 📈 **M2 模組：病程進展評估 (Progression Assessment)**

### **📱 界面設計**
```python
def create_m2_visualization(analysis_result: Dict) -> Dict:
    """創建 M2 病程進展評估視覺化界面"""
    
    return {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📈 病程進展評估",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": f"評估階段: {analysis_result.get('stage', '輕度')}",
                    "size": "sm",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#4ECDC4"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 進展階段圖表
                create_progression_chart(analysis_result),
                
                # 症狀特徵
                create_symptom_features_section(analysis_result),
                
                # 照護重點
                create_care_focus_section(analysis_result),
                
                # 指標和來源
                create_metrics_and_sources_section(analysis_result)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "詳細病程分析",
                        "data": "action=m2_details"
                    },
                    "style": "primary",
                    "color": "#4ECDC4"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "照護計劃建議",
                        "data": "action=care_plan"
                    },
                    "style": "secondary"
                }
            ]
        }
    }

def create_progression_chart(analysis_result: Dict) -> Dict:
    """創建進展階段圖表"""
    stages = ["輕度", "中度", "重度"]
    current_stage = analysis_result.get("current_stage", 0)
    
    stage_indicators = []
    for i, stage in enumerate(stages):
        color = "#4ECDC4" if i == current_stage else "#f0f0f0"
        stage_indicators.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": stage,
                    "size": "xs",
                    "align": "center"
                },
                {
                    "type": "box",
                    "width": "20px",
                    "height": "20px",
                    "backgroundColor": color,
                    "cornerRadius": "10px"
                }
            ],
            "flex": 1
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "🔄 病程進展階段",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": stage_indicators,
                "margin": "sm"
            }
        ],
        "margin": "sm"
    }
```

---

## 🧠 **M3 模組：行為心理症狀分析 (BPSD Analysis)**

### **📱 界面設計**
```python
def create_m3_visualization(analysis_result: Dict) -> Dict:
    """創建 M3 行為心理症狀分析視覺化界面"""
    
    return {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🧠 行為心理症狀分析",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": f"主要症狀: {analysis_result.get('primary_symptom', '激動/攻擊')}",
                    "size": "sm",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#45B7D1"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 症狀分類熱力圖
                create_symptom_heatmap(analysis_result),
                
                # 觸發因素
                create_triggers_section(analysis_result),
                
                # 干預建議
                create_interventions_section(analysis_result),
                
                # 指標和來源
                create_metrics_and_sources_section(analysis_result)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "詳細症狀分析",
                        "data": "action=m3_details"
                    },
                    "style": "primary",
                    "color": "#45B7D1"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "專業諮詢",
                        "data": "action=professional_consultation"
                    },
                    "style": "secondary"
                }
            ]
        }
    }

def create_symptom_heatmap(analysis_result: Dict) -> Dict:
    """創建症狀分類熱力圖"""
    bpsd_categories = [
        "激動/攻擊", "憂鬱/焦慮", "精神病症狀", "冷漠/退縮", "睡眠障礙"
    ]
    
    severity_levels = analysis_result.get("severity_levels", {})
    
    category_cards = []
    for category in bpsd_categories:
        severity = severity_levels.get(category, 0)
        color = get_severity_color(severity)
        
        category_cards.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": category,
                    "size": "xs",
                    "align": "center"
                },
                {
                    "type": "box",
                    "width": "100%",
                    "height": "20px",
                    "backgroundColor": color,
                    "cornerRadius": "4px"
                }
            ],
            "flex": 1,
            "margin": "xs"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "🔥 症狀嚴重程度",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": category_cards
            }
        ],
        "margin": "sm"
    }
```

---

## 🏥 **M4 模組：照護資源導航 (Care Navigation)**

### **📱 界面設計**
```python
def create_m4_visualization(analysis_result: Dict) -> Dict:
    """創建 M4 照護資源導航視覺化界面"""
    
    return {
        "type": "bubble",
        "size": "kilo",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏥 照護資源導航",
                    "weight": "bold",
                    "size": "lg",
                    "color": "#ffffff"
                },
                {
                    "type": "text",
                    "text": f"推薦類別: {analysis_result.get('recommended_category', '醫療資源')}",
                    "size": "sm",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#96CEB4"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 資源分類
                create_resource_categories(analysis_result),
                
                # 具體資源推薦
                create_resource_recommendations(analysis_result),
                
                # 聯絡資訊
                create_contact_info(analysis_result),
                
                # 指標和來源
                create_metrics_and_sources_section(analysis_result)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "詳細資源資訊",
                        "data": "action=m4_details"
                    },
                    "style": "primary",
                    "color": "#96CEB4"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "預約諮詢",
                        "data": "action=book_consultation"
                    },
                    "style": "secondary"
                }
            ]
        }
    }

def create_resource_categories(analysis_result: Dict) -> Dict:
    """創建資源分類區塊"""
    categories = [
        {"name": "醫療資源", "icon": "🏥", "color": "#FF6B6B"},
        {"name": "社會支持", "icon": "🤝", "color": "#4ECDC4"},
        {"name": "照護技巧", "icon": "📚", "color": "#45B7D1"},
        {"name": "緊急處理", "icon": "🚨", "color": "#FFA500"},
        {"name": "法律權益", "icon": "⚖️", "color": "#9B59B6"}
    ]
    
    category_cards = []
    for category in categories:
        category_cards.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": category["icon"],
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": category["name"],
                    "size": "sm",
                    "flex": 1
                }
            ],
            "backgroundColor": category["color"] + "20",
            "cornerRadius": "8px",
            "paddingAll": "sm",
            "margin": "xs"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "📋 資源分類",
                "weight": "bold",
                "size": "sm"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": category_cards
            }
        ],
        "margin": "sm"
    }
```

---

## 📊 **指標監控系統**

### **🔍 關鍵指標追蹤**
```python
class MetricsTracker:
    """指標追蹤系統"""
    
    def __init__(self):
        self.metrics = {
            "auc": [],
            "recall_at_k": [],
            "user_satisfaction": [],
            "physician_diff": [],
            "response_time": [],
            "error_rate": []
        }
    
    def record_metrics(self, analysis_result: Dict):
        """記錄分析指標"""
        self.metrics["auc"].append(analysis_result.get("auc", 0))
        self.metrics["recall_at_k"].append(analysis_result.get("recall_at_k", 0))
        self.metrics["user_satisfaction"].append(analysis_result.get("user_satisfaction", 0))
        self.metrics["physician_diff"].append(analysis_result.get("physician_diff", 0))
        self.metrics["response_time"].append(analysis_result.get("response_time", 0))
        self.metrics["error_rate"].append(analysis_result.get("error_rate", 0))
    
    def get_performance_report(self) -> Dict:
        """獲取效能報告"""
        return {
            "avg_auc": np.mean(self.metrics["auc"]),
            "avg_recall_at_k": np.mean(self.metrics["recall_at_k"]),
            "avg_user_satisfaction": np.mean(self.metrics["user_satisfaction"]),
            "avg_physician_diff": np.mean(self.metrics["physician_diff"]),
            "avg_response_time": np.mean(self.metrics["response_time"]),
            "avg_error_rate": np.mean(self.metrics["error_rate"])
        }
    
    def check_threshold_alerts(self) -> List[Dict]:
        """檢查閾值警報"""
        alerts = []
        
        # AUC 閾值檢查
        avg_auc = np.mean(self.metrics["auc"])
        if avg_auc < 0.8:
            alerts.append({
                "type": "warning",
                "message": f"AUC 指標過低: {avg_auc:.3f}",
                "severity": "medium",
                "recipients": ["devops", "clinical_consultant"]
            })
        
        # 用戶滿意度閾值檢查
        avg_satisfaction = np.mean(self.metrics["user_satisfaction"])
        if avg_satisfaction < 4.0:
            alerts.append({
                "type": "warning",
                "message": f"用戶滿意度過低: {avg_satisfaction:.1f}/5.0",
                "severity": "high",
                "recipients": ["devops", "clinical_consultant", "product_manager"]
            })
        
        # 醫師覆核差異閾值檢查
        avg_physician_diff = np.mean(self.metrics["physician_diff"])
        if avg_physician_diff > 0.2:
            alerts.append({
                "type": "error",
                "message": f"醫師覆核差異過大: {avg_physician_diff:.2f}",
                "severity": "high",
                "recipients": ["devops", "clinical_consultant", "medical_director"]
            })
        
        return alerts
```

### **🚨 自動警報系統**
```python
class AlertSystem:
    """自動警報系統"""
    
    def __init__(self):
        self.thresholds = {
            "auc_min": 0.8,
            "recall_at_k_min": 0.75,
            "user_satisfaction_min": 4.0,
            "physician_diff_max": 0.2,
            "response_time_max": 5.0,
            "error_rate_max": 0.05
        }
    
    async def send_alert(self, alert: Dict):
        """發送警報"""
        recipients = alert.get("recipients", [])
        
        for recipient in recipients:
            if recipient == "devops":
                await self.send_devops_alert(alert)
            elif recipient == "clinical_consultant":
                await self.send_clinical_alert(alert)
            elif recipient == "product_manager":
                await self.send_product_alert(alert)
            elif recipient == "medical_director":
                await self.send_medical_director_alert(alert)
    
    async def send_devops_alert(self, alert: Dict):
        """發送 DevOps 警報"""
        message = f"""
🚨 系統效能警報
類型: {alert['type']}
嚴重程度: {alert['severity']}
訊息: {alert['message']}
時間: {datetime.now().isoformat()}
        """
        
        # 發送到 Slack/Discord/Email
        await self.send_to_devops_channel(message)
    
    async def send_clinical_alert(self, alert: Dict):
        """發送臨床顧問警報"""
        message = f"""
🏥 臨床品質警報
類型: {alert['type']}
嚴重程度: {alert['severity']}
訊息: {alert['message']}
時間: {datetime.now().isoformat()}
        """
        
        # 發送到臨床顧問群組
        await self.send_to_clinical_channel(message)
```

---

## 📚 **引用來源系統**

### **🔗 來源管理**
```python
class CitationManager:
    """引用來源管理系統"""
    
    def __init__(self):
        self.sources = {
            "dsm5": {
                "title": "Diagnostic and Statistical Manual of Mental Disorders, 5th Edition",
                "author": "American Psychiatric Association",
                "year": "2013",
                "url": "https://doi.org/10.1176/appi.books.9780890425596"
            },
            "taiwan_dementia": {
                "title": "台灣失智症協會照護指南",
                "author": "台灣失智症協會",
                "year": "2023",
                "url": "https://www.tada2002.org.tw/"
            },
            "who_dementia": {
                "title": "WHO Guidelines on Risk Reduction of Cognitive Decline and Dementia",
                "author": "World Health Organization",
                "year": "2019",
                "url": "https://www.who.int/publications/i/item/risk-reduction-of-cognitive-decline-and-dementia"
            }
        }
    
    def get_citation_text(self, source_keys: List[str]) -> str:
        """獲取引用文字"""
        citations = []
        for key in source_keys:
            if key in self.sources:
                source = self.sources[key]
                citations.append(f"{source['author']} ({source['year']})")
        
        if citations:
            return f"基於: {', '.join(citations)}"
        else:
            return "基於 DSM-5 診斷標準和台灣失智症協會指南"
    
    def get_detailed_sources(self, source_keys: List[str]) -> List[Dict]:
        """獲取詳細來源資訊"""
        detailed_sources = []
        for key in source_keys:
            if key in self.sources:
                detailed_sources.append(self.sources[key])
        
        return detailed_sources
```

---

## 🎯 **完整整合範例**

### **📱 主工作流程**
```python
async def create_comprehensive_visualization(analysis_result: Dict) -> Dict:
    """創建完整的視覺化界面"""
    
    # 根據分析結果選擇模組
    selected_module = analysis_result.get("selected_module", "M1")
    
    # 記錄指標
    metrics_tracker.record_metrics(analysis_result)
    
    # 檢查警報
    alerts = metrics_tracker.check_threshold_alerts()
    for alert in alerts:
        await alert_system.send_alert(alert)
    
    # 獲取引用來源
    citation_text = citation_manager.get_citation_text(
        analysis_result.get("source_keys", ["dsm5", "taiwan_dementia"])
    )
    analysis_result["sources"] = citation_text
    
    # 創建對應模組的視覺化
    if selected_module == "M1":
        return create_m1_visualization(analysis_result)
    elif selected_module == "M2":
        return create_m2_visualization(analysis_result)
    elif selected_module == "M3":
        return create_m3_visualization(analysis_result)
    elif selected_module == "M4":
        return create_m4_visualization(analysis_result)
    else:
        return create_m1_visualization(analysis_result)  # 預設
```

---

## 📈 **預期效果**

### **✅ 視覺化特色**
- **M1 模組**: 警訊分析卡片，風險等級指示
- **M2 模組**: 進展階段圖表，症狀特徵展示
- **M3 模組**: 症狀熱力圖，干預建議
- **M4 模組**: 資源分類導航，聯絡資訊

### **📊 指標監控**
- **AUC**: 模型準確性指標
- **Recall@K**: 檢索相關性指標
- **用戶滿意度**: 用戶體驗指標
- **醫師覆核差異**: 專業一致性指標

### **🚨 自動警報**
- **閾值監控**: 即時監控關鍵指標
- **自動通知**: DevOps 和臨床顧問自動警報
- **分級處理**: 根據嚴重程度分級處理

### **📚 引用來源**
- **專業標準**: 基於 DSM-5 和台灣失智症協會指南
- **透明化**: 明確標示分析依據
- **可追溯**: 提供詳細的來源資訊

---

*這個完整的 M1-M4 視覺化模組設計，結合了您提供的界面參考，並整合了關鍵指標監控、自動警報系統和引用來源管理，為失智症分析系統提供了專業、可信、可解釋的視覺化體驗。* 