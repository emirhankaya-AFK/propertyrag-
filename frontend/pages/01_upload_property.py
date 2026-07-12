import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/api"

st.title("📂 Register Property & Upload Documents")

col1, col2 = st.columns([5, 5])

with col1:
    st.markdown("### 📝 Register New Property")
    with st.form("create_form", clear_on_submit=True):
        address = st.text_input("Property Address:", placeholder="e.g., 742 Evergreen Terrace, Springfield")
        price = st.number_input("Purchase Price ($):", min_value=10000, value=300000, step=10000)
        down_payment = st.number_input("Down Payment ($):", min_value=0, value=60000, step=5000)
        rate = st.number_input("Interest Rate (%):", min_value=0.0, value=6.5, step=0.1)
        holding = st.number_input("Holding Period (Years):", min_value=1, max_value=30, value=10)
        
        submit_btn = st.form_submit_button("Register Property")
        
        if submit_btn and address:
            with st.spinner("Saving property parameters..."):
                try:
                    payload = {
                        "address": address,
                        "purchase_price": price,
                        "down_payment": down_payment,
                        "interest_rate": rate,
                        "holding_period_years": holding
                    }
                    res = requests.post(f"{API_URL}/properties/", json=payload)
                    if res.status_code == 200:
                        st.success("Property registered successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to register property.")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

with col2:
    st.markdown("### 📄 Attach Documents (Deeds, Inspections)")
    try:
        prop_res = requests.get(f"{API_URL}/properties/")
        properties = prop_res.json() if prop_res.status_code == 200 else []
    except Exception:
        properties = []
        
    if not properties:
        st.info("Register a property first to enable document upload.")
    else:
        prop_options = {p["address"]: p["id"] for p in properties}
        selected_address = st.selectbox("Select Target Property", list(prop_options.keys()))
        selected_id = prop_options[selected_address]
        
        with st.form("upload_doc_form", clear_on_submit=True):
            uploaded_file = st.file_uploader("Select PDF Document", type=["pdf"])
            upload_btn = st.form_submit_button("Upload and Process Document")
            
            if upload_btn and uploaded_file:
                with st.spinner("Processing document text in the background..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        res = requests.post(f"{API_URL}/properties/{selected_id}/upload-doc", files=files)
                        if res.status_code == 200:
                            st.success("Document attached! Background parsing, risk analysis, and cash flow projections triggered.")
                        else:
                            st.error("Failed to process document.")
                    except Exception as e:
                        st.error(f"Upload connection failed: {e}")

# List and delete
st.write("---")
st.markdown("### 📋 Property Registry")
if properties:
    for p in properties:
        c1, c2, c3 = st.columns([6, 2, 2])
        with c1:
            st.markdown(f"**{p['address']}**")
            st.caption(f"Price: ${p['purchase_price']:,} | Down Payment: ${p.get('down_payment', 0):,} ({p.get('interest_rate') or 0}%)")
        with c2:
            st.caption(f"Registered: {p['created_at'][:10]}")
        with c3:
            if st.button("Delete 🗑️", key=p["id"]):
                with st.spinner("Deleting..."):
                    try:
                        del_res = requests.delete(f"{API_URL}/properties/{p['id']}")
                        if del_res.status_code == 200:
                            st.success("Deleted!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Delete failed: {e}")
