from pydantic import BaseModel
from typing import List

class ComparableProperty(BaseModel):
    address: str
    sale_price: float
    distance_miles: float
    bedrooms: int
    bathrooms: float
    sqft: int
    price_per_sqft: float
    sale_date: str

class MarketAnalysis(BaseModel):
    property_id: str
    price_per_sqft: float
    median_comp_price: float
    comp_price_variance_pct: float
    comparables: List[ComparableProperty]
    neighborhood_trend: str # up, flat, down
