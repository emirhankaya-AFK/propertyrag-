import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/api"

st.set_page_config(
    page_title="PropertyRAG - Real Estate Investment Advisor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Real Estate Theme styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #111827 100%);
        color: #f3f4f6;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    h1 {
        background: linear-gradient(to right, #fbbf24, #f59e0b, #d97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .prop-card {
        background: rgba(31, 41, 55, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(251, 191, 36, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .prop-card:hover {
        transform: translateY(-2px);
        border-color: rgba(251, 191, 36, 0.5);
    }
    
    .price-tag {
        color: #fbbf24;
        font-weight: 800;
        font-size: 18px;
    }
    
    .badge-buy {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 PropertyRAG")
st.subheader("Autonomous Real Estate Document Analysis & Investment Modeling")

st.markdown("""
Welcome to **PropertyRAG**! This professional advisor matches property legal deeds, inspections, and appraisals, evaluates returns, lists structural/title risks, runs sensitivity projections, and delivers structured Buy/Pass reports.

### Features Available:
1. **Upload Property Docs**: Input purchase parameters and upload inspection reports or deeds.
2. **Property Summary**: View key features (sqft, bedrooms, roof structure, age, layout).
3. **Risk Assessment**: Color-coded risk logs scoring structural, title, zoning, and age hazards.
4. **Investment Analysis**: Interactive cash flow sheet with dynamic loan rate adjustments.
5. **Market Comps**: View comps pricing tables showing deviations from average sales.
6. **Investment Report**: Complete summary dashboard showing final BUY / PASS recommendation.
""")

try:
    res = requests.get(f"{API_URL}/properties/")
    if res.status_code == 200:
        properties = res.json()
        st.markdown(f"### 📂 Active Portfolio ({len(properties)} Properties)")
        if not properties:
            st.info("No properties analyzed yet. Go to **Upload Property** to register your first asset.")
        else:
            cols = st.columns(3)
            for idx, p in enumerate(properties):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="prop-card">
                        <h4 style="margin: 0 0 8px 0; color: #fff;">{p['address']}</h4>
                        <p style="margin: 0 0 12px 0;"><span class="price-tag">${p['purchase_price']:,}</span></p>
                        <div style="font-size: 12px; color: #9ca3af; margin-bottom: 12px;">
                            <strong>Specs:</strong> {p.get('bedrooms')} Bed | {p.get('bathrooms')} Bath | {p.get('building_sqft')} Sqft
                        </div>
                        <span class="badge-buy">Year Built: {p.get('year_built')}</span>
                    </div>
                    """, unsafe_allow_html=True)
except Exception as e:
    st.warning("Could not connect to PropertyRAG backend. Make sure the FastAPI server is running on port 8002.")
