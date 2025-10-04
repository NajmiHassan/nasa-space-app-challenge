# gemini_api.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    """Wrapper class for Google Gemini API integration."""

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = "gemini-2.0-flash-lite"
        self.model = None
        self._configure()

    def _configure(self):
        """Configure Gemini model if key exists."""
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY not found in .env file.")
            return
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            print(f"Error initializing Gemini model: {e}")
            self.model = None

    def summarize_study(self, metadata: dict) -> str:
        """Generate a summary for NASA OSDR study metadata."""
        if not self.model:
            return "Gemini model not configured properly."

        prompt = (
            "Summarize this NASA space biology study for a general audience. "
            "Focus on the experiment goal, biological context, and results.\n\n"
            f"{metadata}"
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating summary: {e}"
