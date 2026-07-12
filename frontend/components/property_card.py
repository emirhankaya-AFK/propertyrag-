import streamlit as st
from typing import Dict, Any

class PropertyCardComponent:
    @staticmethod
    def render_card(details: Dict[str, Any]):
        """
        Renders a beautiful grid displaying the structural details of the property.
        """
        st.markdown(f"""
        <div style="background: rgba(31, 41, 55, 0.45); border: 1px solid rgba(251, 191, 36, 0.15); border-radius: 12px; padding: 24px; margin-bottom: 24px;">
            <h2 style="color: #fff; margin-top: 0; margin-bottom: 4px;">{details.get('address')}</h2>
            <p style="color: #9ca3af; font-size: 14px; margin-top: 0;">Physical specs parsed from property inspection reports:</p>
            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 16px 0;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Building Size</span>
                    <strong style="color: #fbbf24; font-size: 20px;">{details.get('building_sqft')} Sqft</strong>
                </div>
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Lot Size</span>
                    <strong style="color: #fbbf24; font-size: 20px;">{details.get('lot_size_sqft')} Sqft</strong>
                </div>
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Year Built</span>
                    <strong style="color: #fbbf24; font-size: 20px;">{details.get('year_built')}</strong>
                </div>
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Bedrooms</span>
                    <strong style="color: #fff; font-size: 20px;">{details.get('bedrooms')} Beds</strong>
                </div>
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Bathrooms</span>
                    <strong style="color: #fff; font-size: 20px;">{details.get('bathrooms')} Baths</strong>
                </div>
                <div>
                    <span style="color: #9ca3af; font-size: 12px; display: block; text-transform: uppercase;">Document Parsed</span>
                    <strong style="color: #10b981; font-size: 16px;">Active PDF</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
