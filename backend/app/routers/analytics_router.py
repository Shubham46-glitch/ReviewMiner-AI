from fastapi import APIRouter, HTTPException, Response
from backend.app.routers.dataset_router import STORED_DATASETS, ACTIVE_DATASET_ID
from backend.app.services.text_engine import get_top_ngrams, generate_wordcloud_base64, perform_lda_topic_modeling, extract_aspect_sentiments
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from fpdf import FPDF
import pandas as pd
import numpy as np

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

def get_active_df():
    if not ACTIVE_DATASET_ID or ACTIVE_DATASET_ID not in STORED_DATASETS:
        return None
    return STORED_DATASETS[ACTIVE_DATASET_ID]["processed_df"]

@router.get("/preprocessing")
async def get_preprocessing_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
    
    orig_words = int(pdf["Text"].astype(str).str.split().str.len().sum())
    clean_tokens = int(pdf["Cleaned_Text"].astype(str).str.split().str.len().sum())
    
    preview = pdf[["Text", "Cleaned_Text"]].head(20).to_dict(orient="records")
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
        
    lengths = pdf["Text"].astype(str).str.len().tolist()
    word_counts = pdf["Text"].astype(str).str.split().str.len().tolist()
    
    top_unigrams = get_top_ngrams(pdf["Cleaned_Text"], n=15, ngram_range=(1,1))
    top_bigrams = get_top_ngrams(pdf["Cleaned_Text"], n=15, ngram_range=(2,2))
    top_trigrams = get_top_ngrams(pdf["Cleaned_Text"], n=15, ngram_range=(3,3))
    
    plat_counts = pdf["Window"].value_counts().to_dict() if "Window" in pdf.columns else {}

    return {
        "total_reviews": len(pdf),
        "avg_length": round(float(np.mean(lengths)), 1) if lengths else 0,
        "duplicate_count": int(pdf["Text"].duplicated().sum()),
        "missing_count": int(pdf["Text"].isnull().sum()),
        "lengths_distribution": lengths[:500],
        "word_counts": word_counts[:500],
        "platform_distribution": plat_counts,
        "top_unigrams": top_unigrams,
        "top_bigrams": top_bigrams,
        "top_trigrams": top_trigrams
    }

@router.get("/sentiment")
async def get_sentiment_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    total = len(pdf)
    counts = pdf["Label"].value_counts().to_dict()
    pos = counts.get("Positive", 0)
    neu = counts.get("Neutral", 0)
    neg = counts.get("Negative", 0)
    
    plat_sentiment = {}
    if "Window" in pdf.columns:
        grouped = pdf.groupby(["Window", "Label"]).size().unstack(fill_value=0)
        plat_sentiment = grouped.to_dict(orient="index")

    return {
        "total_reviews": total,
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "positive_pct": round(pos / total * 100, 1) if total > 0 else 0,
        "neutral_pct": round(neu / total * 100, 1) if total > 0 else 0,
        "negative_pct": round(neg / total * 100, 1) if total > 0 else 0,
        "platform_sentiment": plat_sentiment
    }

@router.get("/wordclouds")
async def get_wordcloud_analytics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    all_text = " ".join(pdf["Cleaned_Text"].astype(str))
    pos_text = " ".join(pdf[pdf["Label"] == "Positive"]["Cleaned_Text"].astype(str))
    neg_text = " ".join(pdf[pdf["Label"] == "Negative"]["Cleaned_Text"].astype(str))
    
    wc_overall = generate_wordcloud_base64(all_text, "viridis")
    wc_positive = generate_wordcloud_base64(pos_text, "Greens")
    wc_negative = generate_wordcloud_base64(neg_text, "Reds")
    
    top_terms = get_top_ngrams(pdf["Cleaned_Text"], n=20, ngram_range=(1,1))
    
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
        
    total = len(pdf)
    pos = len(pdf[pdf["Label"] == "Positive"])
    neu = len(pdf[pdf["Label"] == "Neutral"])
    neg = len(pdf[pdf["Label"] == "Negative"])
    
    sat_score = round(((pos * 1) + (neu * 0.5)) / total * 100, 1) if total > 0 else 0
    
    neg_corpus = pdf[pdf["Label"] == "Negative"]["Cleaned_Text"].astype(str)
    pos_corpus = pdf[pdf["Label"] == "Positive"]["Cleaned_Text"].astype(str)
    
    neg_kw = get_top_ngrams(neg_corpus, n=10)
    pos_kw = get_top_ngrams(pos_corpus, n=10)
    
    neg_words = [k["word"] for k in neg_kw]
    pos_words = [k["word"] for k in pos_kw]
    
    recommendations = []
    if any(w in neg_words for w in ['late', 'delay', 'delivery', 'time', 'slow']):
        recommendations.append("🚚 Optimize delivery timelines & supply chain distribution.")
    if any(w in neg_words for w in ['broken', 'damage', 'quality', 'bad', 'poor', 'worst', 'cheap']):
        recommendations.append("📦 Upgrade product packaging and enforce strict QA testing.")
    if any(w in neg_words for w in ['rude', 'service', 'support', 'staff', 'unhelpful', 'email']):
        recommendations.append("📞 Enhance customer support response speeds & train service reps.")
    if any(w in neg_words for w in ['price', 'expensive', 'cost', 'money', 'worth']):
        recommendations.append("💰 Review pricing strategy or introduce promotional loyalty tiers.")
    if not recommendations:
        recommendations.append("🌟 Maintain excellent operational standards and scale top customer features.")

    return {
        "customer_satisfaction_pct": sat_score,
        "positive_pct": round(pos / total * 100, 1) if total > 0 else 0,
        "negative_pct": round(neg / total * 100, 1) if total > 0 else 0,
        "neutral_pct": round(neu / total * 100, 1) if total > 0 else 0,
        "top_complaints": neg_words[:5],
        "top_positive_features": pos_words[:5],
        "recommendations": recommendations
    }

@router.get("/topics")
async def get_lda_topics():
    pdf = get_active_df()
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
    topics = perform_lda_topic_modeling(pdf, n_topics=4, n_words=6)
    return {"topics": topics}

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
    
    class PDFReport(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Executive Business Intelligence Report - ReviewMiner AI', 0, 1, 'C')
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "1. Executive Summary & KPIs", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Customer Satisfaction Score: {pdf_data['customer_satisfaction_pct']}%", ln=1)
    pdf.cell(0, 10, f"Positive Reviews Share: {pdf_data['positive_pct']}%", ln=1)
    pdf.cell(0, 10, f"Negative Reviews Share: {pdf_data['negative_pct']}%", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "2. Key Intelligence Drivers", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Top Appreciated Features: {', '.join(pdf_data['top_positive_features'])}", ln=1)
    pdf.cell(0, 10, f"Top Customer Complaints: {', '.join(pdf_data['top_complaints'])}", ln=1)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "3. Strategic Recommendations", ln=1)
    pdf.set_font("Arial", size=12)
    for rec in pdf_data['recommendations']:
        clean_rec = rec.encode('ascii', 'ignore').decode('ascii').strip()
        pdf.multi_cell(0, 10, f"- {clean_rec}")
        
    buf = pdf.output(dest='S')
    if isinstance(buf, str):
        pdf_bytes = buf.encode('latin-1')
    else:
        pdf_bytes = bytes(buf)
        
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=Executive_Report.pdf"})
