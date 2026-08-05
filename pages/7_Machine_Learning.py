import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme

setup_page("Machine Learning Dashboard", "Train and evaluate sentiment classification models.", "🤖")

import data_manager

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No dataset uploaded yet. Please navigate to the **Dataset Upload & Info** page to upload your text data.")
    st.stop()
df['Cleaned_Text'] = df['Cleaned_Text'].astype(str).fillna("")
df = df[df['Cleaned_Text'].str.strip() != ""].reset_index(drop=True)
if 'Label' not in df.columns or df['Label'].nunique() == 0:
    df['Label'] = 'Neutral'

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("1️⃣ Data Preparation")
col1, col2, col3 = st.columns(3)
with col1:
    custom_metric_card("Total Samples", f"{len(df):,}", "Cleaned records", icon="📄")
with col2:
    custom_metric_card("Classes", df['Label'].nunique(), "Categories", icon="🏷️", color="#06B6D4")
with col3:
    custom_metric_card("Missing Values", df.isnull().sum().sum(), "NaT/NaN", icon="✅", color="#22C55E")
st.markdown('</div>', unsafe_allow_html=True)

if len(df) < 2:
    st.warning("⚠️ Machine Learning requires at least 2 text samples. Please upload a larger dataset.")
    st.stop()

if df['Label'].nunique() < 2:
    st.warning(f"⚠️ Machine Learning requires at least 2 distinct sentiment classes (e.g. Positive and Negative). Your dataset currently contains only 1 class ('{df['Label'].iloc[0]}'). Please map sentiment labels in the Dataset tab or auto-generate labels using VADER.")
    st.stop()

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("2️⃣ Feature Extraction (TF-IDF)")
X = df['Cleaned_Text']
y = df['Label']

try:
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X_vec = vectorizer.fit_transform(X)
except ValueError:
    try:
        vectorizer = TfidfVectorizer(max_features=5000)
        X_vec = vectorizer.fit_transform(X)
    except Exception as e:
        st.error(f"Error during feature extraction: {str(e)}")
        st.stop()

vocab_size = len(vectorizer.vocabulary_)
matrix_shape = X_vec.shape

col_tf1, col_tf2 = st.columns(2)
with col_tf1:
    custom_metric_card("Vocabulary Size", f"{vocab_size:,}", "Unique Words Extract", icon="📚", color="#7C3AED")
with col_tf2:
    custom_metric_card("Matrix Shape", f"{matrix_shape[0]} × {matrix_shape[1]}", "Rows by Cols", icon="🧮", color="#06B6D4")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("3️⃣ Train Test Split")

# Stratify only if each class has at least 2 samples
class_counts = y.value_counts()
can_stratify = (y.nunique() > 1) and (class_counts.min() >= 2) and (len(y) >= 5)

if can_stratify:
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42, stratify=y)
elif len(y) >= 4:
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
else:
    # Very small custom uploaded dataset
    X_train, X_test, y_train, y_test = X_vec, X_vec, y, y

col_tt1, col_tt2 = st.columns(2)
with col_tt1:
    custom_metric_card("Training Set", X_train.shape[0], "Samples", icon="🏋️", color="#FACC15")
with col_tt2:
    custom_metric_card("Testing Set", X_test.shape[0], "Samples", icon="🧪", color="#EF4444")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.header("4️⃣ Model Training & Evaluation")
st.markdown("<p style='color: #94A3B8;'>Compare Multinomial Naive Bayes, Logistic Regression, and Linear SVM.</p>", unsafe_allow_html=True)

models = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Linear SVM": SVC(kernel='linear', probability=True)
}

if st.button("🚀 Train Models Now", type="primary"):
    with st.spinner("Training models..."):
        results = []
        trained_models = {}
        for name, model in models.items():
            try:
                start = time.time()
                model.fit(X_train, y_train)
                train_t = time.time() - start
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                trained_models[name] = model
                results.append({
                    "Algorithm": name, "Accuracy": acc, "Precision": prec, "Recall": rec, "F1 Score": f1, "Train Time (s)": round(train_t, 4)
                })
            except Exception as err:
                st.warning(f"Could not train {name}: {str(err)}")
            
        if not results:
            st.error("Failed to train models on the current dataset.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        results_df = pd.DataFrame(results)
        best_idx = results_df['F1 Score'].idxmax()
        best_name = results_df.loc[best_idx, 'Algorithm']
        best_model = trained_models[best_name]
        
        st.success(f"Models Trained! 🏆 Winner: {best_name}")
        st.dataframe(results_df.style.highlight_max(subset=['F1 Score', 'Accuracy'], color='#06B6D4', axis=0).format(precision=4), use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("5️⃣ Confusion Matrix")
        try:
            y_pred_best = best_model.predict(X_test)
            labels = sorted(y.unique().tolist())
            cm = confusion_matrix(y_test, y_pred_best, labels=labels)
            fig_cm = px.imshow(cm, x=labels, y=labels, text_auto=True, color_continuous_scale='Purples')
            fig_cm = apply_plotly_theme(fig_cm)
            st.plotly_chart(fig_cm, use_container_width=True)
        except Exception as e:
            st.info(f"Confusion Matrix unavailable: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("6️⃣ Classification Report")
        try:
            report = classification_report(y_test, y_pred_best, target_names=labels, output_dict=True)
            st.dataframe(pd.DataFrame(report).transpose().style.format("{:.4f}"), use_container_width=True)
        except Exception as e:
            st.info(f"Classification report unavailable: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("7️⃣ Top Important Features")
        try:
            f_names = vectorizer.get_feature_names_out()
            imp = None
            if best_name == "Multinomial Naive Bayes" and hasattr(best_model, 'feature_log_prob_'):
                imp = np.max(best_model.feature_log_prob_, axis=0)
            elif hasattr(best_model, 'coef_'):
                coef = best_model.coef_
                if coef.ndim == 1 or coef.shape[0] == 1:
                    imp = np.abs(coef.ravel())
                else:
                    imp = np.max(np.abs(coef), axis=0)
            
            if imp is not None and len(imp) > 0:
                n_feat = min(20, len(imp))
                top_idx = np.argsort(imp)[-n_feat:]
                imp_df = pd.DataFrame({'Word': f_names[top_idx], 'Importance': imp[top_idx]}).sort_values('Importance')
                fig_imp = px.bar(imp_df, x="Importance", y="Word", orientation='h', color="Importance", color_continuous_scale="Plasma")
                fig_imp = apply_plotly_theme(fig_imp)
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.info("Feature importance not available for this model.")
        except Exception as e:
            st.info("Top feature importance chart unavailable.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("8️⃣ Save Model")
        try:
            joblib.dump(best_model, "sentiment_model.pkl")
            joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
            st.success("✅ `sentiment_model.pkl` & `tfidf_vectorizer.pkl` serialized and saved.")
        except Exception as e:
            st.warning(f"Could not save model files: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('</div>', unsafe_allow_html=True)
