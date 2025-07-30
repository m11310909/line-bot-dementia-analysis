#!/usr/bin/env python3
import socket
import sys
import subprocess

def check_port(port):
    """檢查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def find_available_port(start_port=8000, max_attempts=10):
    """找到可用端口"""
    for port in range(start_port, start_port + max_attempts):
        if check_port(port):
            return port
    return None

def start_server():
    """啟動服務器"""
    # 嘗試找到可用端口
    available_port = find_available_port()
    
    if available_port:
        print(f"🚀 在端口 {available_port} 啟動服務...")
        
        # 修改 app.py 中的端口
        with open('app.py', 'r') as f:
            content = f.read()
        
        # 替換端口設定
        new_content = content.replace('port=8000', f'port={available_port}')
        
        with open('app.py', 'w') as f:
            f.write(new_content)
        
        print(f"✅ 已更新 app.py 端口為 {available_port}")
        print(f"📡 服務將在 http://localhost:{available_port} 啟動")
        
        # 啟動服務
        subprocess.run([sys.executable, 'app.py'])
    else:
        print("❌ 找不到可用端口，請手動停止其他服務")

if __name__ == "__main__":
    start_server()
