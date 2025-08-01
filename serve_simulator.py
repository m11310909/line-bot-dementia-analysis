#!/usr/bin/env python3
"""
Flex Message Simulator Server
提供本地 HTTP 服務器來展示 Flex Message 模擬器
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def serve_simulator():
    """啟動 Flex Message 模擬器服務器"""
    
    # 檢查文件是否存在
    simulator_file = Path("flex_message_simulator.html")
    if not simulator_file.exists():
        print("❌ flex_message_simulator.html 文件不存在")
        return
    
    # 設置端口
    PORT = 8080
    
    # 創建服務器
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Flex Message 模擬器服務器已啟動")
        print(f"📱 本地訪問地址: http://localhost:{PORT}/flex_message_simulator.html")
        print(f"🌐 網路訪問地址: http://0.0.0.0:{PORT}/flex_message_simulator.html")
        print("=" * 60)
        print("🎨 功能特色:")
        print("• 展示所有 M1-M4 模組的 Flex Message")
        print("• 互動式測試和預覽")
        print("• 即時 JSON 格式顯示")
        print("• 響應式設計，支援手機瀏覽")
        print("=" * 60)
        print("💡 使用說明:")
        print("1. 點擊模組卡片選擇要測試的模組")
        print("2. 輸入測試訊息或使用預設示例")
        print("3. 點擊測試按鈕查看 Flex Message 預覽")
        print("4. 可以顯示/隱藏 JSON 格式")
        print("=" * 60)
        
        # 自動打開瀏覽器
        try:
            webbrowser.open(f"http://localhost:{PORT}/flex_message_simulator.html")
            print("✅ 已自動打開瀏覽器")
        except:
            print("⚠️  無法自動打開瀏覽器，請手動訪問上述地址")
        
        print("\n🔄 服務器運行中... (按 Ctrl+C 停止)")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服務器已停止")

if __name__ == "__main__":
    serve_simulator() 