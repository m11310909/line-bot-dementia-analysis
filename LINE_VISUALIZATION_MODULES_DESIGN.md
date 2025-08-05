# 🎨 LINE 視覺化模組設計文檔

## 📊 分析結果摘要

基於 LINE Simulator 分析，失智小幫手系統的回應格式統計：
- **總測試數**: 40 個回應
- **Flex Message**: 38 個 (95%)
- **文字回應**: 2 個 (5%)
- **混合格式**: 0 個

## 🎯 4組優化視覺化模組設計

### 1. 🚨 M1 警訊監控儀表板

#### 📋 當前格式分析
- **回應類型**: Flex Message (100%)
- **常見元素**: 🚨, 🎯 AI 信心度, 🧠 推理路徑, 💬 失智小幫手
- **結構**: Header + Body + Footer (100%)

#### 🎨 優化視覺化設計

**佈局**: 垂直輪播卡片 (Vertical Carousel)

**組件設計**:
```json
{
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "🚨 警訊監控儀表板",
        "weight": "bold",
        "color": "#ffffff",
        "size": "lg"
      }
    ],
    "backgroundColor": "#E74C3C"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "風險等級",
            "size": "sm",
            "color": "#666666"
          },
          {
            "type": "text",
            "text": "🔴 高風險",
            "size": "sm",
            "color": "#E74C3C",
            "weight": "bold"
          }
        ]
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "📋 檢測症狀",
            "weight": "bold",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
              {
                "type": "text",
                "text": "✅ 忘記關瓦斯",
                "size": "xs",
                "color": "#27AE60"
              },
              {
                "type": "text",
                "text": "✅ 重複問問題",
                "size": "xs",
                "color": "#27AE60"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "立即諮詢",
          "data": "action=consult_emergency"
        },
        "style": "primary",
        "color": "#E74C3C"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "記錄症狀",
          "data": "action=record_symptoms"
        },
        "style": "secondary"
      }
    ]
  }
}
```

**視覺化特色**:
- 🚨 警報燈號系統 (紅/黃/綠)
- 📊 症狀嚴重程度圖表
- ⏰ 時間軸症狀追蹤
- 🎯 風險評估儀表板

---

### 2. 📊 M2 病程階段評估

#### 📋 當前格式分析
- **回應類型**: Flex Message (100%)
- **常見元素**: 📊, 🎯 AI 信心度, 🧠 推理路徑, 💬 失智小幫手
- **結構**: Header + Body + Footer (100%)

#### 🎨 優化視覺化設計

**佈局**: 水平進度條 (Horizontal Progress)

**組件設計**:
```json
{
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "📊 病程階段評估",
        "weight": "bold",
        "color": "#ffffff",
        "size": "lg"
      }
    ],
    "backgroundColor": "#E67E22"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "當前階段",
            "size": "sm",
            "color": "#666666"
          },
          {
            "type": "text",
            "text": "🟡 中度失智",
            "size": "lg",
            "weight": "bold",
            "color": "#E67E22"
          }
        ]
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "📈 進展程度",
            "weight": "bold",
            "size": "sm"
          },
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
                    "text": "輕度",
                    "size": "xs",
                    "color": "#27AE60"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "中度",
                    "size": "xs",
                    "color": "#E67E22",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "重度",
                    "size": "xs",
                    "color": "#E74C3C"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "詳細評估",
          "data": "action=detailed_assessment"
        },
        "style": "primary",
        "color": "#E67E22"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "預後分析",
          "data": "action=prognosis_analysis"
        },
        "style": "secondary"
      }
    ]
  }
}
```

**視覺化特色**:
- 📈 病程進展圖表
- 🎯 階段評估儀表板
- 📊 認知功能雷達圖
- ⏳ 預後時間軸

---

### 3. 🧠 M3 BPSD 症狀分析

#### 📋 當前格式分析
- **回應類型**: Flex Message (100%)
- **常見元素**: 🧠, 🎯 AI 信心度, 🧠 推理路徑, 💬 失智小幫手
- **結構**: Header + Body + Footer (100%)

#### 🎨 優化視覺化設計

**佈局**: 網格卡片 (Grid Cards)

