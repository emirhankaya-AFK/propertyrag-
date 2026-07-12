from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import get_property, get_investment_analysis, save_investment_analysis
from ..agents.investment_agent import InvestmentAgent

router = APIRouter(prefix="/investment", tags=["investment"])

class RecalculateRequest(BaseModel):
    down_payment: float
    interest_rate: float
    monthly_rent: float
    holding_years: int = 10

@router.get("/{prop_id}/projections")
async def get_projections(prop_id: str):
    inv = get_investment_analysis(prop_id)
    if not inv:
        # Generate on the fly with defaults
        prop = get_property(prop_id)
        if not prop:
            raise HTTPException(status_code=404, detail="Property not found.")
            
        inv_result = InvestmentAgent.analyze_investment(
            property_id=prop_id,
            price=prop["purchase_price"],
            down_payment=prop["down_payment"] or prop["purchase_price"] * 0.2,
            interest_rate=prop["interest_rate"] or 6.5,
            holding_years=prop["holding_period_years"] or 10,
            monthly_rent=prop["monthly_rent_estimate"] or prop["purchase_price"] * 0.007
        )
        # Save
        save_investment_analysis(
            prop_id,
            inv_result.cap_rate,
            inv_result.cash_on_cash_return,
            inv_result.npv_10_years,
            inv_result.irr_10_years,
            inv_result.model_dump()
        )
        return inv_result.model_dump()
        
    return inv["data"]

@router.post("/{prop_id}/recalculate")
async def recalculate_projections(prop_id: str, req: RecalculateRequest):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
        
    inv_result = InvestmentAgent.analyze_investment(
        property_id=prop_id,
        price=prop["purchase_price"],
        down_payment=req.down_payment,
        interest_rate=req.interest_rate,
        holding_years=req.holding_years,
        monthly_rent=req.monthly_rent
    )
    
    # Save back
    save_investment_analysis(
        prop_id,
        inv_result.cap_rate,
        inv_result.cash_on_cash_return,
        inv_result.npv_10_years,
        inv_result.irr_10_years,
        inv_result.model_dump()
    )
    
    return inv_result.model_dump()
