import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme, check_dataset_loaded

setup_page("Exploratory Data Analysis (EDA)", "Automated profiling, quality, numerical, categorical & text analytics", "📊")
check_dataset_loaded()

import data_manager

df = data_manager.get_current_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset loaded.")
    st.stop()

# Helper for Semantic Type Detection
def infer_semantic_type(col_name: str, series: pd.Series) -> str:
    if col_name in ['Cleaned_Text']:
        return 'Text'
    
    clean_series = series.dropna()
    if clean_series.empty:
        return 'Categorical'
        
    c_lower = col_name.lower()
    
    # Date Detection
    if pd.api.types.is_datetime64_any_dtype(series) or any(k in c_lower for k in ['date', 'time', 'timestamp', 'created_at', 'year', 'month']):
        try:
            parsed = pd.to_datetime(clean_series.head(50), errors='coerce')
            if parsed.notnull().sum() / len(parsed) > 0.4:
                return 'Date'
        except Exception:
            pass

    # Numeric Detection
    if np.issubdtype(series.dtype, np.number):
        return 'Numeric'
    else:
        try:
            converted = pd.to_numeric(clean_series.head(100), errors='coerce')
            if converted.notnull().sum() / len(converted) > 0.6:
                return 'Numeric'
        except Exception:
            pass

    # Boolean Detection
    if series.nunique() <= 2:
        vals = set(clean_series.astype(str).str.lower().unique())
        if vals.issubset({'true', 'false', '1', '0', 'yes', 'no', 't', 'f', '1.0', '0.0'}):
            return 'Boolean'

    # Identifier Detection
    if series.nunique() == len(series) and any(k in c_lower for k in ['id', 'key', 'code', 'index', 'num', 'uuid']):
        return 'Identifier'

    # Text Detection
    avg_len = clean_series.astype(str).str.len().mean()
    if avg_len > 25 or any(k in c_lower for k in ['text', 'review', 'comment', 'feedback', 'description', 'message', 'content', 'body', 'opinion', 'tweet']):
        return 'Text'

    return 'Categorical'

semantic_types = {c: infer_semantic_type(c, df[c]) for c in df.columns}

text_cols = [c for c, t in semantic_types.items() if t == 'Text']
num_cols = [c for c, t in semantic_types.items() if t == 'Numeric']
cat_cols = [c for c, t in semantic_types.items() if t == 'Categorical']
date_cols = [c for c, t in semantic_types.items() if t == 'Date']
bool_cols = [c for c, t in semantic_types.items() if t == 'Boolean']
id_cols = [c for c, t in semantic_types.items() if t == 'Identifier']

# =========================================================
# STEP 2 — DATASET OVERVIEW
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("📋 Section A — Dataset Overview")

dataset_size_kb = round(df.memory_usage(deep=True).sum() / 1024, 1)
size_str = f"{dataset_size_kb:.1f} KB" if dataset_size_kb < 1024 else f"{dataset_size_kb/1024:.2f} MB"

col_a1, col_a2, col_a3, col_a4, col_a5, col_a6, col_a7 = st.columns(7)
with col_a1: custom_metric_card("Total Records", f"{len(df):,}", "Rows", icon="📄")
with col_a2: custom_metric_card("Total Columns", f"{df.shape[1]}", "Fields", icon="📐", color="#06B6D4")
with col_a3: custom_metric_card("Text Columns", f"{len(text_cols)}", "Text", icon="📝", color="#7C3AED")
with col_a4: custom_metric_card("Numeric Cols", f"{len(num_cols)}", "Numbers", icon="🔢", color="#FACC15")
with col_a5: custom_metric_card("Categorical", f"{len(cat_cols)+len(bool_cols)}", "Factors", icon="🏷️", color="#22C55E")
with col_a6: custom_metric_card("Date Columns", f"{len(date_cols)}", "Timestamps", icon="📅", color="#EF4444")
with col_a7: custom_metric_card("Dataset Size", size_str, "Memory", icon="💾", color="#A855F7")

st.subheader("Interactive Schema Table")
schema_rows = []
for c in df.columns:
    schema_rows.append({
        "Column Name": c,
        "Data Type": str(df[c].dtype),
        "Detected Semantic Type": semantic_types[c],
        "Non-Null Count": int(df[c].notnull().sum()),
        "Null Count": int(df[c].isnull().sum()),
        "Missing %": f"{(df[c].isnull().sum() / len(df) * 100):.1f}%",
        "Unique Values": int(df[c].nunique()),
        "Duplicate Count": int(df[c].duplicated().sum())
    })
