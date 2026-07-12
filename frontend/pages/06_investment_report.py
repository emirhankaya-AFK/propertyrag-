import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/api"

st.title("📋 Executive Investment Report")

try:
    prop_res = requests.get(f"{API_URL}/properties/")
    properties = prop_res.json() if prop_res.status_code == 200 else []
except Exception:
    properties = []

if not properties:
    st.info("No properties registered yet.")
else:
    prop_options = {p["address"]: p["id"] for p in properties}
    selected_address = st.selectbox("Select Property for Report", list(prop_options.keys()))
    selected_id = prop_options[selected_address]
    
    col1, col2 = st.columns([5, 5])
    
    with col1:
        with st.spinner("Compiling investment decision..."):
            try:
                res = requests.get(f"{API_URL}/reports/{selected_id}/investment-decision")
                if res.status_code == 200:
                    data = res.json()
                    decision = data["decision"]
                    justification = data["justification"]
                    
                    dec_bg = "rgba(16, 185, 129, 0.15)" if "BUY" in decision else "rgba(239, 68, 68, 0.15)"
                    dec_fg = "#34d399" if "BUY" in decision else "#f87171"
                    dec_border = "1px solid #10b981" if "BUY" in decision else "1px solid #ef4444"
                    
                    st.markdown(f"""
                    <div style="background: {dec_bg}; border: {dec_border}; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
                        <span style="font-size: 14px; color: #cbd5e1; text-transform: uppercase; font-weight: 600;">System Recommendation</span>
                        <h2 style="color: {dec_fg}; margin: 8px 0; font-size: 32px; font-weight: 800;">{decision}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🤖 Advisor Justification")
                    st.info(justification)
                else:
                    st.warning("Investment report not available yet.")
            except Exception as e:
                st.error(f"Failed connection: {e}")
                
    with col2:
        st.markdown("### 💬 Document Q&A Explorer")
        st.write("Query the parsed deed, appraisal, or inspection report:")
        
        q = st.text_input("Ask about the property:", placeholder="e.g. Is the roof in good condition? What foundation issues exist?")
        if st.button("Query Documents") and q:
            with st.spinner("Searching RAG index..."):
                try:
                    qa_res = requests.post(f"{API_URL}/qa/{selected_id}/ask", json={"question": q})
                    if qa_res.status_code == 200:
                        qa_data = qa_res.json()
                        
                        st.markdown("**Answer:**")
                        st.markdown(f'<div style="background: rgba(31, 41, 55, 0.35); padding: 16px; border-left: 4px solid #fbbf24; border-radius: 8px; font-size: 14px;">{qa_data["answer"]}</div>', unsafe_allow_html=True)
                        
                        st.write("")
                        st.markdown("**Retrieved Contexts:**")
                        for idx, s in enumerate(qa_data.get("sources", [])):
                            st.markdown(f"""
                            <div style="font-size: 12px; color: #9ca3af; margin-bottom: 6px;">
                                <strong>Context #{idx+1} (Doc: {s['doc_type'].upper()} | Score: {s['score']:.2f})</strong><br>
                                <em>"{s['snippet']}"</em>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("Error query.")
                except Exception as e:
                    st.error(f"QA query failed: {e}")
