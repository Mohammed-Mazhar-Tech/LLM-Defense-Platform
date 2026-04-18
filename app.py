from flask import Flask, render_template, request, jsonify, session
from defense_pipeline import DefensePlatform
import ollama

app = Flask(__name__)

app.secret_key = "llm-defense-secret"

# 🔹 Warm up LLM when server starts
print("Loading LLM model...")

ollama.chat(
    model="llama3:8b-instruct-q4_0",
    messages=[{"role":"user","content":"hello"}]
)

print("LLM model ready")

platform = DefensePlatform()


@app.route("/")
def home():

    if "history" not in session:
        session["history"] = []

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"status":"ERROR"})

    history = session.get("history", [])
    history.append({"role":"user","text":prompt})

    result = platform.process(prompt)

    if result["status"] == "SAFE":
        history.append({
            "role":"assistant",
            "text":result["response"]
        })
    else:
        history.append({
            "role":"assistant",
            "text":"⚠️ " + result["reason"]
        })

    session["history"] = history

    return jsonify({
        "result": result,
        "history": history
    })


if __name__ == "__main__":
    app.run(debug=True)