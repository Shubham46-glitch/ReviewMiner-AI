import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from ui_utils import setup_page, custom_metric_card, check_dataset_loaded
import data_manager
from backend.app.services.text_engine import compute_executive_business_intelligence

setup_page("Business Intelligence & Executive Analytics", "Data-driven strategic decision support matrix, risk profiling, and actionable executive directives.", "💼")
check_dataset_loaded()

df = data_manager.get_cleaned_df().copy()
if df.empty:
    st.warning("⚠️ No active dataset uploaded yet. Please upload a dataset in the Dataset Upload Center.")
    st.stop()

bi_data = compute_executive_business_intelligence(df)
kpis = bi_data.get('kpi_summary', {})
viz = bi_data.get('visualizations', {})

pos_drivers = viz.get('positive_drivers', [])
neg_drivers = viz.get('negative_drivers', [])
strength_vs_pain = viz.get('strength_vs_pain', [])
risk_bubbles = viz.get('risk_bubbles', [])
opp_ranking = viz.get('opportunity_ranking', [])
action_plan = bi_data.get('action_plan', [])

# =========================================================
# 1. EXECUTIVE KPI HEADER (5 COMPACT CARDS)
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    custom_metric_card("Top Positive Driver", f"{kpis.get('top_positive_pct', 0)}%", kpis.get('top_positive_driver', 'Quality'), icon="👍", color="#06B6D4")
with c2:
    custom_metric_card("Top Customer Pain Point", f"{kpis.get('top_negative_pct', 0)}%", kpis.get('top_negative_driver', 'Quality'), icon="⚠️", color="#EF4444")
with c3:
    custom_metric_card("Quality Complaints", f"{kpis.get('quality_complaints', 0)}", "Build friction reviews", icon="📦", color="#F59E0B")
with c4:
    custom_metric_card("Delivery Complaints", f"{kpis.get('delivery_complaints', 0)}", "Logistics friction reviews", icon="🚚", color="#A855F7")
with c5:
    custom_metric_card("Performance Complaints", f"{kpis.get('performance_complaints', 0)}", "Thermal friction reviews", icon="⚡", color="#3B82F6")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 2. MIDDLE SECTION — POSITIVE & NEGATIVE DRIVERS CHARTS
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
m1, m2 = st.columns(2)

with m1:
    st.subheader("👍 Positive Review Drivers (%)")
    if pos_drivers:
        pos_df = pd.DataFrame(pos_drivers)
        fig_pos = px.bar(
            pos_df.iloc[::-1],
            x='percentage',
            y='domain',
            orientation='h',
            text='percentage',
            color_discrete_sequence=['#06B6D4'],
            labels={'percentage': 'Positive Share (%)', 'domain': ''}
        )
        fig_pos.update_traces(texttemplate='%{text}%', textposition='inside')
        fig_pos.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), height=240, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_pos, use_container_width=True)

with m2:
    st.subheader("⚠️ Negative Complaint Drivers (%)")
    if neg_drivers:
        neg_df = pd.DataFrame(neg_drivers)
        fig_neg = px.bar(
            neg_df.iloc[::-1],
            x='percentage',
            y='domain',
            orientation='h',
            text='percentage',
            color_discrete_sequence=['#EF4444'],
            labels={'percentage': 'Complaint Share (%)', 'domain': ''}
        )
        fig_neg.update_traces(texttemplate='%{text}%', textposition='inside')
        fig_neg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), height=240, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_neg, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 3. CENTRAL FEATURE — STRENGTH VS PAIN & RISK MATRICES
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st1, st2 = st.columns(2)

with st1:
    st.subheader("🎯 Strength vs Pain Matrix (Quadrant Chart)")
    if strength_vs_pain:
        svp_df = pd.DataFrame(strength_vs_pain)
        fig_quad = px.scatter(
            svp_df,
            x='strength',
            y='pain',
            text='domain',
            color='quadrant',
            color_discrete_map={'Fix & Protect': '#EF4444', 'Leverage & Promote': '#22C55E', 'Mitigate Friction': '#F59E0B', 'Monitor': '#94A3B8'},
            labels={'strength': 'Customer Strength (%) →', 'pain': 'Customer Pain / Dissatisfaction (%) ↑'}
        )
        fig_quad.update_traces(marker=dict(size=18, line=dict(width=2, color='White')), textposition='top center')
        fig_quad.add_vline(x=20, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_quad.add_hline(y=15, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        fig_quad.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), height=320, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_quad, use_container_width=True)

