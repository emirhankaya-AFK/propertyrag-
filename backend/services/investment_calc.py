from typing import Dict, Any

class InvestmentCalculatorService:
    @staticmethod
    def calculate_mortgage(loan_amount: float, annual_rate: float, years: int = 30) -> float:
        """
        Calculates monthly mortgage payment (amortization).
        """
        if annual_rate == 0:
            return loan_amount / (years * 12)
        r = (annual_rate / 100) / 12
        n = years * 12
        return loan_amount * (r * (1 + r)**n) / ((1 + r)**n - 1)

    @staticmethod
    def calculate_irr(cash_flows: list, guess: float = 0.1) -> float:
        """
        Calculates Internal Rate of Return (IRR) using Newton-Raphson method.
        """
        max_iters = 1000
        precision = 1e-6
        for i in range(max_iters):
            npv = 0.0
            d_npv = 0.0
            for t, cf in enumerate(cash_flows):
                npv += cf / (1 + guess)**t
                if t > 0:
                    d_npv -= t * cf / (1 + guess)**(t + 1)
            if abs(d_npv) < 1e-12:
                break
            next_guess = guess - npv / d_npv
            if abs(next_guess - guess) < precision:
                return next_guess * 100
            guess = next_guess
        return 0.0  # Fallback

    @staticmethod
    def run_projections(
        price: float,
        down_payment: float,
        interest_rate: float,
        holding_years: int = 10,
        monthly_rent: float = 2000.0,
        annual_tax_rate: float = 0.012,
        annual_appreciation_rate: float = 0.03
    ) -> Dict[str, Any]:
        """
        Generates 10-year real estate cash-flow projections and investment indicators.
        """
        loan_amount = price - down_payment
        monthly_mortgage = InvestmentCalculatorService.calculate_mortgage(loan_amount, interest_rate)
        
        # Monthly Operating Expenses
        monthly_tax = (price * annual_tax_rate) / 12
        monthly_insurance = 100.0
        monthly_maintenance = (price * 0.01) / 12  # 1% rule
        monthly_hoa = 100.0
        monthly_vacancy = monthly_rent * 0.05
        
        total_monthly_expenses = monthly_tax + monthly_insurance + monthly_maintenance + monthly_hoa + monthly_vacancy
        
        monthly_cash_flow = monthly_rent - (total_monthly_expenses + monthly_mortgage)
        annual_cash_flow = monthly_cash_flow * 12
        
        # NOI (excludes mortgage payment)
        noi = (monthly_rent - total_monthly_expenses) * 12
        cap_rate = (noi / price) * 100
        
        cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment > 0 else 0
        
        # Build Cash Flow Array for NPV/IRR
        # Year 0: -Down Payment
        # Years 1-9: Annual Cash Flow
        # Year 10: Annual Cash Flow + Estimated Resale Value (less remaining loan balance)
        resale_value = price * (1 + annual_appreciation_rate)**holding_years
        
        # Approximate remaining principal
        r = (interest_rate / 100) / 12
        n = 30 * 12
        p = holding_years * 12
        if r > 0:
            remaining_loan = loan_amount * (((1 + r)**n - (1 + r)**p) / ((1 + r)**n - 1))
        else:
            remaining_loan = loan_amount * (1 - p/n)
            
        equity_payout = resale_value - remaining_loan
        
        cash_flows = [-down_payment]
        for y in range(1, holding_years):
            # Cash flows grow slightly with rent inflation (e.g. 2% annual)
            cash_flows.append(annual_cash_flow * (1.02)**y)
        # Year 10 payout
        cash_flows.append((annual_cash_flow * (1.02)**holding_years) + equity_payout)
        
        # NPV at 6% discount rate
        discount_rate = 0.06
        npv = sum(cf / (1 + discount_rate)**t for t, cf in enumerate(cash_flows))
        
        # IRR
        irr = InvestmentCalculatorService.calculate_irr(cash_flows)
        
        # Sensitivity Analysis (variations in interest rates)
        sensitivity = {}
        for delta in [-1.0, 0.0, 1.0, 2.0]:
            rate = max(0.0, interest_rate + delta)
            m_mortgage = InvestmentCalculatorService.calculate_mortgage(loan_amount, rate)
            m_flow = monthly_rent - (total_monthly_expenses + m_mortgage)
            sensitivity[f"rate_{rate:.1f}"] = {
                "monthly_mortgage": m_mortgage,
                "monthly_cash_flow": m_flow,
                "cash_on_cash": (m_flow * 12 / down_payment) * 100 if down_payment > 0 else 0
            }
            
        return {
            "purchase_price": price,
            "loan_amount": loan_amount,
            "monthly_mortgage": monthly_mortgage,
            "monthly_expenses": total_monthly_expenses,
            "monthly_cash_flow": monthly_cash_flow,
            "noi": noi,
            "cap_rate": cap_rate,
            "cash_on_cash_return": cash_on_cash,
            "npv_10_years": npv,
            "irr_10_years": irr,
            "sensitivity_analysis": sensitivity
        }
