# M1-M3 模組 LINE 測試指南

## 📋 概述

本指南提供完整的 M1-M3 模組測試方法，包括：
- **M1**: 失智症十大警訊識別
- **M2**: 病程階段分析  
- **M3**: BPSD 行為心理症狀分析

## 🚀 快速開始

### 1. 自動測試腳本

```bash
# 執行完整測試
./test_m1_m2_m3_on_line.sh

# 或手動執行
python3 test_m1_m2_m3_modules.py
```

### 2. LINE Bot 專用測試

```bash
# 測試 LINE Bot 整合
python3 test_line_bot_modules.py

# 指定 LINE Bot URL
python3 test_line_bot_modules.py http://localhost:5000
```

## 📊 模組功能說明

### M1 模組：失智症十大警訊
- **功能**: 識別失智症早期警訊
- **測試案例**:
  - "媽媽常忘記關瓦斯"
  - "爸爸會迷路找不到回家的路"
  - "奶奶忘記吃藥"
  - "爺爺無法處理財務"

### M2 模組：病程階段分析
- **功能**: 分析失智症病程階段
- **測試案例**:
  - 輕度: "可以自己洗澡但需要提醒吃藥"
  - 中度: "需要協助穿衣，會迷路，晚上不睡覺"
  - 重度: "已經不認得家人，需要餵食"

### M3 模組：BPSD 行為心理症狀
- **功能**: 分析行為心理症狀
- **測試案例**:
  - 妄想: "懷疑有人偷東西"
  - 幻覺: "看到已故的親人"
  - 激動: "大聲叫罵，推人"
  - 憂鬱: "整天悶悶不樂，擔心"
  - 睡眠: "晚上不睡覺，到處走動"

## 🔧 手動測試步驟

### 步驟 1: 啟動 API 服務

```bash
# 啟動 M1-M2-M3 整合 API
python3 m1_m2_m3_integrated_api.py &

# 等待服務啟動
sleep 15

# 檢查服務狀態
curl http://localhost:8005/health
```

### 步驟 2: 測試 API 端點

```bash
# 測試健康檢查
curl http://localhost:8005/health

# 測試模組狀態
curl http://localhost:8005/modules/status

# 測試綜合分析
curl -X POST http://localhost:8005/comprehensive-analysis \
  -H "Content-Type: application/json" \
  -d '{"user_input": "媽媽常忘記關瓦斯"}'
```

### 步驟 3: 測試 LINE Bot

```bash
# 啟動 LINE Bot
python3 updated_line_bot_webhook.py &

# 測試 LINE Bot 健康狀態
curl http://localhost:5000/health
```

## 📱 LINE 實際測試

### 測試訊息範例

#### M1 警訊測試
```
媽媽常忘記關瓦斯
爸爸會迷路找不到回家的路
奶奶忘記吃藥
爺爺無法處理財務
外婆對時間地點感到混亂
```

#### M2 階段測試
```
可以自己洗澡但需要提醒吃藥
需要協助穿衣，會迷路，晚上不睡覺
已經不認得家人，需要餵食
```

#### M3 BPSD 測試
```
懷疑有人偷東西
看到已故的親人
大聲叫罵，推人
整天悶悶不樂，擔心
晚上不睡覺，到處走動
```

### 預期回應

#### M1 回應範例
```
🚨 檢測到失智症警訊
📋 症狀: 記憶力減退
⚠️  建議: 請盡快就醫評估
```

#### M2 回應範例
```
🏥 病程階段分析
📊 檢測階段: 中度失智症
💡 照護建議: 需要全天候照顧
```

#### M3 回應範例
```
🧠 BPSD 症狀分析
🔍 檢測症狀: 妄想症狀
💊 建議: 諮詢精神科醫師
```

## 🔍 故障排除

### 常見問題

#### 1. API 服務無法啟動
```bash
# 檢查端口是否被佔用
lsof -i :8005

# 停止佔用端口的程序
pkill -f "m1_m2_m3_integrated_api"

# 重新啟動
python3 m1_m2_m3_integrated_api.py
```

#### 2. LINE Bot 無法回應
```bash
# 檢查 LINE Bot 配置
cat updated_line_bot_webhook.py | grep -A 5 "CHANNEL_ACCESS_TOKEN"

# 檢查 webhook URL 設置
curl -X POST https://api.line.me/v2/bot/channel/webhook/test \
  -H "Authorization: Bearer YOUR_CHANNEL_ACCESS_TOKEN"
```

#### 3. 模組載入失敗
```bash
# 檢查資料檔案
ls -la data/chunks/

# 重新生成 M2 資料
python3 create_m2_data.py

# 重新生成 M3 資料
python3 create_m3_data.py
```

### 日誌檢查

```bash
# 檢查 API 日誌
tail -f logs/api.log

# 檢查 LINE Bot 日誌
tail -f logs/line_bot.log

# 檢查錯誤日誌
grep -i error logs/*.log
```

## 📊 測試報告範例

```
🚀 M1-M3 模組完整測試
==================================================
測試時間: 2024-01-15 14:30:25
測試目標: http://localhost:8005

✅ 通過 健康檢查
✅ 通過 模組狀態
✅ 通過 M1 警訊識別
✅ 通過 M2 階段分析
✅ 通過 M3 BPSD 症狀
✅ 通過 Flex Message
✅ 通過 LINE Bot 整合

==================================================
📊 測試報告
==================================================
總測試數: 7
通過數: 7
失敗數: 0
成功率: 100.0%

🎉 所有測試通過！M1-M3 模組運行正常
```

## 🎯 進階測試

### 效能測試

```bash
# 壓力測試
ab -n 100 -c 10 -p test_data.json -T application/json \
   http://localhost:8005/comprehensive-analysis
```

### 整合測試

```bash
# 執行完整整合測試
python3 enhanced/integration_testing_suite.py
```

### 自動化測試

```bash
# 設定自動測試
crontab -e

# 每小時執行一次測試
0 * * * * cd /path/to/project && ./test_m1_m2_m3_on_line.sh >> test.log 2>&1
```

## 📞 支援

如果遇到問題，請檢查：

1. **環境配置**: Python 3.7+, 必要套件
2. **API 服務**: 端口 8005 是否正常
3. **LINE Bot**: Channel Token 和 Webhook URL
4. **資料檔案**: M1-M3 知識庫檔案
5. **網路連接**: 確保可以訪問 LINE API

## 🔄 更新日誌

- **v1.0**: 初始版本，支援 M1-M3 基本測試
- **v1.1**: 新增 LINE Bot 專用測試
- **v1.2**: 新增自動化測試腳本
- **v1.3**: 新增故障排除指南 