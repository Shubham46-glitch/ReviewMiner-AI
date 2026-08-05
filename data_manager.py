import streamlit as st
import pandas as pd
import numpy as np
import re
import string
from preprocess import clean_text

try:
    import nltk
    nltk.download('vader_lexicon', quiet=True)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    VADER_ANALYZER = SentimentIntensityAnalyzer()
    HAS_VADER = True
except Exception:
    VADER_ANALYZER = None
    HAS_VADER = False

def init_session_state():
    if "is_custom_dataset" not in st.session_state:
        st.session_state["is_custom_dataset"] = False
    if "dataset_name" not in st.session_state:
        st.session_state["dataset_name"] = "No Dataset Loaded"
    if "raw_df" not in st.session_state:
        st.session_state["raw_df"] = None
    if "cleaned_df" not in st.session_state:
        st.session_state["cleaned_df"] = None

def get_current_df():
    init_session_state()
    if st.session_state.raw_df is not None:
        return st.session_state.raw_df
    return pd.DataFrame(columns=["Text", "Label", "Window", "Cleaned_Text"])

def get_cleaned_df():
    init_session_state()
    if st.session_state.cleaned_df is not None:
        return st.session_state.cleaned_df
    return pd.DataFrame(columns=["Text", "Label", "Window", "Cleaned_Text"])

def is_custom_data_active():
    init_session_state()
    return st.session_state.raw_df is not None

def get_dataset_name():
    init_session_state()
    return st.session_state.dataset_name

def read_file_with_encodings(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith('.xlsx') or name.endswith('.xls'):
        return pd.read_excel(uploaded_file)
    
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
    for enc in encodings:
        try:
            uploaded_file.seek(0)
            sep = '\t' if name.endswith('.tsv') else ','
            df = pd.read_csv(uploaded_file, encoding=enc, sep=sep)
            return df
        except Exception:
            continue
            
    uploaded_file.seek(0)
    return pd.read_csv(uploaded_file, on_bad_lines='skip')

def auto_detect_columns(df):
    cols = df.columns.tolist()
    text_col = None
    label_col = None
    platform_col = None

    text_candidates = ['text', 'review', 'reviews', 'comment', 'comments', 'feedback', 'description', 'message', 'content', 'body', 'job_description', 'title', 'summary', 'tweet', 'tweets', 'statement', 'opinion', 'post', 'posts', 'input']
    for col in cols:
        if col.lower() in text_candidates:
            text_col = col
            break
            
    if not text_col:
        max_avg_len = -1
        for col in cols:
            if df[col].dtype == 'object' or str(df[col].dtype) == 'string':
                avg_len = df[col].astype(str).str.len().mean()
                if avg_len > max_avg_len:
                    max_avg_len = avg_len
                    text_col = col
        if not text_col and len(cols) > 0:
            text_col = cols[0]

    label_candidates = ['label', 'sentiment', 'rating', 'score', 'stars', 'category', 'target', 'class', 'type', 'polarity']
    for col in cols:
        if col != text_col and col.lower() in label_candidates:
            label_col = col
            break

    platform_candidates = ['window', 'platform', 'source', 'channel', 'device', 'app', 'store', 'company', 'location', 'source_name']
    for col in cols:
        if col not in [text_col, label_col] and col.lower() in platform_candidates:
            platform_col = col
            break

    return text_col, label_col, platform_col

def predict_vader_sentiment(text):
    if not isinstance(text, str) or not text.strip():
        return "Neutral"
    if HAS_VADER and VADER_ANALYZER:
        scores = VADER_ANALYZER.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    else:
        pos_words = set(['good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome', 'nice', 'perfect', 'happy', 'fantastic'])
        neg_words = set(['bad', 'terrible', 'worst', 'horrible', 'poor', 'hate', 'awful', 'waste', 'slow', 'broken', 'disappointed'])
        words = set(re.findall(r'\w+', text.lower()))
        p_count = len(words.intersection(pos_words))
        n_count = len(words.intersection(neg_words))
        if p_count > n_count:
            return "Positive"
        elif n_count > p_count:
            return "Negative"
        return "Neutral"

def process_and_set_custom_df(raw_df, text_col, label_col=None, platform_col=None, dataset_name="Custom Uploaded Dataset", auto_label_missing=True):
    init_session_state()
    df = raw_df.copy()

    if text_col in df.columns:
        df['Text'] = df[text_col].astype(str).fillna("")
    else:
        raise ValueError(f"Selected text column '{text_col}' not found in dataset.")

    if label_col and label_col in df.columns:
        def map_label(val):
            if pd.isna(val) or val is None:
                return 'Neutral'
            val_str = str(val).strip()
            if val_str.lower() in ['positive', 'pos', '5', '4', 'high', 'good']:
                return 'Positive'
            elif val_str.lower() in ['negative', 'neg', '0', '-1', '2', 'low', 'bad']:
                return 'Negative'
            elif val_str.lower() in ['neutral', 'neu', '3', 'medium']:
                return 'Neutral'
            try:
                num = float(val)
                if num >= 4:
                    return 'Positive'
                elif num <= 2:
                    return 'Negative'
                else:
                    return 'Neutral'
            except ValueError:
                return val_str.capitalize() if val_str else 'Neutral'

        df['Label'] = df[label_col].apply(map_label)
    else:
        if auto_label_missing:
            df['Label'] = df['Text'].apply(predict_vader_sentiment)
        else:
            df['Label'] = 'Neutral'

    if platform_col and platform_col in df.columns:
        df['Window'] = df[platform_col].astype(str).fillna("General")
    else:
        df['Window'] = "Uploaded Data"

    df['Cleaned_Text'] = df['Text'].apply(clean_text)
    df['Cleaned_Text'] = df.apply(lambda r: r['Cleaned_Text'] if r['Cleaned_Text'].strip() != "" else r['Text'].lower(), axis=1)
    df = df[df['Text'].str.strip() != ""].reset_index(drop=True)

    st.session_state.raw_df = df
    st.session_state.cleaned_df = df
    st.session_state.is_custom_dataset = True
    st.session_state.dataset_name = dataset_name
    return df

def reset_to_default_dataset():
    init_session_state()
    st.session_state.is_custom_dataset = False
    st.session_state.dataset_name = "No Dataset Loaded"
    st.session_state.raw_df = None
    st.session_state.cleaned_df = None

def compute_kmeans_clusters(df, n_clusters=3):
    if df.empty or 'Cleaned_Text' not in df.columns:
        return df, None, None
    corpus = df['Cleaned_Text'].astype(str).tolist()
    if len(corpus) < n_clusters:
        n_clusters = max(1, len(corpus))
    
    try:
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        vec = TfidfVectorizer(max_features=1000, stop_words='english')
        X_vec = vec.fit_transform(corpus)
        if X_vec.shape[1] == 0:
            vec = TfidfVectorizer(max_features=1000)
            X_vec = vec.fit_transform(corpus)
            
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_vec)
        
        df_result = df.copy()
        df_result['Cluster'] = [f"Cluster {c+1}" for c in cluster_labels]
        
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(X_vec.toarray())
        df_result['PCA_1'] = coords[:, 0]
        df_result['PCA_2'] = coords[:, 1]
        
        return df_result, kmeans, vec
    except Exception:
        return df, None, None

