#!/bin/bash

# Complete Startup Script for LINE Bot Dementia Analysis System
# This script starts both RAG API and LINE Bot webhook properly

echo "🚀 Starting LINE Bot Dementia Analysis System..."
echo "=" * 60

# Kill any existing Python processes
echo "🔄 Cleaning up existing processes..."
pkill -f python
sleep 2

# Check if environment variables are set
echo "📍 Checking environment variables..."
if [ -z "$AISTUDIO_API_KEY" ]; then
    echo "❌ AISTUDIO_API_KEY not set"
    echo "Please run: export AISTUDIO_API_KEY='your-api-key-here'"
    exit 1
else
    echo "✅ AISTUDIO_API_KEY configured"
fi

if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "❌ LINE_CHANNEL_ACCESS_TOKEN not set"
    echo "Please set LINE Bot credentials in Replit Secrets"
else
    echo "✅ LINE_CHANNEL_ACCESS_TOKEN configured"
fi

if [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "❌ LINE_CHANNEL_SECRET not set"
    echo "Please set LINE Bot credentials in Replit Secrets"
else
    echo "✅ LINE_CHANNEL_SECRET configured"
fi

echo ""
echo "🔧 Starting services..."

# Start RAG API on port 8004
echo "1️⃣ Starting RAG API service..."
if [ -f "integrated_m1_m2_api_8004.py" ]; then
    PORT=8004 nohup python integrated_m1_m2_api_8004.py > rag_api.log 2>&1 &
    RAG_PID=$!
    echo "   ✅ RAG API started (PID: $RAG_PID) on port 8004"
elif [ -f "m1_m2_integrated_rag.py" ]; then
    PORT=8004 nohup python m1_m2_integrated_rag.py > rag_api.log 2>&1 &
    RAG_PID=$!
    echo "   ✅ RAG API started (PID: $RAG_PID) on port 8004"
else
    echo "   ❌ RAG API file not found"
    exit 1
fi

# Wait for RAG API to start
echo "   ⏳ Waiting for RAG API to initialize..."
sleep 5

# Check if RAG API is responding
for i in {1..10}; do
    if curl -s http://localhost:8004/health > /dev/null 2>&1; then
        echo "   ✅ RAG API is responding"
        break
    elif [ $i -eq 10 ]; then
        echo "   ❌ RAG API failed to start"
        exit 1
    else
        echo "   ⏳ Waiting for RAG API... (attempt $i/10)"
        sleep 2
    fi
done

# Start LINE Bot webhook
echo "2️⃣ Starting LINE Bot webhook..."
if [ -f "working_webhook.py" ]; then
    PORT=3000 python working_webhook.py
elif [ -f "updated_line_bot_webhook.py" ]; then
    # Update the environment variables for the existing webhook
    export FLEX_API_URL="http://localhost:8004/m1-flex"
    export RAG_HEALTH_URL="http://localhost:8004/health"
    export RAG_ANALYZE_URL="http://localhost:8004/api/v1/analyze"
    PORT=3000 python updated_line_bot_webhook.py
else
    echo "   ❌ Webhook file not found"
    exit 1
fi

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $RAG_PID 2>/dev/null
    pkill -f python
    echo "   ✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo ""
echo "🎉 System started successfully!"
echo "📍 RAG API: http://localhost:8004"
echo "📍 LINE Webhook: http://localhost:3000"
echo "📍 Public URL: https://$REPL_SLUG.$REPL_OWNER.repl.co"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep script running
wait