import streamlit as st
import pandas as pd
from ui_utils import setup_page, custom_metric_card

setup_page("Dataset Overview", "Explore the raw unstructured product reviews", "📂")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("product_reviews.csv")
    except FileNotFoundError:
        st.error("Dataset not found!")
        st.stop()

df = load_data()

col1, col2, col3 = st.columns(3)
with col1:
    custom_metric_card("Total Rows", f"{df.shape[0]:,}", "Customer reviews loaded", icon="📄")
with col2:
    custom_metric_card("Total Columns", f"{df.shape[1]}", "Data attributes available", icon="🗂️", color="#06B6D4")
with col3:
    custom_metric_card("Missing Values", f"{df.isnull().sum().sum()}", "Incomplete records", icon="⚠️", color="#EF4444")

st.markdown("""
<div class="premium-card">
    <h3>🔍 Interactive Data Explorer</h3>
    <p style="color: #94A3B8; margin-bottom: 20px;">Search, sort, and filter the raw dataset before preprocessing.</p>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
