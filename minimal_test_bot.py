from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Minimal Bot is running!"

@app.route('/callback', methods=['POST'])
def callback():
    print("✅ Webhook received!")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body: {request.get_data(as_text=True)}")
    return '', 200

if __name__ == '__main__':
    print("🚀 Starting minimal test bot on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
