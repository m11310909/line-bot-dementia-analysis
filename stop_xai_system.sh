#!/bin/bash

# 🛑 XAI Enhanced System Stop Script

echo "🛑 Stopping XAI Enhanced System..."

# Stop processes by PID if available
if [ -f .chatbot_pid ]; then
    CHATBOT_PID=$(cat .chatbot_pid)
    echo "🔄 Stopping Chatbot API (PID: $CHATBOT_PID)..."
    kill $CHATBOT_PID 2>/dev/null || true
    rm .chatbot_pid
fi

if [ -f .xai_pid ]; then
    XAI_PID=$(cat .xai_pid)
    echo "🔄 Stopping XAI Wrapper Service (PID: $XAI_PID)..."
    kill $XAI_PID 2>/dev/null || true
    rm .xai_pid
fi

if [ -f .bot_pid ]; then
    BOT_PID=$(cat .bot_pid)
    echo "🔄 Stopping Enhanced LINE Bot (PID: $BOT_PID)..."
    kill $BOT_PID 2>/dev/null || true
    rm .bot_pid
fi

# Stop processes by name
echo "🔄 Stopping processes by name..."
pkill -f "enhanced_chatbot_api.py" || true
pkill -f "enhanced_line_bot_with_xai.py" || true
pkill -f "xai-wrapper" || true
pkill -f "uvicorn.*8008" || true
pkill -f "uvicorn.*8009" || true
pkill -f "uvicorn.*8081" || true

# Wait a moment for processes to stop
sleep 3

# Check if ports are free
echo "🔍 Checking if ports are free..."
for port in 8008 8009 8081; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is still in use"
    else
        echo "✅ Port $port is free"
    fi
done

echo "✅ XAI Enhanced System stopped successfully!" 