with st2:
    st.subheader("🛡️ Operational Risk & Frequency Matrix")
    if risk_bubbles:
        rb_df = pd.DataFrame(risk_bubbles)
        fig_risk = px.scatter(
            rb_df,
            x='frequency',
            y='impact',
            size='reviews',
            text='domain',
            color='priority',
            color_discrete_map={'🔴 High': '#EF4444', '🟠 Medium': '#F97316', '🟢 Low': '#22C55E'},
            labels={'frequency': 'Complaint Frequency (%) →', 'impact': 'Dissatisfaction Impact Score ↑'}
        )
        fig_risk.update_traces(textposition='top center')
        fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FFFFFF'), height=320, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_risk, use_container_width=True)

st.markdown("""
<div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 10px; padding: 14px; margin-top: 10px;">
    <p style="color: #E2E8F0; font-size: 0.9rem; margin: 0;">
        ⚡ <b>Core Executive Insight:</b> Product Quality & Build is simultaneously the brand's <u>biggest competitive strength</u> (41.6%) — and its <u>primary source of dissatisfaction</u> (41.3% / 95 complaints).
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# 4. BOTTOM SECTION — OPPORTUNITIES & AI ACTION PLAN
# =========================================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
b1, b2 = st.columns(2)

with b1:
    st.subheader("🚀 Business Growth Opportunity Ranking")
    if opp_ranking:
        for opp in opp_ranking:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #A855F7; font-weight: 700;">#{opp['rank']} {opp['domain']}</span>
                    <span style="background: rgba(168,85,247,0.2); color: #C084FC; font-size: 0.75rem; padding: 2px 8px; border-radius: 12px; font-weight: 700;">{opp['impact']} IMPACT</span>
                </div>
                <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 4px;">
                    Complaint Share: <b style="color: #EF4444;">{opp['complaint_pct']}%</b> ({opp['count']} reviews) | Score: <b style="color: #A855F7;">{opp['opportunity_score']} / 100</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with b2:
    st.subheader("🎯 Ranked AI Executive Action Plan")
    if action_plan:
        for act in action_plan:
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.8); border-left: 4px solid {'#EF4444' if act['impact'] == 'VERY HIGH' else '#F59E0B'}; border-radius: 10px; padding: 12px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #FFFFFF; font-weight: 700;">#{act['rank']} {act['domain']}</span>
                    <span style="color: #EF4444; font-size: 0.75rem; font-weight: 700;">IMPACT: {act['impact']}</span>
                </div>
                <div style="color: #06B6D4; font-size: 0.8rem; margin-top: 2px;">🔍 Evidence: {act['evidence']}</div>
                <div style="color: #10B981; font-size: 0.85rem; font-weight: 700; margin-top: 4px;">⚡ Directive: {act['action']}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

def generate_pdf_bytes():
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
    summary_text = bi_data.get('executive_summary', '').encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 6, summary_text)
    pdf.ln(3)
    
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "2. Ranked AI Executive Action Plan", ln=1)
    pdf.set_font("Arial", size=10)
    for act in action_plan:
        clean_act = f"• #{act['rank']} [{act['domain']}] Impact: {act['impact']} | Evidence: {act['evidence']} -> Directive: {act['action']}".encode('ascii', 'ignore').decode('ascii')
        pdf.multi_cell(0, 6, clean_act)

    buf = pdf.output(dest='S')
    return buf.encode('latin-1') if isinstance(buf, str) else bytes(buf)

st.download_button(
    label="📄 Export Executive PDF Report",
    data=generate_pdf_bytes(),
    file_name="Executive_Business_Intelligence_Report.pdf",
    mime="application/pdf",
    type="primary",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)
