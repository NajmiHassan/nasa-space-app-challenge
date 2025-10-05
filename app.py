import os
import re
import json
import time
import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components

from paper_reader import PaperReader
from gemini_api import GeminiClient

# ---------- Setup ----------
st.set_page_config(page_title="NASA Space Biology Knowledge Engine", layout="wide")
st.title("🧬 NASA Space Biology Knowledge Engine — Local Papers")
st.markdown("Search, skim abstracts, summarize with Gemini, generate insights, and visualize topics 🔍")

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

@st.cache_data
def extract_keywords_from_query(query: str):
    return gemini.extract_keywords(query)


# ---------- Sidebar ----------
st.sidebar.header("🔍 Search Options")
query = st.sidebar.text_input(
    "Enter your question or search phrase",
    placeholder="e.g., Find papers related to plant growth in microgravity"
)
st.sidebar.info("You can enter keywords or full sentences (e.g., 'Find studies on plant growth in space').")
st.sidebar.markdown("---")


generate_cloud = st.sidebar.button("🌐 Generate Keyword Cloud for Filtered Papers")
generate_graph = st.sidebar.button("🧩 Generate AI Topic Graph")

# ---------- Main logic ----------
if query:
    st.subheader(f"Results for **'{query}'**")
    matches = []
    with st.spinner("🔍 Interpreting your query..."):
        search_keywords = extract_keywords_from_query(query)

    st.write(f"🔍 Interpreted keywords: {', '.join(search_keywords)}")


    for fname in paper_reader.list_papers():
        text = read_pdf_cached(fname)
        if any(k in text[:5000].lower() or k in fname.lower() for k in search_keywords):
            matches.append((fname, text))


    if not matches:
        st.warning("No matching papers found.")
    else:
        st.success(f"Found {len(matches)} related papers.")
        all_categories = []

        # ---------- Show each paper ----------
        for fname, text in matches:
            cats = categorize_paper(text)
            all_categories.extend(cats)
            with st.expander(f"📄 {fname} — *{', '.join(cats)}*"):
                st.markdown(f"**📑 Abstract Snippet:**\n\n{text[:500].replace('\n',' ')}...")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("🧠 Gemini Summary", key=f"sum_{fname}"):
                        with st.spinner("Generating Gemini summary..."):
                            summary = gen_summary_cached(text[:8000], fname)
                            st.markdown("### ✨ Gemini Summary")
                            st.markdown(summary)

                with col2:
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

        # ---------- Generate Combined Keyword Cloud ----------
        if generate_cloud:
            st.markdown("---")
            st.header(f"🌐 Keyword Cloud — Filtered Papers for '{query}'")
            all_text = " ".join([t for _, t in matches])
            top_keywords = extract_top_keywords(all_text, n=50)
            wordcloud = WordCloud(width=900, height=450, background_color="white").generate_from_frequencies(dict(top_keywords))
            fig, ax = plt.subplots(figsize=(10,5))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        # ---------- AI Topic Graph ----------
        if generate_graph:
            st.markdown("---")
            st.header(f"🧩 AI Topic Graph — Filtered Papers for '{query}'")
            paper_topics = {}
            for fname, text in matches:
                abstract = text[:2000]
                topics = gemini.summarize_study(
                    f"Identify up to 3 main research topics for this paper abstract. Return as JSON list.\n\n{abstract}"
                )
                try:
                    topics_list = json.loads(topics)
                except:
                    topics_list = [t.strip() for t in re.split(r"[,\n]", topics) if t.strip()]
                paper_topics[fname] = topics_list

            G = nx.Graph()
            for paper, topics in paper_topics.items():
                G.add_node(paper, color='lightblue', title=paper)
                for topic in topics:
                    G.add_node(topic, color='lightgreen', title=topic)
                    G.add_edge(paper, topic)

            net = Network(height="600px", width="100%", notebook=False)
            net.from_nx(G)
            net.show_buttons(filter_=['physics'])
            graph_path = "topic_graph.html"
            net.save_graph(graph_path)
            components.html(open(graph_path, 'r', encoding='utf-8').read(), height=650)

else:
    st.info("Type a keyword in the sidebar to begin searching local papers.")
