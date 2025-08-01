#!/bin/bash

echo "🔧 Fixing LINE Bot SDK version conflicts..."

# Backup
cp enhanced_m1_m2_m3_integrated_api.py enhanced_m1_m2_m3_integrated_api.py.v2backup

# Fix: Remove v3 imports (keep v2 only)
sed -i '' '/from linebot.v3/d' enhanced_m1_m2_m3_integrated_api.py

# Fix: Replace v3 message creation with v2
sed -i '' 's/ReplyMessageRequest(//' enhanced_m1_m2_m3_integrated_api.py
sed -i '' 's/messages=\[flex_message\]/flex_message/' enhanced_m1_m2_m3_integrated_api.py

# Fix: Ensure proper v2 reply method
sed -i '' 's/line_bot_api.reply_message_async/line_bot_api.reply_message/' enhanced_m1_m2_m3_integrated_api.py

echo "✅ Fixed LINE Bot SDK conflicts"
echo "🚀 Restarting bot..."

# Kill existing process and restart
pkill -f python3
sleep 2
python3 enhanced_m1_m2_m3_integrated_api.py