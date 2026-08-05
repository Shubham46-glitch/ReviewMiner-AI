import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import data_manager

setup_page("Product & Brand Intelligence", "Hierarchical Treemaps, Sunburst diagrams, & Product rating distribution analytics", "🏢")

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

schema = data_manager.detect_dataset_schema(df)
product_col = schema['product']
brand_col = schema['brand']
cat_col = schema['category']
rating_col = schema['rating']

if not any([product_col, brand_col, cat_col, rating_col]):
    st.info("ℹ️ This dataset does not contain explicit Product, Brand, Category, or Rating columns. Dynamic product analytics are safely suppressed for this dataset.")
    st.stop()

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Product & Brand Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    uniq_p = df[product_col].nunique() if product_col and product_col in df.columns else "N/A"
    custom_metric_card("Unique Products", f"{uniq_p}", "Catalog items", icon="📦")
with col2:
    uniq_b = df[brand_col].nunique() if brand_col and brand_col in df.columns else "N/A"
    custom_metric_card("Unique Brands", f"{uniq_b}", "Manufacturers", icon="🏢", color="#06B6D4")
with col3:
    uniq_c = df[cat_col].nunique() if cat_col and cat_col in df.columns else "N/A"
    custom_metric_card("Categories", f"{uniq_c}", "Product divisions", icon="🏷️", color="#22C55E")
with col4:
    avg_r = f"{df[rating_col].mean():.2f} / 5" if rating_col and rating_col in df.columns else "N/A"
    custom_metric_card("Average Rating", avg_r, "Overall score", icon="⭐", color="#FACC15")
st.markdown('</div>', unsafe_allow_html=True)

# Hierarchical Treemap & Sunburst
path_cols = [c for c in [cat_col, brand_col, product_col] if c and c in df.columns]

if path_cols:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("2️⃣ Hierarchical Treemap & Sunburst Visualization")
    st.markdown("<p style='color: #94A3B8;'>Drill down across product categories, brands, and items:</p>", unsafe_allow_html=True)
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        fig_tree = px.treemap(df, path=path_cols, title="Product Hierarchy Treemap")
        fig_tree = apply_plotly_theme(fig_tree)
        st.plotly_chart(fig_tree, use_container_width=True)
        
    with col_v2:
        fig_sun = px.sunburst(df, path=path_cols, title="Product Hierarchy Sunburst")
        fig_sun = apply_plotly_theme(fig_sun)
        st.plotly_chart(fig_sun, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Rating Box Plot by Category / Brand
if rating_col and rating_col in df.columns:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("3️⃣ Rating Box Plot Distributions")
    group_col = cat_col if cat_col and cat_col in df.columns else (brand_col if brand_col and brand_col in df.columns else product_col)
    
    if group_col:
        fig_box = px.box(df, x=group_col, y=rating_col, color=group_col, title=f"Rating Distribution by {group_col}")
        fig_box = apply_plotly_theme(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
