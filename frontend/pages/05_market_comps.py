import streamlit as st
import requests
import pandas as pd
from components.price_trend_chart import PriceTrendChartComponent

API_URL = "http://127.0.0.1:8002/api"

st.title("📊 Comparable Market Comps")

try:
    prop_res = requests.get(f"{API_URL}/properties/")
    properties = prop_res.json() if prop_res.status_code == 200 else []
except Exception:
    properties = []

if not properties:
    st.info("No properties registered yet.")
else:
    prop_options = {p["address"]: p["id"] for p in properties}
    selected_address = st.selectbox("Select Core Property", list(prop_options.keys()))
    selected_id = prop_options[selected_address]
    
    with st.spinner("Retrieving local sales database..."):
        try:
            res = requests.get(f"{API_URL}/comparable/{selected_id}")
            if res.status_code == 200:
                data = res.json()
                
                # Comp metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Subject Price/Sqft", f"${data['price_per_sqft']:.2f}")
                with col2:
                    st.metric("Comps Median Price", f"${data['median_comp_price']:,.2f}")
                with col3:
                    variance = data['comp_price_variance_pct']
                    st.metric("Variance vs comps", f"{variance:.1f}%", delta=f"{variance:.1f}%", delta_color="inverse")
                    
                # Chart
                st.write("")
                selected_prop = next(p for p in properties if p["id"] == selected_id)
                PriceTrendChartComponent.render_comp_chart(selected_prop["purchase_price"], data["comparables"])
                
                # Table
                st.write("")
                st.markdown("### 📋 Comparable Properties Database")
                
                df_data = []
                for idx, c in enumerate(data["comparables"]):
                    df_data.append({
                        "Comparable Address": c["address"],
                        "Sale Price ($)": f"${c['sale_price']:,}",
                        "Distance (Miles)": f"{c['distance_miles']} mi",
                        "Beds/Baths": f"{c['bedrooms']}B / {c['bathrooms']}Ba",
                        "Size (Sqft)": f"{c['sqft']} sqft",
                        "Price/Sqft": f"${c['price_per_sqft']:.2f}",
                        "Sale Date": c["sale_date"]
                    })
                    
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.error("Error retrieving comparables.")
        except Exception as e:
            st.error(f"Failed to fetch market data: {e}")
