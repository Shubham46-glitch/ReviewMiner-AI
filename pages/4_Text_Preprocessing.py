import streamlit as st
import pandas as pd
import re
import string
from ui_utils import setup_page, custom_metric_card

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    # We assume these are downloaded
    STOPWORDS = set(stopwords.words('english'))
    USE_NLTK = True
except ImportError:
    USE_NLTK = False
    STOPWORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r'\s+', ' ', text).strip()
    if USE_NLTK:
        words = word_tokenize(text)
    else:
        words = text.split()
    cleaned_words = [w for w in words if w not in STOPWORDS]
    return " ".join(cleaned_words)

setup_page("Text Preprocessing", "Clean, tokenize, and normalize raw text data", "🧹")

st.markdown("""
<div class="premium-card">
    <h3>Data Cleaning Pipeline</h3>
    <p style="color: #94A3B8;">The following preprocessing steps are applied to the raw text to prepare it for machine learning:</p>
    <ul style="color: #06B6D4;">
        <li>Convert all text to lowercase</li>
        <li>Remove punctuation and special characters</li>
        <li>Remove extra whitespace</li>
        <li>Tokenization</li>
        <li>Stopword removal</li>
    </ul>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_preprocess():
    try:
        df = pd.read_csv("product_reviews.csv")
    except FileNotFoundError:
        return None
    if 'Text' in df.columns:
        df['Cleaned_Text'] = df['Text'].apply(clean_text)
        return df
    return None

if st.button("🚀 Run Preprocessing Pipeline"):
    with st.spinner("Processing text..."):
        df_clean = load_and_preprocess()
        
    if df_clean is not None:
        st.success("Preprocessing Complete! The data is now ready for Text Mining.")
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("Transformation Results")
        
        col1, col2 = st.columns(2)
        with col1:
            custom_metric_card("Original Words", "Variable", "Raw messy text", icon="📝", color="#EF4444")
        with col2:
            custom_metric_card("Cleaned Tokens", "Optimized", "Ready for TF-IDF", icon="✨", color="#22C55E")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("Preview Preprocessed Data")
        st.dataframe(df_clean[['Text', 'Cleaned_Text']].head(20), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save happens in the background script typically, but we can do it here too if needed
        # df_clean.to_csv("product_reviews_cleaned.csv", index=False)
    else:
        st.error("Could not load or process 'product_reviews.csv'.")
else:
    st.info("Click the button above to execute the natural language processing pipeline.")
