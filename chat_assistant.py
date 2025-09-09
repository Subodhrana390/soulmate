import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import google.generativeai as genai

# ✅ Configure Gemini Flash
genai.configure(api_key="AIzaSyAFKVgyAQ9exdf2nPzZNjAqOZ5piZvnt5o")
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎤 Function: Voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... please speak")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your voice."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        except Exception as e:
            return f"Error: {e}"

# 🤖 Setup persistent chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 🤖 Function: Chat with Gemini Flash
def chatbot_response(user_input):
    chat = st.session_state.chat_session
    response = chat.send_message(user_input)
    return response.text

# 🔊 Function: Speak AI response
def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        tts.save(temp_path)
        st.audio(temp_path, format="audio/mp3")

# 🌸 Main Chat UI
def show_chat():
    st.header("💬 Casual AI Chat (Gemini Flash + Voice)")

    if "history" not in st.session_state:
        st.session_state.history = []

    # User text input
    user_input = st.text_input("Type your message 👇")

    # Voice input
    if st.button("🎤 Speak"):
        user_input = get_voice_input()

    # Handle input
    if user_input:
        bot_reply = chatbot_response(user_input)

        # Save history
        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("bot", bot_reply))

        # AI speaks
        speak_text(bot_reply)

    # Display chat
    for sender, message in st.session_state.history:
        if sender == "user":
            st.markdown(f"🧑 **You:** {message}")
        else:
            st.markdown(f"🤖 **Bot:** {message}")
