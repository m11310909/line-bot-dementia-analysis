# 🧠 XAI-Enhanced LINE Bot System

## 📋 Overview

This system enhances your existing LINE Bot with **Explainable AI (XAI)** visualization capabilities, providing users with transparent, interpretable responses for dementia-related queries.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   LINE Users    │───▶│  Enhanced LINE   │───▶│  XAI Wrapper    │
│                 │    │      Bot         │    │    Service      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Chatbot API     │    │  Visualization  │
                       │  (M1-M4 Modules) │    │   Generator     │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Start the Complete System

```bash
# Start all services
./start_xai_system.sh
```

### 2. Test the System

```bash
# Run comprehensive tests
python3 test_xai_system.py
```

### 3. Stop the System

```bash
# Stop all services
./stop_xai_system.sh
```

## 🔧 Services

### 1. Enhanced Chatbot API (Port 8008)
- **Purpose**: Core M1-M4 analysis modules
- **Features**: 
  - M1: Warning signs detection
  - M2: Progression stage assessment
  - M3: BPSD symptoms analysis
  - M4: Care navigation

### 2. XAI Wrapper Service (Port 8009)
- **Purpose**: Enhances chatbot responses with XAI visualization
- **Features**:
  - Keyword extraction and analysis
  - Intent classification
  - Confidence scoring
  - Module detection (M1-M4)
  - Visualization data generation

### 3. Enhanced LINE Bot (Port 8081)
- **Purpose**: LINE webhook handler with XAI integration
- **Features**:
  - Confidence-based response selection
  - Enhanced Flex Message generation
  - Fallback to original responses

## 🧠 XAI Features

### Module Detection
The system automatically detects which analysis module to use:

- **M1 (Warning Signs)**: Keywords like "忘記", "洗衣機", "瓦斯"
- **M2 (Progression)**: Keywords like "中度", "階段", "惡化"
- **M3 (BPSD)**: Keywords like "妄想", "躁動", "憂鬱"
- **M4 (Care)**: Keywords like "照護", "協助", "醫療"

### Confidence Scoring
- **High Confidence (≥0.6)**: Enhanced XAI visualization
- **Low Confidence (<0.6)**: Standard response with fallback

### Visualization Types
- **M1**: Comparison cards (normal aging vs warning signs)
- **M2**: Progression charts with stage indicators
- **M3**: Symptom analysis with severity levels
- **M4**: Care navigation with priority levels

## 📊 API Endpoints

### XAI Wrapper Service
```bash
# Health check
curl http://localhost:8009/health

# Analyze with XAI enhancement
curl -X POST http://localhost:8009/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "爸爸不會用洗衣機",
    "user_id": "test_user"
  }'
```

### Enhanced LINE Bot
```bash
# Health check
curl http://localhost:8081/health

# Webhook (for LINE platform)
POST https://your-ngrok-url.ngrok-free.app/webhook
```

## 🧪 Testing

### Manual Testing
```bash
# Test M1 (Warning Signs)
curl -X POST http://localhost:8009/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "爸爸不會用洗衣機", "user_id": "test_user"}'

# Test M2 (Progression)
curl -X POST http://localhost:8009/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "媽媽中度失智", "user_id": "test_user"}'

# Test M3 (BPSD)
curl -X POST http://localhost:8009/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "爺爺有妄想症狀", "user_id": "test_user"}'

# Test M4 (Care)
curl -X POST http://localhost:8009/analyze \
  -H "Content-Type: application/json" \
  -d '{"user_input": "需要醫療協助", "user_id": "test_user"}'
```

### Automated Testing
```bash
# Run comprehensive test suite
python3 test_xai_system.py
```

## ⚙️ Configuration

### Environment Variables
```bash
# LINE Bot Configuration
export LINE_CHANNEL_ACCESS_TOKEN="your_token"
export LINE_CHANNEL_SECRET="your_secret"

# XAI Configuration
export USE_XAI_WRAPPER=true
export XAI_WRAPPER_URL=http://localhost:8009/analyze
export CONFIDENCE_THRESHOLD=0.6
```

### Service URLs
- **Chatbot API**: `http://localhost:8008/analyze`
- **XAI Wrapper**: `http://localhost:8009/analyze`
- **LINE Bot**: `http://localhost:8081/webhook`

## 📁 File Structure

```
line-bot-dementia-analysis/
├── enhanced_chatbot_api.py          # M1-M4 Chatbot API
├── enhanced_line_bot_with_xai.py    # Enhanced LINE Bot
├── test_xai_system.py               # Test suite
├── start_xai_system.sh              # Startup script
├── stop_xai_system.sh               # Stop script
├── services/
│   └── xai-wrapper/
│       ├── app/
│       │   ├── main.py              # XAI Wrapper Service
│       │   └── flex_builder.py      # Flex Message Builder
│       ├── requirements.txt          # Dependencies
│       └── Dockerfile               # Container config
└── XAI_SYSTEM_README.md            # This file
```

## 🔍 Monitoring

### Health Checks
```bash
# Check all services
curl http://localhost:8008/health  # Chatbot API
curl http://localhost:8009/health  # XAI Wrapper
curl http://localhost:8081/health  # LINE Bot
```

### Logs
- **Chatbot API**: Check terminal output
- **XAI Wrapper**: Check terminal output
- **LINE Bot**: Check terminal output

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Stop existing processes
   ./stop_xai_system.sh
   # Restart
   ./start_xai_system.sh
   ```

2. **XAI Wrapper Not Responding**
   ```bash
   # Check if service is running
   curl http://localhost:8009/health
   # Restart if needed
   cd services/xai-wrapper
   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8009
   ```

3. **Module Detection Issues**
   - Check keyword patterns in `services/xai-wrapper/app/main.py`
   - Verify confidence thresholds
   - Review test cases in `test_xai_system.py`

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python3 enhanced_line_bot_with_xai.py
```

## 🎯 Benefits

### For Users
- **Transparency**: Understand how the system analyzes their input
- **Confidence**: See confidence levels for recommendations
- **Visualization**: Rich, informative Flex Messages
- **Trust**: Explainable AI builds user trust

### For Developers
- **Modularity**: Easy to extend with new modules
- **Maintainability**: Clean separation of concerns
- **Testability**: Comprehensive test suite
- **Scalability**: Microservices architecture

### For Healthcare
- **Accuracy**: Multi-module analysis improves accuracy
- **Compliance**: Transparent decision-making process
- **Education**: Users learn about dementia symptoms
- **Early Detection**: Better identification of warning signs

## 🔮 Future Enhancements

### Planned Features
- [ ] **Advanced NLP**: Integration with more sophisticated language models
- [ ] **Personalization**: User-specific analysis based on history
- [ ] **Multi-language**: Support for additional languages
- [ ] **Analytics**: Usage analytics and insights
- [ ] **Integration**: Connect with healthcare systems

### Technical Improvements
- [ ] **Caching**: Redis-based response caching
- [ ] **Load Balancing**: Multiple service instances
- [ ] **Monitoring**: Prometheus/Grafana integration
- [ ] **CI/CD**: Automated testing and deployment

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Run the test suite: `python3 test_xai_system.py`
3. Review logs for error messages
4. Check service health endpoints

---

**🎉 Congratulations!** Your LINE Bot now has advanced XAI capabilities that provide users with transparent, interpretable responses for dementia-related queries. 