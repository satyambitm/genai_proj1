"""
MedReport AI — Premium Streamlit Frontend Dashboard.

A polished, product-grade medical report analyzer UI with
medical-themed design, data visualizations, and cool output displays.
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ── Page Config ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MedReport AI — Medical Report Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium Medical-Themed CSS ─────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ── Global Reset ────────────────────────── */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(160deg, #0a0e27 0%, #0d1b3e 25%, #0f2847 50%, #0a1628 75%, #060b1a 100%);
        color: #e0e6ed;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* ── Medical Background Pattern ─────────── */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            radial-gradient(circle at 15% 25%, rgba(0, 210, 190, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 85% 75%, rgba(56, 130, 246, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 50% 10%, rgba(139, 92, 246, 0.03) 0%, transparent 40%),
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M28 2h4v16h-4zM28 42h4v16h-4zM2 28h16v4H2zM42 28h16v4H42z' fill='rgba(0,210,190,0.015)' fill-rule='evenodd'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
    }

    /* ── Hero Section ────────────────────────── */
    .hero-container {
        position: relative;
        background: linear-gradient(135deg, rgba(0, 210, 190, 0.12) 0%, rgba(56, 130, 246, 0.08) 50%, rgba(139, 92, 246, 0.06) 100%);
        border: 1px solid rgba(0, 210, 190, 0.2);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(0, 210, 190, 0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-container::after {
        content: '✚';
        position: absolute;
        top: 20px;
        right: 40px;
        font-size: 120px;
        opacity: 0.03;
        color: #00d2be;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00d2be, #3882f6);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #00d2be 50%, #3882f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.7rem 0;
        line-height: 1.15;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(224, 230, 237, 0.7);
        max-width: 650px;
        line-height: 1.6;
    }

    /* ── Disclaimer ──────────────────────────── */
    .medical-disclaimer {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-left: 4px solid #f59e0b;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.3rem;
        margin-bottom: 2rem;
        font-size: 0.85rem;
        color: #fbbf24;
        backdrop-filter: blur(10px);
    }

    /* ── Glass Cards ─────────────────────────── */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0, 210, 190, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 210, 190, 0.3);
        box-shadow: 0 8px 32px rgba(0, 210, 190, 0.08);
        transform: translateY(-2px);
    }
    .glass-card-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #00d2be;
        margin-bottom: 0.8rem;
    }

    /* ── Stat Cards ──────────────────────────── */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 130, 246, 0.15);
        border-radius: 16px;
        padding: 1.4rem;
        text-align: center;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d2be, #3882f6);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .stat-card:hover::before { opacity: 1; }
    .stat-card:hover {
        border-color: rgba(56, 130, 246, 0.35);
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(56, 130, 246, 0.1);
    }
    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.4rem;
    }
    .stat-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d2be, #3882f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .stat-label {
        font-size: 0.78rem;
        color: rgba(224, 230, 237, 0.5);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }

    /* ── Severity Badges ─────────────────────── */
    .badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-normal { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-low { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-medium { background: rgba(249, 115, 22, 0.15); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.3); }
    .badge-high { background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-critical { background: rgba(239, 68, 68, 0.25); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.5); animation: pulse-critical 2s infinite; }

    @keyframes pulse-critical {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.3); }
        50% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
    }

    /* ── Finding Cards ───────────────────────── */
    .finding-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .finding-card:hover {
        background: rgba(15, 23, 42, 0.7);
        border-color: rgba(0, 210, 190, 0.2);
    }
    .finding-card.abnormal {
        border-left: 3px solid #ef4444;
    }
    .finding-param {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.4rem;
    }
    .finding-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d2be;
    }
    .finding-meta {
        font-size: 0.82rem;
        color: rgba(224, 230, 237, 0.45);
        margin-top: 0.3rem;
    }

    /* ── Question Cards ──────────────────────── */
    .question-card {
        background: rgba(56, 130, 246, 0.06);
        border: 1px solid rgba(56, 130, 246, 0.15);
        border-left: 3px solid #3882f6;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin-bottom: 0.6rem;
        font-size: 0.92rem;
        color: #93c5fd;
        transition: all 0.3s ease;
    }
    .question-card:hover {
        background: rgba(56, 130, 246, 0.1);
        transform: translateX(4px);
    }

    /* ── Upload Area ─────────────────────────── */
    .upload-zone {
        background: rgba(0, 210, 190, 0.04);
        border: 2px dashed rgba(0, 210, 190, 0.2);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    .upload-zone:hover {
        border-color: rgba(0, 210, 190, 0.4);
        background: rgba(0, 210, 190, 0.06);
    }
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 0.8rem;
    }
    .upload-text {
        color: rgba(224, 230, 237, 0.6);
        font-size: 0.9rem;
    }

    /* ── Section Headers ─────────────────────── */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 1.8rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .section-header-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(0, 210, 190, 0.3), transparent);
    }

    /* ── Medical Term Pills ──────────────────── */
    .term-pill {
        display: inline-block;
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        color: #c4b5fd;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
        transition: all 0.2s ease;
    }
    .term-pill:hover {
        background: rgba(139, 92, 246, 0.2);
        transform: scale(1.05);
    }

    /* ── Abnormality Alert Card ──────────────── */
    .alert-card {
        background: rgba(239, 68, 68, 0.06);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .alert-card:hover {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.3);
    }
    .alert-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: #fca5a5;
        margin-bottom: 0.4rem;
    }
    .alert-body {
        font-size: 0.88rem;
        color: rgba(224, 230, 237, 0.65);
        line-height: 1.5;
    }
    .alert-rec {
        font-size: 0.82rem;
        color: rgba(251, 191, 36, 0.8);
        font-style: italic;
        margin-top: 0.4rem;
    }

    /* ── Summary Card ────────────────────────── */
    .summary-card {
        background: linear-gradient(135deg, rgba(0, 210, 190, 0.06), rgba(56, 130, 246, 0.04));
        border: 1px solid rgba(0, 210, 190, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        font-size: 1rem;
        line-height: 1.7;
        color: rgba(224, 230, 237, 0.85);
    }

    /* ── Progress Shimmer ────────────────────── */
    .shimmer {
        background: linear-gradient(90deg, rgba(0,210,190,0.05) 25%, rgba(0,210,190,0.15) 50%, rgba(0,210,190,0.05) 75%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
        border-radius: 12px;
        height: 20px;
        margin-bottom: 0.5rem;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }

    /* ── Sidebar Styling ─────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #0d1b3e 100%);
        border-right: 1px solid rgba(0, 210, 190, 0.1);
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e6ed;
    }

    /* ── Streamlit overrides ─────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #00d2be 0%, #3882f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 210, 190, 0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0, 210, 190, 0.35) !important;
    }

    .stFileUploader {
        background: rgba(0, 210, 190, 0.04) !important;
        border: 2px dashed rgba(0, 210, 190, 0.2) !important;
        border-radius: 16px !important;
    }

    .stExpander {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(224, 230, 237, 0.6);
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 210, 190, 0.15) !important;
        color: #00d2be !important;
    }

    /* Fix text color in dark mode */
    .stMarkdown, .stText, p, span, li {
        color: #e0e6ed;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }

    /* Plotly chart containers */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Divider */
    .neon-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 210, 190, 0.3), rgba(56, 130, 246, 0.3), transparent);
        margin: 2rem 0;
    }

    /* Pulse dot for live status */
    .pulse-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00d2be;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0,210,190,0.4); }
        50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(0,210,190,0); }
    }
</style>
""", unsafe_allow_html=True)

