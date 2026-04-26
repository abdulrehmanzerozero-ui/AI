from flask import Flask, request, jsonify
from groq import Groq
from tavily import TavilyClient

app = Flask(__name__)

# 🔑 API KEYS (put yours here)
GROQ_API_KEY = "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"
TAVILY_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# 🧠 SEARCH TOOL
def search(query):
    try:
        res = tavily.search(query=query)
        return res["results"][0]["content"]
    except:
        return "No results found"

# 🤖 AI BRAIN
def brain(message):
    msg = message.lower()

    # tool routing
    if "search" in msg or "who is" in msg or "latest" in msg:
        return search(message)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a smart AI assistant made by ProBots."},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content

# 🌐 API ENDPOINT
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]

    return jsonify({
        "reply": brain(user_message)
    })

# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)