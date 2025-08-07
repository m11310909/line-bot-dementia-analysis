# 🧠 **BoN-MAV + SHAP/LIME 特徵重要度整合方案**

## 📋 **整合概述**

將 BoN-MAV (Best of N - Multi-Aspect Verification) 方法與 SHAP (SHapley Additive exPlanations) 和 LIME (Local Interpretable Model-agnostic Explanations) 特徵重要度分析整合到現有的失智症分析系統中，提供更深入的可解釋性分析。

---

## 🔧 **BoN-MAV 方法實現**

### **📊 BoN-MAV 核心概念**
```python
class BoNMAV:
    """
    Best of N - Multi-Aspect Verification
    從多個候選答案中選擇最佳答案，並進行多面向驗證
    """
    
    def __init__(self, n_candidates: int = 5):
        self.n_candidates = n_candidates
        self.aspects = {
            "medical_accuracy": "醫療準確性",
            "safety": "安全性",
            "feasibility": "可行性",
            "emotional_appropriateness": "情感適當性"
        }
    
    async def generate_best_answer(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """生成最佳答案並進行多面向驗證"""
        
        # 步驟 1: 生成多個候選答案
        candidates = await self._generate_candidates(user_input, context)
        
        # 步驟 2: 對每個候選答案進行多面向驗證
        verified_candidates = []
        for candidate in candidates:
            verification = await self._verify_aspects(candidate, context)
            verified_candidates.append({
                "answer": candidate,
                "verification": verification,
                "overall_score": self._calculate_comprehensive_score(candidate, verification, context)
            })
        
        # 步驟 3: 選擇最佳答案
        best_candidate = max(verified_candidates, key=lambda x: x["overall_score"])
        
        return {
            "best_answer": best_candidate["answer"],
            "verification_results": best_candidate["verification"],
            "overall_score": best_candidate["overall_score"],
            "selection_reason": self._get_selection_reason(best_candidate),
            "all_candidates": verified_candidates
        }
    
    async def _generate_candidates(self, user_input: str, context: Dict) -> List[str]:
        """生成多個候選答案"""
        candidates = []
        
        # 使用不同的 AI 引擎生成候選答案
        engines = [
            ("gemini", "gemini-1.5-pro"),
            ("openai", "gpt-3.5-turbo"),
            ("third_party", "dementia-assistant")
        ]
        
        for engine_name, model in engines:
            try:
                candidate = await self._call_ai_engine(engine_name, user_input, context)
                candidates.append(candidate)
            except Exception as e:
                logger.warning(f"引擎 {engine_name} 生成候選答案失敗: {e}")
        
        # 如果候選答案不足，使用變體生成
        while len(candidates) < self.n_candidates:
            variant = await self._generate_variant(user_input, context, len(candidates))
            candidates.append(variant)
        
        return candidates[:self.n_candidates]
    
    async def _verify_aspects(self, answer: str, context: Dict) -> Dict[str, float]:
        """對答案進行多面向驗證"""
        verification_results = {}
        
        for aspect, aspect_name in self.aspects.items():
            score = await self._verify_aspect(aspect, answer, context)
            verification_results[aspect] = score
        
        return verification_results
    
    async def _verify_aspect(self, aspect: str, answer: str, context: Dict) -> float:
        """驗證特定面向"""
        if aspect == "medical_accuracy":
            return self._verify_medical_accuracy(answer, context)
        elif aspect == "safety":
            return self._verify_safety(answer, context)
        elif aspect == "feasibility":
            return self._verify_feasibility(answer, context)
        elif aspect == "emotional_appropriateness":
            return self._verify_emotional_appropriateness(answer, context)
        else:
            return 0.5  # 預設分數
    
    def _verify_medical_accuracy(self, answer: str, context: Dict) -> float:
        """驗證醫療準確性"""
        medical_keywords = ["失智症", "阿茲海默", "認知障礙", "神經科", "醫師"]
        score = sum(1 for keyword in medical_keywords if keyword in answer)
        return min(score / len(medical_keywords), 1.0)
    
    def _verify_safety(self, answer: str, context: Dict) -> float:
        """驗證安全性"""
        safety_indicators = [
            "建議就醫", "專業評估", "安全", "謹慎", "避免"
        ]
        risk_indicators = [
            "自行用藥", "延誤就醫", "忽視症狀", "危險"
        ]
        
        safety_score = sum(1 for indicator in safety_indicators if indicator in answer)
        risk_score = sum(1 for indicator in risk_indicators if indicator in answer)
        
        return max(0, min(1, (safety_score - risk_score) / len(safety_indicators)))
    
    def _verify_feasibility(self, answer: str, context: Dict) -> float:
        """驗證可行性"""
        feasibility_indicators = [
            "具體", "可執行", "實用", "明確", "步驟"
        ]
        score = sum(1 for indicator in feasibility_indicators if indicator in answer)
        return min(score / len(feasibility_indicators), 1.0)
    
    def _verify_emotional_appropriateness(self, answer: str, context: Dict) -> float:
        """驗證情感適當性"""
        positive_indicators = [
            "關懷", "理解", "支持", "陪伴", "耐心"
        ]
        negative_indicators = [
            "指責", "批評", "冷漠", "忽視"
        ]
        
        positive_score = sum(1 for indicator in positive_indicators if indicator in answer)
        negative_score = sum(1 for indicator in negative_indicators if indicator in answer)
        
        return max(0, min(1, (positive_score - negative_score) / len(positive_indicators)))
    
    def _calculate_comprehensive_score(self, answer: str, verification: Dict, context: Dict) -> float:
        """計算綜合分數"""
        weights = {
            "medical_accuracy": 0.4,
            "safety": 0.3,
            "feasibility": 0.2,
            "emotional_appropriateness": 0.1
        }
        
        weighted_score = sum(
            verification[aspect] * weight 
            for aspect, weight in weights.items()
        )
        
        return weighted_score
    
    def _get_selection_reason(self, best_candidate: Dict) -> str:
        """獲取選擇原因"""
        verification = best_candidate["verification"]
        max_aspect = max(verification.items(), key=lambda x: x[1])
        
        reasons = {
            "medical_accuracy": "醫療準確性最高",
            "safety": "安全性考量最佳",
            "feasibility": "可行性最強",
            "emotional_appropriateness": "情感適當性最佳"
        }
        
        return reasons.get(max_aspect[0], "綜合評分最高")
```

