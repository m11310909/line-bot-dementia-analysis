"""
系統健康監控腳本
監控系統狀態、性能和錯誤
"""
import os
import psutil
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import threading
import json

class SystemHealthMonitor:
    """系統健康監控器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {
            'log_file': 'logs/health_monitor.log',
            'check_interval': 30,  # 秒
            'memory_threshold': 80,  # %
            'cpu_threshold': 80,   # %
            'disk_threshold': 90,  # %
            'port_check': [8000, 5000],
            'process_names': ['line_bot_demo', 'uvicorn']
        }
        
        self.setup_logging()
        self.health_data = []
        self.alerts = []
        self.monitoring = False
        
    def setup_logging(self):
        """設置日誌"""
        log_dir = os.path.dirname(self.config['log_file'])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config['log_file']),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_system_resources(self) -> Dict:
        """檢查系統資源使用情況"""
        try:
            # CPU 使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 內存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盤使用率
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 進程數量
            process_count = len(psutil.pids())
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk_percent,
                'disk_free_gb': disk.free / (1024**3),
                'process_count': process_count
            }
        except Exception as e:
            self.logger.error(f"系統資源檢查失敗: {e}")
            return {}
    
    def check_ports(self) -> Dict:
        """檢查端口狀態"""
        port_status = {}
        
        for port in self.config['port_check']:
            try:
                # 檢查端口是否被佔用
                connections = psutil.net_connections()
                port_in_use = any(conn.laddr.port == port for conn in connections 
                                if conn.laddr)
                port_status[port] = 'in_use' if port_in_use else 'available'
            except Exception as e:
                self.logger.warning(f"端口 {port} 檢查失敗: {e}")
                port_status[port] = 'unknown'
        
        return port_status
    
    def check_processes(self) -> Dict:
        """檢查關鍵進程狀態"""
        process_status = {}
        
        for proc_name in self.config['process_names']:
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                    # 檢查進程名稱和命令行
                    proc_info = proc.info
                    proc_name_lower = proc_name.lower()
                    
                    # 檢查進程名稱
                    name_match = proc_name_lower in proc_info['name'].lower()
                    
                    # 檢查命令行參數
                    cmdline_match = False
                    if proc_info['cmdline']:
                        cmdline_str = ' '.join(proc_info['cmdline']).lower()
                        cmdline_match = proc_name_lower in cmdline_str
                    
                    if name_match or cmdline_match:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cmdline': proc_info['cmdline'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent']
                        })
                
                process_status[proc_name] = {
                    'count': len(processes),
                    'processes': processes,
                    'status': 'running' if processes else 'not_running'
                }
            except Exception as e:
                self.logger.warning(f"進程 {proc_name} 檢查失敗: {e}")
                process_status[proc_name] = {'status': 'unknown', 'error': str(e)}
        
        return process_status
    
    def check_log_errors(self) -> Dict:
        """檢查日誌中的錯誤"""
        error_patterns = [
            "ERROR",
            "CRITICAL",
            "Exception",
            "Traceback",
            "Failed",
            "Error"
        ]
        
        log_files = [
            'logs/xai_flex.log',
            'logs/app.log',
            'logs/error.log'
        ]
        
        error_summary = {
            'total_errors': 0,
            'recent_errors': [],
            'error_types': {}
        }
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        # 只讀取最後1000行
                        lines = f.readlines()[-1000:]
                    
                    for line in lines:
                        for pattern in error_patterns:
                            if pattern in line:
                                error_summary['total_errors'] += 1
                                
                                # 記錄最近的錯誤
                                if len(error_summary['recent_errors']) < 10:
                                    error_summary['recent_errors'].append({
                                        'file': log_file,
                                        'line': line.strip(),
                                        'pattern': pattern
                                    })
                                
                                # 統計錯誤類型
                                error_summary['error_types'][pattern] = \
                                    error_summary['error_types'].get(pattern, 0) + 1
                                break
                                
                except Exception as e:
                    self.logger.warning(f"讀取日誌文件 {log_file} 失敗: {e}")
        
        return error_summary
    
    def generate_alerts(self, health_data: Dict) -> List[Dict]:
        """生成健康警報"""
        alerts = []
        
        # CPU 警報
        if 'cpu_percent' in health_data and health_data['cpu_percent'] > self.config['cpu_threshold']:
            alerts.append({
                'type': 'CPU_HIGH',
                'level': 'WARNING',
                'message': f"CPU使用率過高: {health_data['cpu_percent']:.1f}%",
                'threshold': self.config['cpu_threshold']
            })
        
        # 內存警報
        if 'memory_percent' in health_data and health_data['memory_percent'] > self.config['memory_threshold']:
            alerts.append({
                'type': 'MEMORY_HIGH',
                'level': 'WARNING',
                'message': f"內存使用率過高: {health_data['memory_percent']:.1f}%",
                'threshold': self.config['memory_threshold']
            })
        
        # 磁盤警報
        if 'disk_percent' in health_data and health_data['disk_percent'] > self.config['disk_threshold']:
            alerts.append({
                'type': 'DISK_HIGH',
                'level': 'CRITICAL',
                'message': f"磁盤使用率過高: {health_data['disk_percent']:.1f}%",
                'threshold': self.config['disk_threshold']
            })
        
        # 進程警報
        if 'processes' in health_data:
            for proc_name, proc_info in health_data['processes'].items():
                if proc_info['status'] == 'not_running':
                    alerts.append({
                        'type': 'PROCESS_DOWN',
                        'level': 'CRITICAL',
                        'message': f"關鍵進程未運行: {proc_name}",
                        'process': proc_name
                    })
        
        # 錯誤警報
        if 'log_errors' in health_data and health_data['log_errors']['total_errors'] > 10:
            alerts.append({
                'type': 'HIGH_ERROR_RATE',
                'level': 'WARNING',
                'message': f"錯誤日誌過多: {health_data['log_errors']['total_errors']} 個錯誤",
                'error_count': health_data['log_errors']['total_errors']
            })
        
        return alerts
    
    def collect_health_data(self) -> Dict:
        """收集完整的健康數據"""
        health_data = {
            'timestamp': datetime.now().isoformat(),
            'system_resources': self.check_system_resources(),
            'ports': self.check_ports(),
            'processes': self.check_processes(),
            'log_errors': self.check_log_errors()
        }
        
        # 展平資源數據到頂層
        if health_data['system_resources']:
            health_data.update(health_data['system_resources'])
        
        # 生成警報
        alerts = self.generate_alerts(health_data)
        health_data['alerts'] = alerts
        
        return health_data
    
    def save_health_report(self, health_data: Dict):
        """保存健康報告"""
        report_file = f"logs/health_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            # 讀取現有數據
            if os.path.exists(report_file):
                with open(report_file, 'r', encoding='utf-8') as f:
                    reports = json.load(f)
            else:
                reports = []
            
            # 添加新數據
            reports.append(health_data)
            
            # 只保留最近100條記錄
            reports = reports[-100:]
            
            # 保存數據
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(reports, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"保存健康報告失敗: {e}")
    
    def monitor_once(self):
        """執行一次健康檢查"""
        try:
            health_data = self.collect_health_data()
            
            # 記錄基本信息
            self.logger.info(f"系統健康檢查 - CPU: {health_data.get('cpu_percent', 0):.1f}%, "
                           f"內存: {health_data.get('memory_percent', 0):.1f}%, "
                           f"磁盤: {health_data.get('disk_percent', 0):.1f}%")
            
            # 記錄警報
            for alert in health_data.get('alerts', []):
                if alert['level'] == 'CRITICAL':
                    self.logger.critical(alert['message'])
                elif alert['level'] == 'WARNING':
                    self.logger.warning(alert['message'])
            
            # 保存數據
            self.health_data.append(health_data)
            self.save_health_report(health_data)
            
            return health_data
            
        except Exception as e:
            self.logger.error(f"健康檢查失敗: {e}")
            return {}
    
    def start_monitoring(self):
        """開始持續監控"""
        self.monitoring = True
        self.logger.info("開始系統健康監控")
        
        def monitor_loop():
            while self.monitoring:
                try:
                    self.monitor_once()
                    time.sleep(self.config['check_interval'])
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"監控循環錯誤: {e}")
                    time.sleep(5)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        return monitor_thread
    
    def stop_monitoring(self):
        """停止監控"""
        self.monitoring = False
        self.logger.info("停止系統健康監控")

# 使用示例
if __name__ == "__main__":
    monitor = SystemHealthMonitor()
    
    # 執行一次檢查
    health_data = monitor.monitor_once()
    print(json.dumps(health_data, indent=2, ensure_ascii=False))
    
    # 或開始持續監控
    # monitor.start_monitoring()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     monitor.stop_monitoring() 