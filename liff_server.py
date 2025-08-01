#!/usr/bin/env python3
"""
Simple HTTP Server for LIFF Page
Serves the LIFF page locally for testing
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    # Change to liff directory
    os.chdir('liff')
    
    # Create server
    port = 8081
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
    
    print(f"🚀 LIFF Server starting on port {port}")
    print(f"📍 URL: http://localhost:{port}")
    print(f"📱 LIFF Page: http://localhost:{port}/index.html")
    print("=" * 50)
    print("💡 To test with LINE Bot:")
    print("   1. Update the button URL in RAG API to point to this server")
    print("   2. Use ngrok to expose this server to the internet")
    print("   3. Update your LINE Bot LIFF settings with the ngrok URL")
    print("=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    main() 