**組件設計**:
```json
{
  "type": "bubble",
  "size": "kilo",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "🧠 BPSD 症狀分析",
        "weight": "bold",
        "color": "#ffffff",
        "size": "lg"
      }
    ],
    "backgroundColor": "#9B59B6"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "檢測症狀",
            "weight": "bold",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "🔴 妄想症狀",
                    "size": "xs",
                    "color": "#E74C3C"
                  },
                  {
                    "type": "text",
                    "text": "嚴重度: 高",
                    "size": "xs",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "🟡 攻擊行為",
                    "size": "xs",
                    "color": "#E67E22"
                  },
                  {
                    "type": "text",
                    "text": "嚴重度: 中",
                    "size": "xs",
                    "color": "#666666"
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "💊 治療建議",
            "weight": "bold",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "spacing": "xs",
            "contents": [
              {
                "type": "text",
                "text": "🏥 藥物治療",
                "size": "xs",
                "color": "#3498DB"
              },
              {
                "type": "text",
                "text": "🧘 行為療法",
                "size": "xs",
                "color": "#3498DB"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "症狀追蹤",
          "data": "action=symptom_tracking"
        },
        "style": "primary",
        "color": "#9B59B6"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "治療方案",
          "data": "action=treatment_plan"
        },
        "style": "secondary"
      }
    ]
  }
}
```

**視覺化特色**:
- 🧠 症狀分類圖表
- 📊 行為頻率統計
- 🎯 症狀嚴重度評估
- 💊 藥物反應追蹤

---

### 4. 🏥 M4 照護資源導航

#### 📋 當前格式分析
- **回應類型**: Flex Message (80%) + 文字回應 (20%)
- **常見元素**: 🏥, M4 照護需求, AI 驅動的照護需求識別, 📋 需求評估
- **結構**: Header + Body + Footer (80%)

#### 🎨 優化視覺化設計

**佈局**: 垂直列表 (Vertical List)

**組件設計**:
```json
{
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
        "color": "#ffffff",
        "size": "lg"
      }
    ],
    "backgroundColor": "#3498DB"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "📋 需求評估",
            "weight": "bold",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "醫療協助需求",
            "size": "xs",
            "color": "#666666"
          }
        ]
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "🏥 可用資源",
            "weight": "bold",
            "size": "sm"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "🏥 醫療機構",
                    "size": "xs",
                    "color": "#27AE60"
                  },
                  {
                    "type": "text",
                    "text": "(5家)",
                    "size": "xs",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "👨‍⚕️ 照護服務",
                    "size": "xs",
                    "color": "#27AE60"
                  },
                  {
                    "type": "text",
                    "text": "(3項)",
                    "size": "xs",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "🤝 社會支持",
                    "size": "xs",
                    "color": "#27AE60"
                  },
                  {
                    "type": "text",
                    "text": "(4項)",
                    "size": "xs",
                    "color": "#666666"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "立即諮詢",
          "data": "action=consult_resources"
        },
        "style": "primary",
        "color": "#3498DB"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "預約服務",
          "data": "action=book_service"
        },
        "style": "secondary"
      }
    ]
  }
}
```

**視覺化特色**:
- 🏥 資源地圖視覺化
- 📞 聯絡資訊卡片
- 💰 費用估算工具
- 📅 預約排程系統

---

## 🎯 互動模式設計

### 通用互動模式
1. **點擊展開詳細資訊**: 長按卡片顯示完整分析
2. **滑動查看多個選項**: 左右滑動切換不同視角
3. **長按顯示操作選單**: 長按按鈕顯示更多選項
4. **搖晃重新整理內容**: 搖晃手機更新最新資訊

### 模組特定互動
- **M1**: 點擊症狀項目查看詳細說明
- **M2**: 滑動進度條查看不同階段
- **M3**: 點擊症狀卡片查看治療建議
- **M4**: 點擊資源項目查看詳細資訊

---

## 📊 視覺化優化建議總結

### 🎨 設計原則
1. **一致性**: 統一的視覺語言和互動模式
2. **可讀性**: 清晰的資訊層次和字體大小
3. **可操作性**: 直觀的按鈕和手勢操作
4. **個性化**: 根據用戶需求調整顯示內容

### 🚀 實施建議
1. **分階段實施**: 先實現核心功能，再逐步優化
2. **用戶測試**: 收集真實用戶反饋進行迭代
3. **性能優化**: 確保載入速度和響應時間
4. **無障礙設計**: 考慮不同用戶群體的需求

---

**設計完成時間**: 2025-08-03  
**版本**: 1.0.0  
**狀態**: 完成設計，準備實施 