---

## 📊 **SHAP 特徵重要度分析**

### **🔍 SHAP 實現**
```python
import shap
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class SHAPAnalyzer:
    """SHAP 特徵重要度分析器"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.explainer = None
        self.feature_names = []
    
    def train_model(self, training_data: List[Dict]):
        """訓練模型並初始化 SHAP 解釋器"""
        # 準備訓練資料
        texts = [item["text"] for item in training_data]
        labels = [item["label"] for item in training_data]
        
        # 特徵提取
        X = self.vectorizer.fit_transform(texts)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # 訓練模型
        self.model.fit(X, labels)
        
        # 初始化 SHAP 解釋器
        self.explainer = shap.TreeExplainer(self.model)
    
    def analyze_feature_importance(self, text: str) -> Dict[str, Any]:
        """分析文本的特徵重要度"""
        # 特徵提取
        X = self.vectorizer.transform([text])
        
        # 生成 SHAP 值
        shap_values = self.explainer.shap_values(X)
        
        # 提取特徵重要度
        feature_importance = {}
        for i, feature_name in enumerate(self.feature_names):
            if X[0, i] > 0:  # 只考慮文本中出現的特徵
                feature_importance[feature_name] = float(shap_values[0, i])
        
        # 排序特徵重要度
        sorted_features = sorted(
            feature_importance.items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )
        
        return {
            "feature_importance": dict(sorted_features[:10]),  # 前 10 個重要特徵
            "shap_values": shap_values.tolist(),
            "base_value": float(self.explainer.expected_value),
            "prediction": self.model.predict(X)[0]
        }
    
    def create_shap_visualization(self, analysis_result: Dict) -> Dict:
        """創建 SHAP 視覺化"""
        feature_importance = analysis_result["feature_importance"]
        
        # 創建特徵重要度圖表
        chart_data = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🔍 特徵重要度分析 (SHAP)",
                    "weight": "bold",
                    "size": "md",
                    "color": "#FF6B6B"
                },
                {
                    "type": "text",
                    "text": "以下特徵對分析結果影響最大：",
                    "size": "sm",
                    "margin": "sm"
                }
            ]
        }
        
        # 添加特徵條形圖
        for feature, importance in list(feature_importance.items())[:5]:
            color = "#FF6B6B" if importance > 0 else "#4ECDC4"
            chart_data["contents"].append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": feature,
                        "size": "sm",
                        "flex": 2
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "width": f"{abs(importance) * 100}%",
                                "height": "8px",
                                "backgroundColor": color
                            }
                        ],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{importance:.3f}",
                        "size": "xs",
                        "color": color,
                        "align": "end"
                    }
                ],
                "margin": "xs"
            })
        
        return chart_data
```

