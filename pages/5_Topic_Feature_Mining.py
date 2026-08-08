import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme, check_dataset_loaded

setup_page("Topic & Aspect Text Mining", "Extract deep NLP analytics, n-grams, topics, and aspects from reviews.", "🔍")
check_dataset_loaded()

import data_manager

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset loaded. Please upload a dataset in the Upload Center.")
    st.stop()

df['Cleaned_Text'] = df['Cleaned_Text'].astype(str).fillna("")
df['Text'] = df['Text'].astype(str).fillna("")
if 'Label' not in df.columns:
    df['Label'] = 'Neutral'

# Helper for N-Grams
def get_top_ngrams_df(corpus, n=20, n_gram_range=(1,1)):
    if corpus.empty or not corpus.str.strip().any():
        return pd.DataFrame(columns=['Word', 'Frequency'])
    try:
        vec = CountVectorizer(ngram_range=n_gram_range, stop_words='english').fit(corpus)
        bag = vec.transform(corpus)
        sum_words = bag.sum(axis=0)
        words_freq = [(word, int(sum_words[0, idx])) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)[:n]
        return pd.DataFrame(words_freq, columns=['Word', 'Frequency'])
    except Exception:
        return pd.DataFrame(columns=['Word', 'Frequency'])

# Helper for Word Cloud
def generate_wc_fig(text, title):
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        wc = WordCloud(width=800, height=400, background_color='#111827', colormap='viridis', max_words=100).generate(text)
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#111827')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, color='white', fontsize=16)
        fig.patch.set_facecolor('#111827')
        return fig
    except Exception:
        return None

