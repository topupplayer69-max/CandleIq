from flask import Flask, request, jsonify
from groq import Groq
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return "CandleIQ is Live! 🚀"

@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    data = request.json
    stock = data.get('stock', 'Unknown')
    candles = data.get('candles', 'No data')
    
    client = Groq(api_key=os.environ.get("GROQ_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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
        }],
        max_tokens=500
    )
    return jsonify({"result": response.choices[0].message.content})

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    data = request.json
    image_base64 = data.get('image')
    
    client = Groq(api_key=os.environ.get("GROQ_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
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
        }],
        max_tokens=500
    )
    return jsonify({"result": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
