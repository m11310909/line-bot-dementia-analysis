#!/usr/bin/env python3
"""
啟動系統健康監控
持續監控系統狀態並生成報告
"""

import time
import signal
import sys
from system_health_monitor import SystemHealthMonitor

def signal_handler(signum, frame):
    """處理中斷信號"""
    print("\n🛑 收到中斷信號，正在停止監控...")
    if hasattr(start_monitoring, 'monitor'):
        start_monitoring.monitor.stop_monitoring()
    sys.exit(0)

def main():
    """主函數"""
    print("🚀 啟動系統健康監控")
    print("=" * 50)
    
    # 設置信號處理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 創建監控器
    config = {
        'log_file': 'logs/health_monitor.log',
        'check_interval': 30,  # 30秒檢查一次
        'memory_threshold': 80,
        'cpu_threshold': 80,
        'disk_threshold': 90,
        'port_check': [8000, 5000],
        'process_names': ['line_bot_demo', 'uvicorn', 'python']
    }
    
    monitor = SystemHealthMonitor(config)
    
    # 執行一次初始檢查
    print("📊 執行初始健康檢查...")
    initial_health = monitor.monitor_once()
    
    print(f"✅ 系統狀態:")
    print(f"   CPU: {initial_health.get('cpu_percent', 0):.1f}%")
    print(f"   內存: {initial_health.get('memory_percent', 0):.1f}%")
    print(f"   磁盤: {initial_health.get('disk_percent', 0):.1f}%")
    
    # 顯示進程狀態
    processes = initial_health.get('processes', {})
    print(f"   📋 進程狀態:")
    for proc_name, proc_info in processes.items():
        status_icon = "✅" if proc_info['status'] == 'running' else "❌"
        print(f"     {status_icon} {proc_name}: {proc_info['status']} ({proc_info['count']} 個進程)")
    
    # 顯示警報
    alerts = initial_health.get('alerts', [])
    if alerts:
        print(f"   ⚠️  警報 ({len(alerts)} 個):")
        for alert in alerts:
            level_icon = "🔴" if alert['level'] == 'CRITICAL' else "🟡"
            print(f"     {level_icon} {alert['message']}")
    else:
        print("   ✅ 無警報")
    
    print("\n🔄 開始持續監控 (每30秒檢查一次)")
    print("按 Ctrl+C 停止監控")
    print("-" * 50)
    
    # 開始持續監控
    monitor.start_monitoring()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 用戶中斷，正在停止監控...")
        monitor.stop_monitoring()
        print("✅ 監控已停止")

if __name__ == "__main__":
    main() 