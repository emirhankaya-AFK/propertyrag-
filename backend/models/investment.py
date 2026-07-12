from pydantic import BaseModel
from typing import List, Dict

class InvestmentAnalysis(BaseModel):
    property_id: str
    purchase_price: float
    cap_rate: float
    cash_on_cash_return: float
    npv_10_years: float
    irr_10_years: float
    monthly_mortgage: float
    monthly_expenses: float
    monthly_cash_flow: float
    sensitivity_analysis: Dict[str, Dict[str, float]] # e.g. {"interest_rate_plus_1": {"monthly_cash_flow": ...}}
