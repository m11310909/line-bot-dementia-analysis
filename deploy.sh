#!/bin/bash

echo "🚀 Starting Dockerized Microservices Deployment - Phase 2 Enhanced"
echo "================================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create .env file from env.example"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data shared/modules shared/utils docs

# Copy modules to shared directory
echo "📋 Copying modules to shared directory..."
cp -r modules/* shared/modules/ 2>/dev/null || echo "⚠️  No modules directory found, skipping..."

# Get external URL from .env or prompt user
EXTERNAL_URL=$(grep EXTERNAL_URL .env | cut -d '=' -f2)
if [ -z "$EXTERNAL_URL" ] || [ "$EXTERNAL_URL" = "https://your-ngrok-url.ngrok-free.app" ]; then
    echo ""
    echo "🌐 ngrok Configuration"
    echo "====================="
    echo "Please provide your ngrok URL:"
    read -p "Enter ngrok URL (e.g., https://abc123.ngrok-free.app): " ngrok_url
    
    if [ ! -z "$ngrok_url" ]; then
        sed -i.bak "s|EXTERNAL_URL=.*|EXTERNAL_URL=$ngrok_url|" .env
        EXTERNAL_URL=$ngrok_url
        echo "✅ Updated .env with ngrok URL"
    fi
fi

# Check GPU availability
echo "🔍 Checking GPU availability..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected"
    GPU_AVAILABLE=true
else
    echo "⚠️  No NVIDIA GPU detected, RAG service will use CPU"
    GPU_AVAILABLE=false
fi

echo "🔨 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Health checks
echo "🏥 Performing health checks..."

# Check LINE Bot service
if curl -f http://localhost:8081/health > /dev/null 2>&1; then
    echo "✅ LINE Bot Service: Healthy"
else
    echo "❌ LINE Bot Service: Unhealthy"
fi

# Check XAI Analysis service
if curl -f http://localhost:8005/health > /dev/null 2>&1; then
    echo "✅ XAI Analysis Service: Healthy"
else
    echo "❌ XAI Analysis Service: Unhealthy"
fi

# Check RAG Service
if curl -f http://localhost:8006/health > /dev/null 2>&1; then
    echo "✅ RAG Service: Healthy"
    if [ "$GPU_AVAILABLE" = true ]; then
        echo "🚀 GPU acceleration: Available"
    else
        echo "💻 GPU acceleration: Not available (using CPU)"
    fi
else
    echo "❌ RAG Service: Unhealthy"
fi

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U linebot_user > /dev/null 2>&1; then
    echo "✅ PostgreSQL: Healthy"
else
    echo "❌ PostgreSQL: Unhealthy"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Healthy"
else
    echo "❌ Redis: Unhealthy"
fi

echo ""
echo "📊 Service URLs:"
echo "   LINE Bot Webhook: $EXTERNAL_URL/webhook"
echo "   XAI Analysis: http://localhost:8005"
echo "   RAG Service: http://localhost:8006"
echo "   LIFF Frontend: http://localhost:3000"
echo "   PostgreSQL: localhost:5432"
echo "   Redis: localhost:6379"

echo ""
echo "🎯 Phase 2 Enhanced Features:"
echo "   ✅ GPU-accelerated RAG service"
echo "   ✅ Enhanced XAI visualization"
echo "   ✅ Non-linear module navigation"
echo "   ✅ Advanced Flex Messages"
echo "   ✅ Microservices architecture"

echo ""
echo "📋 Next Steps:"
echo "   1. Update LINE Developer Console webhook URL: $EXTERNAL_URL/webhook"
echo "   2. Test the bot by sending a message"
echo "   3. Monitor logs: docker-compose logs -f [service-name]"
echo "   4. Check GPU status: curl http://localhost:8006/gpu-status"

echo ""
echo "🔧 Useful Commands:"
echo "   - View all logs: docker-compose logs -f"
echo "   - Restart services: docker-compose restart"
echo "   - Stop all services: docker-compose down"
echo "   - Get webhook URL: curl http://localhost:8081/webhook-url"
echo "   - Check GPU status: curl http://localhost:8006/gpu-status"
echo "   - Test XAI features: curl http://localhost:8005/xai-features"

echo ""
echo "🎉 Phase 2 Deployment Complete!"
echo "================================================================"
