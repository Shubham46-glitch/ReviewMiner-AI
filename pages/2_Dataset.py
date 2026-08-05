import streamlit as st
import pandas as pd
import plotly.express as px
import data_manager
from ui_utils import setup_page, custom_metric_card, apply_plotly_theme

setup_page("Dataset Upload & Overview", "Upload your custom text data or explore the active dataset", "📂")

df = data_manager.get_current_df()
is_custom = data_manager.is_custom_data_active()
ds_name = data_manager.get_dataset_name()

tab1, tab2 = st.tabs(["📤 Custom Text Data Upload Center", "📊 Dataset Explorer"])

with tab1:
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #7C3AED;">Upload Custom Text Data</h3>
        <p style="color: #94A3B8;">
            Upload your customer reviews, feedback comments, job descriptions, or plain text documents. All text mining modules (EDA, Word Clouds, Sentiment Analysis, Machine Learning, and Reports) will dynamically analyze your data!
        </p>
    </div>
    """, unsafe_allow_html=True)

    upload_mode = st.radio("Choose Input Method", ["CSV / Excel / TSV File Upload", "Plain Text File (.txt)", "Direct Raw Text Entry"], horizontal=True)

    if upload_mode == "CSV / Excel / TSV File Upload":
        uploaded_file = st.file_uploader("Upload CSV, Excel, or TSV file containing text data", type=["csv", "xlsx", "xls", "tsv"])
        
        if uploaded_file is not None:
            try:
                temp_df = data_manager.read_file_with_encodings(uploaded_file)
                st.success(f"File loaded successfully! Found **{temp_df.shape[0]:,}** rows and **{temp_df.shape[1]}** columns.")
                
                st.markdown("#### Map Dataset Columns")
                auto_text, auto_label, auto_plat = data_manager.auto_detect_columns(temp_df)
                
                all_cols = temp_df.columns.tolist()
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    text_idx = all_cols.index(auto_text) if auto_text in all_cols else 0
                    selected_text_col = st.selectbox("Select Text/Review Column *", options=all_cols, index=text_idx)
                    
                with col_m2:
                    label_options = ["[Auto-Generate Sentiment Labels using AI (VADER)]"] + all_cols
                    label_idx = label_options.index(auto_label) if auto_label in label_options else 0
                    selected_label_col = st.selectbox("Select Sentiment Label Column", options=label_options, index=label_idx)
                    
                with col_m3:
                    plat_options = ["[None / Default Category]"] + all_cols
                    plat_idx = plat_options.index(auto_plat) if auto_plat in plat_options else 0
                    selected_plat_col = st.selectbox("Select Platform / Category Column", options=plat_options, index=plat_idx)
                
                st.markdown("##### Preview Raw Uploaded Data")
                st.dataframe(temp_df.head(5), use_container_width=True)
                
                if st.button("🚀 Process & Apply Custom Dataset", type="primary", use_container_width=True):
                    with st.spinner("Processing custom text data & applying Text Mining pipeline..."):
                        final_label_col = None if selected_label_col.startswith("[Auto-Generate") else selected_label_col
                        final_plat_col = None if selected_plat_col.startswith("[None") else selected_plat_col
                        
                        data_manager.process_and_set_custom_df(
                            raw_df=temp_df,
                            text_col=selected_text_col,
                            label_col=final_label_col,
                            platform_col=final_plat_col,
                            dataset_name=uploaded_file.name,
                            auto_label_missing=True
                        )
                        st.session_state['just_uploaded'] = True
                        st.success(f"Custom Dataset '{uploaded_file.name}' processed successfully!")
                        st.rerun()
            except Exception as e:
                st.error(f"Error reading uploaded file: {str(e)}")

    elif upload_mode == "Plain Text File (.txt)":
        uploaded_txt = st.file_uploader("Upload Plain Text (.txt) file", type=["txt"])
        split_option = st.selectbox("Split text into records by:", ["Line by Line", "Double Line Breaks (Paragraphs)"])
        
        if uploaded_txt is not None:
            content = uploaded_txt.read().decode("utf-8", errors="ignore")
            if split_option == "Line by Line":
                lines = [line.strip() for line in content.split("\n") if line.strip()]
            else:
                lines = [p.strip() for p in content.split("\n\n") if p.strip()]
                
            st.info(f"Extracted **{len(lines):,}** text records from **{uploaded_txt.name}**.")
            temp_df = pd.DataFrame({"Text": lines, "Window": "TXT Upload"})
            
            st.dataframe(temp_df.head(10), use_container_width=True)
            
            if st.button("🚀 Process & Apply Text File", type="primary", use_container_width=True):
                with st.spinner("Analyzing sentiment and preparing text mining workspace..."):
                    data_manager.process_and_set_custom_df(
                        raw_df=temp_df,
                        text_col="Text",
                        label_col=None,
                        platform_col="Window",
                        dataset_name=uploaded_txt.name,
                        auto_label_missing=True
                    )
                    st.session_state['just_uploaded'] = True
                    st.success("Text file processed and set as active dataset!")
                    st.rerun()

    elif upload_mode == "Direct Raw Text Entry":
        st.markdown("<p style='color: #94A3B8;'>Paste multiple reviews or text lines below (one record per line):</p>", unsafe_allow_html=True)
        raw_text_input = st.text_area("Paste text records here...", height=200, placeholder="The product quality is superb, fast delivery!\nItem arrived broken, terrible service.\nAverage product, nothing special.")
        
        if st.button("🚀 Process & Apply Pasted Text", type="primary", use_container_width=True):
            if not raw_text_input.strip():
                st.warning("Please enter text before processing.")
            else:
                lines = [line.strip() for line in raw_text_input.split("\n") if line.strip()]
                temp_df = pd.DataFrame({"Text": lines, "Window": "Manual Entry"})
                
                with st.spinner("Analyzing sentiment and setting up text mining pipeline..."):
                    data_manager.process_and_set_custom_df(
                        raw_df=temp_df,
                        text_col="Text",
                        label_col=None,
                        platform_col="Window",
                        dataset_name="Direct Text Input",
                        auto_label_missing=True
                    )
                    st.session_state['just_uploaded'] = True
                    st.success(f"Successfully processed {len(lines)} pasted text records!")
                    st.rerun()

    # --- INSTANT ANALYTICS & INSIGHTS DISPLAY AFTER UPLOAD ---
    if is_custom and not df.empty:
        st.divider()
        st.markdown(f"""
        <div class="premium-card" style="border-left: 5px solid #06B6D4;">
            <h3 style="color: #06B6D4;">⚡ Instant Analysis Results: {ds_name}</h3>
            <p style="color: #94A3B8;">Dataset processed cleanly! Below is an immediate analytical summary of your uploaded data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        pos_cnt = len(df[df['Label'] == 'Positive']) if 'Label' in df.columns else 0
        neu_cnt = len(df[df['Label'] == 'Neutral']) if 'Label' in df.columns else 0
        neg_cnt = len(df[df['Label'] == 'Negative']) if 'Label' in df.columns else 0
        total_rec = len(df)
        pos_pct = (pos_cnt / total_rec * 100) if total_rec > 0 else 0
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            custom_metric_card("Total Records", f"{total_rec:,}", "Processed text rows", icon="📄")
        with col_m2:
            custom_metric_card("Positive Share", f"{pos_pct:.1f}%", f"{pos_cnt:,} positive", icon="😊", color="#22C55E")
        with col_m3:
            custom_metric_card("Negative Share", f"{(neg_cnt/total_rec*100):.1f}%", f"{neg_cnt:,} negative", icon="😡", color="#EF4444")
        with col_m4:
            custom_metric_card("Neutral Share", f"{(neu_cnt/total_rec*100):.1f}%", f"{neu_cnt:,} neutral", icon="😐", color="#FACC15")

        if 'Label' in df.columns:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.subheader("📊 Sentiment Analysis Results")
            col_chart1, col_chart2 = st.columns(2)
            sentiment_counts = df['Label'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            color_map = {"Positive": "#22C55E", "Neutral": "#FACC15", "Negative": "#EF4444"}
            
            with col_chart1:
                fig_pie = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment', color_discrete_map=color_map, hole=0.4, title="Sentiment Share")
                fig_pie = apply_plotly_theme(fig_pie)
                st.plotly_chart(fig_pie, use_container_width=True)
            with col_chart2:
                fig_bar = px.bar(sentiment_counts, x='Sentiment', y='Count', color='Sentiment', color_discrete_map=color_map, text_auto=True, title="Sentiment Counts")
                fig_bar = apply_plotly_theme(fig_bar)
                st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("🚀 Jump to Modules")
        st.markdown("<p style='color: #94A3B8;'>Choose a module to explore deeper insights on your uploaded data:</p>", unsafe_allow_html=True)
        btn_c1, btn_c2, btn_c3, btn_c4 = st.columns(4)
        with btn_c1:
            if st.button("📊 Exploratory Data (EDA)", use_container_width=True):
                st.switch_page("pages/3_EDA.py")
        with btn_c2:
            if st.button("☁️ Text Mining", use_container_width=True):
                st.switch_page("pages/5_Text_Mining.py")
        with btn_c3:
            if st.button("🤖 Machine Learning", use_container_width=True):
                st.switch_page("pages/7_Machine_Learning.py")
        with btn_c4:
            if st.button("📈 Business Intelligence", use_container_width=True):
                st.switch_page("pages/9_Business_Intelligence.py")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    if is_custom and not df.empty:
        st.subheader(f"📁 Dataset Explorer: {ds_name}")
    else:
        st.subheader("📦 Dataset Explorer")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            custom_metric_card("Total Rows", f"{df.shape[0]:,}", "Text records loaded", icon="📄")
        with col2:
            custom_metric_card("Total Columns", f"{df.shape[1]}", "Data attributes available", icon="🗂️", color="#06B6D4")
        with col3:
            custom_metric_card("Missing Values", f"{df.isnull().sum().sum()}", "Incomplete cells", icon="⚠️", color="#EF4444")

        st.markdown("""
        <div class="premium-card">
            <h3>🔍 Interactive Data Explorer</h3>
            <p style="color: #94A3B8; margin-bottom: 20px;">Search, sort, and filter the processed dataset feeding the Text Mining pipeline.</p>
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No dataset uploaded yet. Please upload a dataset in the 'Upload Custom Text Data' tab above.")
