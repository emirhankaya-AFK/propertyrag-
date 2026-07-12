import streamlit as st
import base64
from pathlib import Path

class DocumentViewerComponent:
    @staticmethod
    def render_document(file_path: str):
        """
        Embeds local PDF files inside Streamlit using base64.
        """
        path = Path(file_path)
        if not path.exists():
            st.error("Document PDF not found.")
            return
            
        try:
            with open(path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf"></iframe>'
            st.markdown(display, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load PDF view: {e}.")
