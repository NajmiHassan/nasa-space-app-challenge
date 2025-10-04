import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiClient:
    """Simple wrapper for Google Gemini (generative AI) calls."""

    def __init__(self, model_name="gemini-2.0-flash-lite"):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
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
        if not self.model:
            return "Gemini model not configured."
        truncated = paper_text[:7000]
        prompt = (
            f"You are an expert science communicator. Read the following text and produce a concise summary for a general audience.\n"
            f"Title: {paper_title}\n\n"
            f"Produce FIVE short bullet points:\n"
            f"1) Study goal\n2) Experiment setup\n3) Key results\n4) Biological implications\n5) Relevance for space exploration or open questions.\n\n"
            f"Text:\n{truncated}"
        )
        try:
            response = self.model.generate_content(prompt)
            return getattr(response, "text", str(response)).strip()
        except Exception as e:
            return f"Error generating summary: {e}"

    def extract_metadata(self, paper_text: str) -> dict:
        if not self.model:
            return {"error": "Gemini model not configured."}
        truncated = paper_text[:9000]
        prompt = (
            "Extract the following metadata from the research text and output a JSON object ONLY.\n"
            "Keys: Title, Year, Authors (list), Keywords (list), Organisms (list), Methods (list), "
            "MainTopic (short), KeyFindings (list), Conclusions (list)\n\n"
            f"Text:\n{truncated}\n\n"
            "Output example:\n"
            '{"Title": "...", "Year": "YYYY", "Authors": ["A B","C D"], "Keywords": ["x","y"], '
            '"Organisms": ["mouse"], "Methods": ["RNA-seq"], "MainTopic": "plant growth", '
            '"KeyFindings": ["..."], "Conclusions": ["..."]}'
        )
        try:
            response = self.model.generate_content(prompt)
            text = getattr(response, "text", str(response)).strip()
            try:
                parsed = json.loads(text)
                return parsed
            except Exception:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end != -1 and end > start:
                    try:
                        parsed = json.loads(text[start:end])
                        return parsed
                    except Exception:
                        return {"raw": text}
                return {"raw": text}
        except Exception as e:
            return {"error": str(e)}
