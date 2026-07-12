import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

class PriceTrendChartComponent:
    @staticmethod
    def render_comp_chart(subject_price: float, comps: List[Dict[str, Any]]):
        """
        Renders a bar chart comparing the subject property price with comparable sales in the neighborhood.
        """
        addresses = [c["address"] for c in comps]
        prices = [c["sale_price"] for c in comps]
        
        # Add subject property
        addresses.insert(0, "SUBJECT PROPERTY")
        prices.insert(0, subject_price)
        
        colors = ["#fbbf24"] + ["#3b82f6"] * len(comps)
        
        fig = go.Figure(
            data=[go.Bar(x=addresses, y=prices, marker_color=colors)],
            layout=go.Layout(
                title="Comparable Sales Pricing Comparison",
                yaxis_title="Sale Price ($)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f3f4f6"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_sensitivity_chart(sensitivity: Dict[str, Dict[str, float]]):
        """
        Renders a line chart showing how cash flow varies based on loan rates.
        """
        rates = []
        cash_flows = []
        
        # Parse rates from keys
        for key, val in sensitivity.items():
            rate_val = float(key.split("_")[1])
            rates.append(rate_val)
            cash_flows.append(val["monthly_cash_flow"])
            
        fig = go.Figure(
            data=[go.Scatter(x=rates, y=cash_flows, mode="lines+markers", line=dict(color="#f59e0b", width=3))],
            layout=go.Layout(
                title="Monthly Cash Flow Sensitivity to Loan Interest Rate",
                xaxis_title="Interest Rate (%)",
                yaxis_title="Monthly Cash Flow ($)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f3f4f6"
            )
        )
        st.plotly_chart(fig, use_container_width=True)
