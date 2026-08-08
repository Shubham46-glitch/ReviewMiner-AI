from fastapi import APIRouter, HTTPException, Response
import backend.app.routers.dataset_router as dataset_router
from backend.app.services.text_engine import auto_detect_columns, get_cleaned_text_series, get_top_ngrams, generate_wordcloud_base64, perform_lda_topic_modeling, extract_aspect_sentiments, extract_emotion_distribution, extract_complaint_analytics, compute_full_sentiment_analytics, compute_executive_business_intelligence
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from fpdf import FPDF
import pandas as pd
import numpy as np

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

def get_active_df():
    if not dataset_router.ACTIVE_DATASET_ID or dataset_router.ACTIVE_DATASET_ID not in dataset_router.STORED_DATASETS:
        dataset_router.ensure_default_dataset()
    if dataset_router.ACTIVE_DATASET_ID and dataset_router.ACTIVE_DATASET_ID in dataset_router.STORED_DATASETS:
        return dataset_router.STORED_DATASETS[dataset_router.ACTIVE_DATASET_ID]["processed_df"]
    return None

def infer_semantic_type(col_name: str, series: pd.Series) -> str:
    if col_name in ['Cleaned_Text']:
        return 'Text'
    
    clean_series = series.dropna()
    if clean_series.empty:
        return 'Categorical'
        
    c_lower = col_name.lower()
    
    # 1. Date Detection
    if pd.api.types.is_datetime64_any_dtype(series) or any(k in c_lower for k in ['date', 'time', 'timestamp', 'created_at', 'year', 'month']):
        try:
            parsed = pd.to_datetime(clean_series.head(50), errors='coerce')
            if parsed.notnull().sum() / len(parsed) > 0.4:
                return 'Date'
        except Exception:
            pass

    # 2. Numeric Detection (safe for all pandas dtypes)
    if pd.api.types.is_numeric_dtype(series):
        return 'Numeric'
    else:
        try:
            converted = pd.to_numeric(clean_series.head(100), errors='coerce')
            if converted.notnull().sum() / len(converted) > 0.6:
                return 'Numeric'
        except Exception:
            pass


    # 3. Boolean Detection
    if series.nunique() <= 2:
        vals = set(clean_series.astype(str).str.lower().unique())
        if vals.issubset({'true', 'false', '1', '0', 'yes', 'no', 't', 'f', '1.0', '0.0'}):
            return 'Boolean'

    # 4. Identifier Detection
    if series.nunique() == len(series) and any(k in c_lower for k in ['id', 'key', 'code', 'index', 'num', 'uuid']):
        return 'Identifier'

    # 5. Text Detection (Long text / review content)
    avg_len = clean_series.astype(str).str.len().mean()
    if avg_len > 25 or any(k in c_lower for k in ['text', 'review', 'comment', 'feedback', 'description', 'message', 'content', 'body', 'opinion', 'tweet']):
        return 'Text'

    return 'Categorical'

@router.get("/preprocessing")
async def get_preprocessing_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
    
    orig_col = "Text" if "Text" in pdf.columns else pdf.columns[0]
    clean_col = "Cleaned_Text" if "Cleaned_Text" in pdf.columns else orig_col
    
    orig_words = int(pdf[orig_col].astype(str).str.split().str.len().sum())
    clean_tokens = int(pdf[clean_col].astype(str).str.split().str.len().sum())
    
    preview = pdf[[orig_col, clean_col]].head(20).to_dict(orient="records")
    return {
        "original_total_words": orig_words,
        "cleaned_total_tokens": clean_tokens,
        "reduction_pct": round((1 - clean_tokens / orig_words) * 100, 1) if orig_words > 0 else 0,
        "comparison_preview": preview
    }

