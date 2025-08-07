# 🎨 LINE Flex Messages 實現指南

## 📋 概述

本指南介紹如何在您的 LINE Bot 中實現 Flex Messages，提供豐富的視覺化回應體驗。

## ✨ 主要功能

### 🎯 視覺化分析結果
- **彩色標題**: 根據分析模組使用不同顏色
- **風險等級顯示**: 直觀的風險評估
- **症狀列表**: 清晰的症狀描述
- **建議項目**: 實用的照護建議
- **免責聲明**: 專業醫療提醒

### 🎨 設計特色
- **響應式佈局**: 適配不同螢幕尺寸
- **模組化設計**: 支援多種分析類型
- **錯誤處理**: 優雅的錯誤提示
- **測試模式**: 安全的開發環境

## 🚀 實現方式

### 1. Flex Message 結構

```json
{
  "type": "flex",
  "altText": "失智症分析結果 - M1",
  "contents": {
    "type": "bubble",
    "size": "giga",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "🔍 M1 分析結果",
          "weight": "bold",
          "size": "lg",
          "color": "#FFFFFF"
        }
      ],
      "backgroundColor": "#FF6B6B",
      "paddingAll": "20px"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "spacing": "md",
      "contents": [
        {
          "type": "text",
          "text": "📋 可能症狀",
          "weight": "bold",
          "size": "md"
        },
        {
          "type": "text",
          "text": "• 記憶力減退\n• 語言障礙",
          "size": "sm",
          "color": "#666666",
          "wrap": true
        }
      ],
      "paddingAll": "20px"
    }
  }
}
```

### 2. 顏色配置

| 模組 | 顏色 | 用途 |
|------|------|------|
| M1 | #FF6B6B | 記憶力分析 |
| M2 | #4ECDC4 | 病程進展 |
| M3 | #45B7D1 | 行為心理症狀 |
| M4 | #96CEB4 | 照護資源 |
| 綜合 | #FFA07A | 綜合分析 |

### 3. 風險等級顏色

| 等級 | 顏色 | 含義 |
|------|------|------|
| Low | #4CAF50 | 低風險 |
| Medium | #FF9800 | 中等風險 |
| High | #F44336 | 高風險 |

## 🔧 使用方法

### 1. 啟動服務

```bash
# 測試模式
TEST_MODE=true python3 enhanced_m1_m2_m3_integrated_api_fixed.py

# 生產模式
python3 enhanced_m1_m2_m3_integrated_api_fixed.py
```

### 2. 測試 Flex Messages

```bash
python3 test_flex_messages.py
```

### 3. 發送測試訊息

```bash
curl -X POST http://localhost:8005/test-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "events": [{
      "type": "message",
      "message": {
        "type": "text",
        "text": "我最近常常忘記事情"
      },
      "source": {
        "type": "user",
        "userId": "Utestuser1"
      }
    }]
  }'
```

## 📊 分析模組

### M1 - 記憶力分析
- **症狀**: 記憶力減退、語言障礙、定向力下降
- **建議**: 就醫檢查、注意安全、建立提醒系統

### M2 - 病程進展
- **症狀**: 認知功能下降、行為改變、情緒波動
- **建議**: 認知訓練、環境安全、情緒支持

### M3 - 行為心理症狀
- **症狀**: 妄想、幻覺、攻擊行為
- **建議**: 藥物治療、行為療法、環境調整

### 綜合分析
- **範圍**: 涵蓋所有模組
- **建議**: 全面醫療評估、多面向照護

## 🛠️ 自定義配置

### 1. 修改顏色主題

```python
color_map = {
    "M1": "#FF6B6B",  # 自定義顏色
    "M2": "#4ECDC4",
    "M3": "#45B7D1",
    "M4": "#96CEB4",
    "comprehensive": "#FFA07A"
}
```

### 2. 調整佈局

```python
# 修改氣泡大小
"size": "giga"  # 可選: nano, micro, kilo, mega, giga

# 調整間距
"spacing": "md"  # 可選: none, xs, sm, md, lg, xl, xxl
```

### 3. 添加新模組

```python
def create_flex_message(analysis_result, module_type):
    # 添加新的模組類型
    if module_type == "M5":
        # 自定義 M5 模組的 Flex Message
        pass
```

## 🔍 故障排除

### 1. 常見問題

**Q: Flex Message 無法顯示**
- 檢查 LINE Bot 憑證是否正確
- 確認 Flex Message 格式是否符合規範
- 查看錯誤日誌

**Q: 顏色不正確**
- 確認顏色代碼格式為 #RRGGBB
- 檢查模組類型是否匹配

**Q: 測試模式無回應**
- 確認 TEST_MODE=true 環境變數
- 檢查控制台輸出

### 2. 調試技巧

```python
# 啟用詳細日誌
logging.basicConfig(level=logging.DEBUG)

# 檢查 Flex Message 結構
print(json.dumps(flex_message, indent=2, ensure_ascii=False))
```

## 📈 性能優化

### 1. 快取機制
- 快取常用的 Flex Message 模板
- 減少重複生成

### 2. 異步處理
- 使用異步函數處理大量請求
- 避免阻塞主線程

### 3. 錯誤恢復
- 實現優雅的錯誤處理
- 提供備用文字回應

## 🎯 最佳實踐

### 1. 設計原則
- 保持簡潔明瞭
- 使用一致的視覺語言
- 確保可讀性

### 2. 內容策略
- 提供實用的建議
- 包含專業醫療提醒
- 使用友善的語言

### 3. 測試策略
- 全面測試各種情況
- 驗證不同設備顯示
- 檢查無障礙訪問

## 🔮 未來擴展

### 1. 進階功能
- 互動式按鈕
- 圖片整合
- 動態內容

### 2. 個人化
- 用戶偏好設定
- 歷史記錄追蹤
- 個性化建議

### 3. 多語言支援
- 國際化支援
- 本地化內容
- 文化適應

## 📞 支援

如有問題或建議，請參考：
- LINE Bot API 文檔
- Flex Messages 規範
- 專案 GitHub 頁面

---

**🎉 恭喜！您已成功實現 LINE Flex Messages 功能！** 