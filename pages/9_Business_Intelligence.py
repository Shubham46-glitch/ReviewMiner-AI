import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import time
from fpdf import FPDF
import base64
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme

setup_page("Business Intelligence Dashboard", "Transform customer reviews into actionable business insights.", "📈")

import data_manager

df = data_manager.get_cleaned_df()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()
df['Cleaned_Text'] = df['Cleaned_Text'].astype(str).fillna("")
if 'Label' not in df.columns: df['Label'] = 'Neutral'
if 'Window' not in df.columns: df['Window'] = 'Unknown'
if 'Text' not in df.columns: df['Text'] = df.get('Cleaned_Text', '')

st.sidebar.header("🎛️ Executive Filters")
platforms = df['Window'].dropna().unique().tolist()
selected_platforms = st.sidebar.multiselect("Select Platform", options=platforms, default=platforms)

sentiments = df['Label'].dropna().unique().tolist()
selected_sentiments = st.sidebar.multiselect("Select Sentiment", options=sentiments, default=sentiments)

search_keyword = st.sidebar.text_input("Search Specific Keyword", "")
max_val = max(1, len(df))
min_val = min(10, max_val)
review_count = st.sidebar.slider("Number of Reviews to Display (Table)", min_value=min_val, max_value=max_val, value=min(100, max_val))

filtered_df = df[df['Window'].isin(selected_platforms) & df['Label'].isin(selected_sentiments)]
if search_keyword:
    filtered_df = filtered_df[filtered_df['Text'].astype(str).str.contains(search_keyword, case=False, na=False)]

if filtered_df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

total_reviews = len(filtered_df)
pos_count = len(filtered_df[filtered_df['Label'] == 'Positive'])
neu_count = len(filtered_df[filtered_df['Label'] == 'Neutral'])
neg_count = len(filtered_df[filtered_df['Label'] == 'Negative'])

pos_pct = (pos_count / total_reviews) * 100 if total_reviews > 0 else 0
neu_pct = (neu_count / total_reviews) * 100 if total_reviews > 0 else 0
neg_pct = (neg_count / total_reviews) * 100 if total_reviews > 0 else 0
overall_score = ((pos_count * 1) + (neu_count * 0.5) + (neg_count * 0)) / total_reviews * 100 if total_reviews > 0 else 0

st.header("Executive Summary")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    custom_metric_card("Total", f"{total_reviews:,}", "Reviews", icon="📄")
with col2:
    custom_metric_card("Satisfaction", f"{pos_pct:.1f}%", "Happy customers", icon="😊", color="#22C55E")
with col3:
    custom_metric_card("Negative", f"{neg_pct:.1f}%", "Dissatisfied", icon="😡", color="#EF4444")
with col4:
    custom_metric_card("Neutral", f"{neu_pct:.1f}%", "Indifferent", icon="😐", color="#FACC15")
with col5:
    custom_metric_card("Sentiment Score", f"{overall_score:.1f}", "/ 100 Total", icon="⭐", color="#06B6D4")

st.divider()

st.header("Sentiment Distribution & Satisfaction")
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
color_map = {"Positive": "#22C55E", "Neutral": "#FACC15", "Negative": "#EF4444"}
sentiment_counts = filtered_df['Label'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']

with col_s1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pos_pct,
        number = {'suffix': "%"},
        title={'text': "Satisfaction"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#22C55E"}, 'bgcolor': "rgba(255,255,255,0.05)"}
    ))
    fig_gauge = apply_plotly_theme(fig_gauge)
    fig_gauge.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, title="Pie Chart")
    fig_pie = apply_plotly_theme(fig_pie)
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250, showlegend=False)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment', color_discrete_map=color_map, text_auto=True, title="Bar Chart")
    fig_bar = apply_plotly_theme(fig_bar)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
        
with col_s4:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    fig_donut = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, hole=0.6, title="Donut Chart")
    fig_donut = apply_plotly_theme(fig_donut)
    fig_donut.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250, showlegend=False)
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.header("🏢 Platform Performance Analysis")
platform_stats = []
for p in filtered_df['Window'].unique():
    p_df = filtered_df[filtered_df['Window'] == p]
    p_total = len(p_df)
    p_pos = len(p_df[p_df['Label'] == 'Positive'])
    p_neg = len(p_df[p_df['Label'] == 'Negative'])
    platform_stats.append({
        "Platform": p, "Total Reviews": p_total,
        "Positive %": (p_pos/p_total*100) if p_total > 0 else 0,
        "Negative %": (p_neg/p_total*100) if p_total > 0 else 0
    })

