app.py
from flask import Flask, request, jsonify
import anthropic
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "CandleIQ is Live! 🚀"

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json
    stock = data.get('stock', 'Unknown')
    candles = data.get('candles', 'No data')
    claude = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_KEY"))
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""You are CandleIQ, expert Indian stock analyzer.
Stock: {stock}
Candle Data: {candles}
Give me:
1. Pattern detected
2. Trend: Bullish / Bearish / Sideways
3. Signal: Strong / Moderate / Weak
4. Verdict: INVEST ✅ / SKIP ❌ / WATCH 👀
5. One line reason
User manages their own financial risk."""
        }]
    )
    return jsonify({"result": message.content[0].text})

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    data = request.json
    image_base64 = data.get('image')
    claude = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_KEY"))
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_base64
                    }
                },
                {
                    "type": "text",
                    "text": """You are CandleIQ. Analyze this Indian stock chart.
1. Pattern detected
2. Trend: Bullish / Bearish / Sideways
3. Signal: Strong / Moderate / Weak
4. Verdict: INVEST ✅ / SKIP ❌ / WATCH 👀
5. One line reason
User manages their own financial risk."""
                }
            ]
        }]
    )
    return jsonify({"result": message.content[0].text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
