#!/bin/bash

# Stop All Services Script
# This script stops all LINE Bot system services

echo "🛑 Stopping LINE Bot System Services"
echo "==================================="

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file="${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            echo "🔄 Stopping $service_name (PID: $pid)..."
            kill $pid
            sleep 2
            if ps -p $pid > /dev/null 2>&1; then
                echo "🔄 Force killing $service_name..."
                kill -9 $pid
            fi
            echo "✅ $service_name stopped"
        else
            echo "⚠️  $service_name not running"
        fi
        rm -f "$pid_file"
    else
        echo "⚠️  No PID file found for $service_name"
    fi
}

# Stop RAG API Service
stop_service "rag_api_service"

# Stop Webhook Service
stop_service "updated_line_bot_webhook"

# Stop ngrok
echo ""
echo "🌐 Stopping ngrok..."
if [ -f "ngrok.pid" ]; then
    ngrok_pid=$(cat ngrok.pid)
    if ps -p $ngrok_pid > /dev/null 2>&1; then
        kill $ngrok_pid
        echo "✅ ngrok stopped"
    else
        echo "⚠️  ngrok not running"
    fi
    rm -f ngrok.pid
else
    echo "⚠️  No ngrok PID file found"
fi

# Kill any remaining Python processes related to our services
echo ""
echo "🧹 Cleaning up remaining processes..."
pkill -f "rag_api_service.py" 2>/dev/null || true
pkill -f "updated_line_bot_webhook.py" 2>/dev/null || true
pkill -f "ngrok" 2>/dev/null || true

echo ""
echo "✅ All services stopped!"
echo ""
echo "📊 Port Status:"
echo "==============="
echo "Port 8005 (RAG API): $(lsof -i :8005 >/dev/null 2>&1 && echo "❌ Still in use" || echo "✅ Free")"
echo "Port 3000 (Webhook): $(lsof -i :3000 >/dev/null 2>&1 && echo "❌ Still in use" || echo "✅ Free")"
echo "Port 4040 (ngrok): $(lsof -i :4040 >/dev/null 2>&1 && echo "❌ Still in use" || echo "✅ Free")" 