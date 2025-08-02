#!/bin/bash

# 🚀 Dockerized Microservices Deployment Script with ngrok support

echo "🚀 Starting Dockerized Microservices Deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp env.example .env
    echo "📝 Please edit .env file with your actual credentials"
    echo "   - LINE_CHANNEL_ACCESS_TOKEN"
    echo "   - LINE_CHANNEL_SECRET"
    echo "   - EXTERNAL_URL (ngrok URL)"
    echo "   - LIFF_ID (optional)"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs data shared/modules nginx/ssl

# Copy existing modules to shared directory
echo "📋 Copying existing modules..."
cp -r modules/* shared/modules/ 2>/dev/null || echo "⚠️  No existing modules found"

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🏥 Checking service health..."
services=("line-bot" "xai-analysis" "rag-service" "postgres" "redis")

for service in "${services[@]}"; do
    echo "Checking $service..."
    if docker-compose ps $service | grep -q "Up"; then
        echo "✅ $service is running"
    else
        echo "❌ $service failed to start"
    fi
done

# Get external URL from .env or prompt user
EXTERNAL_URL=$(grep EXTERNAL_URL .env | cut -d '=' -f2)
if [ -z "$EXTERNAL_URL" ] || [ "$EXTERNAL_URL" = "https://your-ngrok-url.ngrok-free.app" ]; then
    echo ""
    echo "🌐 ngrok Configuration"
    echo "====================="
    echo "Please provide your ngrok URL:"
    read -p "Enter ngrok URL (e.g., https://abc123.ngrok-free.app): " ngrok_url
    
    if [ ! -z "$ngrok_url" ]; then
        # Update .env file with ngrok URL
        sed -i.bak "s|EXTERNAL_URL=.*|EXTERNAL_URL=$ngrok_url|" .env
        EXTERNAL_URL=$ngrok_url
        echo "✅ Updated .env with ngrok URL"
    fi
fi

# Display service URLs
echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📊 Service URLs:"
echo "   LINE Bot Webhook: $EXTERNAL_URL/webhook"
echo "   XAI Analysis: http://localhost:8005"
echo "   RAG Service: http://localhost:8006"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"
echo ""
echo "📋 Next steps:"
echo "   1. Update LINE Developer Console webhook URL to: $EXTERNAL_URL/webhook"
echo "   2. Test the bot with: 爸爸不會用洗衣機"
echo "   3. Check logs: docker-compose logs -f"
echo ""
echo "🛠️  Useful commands:"
echo "   - View logs: docker-compose logs -f [service_name]"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Update services: docker-compose up --build -d"
echo "   - Get webhook URL: curl http://localhost:8081/webhook-url"
