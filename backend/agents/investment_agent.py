from typing import Dict, Any
from ..services.investment_calc import InvestmentCalculatorService
from ..models.investment import InvestmentAnalysis

class InvestmentAgent:
    @staticmethod
    def analyze_investment(
        property_id: str,
        price: float,
        down_payment: float,
        interest_rate: float,
        holding_years: int = 10,
        monthly_rent: float = 2000.0
    ) -> InvestmentAnalysis:
        """
        Runs financial projections and compiles them into InvestmentAnalysis model.
        """
        proj = InvestmentCalculatorService.run_projections(
            price=price,
            down_payment=down_payment,
            interest_rate=interest_rate,
            holding_years=holding_years,
            monthly_rent=monthly_rent
        )
        
        return InvestmentAnalysis(
            property_id=property_id,
            purchase_price=price,
            cap_rate=proj["cap_rate"],
            cash_on_cash_return=proj["cash_on_cash_return"],
            npv_10_years=proj["npv_10_years"],
            irr_10_years=proj["irr_10_years"],
            monthly_mortgage=proj["monthly_mortgage"],
            monthly_expenses=proj["monthly_expenses"],
            monthly_cash_flow=proj["monthly_cash_flow"],
            sensitivity_analysis=proj["sensitivity_analysis"]
        )
