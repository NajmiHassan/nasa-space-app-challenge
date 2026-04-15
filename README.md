# NASA Space Biology Knowledge Engine

- **Streamlit application:** [https://nasa-space-app-challenge-xd3zh8qdvvpz6wgcfguehy.streamlit.app/]
- **Presentation:** [https://docs.google.com/presentation/d/1qGccb_PpgbKTmouMRoO1dBJj-nKjcKldq4nCHH1IHLg/edit?usp=sharing]
- **Video explanation:** [https://youtu.be/29cE5yI8RcI]

A local AI-powered Streamlit web application for exploring and analyzing NASA space biology research papers. The app processes 48 PDF documents containing scientific studies on biological effects of spaceflight, microgravity, and related topics.

## 🚀 How It Works

The application uses Google Gemini AI to intelligently process natural language queries and extract relevant scientific keywords. It then searches through the local collection of NASA space biology papers to find matches, generates AI-powered summaries, and creates interactive visualizations of research topics.

### Core Functionality

1. **Intelligent Search**: Enter natural language questions or keywords about space biology topics
2. **AI Keyword Extraction**: Gemini AI automatically identifies 3-6 relevant search terms from your query
3. **Local PDF Processing**: Searches through 48 NASA research papers stored locally
4. **Automatic Categorization**: Papers are classified into research categories (Bone/Muscle Loss, Microgravity Effects, Plant Biology, etc.)
5. **AI Summarization**: Generate concise summaries using Google Gemini (requires API key)
6. **Interactive Visualizations**:
   - Keyword clouds showing term frequency
   - Network graphs of research topics
   - Category distribution charts
7. **Data Export**: Save paper summaries and metadata to CSV files

## 📊 Features

- **Natural Language Search**: Ask questions like "Find papers about plant growth in microgravity"
- **Paper Exploration**: View abstract snippets and generate AI summaries
- **Topic Analysis**: Automatic categorization and visualization of research themes
- **Local Data Storage**: All 48 papers are processed locally (no internet required for search)
- **AI-Powered Insights**: Gemini integration for intelligent query processing and summarization
- **Interactive Dashboard**: Streamlit-based web interface with expandable paper views

## 🛠️ Technical Stack

- **Frontend**: Streamlit (Python web framework)
- **AI**: Google Gemini 2.0 Flash Lite API
- **PDF Processing**: PyPDF2 for text extraction
- **Data Analysis**: pandas for data manipulation
- **Visualization**:
  - matplotlib for charts
  - wordcloud for keyword visualization
  - networkx + pyvis for interactive graphs
- **Environment**: python-dotenv for API key management

## 📋 Requirements

- Python 3.9+
- 48 NASA space biology PDF papers (included in `papers/first_50/`)
- Google Gemini API key (optional, for AI features)

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nasa-space-app-challenge
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Gemini API** (Optional but recommended):
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**:
   Open your browser to the URL shown in the terminal (typically http://localhost:8501)

## 🔍 Usage Guide

### Search Queries
The search accepts natural language questions or keyword phrases:

**Examples:**
- "Find papers about plant growth in microgravity"
- "Studies on bone loss in space"
- "Research about radiation effects on astronauts"
- "Microbiome changes in space environment"
- "plant photosynthesis space"
- "muscle atrophy microgravity"

### App Features

1. **Search Sidebar**:
   - Enter your query in the text input
   - Click buttons to generate keyword clouds or topic graphs

2. **Results Display**:
   - Expandable paper cards showing abstracts
   - AI summary generation (requires Gemini API key)
   - Save functionality for summaries and metadata

3. **Visualizations**:
   - Topic distribution bar chart
   - Interactive keyword cloud
   - Network graph of research topics

### Data Files

- **Papers**: Located in `papers/first_50/` (48 PDF files)
- **Saved Summaries**: Automatically saved to `summaries.csv`
- **Topic Graph**: Generated as `topic_graph.html`

## 📁 Project Structure

```
nasa-space-app-challenge/
├── app.py                 # Main Streamlit application
├── gemini_api.py          # Google Gemini AI integration
├── paper_reader.py        # PDF text extraction utilities
├── osdr_api.py           # NASA OSDR API client (unused in current version)
├── requirements.txt       # Python dependencies
├── papers/
│   └── first_50/         # 48 NASA space biology PDF papers
├── README.md             # This file
└── .env                  # API keys (create this file)
```

## 🤖 AI Features

When Gemini API key is provided:
- **Query Processing**: Converts natural language to scientific keywords
- **Summarization**: Generates 5-point structured summaries of papers
- **Metadata Extraction**: Pulls title, authors, keywords, methods, etc.
- **Topic Analysis**: Identifies main research topics for network visualization

Without API key:
- Basic keyword search still works
- AI features are disabled with graceful fallbacks

## 🎯 Research Categories

Papers are automatically categorized into:
- Bone/Muscle Loss
- Microgravity Effects
- Plant Biology in Space
- Microbiome/ISS Environment
- Radiation Effects
- Immune System
- Genomics/Omics Studies
- Other

## 🔗 Links

- **Live Demo**: [Streamlit Cloud App](https://spacebioapp-kc72ri5ahc95xefjh9ydwf.streamlit.app/)
- **Presentation**: [Google Slides](https://docs.google.com/presentation/d/1qGccb_PpgbKTmouMRoO1dBJj-nKjcKldq4nCHH1IHLg/edit?slide=id.p9#slide=id.p9)

## 📝 Notes

- All PDF processing happens locally - no papers are uploaded to external services
- The app works with the provided 48 papers; adding more PDFs requires placing them in `papers/first_50/`
- Gemini API calls require internet connection and valid API key
- Generated visualizations and summaries are cached for performance
