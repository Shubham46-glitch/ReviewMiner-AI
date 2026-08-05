import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import data_manager

setup_page("Anomaly Detection Engine", "Unsupervised Isolation Forest market outlier & suspicious pattern detector", "⚠️")

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

st.sidebar.header("🎛️ Anomaly Sensitivity")
contamination_val = st.sidebar.slider("Contamination Rate (Expected Outliers %)", min_value=0.01, max_value=0.20, value=0.05, step=0.01)

with st.spinner("Executing Isolation Forest anomaly model..."):
    df_anomalies = data_manager.detect_anomalies(df, contamination=contamination_val)

anomaly_cnt = len(df_anomalies[df_anomalies['Is_Anomaly'] == 'Anomaly ⚠️'])
normal_cnt = len(df_anomalies[df_anomalies['Is_Anomaly'] == 'Normal ✅'])

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Anomaly Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    custom_metric_card("Total Examined", f"{len(df_anomalies):,}", "Records evaluated", icon="📄")
with col2:
    custom_metric_card("Flagged Outliers", f"{anomaly_cnt:,}", f"{(anomaly_cnt/len(df_anomalies)*100):.1f}% of dataset", icon="⚠️", color="#EF4444")
with col3:
    custom_metric_card("Normal Records", f"{normal_cnt:,}", f"{(normal_cnt/len(df_anomalies)*100):.1f}% baseline", icon="✅", color="#22C55E")
with col4:
    custom_metric_card("Sensitivity Rate", f"{contamination_val*100:.0f}%", "Contamination parameter", icon="🎛️", color="#06B6D4")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("2️⃣ Anomaly Decision Score Distribution")
st.markdown("<p style='color: #94A3B8;'>Isolation Forest calculates anomaly scores based on random partition depth. Lower scores indicate rare/outlier records.</p>", unsafe_allow_html=True)

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    fig_scatter = px.scatter(
        df_anomalies, 
        x='Char_Length', 
        y='Anomaly_Score', 
        color='Is_Anomaly',
        color_discrete_map={"Normal ✅": "#22C55E", "Anomaly ⚠️": "#EF4444"},
        hover_data=['Text'],
        title="Anomaly Score vs Text Character Length"
    )
    fig_scatter = apply_plotly_theme(fig_scatter)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_viz2:
    fig_hist = px.histogram(
        df_anomalies, 
        x='Anomaly_Score', 
        color='Is_Anomaly',
        color_discrete_map={"Normal ✅": "#22C55E", "Anomaly ⚠️": "#EF4444"},
        title="Anomaly Decision Score Distribution"
    )
    fig_hist = apply_plotly_theme(fig_hist)
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("3️⃣ Flagged Outliers & Anomalous Records")
st.markdown("<p style='color: #94A3B8;'>Review the top flagged records containing anomalous length, vocabulary, or structural patterns:</p>", unsafe_allow_html=True)

anomalies_only = df_anomalies[df_anomalies['Is_Anomaly'] == 'Anomaly ⚠️'].sort_values('Anomaly_Score').reset_index(drop=True)
if not anomalies_only.empty:
    st.dataframe(anomalies_only[['Anomaly_Score', 'Char_Length', 'Word_Count', 'Text', 'Label'] if 'Label' in anomalies_only.columns else ['Anomaly_Score', 'Char_Length', 'Word_Count', 'Text']], use_container_width=True)
else:
    st.info("No anomalies detected at the current sensitivity setting.")
st.markdown('</div>', unsafe_allow_html=True)
