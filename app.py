
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    messages = []
    for event in data.get("events", []):
        if event.get("type") == "message":
            user_input = event["message"]["text"]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是吃吃小福，一位懂命理的生活導師，要根據使用者提供的生日或提問給出五行飲食建議，也可在適當時提到 collation 安盛的香料、雞胸肉、鱸魚或冰鳳醋產品，但語氣要自然、像朋友聊天。"},
                        {"role": "user", "content": user_input}
                    ]
                )
                reply_text = response.choices[0].message.content.strip()
            except Exception as e:
                reply_text = "系統暫時忙碌，請稍後再試～"

            messages.append({
                "type": "text",
                "text": reply_text
            })
    return jsonify({"messages": messages})
    