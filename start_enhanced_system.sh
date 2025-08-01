#!/bin/bash

# Enhanced M1-M4 Visualization System Startup Script
# Version: 2.0.0

echo "🎨 Enhanced M1-M4 Visualization System"
echo "======================================"
echo "Starting redesigned visualization system..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required files exist
required_files=(
    "enhanced_flex_message_generator.py"
    "enhanced_m1_m2_m3_m4_integrated_api.py"
    "test_enhanced_visualization.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file not found: $file"
        exit 1
    fi
done

echo "✅ All required files found"
echo ""

# Check if port 8006 is available
if lsof -Pi :8006 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 8006 is already in use"
    echo "   Stopping existing process..."
    pkill -f "enhanced_m1_m2_m3_m4_integrated_api.py" || true
    sleep 2
fi

echo "🚀 Starting Enhanced API on port 8006..."
echo ""

# Start the enhanced API in background
python3 enhanced_m1_m2_m3_m4_integrated_api.py &
API_PID=$!

# Wait for API to start
echo "⏳ Waiting for API to start..."
sleep 5

# Test API health
echo "🧪 Testing API health..."
if curl -s http://localhost:8006/health > /dev/null; then
    echo "✅ API is running successfully"
else
    echo "❌ API failed to start"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Enhanced System Started Successfully!"
echo "========================================"
echo ""
echo "📊 API Endpoints:"
echo "   • Health Check: http://localhost:8006/health"
echo "   • Design System: http://localhost:8006/design-system"
echo "   • API Docs: http://localhost:8006/docs"
echo ""
echo "🧪 Test Endpoints:"
echo "   • M1 Analysis: POST http://localhost:8006/analyze/M1"
echo "   • M2 Analysis: POST http://localhost:8006/analyze/M2"
echo "   • M3 Analysis: POST http://localhost:8006/analyze/M3"
echo "   • M4 Analysis: POST http://localhost:8006/analyze/M4"
echo ""
echo "📱 Flex Message Endpoints:"
echo "   • M1 Flex: POST http://localhost:8006/flex/M1"
echo "   • M2 Flex: POST http://localhost:8006/flex/M2"
echo "   • M3 Flex: POST http://localhost:8006/flex/M3"
echo "   • M4 Flex: POST http://localhost:8006/flex/M4"
echo ""
echo "🧪 Quick Test:"
echo "   curl -X POST http://localhost:8006/flex/M1 \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"text\": \"我媽媽最近記憶力變差\"}'"
echo ""
echo "📋 Management Commands:"
echo "   • View logs: tail -f nohup.out"
echo "   • Stop API: pkill -f enhanced_m1_m2_m3_m4_integrated_api.py"
echo "   • Test system: python3 test_enhanced_visualization.py"
echo ""
echo "🎨 Features:"
echo "   ✅ Enhanced Flex Message Design"
echo "   ✅ Senior-friendly Typography"
echo "   ✅ Progressive Information Disclosure"
echo "   ✅ Confidence Indicators"
echo "   ✅ LIFF Integration Ready"
echo ""
echo "📈 System Status:"
echo "   • API PID: $API_PID"
echo "   • Port: 8006"
echo "   • Status: Running"
echo ""

# Save PID for easy management
echo $API_PID > .enhanced_api.pid

echo "💡 Next Steps:"
echo "   1. Test the API endpoints above"
echo "   2. Integrate with your LINE Bot webhook"
echo "   3. Update your webhook to use port 8006"
echo "   4. Test with real user messages"
echo ""

# Keep script running and show logs
echo "📝 API Logs (Ctrl+C to stop):"
echo "================================"
tail -f nohup.out 2>/dev/null || echo "No logs available yet" 