# =========================================================
# SECTION A — Text Preprocessing Pipeline
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("⚙️ Section A — NLP Preprocessing Pipeline")
st.markdown("""
<div style="background: rgba(124, 58, 237, 0.1); border-left: 4px solid #7C3AED; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
    <h4 style="color: #A78BFA; margin: 0;">Automated Text Cleaning Pipeline</h4>
    <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 5px;">
        Raw Text ➔ Lowercasing ➔ Noise Cleaning ➔ Tokenization ➔ Stopword Removal ➔ Lemmatization ➔ Processed NLP Text
    </p>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 View Preprocessing Sample Comparison (Raw vs Cleaned Text)"):
    sample_df = df[['Text', 'Cleaned_Text']].head(10).copy()
    sample_df['Raw Word Count'] = sample_df['Text'].apply(lambda x: len(x.split()))
    sample_df['Cleaned Token Count'] = sample_df['Cleaned_Text'].apply(lambda x: len(x.split()))
    sample_df.columns = ['Original Raw Text', 'Processed Cleaned Text', 'Raw Words', 'Cleaned Tokens']
    st.dataframe(sample_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION B — Text Statistics
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("📊 Section B — Text Statistics")

df['Word_Count'] = df['Text'].str.split().str.len()
df['Char_Length'] = df['Text'].str.len()

col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
with col_b1: custom_metric_card("Total Documents", f"{len(df):,}", "Records", icon="📄")
with col_b2: custom_metric_card("Avg Words/Doc", f"{df['Word_Count'].mean():.1f}", "Words", icon="📝", color="#06B6D4")
with col_b3: custom_metric_card("Avg Chars/Doc", f"{df['Char_Length'].mean():.1f}", "Characters", icon="📏", color="#7C3AED")
with col_b4: custom_metric_card("Min Text Length", f"{df['Word_Count'].min()}", "Words", icon="📉", color="#FACC15")
with col_b5: custom_metric_card("Max Text Length", f"{df['Word_Count'].max()}", "Words", icon="📈", color="#EF4444")

col_bs1, col_bs2 = st.columns(2)
with col_bs1:
    fig_w_hist = px.histogram(df, x='Word_Count', nbins=30, title="Word Count Distribution", color_discrete_sequence=['#06B6D4'])
    fig_w_hist = apply_plotly_theme(fig_w_hist)
    fig_w_hist.update_layout(xaxis_title="Word Count per Document", yaxis_title="Number of Documents (Frequency)")
    st.plotly_chart(fig_w_hist, use_container_width=True)

with col_bs2:
    fig_l_box = px.box(df, y='Char_Length', title="Review Character Length Box Plot", color_discrete_sequence=['#7C3AED'])
    fig_l_box = apply_plotly_theme(fig_l_box)
    fig_l_box.update_layout(yaxis_title="Character Length per Document")
    st.plotly_chart(fig_l_box, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION C — Keyword Mining & Word Cloud
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔑 Section C — Keyword Mining")

# Dynamic Filters (Only show filters for columns that exist)
filter_cols = []
if 'Label' in df.columns and df['Label'].nunique() > 0: filter_cols.append('Sentiment')
schema = data_manager.detect_dataset_schema(df)
if schema['product'] and schema['product'] in df.columns: filter_cols.append('Product')
if schema['brand'] and schema['brand'] in df.columns: filter_cols.append('Brand')
if schema['category'] and schema['category'] in df.columns: filter_cols.append('Category')
if schema['platform'] and schema['platform'] in df.columns or 'Window' in df.columns: filter_cols.append('Platform')

filtered_df = df.copy()

if filter_cols:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_filter = st.selectbox("Filter Keywords By Dimension", options=["All Data"] + filter_cols)
    with col_f2:
        if selected_filter == "Sentiment":
            val = st.selectbox("Select Sentiment", options=df['Label'].unique())
            filtered_df = df[df['Label'] == val]
        elif selected_filter == "Product" and schema['product']:
            val = st.selectbox("Select Product", options=df[schema['product']].unique())
            filtered_df = df[df[schema['product']] == val]
        elif selected_filter == "Brand" and schema['brand']:
            val = st.selectbox("Select Brand", options=df[schema['brand']].unique())
            filtered_df = df[df[schema['brand']] == val]
        elif selected_filter == "Category" and schema['category']:
            val = st.selectbox("Select Category", options=df[schema['category']].unique())
            filtered_df = df[df[schema['category']] == val]
        elif selected_filter == "Platform":
            p_col = schema['platform'] if schema['platform'] else ('Window' if 'Window' in df.columns else None)
            if p_col:
                val = st.selectbox("Select Platform", options=df[p_col].unique())
                filtered_df = df[df[p_col] == val]

col_kw1, col_kw2 = st.columns([1, 1])
with col_kw1:
    num_kw = st.slider("Select Top Keywords Count", min_value=10, max_value=50, value=20)
    top_kw_df = get_top_ngrams_df(filtered_df['Cleaned_Text'], n=num_kw, n_gram_range=(1,1))
    if not top_kw_df.empty:
        fig_kw = px.bar(top_kw_df, x='Frequency', y='Word', orientation='h', title=f"Top {num_kw} Extracted Keywords", color='Frequency', color_continuous_scale='Blues')
        fig_kw = apply_plotly_theme(fig_kw)
        fig_kw.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Keyword"), xaxis_title="Occurrence Frequency", margin=dict(l=110, r=20, t=40, b=50))
        st.plotly_chart(fig_kw, use_container_width=True)
    else:
        st.info("No keywords available for selected filter.")

with col_kw2:
    st.subheader("Word Cloud Visualization")
    text_corpus = " ".join(filtered_df['Cleaned_Text'])
    wc_fig = generate_wc_fig(text_corpus, "Keyword Word Cloud")
    if wc_fig:
        st.pyplot(wc_fig)
    else:
        st.info("Insufficient text for word cloud.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION D — N-Gram Analysis
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔗 Section D — N-Gram Analysis (Keyphrase Combinations)")
st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>N-Gram analysis extracts 1-word (Unigrams), 2-word (Bigrams), and 3-word (Trigrams) phrases dynamically from your dataset.</p>", unsafe_allow_html=True)

col_ng1, col_ng2, col_ng3 = st.columns(3)
with col_ng1:
    unigram_df = get_top_ngrams_df(df['Cleaned_Text'], n=15, n_gram_range=(1,1))
    if not unigram_df.empty:
        fig_uni = px.bar(unigram_df, x='Frequency', y='Word', orientation='h', title="Top 15 Single Words (Unigrams)", color_discrete_sequence=['#06B6D4'])
        fig_uni = apply_plotly_theme(fig_uni)
        fig_uni.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Unigram Word"), xaxis_title="Occurrence Frequency", margin=dict(l=110, r=20, t=40, b=50))
        st.plotly_chart(fig_uni, use_container_width=True)
    else:
        st.info("No unigrams extracted.")

with col_ng2:
    bigram_df = get_top_ngrams_df(df['Cleaned_Text'], n=15, n_gram_range=(2,2))
    if not bigram_df.empty:
        fig_bi = px.bar(bigram_df, x='Frequency', y='Word', orientation='h', title="Top 15 Bigrams (2-Word Phrases)", color_discrete_sequence=['#7C3AED'])
        fig_bi = apply_plotly_theme(fig_bi)
        fig_bi.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Bigram Phrase"), xaxis_title="Occurrence Frequency", margin=dict(l=130, r=20, t=40, b=50))
        st.plotly_chart(fig_bi, use_container_width=True)
    else:
        st.info("No bigrams extracted.")

with col_ng3:
    trigram_df = get_top_ngrams_df(df['Cleaned_Text'], n=15, n_gram_range=(3,3))
    if not trigram_df.empty:
        fig_tri = px.bar(trigram_df, x='Frequency', y='Word', orientation='h', title="Top 15 Trigrams (3-Word Phrases)", color_discrete_sequence=['#22C55E'])
        fig_tri = apply_plotly_theme(fig_tri)
        fig_tri.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Trigram Phrase"), xaxis_title="Occurrence Frequency", margin=dict(l=140, r=20, t=40, b=50))
        st.plotly_chart(fig_tri, use_container_width=True)
    else:
        st.info("No trigrams extracted.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION E — Topic Mining (LDA Topic Modeling)
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🧠 Section E — Topic Discovery (Latent Dirichlet Allocation)")

n_topics = st.slider("Select Number of Topics to Discover", min_value=2, max_value=8, value=4)
topics = data_manager.perform_lda_topic_modeling(df, n_topics=n_topics, n_words=6)

if topics:
    col_tp1, col_tp2 = st.columns([1, 1])
    with col_tp1:
        st.subheader("Discovered Topic Clusters")
        topic_summary = []
        for t in topics:
            topic_summary.append({"Topic": t['topic_id'], "Top Keywords": t['keywords']})
        st.dataframe(pd.DataFrame(topic_summary), use_container_width=True, hide_index=True)
    
    with col_tp2:
        topic_names = [t['topic_id'] for t in topics]
        topic_word_counts = [len(t['top_words']) for t in topics]
        fig_top = px.bar(x=topic_names, y=topic_word_counts, title="Topic Feature Distribution", color=topic_names)
        fig_top = apply_plotly_theme(fig_top)
        fig_top.update_layout(xaxis_title="Topic Cluster", yaxis_title="Feature Count", showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)
else:
    st.info("Insufficient text documents for topic discovery.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION F — Aspect Mining
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🎯 Section F — Aspect & Feature Mining")

aspects = data_manager.extract_aspect_sentiments(df)
if aspects:
    aspect_df = pd.DataFrame(aspects)
    col_asp1, col_asp2 = st.columns(2)
    with col_asp1:
        fig_asp = px.bar(aspect_df, x='mentions', y='aspect', orientation='h', title="Most Frequently Discussed Aspects", color='positive_score', color_continuous_scale='Tealgrn')
        fig_asp = apply_plotly_theme(fig_asp)
        fig_asp.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Product/Service Aspect"), xaxis_title="Total Mentions Count", margin=dict(l=130, r=20, t=40, b=50))
        st.plotly_chart(fig_asp, use_container_width=True)
        
    with col_asp2:
        fig_asp_sent = px.bar(aspect_df, x='aspect', y=['positive_count', 'neutral_count', 'negative_count'], title="Aspect Sentiment Breakdown", barmode='stack', color_discrete_map={'positive_count': '#22C55E', 'neutral_count': '#FACC15', 'negative_count': '#EF4444'})
        fig_asp_sent = apply_plotly_theme(fig_asp_sent)
        fig_asp_sent.update_layout(xaxis_title="Aspect", yaxis_title="Review Count")
        st.plotly_chart(fig_asp_sent, use_container_width=True)

    st.subheader("Aspect Contribution Table")
    st.dataframe(aspect_df, use_container_width=True, hide_index=True)
else:
    st.info("Aspect extraction unavailable for current dataset.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION G — Complaint & Praise Mining
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🚨 Section G — Complaint & Praise Keyphrase Mining")

col_cmp1, col_cmp2 = st.columns(2)
with col_cmp1:
    st.subheader("👍 Top Praise & Positive Keyphrases")
    pos_df = df[df['Label'] == 'Positive'] if 'Label' in df.columns else df
    pos_kw_df = get_top_ngrams_df(pos_df['Cleaned_Text'], n=15, n_gram_range=(1,2))
    if not pos_kw_df.empty:
        fig_pos = px.bar(pos_kw_df, x='Frequency', y='Word', orientation='h', title="Top Positive Keyphrases", color_discrete_sequence=['#22C55E'])
        fig_pos = apply_plotly_theme(fig_pos)
        fig_pos.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Positive Phrase"), xaxis_title="Frequency", margin=dict(l=130, r=20, t=40, b=50))
        st.plotly_chart(fig_pos, use_container_width=True)
    else:
        st.info("No positive phrases extracted.")

with col_cmp2:
    st.subheader("👎 Top Complaint & Friction Categories")
    complaints = data_manager.extract_complaint_categories(df)
    if complaints:
        complaint_df = pd.DataFrame(complaints)
        fig_cmp = px.bar(complaint_df, x='count', y='category', orientation='h', title="Top Pain Points", color='count', color_continuous_scale='Reds')
        fig_cmp = apply_plotly_theme(fig_cmp)
        fig_cmp.update_layout(yaxis=dict(autorange="reversed", automargin=True, title="Complaint Category"), xaxis_title="Complaint Count", margin=dict(l=130, r=20, t=40, b=50))
        st.plotly_chart(fig_cmp, use_container_width=True)
    else:
        st.info("No complaint themes detected in current dataset.")
st.markdown('</div>', unsafe_allow_html=True)
