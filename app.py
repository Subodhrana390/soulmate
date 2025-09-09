import streamlit as st
import notepad
import chat_assistant
import affirmations
import health
import song_suggester  # ✅ keep this, remove music_mood import
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyAFKVgyAQ9exdf2nPzZNjAqOZ5piZvnt5o")

st.set_page_config(page_title="SoulTalk AI", page_icon="🌸")
st.title("🌸 SoulTalk AI")

st.sidebar.title("Menu")
choice = st.sidebar.radio(
    "Choose an option:",
   ["Notepad", "Chat Assistant", "Affirmations", "Health", "Music Mood", "Meditation"]

)

# Handle menu options
if choice == "Notepad":
    notepad.show_notepad()
elif choice == "Chat Assistant":
    chat_assistant.show_chat()
elif choice == "Affirmations":
    affirmations.show_affirmations()
elif choice == "Health":
    health.show_health_tips()
elif choice == "Music Mood":       # ✅ now correct
    song_suggester.show_song_suggester()
elif choice == "Meditation":
    import meditation
    meditation.show_meditation()

