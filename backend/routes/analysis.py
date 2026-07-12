from fastapi import APIRouter, HTTPException
from ..db import get_property, get_risk_assessment

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/{prop_id}/risk")
async def get_property_risk(prop_id: str):
    assess = get_risk_assessment(prop_id)
    if not assess:
        raise HTTPException(status_code=404, detail="Risk assessment not ready or property has no uploaded reports.")
    return assess

@router.get("/{prop_id}/details")
async def get_property_details(prop_id: str):
    prop = get_property(prop_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found.")
    return {
        "address": prop["address"],
        "building_sqft": prop["building_sqft"],
        "lot_size_sqft": prop["lot_size_sqft"],
        "bedrooms": prop["bedrooms"],
        "bathrooms": prop["bathrooms"],
        "year_built": prop["year_built"]
    }
