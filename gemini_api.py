# gemini_api.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    """Wrapper for Google Gemini API."""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-2.0-flash-lite"
        self.model = None
        self._configure()

    def _configure(self):
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY not found in .env file.")
            return
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            self.model = None

    def summarize_study(self, paper_text: str, paper_title: str = "") -> str:
        """Generate a layperson-friendly summary of a research paper."""
        if not self.model:
            return "Gemini model not configured properly."

        prompt = (
            f"You are an expert space biologist summarizing NASA bioscience research.\n"
            f"Title: {paper_title}\n\n"
            f"Summarize this paper in 5 bullet points:\n"
            f"1. Study goal\n2. Experiment setup\n3. Key results\n"
            f"4. Biological implications\n5. Relevance for space exploration.\n\n"
            f"Paper text:\n{paper_text[:8000]}"
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating summary: {e}"
