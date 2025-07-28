#!/usr/bin/env bash

set -e

# get_webhook.sh: Start Flask server, establish localhost.run tunnel, and output webhook URL.
# Assumes user has SSH key at ~/.ssh/id_rsa (protected by ssh-agent or passphrase prompt).

# 1. Start Flask server in the background
echo "🚀 啟動 Flask server..."
# Use python3 explicitly
env python3 app.py > flask.log 2>&1 &
FLASK_PID=$!

# Give Flask time to start
sleep 2

# 2. Start SSH tunnel using openssh from nix-shell
echo "🌐 建立 localhost.run 隧道..."
nix-shell -p openssh --run \
  "ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no \
       -o UserKnownHostsFile=/dev/null \
       -R 80:localhost:5000 ssh.localhost.run 2>&1 | tee tunnel.log" &
TUNNEL_PID=$!

# Wait briefly for tunnel setup
sleep 3

# 3. Extract public URL from tunnel log
WEBHOOK_URL=$(grep -Eo "https?://[a-zA-Z0-9.-]+\\.lhr\\.life" tunnel.log | head -n1)

if [[ -z "$WEBHOOK_URL" ]]; then
  echo "❌ 無法取得 webhook URL，請確認隧道與 SSH 金鑰設定是否正確。"
  kill $TUNNEL_PID $FLASK_PID 2>/dev/null || true
  exit 1
fi

# 4. Output the webhook URL
echo "✅ 你的公開 Webhook URL："
echo "$WEBHOOK_URL/webhook"

# 5. Clean up on exit
trap "echo 'Stopping...'; kill $TUNNEL_PID $FLASK_PID; exit" SIGINT SIGTERM

# 6. Keep script alive to maintain processes
echo "📡 正在接收 webhook...（按 Ctrl+C 可停止）"
wait $TUNNEL_PID
