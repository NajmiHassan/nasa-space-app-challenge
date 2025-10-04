import os
import re
import json
import time
import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from paper_reader import PaperReader
from gemini_api import GeminiClient

# ---------- Setup ----------
st.set_page_config(page_title="NASA Space Biology Knowledge Engine", layout="wide")
st.title("🧬 NASA Space Biology Knowledge Engine — Local Papers")
st.markdown("Search, skim abstracts, summarize with Gemini, and explore insights 🔍")

# Initialize
paper_reader = PaperReader("papers/first_50")
gemini = GeminiClient()

# ---------- Cached helpers ----------
@st.cache_data
def read_pdf_cached(file_name):
    return paper_reader.read_pdf(file_name)

@st.cache_data
def gen_summary_cached(text, title):
    return gemini.summarize_study(text, paper_title=title)

@st.cache_data
def gen_metadata_cached(text):
    return gemini.extract_metadata(text)

@st.cache_data
def extract_top_keywords(text, n=30):
    words = re.findall(r"[A-Za-z]{4,}", text.lower())
    stopwords = {
        "this","that","with","from","which","about","were","have","been","also",
        "these","they","such","their","when","where","into","will","there","study",
        "data","results","space","microgravity","experiment","using","found"
    }
    filtered = [w for w in words if w not in stopwords]
    counter = Counter(filtered)
    return counter.most_common(n)

def categorize_paper(text):
    """Rough classification based on simple keyword rules."""
    categories = {
        "Bone/Muscle Loss": ["bone", "muscle", "atrophy"],
        "Microgravity Effects": ["gravity", "microgravity", "weightlessness"],
        "Plant Biology in Space": ["plant", "photosynthesis", "seed", "root"],
        "Microbiome/ISS Environment": ["bacteria", "microbiome", "biofilm"],
        "Radiation Effects": ["radiation", "cosmic", "ionizing"],
        "Immune System": ["immune", "inflammation", "cytokine"],
        "Genomics/Omics Studies": ["rna", "genome", "proteomics", "transcriptome"],
    }
    matches = []
    for cat, kw in categories.items():
        if any(k in text.lower() for k in kw):
            matches.append(cat)
    return matches or ["Other"]

def plot_category_distribution(cat_list):
    df = pd.DataFrame(cat_list, columns=["Category"])
    counts = df["Category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts["Category"], counts["Count"])
    ax.set_xlabel("Category")
    ax.set_ylabel("Paper Count")
    ax.set_title("Distribution of Research Topics")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

def save_row_csv(row: dict, csv_path="summaries.csv"):
    df_row = pd.DataFrame([row])
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        if 'File' in df_existing.columns and row.get('File') in df_existing['File'].astype(str).tolist():
            return False
        df_row.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        df_row.to_csv(csv_path, index=False)
    return True

# ---------- Sidebar ----------
st.sidebar.header("🔍 Search Options")
query = st.sidebar.text_input("Enter keyword (e.g., plant, gravity, RNA)")
st.sidebar.info("Use keywords related to biology or space environment.")
st.sidebar.markdown("---")

# ---------- Main logic ----------
if query:
    st.subheader(f"Results for **'{query}'**")
    matches = []
    for fname in paper_reader.list_papers():
        text = read_pdf_cached(fname)
        if query.lower() in fname.lower() or query.lower() in text[:5000].lower():
            matches.append((fname, text))

    if not matches:
        st.warning("No matching papers found.")
    else:
        st.success(f"Found {len(matches)} related papers.")

        all_categories = []

        for fname, text in matches:
            snippet = text[:400].replace("\n", " ")
            cats = categorize_paper(text)
            all_categories.extend(cats)

            with st.expander(f"📄 {fname} — *{', '.join(cats)}*"):
                st.markdown(f"**📑 Abstract Snippet:**\n\n{text[:3000][:500]}...")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🧠 Gemini Summary", key=f"sum_{fname}"):
                        with st.spinner("Generating Gemini summary..."):
                            summary = gen_summary_cached(text[:8000], fname)
                            st.markdown("### ✨ Gemini Summary")
                            st.markdown(summary)

                with col2:
                    if st.button("📊 Generate Paper Keyword Cloud", key=f"cloud_{fname}"):
                        top_keywords = extract_top_keywords(text)
                        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(dict(top_keywords))
                        fig, ax = plt.subplots()
                        ax.imshow(wordcloud, interpolation="bilinear")
                        ax.axis("off")
                        st.pyplot(fig)

                with col3:
                    if st.button("💾 Save Summary + Metadata", key=f"save_{fname}"):
                        meta = gen_metadata_cached(text)
                        summary = gen_summary_cached(text[:8000], fname)
                        row = {
                            "File": fname,
                            "Title": meta.get("Title") if isinstance(meta, dict) else None,
                            "Summary": summary,
                            "Categories": json.dumps(cats),
                            "SavedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                        ok = save_row_csv(row)
                        st.success("Saved!" if ok else "Already saved previously.")

        # ---------- Insights Dashboard ----------
        st.markdown("---")
        st.header("📊 Insights Dashboard — Topic Distribution")
        plot_category_distribution(all_categories)

        combined_text = " ".join([text[:2000] for _, text in matches])
        with st.spinner("Analyzing overall insights..."):
            insights = gemini.summarize_study(
                f"Here are multiple study abstracts: {combined_text[:10000]}. "
                "Summarize key discoveries, common patterns, and research trends."
            )
        st.markdown("### 🧩 Gemini Insights Summary")
        st.markdown(insights)
else:
    st.info("Type a keyword in the sidebar to begin searching local papers.")
