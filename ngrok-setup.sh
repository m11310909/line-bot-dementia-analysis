#!/bin/bash

# 🌐 ngrok Setup Script for Dockerized LINE Bot

echo "🌐 Setting up ngrok for Dockerized LINE Bot..."

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install ngrok first."
    echo "   Download from: https://ngrok.com/download"
    exit 1
fi

# Check if Docker services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Docker services are not running. Please start them first:"
    echo "   ./deploy.sh"
    exit 1
fi

# Kill existing ngrok processes
echo "🧹 Killing existing ngrok processes..."
pkill ngrok 2>/dev/null || true
sleep 2

# Start ngrok tunnel
echo "🚀 Starting ngrok tunnel..."
ngrok http 8081 > ngrok.log 2>&1 &

# Wait for ngrok to start
echo "⏳ Waiting for ngrok to start..."
sleep 10

# Get ngrok URL
echo "🔍 Getting ngrok URL..."
for i in {1..30}; do
    ngrok_url=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)
    if [ ! -z "$ngrok_url" ] && [ "$ngrok_url" != "null" ]; then
        echo "✅ ngrok URL: $ngrok_url"
        break
    fi
    sleep 2
done

if [ -z "$ngrok_url" ] || [ "$ngrok_url" = "null" ]; then
    echo "❌ Failed to get ngrok URL"
    echo "📋 Check ngrok.log for details"
    exit 1
fi

# Update .env file
echo "📝 Updating .env file with ngrok URL..."
sed -i.bak "s|EXTERNAL_URL=.*|EXTERNAL_URL=$ngrok_url|" .env

# Restart LINE Bot service to pick up new URL
echo "🔄 Restarting LINE Bot service..."
docker-compose restart line-bot

# Wait for service to restart
sleep 10

# Test webhook URL
echo "🧪 Testing webhook URL..."
webhook_url="$ngrok_url/webhook"
if curl -s "$webhook_url" > /dev/null; then
    echo "✅ Webhook URL is accessible"
else
    echo "⚠️  Webhook URL might not be accessible yet"
fi

echo ""
echo "🎉 ngrok setup completed!"
echo ""
echo "📊 Current Configuration:"
echo "   ngrok URL: $ngrok_url"
echo "   Webhook URL: $webhook_url"
echo ""
echo "📋 Next steps:"
echo "   1. Update LINE Developer Console webhook URL to: $webhook_url"
echo "   2. Test the bot with: 爸爸不會用洗衣機"
echo "   3. Monitor ngrok: tail -f ngrok.log"
echo ""
echo "🛠️  Useful commands:"
echo "   - View ngrok logs: tail -f ngrok.log"
echo "   - Get webhook URL: curl http://localhost:8081/webhook-url"
echo "   - Stop ngrok: pkill ngrok"
echo "   - Restart ngrok: ./ngrok-setup.sh" 