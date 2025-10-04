# paper_reader.py
import os
import PyPDF2

class PaperReader:
    """Reads and extracts text sections from local PDF files."""

    def __init__(self, papers_dir="papers/first_50"):
        self.papers_dir = papers_dir

    def list_papers(self):
        """Return all PDF filenames."""
        return [f for f in os.listdir(self.papers_dir) if f.endswith(".pdf")]

    def read_pdf(self, file_name):
        """Extracts text from a PDF file."""
        text = ""
        file_path = os.path.join(self.papers_dir, file_name)
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
        return text

    def extract_sections(self, text):
        """
        Roughly split text into sections like Introduction/Results/Conclusion.
        (Simple substring search — enough for NASA challenge prototype)
        """
        sections = {}
        lowered = text.lower()
        for section in ["introduction", "methods", "results", "discussion", "conclusion"]:
            idx = lowered.find(section)
            if idx != -1:
                # extract 2000 chars from each section for preview
                sections[section.capitalize()] = text[idx:idx + 2000]
        return sections
