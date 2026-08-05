import streamlit as st
import pandas as pd
import plotly.express as px
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme

setup_page("Exploratory Data Analysis", "Analyze distributions, missing values, and dataset properties", "📊")

import data_manager

df = data_manager.get_current_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.subheader("Dataset Summary Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    custom_metric_card("Total Reviews", f"{len(df):,}", "Total records", icon="📄")
with col2:
    custom_metric_card("Rows & Columns", f"{df.shape[0]} × {df.shape[1]}", "Matrix shape", icon="📐", color="#06B6D4")
with col3:
    custom_metric_card("Missing Values", f"{df.isnull().sum().sum()}", "Needs imputation", icon="⚠️", color="#FACC15")
with col4:
    custom_metric_card("Duplicates", f"{df.duplicated().sum()}", "Redundant rows", icon="👯", color="#EF4444")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.subheader("Column Information")
col_info1, col_info2 = st.columns(2)
with col_info1:
    types_df = pd.DataFrame(df.dtypes, columns=['Data Type']).reset_index().rename(columns={'index': 'Column Name'})
    st.dataframe(types_df, use_container_width=True)
with col_info2:
    missing_df = pd.DataFrame(df.isnull().sum(), columns=['Missing Values']).reset_index().rename(columns={'index': 'Column Name'})
    st.dataframe(missing_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if 'Label' in df.columns:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Sentiment Distribution")
    col_plot1, col_plot2 = st.columns(2)
    
    sentiment_counts = df['Label'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    color_map = {"Positive": "#22C55E", "Neutral": "#FACC15", "Negative": "#EF4444"}
    
    with col_plot1:
        fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, title="Sentiment Share")
        fig_pie = apply_plotly_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_plot2:
        fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment', color_discrete_map=color_map, text_auto=True, title="Sentiment Counts")
        fig_bar = apply_plotly_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if 'Window' in df.columns:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Platform Analysis")
    platform_counts = df['Window'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Count']
    
    fig_plat = px.bar(platform_counts, x='Count', y='Platform', orientation='h', color='Platform', title="Reviews by Platform")
    fig_plat = apply_plotly_theme(fig_plat)
    st.plotly_chart(fig_plat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Statistical Distribution Analytics (Box Plots & Violin Plots)
if 'Text' in df.columns:
    df_stat = df.copy()
    df_stat['Word_Count'] = df_stat['Text'].astype(str).str.split().str.len()
    df_stat['Char_Length'] = df_stat['Text'].astype(str).str.len()

    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("📈 Statistical Text Length & Word Count Distributions")
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if 'Label' in df_stat.columns:
            fig_box = px.box(df_stat, x='Label', y='Word_Count', color='Label', color_discrete_map={"Positive": "#22C55E", "Neutral": "#FACC15", "Negative": "#EF4444"}, title="Word Count Box Plot by Sentiment")
        else:
            fig_box = px.box(df_stat, y='Word_Count', title="Word Count Box Plot")
        fig_box = apply_plotly_theme(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_s2:
        if 'Label' in df_stat.columns:
            fig_violin = px.violin(df_stat, x='Label', y='Char_Length', color='Label', box=True, points="all", color_discrete_map={"Positive": "#22C55E", "Neutral": "#FACC15", "Negative": "#EF4444"}, title="Character Length Violin Plot")
        else:
            fig_violin = px.violin(df_stat, y='Char_Length', box=True, points="all", title="Character Length Violin Plot")
        fig_violin = apply_plotly_theme(fig_violin)
        st.plotly_chart(fig_violin, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
