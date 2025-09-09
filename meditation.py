import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from googletrans import Translator
import os
import tempfile

def show_meditation():
    st.header("🧘 Mood-based Meditation Generator")

    # Mood options
    mood = st.selectbox("How are you feeling right now?", 
                        ["Stressed", "Anxious", "Sad", "Angry", "Tired", "Happy", "Neutral"])

    # Language choice
    language = st.radio("Select Meditation Language:", ["English", "Hindi"])

    # New Feature: Cross-translation mode
    cross_mode = st.checkbox("🔄 Translate opposite (Speak Hindi → Get English, Speak English → Get Hindi)")

    if st.button("Generate Meditation"):
        with st.spinner("Creating your meditation..."):
            translator = Translator()

            # Step 1: Always generate meditation in English first
            prompt = f"Create a short 2-minute guided meditation script for someone feeling {mood}. " \
                     f"Use simple, calming, and supportive language."

            model = genai.GenerativeModel("gemini-2.5-flash")   # ✅ Use flash model
            response = model.generate_content(prompt)
            meditation_text = response.text

            # Step 2: Handle normal or cross translation
            if cross_mode:
                if language == "English":
                    # User chose English, but deliver in Hindi
                    meditation_text = translator.translate(meditation_text, src="en", dest="hi").text
                    lang_code = "hi"
                else:
                    # User chose Hindi, but deliver in English
                    meditation_text = translator.translate(meditation_text, src="en", dest="en").text
                    lang_code = "en"
            else:
                # Normal mode (direct in selected language)
                if language == "Hindi":
                    meditation_text = translator.translate(meditation_text, src="en", dest="hi").text
                    lang_code = "hi"
                else:
                    lang_code = "en"

            # Step 3: Show text
            st.subheader("✨ Your Meditation Script")
            st.write(meditation_text)

            # Step 4: Convert to speech
            tts = gTTS(meditation_text, lang=lang_code)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                temp_filename = tmp.name

            tts.save(temp_filename)

            with open(temp_filename, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")

            os.remove(temp_filename)
