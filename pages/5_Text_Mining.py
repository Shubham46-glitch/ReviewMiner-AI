import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from ui_utils import setup_page, apply_plotly_theme

setup_page("Text Mining Dashboard", "Extract deep text analytics, themes, and keywords from reviews.", "☁️")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("product_reviews_cleaned.csv")
    except FileNotFoundError:
        st.error("product_reviews_cleaned.csv not found! Please run the preprocessing script first.")
        st.stop()

df = load_data()
df['Cleaned_Text'] = df['Cleaned_Text'].astype(str).fillna("")

# Utility to generate word clouds
def plot_wordcloud(text, title):
    wc = WordCloud(width=800, height=400, background_color='#111827', colormap='viridis', max_words=100).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#111827')
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, color='white', fontsize=18)
    fig.patch.set_facecolor('#111827')
    return fig

# Utility to get top n-grams
def get_top_n_words(corpus, n=20, n_gram_range=(1,1)):
    if not corpus.empty and corpus.str.strip().any():
        vec = CountVectorizer(ngram_range=n_gram_range, stop_words='english').fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
        return pd.DataFrame(words_freq[:n], columns=['Word', 'Frequency'])
    return pd.DataFrame(columns=['Word', 'Frequency'])

st.divider()

# --- 1 to 4: Word Clouds ---
st.header("☁️ Word Cloud Analysis")

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.subheader("1. Overall Word Cloud")
all_text = " ".join(df['Cleaned_Text'])
st.pyplot(plot_wordcloud(all_text, "All Reviews Word Cloud"))
st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("2. Positive Reviews")
    pos_text = " ".join(df[df['Label'] == 'Positive']['Cleaned_Text'])
    if pos_text: st.pyplot(plot_wordcloud(pos_text, "Positive Word Cloud"))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("3. Negative Reviews")
    neg_text = " ".join(df[df['Label'] == 'Negative']['Cleaned_Text'])
    if neg_text: st.pyplot(plot_wordcloud(neg_text, "Negative Word Cloud"))
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("4. Neutral Reviews")
    neu_text = " ".join(df[df['Label'] == 'Neutral']['Cleaned_Text'])
    if neu_text: st.pyplot(plot_wordcloud(neu_text, "Neutral Word Cloud"))
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 5 to 7: Frequent Words Analysis ---
st.header("📊 Frequent Words Analysis")

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.subheader("5. Top 20 Most Frequent Words (Overall)")
top_overall = get_top_n_words(df['Cleaned_Text'], 20)
fig1 = px.bar(top_overall, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Blues')
fig1.update_layout(yaxis={'categoryorder':'total ascending'})
fig1 = apply_plotly_theme(fig1)
st.plotly_chart(fig1, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("6. Top 20 Positive Words")
    top_pos = get_top_n_words(df[df['Label'] == 'Positive']['Cleaned_Text'], 20)
    fig2 = px.bar(top_pos, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Greens')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    fig2 = apply_plotly_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("7. Top 20 Negative Words")
    top_neg = get_top_n_words(df[df['Label'] == 'Negative']['Cleaned_Text'], 20)
    fig3 = px.bar(top_neg, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Reds')
    fig3.update_layout(yaxis={'categoryorder':'total ascending'})
    fig3 = apply_plotly_theme(fig3)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 8 and 9: N-Gram Analysis ---
st.header("🔗 N-Gram Analysis")
st.markdown("<p style='color: #94A3B8;'>Understanding which words appear together provides context that single words lack.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("8. Top 15 Bigrams")
    top_bigrams = get_top_n_words(df['Cleaned_Text'], 15, (2,2))
    fig4 = px.bar(top_bigrams, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Purples')
    fig4.update_layout(yaxis={'categoryorder':'total ascending'})
    fig4 = apply_plotly_theme(fig4)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("9. Top 15 Trigrams")
    top_trigrams = get_top_n_words(df['Cleaned_Text'], 15, (3,3))
    fig5 = px.bar(top_trigrams, x='Frequency', y='Word', orientation='h', color='Frequency', color_continuous_scale='Oranges')
    fig5.update_layout(yaxis={'categoryorder':'total ascending'})
    fig5 = apply_plotly_theme(fig5)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 10: TF-IDF Keyword Extraction ---
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔑 10. Keyword Extraction (TF-IDF)")
st.markdown("<p style='color: #94A3B8;'>TF-IDF extracts keywords that are highly unique and significant to the dataset, balancing out extremely common words.</p>", unsafe_allow_html=True)

tfidf_vec = TfidfVectorizer(max_features=20, stop_words='english')
tfidf_matrix = tfidf_vec.fit_transform(df['Cleaned_Text'])
avg_tfidf = tfidf_matrix.mean(axis=0).A1
tfidf_df = pd.DataFrame({'Keyword': tfidf_vec.get_feature_names_out(), 'TF-IDF Score': avg_tfidf})
tfidf_df = tfidf_df.sort_values(by='TF-IDF Score', ascending=False)

fig6 = px.bar(tfidf_df, x='TF-IDF Score', y='Keyword', orientation='h', color='TF-IDF Score', color_continuous_scale='Plasma')
fig6.update_layout(yaxis={'categoryorder':'total ascending'})
fig6 = apply_plotly_theme(fig6)
st.plotly_chart(fig6, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
