import streamlit as st
from ui_utils import setup_page

setup_page("Anomaly Detection", "Consolidated into Machine Learning Dashboard", "⚠️")

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("⚠️ Outlier & Anomaly Detection Module")
st.info("ℹ️ All Machine Learning algorithms (including **Isolation Forest Anomaly Detection**) are consolidated into **Page 7: Machine Learning**.")
st.markdown("Navigate to **7_Machine_Learning ➔ Tab 4: Anomaly Detection** in the sidebar to run anomaly analysis on your active dataset.")
st.markdown('</div>', unsafe_allow_html=True)
