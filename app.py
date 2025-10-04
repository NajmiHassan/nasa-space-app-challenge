# app.py
import streamlit as st
from gemini_api import GeminiClient
from paper_reader import PaperReader

# Initialize clients
paper_reader = PaperReader("papers/first_50")
gemini_client = GeminiClient()

# Streamlit setup
st.set_page_config(
    page_title="NASA Space Biology Knowledge Engine (Local Papers)",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 NASA Space Biology Knowledge Engine (Local Papers)")
st.markdown(
    "Explore NASA bioscience research locally — search, read, and summarize studies "
    "with **Gemini AI** to reveal biological insights for space exploration."
)

query = st.text_input("🔍 Search papers by keyword:", placeholder="e.g., microgravity, plants, RNA")

if query:
    matching_papers = [p for p in paper_reader.list_papers() if query.lower() in p.lower()]

    if matching_papers:
        st.success(f"Found {len(matching_papers)} papers for '{query}'.")
        for file_name in matching_papers:
            with st.expander(f"📄 {file_name}"):
                col1, col2 = st.columns([1, 2])

                with col1:
                    if st.button("📘 View Extracted Sections", key=f"sections_{file_name}"):
                        text = paper_reader.read_pdf(file_name)
                        sections = paper_reader.extract_sections(text)
                        if not sections:
                            st.warning("No recognizable sections found.")
                        else:
                            for sec, content in sections.items():
                                st.markdown(f"### {sec}")
                                st.text(content[:600] + "...")

                with col2:
                    if st.button("✨ Generate Gemini Summary", key=f"summary_{file_name}"):
                        with st.spinner("Analyzing and summarizing paper..."):
                            text = paper_reader.read_pdf(file_name)
                            summary = gemini_client.summarize_study(text, paper_title=file_name)
                            st.markdown("### 🧠 Gemini AI Summary")
                            st.markdown(summary)
    else:
        st.warning("No papers found matching that keyword.")
else:
    st.info("Type a keyword to search your local NASA bioscience papers.")
