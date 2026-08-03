import streamlit as st
import streamlit.components.v1 as components
import data_manager

def get_active_keyword(title):
    t = title.lower()
    if "dashboard" in t:
        return "app"
    elif "dataset" in t:
        return "Dataset"
    elif "eda" in t or "exploratory" in t:
        return "EDA"
    elif "preprocessing" in t:
        return "Text_Preprocessing"
    elif "mining" in t:
        return "Text_Mining"
    elif "sentiment" in t:
        return "Sentiment_Analysis"
    elif "machine learning" in t:
        return "Machine_Learning"
    elif "prediction" in t:
        return "Review_Prediction"
    elif "business intelligence" in t:
        return "Business_Intelligence"
    return ""

def setup_page(title, subtitle, icon=""):
    st.set_page_config(page_title=title, layout="wide", page_icon=icon, initial_sidebar_state="expanded")
    active_kw = get_active_keyword(title)
    apply_custom_theme(active_kw)
    render_sidebar(active_kw)
    page_header(title, subtitle, icon)

def apply_custom_theme(active_kw=""):
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
        }}

        /* Hide default Streamlit elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebarNav"] {{display: none;}}
        
        /* Global Background */
        .stApp {{
            background-color: #0B1220;
            color: #FFFFFF;
        }}
        
        /* Sidebar Styling & Compact Layout */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
            border-right: 1px solid rgba(124, 58, 237, 0.15);
        }}
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}
        
        /* Animated Title CSS */
        .animated-title {{
            font-size: 1.6rem !important;
            font-weight: 900 !important;
            background: linear-gradient(270deg, #7C3AED, #06B6D4, #22C55E, #7C3AED);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 4s ease infinite;
            margin-bottom: 2px;
            text-align: center;
            line-height: 1.2;
        }}
        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Sleek Sidebar Page Links - Inactive State */
        div.stPageLink {{
            margin-bottom: 4px !important;
        }}
        div.stPageLink > a,
        a[data-testid="stPageLink-NavLink"],
        [data-testid="stSidebar"] a[href] {{
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            padding: 7px 12px !important;
            display: flex !important;
            align-items: center !important;
            box-shadow: none !important;
            text-decoration: none !important;
            color: #94A3B8 !important;
            font-weight: 600 !important;
            transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease !important;
        }}

        div.stPageLink p,
        a[data-testid="stPageLink-NavLink"] p,
        a[data-testid="stPageLink-NavLink"] span {{
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            margin: 0 !important;
            padding: 0 !important;
            color: #94A3B8 !important;
            white-space: nowrap !important;
        }}

        /* Hover Effect */
        div.stPageLink > a:hover,
        a[data-testid="stPageLink-NavLink"]:hover,
        [data-testid="stSidebar"] a[href]:hover {{
            background: rgba(124, 58, 237, 0.3) !important;
            border-color: #7C3AED !important;
            color: #FFFFFF !important;
        }}
        div.stPageLink > a:hover p,
        a[data-testid="stPageLink-NavLink"]:hover p {{
            color: #FFFFFF !important;
        }}
        
        /* ACTIVE PAGE LINK - Vibrant Purple to Cyan Gradient Glow */
        div.stPageLink > a[aria-current="page"],
        div.stPageLink > a[data-active="true"],
        a[href*="{active_kw}"] {{
            background: linear-gradient(90deg, #7C3AED 0%, #06B6D4 100%) !important;
            border: 1px solid #06B6D4 !important;
            color: #FFFFFF !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.6) !important;
        }}

        div.stPageLink > a[aria-current="page"] p,
        div.stPageLink > a[aria-current="page"] span,
        div.stPageLink > a[data-active="true"] p,
        a[href*="{active_kw}"] p,
        a[href*="{active_kw}"] span {{
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }}

        /* Custom Button Styling */
        .stButton>button {{
            background-color: #7C3AED;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.4rem 0.8rem;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }}
        .stButton>button:hover {{
            background-color: #06B6D4;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
        }}
        
        /* Premium Cards */
        .premium-card {{
            background: #111827;
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
        }}
        .premium-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.3);
        }}
        
        /* Metric Cards */
        .metric-card {{
            display: flex;
            flex-direction: column;
            background: linear-gradient(145deg, #111827, #1f2937);
            border-left: 4px solid #7C3AED;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 15px 20px -3px rgba(124, 58, 237, 0.3);
        }}
        .metric-title {{
            color: #94A3B8;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .metric-value {{
            color: #FFFFFF;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        .metric-desc {{
            color: #06B6D4;
            font-size: 0.85rem;
            font-weight: 400;
        }}
        
        /* Dataframes */
        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        /* Typography */
        h1, h2, h3, h4 {{
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }}
        h1 {{
            background: -webkit-linear-gradient(45deg, #7C3AED, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .stMarkdown, .stPlotlyChart, [data-testid="stDataFrame"] {{
            animation: fadeIn 0.4s ease-out forwards;
        }}
        
    </style>
    """, unsafe_allow_html=True)

def render_sidebar(active_kw=""):
    with st.sidebar:
        # JS Component to lock & restore sidebar scroll position and permanently highlight active page link
        js_code = """
        <script>
            (function() {
                try {
                    const parentDoc = window.parent.document;
                    function getSidebar() {
                        return parentDoc.querySelector('[data-testid="stSidebarUserContent"]') || 
                               parentDoc.querySelector('[data-testid="stSidebar"]');
                    }
                    
                    function styleAndRestore() {
                        const sidebar = getSidebar();
                        if (!sidebar) return;
                        
                        const savedScroll = window.parent.sessionStorage.getItem("st_sidebar_scroll_pos");
                        if (savedScroll !== null) {
                            sidebar.scrollTop = parseInt(savedScroll, 10);
                        }
                        
                        const allLinks = Array.from(sidebar.querySelectorAll('div.stPageLink > a, a[data-testid="stPageLink-NavLink"]'));
                        const kw = "ACTIVE_KW";
                        let activeIndex = -1;
                        if (kw === "app") activeIndex = 0;
                        else if (kw === "Dataset") activeIndex = 1;
                        else if (kw === "EDA") activeIndex = 2;
                        else if (kw === "Text_Preprocessing") activeIndex = 3;
                        else if (kw === "Text_Mining") activeIndex = 4;
                        else if (kw === "Sentiment_Analysis") activeIndex = 5;
                        else if (kw === "Machine_Learning") activeIndex = 6;
                        else if (kw === "Review_Prediction") activeIndex = 7;
                        else if (kw === "Business_Intelligence") activeIndex = 8;
                        
                        allLinks.forEach((link, idx) => {
                            const href = link.getAttribute("href") || "";
                            const isCurrent = (idx === activeIndex) || 
                                              (kw && href.includes(kw)) ||
                                              (link.getAttribute("aria-current") === "page");
                            
                            const p = link.querySelector('p') || link;
                            const span = link.querySelector('span');
                            
                            if (isCurrent) {
                                link.style.setProperty("background", "linear-gradient(90deg, #7C3AED 0%, #06B6D4 100%)", "important");
                                link.style.setProperty("border", "1px solid #06B6D4", "important");
                                link.style.setProperty("color", "#FFFFFF", "important");
                                link.style.setProperty("font-weight", "800", "important");
                                link.style.setProperty("box-shadow", "0 4px 15px rgba(124, 58, 237, 0.6)", "important");
                                if (p) { 
                                    p.style.setProperty("color", "#FFFFFF", "important"); 
                                    p.style.setProperty("font-weight", "800", "important"); 
                                }
                                if (span) { 
                                    span.style.setProperty("color", "#FFFFFF", "important"); 
                                }
                                link.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'instant' });
                            } else {
                                link.style.setProperty("background", "rgba(17, 24, 39, 0.7)", "important");
                                link.style.setProperty("border", "1px solid rgba(255, 255, 255, 0.08)", "important");
                                link.style.setProperty("color", "#94A3B8", "important");
                                link.style.setProperty("font-weight", "600", "important");
                                link.style.setProperty("box-shadow", "none", "important");
                                if (p) { 
                                    p.style.setProperty("color", "#94A3B8", "important"); 
                                    p.style.setProperty("font-weight", "600", "important"); 
                                }
                            }
                        });
                        
                        if (!sidebar.dataset.scrollBound) {
                            sidebar.dataset.scrollBound = "true";
                            sidebar.addEventListener("scroll", function() {
                                window.parent.sessionStorage.setItem("st_sidebar_scroll_pos", sidebar.scrollTop);
                            }, { passive: true });
                        }
                    }
                    
                    styleAndRestore();
                    setTimeout(styleAndRestore, 50);
                    setTimeout(styleAndRestore, 150);
                    setTimeout(styleAndRestore, 300);
                } catch(e) {}
            })();
        </script>
        """.replace("ACTIVE_KW", active_kw)
        components.html(js_code, height=0)

        # Animated Big Title
        st.markdown("""
        <div style="margin-bottom: 12px; text-align: center;">
            <div class="animated-title">ReviewMiner AI</div>
            <div style="color: #06B6D4; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.5px;">AI Powered Text Mining</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset Status Indicator Badge (Sleek & Compact)
        is_custom = data_manager.is_custom_data_active()
        ds_name = data_manager.get_dataset_name()
        current_df = data_manager.get_current_df()
        row_count = len(current_df) if current_df is not None else 0
        
        if is_custom:
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.12); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 8px; padding: 6px 10px; margin-bottom: 8px;">
                <div style="color: #06B6D4; font-size: 0.65rem; font-weight: 700;">ACTIVE DATASET</div>
                <div style="color: #FFFFFF; font-size: 0.85rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">📁 {ds_name} ({row_count:,})</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Reset Default Data", use_container_width=True):
                data_manager.reset_to_default_dataset()
                st.rerun()
        else:
            st.markdown(f"""
            <div style="background: rgba(124, 58, 237, 0.12); border: 1px solid rgba(124, 58, 237, 0.4); border-radius: 8px; padding: 6px 10px; margin-bottom: 8px;">
                <div style="color: #A78BFA; font-size: 0.65rem; font-weight: 700;">ACTIVE DATASET</div>
                <div style="color: #FFFFFF; font-size: 0.85rem; font-weight: 600;">📦 Default Reviews ({row_count:,})</div>
            </div>
            """, unsafe_allow_html=True)

        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("pages/2_Dataset.py", label="Dataset Upload & Info", icon="📂")
        st.page_link("pages/3_EDA.py", label="EDA", icon="📊")
        st.page_link("pages/4_Text_Preprocessing.py", label="Text Preprocessing", icon="🧹")
        st.page_link("pages/5_Text_Mining.py", label="Text Mining", icon="☁️")
        st.page_link("pages/6_Sentiment_Analysis.py", label="Sentiment Analysis", icon="😊")
        st.page_link("pages/7_Machine_Learning.py", label="Machine Learning", icon="🤖")
        st.page_link("pages/8_Review_Prediction.py", label="Review Prediction", icon="🔮")
        st.page_link("pages/9_Business_Intelligence.py", label="Business Intelligence", icon="📈")

def custom_metric_card(title, value, description, color="#7C3AED", icon=""):
    html = f"""
    <div class="metric-card" style="border-left-color: {color};">
        <div class="metric-title"><span>{icon}</span> {title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-desc" style="color: {color};">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def page_header(title, subtitle, icon=""):
    st.title(f"{icon} {title}")
    st.markdown(f"<p style='color: #94A3B8; font-size: 1.1rem; margin-top: -15px;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)

def apply_plotly_theme(fig):
    fig.update_layout(
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
