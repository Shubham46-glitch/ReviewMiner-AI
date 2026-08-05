import streamlit as st
import pandas as pd
import plotly.express as px
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import time

setup_page("Sentiment Analysis Dashboard", "Analyze customer sentiment distribution and business insights.", "😊")

import data_manager

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

if 'Label' not in df.columns: df['Label'] = 'Neutral'
if 'Window' not in df.columns: df['Window'] = 'Unknown'
if 'Text' not in df.columns: df['Text'] = df.get('Cleaned_Text', '')

st.sidebar.header("🎛️ Dashboard Filters")
platforms = df['Window'].dropna().unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform", options=platforms, default=platforms)

sentiments = df['Label'].dropna().unique().tolist()
selected_sentiments = st.sidebar.multiselect("Select Sentiment", options=sentiments, default=sentiments)
search_keyword = st.sidebar.text_input("Search Keyword in Reviews", "")
max_val = max(1, len(df))
min_val = min(10, max_val)
num_reviews = st.sidebar.slider("Number of Reviews in Table", min_value=min_val, max_value=max_val, value=min(100, max_val))

filtered_df = df[df['Window'].isin(selected_platforms) & df['Label'].isin(selected_sentiments)]
if search_keyword:
    filtered_df = filtered_df[filtered_df['Text'].astype(str).str.contains(search_keyword, case=False, na=False)]

if filtered_df.empty:
    st.warning("No data matches your current filters.")
    st.stop()

total_reviews = len(filtered_df)
pos_count = len(filtered_df[filtered_df['Label'] == 'Positive'])
neu_count = len(filtered_df[filtered_df['Label'] == 'Neutral'])
neg_count = len(filtered_df[filtered_df['Label'] == 'Negative'])

def get_percentage(part, whole):
    return f"{(part / whole) * 100:.1f}%" if whole > 0 else "0%"

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    custom_metric_card("Total Reviews", f"{total_reviews:,}", "Processed records", icon="📄")
with col2:
    custom_metric_card("Positive", f"{pos_count:,}", get_percentage(pos_count, total_reviews), icon="😊", color="#22C55E")
with col3:
    custom_metric_card("Neutral", f"{neu_count:,}", get_percentage(neu_count, total_reviews), icon="😐", color="#FACC15")
with col4:
    custom_metric_card("Negative", f"{neg_count:,}", get_percentage(neg_count, total_reviews), icon="😡", color="#EF4444")
st.markdown('</div>', unsafe_allow_html=True)

st.header("📊 Sentiment Distribution")
col_chart1, col_chart2 = st.columns(2)
color_map = {"Positive": "#22C55E", "Negative": "#EF4444", "Neutral": "#FACC15"}

sentiment_counts = filtered_df['Label'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

with col_chart1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, hole=0.4)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie = apply_plotly_theme(fig_pie)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment', color_discrete_map=color_map, text_auto=True)
    fig_bar = apply_plotly_theme(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.header("🏢 Platform-wise Sentiment")
platform_sentiment = filtered_df.groupby(['Window', 'Label']).size().reset_index(name='Count')

col_plat1, col_plat2 = st.columns(2)
with col_plat1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_stacked = px.bar(platform_sentiment, x='Window', y='Count', color='Label', color_discrete_map=color_map, barmode='stack')
    fig_stacked = apply_plotly_theme(fig_stacked)
    st.plotly_chart(fig_stacked, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_plat2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_grouped = px.bar(platform_sentiment, x='Window', y='Count', color='Label', color_discrete_map=color_map, barmode='group')
    fig_grouped = apply_plotly_theme(fig_grouped)
    st.plotly_chart(fig_grouped, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.header("📋 Sentiment Data Table")
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
display_df = filtered_df[['Text', 'Window', 'Label']].head(num_reviews).copy()
display_df.rename(columns={'Text': 'Review Text', 'Window': 'Platform', 'Label': 'Sentiment'}, inplace=True)
st.dataframe(display_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
