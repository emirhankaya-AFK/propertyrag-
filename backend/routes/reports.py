from fastapi import APIRouter, HTTPException
from ..db import get_property, get_risk_assessment, get_investment_analysis
from ..services.llm_service import LLMService
from ..agents.recommendation_agent import RecommendationAgent

router = APIRouter(prefix="/reports", tags=["reports"])

llm_service = LLMService()
rec_agent = RecommendationAgent(llm_service)

@router.get("/{prop_id}/investment-decision")
async def get_investment_decision(prop_id: str):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
        
    # Get risk score
    assess = get_risk_assessment(prop_id)
    risk_score = assess["overall_risk_score"] if assess else 30
    
    # Get cap rate
    inv = get_investment_analysis(prop_id)
    cap_rate = inv["cap_rate"] if inv else 5.0
    
    rec = rec_agent.generate_recommendation(prop["purchase_price"], cap_rate, risk_score)
    return {
        "property_address": prop["address"],
        "purchase_price": prop["purchase_price"],
        "risk_score": risk_score,
        "cap_rate": cap_rate,
        "decision": rec["decision"],
        "justification": rec["justification"]
    }
