import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import data_manager

setup_page("K-Means Clustering Analytics", "Unsupervised Machine Learning segmentation & 2D PCA visualization", "🧩")

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

st.sidebar.header("🎛️ Clustering Controls")
k_val = st.sidebar.slider("Number of Clusters (K)", min_value=2, max_value=6, value=3)

with st.spinner("Computing TF-IDF vectors & K-Means clusters..."):
    df_clustered, kmeans_model, vectorizer = data_manager.compute_kmeans_clusters(df, n_clusters=k_val)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Cluster Summary Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    custom_metric_card("Total Samples", f"{len(df_clustered):,}", "Clustered records", icon="📄")
with col2:
    custom_metric_card("Clusters (K)", f"{k_val}", "Market Segments", icon="🧩", color="#06B6D4")
with col3:
    largest_c = df_clustered['Cluster'].value_counts().idxmax() if 'Cluster' in df_clustered.columns else "N/A"
    custom_metric_card("Largest Segment", largest_c, "Dominant Group", icon="📊", color="#22C55E")
with col4:
    inertia_val = f"{kmeans_model.inertia_:.1f}" if kmeans_model else "N/A"
    custom_metric_card("Model Inertia", inertia_val, "Sum of Squared Errors", icon="⚡", color="#FACC15")
st.markdown('</div>', unsafe_allow_html=True)

if 'PCA_1' in df_clustered.columns and 'PCA_2' in df_clustered.columns:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("2️⃣ 2D PCA Cluster Map")
    st.markdown("<p style='color: #94A3B8;'>High-dimensional TF-IDF vectors reduced to 2D principal components via PCA.</p>", unsafe_allow_html=True)
    
    fig_pca = px.scatter(
        df_clustered, 
        x='PCA_1', 
        y='PCA_2', 
        color='Cluster', 
        hover_data=['Text', 'Label'] if 'Label' in df_clustered.columns else ['Text'],
        color_discrete_sequence=px.colors.qualitative.Vivid,
        title="Unsupervised Text Cluster Map (PCA projection)"
    )
    fig_pca.update_traces(marker=dict(size=9, opacity=0.8, line=dict(width=1, color='White')))
    fig_pca = apply_plotly_theme(fig_pca)
    st.plotly_chart(fig_pca, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("3️⃣ Cluster Profiles & Top Keywords")

selected_c = st.selectbox("Select Cluster to inspect profile:", sorted(df_clustered['Cluster'].unique().tolist()))
c_df = df_clustered[df_clustered['Cluster'] == selected_c]

col_c1, col_c2 = st.columns([1, 2])
with col_c1:
    custom_metric_card("Cluster Size", f"{len(c_df):,}", f"{(len(c_df)/len(df_clustered)*100):.1f}% of total data", icon="👥")
    if 'Label' in c_df.columns:
        s_counts = c_df['Label'].value_counts().reset_index()
        s_counts.columns = ['Sentiment', 'Count']
        fig_pie = px.pie(s_counts, names='Sentiment', values='Count', title=f"Sentiment in {selected_c}", hole=0.3)
        fig_pie = apply_plotly_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

with col_c2:
    if not c_df['Cleaned_Text'].empty:
        try:
            vec = CountVectorizer(stop_words='english', max_features=15).fit(c_df['Cleaned_Text'])
            bag = vec.transform(c_df['Cleaned_Text'])
            sum_words = bag.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            top_w_df = pd.DataFrame(sorted(words_freq, key=lambda x: x[1], reverse=True), columns=['Word', 'Frequency'])
            
            fig_kw = px.bar(top_w_df, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Purples', title=f"Top 15 Distinct Keywords in {selected_c}")
            fig_kw.update_layout(yaxis={'categoryorder':'total ascending'})
            fig_kw = apply_plotly_theme(fig_kw)
            st.plotly_chart(fig_kw, use_container_width=True)
        except Exception:
            st.info("Insufficient keyword tokens in this cluster.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("4️⃣ Clustered Data Table")
st.dataframe(c_df[['Cluster', 'Text', 'Label'] if 'Label' in c_df.columns else ['Cluster', 'Text']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