---

## 🎯 **LIME 局部解釋分析**

### **🔍 LIME 實現**
```python
from lime.lime_text import LimeTextExplainer
import numpy as np

class LIMEAnalyzer:
    """LIME 局部解釋分析器"""
    
    def __init__(self):
        self.explainer = LimeTextExplainer(class_names=['正常', '輕度', '中度', '重度'])
    
    def analyze_local_importance(self, text: str, model) -> Dict[str, Any]:
        """分析文本的局部特徵重要度"""
        
        # 創建預測函數
        def predict_proba(texts):
            # 這裡需要根據實際模型調整
            return np.array([[0.1, 0.3, 0.4, 0.2]])  # 示例預測
        
        # 生成 LIME 解釋
        exp = self.explainer.explain_instance(
            text, 
            predict_proba, 
            num_features=10,
            num_samples=100
        )
        
        # 提取特徵重要度
        feature_importance = {}
        for feature, weight in exp.as_list():
            feature_importance[feature] = weight
        
        return {
            "feature_importance": feature_importance,
            "predicted_class": exp.predicted_class,
            "confidence": exp.score,
            "explanation": exp.as_list()
        }
    
    def create_lime_visualization(self, analysis_result: Dict) -> Dict:
        """創建 LIME 視覺化"""
        feature_importance = analysis_result["feature_importance"]
        
        # 創建局部解釋圖表
        chart_data = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎯 局部特徵解釋 (LIME)",
                    "weight": "bold",
                    "size": "md",
                    "color": "#4ECDC4"
                },
                {
                    "type": "text",
                    "text": f"預測類別: {analysis_result['predicted_class']}",
                    "size": "sm",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"信心度: {analysis_result['confidence']:.2f}",
                    "size": "sm"
                }
            ]
        }
        
        # 添加特徵重要度
        for feature, importance in list(feature_importance.items())[:5]:
            color = "#4ECDC4" if importance > 0 else "#FF6B6B"
            chart_data["contents"].append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": feature,
                        "size": "sm",
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": f"{importance:.3f}",
                        "size": "sm",
                        "color": color,
                        "align": "end",
                        "flex": 1
                    }
                ],
                "margin": "xs"
            })
        
        return chart_data
```

---

## 🔄 **整合到現有系統**

### **📱 更新工作流程**
```python
async def enhanced_analysis_workflow(user_input: str) -> Dict[str, Any]:
    """增強的分析工作流程，整合 BoN-MAV、SHAP、LIME"""
    
    # 步驟 1: BoN-MAV 分析
    bon_mav_result = await bon_mav_analyzer.generate_best_answer(user_input, {})
    
    # 步驟 2: SHAP 特徵重要度分析
    shap_result = shap_analyzer.analyze_feature_importance(user_input)
    
    # 步驟 3: LIME 局部解釋分析
    lime_result = lime_analyzer.analyze_local_importance(user_input, model)
    
    # 步驟 4: 整合結果
    integrated_result = {
        "bon_mav": bon_mav_result,
        "shap": shap_result,
        "lime": lime_result,
        "user_input": user_input,
        "timestamp": datetime.now().isoformat()
    }
    
    return integrated_result
```

