from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot running on port 80!"

@app.route('/callback', methods=['POST'])
def callback():
    print("✅ Webhook received!")
    return {"status": "ok"}, 200

if __name__ == '__main__':
    print("🚀 Starting bot on port 80...")
    app.run(host='0.0.0.0', port=80, debug=False)
