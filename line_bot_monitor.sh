#!/bin/bash

echo "🔍 LINE Bot Real-time Monitor"
echo "============================="
echo "Monitoring webhook and API activity..."
echo "(Press Ctrl+C to stop)"
echo ""

# Function to monitor a log file
monitor_log() {
    local service=$1
    local log_file=$2
    
    if [ -f "$log_file" ]; then
        echo "📄 Monitoring $service logs..."
        tail -f "$log_file" | while read line; do
            echo "[$service] $line"
        done &
    fi
}

# Monitor webhook server logs
echo "🔵 Webhook Server Activity:"
echo "---------------------------"
# Assuming logs are in standard locations - adjust paths as needed
tail -f webhook.log 2>/dev/null | sed 's/^/[WEBHOOK] /' &
WEBHOOK_PID=$!

echo ""
echo "🟢 RAG API Activity:"
echo "-------------------"
tail -f rag_api.log 2>/dev/null | sed 's/^/[RAG-API] /' &
RAG_PID=$!

# Monitor ngrok requests
echo ""
echo "🟣 ngrok Requests:"
echo "-----------------"
curl -s http://localhost:4040/api/requests | python3 -c "
import json, sys
data = json.load(sys.stdin)
for req in data.get('requests', [])[:5]:
    print(f\"[{req['start'][:19]}] {req['method']} {req['uri']} - {req['response_status']}\")
"

# Keep script running
echo ""
echo "🎯 Send a message to your LINE bot to see activity..."
echo ""

# Trap Ctrl+C to clean up
trap "kill $WEBHOOK_PID $RAG_PID 2>/dev/null; echo ''; echo 'Monitor stopped.'; exit" INT

# Keep monitoring
while true; do
    sleep 1
done 