@router.get("/eda")
async def get_eda_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    semantic_types = {}
    for c in pdf.columns:
        semantic_types[c] = infer_semantic_type(c, pdf[c])

    text_cols = [c for c, t in semantic_types.items() if t == 'Text']
    num_cols = [c for c, t in semantic_types.items() if t == 'Numeric']
    cat_cols = [c for c, t in semantic_types.items() if t == 'Categorical']
    date_cols = [c for c, t in semantic_types.items() if t == 'Date']
    bool_cols = [c for c, t in semantic_types.items() if t == 'Boolean']
    id_cols = [c for c, t in semantic_types.items() if t == 'Identifier']

    mem_bytes = int(pdf.memory_usage(deep=True).sum())
    size_str = f"{round(mem_bytes/1024, 1)} KB" if mem_bytes < 1024*1024 else f"{round(mem_bytes/(1024*1024), 2)} MB"

    schema_table = []
    for c in pdf.columns:
        schema_table.append({
            "column": c,
            "type": str(pdf[c].dtype),
            "semantic_type": semantic_types[c],
            "non_null": int(pdf[c].notnull().sum()),
            "null_count": int(pdf[c].isnull().sum()),
            "missing_pct": round(float(pdf[c].isnull().sum() / len(pdf) * 100), 1),
            "unique_values": int(pdf[c].nunique()),
            "duplicate_count": int(pdf[c].duplicated().sum())
        })

    dup_cnt = int(pdf.duplicated().sum())
    dup_pct = round(dup_cnt / len(pdf) * 100, 1) if len(pdf) > 0 else 0
    missing_by_col = []
    total_missing_sum = 0
    constant_cols = []
    potential_ids = []

    for c in pdf.columns:
        m_cnt = int(pdf[c].isnull().sum())
        total_missing_sum += m_cnt
        m_pct = round(float(m_cnt / len(pdf) * 100), 1)
        nu = int(pdf[c].nunique())
        is_const = (nu <= 1)
        is_id = (nu == len(pdf))
        if is_const: constant_cols.append(c)
        if is_id: potential_ids.append(c)
        
        missing_by_col.append({
            "column": c,
            "missing_count": m_cnt,
            "missing_pct": m_pct,
            "completeness": round(100.0 - m_pct, 1),
            "unique_values": nu,
            "is_constant": is_const,
            "is_potential_id": is_id
        })

    warnings = []
    for c in pdf.columns:
        m_pct = (pdf[c].isnull().sum() / len(pdf)) * 100
        if m_pct > 15:
            warnings.append(f"Column '{c}' contains {m_pct:.1f}% missing values.")
    if dup_pct > 5:
        warnings.append(f"Dataset contains {dup_cnt} ({dup_pct}%) duplicate records.")

    # Numerical Analysis
    num_analysis = {}
    for c in pdf.columns:
        if pdf[c].dtype == 'bool' or c in ["Cleaned_Text"]:
            continue
        if pd.api.types.is_numeric_dtype(pdf[c]):
            try:
                s = pd.to_numeric(pdf[c], errors='coerce').dropna().astype(float)
                if not s.empty and len(s) > 0:
                    q1 = float(np.percentile(s, 25))
                    q3 = float(np.percentile(s, 75))
                    iqr = float(q3 - q1)
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    outliers = s[(s < lower_bound) | (s > upper_bound)]
                    
                    num_analysis[c] = {
                        "count": len(s),
                        "mean": round(float(s.mean()), 2),
                        "median": round(float(s.median()), 2),
                        "std": round(float(s.std()), 2) if len(s) > 1 else 0.0,
                        "min": round(float(s.min()), 2),
                        "max": round(float(s.max()), 2),
                        "q1": round(q1, 2),
                        "q3": round(q3, 2),
                        "iqr": round(iqr, 2),
                        "outlier_count": len(outliers),
                        "values": [float(x) for x in s.tolist()[:500]]
                    }
            except Exception:
                continue


    # Correlation Matrix
    corr_matrix = {}
    valid_num_cols = list(num_analysis.keys())
    if len(valid_num_cols) > 1:
        try:
            num_df = pdf[valid_num_cols].apply(pd.to_numeric, errors='coerce')
            corr = num_df.corr().fillna(0).to_dict()
            corr_matrix = {c1: {c2: round(float(v), 2) for c2, v in row.items()} for c1, row in corr.items()}
        except Exception:
            corr_matrix = {}

    # Categorical Analysis (Include all factor/categorical/boolean/short columns except text)
    primary_text_col = text_cols[0] if text_cols else pdf.columns[0]
    cat_candidates = set(cat_cols + bool_cols + id_cols)
    for c in pdf.columns:
        if c != primary_text_col and c != "Cleaned_Text" and (pdf[c].dtype == 'object' or str(pdf[c].dtype) == 'string' or pdf[c].nunique() <= 50):
            cat_candidates.add(c)

    cat_analysis = {}
    for c in sorted(list(cat_candidates)):
        if c in ["Cleaned_Text", primary_text_col] and pdf[c].nunique() > 100:
            continue
        s = pdf[c].astype(str).fillna("Missing")
        counts = s.value_counts()
        cardinality = len(counts)
        mode_val = str(counts.index[0]) if not counts.empty else "N/A"
        mode_cnt = int(counts.iloc[0]) if not counts.empty else 0
        
        freq_list = []
        top_counts = counts.head(20)
        other_cnt = counts.iloc[20:].sum() if cardinality > 20 else 0
        
        for k, v in top_counts.items():
            freq_list.append({
                "category": str(k),
                "count": int(v),
                "percentage": round(float(v / len(s) * 100), 1)
            })
        if other_cnt > 0:
            freq_list.append({
                "category": "Other",
                "count": int(other_cnt),
                "percentage": round(float(other_cnt / len(s) * 100), 1)
            })
            
        cat_analysis[c] = {
            "cardinality": cardinality,
            "most_frequent_value": mode_val,
            "most_frequent_count": mode_cnt,
            "frequencies": freq_list
        }


    return {
        "overview": {
            "total_records": len(pdf),
            "total_columns": pdf.shape[1],
            "text_columns_count": len(text_cols),
            "numeric_columns_count": len(num_cols),
            "categorical_columns_count": len(cat_cols) + len(bool_cols),
            "date_columns_count": len(date_cols),
            "boolean_columns_count": len(bool_cols),
            "identifier_columns_count": len(id_cols),
            "dataset_size": size_str
        },
        "schema_table": schema_table,
        "data_quality": {
            "has_missing_values": total_missing_sum > 0,
            "zero_missing_message": "Excellent — No Missing Values Detected" if total_missing_sum == 0 else "",
            "duplicate_count": dup_cnt,
            "duplicate_pct": dup_pct,
            "missing_by_column": missing_by_col,
            "constant_columns": constant_cols,
            "potential_id_columns": potential_ids,
            "warnings": warnings
        },
        "numerical_analysis": num_analysis,
        "correlation_matrix": corr_matrix,
        "categorical_analysis": cat_analysis
    }

