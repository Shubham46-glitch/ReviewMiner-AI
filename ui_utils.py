import streamlit as st

def setup_page(title, subtitle, icon=""):
    st.set_page_config(page_title=title, layout="wide", page_icon=icon, initial_sidebar_state="expanded")
    apply_custom_theme()
    render_sidebar()
    page_header(title, subtitle, icon)

def apply_custom_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stSidebarNav"] {display: none;}
        
        /* Global Background */
        .stApp {
            background-color: #0B1220;
            color: #FFFFFF;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
            border-right: 1px solid rgba(124, 58, 237, 0.15);
        }
        
        /* Animated Title CSS */
        .animated-title {
            font-size: 2.3rem !important;
            font-weight: 900 !important;
            background: linear-gradient(270deg, #7C3AED, #06B6D4, #22C55E, #7C3AED);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 4s ease infinite;
            margin-bottom: 5px;
            text-align: left;
            line-height: 1.2;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* FORCE Sidebar Page Links to look like buttons (Targeting every possible wrapper) */
        div.stPageLink > a,
        a[data-testid="stPageLink-NavLink"],
        [data-testid="stSidebar"] a[href] {
            background: linear-gradient(145deg, #1f2937, #111827) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 12px 15px !important;
            margin-bottom: 12px !important;
            display: flex !important;
            align-items: center !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
            text-decoration: none !important;
            color: #FFFFFF !important;
        }
        
        div.stPageLink > a:hover,
        a[data-testid="stPageLink-NavLink"]:hover,
        [data-testid="stSidebar"] a[href]:hover {
            background: linear-gradient(90deg, #7C3AED, #06B6D4) !important;
            border-color: transparent !important;
            transform: translateX(8px) scale(1.02) !important;
            box-shadow: 0 10px 20px rgba(124, 58, 237, 0.5) !important;
            color: #FFFFFF !important;
        }
        
        /* Fix text elements inside links */
        div.stPageLink p,
        a[data-testid="stPageLink-NavLink"] p,
        a[data-testid="stPageLink-NavLink"] span {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin: 0 !important;
            padding: 0 !important;
            color: #FFFFFF !important;
        }
        
        /* Custom Button Styling */
        .stButton>button {
            background-color: #7C3AED;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #06B6D4;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
        }
        
        /* Premium Cards */
        .premium-card {
            background: #111827;
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
        }
        .premium-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(124, 58, 237, 0.3);
        }
        
        /* Metric Cards */
        .metric-card {
            display: flex;
            flex-direction: column;
            background: linear-gradient(145deg, #111827, #1f2937);
            border-left: 4px solid #7C3AED;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 15px 20px -3px rgba(124, 58, 237, 0.3);
        }
        .metric-title {
            color: #94A3B8;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .metric-value {
            color: #FFFFFF;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .metric-desc {
            color: #06B6D4;
            font-size: 0.85rem;
            font-weight: 400;
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Typography */
        h1, h2, h3, h4 {
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        h1 {
            background: -webkit-linear-gradient(45deg, #7C3AED, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stMarkdown, .stPlotlyChart, [data-testid="stDataFrame"] {
            animation: fadeIn 0.6s ease-out forwards;
        }
        
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        # Animated Big Title
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div class="animated-title">ReviewMiner AI</div>
            <div style="color: #06B6D4; font-size: 1rem; font-weight: 700; letter-spacing: 1px;">AI Powered Text Mining</div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("pages/2_Dataset.py", label="Dataset", icon="📂")
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
