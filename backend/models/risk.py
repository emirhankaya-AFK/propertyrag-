from pydantic import BaseModel
from typing import List

class RiskItem(BaseModel):
    category: str
    risk: str
    severity: str # high, medium, low
    details: str

class RiskAssessment(BaseModel):
    property_id: str
    overall_risk_score: int # 0-100
    risks: List[RiskItem]