# ── API Config ─────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000/api"
SEVERITY_COLORS = {
    "normal": "#10b981",
    "low": "#f59e0b",
    "medium": "#f97316",
    "high": "#ef4444",
    "critical": "#dc2626",
}
SEVERITY_ICONS = {
    "normal": "✅",
    "low": "⚠️",
    "medium": "🟠",
    "high": "🔴",
    "critical": "🚨",
}


# ── Helper Functions ───────────────────────────────────────────────────

def create_severity_gauge(normal_count: int, abnormal_count: int, total: int):
    """Create a radial gauge chart showing health score."""
    if total == 0:
        score = 100
    else:
        score = int((normal_count / total) * 100)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={"text": "Health Score", "font": {"size": 16, "color": "#e0e6ed"}},
        number={"suffix": "%", "font": {"size": 40, "color": "#00d2be"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#1e293b"},
            "bar": {"color": "#00d2be", "thickness": 0.3},
            "bgcolor": "rgba(15,23,42,0.5)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.15)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.15)"},
                {"range": [70, 100], "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#f87171", "width": 3},
                "thickness": 0.8,
                "value": 50,
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=30, r=30, t=50, b=10),
        font={"color": "#e0e6ed"},
    )
    return fig


def create_severity_donut(findings: list):
    """Create a donut chart showing severity distribution."""
    severity_counts = {"Normal": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    for f in findings:
        s = f.get("status", "normal").capitalize()
        if s in severity_counts:
            severity_counts[s] += 1

    labels = [k for k, v in severity_counts.items() if v > 0]
    values = [v for v in severity_counts.values() if v > 0]
    colors_map = {"Normal": "#10b981", "Low": "#f59e0b", "Medium": "#f97316", "High": "#ef4444", "Critical": "#dc2626"}
    colors = [colors_map.get(l, "#64748b") for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color="#0a0e27", width=3)),
        textfont=dict(color="#e0e6ed", size=12),
        hoverinfo="label+value+percent",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(font=dict(color="#e0e6ed", size=11), bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text="Status", x=0.5, y=0.5, font_size=14, font_color="#64748b", showarrow=False)],
    )
    return fig


