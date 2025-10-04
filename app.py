# app.py
import streamlit as st
from dotenv import load_dotenv
from gemini_api import GeminiClient
from osdr_api import OSDRClient

# Load environment variables
load_dotenv()

# Initialize clients
gemini_client = GeminiClient()
osdr_client = OSDRClient()

# Streamlit page setup
st.set_page_config(
    page_title="NASA Space Biology Knowledge Engine",
    page_icon="🧬",
    layout="wide",
)

# Sidebar
st.sidebar.title("🛰️ Navigation")
st.sidebar.info("Explore NASA bioscience datasets and summaries with Gemini AI.")
st.sidebar.markdown("---")

# Title
st.title("🧬 NASA Space Biology Knowledge Engine")
st.markdown(
    "Interactively explore NASA's **bioscience research** using data from the "
    "[Open Science Data Repository (OSDR)](https://osdr.nasa.gov/osdr/)."
)

# Search input
query = st.text_input("🔍 Search NASA OSDR studies:", placeholder="e.g., spaceflight, RNA, plants")

# Cached functions for metadata and files
@st.cache_data
def fetch_metadata(osd_id):
    return osdr_client.get_study_metadata(osd_id)

@st.cache_data
def fetch_files(osd_id):
    return osdr_client.get_study_files(osd_id)

if query:
    with st.spinner("Fetching data from NASA OSDR..."):
        results = osdr_client.search_studies_local(query)

    if results:
        st.success(f"Found {len(results)} studies for **{query}**.")
        for i, study in enumerate(results, 1):
            with st.expander(f"🧪 {i}. {study['title']}"):
                st.markdown(f"**Study ID:** `{study['osd_id']}`")
                st.write(study['description'])

                col1, col2, col3 = st.columns(3)
                osd_id = study["osd_id"]

                # Metadata button
                with col1:
                    if st.button("📘 View Metadata", key=f"meta_{i}"):
                        metadata = fetch_metadata(osd_id)
                        if metadata:
                            st.json(metadata)
                        else:
                            st.error("Metadata unavailable.")

                # Files button
                with col2:
                    if st.button("📂 View Files", key=f"files_{i}"):
                        files = fetch_files(osd_id)
                        if files:
                            for k, v in files.get("studies", {}).items():
                                for f in v.get("study_files", []):
                                    st.markdown(f"- **{f['file_name']}** ({f['category']})")
                                    st.caption(f"[🔗 Download](https://osdr.nasa.gov{f['remote_url']})")
                        else:
                            st.warning("No files found.")

                # Gemini summary button
                with col3:
                    if st.button("✨ Gemini Summary", key=f"sum_{i}"):
                        metadata = fetch_metadata(osd_id)
                        if metadata:
                            with st.spinner("Generating AI summary..."):
                                summary = gemini_client.summarize_study(metadata)
                                st.markdown(f"**🧠 Gemini Summary:**\n\n{summary}")
                        else:
                            st.warning("No metadata found for this study.")
    else:
        st.warning("No studies found. Try another keyword.")
else:
    st.info("Type a keyword above to search NASA bioscience datasets.")
