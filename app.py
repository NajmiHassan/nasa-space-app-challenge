# app.py
import streamlit as st
from nasa_api import fetch_nasa_data
from summarizer import summarize_text_hf

st.set_page_config(page_title="NASA Space Bio Explorer", layout="wide")

st.title("🚀 NASA Space Biology Knowledge Explorer")
st.write("Explore NASA's bioscience data and generate AI-powered summaries.")

# Fetch NASA data
if st.button("Fetch NASA Data"):
    data = fetch_nasa_data()
    if "error" not in data:
        st.subheader(data.get("title", "NASA Data"))
        st.image(data.get("url"))
        st.write(data.get("explanation", "No description available."))

        # Summarize the text
        summary = summarize_text_hf(data.get("explanation", ""))
        st.markdown("### 🔍 AI Summary")
        st.write(summary)
    else:
        st.error(data["error"])
