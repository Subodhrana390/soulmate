from flask import Flask, request, jsonify, render_template
import notepad
import affirmations
import health
import song_suggester
import meditation
import google.generativeai as genai

app = Flask(__name__)

# ✅ Configure Gemini Flash
genai.configure(api_key="AIzaSyAFKVgyAQ9exdf2nPzZNjAqOZ5piZvnt5o")
model = genai.GenerativeModel("gemini-1.5-flash")

# ================================
# 🌐 ROUTES
# ================================

# 🏠 Home route → loads frontend (index.html)
@app.route("/")
def home():
    return render_template("index.html")   # Looks inside /templates folder

# 💬 AI Chatbot (Gemini Flash)
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = f"⚠️ Sorry, AI is unavailable. Error: {e}"

    return jsonify({"reply": reply})

# ✨ Affirmations
@app.route("/affirmations", methods=["GET"])
def get_affirmations():
    try:
        return jsonify({"affirmations": affirmations.get_affirmations()})
    except Exception:
        return jsonify({"affirmations": ["Stay positive!", "You are capable."]})

# 🩺 Health Tips
@app.route("/health", methods=["GET"])
def get_health_tips():
    try:
        return jsonify({"tips": health.get_tips()})
    except Exception:
        return jsonify({"tips": ["Drink water regularly.", "Take short breaks."]})

# 🎵 Song Suggestions
@app.route("/songs", methods=["POST"])
def suggest_song():
    mood = request.json.get("mood", "")
    try:
        return jsonify({"songs": song_suggester.suggest(mood)})
    except Exception:
        return jsonify({"songs": ["No songs available."]})

# 🧘 Meditation Steps
@app.route("/meditation", methods=["GET"])
def get_meditation():
    try:
        return jsonify({"steps": meditation.get_steps()})
    except Exception:
        return jsonify({"steps": ["Close your eyes.", "Take deep breaths."]})

# ================================
# 🚀 Run server
# ================================
if __name__ == "__main__":
    app.run(debug=True)
