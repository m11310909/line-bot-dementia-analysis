# 🚀 Quick Start Guide - LINE Bot Dementia Analysis System

## Prerequisites

Before starting, ensure you have:
- Docker and Docker Compose installed
- LINE Developer Account
- API keys for external services (Gemini, etc.)

## Step 1: Setup Environment

### 1.1 Clone and Setup
```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd line-bot-dementia-analysis

# Run the setup script
./setup.sh
```

### 1.2 Configure Environment Variables
```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file with your credentials
nano .env
```

Required environment variables:
```bash
# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
LIFF_ID=your_liff_id

# API Keys
GEMINI_API_KEY=your_gemini_api_key
BOT_API_URL=https://dementia-helper-api.com

# Database
DB_PASSWORD=secure_password_here
```

## Step 2: Start Services

### 2.1 Start All Services
```bash
# Start the complete system
./start.sh
```

This will:
- Build Docker images
- Start all services (LINE Bot, XAI Wrapper, Redis, PostgreSQL, Nginx)
- Wait for services to be healthy
- Display status information

### 2.2 Verify Services
```bash
# Check service health
curl http://localhost:8081/health  # LINE Bot
curl http://localhost:8005/health  # XAI Wrapper
```

## Step 3: Configure LINE Webhook

### 3.1 Get Public URL
```bash
# If using ngrok for development
ngrok http 80

# Note the HTTPS URL provided by ngrok
# Example: https://abc123.ngrok.io
```

### 3.2 Set LINE Webhook URL
1. Go to [LINE Developers Console](https://developers.line.biz/)
2. Select your channel
3. Go to Messaging API settings
4. Set Webhook URL to: `https://your-domain.com/webhook`
5. Enable "Use webhook"
6. Add webhook events: "Message"

## Step 4: Test the System

### 4.1 Run System Tests
```bash
# Test the XAI analysis system
python test_system.py
```

Expected output:
```
🧪 Testing XAI Analysis System...
✅ Input: 媽媽最近常常忘記吃藥
   Module: M1 (Expected: M1)
   Confidence: 85.00%

✅ Input: 失智症中期會有什麼症狀
   Module: M2 (Expected: M2)
   Confidence: 78.00%
```

### 4.2 Test LINE Bot
1. Add your LINE Bot as a friend
2. Send test messages:
   - "媽媽最近常常忘記吃藥"
   - "失智症中期會有什麼症狀"
   - "爸爸晚上很躁動怎麼辦"

## Step 5: Monitor and Debug

### 5.1 View Logs
```bash
# View all logs
./logs.sh

# View specific service logs
./logs.sh line-bot
./logs.sh xai-wrapper
```

### 5.2 Check Service Status
```bash
# Stop services
./stop.sh

# Restart services
./start.sh
```

## Troubleshooting

### Common Issues

#### 1. Environment Variables Missing
```bash
# Error: .env file not found
# Solution: Copy and configure .env.example
cp .env.example .env
# Edit .env with your actual credentials
```

#### 2. Docker Services Not Starting
```bash
# Check Docker status
docker-compose ps

# View detailed logs
docker-compose logs

# Restart specific service
docker-compose restart line-bot
```

#### 3. LINE Webhook Not Receiving Messages
```bash
# Verify webhook URL is accessible
curl -X POST https://your-domain.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'

# Check LINE Bot logs
./logs.sh line-bot
```

#### 4. XAI Service Not Responding
```bash
# Test XAI service directly
curl -X POST http://localhost:8005/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "測試訊息", "user_id": "test_user"}'

# Check XAI service logs
./logs.sh xai-wrapper
```

### Performance Issues

#### 1. Slow Response Times
```bash
# Check Redis connection
docker exec -it line-bot-dementia-analysis_redis_1 redis-cli ping

# Check database connection
docker exec -it line-bot-dementia-analysis_postgres_1 psql -U admin -d dementia_db -c "SELECT 1;"
```

#### 2. High Memory Usage
```bash
# Check container resource usage
docker stats

# Restart services to clear memory
./stop.sh && ./start.sh
```

## Development Mode

### Local Development Setup
```bash
# Install Python dependencies
pip install -r services/xai-wrapper/requirements.txt
pip install -r services/line-bot/requirements.txt

# Run services locally
uvicorn services.xai-wrapper.app.main:app --reload --port 8005
python services/line-bot/app/main.py
```

### Testing Individual Components
```bash
# Test module detection
python -c "
from services.xai_wrapper.app.module_detector import ModuleDetector
detector = ModuleDetector()
result = detector.detect('媽媽忘記吃藥', ['忘記', '吃藥'], 'symptom_check', {})
print(f'Detected module: {result}')
"

# Test XAI analyzer
python -c "
from services.xai_wrapper.app.xai_analyzer import XAIAnalyzer
import asyncio
analyzer = XAIAnalyzer()
result = asyncio.run(analyzer.analyze('測試', {}, 'M1'))
print(f'Analysis result: {result}')
"
```

## Production Deployment

### 1. SSL Configuration
```bash
# Add SSL certificates to ssl/ directory
cp your-cert.pem ssl/cert.pem
cp your-key.pem ssl/key.pem

# Update nginx.conf for HTTPS
```

### 2. Environment Variables for Production
```bash
# Use strong passwords
DB_PASSWORD=very_secure_password_here

# Use production API endpoints
BOT_API_URL=https://production-dementia-api.com

# Enable monitoring
ENABLE_MONITORING=true
```

### 3. Backup Strategy
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec line-bot-dementia-analysis_postgres_1 pg_dump -U admin dementia_db > backup_$DATE.sql
echo "Backup created: backup_$DATE.sql"
EOF
chmod +x backup.sh
```

## API Documentation

### XAI Analysis Endpoint
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "user_input": "媽媽最近常常忘記吃藥",
  "user_id": "user123",
  "context": {
    "previous_interactions": 5,
    "user_preferences": "detailed"
  }
}

Response:
{
  "module": "M1",
  "confidence": 0.85,
  "xai_analysis": {
    "reasoning_path": [...],
    "evidence": [...],
    "explanation": "..."
  },
  "visualization": {
    "type": "comparison_card",
    "flex_message": {...}
  }
}
```

### Health Check Endpoints
```bash
GET /health
# Returns service status

GET /api/v1/health
# Returns detailed health information
```

## Support and Maintenance

### Regular Maintenance Tasks
```bash
# Weekly: Check logs for errors
./logs.sh | grep ERROR

# Monthly: Update dependencies
docker-compose build --no-cache

# Quarterly: Review performance metrics
# Check database size and cache hit rates
```

### Monitoring Commands
```bash
# Check service status
docker-compose ps

# Monitor resource usage
docker stats

# View recent logs
./logs.sh | tail -100
```

## Success Metrics

Track these metrics to ensure system health:
- Response time < 3 seconds
- Error rate < 5%
- User satisfaction > 80%
- System uptime > 99%

## Next Steps

1. **Customize Modules**: Modify module detection patterns in `services/xai-wrapper/app/module_detector.py`
2. **Add Visualizations**: Enhance Flex Messages in `services/xai-wrapper/app/visualization_generator.py`
3. **Integrate External APIs**: Add more data sources in `services/xai-wrapper/app/main.py`
4. **Scale Services**: Configure load balancing and horizontal scaling
5. **Add Analytics**: Implement user behavior tracking and analytics

---

**Need Help?**
- Check the logs: `./logs.sh`
- Review the technical architecture: `TECHNICAL_ARCHITECTURE.md`
- Test individual components: `python test_system.py`
- Monitor system health: `curl http://localhost:8005/health` 