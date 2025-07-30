#!/usr/bin/env python3
"""
解決端口衝突問題
"""

import os
import subprocess
import signal
import time

def find_process_on_port(port):
    """找到使用指定端口的進程"""
    try:
        result = subprocess.run(['lsof', '-ti', f':{port}'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        return []
    except Exception as e:
        print(f"❌ 無法檢查端口 {port}: {e}")
        return []

def kill_process(pid):
    """終止進程"""
    try:
        os.kill(int(pid), signal.SIGTERM)
        print(f"✅ 已終止進程 {pid}")
        return True
    except Exception as e:
        print(f"❌ 無法終止進程 {pid}: {e}")
        return False

def check_port_availability(port):
    """檢查端口是否可用"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def fix_port_conflict(port=8005):
    """解決端口衝突"""
    print(f"🔍 檢查端口 {port} 衝突...")
    
    # 找到使用端口的進程
    pids = find_process_on_port(port)
    
    if pids:
        print(f"⚠️  發現 {len(pids)} 個進程使用端口 {port}:")
        for pid in pids:
            if pid:
                print(f"  - PID: {pid}")
        
        # 詢問是否終止進程
        response = input(f"\n是否終止這些進程以釋放端口 {port}? (y/n): ")
        
        if response.lower() in ['y', 'yes', '是']:
            for pid in pids:
                if pid:
                    kill_process(pid)
            
            # 等待進程終止
            time.sleep(2)
            
            # 再次檢查端口
            if check_port_availability(port):
                print(f"✅ 端口 {port} 現在可用")
                return True
            else:
                print(f"❌ 端口 {port} 仍然被佔用")
                return False
        else:
            print("❌ 用戶取消操作")
            return False
    else:
        print(f"✅ 端口 {port} 可用")
        return True

def suggest_alternative_ports():
    """建議替代端口"""
    alternative_ports = [8006, 8007, 8008, 8009, 8010]
    
    print("\n💡 建議的替代端口:")
    for port in alternative_ports:
        if check_port_availability(port):
            print(f"  ✅ 端口 {port} 可用")
        else:
            print(f"  ❌ 端口 {port} 被佔用")
    
    return [port for port in alternative_ports if check_port_availability(port)]

def modify_api_port(new_port):
    """修改 API 端口"""
    print(f"\n🔧 修改 API 端口為 {new_port}...")
    
    # 檢查 API 檔案
    api_files = [
        'enhanced_m1_m2_m3_integrated_api.py',
        'm1_m2_m3_integrated_api.py',
        'integrated_m1_m2_api.py'
    ]
    
    for file in api_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    content = f.read()
                
                # 替換端口
                new_content = content.replace('8005', str(new_port))
                
                with open(file, 'w') as f:
                    f.write(new_content)
                
                print(f"✅ 已修改 {file} 端口為 {new_port}")
                
            except Exception as e:
                print(f"❌ 修改 {file} 失敗: {e}")

def main():
    """主函數"""
    print("🔧 端口衝突解決工具")
    print("=" * 50)
    
    # 嘗試解決端口 8005 衝突
    if fix_port_conflict(8005):
        print("\n✅ 端口衝突已解決！")
        print("現在可以啟動 API:")
        print("python3 enhanced_m1_m2_m3_integrated_api.py")
    else:
        print("\n❌ 無法解決端口 8005 衝突")
        
        # 建議替代端口
        available_ports = suggest_alternative_ports()
        
        if available_ports:
            new_port = available_ports[0]
            print(f"\n💡 建議使用端口 {new_port}")
            
            response = input(f"是否將 API 端口改為 {new_port}? (y/n): ")
            
            if response.lower() in ['y', 'yes', '是']:
                modify_api_port(new_port)
                print(f"\n✅ API 已修改為使用端口 {new_port}")
                print(f"現在可以啟動 API:")
                print(f"python3 enhanced_m1_m2_m3_integrated_api.py")
            else:
                print("❌ 用戶取消操作")
        else:
            print("\n❌ 沒有可用的替代端口")
            print("請手動終止佔用端口的進程")

if __name__ == "__main__":
    main() 