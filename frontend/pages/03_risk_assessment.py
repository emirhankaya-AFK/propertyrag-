import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/api"

st.title("⚠️ Risk Assessment Report")

try:
    prop_res = requests.get(f"{API_URL}/properties/")
    properties = prop_res.json() if prop_res.status_code == 200 else []
except Exception:
    properties = []

if not properties:
    st.info("No properties registered yet.")
else:
    prop_options = {p["address"]: p["id"] for p in properties}
    selected_address = st.selectbox("Select Property for Risk Audit", list(prop_options.keys()))
    selected_id = prop_options[selected_address]
    
    with st.spinner("Compiling risk records..."):
        try:
            res = requests.get(f"{API_URL}/analysis/{selected_id}/risk")
            if res.status_code == 200:
                data = res.json()
                score = data["overall_risk_score"]
                
                # Render big gauge / header
                score_color = "#10b981" if score < 40 else "#f59e0b" if score <= 60 else "#ef4444"
                
                st.markdown(f"""
                <div style="background: rgba(31, 41, 55, 0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 24px; text-align: center; margin-bottom: 24px;">
                    <span style="font-size: 14px; color: #9ca3af; text-transform: uppercase;">Overall Risk Score</span>
                    <h1 style="-webkit-text-fill-color: {score_color}; font-size: 64px; margin: 10px 0;">{score} / 100</h1>
                    <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 0;">Risk level: <strong>{"LOW" if score < 40 else "MEDIUM" if score <= 60 else "HIGH"}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # List risks
                st.markdown("### 📋 Identified Risks & Concerns")
                for r in data["risks"]:
                    badge_bg = "rgba(16, 185, 129, 0.15)" if r["severity"] == "low" else "rgba(245, 158, 11, 0.15)" if r["severity"] == "medium" else "rgba(239, 68, 68, 0.15)"
                    badge_fg = "#34d399" if r["severity"] == "low" else "#fbbf24" if r["severity"] == "medium" else "#f87171"
                    
                    st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.25); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <strong style="color: #fff; font-size: 15px;">{r['risk']}</strong>
                            <span style="background-color: {badge_bg}; color: {badge_fg}; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; text-transform: uppercase;">{r['severity']} Severity</span>
                        </div>
                        <p style="font-size: 13px; color: #cbd5e1; margin: 0 0 6px 0;">{r['details']}</p>
                        <span style="background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 600; text-transform: uppercase;">Category: {r['category']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Risk assessment data not available for this property yet. Make sure document upload succeeded and processed.")
        except Exception as e:
            st.error(f"Error fetching risk assessment: {e}")
