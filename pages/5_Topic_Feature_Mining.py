import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import data_manager

setup_page("Topic & Aspect Feature Mining", "LDA Topic Modeling, Aspect Feature Radar Chart, & Customer Complaint Extraction", "🔍")

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ LDA Topic Modeling (Unsupervised NLP)")
st.markdown("<p style='color: #94A3B8;'>Latent Dirichlet Allocation (LDA) groups reviews into key underlying themes:</p>", unsafe_allow_html=True)

with st.spinner("Extracting LDA Topic Clusters..."):
    topics = data_manager.perform_lda_topic_modeling(df, n_topics=4, n_words=6)

if topics:
    col_t1, col_t2 = st.columns(2)
    for idx, top in enumerate(topics):
        col_to_use = col_t1 if idx % 2 == 0 else col_t2
        with col_to_use:
            st.markdown(f"##### 📌 {top['topic_id']}")
            st.info(f"**Keywords:** {top['keywords']}")
else:
    st.info("Insufficient text vocabulary to extract LDA topics.")
st.markdown('</div>', unsafe_allow_html=True)

# Aspect Feature Mining (Radar Chart)
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("2️⃣ Aspect-Based Feature Popularity & Radar Chart")
st.markdown("<p style='color: #94A3B8;'>Customer satisfaction ratings across key product/service features:</p>", unsafe_allow_html=True)

aspects = data_manager.extract_aspect_sentiments(df)
if aspects:
    asp_df = pd.DataFrame(aspects)
    
    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=asp_df['positive_score'],
            theta=asp_df['aspect'],
            fill='toself',
            marker=dict(color='#06B6D4')
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Aspect Satisfaction Score Radar (%)"
        )
        fig_radar = apply_plotly_theme(fig_radar)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_r2:
        fig_bar = px.bar(asp_df, x='mentions', y='aspect', orientation='h', color='positive_score', color_continuous_scale='Teal', title="Feature Mention Frequencies")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_bar = apply_plotly_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Complaint Extraction
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("3️⃣ Customer Complaint & Friction Analysis")
st.markdown("<p style='color: #94A3B8;'>Key operational friction points and dissatisfaction categories:</p>", unsafe_allow_html=True)

complaints = data_manager.extract_complaint_categories(df)
if complaints:
    cmp_df = pd.DataFrame(complaints)
    fig_cmp = px.bar(cmp_df, x='count', y='category', orientation='h', color='count', color_continuous_scale='Reds', title="Top Customer Friction Categories")
    fig_cmp.update_layout(yaxis={'categoryorder':'total ascending'})
    fig_cmp = apply_plotly_theme(fig_cmp)
    st.plotly_chart(fig_cmp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
