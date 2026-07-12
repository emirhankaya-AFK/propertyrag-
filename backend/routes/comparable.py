from fastapi import APIRouter, HTTPException
from ..db import get_property
from ..services.llm_service import LLMService
from ..agents.market_agent import MarketAgent

router = APIRouter(prefix="/comparable", tags=["comparable"])

llm_service = LLMService()
market_agent = MarketAgent(llm_service)

@router.get("/{prop_id}")
async def get_comparables(prop_id: str):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
        
    analysis = market_agent.analyze_market(prop_id, prop["address"], prop["purchase_price"])
    return analysis.model_dump()
