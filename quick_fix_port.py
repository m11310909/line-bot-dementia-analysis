#!/usr/bin/env python3
"""
快速解決端口衝突
"""

import os
import subprocess
import time

def kill_port_8005():
    """終止端口 8005 的進程"""
    print("🔧 終止端口 8005 的進程...")
    
    try:
        # 找到使用端口 8005 的進程
        result = subprocess.run(['lsof', '-ti', ':8005'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"發現 {len(pids)} 個進程使用端口 8005")
            
            # 終止所有進程
            for pid in pids:
                if pid.strip():
                    try:
                        subprocess.run(['kill', '-9', pid.strip()], 
                                     capture_output=True)
                        print(f"✅ 已終止進程 {pid}")
                    except Exception as e:
                        print(f"❌ 無法終止進程 {pid}: {e}")
            
            # 等待進程終止
            time.sleep(2)
            print("✅ 端口 8005 已釋放")
            return True
        else:
            print("✅ 端口 8005 沒有被佔用")
            return True
            
    except Exception as e:
        print(f"❌ 檢查端口失敗: {e}")
        return False

def change_port_to_8006():
    """將 API 端口改為 8006"""
    print("🔧 將 API 端口改為 8006...")
    
    try:
        with open('enhanced_m1_m2_m3_integrated_api.py', 'r') as f:
            content = f.read()
        
        # 替換端口
        new_content = content.replace('8005', '8006')
        
        with open('enhanced_m1_m2_m3_integrated_api.py', 'w') as f:
            f.write(new_content)
        
        print("✅ API 端口已改為 8006")
        return True
        
    except Exception as e:
        print(f"❌ 修改端口失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 快速解決端口衝突")
    print("=" * 30)
    
    # 選項 1: 終止佔用端口的進程
    print("\n選項 1: 終止佔用端口 8005 的進程")
    if kill_port_8005():
        print("\n✅ 現在可以啟動 API:")
        print("python3 enhanced_m1_m2_m3_integrated_api.py")
        return
    
    # 選項 2: 改用端口 8006
    print("\n選項 2: 改用端口 8006")
    if change_port_to_8006():
        print("\n✅ 現在可以啟動 API (端口 8006):")
        print("python3 enhanced_m1_m2_m3_integrated_api.py")
        print("\n📝 注意: API 現在運行在端口 8006")
        return
    
    print("\n❌ 無法解決端口衝突")

if __name__ == "__main__":
    main() 