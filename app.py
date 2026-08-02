import streamlit as st
from ui_utils import setup_page

setup_page("Dashboard", "Welcome to the AI Powered Text Mining Platform", "🏠")

st.markdown("""
<div class="premium-card">
    <h2 style="color: #7C3AED;">Welcome to ReviewMiner AI 🤖</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        Transform your unstructured product reviews into actionable business intelligence using cutting-edge natural language processing and machine learning.
    </p>
    <p style="margin-top: 10px;">
        <a href="https://reviewminer-ai-bqtrdcudzerpmdporwzmxt.streamlit.app/" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: bold; font-size: 1.1rem;">🌐 View Live App</a>
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">📊</h1>
        <h3>Exploratory Data</h3>
        <p style="color: #94A3B8;">Dive deep into the raw datasets to uncover underlying patterns and distributions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="premium-card" style="text-align: center;">
        <h1 style="font-size: 3rem;">🤖</h1>
        <h3>Machine Learning</h3>
        <p style="color: #94A3B8;">Train and evaluate advanced classification models like Naive Bayes and SVM.</p>
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
        <li>Navigate to the <b>Dataset</b> tab to view the loaded product reviews.</li>
        <li>Perform data cleaning and tokenization in <b>Text Preprocessing</b>.</li>
        <li>Train your sentiment classifier in the <b>Machine Learning</b> dashboard.</li>
        <li>Test live inputs on the <b>Review Prediction</b> page.</li>
        <li>Export your final reports from the <b>Business Intelligence</b> module.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