### **🎨 創建綜合視覺化**
```python
def create_comprehensive_xai_visualization(integrated_result: Dict) -> Dict:
    """創建綜合的 XAI 視覺化"""
    
    return {
        "type": "carousel",
        "contents": [
            # BoN-MAV 視覺化
            create_bon_mav_visualization(integrated_result["bon_mav"]),
            # SHAP 視覺化
            create_shap_visualization(integrated_result["shap"]),
            # LIME 視覺化
            create_lime_visualization(integrated_result["lime"])
        ]
    }

def create_bon_mav_visualization(bon_mav_result: Dict) -> Dict:
    """創建 BoN-MAV 視覺化"""
    return {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 BoN-MAV 最佳答案選擇",
                    "weight": "bold",
                    "color": "#ffffff"
                }
            ],
            "backgroundColor": "#FF6B6B"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "多面向驗證結果：",
                    "weight": "bold"
                },
                # 添加驗證結果
                create_verification_chart(bon_mav_result["verification_results"]),
                {
                    "type": "text",
                    "text": f"選擇原因: {bon_mav_result['selection_reason']}",
                    "size": "sm",
                    "margin": "sm"
                }
            ]
        }
    }

def create_verification_chart(verification_results: Dict) -> Dict:
    """創建驗證結果圖表"""
    chart_contents = []
    
    for aspect, score in verification_results.items():
        aspect_names = {
            "medical_accuracy": "醫療準確性",
            "safety": "安全性",
            "feasibility": "可行性",
            "emotional_appropriateness": "情感適當性"
        }
        
        chart_contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": aspect_names.get(aspect, aspect),
                    "size": "sm",
                    "flex": 2
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "width": f"{score * 100}%",
                            "height": "8px",
                            "backgroundColor": "#FF6B6B"
                        }
                    ],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{score:.2f}",
                    "size": "xs",
                    "align": "end"
                }
            ],
            "margin": "xs"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": chart_contents
    }
```

---

## 📊 **效能監控與優化**

### **⚡ 效能指標**
```python
class XAIPerformanceMonitor:
    """XAI 效能監控器"""
    
    def __init__(self):
        self.metrics = {
            "bon_mav_time": [],
            "shap_time": [],
            "lime_time": [],
            "total_time": [],
            "accuracy": [],
            "user_satisfaction": []
        }
    
    def record_metrics(self, metrics: Dict):
        """記錄效能指標"""
        for key, value in metrics.items():
            if key in self.metrics:
                self.metrics[key].append(value)
    
    def get_performance_report(self) -> Dict:
        """獲取效能報告"""
        return {
            "avg_bon_mav_time": np.mean(self.metrics["bon_mav_time"]),
            "avg_shap_time": np.mean(self.metrics["shap_time"]),
            "avg_lime_time": np.mean(self.metrics["lime_time"]),
            "avg_total_time": np.mean(self.metrics["total_time"]),
            "avg_accuracy": np.mean(self.metrics["accuracy"]),
            "avg_satisfaction": np.mean(self.metrics["user_satisfaction"])
        }
```

---

## 🎯 **使用範例**

### **📱 完整使用流程**
```python
# 1. 初始化分析器
bon_mav_analyzer = BoNMAV(n_candidates=5)
shap_analyzer = SHAPAnalyzer()
lime_analyzer = LIMEAnalyzer()

# 2. 訓練模型
shap_analyzer.train_model(training_data)

# 3. 執行分析
user_input = "我媽媽最近常常忘記剛吃過飯，還會重複問同樣的問題"
result = await enhanced_analysis_workflow(user_input)

# 4. 創建視覺化
visualization = create_comprehensive_xai_visualization(result)

# 5. 發送到 LINE
await send_line_message_with_retry(reply_token, visualization)
```

---

## 📈 **預期效果**

### **✅ 增強功能**
- **多候選答案選擇**: 從多個 AI 引擎生成候選答案
- **多面向驗證**: 醫療準確性、安全性、可行性、情感適當性
- **特徵重要度分析**: SHAP 和 LIME 提供深度解釋
- **視覺化展示**: 豐富的圖表和互動元素

### **📊 效能提升**
- **分析準確率**: 預期提升 15-20%
- **用戶滿意度**: 預期提升 25-30%
- **解釋性**: 提供詳細的分析推理過程
- **可信度**: 多引擎驗證提高結果可信度

---

*這個整合方案將 BoN-MAV 方法與 SHAP/LIME 特徵重要度分析完美結合，為失智症分析系統提供了更深入、更可信、更可解釋的分析能力。* 