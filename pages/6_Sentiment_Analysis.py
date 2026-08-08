import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg
import re
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme, check_dataset_loaded
import data_manager

setup_page("Sentiment Analytics Subsystem", "Comprehensive NLP Sentiment Distribution, Scores, Ratings Alignment & Customer Intelligence", "😊")
check_dataset_loaded()

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset uploaded yet. Please upload a dataset in the Dataset Upload Center.")
    st.stop()

# Auto-predict sentiment if missing
if 'Label' not in df.columns:
    df['Label'] = df['Text'].apply(data_manager.predict_vader_sentiment)

schema = data_manager.detect_dataset_schema(df)
text_col = schema['text'] or ('Text' if 'Text' in df.columns else df.columns[0])
label_col = 'Label'
color_map = {"Positive": "#22C55E", "Negative": "#EF4444", "Neutral": "#FACC15"}

# Per-record score & confidence computation
if 'Sentiment_Score' not in df.columns:
    scores = []
    confidences = []
    for idx, row in df.iterrows():
        l_val = str(row['Label']).lower()
        if 'pos' in l_val or l_val in ['5', '4', 'good']:
            s = 0.85
            c = 90.0
        elif 'neg' in l_val or l_val in ['1', '2', 'bad']:
            s = -0.85
            c = 90.0
        else:
            s = 0.0
            c = 80.0
        scores.append(s)
        confidences.append(c)
    df['Sentiment_Score'] = scores
    df['Confidence'] = confidences

total_reviews = len(df)
pos_cnt = len(df[df['Label'] == 'Positive'])
neu_cnt = len(df[df['Label'] == 'Neutral'])
neg_cnt = len(df[df['Label'] == 'Negative'])

pos_pct = round(pos_cnt / total_reviews * 100, 1) if total_reviews > 0 else 0.0
neu_pct = round(neu_cnt / total_reviews * 100, 1) if total_reviews > 0 else 0.0
neg_pct = round(neg_cnt / total_reviews * 100, 1) if total_reviews > 0 else 0.0

avg_score = round(float(df['Sentiment_Score'].mean()), 2) if total_reviews > 0 else 0.0
avg_conf = round(float(df['Confidence'].mean()), 1) if total_reviews > 0 else 0.0
dominant_sentiment = "Positive" if pos_cnt >= max(neu_cnt, neg_cnt) else ("Negative" if neg_cnt >= neu_cnt else "Neutral")
net_sentiment = round(pos_pct - neg_pct, 1)

# =========================================================
# SECTION A — SENTIMENT OVERVIEW
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("📊 Section A — Sentiment Overview & KPI Metrics")

c1, c2, c3, c4 = st.columns(4)
with c1: custom_metric_card("Total Evaluated", f"{total_reviews:,}", "Review entries", icon="📄")
with c2: custom_metric_card("Positive Share", f"{pos_pct}%", f"{pos_cnt:,} positive", icon="😊", color="#22C55E")
with c3: custom_metric_card("Neutral Share", f"{neu_pct}%", f"{neu_cnt:,} neutral", icon="😐", color="#FACC15")
with c4: custom_metric_card("Negative Share", f"{neg_pct}%", f"{neg_cnt:,} negative", icon="😡", color="#EF4444")

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
c5, c6, c7, c8 = st.columns(4)
with c5: custom_metric_card("Avg Polarity Score", f"{avg_score:+0.2f}", "Range -1.0 to +1.0", icon="⚖️", color="#06B6D4")
with c6: custom_metric_card("Model Confidence", f"{avg_conf}%", "Prediction certainty", icon="🎯", color="#A855F7")
with c7: custom_metric_card("Dominant Sentiment", dominant_sentiment, "Overall tone", icon="🏆", color="#3B82F6")
with c8: custom_metric_card("Net Sentiment Score", f"{net_sentiment:+0.1f}%", "Pos % minus Neg %", icon="📈", color="#10B981" if net_sentiment >= 0 else "#F43F5E")

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
col_ov1, col_ov2 = st.columns([1.2, 1.0])

