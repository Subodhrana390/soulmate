import streamlit as st

def show_notepad():
    st.header("📝 Write Your Thoughts")

    notes = st.text_area("How are you feeling today?")
    
    if st.button("Save My Thoughts"):
        if notes.strip():
            st.success("✅ Your thoughts are saved safely!")
        else:
            st.warning("⚠ Please write something before saving.")