def create_findings_bar(findings: list):
    """Create a horizontal bar chart of findings with color-coded severity."""
    if not findings:
        return None

    params = [f.get("parameter", "?")[:20] for f in findings]
    statuses = [f.get("status", "normal") for f in findings]
    colors = [SEVERITY_COLORS.get(s, "#64748b") for s in statuses]

    fig = go.Figure(go.Bar(
        y=params,
        x=[1] * len(params),
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[s.upper() for s in statuses],
        textposition="inside",
        textfont=dict(color="white", size=11, family="Space Grotesk"),
        hovertext=[f"{p}: {f.get('value', 'N/A')} {f.get('unit', '')}" for p, f in zip(params, findings)],
        hoverinfo="text",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=max(200, len(params) * 38),
        margin=dict(l=0, r=20, t=10, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(
            tickfont=dict(color="#e0e6ed", size=11, family="Space Grotesk"),
            autorange="reversed",
        ),
        bargap=0.3,
    )
    return fig


# ── Sidebar ────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 1.5rem 0;">
        <div style="font-size: 2.5rem;">🏥</div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 700;
            background: linear-gradient(135deg, #00d2be, #3882f6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            MedReport AI
        </div>
        <div style="font-size: 0.75rem; color: rgba(224,230,237,0.4); letter-spacing: 2px; text-transform: uppercase;">
            Medical Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    api_url = st.text_input("🔗 Backend API URL", value="http://localhost:8000", help="FastAPI server URL")
    API_BASE_URL = f"{api_url}/api"

    st.markdown("---")

    st.markdown("""
    <div class="glass-card" style="padding: 1rem;">
        <div class="glass-card-header">⚡ How It Works</div>
        <div style="font-size: 0.85rem; color: rgba(224,230,237,0.6); line-height: 1.7;">
            <strong style="color: #00d2be;">01.</strong> Upload a medical report<br>
            <strong style="color: #3882f6;">02.</strong> AI extracts key findings<br>
            <strong style="color: #8b5cf6;">03.</strong> Get simplified explanations<br>
            <strong style="color: #f59e0b;">04.</strong> View flagged abnormalities<br>
            <strong style="color: #ef4444;">05.</strong> Ask follow-up questions
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("**📂 Supported Formats**")
    st.caption("📄 PDF  ·  🖼️ PNG/JPG  ·  📝 TXT")
    st.markdown(f"<span style='font-size:0.75rem; color:rgba(224,230,237,0.3);'>Max size: 10MB</span>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("**🕐 Report History**")
    if "history" in st.session_state and st.session_state.history:
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"""
            <div style="background: rgba(0,210,190,0.04); border: 1px solid rgba(0,210,190,0.1);
                border-radius: 10px; padding: 0.6rem; margin-bottom: 0.5rem; font-size: 0.82rem;">
                <div style="color: #00d2be; font-weight: 600;">📄 {item['filename']}</div>
                <div style="color: rgba(224,230,237,0.4); font-size: 0.75rem;">
                    {item.get('report_type', 'N/A').replace('_',' ').title()} · {item.get('findings_count', 0)} findings
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No reports analyzed yet.")


# ── Session State ──────────────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = []


# ── Hero Section ───────────────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">🤖 Powered by GPT-4 Vision</div>
    <div class="hero-title">Medical Report<br>Analyzer & Simplifier</div>
    <div class="hero-subtitle">
        Upload your medical reports and get instant AI-powered analysis.
        Understand your results in simple language, see flagged abnormalities,
        and get follow-up questions for your doctor.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="medical-disclaimer">
    ⚠️ <strong>Medical Disclaimer:</strong> This tool provides AI-generated analysis for <strong>informational purposes only</strong>.
    It is NOT a substitute for professional medical advice. Always consult a qualified healthcare provider.
</div>
""", unsafe_allow_html=True)


# ── Upload Section ─────────────────────────────────────────────────────

st.markdown("""
<div class="section-header">
    📤 Upload Report
    <div class="section-header-line"></div>
</div>
""", unsafe_allow_html=True)

col_up, col_tip = st.columns([3, 1])

with col_up:
    uploaded_file = st.file_uploader(
        "Upload your medical report",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        help="Supported formats: PDF, PNG, JPG, JPEG, TXT (max 10MB)",
        label_visibility="collapsed",
    )

with col_tip:
    st.markdown("""
    <div class="glass-card" style="padding: 1rem;">
        <div class="glass-card-header">💡 Tips</div>
        <div style="font-size: 0.82rem; color: rgba(224,230,237,0.55); line-height: 1.6;">
            • Use clear, readable reports<br>
            • High-res scans work best<br>
            • Crop unnecessary margins
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Analysis Pipeline ─────────────────────────────────────────────────

if uploaded_file is not None:
    file_size_kb = uploaded_file.size / 1024
    st.markdown(f"""
    <div class="glass-card" style="display:flex; align-items:center; gap:1rem; padding:1rem 1.5rem;">
        <div style="font-size:2rem;">📄</div>
        <div>
            <div style="font-weight:600; color:#f1f5f9;">{uploaded_file.name}</div>
            <div style="font-size:0.82rem; color:rgba(224,230,237,0.45);">{file_size_kb:.1f} KB · {uploaded_file.type}</div>
        </div>
        <div style="margin-left:auto;">
            <span class="pulse-dot"></span>
            <span style="font-size:0.82rem; color:#00d2be;">Ready to analyze</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    analyze_btn = st.button("🔬  Analyze Report", type="primary", use_container_width=True)

    if analyze_btn:
        # ── Step 1: Upload ─────────────────────────────────────────
        progress_bar = st.progress(0, text="📤 Uploading report...")
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            upload_resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)

            if upload_resp.status_code != 200:
                st.error(f"❌ Upload failed: {upload_resp.json().get('detail', 'Unknown error')}")
                st.stop()

            upload_data = upload_resp.json()
            file_id = upload_data["file_id"]
            progress_bar.progress(33, text="✅ Uploaded! Analyzing with AI...")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend API. Make sure the server is running.")
            st.code("uvicorn app.main:app --reload --port 8000", language="bash")
            st.stop()
        except Exception as e:
            st.error(f"❌ Upload error: {str(e)}")
            st.stop()

        # ── Step 2: Analyze ────────────────────────────────────────
        try:
            analyze_resp = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"file_id": file_id, "filename": uploaded_file.name},
                timeout=120,
            )

            if analyze_resp.status_code != 200:
                st.error(f"❌ Analysis failed: {analyze_resp.json().get('detail', 'Unknown error')}")
                st.stop()

            analysis_data = analyze_resp.json()
            progress_bar.progress(66, text="🧠 Analysis complete! Simplifying...")

        except Exception as e:
            st.error(f"❌ Analysis error: {str(e)}")
            st.stop()

        # ── Step 3: Simplify ───────────────────────────────────────
        try:
            simplify_resp = requests.post(
                f"{API_BASE_URL}/simplify",
                json={
                    "file_id": file_id,
                    "summary": analysis_data["summary"],
                    "findings": analysis_data["findings"],
                },
                timeout=120,
            )
            simplified_data = simplify_resp.json() if simplify_resp.status_code == 200 else None
        except Exception:
            simplified_data = None

        progress_bar.progress(100, text="✨ Analysis complete!")

        # ── Save to history ────────────────────────────────────────
        st.session_state.history.append({
            "filename": uploaded_file.name,
            "file_id": file_id,
            "report_type": analysis_data.get("report_type", "N/A"),
            "findings_count": len(analysis_data.get("findings", [])),
        })

        # ══════════════════════════════════════════════════════════════
        # ══  RESULTS DISPLAY  ═══════════════════════════════════════
        # ══════════════════════════════════════════════════════════════

        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            📊 Analysis Results
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        findings = analysis_data.get("findings", [])
        normal_count = sum(1 for f in findings if f.get("status", "normal") == "normal")
        abnormal_count = len(findings) - normal_count

        # ── Stats Row (Plotly Gauge + Donut + Stat Cards) ──────────
        gauge_col, donut_col, stats_col = st.columns([1.2, 1, 1.3])

        with gauge_col:
            st.plotly_chart(
                create_severity_gauge(normal_count, abnormal_count, len(findings)),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with donut_col:
            st.plotly_chart(
                create_severity_donut(findings),
                use_container_width=True,
                config={"displayModeBar": False},
            )

        with stats_col:
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; height: 100%;">
                <div class="stat-card">
                    <div class="stat-icon">🔬</div>
                    <div class="stat-value">{len(findings)}</div>
                    <div class="stat-label">Findings</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">{"🚨" if abnormal_count > 0 else "✅"}</div>
                    <div class="stat-value" style="{'background: linear-gradient(135deg, #ef4444, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;' if abnormal_count > 0 else ''}">{abnormal_count}</div>
                    <div class="stat-label">Abnormal</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📋</div>
                    <div class="stat-value" style="font-size: 1rem;">{analysis_data.get('report_type', 'N/A').replace('_', ' ').title()}</div>
                    <div class="stat-label">Type</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📖</div>
                    <div class="stat-value">{len(analysis_data.get('medical_terms', []))}</div>
                    <div class="stat-label">Terms</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # ── Tabbed Results ─────────────────────────────────────────
        tab_summary, tab_findings, tab_alerts, tab_questions = st.tabs([
            "📋 Summary", "🔬 Detailed Findings", "🚩 Abnormalities", "💡 Follow-Up Questions"
        ])

        with tab_summary:
            col_s1, col_s2 = st.columns([1, 1])

            with col_s1:
                st.markdown("#### 🧠 AI Analysis")
                st.markdown(f"""<div class="summary-card">{analysis_data.get('summary', 'N/A')}</div>""", unsafe_allow_html=True)

            with col_s2:
                if simplified_data:
                    st.markdown("#### 💬 Simplified for You")
                    st.markdown(f"""<div class="summary-card">{simplified_data.get('simplified_summary', 'N/A')}</div>""", unsafe_allow_html=True)

            # Medical Terms
            if analysis_data.get("medical_terms"):
                st.markdown("")
                st.markdown("#### 📖 Medical Terms Detected")
                terms_html = " ".join([f'<span class="term-pill">{t}</span>' for t in analysis_data["medical_terms"]])
                st.markdown(terms_html, unsafe_allow_html=True)

        with tab_findings:
            if findings:
                # Bar chart visualization
                bar_fig = create_findings_bar(findings)
                if bar_fig:
                    st.markdown("#### Status Overview")
                    st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

                st.markdown("")
                st.markdown("#### All Findings")

                for f in findings:
                    severity = f.get("status", "normal")
                    icon = SEVERITY_ICONS.get(severity, "ℹ️")
                    is_abnormal = severity != "normal"
                    card_class = "finding-card abnormal" if is_abnormal else "finding-card"

                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div class="finding-param">{icon} {f['parameter']}</div>
                                <div class="finding-value">{f['value']} <span style="font-size: 0.85rem; color: rgba(224,230,237,0.4);">{f.get('unit', '')}</span></div>
                            </div>
                            <span class="badge badge-{severity}">{severity.upper()}</span>
                        </div>
                        <div class="finding-meta">
                            📏 Reference: {f.get('reference_range', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp;
                            💬 {f.get('interpretation', 'N/A')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No findings extracted from the report.")

        with tab_alerts:
            if simplified_data and simplified_data.get("abnormalities"):
                non_normal = [ab for ab in simplified_data["abnormalities"] if ab.get("severity", "normal") != "normal"]
                if non_normal:
                    for ab in non_normal:
                        severity = ab.get("severity", "normal")
                        st.markdown(f"""
                        <div class="alert-card">
                            <div class="alert-title">
                                {SEVERITY_ICONS.get(severity, '⚠️')} {ab['parameter']}:
                                <strong>{ab['value']}</strong>
                                <span class="badge badge-{severity}" style="margin-left: 8px;">{severity.upper()}</span>
                            </div>
                            <div class="alert-body">{ab.get('explanation', '')}</div>
                            <div class="alert-rec">💡 {ab.get('recommendation', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="glass-card" style="text-align: center; padding: 2rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.5rem;">✅</div>
                        <div style="font-size: 1.1rem; color: #34d399; font-weight: 600;">All Clear!</div>
                        <div style="color: rgba(224,230,237,0.5); font-size: 0.9rem;">No significant abnormalities detected.</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Abnormality data not available. Please try analyzing the report again.")

        with tab_questions:
            if simplified_data and simplified_data.get("followup_questions"):
                st.markdown("**Ask your doctor these questions at your next visit:**")
                st.markdown("")
                for i, q in enumerate(simplified_data["followup_questions"], 1):
                    st.markdown(f"""
                    <div class="question-card">
                        <span style="color: #3882f6; font-weight: 700; margin-right: 8px;">Q{i}.</span> {q}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Follow-up questions not available.")

        # ── Final Disclaimer ───────────────────────────────────────
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

        disclaimer_text = simplified_data.get("disclaimer", "") if simplified_data else ""
        if not disclaimer_text:
            disclaimer_text = (
                "⚠️ This AI-generated analysis is for informational purposes only. "
                "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
                "Always consult a qualified healthcare provider for medical decisions."
            )
        st.markdown(f'<div class="medical-disclaimer">{disclaimer_text}</div>', unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem; color: rgba(224,230,237,0.2); font-size: 0.78rem;">
            MedReport AI v1.0 · Powered by OpenAI GPT-4 · Built with FastAPI & Streamlit<br>
            Analysis generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </div>
        """, unsafe_allow_html=True)
