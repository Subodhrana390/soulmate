import streamlit as st
import random

def show_affirmations():
    st.header("🌈 Positive Affirmations")

    affirmations = [
        "You are stronger than you think.",
        "Every day is a fresh start.",
        "Believe in yourself, you are enough.",
        "Your feelings are valid.",
        "Good things are coming your way."
    ]

    if st.button("Show Affirmation"):
        st.success(random.choice(affirmations))
