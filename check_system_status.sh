#!/bin/bash
echo "📊 系統狀態檢查..."
echo "🔧 Redis 狀態:"
brew services list | grep redis
echo ""
echo "🌐 API 狀態:"
curl -s http://localhost:8005/health | python3 -m json.tool 2>/dev/null || echo "API 未運行"
echo ""
echo "💾 快取統計:"
curl -s http://localhost:8005/cache/stats | python3 -m json.tool 2>/dev/null || echo "無法獲取快取統計"
