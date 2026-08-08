import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as gg
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme, check_dataset_loaded
import data_manager
from backend.app.services.ml_engine import GLOBAL_ML_ENGINE

setup_page("Machine Learning Classification", "Supervised ML Training, 3-Model Comparison, Cross-Validation & Prediction Playground", "🤖")
check_dataset_loaded()

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset uploaded yet. Please upload a dataset in the Dataset Upload Center.")
    st.stop()

schema = data_manager.detect_dataset_schema(df)
text_col = schema['text'] or ('Text' if 'Text' in df.columns else df.columns[0])
label_col = schema['label'] or ('Label' if 'Label' in df.columns else df.columns[0])

if 'Label' not in df.columns:
    df['Label'] = df['Text'].apply(data_manager.predict_vader_sentiment)
    label_col = 'Label'

tab1, tab2, tab3 = st.tabs(["🚀 Model Training & Evaluation", "🔍 Test Prediction & Failure Audit", "🌌 K-Means Text Clustering"])

# =========================================================
# TAB 1 — SUPERVISED ML TRAINING & COMPARISON
# =========================================================
with tab1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("🤖 Section 1 — Supervised Machine Learning Pipeline")
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Train and compare 3 classifiers (Multinomial Naive Bayes, Logistic Regression, Linear SVM) dynamically on your uploaded dataset.</p>", unsafe_allow_html=True)

    if st.button("⚡ Train & Evaluate All 3 ML Models Now", type="primary", use_container_width=True):
        with st.spinner("Training Naive Bayes, Logistic Regression, and Linear SVM on active dataset..."):
            try:
                ml_res = GLOBAL_ML_ENGINE.train_model(df, dataset_id="streamlit_dataset", text_col=text_col, label_col=label_col)
                st.session_state['ml_results'] = ml_res
                st.success("✅ Machine Learning Models trained and evaluated successfully!")
            except Exception as e:
                st.error(f"❌ Training error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

    if 'ml_results' not in st.session_state:
        try:
            st.session_state['ml_results'] = GLOBAL_ML_ENGINE.train_model(df, dataset_id="streamlit_dataset", text_col=text_col, label_col=label_col)
        except Exception as e:
            st.info(f"ℹ️ {str(e)}")

    if 'ml_results' in st.session_state:
        ml_res = st.session_state['ml_results']
        t_info = ml_res['target_info']
        best_name = ml_res['best_model_name']
        best_metrics = ml_res['metrics']
        models_comp = ml_res['models_comparison']

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("📋 Dataset & Target Label Detection")
        
        tc1, tc2, tc3, tc4, tc5 = st.columns(5)
        with tc1: custom_metric_card("Target Column", t_info['target_column'], "Detected Label", icon="🎯", color="#06B6D4")
        with tc2: custom_metric_card("Target Classes", f"{t_info['num_classes']}", "Unique Classes", icon="🔢", color="#A855F7")
        with tc3: custom_metric_card("Class Labels", ", ".join(t_info['labels']), "Actual Classes", icon="🏷️", color="#3B82F6")
        with tc4: custom_metric_card("Train / Test Split", f"{t_info['train_samples']} / {t_info['test_samples']}", "80/20 Stratified", icon="秤️", color="#10B981")
        with tc5: custom_metric_card("TF-IDF Features", f"{t_info['vocab_size']:,}", "Vocabulary Size", icon="📚", color="#F59E0B")

        st.markdown("##### 📊 Actual Target Class Distribution")
        dist_data = pd.DataFrame({"Class": list(t_info['class_counts'].keys()), "Samples": list(t_info['class_counts'].values())})
        fig_dist = px.bar(dist_data, x="Class", y="Samples", color="Class", text_auto=True, title="Target Class Sample Volume")
        fig_dist = apply_plotly_theme(fig_dist)
        fig_dist.update_layout(
            title=dict(text="Target Class Sample Volume", font=dict(color="#FFFFFF", size=14)),
            xaxis=dict(title=dict(text="Sentiment Class", font=dict(color="#94A3B8", size=12))),
            yaxis=dict(title=dict(text="Number of Samples", font=dict(color="#94A3B8", size=12))),
            height=280
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("🏆 Model Comparison Matrix")
        
        comp_rows = []
        for m_name, m_val in models_comp.items():
            comp_rows.append({
                "Algorithm Model": m_name,
                "Accuracy Score": f"{m_val['accuracy']*100:.2f}%",
                "Precision Score": f"{m_val['precision']*100:.2f}%",
                "Recall Score": f"{m_val['recall']*100:.2f}%",
                "F1 Score": f"{m_val['f1_score']*100:.2f}%",
                "Status": "🏆 Best Winning Model" if m_name == best_name else "Evaluated"
            })
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

        st.markdown(f"#### 🥇 Winning Classifier: **{best_name}**")
        bk1, bk2, bk3, bk4 = st.columns(4)
        with bk1: custom_metric_card("Accuracy", f"{best_metrics['accuracy']*100:.1f}%", "Overall correctness", icon="🎯", color="#22C55E")
        with bk2: custom_metric_card("Precision", f"{best_metrics['precision']*100:.1f}%", "Positive predictive value", icon="🔍", color="#06B6D4")
        with bk3: custom_metric_card("Recall", f"{best_metrics['recall']*100:.1f}%", "Sensitivity / True positive rate", icon="📈", color="#FACC15")
        with bk4: custom_metric_card("F1 Score", f"{best_metrics['f1_score']*100:.1f}%", "Harmonic mean F-measure", icon="🏆", color="#A855F7")

        col_cm1, col_cm2 = st.columns(2)
        
        with col_cm1:
            st.subheader(f"Confusion Matrix ({best_name})")
            cm_data = ml_res['confusion_matrix']
            cm_matrix = cm_data['matrix']
            cm_labels = cm_data['labels']

            fig_cm = gg.Figure(data=gg.Heatmap(
                z=cm_matrix,
                x=cm_labels,
                y=cm_labels,
                colorscale='Purples',
                text=cm_matrix,
                hoverinfo='x+y+z'
            ))
            for i in range(len(cm_labels)):
                for j in range(len(cm_labels)):
                    fig_cm.add_annotation(
                        x=cm_labels[j],
                        y=cm_labels[i],
                        text=str(cm_matrix[i][j]),
                        showarrow=False,
                        font=dict(color="white" if cm_matrix[i][j] > 0 else "#64748B", size=13, family="Inter")
                    )
            fig_cm = apply_plotly_theme(fig_cm)
            fig_cm.update_layout(
                title=dict(text=f"Confusion Matrix ({best_name})", font=dict(color="#FFFFFF", size=14)),
                xaxis=dict(title=dict(text="Predicted Label", font=dict(color="#94A3B8", size=12))),
                yaxis=dict(title=dict(text="Actual Ground Truth Label", font=dict(color="#94A3B8", size=12)), autorange="reversed"),
                height=320
            )
            st.plotly_chart(fig_cm, use_container_width=True)

        with col_cm2:
            st.subheader("Classification Report Metrics")
            report_df = pd.DataFrame(ml_res['classification_report']).transpose()
            st.dataframe(report_df.style.format("{:.4f}"), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        col_cv, col_feat = st.columns(2)

        with col_cv:
            st.subheader("🔄 5-Fold Stratified Cross-Validation")
            cv_info = ml_res['cross_validation']
            if cv_info['has_cv']:
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; padding: 15px; border-radius: 10px;">
                    <span style="color: #10B981; font-size: 1.2rem; font-weight: 800;">Mean CV Accuracy: {cv_info['mean_accuracy']}%</span><br>
                    <span style="color: #94A3B8; font-size: 0.85rem;">Standard Deviation: ±{cv_info['std_accuracy']}% across 5 stratified folds.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ 5-Fold Cross Validation unavailable: Requires at least 5 samples per target class.")

        with col_feat:
            st.subheader("🔑 Top Model Feature Insights")
            feats = ml_res.get('feature_insights', {})
            if feats:
                for cls_name, top_words in feats.items():
                    st.markdown(f"**Class `{cls_name}` Top Predictive Words:**")
                    st.code(", ".join(top_words))
            else:
                st.info("Top TF-IDF feature insights unavailable.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.header("🎮 Section 8 — Interactive Prediction Playground")
        st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Test real-time review sentiment prediction using the winning trained model.</p>", unsafe_allow_html=True)

        user_input = st.text_area("Enter a new review text for real-time prediction:", "The battery life is amazing and display screen is super crisp!")
        if st.button("🔮 Predict Sentiment Class", type="primary"):
            if not user_input or not user_input.strip():
                st.warning("⚠️ Please enter a review to classify.")
            else:
                pred_res = GLOBAL_ML_ENGINE.predict_sentiment(user_input)
                if pred_res.get("status") == "error":
                    st.error(f"⚠️ {pred_res.get('detail')}")
                else:
                    conf_str = f" (Confidence: **{pred_res['confidence']}%**)" if pred_res.get('confidence') is not None else ""
                    st.markdown(f"### Predicted Class: **`{pred_res['predicted_class']}`**{conf_str}")
                    st.markdown(f"<span style='color: #94A3B8; font-size: 0.85rem;'>Engine Model Used: {pred_res['model_used']}</span>", unsafe_allow_html=True)
                    
                    if pred_res.get('class_probabilities'):
                        prob_df = pd.DataFrame({"Class": list(pred_res['class_probabilities'].keys()), "Probability (%)": list(pred_res['class_probabilities'].values())})
                        fig_p = px.bar(prob_df, x="Class", y="Probability (%)", color="Class", text_auto='.1f', title="Prediction Confidence Probabilities")
                        fig_p = apply_plotly_theme(fig_p)
                        fig_p.update_layout(
                            xaxis=dict(title=dict(text="Sentiment Class", font=dict(color="#94A3B8", size=12))),
                            yaxis=dict(title=dict(text="Probability (%)", font=dict(color="#94A3B8", size=12))),
                            height=260
                        )
                        st.plotly_chart(fig_p, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("🔍 Tab 2 — Test Prediction Explorer & Misclassification Audit")

    if 'ml_results' in st.session_state:
        ml_res = st.session_state['ml_results']
        test_preds = ml_res.get('test_predictions', [])
        misclassified = ml_res.get('misclassifications', [])

        st.subheader("1. Test Set Predictions Explorer")
        filter_status = st.radio("Filter Test Predictions", ["All Test Predictions", "Correct Predictions Only", "Misclassified Failures Only"], horizontal=True)

        df_tp = pd.DataFrame(test_preds)
        if not df_tp.empty:
            if filter_status == "Correct Predictions Only":
                df_tp = df_tp[df_tp['correct'] == True]
            elif filter_status == "Misclassified Failures Only":
                df_tp = df_tp[df_tp['correct'] == False]

            st.dataframe(df_tp[['index', 'review', 'actual', 'predicted', 'correct']], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("2. Misclassification Failure Analysis")
        st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Inspect reviews where the model prediction differed from the actual ground truth label.</p>", unsafe_allow_html=True)

        if misclassified:
            df_mis = pd.DataFrame(misclassified)
            st.dataframe(df_mis[['index', 'review', 'actual', 'predicted']], use_container_width=True, hide_index=True)
        else:
            st.success("🎉 Perfect test accuracy! Zero misclassifications detected on test set.")
    else:
        st.info("ℹ️ Please train Machine Learning models in **Tab 1** first.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.header("🌌 Tab 3 — Unsupervised K-Means Text Clustering")
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Discovers natural structural groupings in review text using TF-IDF features and PCA 2D dimension reduction.</p>", unsafe_allow_html=True)

    n_clusters = st.slider("Select Number of Clusters (K)", min_value=2, max_value=6, value=3)
    df_clustered, km_model, km_vec = data_manager.compute_kmeans_clusters(df, n_clusters=n_clusters)

    if 'Cluster' in df_clustered.columns:
        col_cl1, col_cl2 = st.columns(2)
        with col_cl1:
            fig_cluster_pie = px.pie(df_clustered, names='Cluster', title="Cluster Size Share", hole=0.4)
            fig_cluster_pie = apply_plotly_theme(fig_cluster_pie)
            st.plotly_chart(fig_cluster_pie, use_container_width=True)

        with col_cl2:
            fig_pca = px.scatter(df_clustered, x='PCA_1', y='PCA_2', color='Cluster', title="2D PCA Text Cluster Projection", hover_data=[text_col])
            fig_pca = apply_plotly_theme(fig_pca)
            fig_pca.update_layout(xaxis_title="Principal Component 1", yaxis_title="Principal Component 2")
            st.plotly_chart(fig_pca, use_container_width=True)
    else:
        st.info("ℹ️ Clustering requires a non-empty text dataset.")
    st.markdown('</div>', unsafe_allow_html=True)
