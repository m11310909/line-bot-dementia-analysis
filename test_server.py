from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="LINE Bot 失智症分析系統 - 測試版")

@app.get("/")
async def root():
    return HTMLResponse(content="""
    <html>
        <head>
            <title>LINE Bot 失智症分析系統</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .header { background: #00B900; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .module { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; background: white; }
                .status { color: #00B900; font-weight: bold; }
                .flex-demo { border: 2px solid #00B900; padding: 20px; margin: 20px 0; border-radius: 10px; background: white; }
                .button { background: #00B900; color: white; padding: 10px 20px; border: none; border-radius: 5px; margin: 5px; text-decoration: none; display: inline-block; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🧠 LINE Bot 失智症警訊分析系統</h1>
                <p>✅ 系統運行中 - 10個視覺化模組已載入</p>
                <p>📱 支援 Flex Message 和 LIFF 應用</p>
            </div>
            
            <div class="flex-demo">
                <h2>📋 Flex Message 使用者界面預覽</h2>
                <div style="border: 1px solid #ccc; padding: 15px; border-radius: 8px; background: #f9f9f9;">
                    <h3 style="color: #1DB446; margin-top: 0;">🧠 失智症警訊分析結果</h3>
                    
                    <p><strong>🔸 使用者描述：</strong></p>
                    <p style="color: #666; margin-left: 20px;">媽媽最近常重複問同樣的問題</p>
                    
                    <hr style="margin: 20px 0;">
                    
                    <p><strong style="color: #00B900;">✅ 正常老化現象：</strong></p>
                    <p style="color: #666; margin-left: 20px;">偶爾忘記約會或朋友名字，但能夠自己想起來</p>
                    
                    <p><strong style="color: #FF5551;">⚠️ 警訊分析 (M1-01)：</strong></p>
                    <p style="color: #666; margin-left: 20px;">重複詢問可能顯示短期記憶問題，建議諮詢專業醫師進行評估</p>
                    
                    <a href="#liff-demo" class="button">📱 詳細資訊 (LIFF)</a>
                </div>
            </div>
            
            <h2>🔧 失智症十大警訊模組狀態</h2>
            <div class="module">
                <h3>M1-01: 記憶力減退影響生活</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-02: 計劃事情或解決問題有困難</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-03: 無法勝任原本熟悉的事務</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-04: 對時間地點感到混淆</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-05: 有困難理解視覺影像和空間關係</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-06: 言語表達或書寫出現困難</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-07: 東西擺放錯亂且失去回頭尋找的能力</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-08: 判斷力變差或減弱</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-09: 從工作或社交活動中退出</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            <div class="module">
                <h3>M1-10: 情緒和個性的改變</h3>
                <p class="status">✅ 視覺化模組運行中</p>
            </div>
            
            <div id="liff-demo" class="flex-demo">
                <h2>📱 LIFF 應用界面預覽</h2>
                <div style="border: 1px solid #ccc; padding: 20px; border-radius: 8px; background: white;">
                    <h3>📊 詳細分析報告</h3>
                    <p><strong>使用者：</strong> 家庭照顧者</p>
                    <p><strong>分析時間：</strong> 2025-07-29</p>
                    <p><strong>主要關注：</strong> M1-01 記憶力減退</p>
                    
                    <h4>📈 建議追蹤項目：</h4>
                    <ul>
                        <li>記錄重複問題的頻率</li>
                        <li>觀察日常生活功能變化</li>
                        <li>安排專業醫師評估</li>
                    </ul>
                    
                    <a href="/test-flex" class="button">📋 查看完整 JSON</a>
                    <a href="/health" class="button">🔍 系統狀態</a>
                </div>
            </div>
            
            <h2>📱 使用流程</h2>
            <ol>
                <li><strong>加入 LINE Bot：</strong> 掃描 QR Code 加為好友</li>
                <li><strong>發送描述：</strong> 「媽媽最近常重複問同樣的問題」</li>
                <li><strong>接收分析：</strong> 系統回傳 Flex Message 分析結果</li>
                <li><strong>深入了解：</strong> 點擊按鈕開啟 LIFF 詳細資訊</li>
                <li><strong>持續追蹤：</strong> 記錄長期變化趨勢</li>
            </ol>
        </body>
    </html>
    """)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "visualization_modules": 10,
        "active_services": ["M1 Flex API", "LINE Bot Webhook", "LIFF App"],
        "flex_message": "enabled",
        "liff_integration": "active"
    }

@app.get("/test-flex")
async def test_flex():
    return {
        "type": "flex",
        "altText": "失智症警訊分析結果",
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 失智症警訊分析",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "lg"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔸 使用者描述",
                        "weight": "bold",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "媽媽最近常重複問同樣的問題",
                        "wrap": True,
                        "color": "#666666"
                    },
                    {
                        "type": "separator",
                        "margin": "xxl"
                    },
                    {
                        "type": "text",
                        "text": "✅ 正常老化現象",
                        "weight": "bold",
                        "color": "#00B900",
                        "margin": "xxl"
                    },
                    {
                        "type": "text",
                        "text": "偶爾忘記約會或朋友名字，但能夠自己想起來",
                        "wrap": True,
                        "color": "#666666"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ 警訊分析: M1-01",
                        "weight": "bold",
                        "color": "#FF5551",
                        "margin": "xxl"
                    },
                    {
                        "type": "text",
                        "text": "重複詢問可能顯示短期記憶問題，建議諮詢專業醫師進行評估",
                        "wrap": True,
                        "color": "#666666"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                            "type": "uri",
                            "label": "📱 詳細資訊 (LIFF)",
                            "uri": "https://liff.line.me/your-liff-id"
                        }
                    }
                ]
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
