#!/bin/bash

# Environment Setup Script for LINE Bot Dementia Analysis

echo "🔧 Setting up environment for LINE Bot..."

# Set Gemini API key (replace with your actual key)
export AISTUDIO_API_KEY=""

# Set RAG API URLs to match your working setup
export FLEX_API_URL="http://localhost:8004/m1-flex"
export RAG_HEALTH_URL="http://localhost:8004/health"
export RAG_ANALYZE_URL="http://localhost:8004/api/v1/analyze"

# Replit configuration (auto-detected)
export REPL_SLUG=${REPL_SLUG:-"workspace"}
export REPL_OWNER=${REPL_OWNER:-"ke2211975"}

echo "✅ Environment variables configured:"
echo "   AISTUDIO_API_KEY: ${AISTUDIO_API_KEY:0:20}..."
echo "   FLEX_API_URL: $FLEX_API_URL"
echo "   RAG_HEALTH_URL: $RAG_HEALTH_URL"
echo "   REPL_SLUG: $REPL_SLUG"
echo "   REPL_OWNER: $REPL_OWNER"

# Check LINE Bot credentials
if [ -z "$LINE_CHANNEL_ACCESS_TOKEN" ]; then
    echo "⚠️  LINE_CHANNEL_ACCESS_TOKEN not set"
    echo "   Please add it to Replit Secrets"
else
    echo "✅ LINE_CHANNEL_ACCESS_TOKEN configured"
fi

if [ -z "$LINE_CHANNEL_SECRET" ]; then
    echo "⚠️  LINE_CHANNEL_SECRET not set"
    echo "   Please add it to Replit Secrets"
else
    echo "✅ LINE_CHANNEL_SECRET configured"
fi

echo ""
echo "🚀 Environment ready! Now run:"
echo "   chmod +x start_system.sh"
echo "   ./start_system.sh"