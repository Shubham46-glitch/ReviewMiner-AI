# ReviewMiner AI 🤖 — Enterprise Text Analytics & Executive BI Platform

Welcome to **ReviewMiner AI**, an AI-powered text mining platform designed to transform unstructured customer reviews into actionable business intelligence, interactive sentiment analytics, aspect extraction, and executive decision-support dashboards.

---

## 🌟 Modern Architecture

ReviewMiner AI features two powerful interface experiences powered by a shared Python FastAPI analytics engine:

1. **⚡ React + Vite Dark Executive Dashboard (Recommended)**
   - High-performance, modern UI with interactive Plotly quadrant matrices, risk scatter charts, and real-time sentiment prediction.
2. **🎈 Streamlit Analytics Suite**
   - Pure Python multi-page data science platform.

---

## 🚀 Running Locally

To launch the full **React UI + FastAPI Backend** locally:

### 1. Clone the repository
```bash
git clone https://github.com/Shubham46-glitch/ReviewMiner-AI.git
cd ReviewMiner-AI
```

### 2. Start the Backend API Engine (FastAPI)
```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 3. Start the Frontend App (React + Vite)
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser!

---

## 🎈 Running Streamlit App (Alternative)

If you prefer to run the Streamlit interface:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## 🛠️ Tech Stack & Subsystems

- **Frontend UI:** React 18, TypeScript, Vite, TailwindCSS, Framer Motion, Lucide Icons, Plotly.js
- **Backend Engine:** FastAPI, Python 3.10+, Uvicorn
- **NLP & Mining Subsystem:** NLTK, Scikit-Learn (TF-IDF, Logistic Regression, Naive Bayes, LinearSVC), VADER Lexicon
- **Visualizations:** Plotly, WordCloud
- **Reporting:** FPDF Executive Report Generator

---

## 📑 Core Modules & Features

- **📂 Upload Dataset Center:** Centrally upload any CSV/Excel review dataset with dynamic column detection.
- **📊 EDA Analytics:** Schema overview, text length distributions, missing value audits.
- **Sparkles Topic & Aspect Mining:** Centralized text cleaning pipeline with Word Cloud, Unigram/Bigram/Trigram extraction, LDA Topic Modeling, Aspect $\times$ Sentiment matrix, Phrase & Complaint Mining.
- **😊 Sentiment Analysis:** Dynamic positive/neutral/negative share, polarity distribution, aspect heatmap matrix.
- **🤖 Machine Learning:** Dynamic class detection, automated model comparison, feature importance, test set evaluation.
- **🔮 Sentiment Prediction:** Real-time sentiment classifier playground with automatic TF-IDF pipeline training and Lexicon fallbacks.
- **💼 Executive BI Dashboard:** 2-Axis Strength vs. Pain Matrix (Quadrant Plot), Priority Risk Scatter Chart, Opportunity Progress Ranking, and Ranked Executive Action Plan.
- **📄 Executive Report:** Direct executive management brief with PDF export capability.
