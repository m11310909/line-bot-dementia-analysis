#!/bin/bash

echo "🔄 重啟 ngrok 隧道..."

# 停止現有的 ngrok
./ngrok_stop.sh

# 等待進程完全停止
sleep 2

# 重新啟動
./setup_ngrok_enhanced.sh 