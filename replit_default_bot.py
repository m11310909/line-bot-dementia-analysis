from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Default Replit Bot!"

@app.route('/callback', methods=['POST'])
def callback():
    print("✅ Webhook received!")
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # Use Replit's default port or fallback
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
