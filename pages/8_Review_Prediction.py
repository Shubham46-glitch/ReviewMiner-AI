import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import string
import datetime
import plotly.express as px
import plotly.graph_objects as go
from ui_utils import setup_page, apply_plotly_theme
import time

setup_page("Review Sentiment Prediction", "Enter a product review and let AI predict its sentiment.", "🔮")

@st.cache_resource
def load_models():
    try:
        model = joblib.load("sentiment_model.pkl")
        vectorizer = joblib.load("tfidf_vectorizer.pkl")
        return model, vectorizer
    except FileNotFoundError:
        return None, None

model, vectorizer = load_models()
if not model or not vectorizer:
    st.error("Model or Vectorizer not found! Go to the Machine Learning Dashboard to train them.")
    st.stop()

STOPWORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    cleaned_words = [w for w in words if w not in STOPWORDS]
    return " ".join(cleaned_words)

if 'prediction_history' not in st.session_state: st.session_state.prediction_history = []
if 'review_input' not in st.session_state: st.session_state.review_input = ""

def set_sample(text):
    st.session_state.review_input = text

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Input Review")
col_samp1, col_samp2, col_samp3 = st.columns(3)
with col_samp1:
    st.button("Sample Positive", on_click=set_sample, args=("The product quality is excellent and delivery was very fast. Highly recommend!",), use_container_width=True)
with col_samp2:
    st.button("Sample Neutral", on_click=set_sample, args=("It's an okay product. Does the job, but nothing special for the price.",), use_container_width=True)
with col_samp3:
    st.button("Sample Negative", on_click=set_sample, args=("Terrible experience. The item arrived broken and customer service ignored my emails.",), use_container_width=True)

user_review = st.text_area("Write your product review here...", value=st.session_state.review_input, key="review_input", height=150)

if st.button("🔮 Predict Sentiment", type="primary"):
    if not user_review.strip():
        st.warning("Please enter a review to predict.")
    else:
        with st.spinner("Analyzing text..."):
            time.sleep(0.5)
            cleaned_review = clean_text(user_review)
            X_input = vectorizer.transform([cleaned_review])
            prediction = model.predict(X_input)[0]
            probabilities = model.predict_proba(X_input)[0]
            classes = model.classes_
            confidence = np.max(probabilities) * 100
            
            color_map = {"Positive": "#00CC96", "Negative": "#EF553B", "Neutral": "#F3C01E"}
            emoji_map = {"Positive": "😊", "Negative": "😡", "Neutral": "😐"}
            pred_color = color_map.get(prediction, "white")
            pred_emoji = emoji_map.get(prediction, "🤔")
            
            st.session_state.prediction_history.insert(0, {
                "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Review": user_review,
                "Prediction": prediction,
                "Confidence": f"{confidence:.1f}%"
            })
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.header("2️⃣ Prediction Result")
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #111827, #1f2937); border-left: 5px solid {pred_color}; padding: 20px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);">
                <h1 style="color: {pred_color}; text-align: center;">{pred_emoji} {prediction.upper()}</h1>
                <h3 style="text-align: center; color: #94A3B8;">Confidence: {confidence:.1f}%</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Confidence Score Visualization")
            col_viz1, col_viz2 = st.columns(2)
            with col_viz1:
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = confidence,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': f"{prediction} Probability"},
                    gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': pred_color}, 'bgcolor': "rgba(255,255,255,0.05)"}
                ))
                fig_gauge = apply_plotly_theme(fig_gauge)
                st.plotly_chart(fig_gauge, use_container_width=True)
                
            with col_viz2:
                prob_df = pd.DataFrame({'Sentiment': classes, 'Probability': probabilities * 100})
                fig_bar = px.bar(prob_df, x='Probability', y='Sentiment', orientation='h', color='Sentiment', color_discrete_map=color_map)
                fig_bar = apply_plotly_theme(fig_bar)
                fig_bar.update_layout(xaxis_range=[0,100], showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
                
            st.subheader("How did the AI decide?")
            feature_names = vectorizer.get_feature_names_out()
            nonzero_indices = X_input.nonzero()[1]
            if len(nonzero_indices) > 0:
                words_used = [feature_names[idx] for idx in nonzero_indices]
                keywords_html = " ".join([f"<span style='background: rgba(124, 58, 237, 0.2); padding: 5px 10px; border-radius: 15px; margin-right: 5px; display: inline-block; margin-bottom: 5px; border: 1px solid #7C3AED;'>{w}</span>" for w in words_used])
                st.markdown(f"<p style='color: #94A3B8;'>The model successfully extracted {len(words_used)} important keywords from your review:</p>", unsafe_allow_html=True)
                st.markdown(keywords_html, unsafe_allow_html=True)
            else:
                st.info("The review did not contain any significant keywords recognized by the model's vocabulary.")
else:
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🕰️ Prediction History")
if len(st.session_state.prediction_history) > 0:
    history_df = pd.DataFrame(st.session_state.prediction_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)
    st.download_button("📥 Download CSV", data=history_df.to_csv(index=False).encode('utf-8'), file_name='history.csv', mime='text/csv')
else:
    st.info("No predictions made yet in this session.")
st.markdown('</div>', unsafe_allow_html=True)
