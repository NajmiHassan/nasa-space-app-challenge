Presentation link: https://docs.google.com/presentation/d/1qGccb_PpgbKTmouMRoO1dBJj-nKjcKldq4nCHH1IHLg/edit?slide=id.p9#slide=id.p9

# NASA Space Biology Knowledge Engine

A simple AI-powered web app to explore and summarize NASA space biology papers.

## Features
    - Search papers by keyword or sentence
    - View abstracts and AI-generated summaries
    - Keyword cloud and topic distribution charts
    - AI-based topic graph visualization
    - Save summaries and metadata locally

## Requirements
    - Python 3.9+
    - Streamlit
    - PyPDF2
    - pandas
    - matplotlib
    - wordcloud
    - networkx
    - pyvis
    - dotenv
    - Google Gemini API key (optional, for AI summaries)

## Setup
1. Clone this repository:
    - git clone <repo_url>
    - cd <repo_folder>
    
2. Install dependencies:
    - pip install -r requirements.txt

(Optional) Create a .env file with your Gemini API key:

    - GEMINI_API_KEY=your_key_here

3. Run the App
    - streamlit run app.py
    - Search by keywords or full sentences.