def detect_anomalies(df, contamination=0.05):
    if df.empty or 'Cleaned_Text' not in df.columns:
        return df
    try:
        from sklearn.ensemble import IsolationForest
        from sklearn.feature_extraction.text import TfidfVectorizer
        from scipy.sparse import hstack
        
        df_res = df.copy()
        df_res['Char_Length'] = df_res['Text'].astype(str).str.len()
        df_res['Word_Count'] = df_res['Text'].astype(str).str.split().str.len()
        
        vec = TfidfVectorizer(max_features=100, stop_words='english')
        X_vec = vec.fit_transform(df_res['Cleaned_Text'].astype(str))
        
        features = np.column_stack([df_res['Char_Length'], df_res['Word_Count']])
        X_full = hstack([features, X_vec])
        
        iso = IsolationForest(contamination=contamination, random_state=42)
        preds = iso.fit_predict(X_full)
        scores = iso.decision_function(X_full)
        
        df_res['Anomaly_Score'] = np.round(scores, 4)
        df_res['Is_Anomaly'] = ["Anomaly ⚠️" if p == -1 else "Normal ✅" for p in preds]
        return df_res
    except Exception:
        return df

def match_similarity_vector(df, query_text, top_k=10):
    if df.empty or 'Cleaned_Text' not in df.columns or not query_text.strip():
        return pd.DataFrame()
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        corpus = df['Cleaned_Text'].astype(str).tolist()
        vec = TfidfVectorizer(max_features=2000, stop_words='english')
        X_vec = vec.fit_transform(corpus)
        
        q_clean = clean_text(query_text)
        if not q_clean.strip():
            q_clean = query_text.lower()
            
        q_vec = vec.transform([q_clean])
        sims = cosine_similarity(q_vec, X_vec).flatten()
        
        df_res = df.copy()
        df_res['Match_Score'] = np.round(sims * 100, 2)
        df_res = df_res.sort_values(by='Match_Score', ascending=False).head(top_k).reset_index(drop=True)
        return df_res
    except Exception:
        return pd.DataFrame()