p_stats_df = pd.DataFrame(platform_stats)
if not p_stats_df.empty:
    best_platform = p_stats_df.loc[p_stats_df['Positive %'].idxmax()]['Platform']
    worst_platform = p_stats_df.loc[p_stats_df['Negative %'].idxmax()]['Platform']
    col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
    with col_p1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        fig_plat = px.bar(p_stats_df, x='Platform', y=['Positive %', 'Negative %'], barmode='group', 
                          color_discrete_sequence=["#22C55E", "#EF4444"], title="Sentiment Breakdown by Platform")
        fig_plat = apply_plotly_theme(fig_plat)
        st.plotly_chart(fig_plat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_p2:
        custom_metric_card("Best Platform", best_platform, "Highest Positivity", icon="🏆", color="#22C55E")
    with col_p3:
        custom_metric_card("Needs Improvement", worst_platform, "Highest Negativity", icon="⚠️", color="#EF4444")

st.divider()

def get_top_words(corpus, n=20):
    if not corpus.empty and corpus.str.strip().any():
        try:
            vec = CountVectorizer(stop_words='english').fit(corpus)
            bag = vec.transform(corpus)
            sum_words = bag.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
            return pd.DataFrame(sorted(words_freq, key=lambda x: x[1], reverse=True)[:n], columns=['Word', 'Freq'])
        except ValueError:
            try:
                vec = CountVectorizer().fit(corpus)
                bag = vec.transform(corpus)
                sum_words = bag.sum(axis=0)
                words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
                return pd.DataFrame(sorted(words_freq, key=lambda x: x[1], reverse=True)[:n], columns=['Word', 'Freq'])
            except Exception:
                return pd.DataFrame(columns=['Word', 'Freq'])
        except Exception:
            return pd.DataFrame(columns=['Word', 'Freq'])
    return pd.DataFrame(columns=['Word', 'Freq'])

st.header("🔑 Keyword Intelligence")
pos_corpus = filtered_df[filtered_df['Label'] == 'Positive']['Cleaned_Text']
neg_corpus = filtered_df[filtered_df['Label'] == 'Negative']['Cleaned_Text']
top_pos = get_top_words(pos_corpus, 20)
top_neg = get_top_words(neg_corpus, 20)

col_k1, col_k2 = st.columns(2)
with col_k1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Top 20 Positive Keywords (Most Appreciated)")
    if not top_pos.empty:
        fig_pos_kw = px.bar(top_pos.sort_values('Freq'), x='Freq', y='Word', orientation='h', color='Freq', color_continuous_scale='Greens')
        fig_pos_kw = apply_plotly_theme(fig_pos_kw)
        fig_pos_kw.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
        st.plotly_chart(fig_pos_kw, use_container_width=True)
    else:
        st.info("No positive keywords found.")
    st.markdown('</div>', unsafe_allow_html=True)
with col_k2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Top 20 Negative Keywords (Top Complaints)")
    if not top_neg.empty:
        fig_neg_kw = px.bar(top_neg.sort_values('Freq'), x='Freq', y='Word', orientation='h', color='Freq', color_continuous_scale='Reds')
        fig_neg_kw = apply_plotly_theme(fig_neg_kw)
        fig_neg_kw.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
        st.plotly_chart(fig_neg_kw, use_container_width=True)
    else:
        st.info("No negative keywords found.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.header("☁️ Visual Sentiment Landscapes")
col_w1, col_w2, col_w3 = st.columns(3)
def generate_wc(text, colormap):
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        wc = WordCloud(width=400, height=300, background_color='#111827', colormap=colormap).generate(text)
        fig, ax = plt.subplots(facecolor='#111827')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        fig.patch.set_facecolor('#111827')
        return fig
    except Exception:
        return None

with col_w1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Overall Word Cloud")
    all_text = " ".join(filtered_df['Cleaned_Text'])
    fig_wc1 = generate_wc(all_text, 'viridis')
    if fig_wc1: st.pyplot(fig_wc1)
    else: st.info("No text data for word cloud.")
    st.markdown('</div>', unsafe_allow_html=True)
with col_w2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Positive Word Cloud")
    pos_t = " ".join(pos_corpus)
    fig_wc2 = generate_wc(pos_t, 'Greens')
    if fig_wc2: st.pyplot(fig_wc2)
    else: st.info("No positive text for word cloud.")
    st.markdown('</div>', unsafe_allow_html=True)
with col_w3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.subheader("Negative Word Cloud")
    neg_t = " ".join(neg_corpus)
    fig_wc3 = generate_wc(neg_t, 'Reds')
    if fig_wc3: st.pyplot(fig_wc3)
    else: st.info("No negative text for word cloud.")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.header("🤖 AI Business Insights & Recommendations")
recommendations = []
neg_words = top_neg['Word'].tolist() if not top_neg.empty else []
pos_words = top_pos['Word'].tolist() if not top_pos.empty else []

if any(w in neg_words for w in ['late', 'delay', 'delivery', 'time', 'slow']):
    recommendations.append("🚚 Reduce delivery delays and optimize supply chain logistics.")
if any(w in neg_words for w in ['broken', 'damage', 'quality', 'bad', 'poor', 'worst', 'cheap']):
    recommendations.append("📦 Improve packaging quality and perform stricter QA.")
if any(w in neg_words for w in ['rude', 'service', 'support', 'staff', 'unhelpful', 'email']):
    recommendations.append("📞 Increase customer support response time and implement staff training.")
if any(w in neg_words for w in ['price', 'expensive', 'cost', 'money', 'worth']):
    recommendations.append("💰 Review pricing strategy or offer promotional discounts.")
if not recommendations:
    recommendations.append("🌟 Maintain current operational standards and focus on highly appreciated features.")

col_rec1, col_rec2 = st.columns(2)
with col_rec1:
    st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
    st.subheader("Data-Driven Insights")
    st.markdown(f"""
    - **Satisfaction Rate:** <span style="color:#22C55E">{pos_pct:.1f}%</span>
    - **Dissatisfaction Rate:** <span style="color:#EF4444">{neg_pct:.1f}%</span>
    - **Most Loved Features:** {', '.join(pos_words[:5]) if pos_words else 'N/A'}
    - **Improvement Areas:** {', '.join(neg_words[:5]) if neg_words else 'N/A'}
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_rec2:
    st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
    st.subheader("Strategic Recommendations")
    for rec in recommendations:
        st.markdown(f'<div style="background: rgba(124, 58, 237, 0.1); border-left: 4px solid #7C3AED; padding: 15px; border-radius: 8px; margin-bottom: 10px;">{rec}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.header("📄 Export Executive Report")
col_ex1, col_ex2 = st.columns(2)
with col_ex1:
    st.markdown('<div class="premium-card" style="text-align: center;">', unsafe_allow_html=True)
    csv_export = filtered_df.head(review_count).to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data (CSV)", data=csv_export, file_name='filtered_reviews.csv', mime='text/csv', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with col_ex2:
    st.markdown('<div class="premium-card" style="text-align: center;">', unsafe_allow_html=True)
    class PDFReport(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Executive Business Intelligence Report', 0, 1, 'C')
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    try:
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "1. Dataset Summary", ln=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Total Reviews Analyzed: {total_reviews}", ln=1)
        pdf.cell(0, 10, f"Overall Sentiment Score: {overall_score:.1f}/100", ln=1)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Customer Satisfaction", ln=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Positive Reviews: {pos_pct:.1f}%", ln=1)
        pdf.cell(0, 10, f"Negative Reviews: {neg_pct:.1f}%", ln=1)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Business Insights", ln=1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Most Appreciated Features: {', '.join(pos_words[:5]) if pos_words else 'N/A'}", ln=1)
        pdf.cell(0, 10, f"Top Customer Complaints: {', '.join(neg_words[:5]) if neg_words else 'N/A'}", ln=1)
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "4. Strategic Recommendations", ln=1)
        pdf.set_font("Arial", size=12)
        for r in recommendations:
            clean_r = r.encode('ascii', 'ignore').decode('ascii').strip()
            pdf.multi_cell(0, 10, f"- {clean_r}")
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📑 Download Executive Report (PDF)", data=pdf_bytes, file_name='executive_report.pdf', mime='application/pdf', use_container_width=True)
    except Exception as e:
        st.warning("PDF Generation requires 'fpdf'.")
    st.markdown('</div>', unsafe_allow_html=True)
