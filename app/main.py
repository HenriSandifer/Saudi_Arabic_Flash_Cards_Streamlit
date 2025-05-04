import streamlit as st
import pandas as pd
import random
import os

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_csv("data/vocab.csv")
    df = df.dropna(subset=["arabic_word", "english", "audio_path"])
    return df

df = load_data()

# === Session state ===
if "revealed" not in st.session_state:
    st.session_state.revealed = False
if "index" not in st.session_state:
    st.session_state.index = random.randint(0, len(df) - 1)

def pick_new_card():
    st.session_state.index = random.randint(0, len(df) - 1)
    st.session_state.revealed = False

# === Card Data ===
row = df.iloc[st.session_state.index]

# === Layout ===
st.title("Arabic Flashcards")

# === Flashcard ===
if not st.session_state.revealed:
    st.markdown(
        f"<div style='text-align: center; padding: 20px; "
        f"font-size: 40px; border: 2px solid #4CAF50; border-radius: 12px; "
        f"box-shadow: 2px 2px 10px rgba(0,0,0,0.2); cursor: pointer;'>"
        f"{row['english']}</div>",
        unsafe_allow_html=True
    )
    if st.button("Reveal", use_container_width=True):
        st.session_state.revealed = True
else:
    st.markdown(
        f"<div style='text-align: center; padding: 20px; "
        f"font-size: 40px; border: 2px solid #2196F3; border-radius: 12px; "
        f"box-shadow: 2px 2px 10px rgba(0,0,0,0.2); cursor: pointer;'>"
        f"{row['arabic_word']}</div>",
        unsafe_allow_html=True
    )
    if st.button("Play Audio", use_container_width=True):
        st.audio(row['audio_path'], format="audio/mp3")

    # Show other info
    st.markdown("### Details:")
    st.markdown(f"**English**: {row['english']}")
    st.markdown(f"**Transliteration**: {row['transliteration']}")
    st.markdown(f"**Category**: {row.get('category', '')}")
    st.markdown(f"**Type**: {row.get('type', '')}")
    st.markdown(f"**Dialect**: {row.get('dialect', '')}")
    st.markdown(f"**Root**: {row.get('arabic_full', '')}")

    st.button("Next", on_click=pick_new_card, use_container_width=True)
