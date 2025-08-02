#!/bin/bash

# 🚀 XAI Enhanced System Startup Script
# This script starts all services for the XAI-enhanced LINE Bot system

echo "🚀 Starting XAI Enhanced System..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        echo "✅ Port $port is available"
        return 0
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo "🔄 Stopping process on port $port..."
    pkill -f ":$port" || true
    sleep 2
}

# Stop existing processes
echo "🛑 Stopping existing processes..."
pkill -f "enhanced_chatbot_api.py" || true
pkill -f "enhanced_line_bot_with_xai.py" || true
pkill -f "xai-wrapper" || true
sleep 3

# Check and free ports
echo "🔍 Checking ports..."
check_port 8008 || kill_port 8008
check_port 8009 || kill_port 8009
check_port 8081 || kill_port 8081

# Start Chatbot API (port 8008)
echo "🤖 Starting Enhanced Chatbot API on port 8008..."
python3 enhanced_chatbot_api.py &
CHATBOT_PID=$!
sleep 3

# Check if chatbot API started successfully
if curl -s http://localhost:8008/health > /dev/null; then
    echo "✅ Chatbot API started successfully"
else
    echo "❌ Failed to start Chatbot API"
    exit 1
fi

# Start XAI Wrapper Service (port 8009)
echo "🧠 Starting XAI Wrapper Service on port 8009..."
cd services/xai-wrapper
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8009 &
XAI_PID=$!
cd ../..
sleep 3

# Check if XAI wrapper started successfully
if curl -s http://localhost:8009/health > /dev/null; then
    echo "✅ XAI Wrapper Service started successfully"
else
    echo "❌ Failed to start XAI Wrapper Service"
    exit 1
fi

# Start Enhanced LINE Bot (port 8081)
echo "📱 Starting Enhanced LINE Bot with XAI on port 8081..."
export USE_XAI_WRAPPER=true
export XAI_WRAPPER_URL=http://localhost:8009/analyze
export CONFIDENCE_THRESHOLD=0.6
python3 enhanced_line_bot_with_xai.py &
BOT_PID=$!
sleep 3

# Check if LINE Bot started successfully
if curl -s http://localhost:8081/health > /dev/null; then
    echo "✅ Enhanced LINE Bot started successfully"
else
    echo "❌ Failed to start Enhanced LINE Bot"
    exit 1
fi

# Display system status
echo ""
echo "🎉 XAI Enhanced System Started Successfully!"
echo "=============================================="
echo "📍 Services:"
echo "   🤖 Chatbot API: http://localhost:8008/health"
echo "   🧠 XAI Wrapper: http://localhost:8009/health"
echo "   📱 LINE Bot: http://localhost:8081/health"
echo ""
echo "🔗 Webhook URL: https://4edba6125304.ngrok-free.app/webhook"
echo ""
echo "🧪 Test the system:"
echo "   curl -X POST http://localhost:8009/analyze \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"user_input\": \"爸爸不會用洗衣機\", \"user_id\": \"test_user\"}'"
echo ""
echo "📊 System Status:"
curl -s http://localhost:8008/health | jq '.status' 2>/dev/null || echo "Chatbot API: Running"
curl -s http://localhost:8009/health | jq '.status' 2>/dev/null || echo "XAI Wrapper: Running"
curl -s http://localhost:8081/health | jq '.status' 2>/dev/null || echo "LINE Bot: Running"
echo ""
echo "🔄 To stop the system, run: ./stop_xai_system.sh"
echo ""

# Save PIDs for later cleanup
echo $CHATBOT_PID > .chatbot_pid
echo $XAI_PID > .xai_pid
echo $BOT_PID > .bot_pid

echo "✅ All services started. System is ready!" 