@router.get("/sentiment")
async def get_sentiment_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    return compute_full_sentiment_analytics(pdf)

@router.get("/wordclouds")
async def get_wordcloud_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    clean_col = "Cleaned_Text" if "Cleaned_Text" in pdf.columns else pdf.columns[0]
    lbl_col = "Label" if "Label" in pdf.columns else None
    
    all_text = " ".join(pdf[clean_col].astype(str))
    pos_text = " ".join(pdf[pdf[lbl_col] == "Positive"][clean_col].astype(str)) if lbl_col else all_text
    neg_text = " ".join(pdf[pdf[lbl_col] == "Negative"][clean_col].astype(str)) if lbl_col else all_text
    
    wc_overall = generate_wordcloud_base64(all_text, "viridis")
    wc_positive = generate_wordcloud_base64(pos_text, "Greens")
    wc_negative = generate_wordcloud_base64(neg_text, "Reds")
    
    top_terms = get_top_ngrams(pdf[clean_col], n=20, ngram_range=(1,1))
    
    return {
        "wordcloud_overall": wc_overall,
        "wordcloud_positive": wc_positive,
        "wordcloud_negative": wc_negative,
        "top_keywords": top_terms
    }

@router.get("/business-intelligence")
async def get_bi_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
    return compute_executive_business_intelligence(pdf)

