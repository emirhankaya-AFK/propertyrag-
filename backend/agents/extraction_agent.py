from typing import Dict, Any
from ..services.llm_service import LLMService

class ExtractionAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def extract_property_details(self, doc_text: str, filename: str) -> Dict[str, Any]:
        """
        Extracts structural property details from document text.
        """
        # Trim text to prevent token limit issues
        sample_text = doc_text[:12000]
        
        variables = {
            "address": filename.replace(".pdf", "").replace("_", " "),
            "text": sample_text
        }
        
        return self.llm.generate_json("extraction", variables)
