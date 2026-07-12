import streamlit as st
import requests
from components.property_card import PropertyCardComponent
from components.document_viewer import DocumentViewerComponent

API_URL = "http://127.0.0.1:8002/api"

st.title("📋 Property Features Card")

try:
    prop_res = requests.get(f"{API_URL}/properties/")
    properties = prop_res.json() if prop_res.status_code == 200 else []
except Exception:
    properties = []

if not properties:
    st.info("Please register a property and upload inspection documents first.")
else:
    prop_options = {p["address"]: p["id"] for p in properties}
    selected_address = st.selectbox("Select Property", list(prop_options.keys()))
    selected_id = prop_options[selected_address]
    
    col1, col2 = st.columns([5, 5])
    
    with col1:
        with st.spinner("Loading parsed details..."):
            try:
                res = requests.get(f"{API_URL}/analysis/{selected_id}/details")
                if res.status_code == 200:
                    PropertyCardComponent.render_card(res.json())
                else:
                    st.warning("Property details not loaded yet.")
            except Exception as e:
                st.error(f"Error: {e}")
                
    with col2:
        st.markdown("### 📄 Document Viewer")
        selected_prop = next(p for p in properties if p["id"] == selected_id)
        file_path = selected_prop.get("file_path")
        if file_path:
            DocumentViewerComponent.render_document(file_path)
        else:
            st.info("No document PDF attached to this property. Please upload one in the sidebar.")
