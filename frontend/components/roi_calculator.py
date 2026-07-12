import streamlit as st
from typing import Dict, Any

class ROICalculatorComponent:
    @staticmethod
    def render_projections(proj: Dict[str, Any]):
        """
        Renders the ROI analysis summary and projections.
        """
        st.markdown("### 📊 Financial Projections Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(31, 41, 55, 0.3); border-radius: 8px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
                <span style="font-size: 12px; color: #9ca3af; display: block; text-transform: uppercase;">Cap Rate</span>
                <strong style="font-size: 24px; color: #10b981;">{proj.get('cap_rate', 0.0):.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="background: rgba(31, 41, 55, 0.3); border-radius: 8px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
                <span style="font-size: 12px; color: #9ca3af; display: block; text-transform: uppercase;">Cash on Cash</span>
                <strong style="font-size: 24px; color: #10b981;">{proj.get('cash_on_cash_return', 0.0):.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div style="background: rgba(31, 41, 55, 0.3); border-radius: 8px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
                <span style="font-size: 12px; color: #9ca3af; display: block; text-transform: uppercase;">10-Year NPV</span>
                <strong style="font-size: 24px; color: #fbbf24;">${proj.get('npv_10_years', 0.0):,.0f}</strong>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div style="background: rgba(31, 41, 55, 0.3); border-radius: 8px; padding: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
                <span style="font-size: 12px; color: #9ca3af; display: block; text-transform: uppercase;">10-Year IRR</span>
                <strong style="font-size: 24px; color: #fbbf24;">{proj.get('irr_10_years', 0.0):.2f}%</strong>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("")
        st.markdown("### 💸 Monthly Cash Flow Breakdown")
        
        m_expenses = proj.get("monthly_expenses", 0.0)
        m_mortgage = proj.get("monthly_mortgage", 0.0)
        m_flow = proj.get("monthly_cash_flow", 0.0)
        rent_est = m_expenses + m_mortgage + m_flow
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"- **Estimated Monthly Rent**: `${rent_est:,.2f}`")
            st.markdown(f"- **Operating Expenses**: `${m_expenses:,.2f}`")
        with col_b:
            st.markdown(f"- **Mortgage Payment (P&I)**: `${m_mortgage:,.2f}`")
            st.markdown(f"- **Monthly Net Cash Flow**: `${m_flow:,.2f}`")
