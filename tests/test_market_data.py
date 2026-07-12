import pytest
from backend.services.market_data import MarketDataService

def test_market_comparables():
    subject_price = 350000.0
    res = MarketDataService.get_comparable_sales("742 Evergreen Terrace", subject_price)
    
    assert len(res.comparables) == 3
    assert res.median_comp_price > 0
    assert res.comp_price_variance_pct is not None
    assert res.neighborhood_trend == "up"
    
    for c in res.comparables:
        assert c.sale_price > 0
        assert c.sqft > 0
        assert c.price_per_sqft == c.sale_price / c.sqft
