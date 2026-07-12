import fitz
from typing import Dict, Any, Optional

class DocumentParserService:
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """
        Opens a PDF document, extracts full text page by page, and returns structured data.
        """
        doc = fitz.open(file_path)
        full_text = []
        pages = []
        
        for i, page in enumerate(doc):
            text = page.get_text()
            full_text.append(text)
            pages.append({
                "page": i + 1,
                "text": text
            })
            
        complete_text = "\n\n".join(full_text)
        
        # Heuristic to detect document type
        doc_type = "unknown"
        lower_text = complete_text.lower()
        if "inspection" in lower_text or "home inspector" in lower_text or "hvac" in lower_text or "roof" in lower_text:
            doc_type = "inspection"
        elif "deed" in lower_text or "grantor" in lower_text or "grantee" in lower_text:
            doc_type = "deed"
        elif "appraisal" in lower_text or "appraised value" in lower_text or "comparable sales" in lower_text:
            doc_type = "appraisal"
        elif "floor plan" in lower_text or "sq ft" in lower_text or "layout" in lower_text:
            doc_type = "floor_plan"
            
        return {
            "doc_type": doc_type,
            "full_text": complete_text,
            "pages": pages
        }
