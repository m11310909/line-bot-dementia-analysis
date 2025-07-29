# 一鍵部署腳本：start.sh（含 ngrok 模式）
```bash
#!/usr/bin/env bash
set -e

# 一鍵部署 Dementia Care Bot（不使用 Deploy，改用 ngrok 暴露）
# 1. 安裝依賴
# 2. 停止舊伺服器佔用
# 3. 啟動伺服器（背景執行）
# 4. 啟動 ngrok 並顯示 Webhook URL

PORT=${PORT:-3000}

# 1. 安裝依賴
echo "📦 安裝 npm 與 ngrok..."
npm install
npm install ngrok -g || true

echo "✅ 安裝完成"

# 2. 殺掉舊佔用（保險處理）
if command -v lsof &> /dev/null; then
  PIDS=$(lsof -t -i :$PORT || true)
  if [ -n "$PIDS" ]; then
    echo "⚠️ Port $PORT 被佔用，終止：$PIDS"
    kill -9 $PIDS
  fi
fi

# 3. 啟動伺服器（背景模式）
echo "🚀 背景啟動伺服器 port=$PORT..."
node main.js &
sleep 2

# 4. 啟動 ngrok 並顯示公開網址
echo "🌐 啟動 ngrok 連接外部..."
ngrok http $PORT || echo "❌ 無法啟動 ngrok，請檢查安裝是否成功"
```

# 更新 .replit 配置（不需部署）
```toml
entrypoint = "start.sh"
modules = ["nodejs-20", "python-3.11"]

[deployment]
run = ["bash", "start.sh"]
deploymentTarget = "cloudrun"

[[ports]]
localPort = 3000
externalPort = 3000
```
