import re
import string
import io
import base64
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    
    STOPWORDS = set(stopwords.words('english'))
    LEMMATIZER = WordNetLemmatizer()
    VADER = SentimentIntensityAnalyzer()
    HAS_NLTK = True
except Exception:
    HAS_NLTK = False
    STOPWORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])
    LEMMATIZER = None
    VADER = None

def clean_text_full(text: str, remove_numbers: bool = True) -> str:
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove numbers if specified
    if remove_numbers:
        text = re.sub(r'\d+', ' ', text)
        
    # 3. Remove punctuation
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. Tokenization & Stopwords & Lemmatization
    if HAS_NLTK:
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()
    else:
        tokens = text.split()
        
    cleaned_tokens = []
    for token in tokens:
        if token not in STOPWORDS and len(token) > 1:
            if HAS_NLTK and LEMMATIZER:
                try:
                    token = LEMMATIZER.lemmatize(token)
                except Exception:
                    pass
            cleaned_tokens.append(token)
            
    return " ".join(cleaned_tokens)

def auto_detect_columns(df: pd.DataFrame):
    cols = df.columns.tolist()
    text_col = None
    label_col = None
    platform_col = None

    text_candidates = ['text', 'review', 'reviews', 'comment', 'comments', 'feedback', 'description', 'message', 'content', 'body', 'title', 'summary', 'tweet', 'tweets', 'statement', 'post', 'input']
    for col in cols:
        if col.lower() in text_candidates:
            text_col = col
            break
            
    if not text_col:
        max_len = -1
        for col in cols:
            if df[col].dtype == 'object' or str(df[col].dtype) == 'string':
                avg_l = df[col].astype(str).str.len().mean()
                if avg_l > max_len:
                    max_len = avg_l
                    text_col = col
        if not text_col and len(cols) > 0:
            text_col = cols[0]

    label_candidates = ['label', 'sentiment', 'rating', 'score', 'stars', 'category', 'target', 'class', 'polarity']
    for col in cols:
        if col != text_col and col.lower() in label_candidates:
            label_col = col
            break

    platform_candidates = ['window', 'platform', 'source', 'channel', 'device', 'app', 'store', 'company', 'location']
    for col in cols:
        if col not in [text_col, label_col] and col.lower() in platform_candidates:
            platform_col = col
            break

    return text_col, label_col, platform_col

def predict_vader_sentiment(text: str) -> str:
    if not isinstance(text, str) or not text.strip():
        return "Neutral"
    if HAS_NLTK and VADER:
        try:
            compound = VADER.polarity_scores(text)['compound']
            if compound >= 0.05:
                return "Positive"
            elif compound <= -0.05:
                return "Negative"
            else:
                return "Neutral"
        except Exception:
            pass
            
    pos_words = set(['good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome', 'nice', 'perfect', 'happy', 'fantastic'])
    neg_words = set(['bad', 'terrible', 'worst', 'horrible', 'poor', 'hate', 'awful', 'waste', 'slow', 'broken', 'disappointed'])
    words = set(re.findall(r'\w+', text.lower()))
    p_cnt = len(words.intersection(pos_words))
    n_cnt = len(words.intersection(neg_words))
    if p_cnt > n_cnt:
        return "Positive"
    elif n_cnt > p_cnt:
        return "Negative"
    return "Neutral"

def get_top_ngrams(corpus: pd.Series, n=15, ngram_range=(1,1)):
    if corpus.empty or not corpus.str.strip().any():
        return []
    try:
        vec = CountVectorizer(ngram_range=ngram_range, stop_words='english').fit(corpus)
        bag = vec.transform(corpus)
        sum_words = bag.sum(axis=0)
        words_freq = [(word, int(sum_words[0, idx])) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)[:n]
        return [{"word": w, "frequency": f} for w, f in words_freq]
    except Exception:
        return []

def generate_wordcloud_base64(text: str, colormap: str = "viridis") -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    try:
        wc = WordCloud(width=800, height=400, background_color='#111827', colormap=colormap, max_words=100).generate(text)
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#111827')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        fig.patch.set_facecolor('#111827')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#111827')
        plt.close(fig)
        buf.seek(0)
        return "data:image/png;base64," + base64.b64encode(buf.read()).decode('utf-8')
    except Exception:
        return ""
