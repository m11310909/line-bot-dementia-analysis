# 📄 API 回應格式與範例（Log 協作參考）

所有模組回傳格式皆統一為 `BaseResponse` 結構：

```json
{
  "status": "success",
  "module": "M1",
  "data": { ... },  // 模組特有資料
  "meta": {
    "confidence_score": 0.85
  }
}
