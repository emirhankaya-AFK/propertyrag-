from pydantic import BaseModel
from typing import Dict, Any, Optional

class PropertyDocument(BaseModel):
    id: str
    property_id: str
    doc_type: str  # deed, inspection, appraisal, floor_plan
    file_path: str
    raw_text: str
    parsed_metadata: Optional[Dict[str, Any]] = None