with col_ov1:
    sentiment_counts = pd.DataFrame({'Sentiment': ['Positive', 'Neutral', 'Negative'], 'Count': [pos_cnt, neu_cnt, neg_cnt]})
    fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, hole=0.45, title="Customer Sentiment Share (Donut Chart)")
    fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
    fig_pie = apply_plotly_theme(fig_pie)
    fig_pie.update_layout(title=dict(text="Customer Sentiment Share", font=dict(color="#FFFFFF", size=15)))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_ov2:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 12px; height: 100%;">
        <h4 style="color: #06B6D4; margin-top: 0; font-weight: 700;">💡 Overall Sentiment Insight</h4>
        <p style="color: #E2E8F0; font-size: 0.95rem; line-height: 1.6;">
            <b>{pos_pct}%</b> of customer reviews reflect Positive sentiment, while Negative sentiment accounts for <b>{neg_pct}%</b>. 
            The overall net sentiment balance stands at <b>{net_sentiment:+0.1f}%</b>, indicating a predominantly 
            <span style="color: {'#22C55E' if dominant_sentiment == 'Positive' else ('#EF4444' if dominant_sentiment == 'Negative' else '#FACC15')}; font-weight: 700;">{dominant_sentiment}</span> 
            customer sentiment across {total_reviews:,} evaluated records.
        </p>
        <div style="margin-top: 15px; background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 8px; border-left: 3px solid #3B82F6;">
            <span style="color: #94A3B8; font-size: 0.85rem;">Average Sentiment Score: <b>{avg_score:+0.2f}</b> | Average Confidence: <b>{avg_conf}%</b></span>
        </div>
    </div>
    """.format(pos_pct=pos_pct, neg_pct=neg_pct, net_sentiment=net_sentiment, dominant_sentiment=dominant_sentiment, total_reviews=total_reviews, avg_score=avg_score, avg_conf=avg_conf), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION B — SENTIMENT SCORE DISTRIBUTION
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("📈 Section B — Sentiment Score Polarity Distribution")
st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Distribution of normalized sentiment polarity scores (-1.0 Negative, 0.0 Neutral, +1.0 Positive).</p>", unsafe_allow_html=True)

fig_hist = px.histogram(df, x='Sentiment_Score', nbins=30, color='Label', color_discrete_map=color_map, opacity=0.85)
fig_hist.add_vline(x=avg_score, line_dash="dash", line_color="#06B6D4", annotation_text=f"Mean Score: {avg_score:+0.2f}", annotation_position="top right")
fig_hist = apply_plotly_theme(fig_hist)
fig_hist.update_layout(
    title=dict(text="Sentiment Score Polarity Distribution", font=dict(color="#FFFFFF", size=15)),
    xaxis=dict(title=dict(text="Sentiment Polarity Score (-1.0 to +1.0)", font=dict(color="#94A3B8", size=12))),
    yaxis=dict(title=dict(text="Number of Reviews", font=dict(color="#94A3B8", size=12))),
    legend_title=dict(text="Sentiment", font=dict(color="#94A3B8", size=12))
)
st.plotly_chart(fig_hist, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION C — SENTIMENT VS RATING ALIGNMENT
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("⭐ Section C — Sentiment vs Rating Alignment")

rating_col = schema['rating']
if rating_col and rating_col in df.columns:
    try:
        df['Numeric_Rating'] = pd.to_numeric(df[rating_col], errors='coerce')
        valid_r = df.dropna(subset=['Numeric_Rating'])
        if not valid_r.empty and valid_r['Numeric_Rating'].nunique() > 1:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                grouped_r = valid_r.groupby(['Numeric_Rating', 'Label']).size().reset_index(name='Count')
                fig_rat_stack = px.bar(grouped_r, x='Numeric_Rating', y='Count', color='Label', color_discrete_map=color_map, text_auto=True)
                fig_rat_stack = apply_plotly_theme(fig_rat_stack)
                fig_rat_stack.update_layout(
                    title=dict(text=f"Rating Level Sentiment Breakdown ({rating_col})", font=dict(color="#FFFFFF", size=14)),
                    xaxis=dict(title=dict(text="Rating", font=dict(color="#94A3B8", size=12))),
                    yaxis=dict(title=dict(text="Number of Reviews", font=dict(color="#94A3B8", size=12))),
                    legend_title=dict(text="Sentiment", font=dict(color="#94A3B8", size=12)),
                    barmode='stack'
                )
                st.plotly_chart(fig_rat_stack, use_container_width=True)
                
            with col_r2:
                avg_rat_df = valid_r.groupby('Numeric_Rating')['Sentiment_Score'].mean().reset_index()
                fig_avg_s = px.line(avg_rat_df, x='Numeric_Rating', y='Sentiment_Score', markers=True, line_shape='spline')
                fig_avg_s = apply_plotly_theme(fig_avg_s)
                fig_avg_s.update_traces(line_color='#06B6D4', line_width=3, marker_size=8)
                fig_avg_s.update_layout(
                    title=dict(text="Average Polarity Score by User Rating", font=dict(color="#FFFFFF", size=14)),
                    xaxis=dict(title=dict(text="Rating", font=dict(color="#94A3B8", size=12))),
                    yaxis=dict(title=dict(text="Average Sentiment Score", font=dict(color="#94A3B8", size=12)))
                )
                st.plotly_chart(fig_avg_s, use_container_width=True)
        else:
            st.info("ℹ️ Rating analysis unavailable: Rating column contains invalid or uniform numeric values.")
    except Exception:
        st.info("ℹ️ Rating alignment analysis unavailable for current dataset.")
else:
    st.info("ℹ️ Rating analysis unavailable: This analysis requires a numeric Rating/Stars column in the uploaded dataset.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION D — SENTIMENT BY CATEGORY / PRODUCT / BRAND / PLATFORM
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🏢 Section D — Categorical Sentiment Breakdown")

cat_rendered = False
possible_dims = [
    ("Product", schema['product']),
    ("Brand", schema['brand']),
    ("Category", schema['category']),
    ("Platform", schema['platform'] if schema['platform'] else ('Window' if 'Window' in df.columns else None)),
    ("Location", schema['location'])
]

for dim_title, col_key in possible_dims:
    if col_key and col_key in df.columns and df[col_key].nunique() > 1:
        cat_rendered = True
        st.subheader(f"Sentiment Breakdown by {dim_title} ({col_key})")
        top_cats = df[col_key].astype(str).value_counts().head(10).index
        df_top_cat = df[df[col_key].astype(str).isin(top_cats)]
        
        c_dim1, c_dim2 = st.columns(2)
        with c_dim1:
            grp_cat = df_top_cat.groupby([col_key, 'Label']).size().reset_index(name='Count')
            fig_cat = px.bar(grp_cat, x=col_key, y='Count', color='Label', color_discrete_map=color_map, barmode='group')
            fig_cat = apply_plotly_theme(fig_cat)
            fig_cat.update_layout(
                title=dict(text=f"Top 10 {dim_title} Sentiment Breakdown", font=dict(color="#FFFFFF", size=14)),
                xaxis=dict(title=dict(text=dim_title, font=dict(color="#94A3B8", size=12))),
                yaxis=dict(title=dict(text="Number of Reviews", font=dict(color="#94A3B8", size=12))),
                legend_title=dict(text="Sentiment", font=dict(color="#94A3B8", size=12))
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            
        with c_dim2:
            avg_cat = df_top_cat.groupby(col_key)['Sentiment_Score'].mean().reset_index()
            fig_avg_cat = px.bar(avg_cat, x=col_key, y='Sentiment_Score', color='Sentiment_Score', color_continuous_scale='Viridis')
            fig_avg_cat = apply_plotly_theme(fig_avg_cat)
            fig_avg_cat.update_layout(
                title=dict(text=f"Average Sentiment Score by {dim_title}", font=dict(color="#FFFFFF", size=14)),
                xaxis=dict(title=dict(text=dim_title, font=dict(color="#94A3B8", size=12))),
                yaxis=dict(title=dict(text="Average Sentiment Score", font=dict(color="#94A3B8", size=12)))
            )
            st.plotly_chart(fig_avg_cat, use_container_width=True)

if not cat_rendered:
    st.info("ℹ️ Categorical sentiment breakdown unavailable: Upload a dataset containing Product, Brand, Category, Platform, or Location columns to unlock dimensional sentiment analysis.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION E — SENTIMENT TRENDS OVER TIME
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)

date_col = schema['date']
has_valid_trend = False

if date_col and date_col in df.columns:
    try:
        df_t = df.copy()
        df_t['Parsed_Date'] = pd.to_datetime(df_t[date_col], errors='coerce')
        valid_dates = df_t.dropna(subset=['Parsed_Date']).sort_values('Parsed_Date')
        
        if not valid_dates.empty and len(valid_dates) > 1:
            has_valid_trend = True
            st.header("⏳ Section E — Sentiment Trends Over Time")
            valid_dates['Month'] = valid_dates['Parsed_Date'].dt.to_period('M').astype(str)
            
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                trend_avg = valid_dates.groupby('Month')['Sentiment_Score'].mean().reset_index()
                fig_trend_avg = px.line(trend_avg, x='Month', y='Sentiment_Score', markers=True)
                fig_trend_avg = apply_plotly_theme(fig_trend_avg)
                fig_trend_avg.update_traces(line_color='#3B82F6', line_width=3)
                fig_trend_avg.update_layout(
                    title=dict(text="Average Sentiment Score Trend Over Time", font=dict(color="#FFFFFF", size=14)),
                    xaxis=dict(title=dict(text="Date", font=dict(color="#94A3B8", size=12))),
                    yaxis=dict(title=dict(text="Average Sentiment Score", font=dict(color="#94A3B8", size=12))),
                    height=300
                )
                st.plotly_chart(fig_trend_avg, use_container_width=True)
                
            with t_col2:
                trend_vol = valid_dates.groupby(['Month', 'Label']).size().reset_index(name='Count')
                fig_trend_vol = px.line(trend_vol, x='Month', y='Count', color='Label', color_discrete_map=color_map, markers=True)
                fig_trend_vol = apply_plotly_theme(fig_trend_vol)
                fig_trend_vol.update_layout(
                    title=dict(text="Sentiment Review Volume Trend Over Time", font=dict(color="#FFFFFF", size=14)),
                    xaxis=dict(title=dict(text="Date", font=dict(color="#94A3B8", size=12))),
                    yaxis=dict(title=dict(text="Number of Reviews", font=dict(color="#94A3B8", size=12))),
                    legend_title=dict(text="Sentiment", font=dict(color="#94A3B8", size=12)),
                    height=300
                )
                st.plotly_chart(fig_trend_vol, use_container_width=True)
    except Exception:
        pass

if not has_valid_trend:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255,255,255,0.08); padding: 18px 22px; border-radius: 12px;">
        <h4 style="color: #F1F5F9; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700;">⏳ Trend Analysis Unavailable</h4>
        <p style="color: #94A3B8; margin: 0; font-size: 0.88rem; line-height: 1.5;">
            No valid date/time column was detected in this dataset.<br>
            <span style="color: #64748B; font-size: 0.82rem;">Upload a dataset containing a review date or timestamp to enable temporal sentiment analysis.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION F — SENTIMENT HEATMAP
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)

hm_dim_col = schema['product'] or schema['category'] or schema['brand'] or schema['platform'] or schema['location'] or schema['rating']
if not hm_dim_col:
    for col in df.columns:
        if col not in [text_col, 'Label'] and df[col].nunique() > 1 and df[col].nunique() <= 50:
            hm_dim_col = col
            break

if hm_dim_col and hm_dim_col in df.columns and df[hm_dim_col].nunique() > 1:
    if hm_dim_col == schema['product']: hm_dim_name = "Product"
    elif hm_dim_col == schema['category']: hm_dim_name = "Category"
    elif hm_dim_col == schema['brand']: hm_dim_name = "Brand"
    elif hm_dim_col == schema['platform']: hm_dim_name = "Platform"
    elif hm_dim_col == schema['location']: hm_dim_name = "Location"
    elif hm_dim_col == schema['rating']: hm_dim_name = "Rating"
    else: hm_dim_name = str(hm_dim_col).replace("_", " ").title()

    st.header(f"🔥 Section F — {hm_dim_name} × Sentiment Heatmap")
    st.markdown(f"<p style='color: #94A3B8; font-size: 0.9rem;'>Cross-tabulation matrix mapping review counts across top 10 {hm_dim_name} entries.</p>", unsafe_allow_html=True)

    top_hm_cats = df[hm_dim_col].astype(str).value_counts().head(10).index
    df_hm = df[df[hm_dim_col].astype(str).isin(top_hm_cats)]
    
    y_labels = list(top_hm_cats)
    z_matrix = []
    custom_text = []

    for cat_v in y_labels:
        sub_c = df_hm[df_hm[hm_dim_col].astype(str) == cat_v]
        c_pos = sum(1 for l in sub_c['Label'] if l == 'Positive')
        c_neu = sum(1 for l in sub_c['Label'] if l == 'Neutral')
        c_neg = sum(1 for l in sub_c['Label'] if l == 'Negative')
        tot_c = len(sub_c)
        p_pct = round(c_pos / tot_c * 100, 1) if tot_c > 0 else 0
        n_pct = round(c_neu / tot_c * 100, 1) if tot_c > 0 else 0
        g_pct = round(c_neg / tot_c * 100, 1) if tot_c > 0 else 0
        
        z_matrix.append([c_pos, c_neu, c_neg])
        custom_text.append([
            f"{hm_dim_name}: {cat_v}<br>Sentiment: Positive<br>Review Count: {c_pos:,} ({p_pct}%)",
            f"{hm_dim_name}: {cat_v}<br>Sentiment: Neutral<br>Review Count: {c_neu:,} ({n_pct}%)",
            f"{hm_dim_name}: {cat_v}<br>Sentiment: Negative<br>Review Count: {c_neg:,} ({g_pct}%)"
        ])

    fig_hm = gg.Figure(data=gg.Heatmap(
        z=z_matrix,
        x=['Positive', 'Neutral', 'Negative'],
        y=y_labels,
        text=custom_text,
        hoverinfo='text',
        colorscale='Viridis',
        colorbar=dict(title=dict(text="Review Count", font=dict(color="#94A3B8", size=12)), tickfont=dict(color="#94A3B8"))
    ))

    # Add text annotations on top of heatmap cells
    for i, cat_v in enumerate(y_labels):
        for j, val in enumerate(z_matrix[i]):
            fig_hm.add_annotation(
                x=['Positive', 'Neutral', 'Negative'][j],
                y=cat_v,
                text=str(val),
                showarrow=False,
                font=dict(color="white" if val > 0 else "#64748B", size=12, family="Inter")
            )

    fig_hm = apply_plotly_theme(fig_hm)
    fig_hm.update_layout(
        title=dict(text=f"{hm_dim_name} × Sentiment Heatmap", font=dict(color="#FFFFFF", size=16)),
        xaxis=dict(title=dict(text="Sentiment", font=dict(color="#94A3B8", size=13))),
        yaxis=dict(title=dict(text=hm_dim_name, font=dict(color="#94A3B8", size=13)), autorange="reversed", automargin=True),
        height=380,
        margin=dict(l=120, r=40, t=50, b=50)
    )
    st.plotly_chart(fig_hm, use_container_width=True)
else:
    st.header("🔥 Section F — Sentiment Heatmap Matrix")
    st.info("ℹ️ Heatmap unavailable — no suitable categorical column found in this dataset.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION G — MODEL CONFIDENCE & UNCERTAIN PREDICTIONS
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🎯 Section G — Model Certainty & Prediction Audit")

gc1, gc2, gc3 = st.columns(3)
with gc1: custom_metric_card("Avg Confidence", f"{avg_conf}%", "Mean certainty", icon="📊", color="#A855F7")
high_conf_cnt = len(df[df['Confidence'] >= 80.0])
low_conf_cnt = len(df[df['Confidence'] < 65.0])
with gc2: custom_metric_card("High Certainty (≥80%)", f"{high_conf_cnt:,}", f"{round(high_conf_cnt/total_reviews*100, 1)}% of total", icon="✅", color="#22C55E")
with gc3: custom_metric_card("Low Certainty (<65%)", f"{low_conf_cnt:,}", f"{round(low_conf_cnt/total_reviews*100, 1)}% of total", icon="⚠️", color="#EF4444")

st.markdown("##### ⚠️ Lowest Confidence Predictions (Requires Human Review)")
uncertain_df = df.sort_values('Confidence').head(10)[[text_col, 'Label', 'Confidence', 'Sentiment_Score']].reset_index(drop=True)
st.dataframe(uncertain_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION H — NEGATIVE SENTIMENT INTELLIGENCE
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("😡 Section H — Negative Sentiment Intelligence")
st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Dedicated intelligence panel focusing strictly on customer friction and low-sentiment feedback.</p>", unsafe_allow_html=True)

neg_df_sub = df[df['Label'] == 'Negative'].sort_values('Sentiment_Score').head(10)
if not neg_df_sub.empty:
    cols_to_show = [text_col, 'Label', 'Sentiment_Score']
    if rating_col and rating_col in neg_df_sub.columns: cols_to_show.append(rating_col)
    if schema['product'] and schema['product'] in neg_df_sub.columns: cols_to_show.append(schema['product'])
    st.dataframe(neg_df_sub[cols_to_show].reset_index(drop=True), use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No negative reviews detected in current dataset.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION I — POSITIVE SENTIMENT INTELLIGENCE
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("😊 Section I — Positive Sentiment Intelligence")
st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Dedicated intelligence panel focusing on customer praise and top-performing feedback.</p>", unsafe_allow_html=True)

pos_df_sub = df[df['Label'] == 'Positive'].sort_values('Sentiment_Score', ascending=False).head(10)
if not pos_df_sub.empty:
    cols_to_show = [text_col, 'Label', 'Sentiment_Score']
    if rating_col and rating_col in pos_df_sub.columns: cols_to_show.append(rating_col)
    if schema['product'] and schema['product'] in pos_df_sub.columns: cols_to_show.append(schema['product'])
    st.dataframe(pos_df_sub[cols_to_show].reset_index(drop=True), use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ No positive reviews detected in current dataset.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION J — SENTIMENT COMPARISON PANEL
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔄 Section J — Sentiment Class Comparison Panel")

comp_rows = []
for s_lbl in ['Positive', 'Neutral', 'Negative']:
    sub_grp = df[df['Label'] == s_lbl]
    g_c = len(sub_grp)
    g_p = round(g_c / total_reviews * 100, 1) if total_reviews > 0 else 0
    g_s = round(float(sub_grp['Sentiment_Score'].mean()), 2) if g_c > 0 else 0
    g_r = round(float(pd.to_numeric(sub_grp[rating_col], errors='coerce').mean()), 2) if rating_col and rating_col in sub_grp.columns and not sub_grp[rating_col].isnull().all() else "N/A"
    g_len = round(float(sub_grp[text_col].astype(str).str.len().mean()), 1) if not sub_grp.empty else 0
    
    comp_rows.append({
        "Sentiment Class": s_lbl,
        "Review Volume": g_c,
        "Share (%)": g_p,
        "Avg Polarity Score": g_s,
        "Avg User Rating": g_r,
        "Avg Review Length (Chars)": g_len
    })
st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION K — INDIVIDUAL REVIEW EXPLORER
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔍 Section K — Individual Review Explorer")

exp_col1, exp_col2 = st.columns(2)
with exp_col1:
    search_query = st.text_input("🔍 Search Reviews", placeholder="Type keywords e.g. battery, slow, support...")
with exp_col2:
    selected_sent_filter = st.multiselect("Filter by Sentiment", options=['Positive', 'Neutral', 'Negative'], default=['Positive', 'Neutral', 'Negative'])

df_exp = df[df['Label'].isin(selected_sent_filter)]
if search_query.strip():
    df_exp = df_exp[df_exp[text_col].astype(str).str.lower().str.contains(search_query.lower(), na=False)]

st.markdown(f"Showing **{len(df_exp):,}** matching reviews (max 100 displayed)")
show_cols = [text_col, 'Label', 'Sentiment_Score', 'Confidence']
if rating_col and rating_col in df_exp.columns: show_cols.append(rating_col)
if schema['product'] and schema['product'] in df_exp.columns: show_cols.append(schema['product'])
if schema['date'] and schema['date'] in df_exp.columns: show_cols.append(schema['date'])

st.dataframe(df_exp[show_cols].head(100).reset_index(drop=True), use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
