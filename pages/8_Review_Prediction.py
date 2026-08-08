import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ui_utils import setup_page, apply_plotly_theme, check_dataset_loaded
import data_manager
from backend.app.services.ml_engine import GLOBAL_ML_ENGINE

setup_page("AI Sentiment Prediction", "Enter a review or comment and let the trained model predict its sentiment.", "🔮")
check_dataset_loaded()

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset uploaded yet. Please upload a dataset in the Dataset Upload Center.")
    st.stop()

# Ensure model is trained on active dataset
schema = data_manager.detect_dataset_schema(df)
text_col = schema['text'] or ('Text' if 'Text' in df.columns else df.columns[0])

if 'Label' not in df.columns:
    df['Label'] = df['Text'].apply(data_manager.predict_vader_sentiment)

if GLOBAL_ML_ENGINE.pipeline is None:
    try:
        GLOBAL_ML_ENGINE.train_model(df, dataset_id="active_dataset", text_col=text_col)
    except Exception:
        pass

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("📝 Enter Review or Comment")
st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Write or paste any customer review, product comment, or feedback text below.</p>", unsafe_allow_html=True)

# Sample review helper buttons
col_s1, col_s2, col_s3 = st.columns(3)
if 'pred_input' not in st.session_state:
    st.session_state['pred_input'] = "The product quality is excellent and delivery was very fast. Highly recommend!"

with col_s1:
    if st.button("Sample Positive", use_container_width=True):
        st.session_state['pred_input'] = "The product quality is excellent and delivery was very fast. Highly recommend!"
with col_s2:
    if st.button("Sample Neutral", use_container_width=True):
        st.session_state['pred_input'] = "The product arrived yesterday and I have used it twice."
with col_s3:
    if st.button("Sample Negative", use_container_width=True):
        st.session_state['pred_input'] = "This is a terrible product. The quality is poor and I am very disappointed."

user_review = st.text_area("Write or paste a review here...", value=st.session_state['pred_input'], height=130)

if st.button("🔮 Predict Sentiment", type="primary", use_container_width=True):
    if not user_review or not user_review.strip():
        st.warning("⚠️ Please enter a review to classify.")
    else:
        with st.spinner("Predicting sentiment via AI sentiment engine..."):
            res = GLOBAL_ML_ENGINE.predict_sentiment(user_review)
            
            if res.get("status") == "error":
                st.error(f"⚠️ {res.get('detail')}")
            else:
                sent = res['predicted_sentiment']
                conf = res.get('confidence')
                probs = res.get('probabilities', {})
                model_used = res.get('model_used', 'Trained Sentiment Model')

                # Color & Emoji map
                if sent.lower() in ['positive', 'pos', '5', '4']:
                    pred_color = "#22C55E"
                    emoji = "🟢"
                    display_sent = "POSITIVE"
                elif sent.lower() in ['negative', 'neg', '1', '2']:
                    pred_color = "#EF4444"
                    emoji = "🔴"
                    display_sent = "NEGATIVE"
                else:
                    pred_color = "#FACC15"
                    emoji = "🟡"
                    display_sent = "NEUTRAL"

                st.markdown('</div>', unsafe_allow_html=True)
                
                # Result Container
                st.markdown('<div class="premium-card">', unsafe_allow_html=True)
                st.header("🎯 Prediction Result")
                
                conf_text = f"<h3 style='text-align: center; color: #94A3B8; margin-top: 5px;'>Confidence: {conf:.1f}%</h3>" if conf is not None else ""
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.9); border-left: 6px solid {pred_color}; border-radius: 12px; padding: 25px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5);">
                    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Predicted Sentiment</div>
                    <h1 style="color: {pred_color}; text-align: center; font-size: 2.5rem; margin: 10px 0; font-weight: 900;">{emoji} {display_sent}</h1>
                    {conf_text}
                    <div style="text-align: center; color: #64748B; font-size: 0.8rem; margin-top: 10px;">Classifier Model: <b>{model_used}</b></div>
                </div>
                """, unsafe_allow_html=True)

                # Sentiment Probabilities Breakdown
                if probs and len(probs) > 0:
                    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
                    st.subheader("📊 Sentiment Class Probabilities")
                    
                    prob_df = pd.DataFrame({'Sentiment': list(probs.keys()), 'Probability (%)': list(probs.values())})
                    color_discrete = {"Positive": "#22C55E", "Negative": "#EF4444", "Neutral": "#FACC15"}
                    
                    fig_bar = px.bar(
                        prob_df, 
                        x='Probability (%)', 
                        y='Sentiment', 
                        orientation='h', 
                        color='Sentiment', 
                        color_discrete_map=color_discrete, 
                        text_auto='.1f',
                        title="Sentiment Class Probability Breakdown"
                    )
                    fig_bar = apply_plotly_theme(fig_bar)
                    fig_bar.update_layout(
                        xaxis=dict(title=dict(text="Probability (%)", font=dict(color="#94A3B8", size=12)), range=[0, 100]),
                        yaxis=dict(title=dict(text="Sentiment Class", font=dict(color="#94A3B8", size=12))),
                        showlegend=False,
                        height=240
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.markdown('</div>', unsafe_allow_html=True)
