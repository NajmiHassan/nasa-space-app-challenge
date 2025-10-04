import os
import PyPDF2

class PaperReader:
    """Reads and extracts text sections from local PDF files."""

    def __init__(self, papers_dir="papers/first_50"):
        self.papers_dir = papers_dir

    def list_papers(self):
        """Return all PDF filenames sorted."""
        try:
            files = [f for f in os.listdir(self.papers_dir) if f.lower().endswith(".pdf")]
            files.sort()
            return files
        except FileNotFoundError:
            return []

    def read_pdf(self, file_name):
        """Extracts text from a PDF file and returns plain text."""
        text = ""
        file_path = os.path.join(self.papers_dir, file_name)
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
        return text

    def extract_sections(self, text):
        """
        Roughly split text into sections by searching for common section headers.
        Returns a dict {SectionName: snippet}.
        """
        sections = {}
        lowered = text.lower()
        headings = ["abstract", "introduction", "methods", "materials and methods",
                    "results", "discussion", "conclusion", "conclusions"]
        for h in headings:
            idx = lowered.find(h)
            if idx != -1:
                snippet = text[idx: idx + 2000]
                sections[h.capitalize()] = snippet.strip()
        return sections
