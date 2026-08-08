import streamlit as st
import data_manager
from ui_utils import setup_page

is_custom = data_manager.is_custom_data_active()

if st.session_state.get('just_uploaded'):
    st.toast("Dataset uploaded successfully. Analytics generated.", icon="🎉")
    st.session_state['just_uploaded'] = False

if not is_custom:
    setup_page("Upload Dataset", "Upload a dataset to unlock analytics", "📂")
    st.warning("🔒 Upload a dataset to unlock analytics.")
    
    st.markdown("""
    <div class="premium-card" style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 10px;">📂</h1>
        <h2 style="color: #7C3AED; margin-bottom: 10px;">Upload Dataset Required</h2>
        <p style="color: #94A3B8; font-size: 1.1rem; max-width: 600px; margin: 0 auto 25px auto; line-height: 1.6;">
            The application cannot generate analytics until a dataset is uploaded. Please upload a dataset below to unlock EDA, sentiment analysis, topic mining, and machine learning.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    if st.button("📤 Open Dataset Upload Center", type="primary", use_container_width=True):
        st.switch_page("pages/2_Dataset.py")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

setup_page("Dashboard", "Welcome to the AI Powered Text Mining Platform", "🏠")

ds_name = data_manager.get_dataset_name()
curr_df = data_manager.get_current_df()

st.markdown("""
<div class="premium-card">
    <h2 style="color: #7C3AED;">Welcome to ReviewMiner AI 🤖</h2>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        Transform your unstructured text data into actionable intelligence using advanced Natural Language Processing, Sentiment Analysis, and Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# Active Dataset Banner
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
col_banner1, col_banner2 = st.columns([3, 1])
with col_banner1:
    st.markdown(f"""
    <h3 style="color: #06B6D4; margin: 0;">📁 Uploaded Dataset: {ds_name}</h3>
    <p style="color: #94A3B8; margin-top: 5px;">Loaded <b>{len(curr_df):,}</b> custom text records. All text mining modules are operating on your uploaded data.</p>
    """, unsafe_allow_html=True)
with col_banner2:
    if st.button("📤 Change Dataset", use_container_width=True, type="primary"):
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
    <h3>🚀 Workflow Overview</h3>
    <ol style="color: #94A3B8; font-size: 1.1rem; line-height: 1.8;">
        <li><b>Upload Dataset</b> ➔ Upload your custom CSV/TXT dataset.</li>
        <li><b>Dashboard</b> ➔ View overall dataset summary metrics and active dataset info.</li>
        <li><b>EDA</b> ➔ Explore word counts, character distributions, and token frequency.</li>
        <li><b>Topic & Aspect Mining</b> ➔ Discover main topics and aspect sentiment breakdown.</li>
        <li><b>Sentiment Analysis</b> ➔ Analyze positive, negative, and neutral sentiment distributions.</li>
        <li><b>Machine Learning</b> ➔ Train Naive Bayes and SVM models on your text data.</li>
        <li><b>Prediction</b> ➔ Test live single review sentiment predictions.</li>
        <li><b>Business Intelligence</b> ➔ Extract automated executive recommendations and reports.</li>
    </ol>
</div>
""", unsafe_allow_html=True)
