#!/bin/bash
echo "🚀 Starting LINE Bot Dementia Analysis System..."

# Check environment
if [ ! -f .env ]; then
    echo "❌ .env file not found! Copy .env.example to .env and fill in values."
    exit 1
fi

# Load environment variables
export $(cat .env | xargs)

# Start services
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check health
echo "🔍 Checking service health..."
curl -s http://localhost:8081/health
curl -s http://localhost:8005/health

echo "✅ System is running!"
echo "📱 LINE Webhook: http://localhost:8081/webhook"
echo "🧠 XAI API: http://localhost:8005/api/v1/analyze"
