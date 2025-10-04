# osdr_api.py
import requests
from typing import List, Dict

BASE_URL = "https://osdr.nasa.gov/osdr/data/osd"

class OSDRClient:
    """NASA Open Science Data Repository API Client"""

    def __init__(self):
        pass

    # Local study index to avoid 404 on search
    STUDIES_INDEX = [
        {"osd_id": "86", "title": "Plant Growth in Space", "description": "Effects of microgravity on plants"},
        {"osd_id": "87", "title": "Mouse RNA-seq Analysis", "description": "Gene expression profiling in mice"},
        {"osd_id": "137", "title": "Epigenomics Study", "description": "DNA methylation changes in microgravity"},
    ]

    def search_studies_local(self, keyword: str, index=None) -> List[Dict]:
        """Filter local index for studies containing the keyword."""
        if index is None:
            index = self.STUDIES_INDEX
        keyword_lower = keyword.lower()
        results = [s for s in index if keyword_lower in s['title'].lower() or keyword_lower in s['description'].lower()]
        return results

    def get_study_metadata(self, study_id: str) -> Dict:
        """Fetch metadata for a given OSDR study ID."""
        url = f"{BASE_URL}/meta/{study_id}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Error fetching metadata for {study_id}: {e}")
            return None

    def get_study_files(self, study_id: str) -> Dict:
        """Fetch associated files for a study."""
        url = f"{BASE_URL}/files/{study_id}"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Error fetching files for {study_id}: {e}")
            return None
