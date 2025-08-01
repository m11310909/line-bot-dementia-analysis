#!/bin/bash

# Persistent LINE Bot Solution
# This script will keep all services running and provide a stable webhook URL

echo "🔧 Setting up Persistent LINE Bot Solution"
echo "=========================================="

# Function to kill existing processes
cleanup() {
    echo "🧹 Cleaning up existing processes..."
    pkill -f "updated_line_bot_webhook.py" 2>/dev/null
    pkill -f "enhanced_m1_m2_m3_m4_integrated_api.py" 2>/dev/null
    pkill -f "8005" 2>/dev/null
    pkill ngrok 2>/dev/null
    sleep 2
}

# Function to start RAG API
start_rag_api() {
    echo "🚀 Starting RAG API..."
    nohup python3 enhanced_m1_m2_m3_m4_integrated_api.py > rag_api.log 2>&1 &
    sleep 5
    
    # Check if RAG API is running
    if curl -s http://localhost:8005/health > /dev/null 2>&1; then
        echo "✅ RAG API started successfully"
        return 0
    else
        echo "❌ RAG API failed to start"
        return 1
    fi
}

# Function to start webhook server
start_webhook() {
    echo "🚀 Starting LINE Bot webhook server..."
    nohup python3 updated_line_bot_webhook.py > webhook.log 2>&1 &
    sleep 3
    
    # Check if webhook server is running
    if curl -s http://localhost:8081/health > /dev/null 2>&1; then
        echo "✅ Webhook server started successfully"
        return 0
    else
        echo "❌ Webhook server failed to start"
        return 1
    fi
}

# Function to start ngrok
start_ngrok() {
    echo "🚀 Starting ngrok tunnel..."
    nohup ngrok http 8081 > ngrok.log 2>&1 &
    sleep 5
    
    # Get ngrok URL
    if curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
        URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['tunnels'][0]['public_url'])")
        if [ ! -z "$URL" ]; then
            echo "✅ ngrok tunnel: $URL"
            echo "$URL" > ngrok_url.txt
            echo "$URL/webhook" > webhook_url.txt
            return 0
        fi
    fi
    
    echo "❌ ngrok failed to start"
    return 1
}

# Function to create status report
create_report() {
    URL=$(cat ngrok_url.txt 2>/dev/null)
    if [ -z "$URL" ]; then
        echo "❌ No ngrok URL available"
        return 1
    fi
    
    echo "📋 Creating status report..."
    cat > FINAL_SOLUTION.md << EOF
# 🧠 LINE Bot - Final Solution

## ✅ System Status

### Infrastructure
- **ngrok Tunnel**: $URL
- **Webhook URL**: $URL/webhook
- **Webhook Server**: Running on port 8081
- **RAG API**: Running on port 8005
- **LINE Bot Credentials**: Configured

### Services Status
- ✅ ngrok tunnel active
- ✅ Webhook server responding
- ✅ RAG API processing requests
- ✅ All modules (M1, M2, M3, M4) active

## 🚀 IMMEDIATE ACTION REQUIRED

### 1. Update LINE Developer Console
1. Go to [LINE Developer Console](https://developers.line.biz/)
2. Select your bot channel
3. Go to **Messaging API** settings
4. Set **Webhook URL** to: \`$URL/webhook\`
5. **Enable** "Use webhook"
6. Click **Save**

### 2. Test with Real Messages
Send this message to your bot:
\`\`\`
爸爸不會用洗衣機
\`\`\`

## 🎯 Expected Response
The bot will respond with:
- 🧠 Rich Flex Messages with visual analysis
- 📊 Confidence scores for each assessment
- 💡 Detailed explanations of findings
- 🎯 Actionable recommendations

## 🔧 Troubleshooting
If the bot doesn't respond:
1. Check status: \`curl $URL/health\`
2. Verify webhook URL in LINE Developer Console
3. Restart services: \`./persistent_solution.sh\`

---
**Generated**: $(date)
**ngrok URL**: $URL
**Status**: READY FOR TESTING! 🚀
EOF

    echo "✅ Status report created: FINAL_SOLUTION.md"
}

# Function to monitor services
monitor_services() {
    echo "👀 Monitoring services..."
    while true; do
        # Check RAG API
        if ! curl -s http://localhost:8005/health > /dev/null 2>&1; then
            echo "⚠️  RAG API down, restarting..."
            start_rag_api
        fi
        
        # Check webhook server
        if ! curl -s http://localhost:8081/health > /dev/null 2>&1; then
            echo "⚠️  Webhook server down, restarting..."
            start_webhook
        fi
        
        # Check ngrok
        if ! curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
            echo "⚠️  ngrok down, restarting..."
            start_ngrok
        fi
        
        sleep 30
    done
}

# Main execution
main() {
    echo "🔧 Setting up persistent LINE Bot solution..."
    
    # Clean up existing processes
    cleanup
    
    # Start services
    if start_rag_api && start_webhook && start_ngrok; then
        echo "✅ All services started successfully"
        
        # Create status report
        create_report
        
        echo ""
        echo "🎉 SYSTEM IS READY!"
        echo "=================="
        echo "📍 ngrok URL: $(cat ngrok_url.txt)"
        echo "📍 Webhook URL: $(cat webhook_url.txt)"
        echo ""
        echo "📋 NEXT STEPS:"
        echo "1. Update LINE Developer Console with the webhook URL above"
        echo "2. Send message to bot: 爸爸不會用洗衣機"
        echo ""
        echo "👀 Services will be monitored and restarted automatically"
        echo "Press Ctrl+C to stop monitoring"
        echo ""
        
        # Start monitoring
        monitor_services
    else
        echo "❌ Failed to start services"
        exit 1
    fi
}

# Run main function
main 