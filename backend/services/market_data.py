from typing import List, Dict, Any
from ..models.market_comp import ComparableProperty, MarketAnalysis

class MarketDataService:
    @staticmethod
    def get_comparable_sales(address: str, purchase_price: float) -> MarketAnalysis:
        """
        Queries Zillow/Redfin mock APIs to fetch comparable properties in the neighborhood.
        """
        # Generate clean comparable properties relative to the purchase price
        base_price = purchase_price if purchase_price > 0 else 350000.0
        
        comps = [
            ComparableProperty(
                address="124 Maple Ave, Local Neighborhood",
                sale_price=base_price * 0.98,
                distance_miles=0.25,
                bedrooms=3,
                bathrooms=2.0,
                sqft=1500,
                price_per_sqft=(base_price * 0.98) / 1500,
                sale_date="2026-04-12"
            ),
            ComparableProperty(
                address="78 Spruce Dr, Local Neighborhood",
                sale_price=base_price * 1.05,
                distance_miles=0.45,
                bedrooms=3,
                bathrooms=2.5,
                sqft=1650,
                price_per_sqft=(base_price * 1.05) / 1650,
                sale_date="2026-05-20"
            ),
            ComparableProperty(
                address="201 Pine Blvd, Local Neighborhood",
                sale_price=base_price * 0.94,
                distance_miles=0.6,
                bedrooms=3,
                bathrooms=2.0,
                sqft=1450,
                price_per_sqft=(base_price * 0.94) / 1450,
                sale_date="2026-02-28"
            )
        ]
        
        # Calculate stats
        prices = [c.sale_price for c in comps]
        median_price = sum(prices) / len(prices)
        
        variance = 0.0
        if median_price > 0:
            variance = ((purchase_price - median_price) / median_price) * 100
            
        subject_sqft = 1500  # Default assumption if not parsed
        subject_price_per_sqft = purchase_price / subject_sqft if purchase_price > 0 else 200.0
        
        return MarketAnalysis(
            property_id="subject_prop_id",
            price_per_sqft=subject_price_per_sqft,
            median_comp_price=median_price,
            comp_price_variance_pct=variance,
            comparables=comps,
            neighborhood_trend="up"  # Upward trending market
        )
