import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme
import data_manager

setup_page("AI Similarity Matcher & Gap Analysis", "TF-IDF & Cosine Similarity vector search & term gap recommendation engine", "🎯")

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Enter Profile or Query Vector")
st.markdown("<p style='color: #94A3B8;'>Input a candidate resume, job requirement, or review search query to calculate vector cosine similarity against all dataset records:</p>", unsafe_allow_html=True)

query_input = st.text_area("Input Search Query / Candidate Profile Text:", height=130, placeholder="Python data analytics machine learning engineer fast delivery excellent quality performance customer service")
top_k_select = st.slider("Top Matched Records to Retrieve", min_value=3, max_value=20, value=5)

if st.button("🎯 Calculate Vector Cosine Match & Gap Analysis", type="primary", use_container_width=True):
    if not query_input.strip():
        st.warning("Please enter text before running vector similarity matching.")
    else:
        with st.spinner("Transforming text vectors & calculating Cosine Similarities..."):
            matched_df = data_manager.match_similarity_vector(df, query_input, top_k=top_k_select)
            
        if not matched_df.empty:
            best_match = matched_df.iloc[0]
            top_score = best_match['Match_Score']
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.header("2️⃣ Highest Match Score & Overview")
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=top_score,
                    number={'suffix': "%"},
                    title={'text': "Top Similarity Match Score"},
                    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#06B6D4"}, 'bgcolor': "rgba(255,255,255,0.05)"}
                ))
                fig_gauge = apply_plotly_theme(fig_gauge)
                fig_gauge.update_layout(height=240, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            with col_m2:
                custom_metric_card("Top Match Score", f"{top_score}%", "Vector Cosine Similarity", icon="🏆", color="#06B6D4")
                custom_metric_card("Matches Retrieved", f"{len(matched_df)}", f"Top {top_k_select} ranked results", icon="📊", color="#22C55E")

            st.markdown("##### 🥇 Best Matching Record Text:")
            st.info(f"\"{best_match['Text']}\"")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.header("3️⃣ Top Matched Records Breakdown")
            
            fig_bar = px.bar(
                matched_df, 
                x='Match_Score', 
                y='Text', 
                orientation='h', 
                color='Match_Score', 
                color_continuous_scale='Teal',
                title="Top Ranked Similarity Scores (%)"
            )
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0), height=350)
            fig_bar = apply_plotly_theme(fig_bar)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            st.dataframe(matched_df[['Match_Score', 'Text', 'Label'] if 'Label' in matched_df.columns else ['Match_Score', 'Text']], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No matches found for the given query vector.")
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('</div>', unsafe_allow_html=True)
