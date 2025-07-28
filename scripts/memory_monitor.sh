#!/bin/bash

echo "📊 記憶體監控工具 (按 Ctrl+C 停止)"
echo "===================================="

while true; do
    python -c "
try:
    import psutil
    import datetime
    import gc

    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    now = datetime.datetime.now().strftime('%H:%M:%S')

    print(f'[{now}] 記憶體: {mem.percent:.1f}% ({mem.used/1024/1024:.0f}MB/{mem.total/1024/1024:.0f}MB) CPU: {cpu:.1f}%')

    if mem.percent > 85:
        print('⚠️ 記憶體使用過高，執行垃圾回收...')
        gc.collect()

    if mem.percent > 95:
        print('🚨 記憶體嚴重不足！')
except ImportError:
    print('psutil 未安裝，無法監控記憶體')
    exit(1)
except KeyboardInterrupt:
    print('監控已停止')
    exit(0)
" || break
    sleep 30
done
