from typing import Dict, Any
from ..services.llm_service import LLMService
from ..services.market_data import MarketDataService
from ..models.market_comp import MarketAnalysis

class MarketAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def analyze_market(self, property_id: str, address: str, price: float) -> MarketAnalysis:
        """
        Fetches comps, calculates market variances, and adds LLM narrative insights.
        """
        analysis = MarketDataService.get_comparable_sales(address, price)
        analysis.property_id = property_id
        
        variables = {
            "price": price,
            "count": len(analysis.comparables)
        }
        
        # Add LLM descriptive narrative (we can store this in a custom field or print it)
        narrative = self.llm.generate_text("market", variables)
        print(f"Market Insight Narrative: {narrative}")
        
        return analysis
