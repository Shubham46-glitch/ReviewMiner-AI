import streamlit as st
import data_manager
from ui_utils import setup_page

setup_page("Dashboard", "Welcome to the AI Powered Text Mining Platform", "🏠")

is_custom = data_manager.is_custom_data_active()
ds_name = data_manager.get_dataset_name()
curr_df = data_manager.get_current_df()

st.markdown("""
<div class="premium-card">
    <h2 style="color: #7C3AED;">Welcome to ReviewMiner AI 🤖</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        Transform your unstructured text data into actionable intelligence using advanced Natural Language Processing, Sentiment Analysis, and Machine Learning.
    </p>
    <p style="margin-top: 10px;">
        <a href="https://reviewminer-ai-bqtrdcudzerpmdporwzmxt.streamlit.app/" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: bold; font-size: 1.1rem;">🌐 View Live App</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Active Dataset Banner
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
col_banner1, col_banner2 = st.columns([3, 1])
with col_banner1:
    if is_custom:
        st.markdown(f"""
        <h3 style="color: #06B6D4; margin: 0;">📁 Uploaded Dataset: {ds_name}</h3>
        <p style="color: #94A3B8; margin-top: 5px;">Loaded <b>{len(curr_df):,}</b> custom text records. All text mining modules are operating on your uploaded data.</p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <h3 style="color: #7C3AED; margin: 0;">📤 Upload Text Dataset</h3>
        <p style="color: #94A3B8; margin-top: 5px;">Upload your custom CSV, TXT, or Excel dataset to run text mining and machine learning on your own data!</p>
        """, unsafe_allow_html=True)
with col_banner2:
    if st.button("📤 Upload Text Data", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Dataset.py")
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">📊</h1>
        <h3>Exploratory Data</h3>
        <p style="color: #94A3B8;">Dive deep into raw or uploaded text data to uncover underlying distributions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">🤖</h1>
        <h3>Machine Learning</h3>
        <p style="color: #94A3B8;">Train and evaluate classification models directly on your text dataset.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">📈</h1>
        <h3>Business Intelligence</h3>
        <p style="color: #94A3B8;">Extract key strategic insights and automated recommendations for executives.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="premium-card">
    <h3>🚀 Quick Start Guide</h3>
    <ol style="color: #94A3B8; font-size: 1.1rem; line-height: 1.8;">
        <li>Navigate to the <b>Dataset Upload & Info</b> tab to upload your own CSV/TXT text dataset.</li>
        <li>Perform tokenization, lowercasing, and stopword cleaning in <b>Text Preprocessing</b>.</li>
        <li>Explore word clouds, n-grams, and TF-IDF key terms in <b>Text Mining</b>.</li>
        <li>Train Naive Bayes / SVM classifiers on your uploaded dataset in <b>Machine Learning</b>.</li>
        <li>Test live single reviews on <b>Review Prediction</b> & export executive reports in <b>Business Intelligence</b>.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
