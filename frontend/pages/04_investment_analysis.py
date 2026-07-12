import streamlit as st
import requests
from components.roi_calculator import ROICalculatorComponent
from components.price_trend_chart import PriceTrendChartComponent

API_URL = "http://127.0.0.1:8002/api"

st.title("💰 Investment & Cash Flow Projections")

try:
    prop_res = requests.get(f"{API_URL}/properties/")
    properties = prop_res.json() if prop_res.status_code == 200 else []
except Exception:
    properties = []

if not properties:
    st.info("No properties registered yet.")
else:
    prop_options = {p["address"]: p["id"] for p in properties}
    selected_address = st.selectbox("Select Property for Financial Run", list(prop_options.keys()))
    selected_id = prop_options[selected_address]
    
    selected_prop = next(p for p in properties if p["id"] == selected_id)
    
    # Render recalculator parameters side-by-side
    st.sidebar.markdown("### ⚙️ Adjust Parameters")
    dp = st.sidebar.number_input("Down Payment ($)", min_value=0, value=int(selected_prop.get("down_payment") or 60000), step=5000)
    rate = st.sidebar.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, value=float(selected_prop.get("interest_rate") or 6.5), step=0.1)
    rent = st.sidebar.number_input("Monthly Rent Estimate ($)", min_value=100, value=int(selected_prop.get("monthly_rent_estimate") or 2100), step=100)
    holding = st.sidebar.number_input("Holding Period (Years)", min_value=1, max_value=30, value=int(selected_prop.get("holding_period_years") or 10))
    
    recalc_btn = st.sidebar.button("Recalculate Projections")
    
    if recalc_btn:
        with st.spinner("Re-calculating NPV, Cash-flows and IRR..."):
            try:
                res = requests.post(f"{API_URL}/investment/{selected_id}/recalculate", json={
                    "down_payment": dp,
                    "interest_rate": rate,
                    "monthly_rent": rent,
                    "holding_years": holding
                })
                if res.status_code == 200:
                    st.success("Calculations updated!")
            except Exception as e:
                st.error(f"Error recalculating: {e}")
                
    # Load and render results
    with st.spinner("Loading financial data..."):
        try:
            proj_res = requests.get(f"{API_URL}/investment/{selected_id}/projections")
            if proj_res.status_code == 200:
                proj_data = proj_res.json()
                
                # Render Grid
                ROICalculatorComponent.render_projections(proj_data)
                
                # Render Sensitivity Chart
                st.write("---")
                if "sensitivity_analysis" in proj_data:
                    PriceTrendChartComponent.render_sensitivity_chart(proj_data["sensitivity_analysis"])
            else:
                st.warning("Investment projections not available.")
        except Exception as e:
            st.error(f"Failed to fetch projections: {e}")