schema_df = pd.DataFrame(schema_rows)
st.dataframe(schema_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# STEP 3 — DATA QUALITY
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🛡️ Section B — Data Quality Analytics")

dup_cnt = int(df.duplicated().sum())
dup_pct = round(dup_cnt / len(df) * 100, 1) if len(df) > 0 else 0
total_missing = df.isnull().sum().sum()

if total_missing == 0:
    st.success("✅ **Excellent — No Missing Values Detected**. All columns in your dataset are 100% complete.")
else:
    warnings = []
    for c in df.columns:
        m_pct = (df[c].isnull().sum() / len(df)) * 100
        if m_pct > 15:
            warnings.append(f"⚠️ Column **'{c}'** contains **{m_pct:.1f}%** missing values.")
    if dup_pct > 5:
        warnings.append(f"⚠️ Dataset contains **{dup_cnt} ({dup_pct}%) duplicate rows**.")
    for w in warnings:
        st.warning(w)

col_q1, col_q2 = st.columns(2)
with col_q1:
    missing_counts = df.isnull().sum().reset_index()
    missing_counts.columns = ['Column', 'Missing Count']
    fig_miss = px.bar(missing_counts, x='Column', y='Missing Count', title="Missing Values per Column", color='Missing Count', color_discrete_sequence=['#EF4444'])
    fig_miss = apply_plotly_theme(fig_miss)
    fig_miss.update_layout(xaxis_title="Column Name", yaxis_title="Missing Record Count")
    st.plotly_chart(fig_miss, use_container_width=True)

with col_q2:
    completeness = pd.DataFrame({'Column': df.columns, 'Completeness (%)': [(df[c].notnull().sum() / len(df) * 100) for c in df.columns]})
    fig_comp = px.bar(completeness, x='Column', y='Completeness (%)', title="Column Completeness Percentage", color='Completeness (%)', color_discrete_sequence=['#22C55E'])
    fig_comp = apply_plotly_theme(fig_comp)
    fig_comp.update_layout(xaxis_title="Column Name", yaxis_title="Completeness (%)")
    st.plotly_chart(fig_comp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# STEP 4 — NUMERICAL ANALYSIS
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🔢 Section C — Numerical Column Analysis")

if num_cols:
    selected_num = st.selectbox("Select Numeric Column to Analyze", options=num_cols)
    s = pd.to_numeric(df[selected_num], errors='coerce').dropna()

    q1 = float(s.quantile(0.25))
    q3 = float(s.quantile(0.75))
    iqr = float(q3 - q1)
    outliers = s[(s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)]

    col_ns1, col_ns2, col_ns3, col_ns4, col_ns5, col_ns6 = st.columns(6)
    with col_ns1: st.metric("Mean", f"{s.mean():.2f}")
    with col_ns2: st.metric("Median", f"{s.median():.2f}")
    with col_ns3: st.metric("Min / Max", f"{s.min():.1f} / {s.max():.1f}")
    with col_ns4: st.metric("Std Dev", f"{s.std():.2f}")
    with col_ns5: st.metric("IQR", f"{iqr:.2f}")
    with col_ns6: st.metric("Outliers", f"{len(outliers)}")

    col_nc1, col_nc2 = st.columns(2)
    with col_nc1:
        fig_num_hist = px.histogram(df, x=selected_num, title=f"{selected_num} Distribution Histogram", color_discrete_sequence=['#06B6D4'])
        fig_num_hist = apply_plotly_theme(fig_num_hist)
        fig_num_hist.update_layout(xaxis_title=selected_num, yaxis_title="Frequency")
        st.plotly_chart(fig_num_hist, use_container_width=True)

    with col_nc2:
        fig_num_box = px.box(df, y=selected_num, title=f"{selected_num} Box Plot", color_discrete_sequence=['#7C3AED'])
        fig_num_box = apply_plotly_theme(fig_num_box)
        fig_num_box.update_layout(yaxis_title=selected_num)
        st.plotly_chart(fig_num_box, use_container_width=True)

    if len(num_cols) > 1:
        st.subheader("Correlation Matrix Heatmap")
        corr = df[num_cols].apply(pd.to_numeric, errors='coerce').corr()
        fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='Viridis', title="Numerical Correlation Matrix")
        fig_corr = apply_plotly_theme(fig_corr)
        st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("ℹ️ Numerical analysis unavailable for this dataset. This section requires numeric columns.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# STEP 5 — CATEGORICAL ANALYSIS
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("🏷️ Section D — Categorical Column Analysis")

all_cats = cat_cols + bool_cols
if all_cats:
    selected_cat = st.selectbox("Select Categorical Column to Analyze", options=all_cats)
    s_cat = df[selected_cat].astype(str).fillna("Missing")
    cat_counts = s_cat.value_counts().reset_index()
    cat_counts.columns = [selected_cat, 'Frequency']

    col_cat1, col_cat2 = st.columns(2)
    with col_cat1:
        fig_cat = px.bar(cat_counts.head(20), x='Frequency', y=selected_cat, orientation='h', title=f"Top 20 Categories in '{selected_cat}'", color='Frequency', color_continuous_scale='Greens')
        fig_cat = apply_plotly_theme(fig_cat)
        fig_cat.update_layout(yaxis=dict(autorange="reversed", automargin=True, title=selected_cat), xaxis_title="Frequency Count", margin=dict(l=120, r=20, t=40, b=50))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_cat2:
        st.subheader(f"Cardinality for '{selected_cat}'")
        st.write(f"• **Total Unique Categories:** {df[selected_cat].nunique()}")
        st.write(f"• **Most Frequent Category:** {cat_counts.iloc[0][selected_cat]} ({cat_counts.iloc[0]['Frequency']} records)")
        st.dataframe(cat_counts.head(20), use_container_width=True, hide_index=True)
else:
    st.info("ℹ️ Categorical analysis unavailable for this dataset. This section requires categorical columns.")
st.markdown('</div>', unsafe_allow_html=True)


