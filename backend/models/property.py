from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Property(BaseModel):
    id: str
    address: str
    building_sqft: int
    lot_size_sqft: int
    bedrooms: int
    bathrooms: float
    year_built: int
    purchase_price: float
    annual_tax: float
    monthly_rent_estimate: float
    file_path: Optional[str] = None
    created_at: datetime = datetime.now()

class PropertyCreate(BaseModel):
    address: str
    purchase_price: float
    down_payment: float
    interest_rate: float
    holding_period_years: int
