from typing import Dict, Any
from ..services.llm_service import LLMService

class RecommendationAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def generate_recommendation(self, price: float, cap_rate: float, risk_score: int) -> Dict[str, Any]:
        """
        Determines BUY/PASS decision based on risk and returns, and writes a narrative justification.
        """
        # Logic:
        # Risk score < 40 AND Cap rate > 5% -> "STRONG BUY"
        # Risk score 40-60 AND Cap rate 3-5% -> "BUY (with conditions)"
        # Risk score > 60 OR Cap rate < 3% -> "PASS"
        if risk_score < 40 and cap_rate >= 5.0:
            decision = "STRONG BUY"
        elif (40 <= risk_score <= 60) and (3.0 <= cap_rate < 5.0):
            decision = "BUY (with conditions)"
        else:
            decision = "PASS"
            
        variables = {
            "price": price,
            "cap_rate": cap_rate,
            "risk_score": risk_score
        }
        
        justification = self.llm.generate_text("recommendation", variables)
        
        return {
            "decision": decision,
            "justification": justification
        }
