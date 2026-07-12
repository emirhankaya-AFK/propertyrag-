import pytest
from backend.services.investment_calc import InvestmentCalculatorService

def test_mortgage_calculation():
    # Test $240k loan at 6.0% for 30 years
    m = InvestmentCalculatorService.calculate_mortgage(240000, 6.0, 30)
    # Expected is approx $1,438.92
    assert abs(m - 1438.92) < 1.00

def test_irr_calculation():
    # Test cash flows: -100, 20, 20, 20, 120
    # True IRR is 20%
    flows = [-100, 20, 20, 20, 120]
    irr = InvestmentCalculatorService.calculate_irr(flows)
    assert abs(irr - 20.0) < 0.01

def test_investment_projections():
    res = InvestmentCalculatorService.run_projections(
        price=300000,
        down_payment=60000,
        interest_rate=6.0,
        holding_years=10,
        monthly_rent=2100.0
    )
    
    assert res["purchase_price"] == 300000
    assert res["cap_rate"] > 0
    assert res["monthly_cash_flow"] is not None
    assert "rate_6.0" in res["sensitivity_analysis"]
