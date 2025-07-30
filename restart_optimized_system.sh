#!/bin/bash
echo "🔄 重啟優化系統..."
./stop_optimized_system.sh
sleep 2
./start_optimized_system.sh