@router.get("/topics")
async def get_lda_topics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    text_col, label_col, _ = auto_detect_columns(pdf)
    cleaned_series = get_cleaned_text_series(pdf)
    raw_text_series = pdf[text_col].astype(str) if text_col and text_col in pdf.columns else cleaned_series
    
    lengths = raw_text_series.str.len().tolist()
    word_counts = raw_text_series.str.split().str.len().tolist()
    
    top_unigrams = get_top_ngrams(cleaned_series, n=15, ngram_range=(1,1))
    top_bigrams = get_top_ngrams(cleaned_series, n=15, ngram_range=(2,2))
    top_trigrams = get_top_ngrams(cleaned_series, n=15, ngram_range=(3,3))
    
    wordcloud_base64 = generate_wordcloud_base64(cleaned_series, "viridis")
    
    topics = perform_lda_topic_modeling(pdf, n_topics=4, n_words=6)
    aspects = extract_aspect_sentiments(pdf)
    complaints = extract_complaint_analytics(pdf)
    
    pos_df = pd.DataFrame()
    neg_df = pd.DataFrame()
    
    if label_col and label_col in pdf.columns:
        pos_df = pdf[pdf[label_col].astype(str).str.lower().str.contains("pos|4|5|good|high", na=False)]
        neg_df = pdf[pdf[label_col].astype(str).str.lower().str.contains("neg|1|2|bad|low", na=False)]
    elif 'Label' in pdf.columns:
        pos_df = pdf[pdf['Label'].astype(str).str.lower().str.contains("pos|4|5|good|high", na=False)]
        neg_df = pdf[pdf['Label'].astype(str).str.lower().str.contains("neg|1|2|bad|low", na=False)]
        
    pos_corpus = get_cleaned_text_series(pos_df) if not pos_df.empty else cleaned_series
    neg_corpus = get_cleaned_text_series(neg_df) if not neg_df.empty else cleaned_series
    
    pos_phrases = get_top_ngrams(pos_corpus, n=15, ngram_range=(1,2))
    neg_phrases = get_top_ngrams(neg_corpus, n=15, ngram_range=(1,2))

    return {
        "topics": topics,
        "aspects": aspects,
        "complaints": complaints,
        "top_unigrams": top_unigrams,
        "top_bigrams": top_bigrams,
        "top_trigrams": top_trigrams,
        "wordcloud_base64": wordcloud_base64,
        "positive_phrases": pos_phrases,
        "negative_phrases": neg_phrases,
        "text_statistics": {
            "total_documents": len(pdf),
            "avg_words_per_doc": round(float(np.mean(word_counts)), 1) if word_counts else 0,
            "avg_chars_per_doc": round(float(np.mean(lengths)), 1) if lengths else 0,
            "min_words": min(word_counts) if word_counts else 0,
            "max_words": max(word_counts) if word_counts else 0,
            "word_counts": word_counts[:500],
            "lengths_distribution": lengths[:500]
        }
    }

@router.get("/aspects")
async def get_aspect_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
    aspects = extract_aspect_sentiments(pdf)
    return {"aspects": aspects}

@router.get("/export-pdf")
async def export_pdf_report():
    pdf_data = await get_bi_analytics()
    kpis = pdf_data.get('kpi_summary', {})
    
    class PDFReport(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Executive Business Intelligence Report - ReviewMiner AI', 0, 1, 'C')
            self.ln(2)
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "1. Executive KPI Summary & Overview", ln=1)
    pdf.set_font("Arial", size=10)
    summary_text = pdf_data.get('executive_summary', '').encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(3)
    pdf.cell(0, 6, f"Satisfaction Index: {kpis.get('satisfaction_index', 0)}%", ln=1)
    pdf.cell(0, 6, f"Positive Feedback Share: {kpis.get('positive_pct', 0)}%", ln=1)
    pdf.cell(0, 6, f"Dissatisfaction Rate: {kpis.get('dissatisfaction_rate', 0)}%", ln=1)
    pdf.cell(0, 6, f"Dominant Customer Sentiment: {kpis.get('dominant_sentiment', 'N/A')}", ln=1)
    pdf.ln(4)
    
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "2. Strongest Business Areas", ln=1)
    pdf.set_font("Arial", size=10)
    for area in pdf_data.get('strongest_business_areas', []):
        clean_area = f"- {area['focus_area']}: {area['evidence']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_area)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "3. Priority Problems & Friction Matrix", ln=1)
    pdf.set_font("Arial", size=10)
    for prob in pdf_data.get('priority_problems', []):
        clean_prob = f"- [{prob['priority']}] {prob['issue']}: {prob['evidence']} -> {prob['recommended_action']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_prob)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "4. Business Growth Opportunities", ln=1)
    pdf.set_font("Arial", size=10)
    for opp in pdf_data.get('business_opportunities', []):
        clean_opp = f"- {opp['category']}: {opp['opportunity']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_opp)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "5. Strategic AI Action Recommendations", ln=1)
    pdf.set_font("Arial", size=10)
    for rec in pdf_data.get('strategic_recommendations', []):
        clean_rec = f"- [{rec['priority']}] Evidence: {rec['evidence']} | Action: {rec['action']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_rec)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "6. Executive Action Plan", ln=1)
    pdf.set_font("Arial", size=10)
    for act in pdf_data.get('action_plan', []):
        clean_act = f"- [{act['priority']}] {act['issue']} -> {act['action']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_act)

    buf = pdf.output(dest='S')
    if isinstance(buf, str):
        pdf_bytes = buf.encode('latin-1')
    else:
        pdf_bytes = bytes(buf)
        
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=Executive_BI_Report.pdf"})
