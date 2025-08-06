#!/bin/bash

# Start All Services Script
# This script starts all required services for the LINE Bot system

echo "🚀 Starting LINE Bot System Services"
echo "=================================="

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

# Function to kill processes on a port
kill_port() {
    local port=$1
    echo "🔄 Killing processes on port $port..."
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 2
}

# Function to start a service
start_service() {
    local service_name=$1
    local command=$2
    local port=$3
    
    echo ""
    echo "🔧 Starting $service_name..."
    
    # Check if port is available
    if ! check_port $port; then
        echo "🔄 Attempting to free port $port..."
        kill_port $port
        sleep 2
    fi
    
    # Start the service in background
    echo "📡 Running: $command"
    nohup $command > ${service_name}.log 2>&1 &
    local pid=$!
    
    # Wait a moment and check if it started
    sleep 3
    if ps -p $pid > /dev/null; then
        echo "✅ $service_name started (PID: $pid)"
        echo $pid > ${service_name}.pid
    else
        echo "❌ Failed to start $service_name"
        return 1
    fi
}

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your LINE Bot credentials:"
    echo "LINE_CHANNEL_SECRET=your_secret_here"
    echo "LINE_CHANNEL_ACCESS_TOKEN=your_token_here"
    exit 1
fi

echo "✅ .env file found"

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check required environment variables
if [ -z "$LINE_CHANNEL_SECRET" ] || [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "❌ Missing required LINE Bot credentials in .env"
    echo "Please add:"
    echo "LINE_CHANNEL_SECRET=your_secret_here"
    echo "LINE_CHANNEL_ACCESS_TOKEN=your_token_here"
    exit 1
fi

echo "✅ LINE Bot credentials found"

# Start RAG API Service (port 8005)
start_service "RAG API" "python3 rag_api_service.py" 8005

# Start Webhook Service (port 3000)
start_service "Webhook" "python3 updated_line_bot_webhook.py" 3000

# Start ngrok tunnel
echo ""
echo "🌐 Starting ngrok tunnel..."
if command -v ngrok &> /dev/null; then
    # Kill existing ngrok processes
    pkill -f ngrok 2>/dev/null || true
    sleep 2
    
    # Start ngrok
    nohup ngrok http 3000 > ngrok.log 2>&1 &
    ngrok_pid=$!
    echo "✅ ngrok started (PID: $ngrok_pid)"
    echo $ngrok_pid > ngrok.pid
    
    # Wait for ngrok to start
    echo "⏳ Waiting for ngrok to start..."
    sleep 5
    
    # Get ngrok URL
    if command -v curl &> /dev/null; then
        ngrok_url=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | head -1 | cut -d'"' -f4)
        if [ ! -z "$ngrok_url" ]; then
            echo "✅ ngrok URL: $ngrok_url"
            echo "📝 Update your LINE Bot webhook URL to: $ngrok_url/webhook"
        else
            echo "⚠️  ngrok URL not available yet, check ngrok.log"
        fi
    fi
else
    echo "❌ ngrok not installed. Please install ngrok first."
    echo "Visit: https://ngrok.com/download"
fi

echo ""
echo "🎉 All services started!"
echo ""
echo "📊 Service Status:"
echo "=================="
echo "RAG API: http://localhost:8005/health"
echo "Webhook: http://localhost:3000/health"
echo "ngrok: http://localhost:4040 (status page)"
echo ""
echo "🧪 Test your system:"
echo "python3 test_signature_verification.py"
echo "python3 service_status_check.py"
echo ""
echo "📝 Logs:"
echo "RAG API: rag_api_service.log"
echo "Webhook: updated_line_bot_webhook.log"
echo "ngrok: ngrok.log"
echo ""
echo "🛑 To stop all services:"
echo "./stop_all_services.sh" 