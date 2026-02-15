"""
MedReport AI — Product-Grade Medical Report Analyzer Frontend.

A polished, product-ready website with premium medical UI,
dedicated abnormality alerts with red severity markers,
and interactive data visualizations.
"""

import streamlit as st
import requests
import json
import plotly.graph_objects as go
from datetime import datetime

# ── Page Config ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MedReport AI | AI-Powered Medical Report Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
# ══  PREMIUM PRODUCT CSS  ════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Global ──────────────────────────────── */
    * { box-sizing: border-box; }
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #060918;
        color: #c8d6e5;
    }
    #MainMenu, footer, header, .stDeployButton { display: none !important; }

    /* ── Animated background ─────────────────── */
    .stApp::before {
        content: '';
        position: fixed; top: 0; left: 0;
        width: 100%; height: 100%;
        background:
            radial-gradient(ellipse at 10% 20%, rgba(0,210,190,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(56,130,246,0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 0%, rgba(139,92,246,0.04) 0%, transparent 40%),
            url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M36 4h8v24h-8zM36 52h8v24h-8zM4 36h24v8H4zM52 36h24v8H52z' fill='rgba(0,210,190,0.012)' fill-rule='evenodd'/%3E%3C/svg%3E");
        pointer-events: none; z-index: 0;
    }

    /* ── Top Navigation Bar ──────────────────── */
    .topnav {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 0; margin-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0,210,190,0.08);
    }
    .topnav-brand {
        display: flex; align-items: center; gap: 0.8rem;
    }
    .topnav-logo {
        width: 42px; height: 42px; border-radius: 12px;
        background: linear-gradient(135deg, #00d2be, #3882f6);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; color: white; font-weight: 700;
    }
    .topnav-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem; font-weight: 700;
        background: linear-gradient(135deg, #00d2be, #3882f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .topnav-tagline {
        font-size: 0.7rem; color: rgba(200,214,229,0.35);
        letter-spacing: 2px; text-transform: uppercase;
    }
    .topnav-links {
        display: flex; gap: 1.5rem; align-items: center;
    }
    .topnav-link {
        font-size: 0.85rem; color: rgba(200,214,229,0.5);
        text-decoration: none; transition: color 0.2s;
        cursor: default;
    }
    .topnav-link:hover { color: #00d2be; }
    .topnav-cta {
        background: linear-gradient(135deg, #00d2be, #3882f6);
        color: white !important; padding: 8px 20px;
        border-radius: 10px; font-weight: 600; font-size: 0.82rem;
        text-decoration: none; transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,210,190,0.2);
    }
    .topnav-cta:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 25px rgba(0,210,190,0.35);
    }

    /* ── Hero Section ────────────────────────── */
    .hero {
        position: relative; text-align: center;
        padding: 3.5rem 2rem 2.5rem;
        background: linear-gradient(160deg, rgba(0,210,190,0.08) 0%, rgba(56,130,246,0.04) 50%, rgba(6,9,24,0) 100%);
        border: 1px solid rgba(0,210,190,0.08);
        border-radius: 28px; margin-bottom: 2.5rem;
        overflow: hidden;
    }
    .hero::before {
        content: ''; position: absolute; top: -100px; right: -50px;
        width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(0,210,190,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero::after {
        content: '✚'; position: absolute; bottom: 20px; left: 40px;
        font-size: 160px; opacity: 0.015; color: #00d2be;
    }
    .hero-pill {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(0,210,190,0.1); border: 1px solid rgba(0,210,190,0.2);
        padding: 6px 16px; border-radius: 30px;
        font-size: 0.78rem; font-weight: 600; color: #00d2be;
        letter-spacing: 0.5px; margin-bottom: 1.5rem;
    }
    .hero-pill-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #00d2be; animation: blink 2s infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; } 50% { opacity: 0.3; }
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem; font-weight: 800; line-height: 1.1;
        letter-spacing: -1.5px; margin: 0 0 1rem 0;
        background: linear-gradient(135deg, #ffffff 20%, #00d2be 60%, #3882f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p {
        font-size: 1.1rem; color: rgba(200,214,229,0.55);
        max-width: 600px; margin: 0 auto; line-height: 1.7;
    }

    /* ── Feature Cards Row ───────────────────── */
    .features-row {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 1rem; margin-bottom: 2.5rem;
    }
    .feature-card {
        background: rgba(12,18,40,0.6);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px; padding: 1.3rem; text-align: center;
        transition: all 0.3s ease; backdrop-filter: blur(10px);
        position: relative; overflow: hidden;
    }
    .feature-card::after {
        content: ''; position: absolute; bottom: 0; left: 0; right: 0;
        height: 2px; background: linear-gradient(90deg, var(--fc-color, #00d2be), transparent);
        opacity: 0; transition: opacity 0.3s;
    }
    .feature-card:hover { border-color: rgba(0,210,190,0.15); transform: translateY(-3px); }
    .feature-card:hover::after { opacity: 1; }
    .feature-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }
    .feature-title { font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 0.3rem; }
    .feature-desc { font-size: 0.78rem; color: rgba(200,214,229,0.4); line-height: 1.5; }

    /* ── Medical Disclaimer ──────────────────── */
    .disclaimer-bar {
        display: flex; align-items: center; gap: 0.8rem;
        background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.15);
        border-radius: 12px; padding: 0.7rem 1.2rem; margin-bottom: 2rem;
        font-size: 0.83rem; color: rgba(251,191,36,0.8);
    }

    /* ── Upload Section ──────────────────────── */
    .upload-section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem; font-weight: 700; color: #f1f5f9;
        margin-bottom: 1rem;
    }

    /* ── Glass Card (reusable) ───────────────── */
    .gcard {
        background: rgba(12,18,40,0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px; padding: 1.5rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    .gcard:hover {
        border-color: rgba(0,210,190,0.12);
    }
    .gcard-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1.8px;
        color: #00d2be; margin-bottom: 1rem;
    }

    /* ── Stat Cards (circular) ───────────────── */
    .stats-grid {
        display: grid; grid-template-columns: repeat(4, 1fr);
        gap: 1rem; margin-bottom: 1.5rem;
    }
    .scard {
        background: rgba(12,18,40,0.7);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px; padding: 1.2rem 0.8rem;
        text-align: center; transition: all 0.3s;
        position: relative; overflow: hidden;
    }
    .scard::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0;
        height: 3px; opacity: 0; transition: opacity 0.3s;
    }
    .scard:hover { transform: translateY(-3px); border-color: rgba(0,210,190,0.15); }
    .scard:hover::before { opacity: 1; }
    .scard-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
    .scard-val {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem; font-weight: 800; line-height: 1.2;
    }
    .scard-val.teal { color: #00d2be; }
    .scard-val.red { color: #f87171; }
    .scard-val.blue { color: #60a5fa; }
    .scard-val.purple { color: #a78bfa; }
    .scard-label {
        font-size: 0.7rem; color: rgba(200,214,229,0.35);
        text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem;
    }

    /* ══════════════════════════════════════════════
       ══  ABNORMALITY COLUMN (RED SEVERITY)  ══════
       ══════════════════════════════════════════════ */
    .abnorm-section {
        background: rgba(239,68,68,0.04);
        border: 1px solid rgba(239,68,68,0.12);
        border-radius: 20px; padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .abnorm-header {
        display: flex; align-items: center; gap: 0.7rem;
        margin-bottom: 1.2rem;
    }
    .abnorm-header-icon {
        width: 36px; height: 36px; border-radius: 10px;
        background: rgba(239,68,68,0.15);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
    }
    .abnorm-header-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem; font-weight: 700; color: #fca5a5;
    }
    .abnorm-header-count {
        margin-left: auto;
        background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3);
        color: #f87171; padding: 4px 14px;
        border-radius: 20px; font-size: 0.78rem; font-weight: 700;
    }

    /* Individual abnormality card */
    .abnorm-card {
        background: rgba(239,68,68,0.03);
        border: 1px solid rgba(239,68,68,0.1);
        border-left: 4px solid;
        border-radius: 0 14px 14px 0;
        padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
        transition: all 0.3s ease;
    }
    .abnorm-card:hover {
        background: rgba(239,68,68,0.06);
        transform: translateX(4px);
    }

    /* Severity-specific left-border colors */
    .abnorm-card.sev-low { border-left-color: #f59e0b; }
    .abnorm-card.sev-medium { border-left-color: #f97316; }
    .abnorm-card.sev-high { border-left-color: #ef4444; }
    .abnorm-card.sev-critical { border-left-color: #dc2626; }

    .abnorm-param-row {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .abnorm-param {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700; font-size: 1rem; color: #f1f5f9;
    }

    /* Severity badge */
    .sev-badge {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 4px 12px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 800;
        letter-spacing: 0.5px; text-transform: uppercase;
    }
    .sev-badge.low { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .sev-badge.medium { background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }
    .sev-badge.high { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.35); }
    .sev-badge.critical {
        background: rgba(220,38,38,0.25); color: #fca5a5;
        border: 1px solid rgba(220,38,38,0.5);
        animation: pulse-crit 2s infinite;
    }
    @keyframes pulse-crit {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.3); }
        50% { box-shadow: 0 0 0 6px rgba(239,68,68,0); }
    }

    /* Severity bar visualizer */
    .sev-bar-track {
        height: 6px; border-radius: 3px;
        background: rgba(255,255,255,0.05);
        margin: 0.5rem 0; overflow: hidden;
    }
    .sev-bar-fill {
        height: 100%; border-radius: 3px;
        transition: width 0.6s ease;
    }
    .sev-bar-fill.low { width: 25%; background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .sev-bar-fill.medium { width: 50%; background: linear-gradient(90deg, #f97316, #fb923c); }
    .sev-bar-fill.high { width: 75%; background: linear-gradient(90deg, #ef4444, #f87171); }
    .sev-bar-fill.critical { width: 100%; background: linear-gradient(90deg, #dc2626, #ef4444); }

    .abnorm-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.3rem; font-weight: 700; color: #f87171;
    }
    .abnorm-unit {
        font-size: 0.82rem; color: rgba(200,214,229,0.35);
    }
    .abnorm-ref {
        font-size: 0.8rem; color: rgba(200,214,229,0.3);
        margin-top: 0.4rem;
    }
    .abnorm-explain {
        font-size: 0.88rem; color: rgba(200,214,229,0.6);
        line-height: 1.6; margin-top: 0.6rem;
        padding-top: 0.6rem; border-top: 1px solid rgba(255,255,255,0.04);
    }
    .abnorm-rec {
        display: flex; align-items: flex-start; gap: 0.5rem;
        font-size: 0.82rem; color: rgba(251,191,36,0.7);
        margin-top: 0.5rem; font-style: italic;
    }

    /* All-clear card */
    .all-clear {
        text-align: center; padding: 2.5rem 1.5rem;
        background: rgba(16,185,129,0.04);
        border: 1px solid rgba(16,185,129,0.1);
        border-radius: 16px;
    }
    .all-clear-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .all-clear-title { font-size: 1.2rem; font-weight: 700; color: #34d399; }
    .all-clear-sub { font-size: 0.88rem; color: rgba(200,214,229,0.4); margin-top: 0.3rem; }

    /* ── Finding Cards (normal) ──────────────── */
    .finding-card {
        background: rgba(12,18,40,0.5);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 14px; padding: 1rem 1.2rem;
        margin-bottom: 0.6rem; transition: all 0.3s;
    }
    .finding-card:hover {
        border-color: rgba(0,210,190,0.15);
        transform: translateX(4px);
    }
    .finding-row {
        display: flex; align-items: center; justify-content: space-between;
    }
    .finding-name {
        font-weight: 600; font-size: 0.92rem; color: #e2e8f0;
    }
    .finding-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem; font-weight: 600; color: #00d2be;
    }
    .badge-normal {
        display: inline-block; padding: 3px 10px;
        border-radius: 20px; font-size: 0.68rem; font-weight: 700;
        background: rgba(16,185,129,0.12); color: #34d399;
        border: 1px solid rgba(16,185,129,0.25);
        text-transform: uppercase; letter-spacing: 0.3px;
    }

    /* ── Question Cards ──────────────────────── */
    .q-card {
        background: rgba(56,130,246,0.04);
        border: 1px solid rgba(56,130,246,0.1);
        border-left: 3px solid #3882f6;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem; margin-bottom: 0.5rem;
        transition: all 0.3s; font-size: 0.92rem; color: #93c5fd;
    }
    .q-card:hover { background: rgba(56,130,246,0.08); transform: translateX(4px); }
    .q-num { color: #3882f6; font-weight: 800; margin-right: 8px; }

    /* ── Summary Card ────────────────────────── */
    .summary-box {
        background: linear-gradient(135deg, rgba(0,210,190,0.04), rgba(56,130,246,0.03));
        border: 1px solid rgba(0,210,190,0.1);
        border-radius: 16px; padding: 1.5rem;
        font-size: 0.95rem; line-height: 1.8;
        color: rgba(200,214,229,0.8);
    }

    /* ── Term Pills ──────────────────────────── */
    .pill {
        display: inline-block;
        background: rgba(139,92,246,0.08);
        border: 1px solid rgba(139,92,246,0.15);
        color: #c4b5fd; padding: 4px 12px;
        border-radius: 20px; font-size: 0.78rem;
        margin: 3px; transition: all 0.2s;
    }
    .pill:hover { background: rgba(139,92,246,0.15); transform: scale(1.05); }

    /* ── Divider ─────────────────────────────── */
    .neon-div {
        height: 1px; margin: 2rem 0;
        background: linear-gradient(90deg, transparent, rgba(0,210,190,0.2), rgba(56,130,246,0.2), transparent);
    }

    /* ── Section Header ──────────────────────── */
    .sec-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem; font-weight: 700; color: #f1f5f9;
        margin: 1.5rem 0 1rem; display: flex;
        align-items: center; gap: 0.6rem;
    }
    .sec-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(0,210,190,0.2), transparent); }

    /* ── Footer ──────────────────────────────── */
    .site-footer {
        text-align: center; padding: 2.5rem 0 1rem;
        border-top: 1px solid rgba(255,255,255,0.03);
        margin-top: 3rem;
    }
    .site-footer-brand {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem; font-weight: 700;
        background: linear-gradient(135deg, #00d2be, #3882f6);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .site-footer-links {
        display: flex; justify-content: center; gap: 2rem;
        margin: 1rem 0; font-size: 0.82rem; color: rgba(200,214,229,0.3);
    }
    .site-footer-copy {
        font-size: 0.75rem; color: rgba(200,214,229,0.2);
    }

    /* ── Streamlit Overrides ─────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #00d2be 0%, #3882f6 100%) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important; font-size: 1rem !important;
        letter-spacing: 0.3px !important; transition: all 0.3s !important;
        box-shadow: 0 4px 20px rgba(0,210,190,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0,210,190,0.35) !important;
    }
    .stFileUploader {
        background: rgba(0,210,190,0.03) !important;
        border: 2px dashed rgba(0,210,190,0.15) !important;
        border-radius: 16px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: rgba(12,18,40,0.6);
        border-radius: 14px; padding: 5px; border: 1px solid rgba(255,255,255,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px; color: rgba(200,214,229,0.5); font-weight: 500;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0,210,190,0.12) !important; color: #00d2be !important;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060918 0%, #0c1230 100%);
        border-right: 1px solid rgba(0,210,190,0.06);
    }
    .stMarkdown, .stText, p, span, li { color: #c8d6e5; }
    h1, h2, h3, h4, h5, h6 { color: #f1f5f9 !important; }
</style>
""", unsafe_allow_html=True)

# ── API Config ─────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000/api"

SEVERITY_LABELS = {
    "normal": "Normal", "low": "Low Risk", "medium": "Moderate",
    "high": "High Risk", "critical": "Critical",
}
SEVERITY_ICONS = {
    "normal": "✅", "low": "⚠️", "medium": "🟠", "high": "🔴", "critical": "🚨",
}
SEVERITY_PERCENT = {
    "normal": 0, "low": 25, "medium": 50, "high": 75, "critical": 100,
}

if "history" not in st.session_state:
    st.session_state.history = []


# ── Helper: Plotly Gauge ───────────────────────────────────────────────

def make_gauge(normal: int, total: int):
    score = int((normal / total) * 100) if total > 0 else 100
    color = "#10b981" if score >= 80 else ("#f59e0b" if score >= 50 else "#ef4444")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 38, "color": color, "family": "Space Grotesk"}},
        title={"text": "Overall Health Score", "font": {"size": 13, "color": "#64748b"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "rgba(0,0,0,0)"},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(255,255,255,0.02)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(239,68,68,0.08)"},
                {"range": [40, 70], "color": "rgba(245,158,11,0.08)"},
                {"range": [70, 100], "color": "rgba(16,185,129,0.08)"},
            ],
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=200, margin=dict(l=20, r=20, t=45, b=0),
        font={"color": "#c8d6e5"},
    )
    return fig


def make_donut(findings: list):
    counts = {"Normal": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0}
    for f in findings:
        s = f.get("status", "normal").capitalize()
        if s in counts:
            counts[s] += 1
    labels = [k for k, v in counts.items() if v > 0]
    values = [v for v in counts.values() if v > 0]
    cmap = {"Normal": "#10b981", "Low": "#f59e0b", "Medium": "#f97316", "High": "#ef4444", "Critical": "#dc2626"}
    colors = [cmap.get(l, "#64748b") for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.7,
        marker=dict(colors=colors, line=dict(color="#060918", width=3)),
        textfont=dict(color="#c8d6e5", size=11),
        hoverinfo="label+value+percent",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=200, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(font=dict(color="#c8d6e5", size=10), bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text="Severity", x=0.5, y=0.5, font_size=12, font_color="#475569", showarrow=False)],
    )
    return fig


# ══════════════════════════════════════════════════════════════════════
# ══  SIDEBAR  ════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 1rem;">
        <div style="font-size:2.5rem;">🏥</div>
        <div style="font-family:'Space Grotesk'; font-size:1.3rem; font-weight:700;
            background:linear-gradient(135deg,#00d2be,#3882f6);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;">MedReport AI</div>
        <div style="font-size:0.68rem; color:rgba(200,214,229,0.3); letter-spacing:2px; text-transform:uppercase;">
            v1.0 · Medical Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    api_url = st.text_input("🔗 API Server", value="http://localhost:8000")
    API_BASE_URL = f"{api_url}/api"

    st.markdown("---")
    st.markdown("""
    <div class="gcard" style="padding:1rem;">
        <div class="gcard-header">⚡ How It Works</div>
        <div style="font-size:0.82rem; color:rgba(200,214,229,0.5); line-height:1.8;">
            <strong style="color:#00d2be;">1.</strong> Upload medical report<br>
            <strong style="color:#3882f6;">2.</strong> AI extracts key findings<br>
            <strong style="color:#8b5cf6;">3.</strong> Get simplified explanations<br>
            <strong style="color:#ef4444;">4.</strong> View flagged abnormalities<br>
            <strong style="color:#f59e0b;">5.</strong> Ask follow-up questions
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    st.caption("📄 PDF  ·  🖼️ PNG/JPG  ·  📝 TXT")
    st.caption("Max file size: 10MB")

    st.markdown("---")
    st.markdown("**📂 Recent Reports**")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f"""<div style="background:rgba(0,210,190,0.03); border:1px solid rgba(0,210,190,0.08);
                border-radius:10px; padding:0.5rem 0.8rem; margin-bottom:0.4rem; font-size:0.8rem;">
                <div style="color:#00d2be; font-weight:600;">📄 {h['filename'][:25]}</div>
                <div style="color:rgba(200,214,229,0.3); font-size:0.72rem;">
                    {h.get('report_type','N/A').replace('_',' ').title()} · {h.get('findings_count',0)} findings
                </div></div>""", unsafe_allow_html=True)
    else:
        st.caption("No reports analyzed yet.")


# ══════════════════════════════════════════════════════════════════════
# ══  TOP NAVIGATION  ═════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="topnav">
    <div class="topnav-brand">
        <div class="topnav-logo">✚</div>
        <div>
            <div class="topnav-name">MedReport AI</div>
            <div class="topnav-tagline">Medical Intelligence Platform</div>
        </div>
    </div>
    <div class="topnav-links">
        <span class="topnav-link">Features</span>
        <span class="topnav-link">How It Works</span>
        <span class="topnav-link">About</span>
        <span class="topnav-cta">Get Started ↓</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ══  HERO SECTION  ═══════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-pill">
        <span class="hero-pill-dot"></span>
        Powered by Gemini 2.0 Flash &amp; RAG
    </div>
    <h1>Your Medical Reports,<br>Simplified by AI</h1>
    <p>
        Upload lab tests, radiology reports, or prescriptions —
        get instant AI analysis, clear explanations in simple language,
        flagged abnormalities, and smart follow-up questions for your doctor.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Feature Cards ──────────────────────────────────────────────────────

st.markdown("""
<div class="features-row">
    <div class="feature-card" style="--fc-color: #00d2be;">
        <div class="feature-icon">🔬</div>
        <div class="feature-title">AI Analysis</div>
        <div class="feature-desc">GPT-4 extracts and interprets every finding from your report</div>
    </div>
    <div class="feature-card" style="--fc-color: #3882f6;">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Plain Language</div>
        <div class="feature-desc">Complex medical terms explained like a friendly doctor would</div>
    </div>
    <div class="feature-card" style="--fc-color: #ef4444;">
        <div class="feature-icon">🚩</div>
        <div class="feature-title">Abnormality Alerts</div>
        <div class="feature-desc">Red-flagged results with severity levels and visual indicators</div>
    </div>
    <div class="feature-card" style="--fc-color: #8b5cf6;">
        <div class="feature-icon">❓</div>
        <div class="feature-title">Follow-Up Questions</div>
        <div class="feature-desc">Smart questions to ask your doctor at your next visit</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Disclaimer ─────────────────────────────────────────────────────────

st.markdown("""
<div class="disclaimer-bar">
    <span>⚠️</span>
    <span><strong>Medical Disclaimer:</strong> This tool provides AI-generated analysis for
    <strong>informational purposes only</strong>. It is NOT a substitute for professional medical advice.
    Always consult a qualified healthcare provider.</span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ══  UPLOAD SECTION  ═════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

st.markdown('<div class="upload-section-title">📤 Upload Your Medical Report</div>', unsafe_allow_html=True)

col_upload, col_tips = st.columns([3, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        help="Supported: PDF, PNG, JPG, JPEG, TXT (max 10MB)",
        label_visibility="collapsed",
    )

with col_tips:
    st.markdown("""
    <div class="gcard" style="padding:1rem;">
        <div class="gcard-header">💡 Pro Tips</div>
        <div style="font-size:0.8rem; color:rgba(200,214,229,0.45); line-height:1.7;">
            • Use clear, high-res scans<br>
            • Crop unnecessary margins<br>
            • Works best with lab reports<br>
            • PDF gives the best results
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ══  ANALYSIS PIPELINE  ═════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

if uploaded_file is not None:
    file_kb = uploaded_file.size / 1024

    st.markdown(f"""
    <div class="gcard" style="display:flex; align-items:center; gap:1rem; padding:1rem 1.5rem; margin-bottom:1rem;">
        <div style="font-size:2rem;">📄</div>
        <div style="flex:1;">
            <div style="font-weight:600; color:#f1f5f9;">{uploaded_file.name}</div>
            <div style="font-size:0.8rem; color:rgba(200,214,229,0.35);">{file_kb:.1f} KB · {uploaded_file.type}</div>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
            <div style="width:8px; height:8px; border-radius:50%; background:#00d2be;
                animation: blink 2s infinite;"></div>
            <span style="font-size:0.82rem; color:#00d2be; font-weight:500;">Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔬  Analyze Report", type="primary", use_container_width=True):

        # ── Upload ─────────────────────────────────
        progress = st.progress(0, text="📤 Uploading report...")
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            up_resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
            if up_resp.status_code != 200:
                st.error(f"❌ Upload failed: {up_resp.json().get('detail', 'Unknown error')}")
                st.stop()
            file_id = up_resp.json()["file_id"]
            progress.progress(30, text="✅ Uploaded! Analyzing with AI...")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the backend. Make sure the server is running.")
            st.code("uvicorn app.main:app --reload --port 8000", language="bash")
            st.stop()
        except Exception as e:
            st.error(f"❌ Upload error: {e}")
            st.stop()

        # ── Analyze ────────────────────────────────
        try:
            a_resp = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"file_id": file_id, "filename": uploaded_file.name},
                timeout=120,
            )
            if a_resp.status_code != 200:
                st.error(f"❌ Analysis failed: {a_resp.json().get('detail', 'Unknown error')}")
                st.stop()
            analysis = a_resp.json()
            progress.progress(65, text="🧠 Analyzed! Simplifying...")
        except Exception as e:
            st.error(f"❌ Analysis error: {e}")
            st.stop()

        # ── Simplify ──────────────────────────────
        try:
            s_resp = requests.post(
                f"{API_BASE_URL}/simplify",
                json={"file_id": file_id, "summary": analysis["summary"], "findings": analysis["findings"]},
                timeout=120,
            )
            simplified = s_resp.json() if s_resp.status_code == 200 else None
        except Exception:
            simplified = None

        progress.progress(100, text="✨ Complete!")

        # ── Save history ───────────────────────────
        st.session_state.history.append({
            "filename": uploaded_file.name,
            "file_id": file_id,
            "report_type": analysis.get("report_type", "general"),
            "findings_count": len(analysis.get("findings", [])),
        })

        # ══════════════════════════════════════════
        # ══  RESULTS  ═════════════════════════════
        # ══════════════════════════════════════════

        st.markdown('<div class="neon-div"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="sec-header">📊 Analysis Results <div class="sec-line"></div></div>
        """, unsafe_allow_html=True)

        findings = analysis.get("findings", [])
        normal_count = sum(1 for f in findings if f.get("status") == "normal")
        abnormal_findings = [f for f in findings if f.get("status", "normal") != "normal"]
        abnormal_count = len(abnormal_findings)

        # ── Stat Cards Row ─────────────────────────
        st.markdown(f"""
        <div class="stats-grid">
            <div class="scard" style="--scard-color:#00d2be;">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#00d2be,#3882f6);"></div>
                <div class="scard-icon">🔬</div>
                <div class="scard-val teal">{len(findings)}</div>
                <div class="scard-label">Total Findings</div>
            </div>
            <div class="scard">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#ef4444,#f97316);"></div>
                <div class="scard-icon">{"🚨" if abnormal_count > 0 else "✅"}</div>
                <div class="scard-val red">{abnormal_count}</div>
                <div class="scard-label">Abnormal</div>
            </div>
            <div class="scard">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#3882f6,#60a5fa);"></div>
                <div class="scard-icon">📋</div>
                <div class="scard-val blue" style="font-size:1rem;">{analysis.get('report_type','general').replace('_',' ').title()}</div>
                <div class="scard-label">Report Type</div>
            </div>
            <div class="scard">
                <div style="position:absolute;top:0;left:0;right:0;height:3px;
                    background:linear-gradient(90deg,#8b5cf6,#a78bfa);"></div>
                <div class="scard-icon">📖</div>
                <div class="scard-val purple">{len(analysis.get('medical_terms',[]))}</div>
                <div class="scard-label">Medical Terms</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Charts Row ─────────────────────────────
        ch1, ch2 = st.columns(2)
        with ch1:
            st.plotly_chart(make_gauge(normal_count, len(findings)), use_container_width=True, config={"displayModeBar": False})
        with ch2:
            st.plotly_chart(make_donut(findings), use_container_width=True, config={"displayModeBar": False})

        # ══════════════════════════════════════════════════════════
        # ══  ABNORMALITIES SECTION (RED COLUMN)  ═════════════════
        # ══════════════════════════════════════════════════════════

        st.markdown(f"""
        <div class="sec-header">🚩 Abnormalities & Alerts <div class="sec-line"></div></div>
        """, unsafe_allow_html=True)

        if abnormal_findings:
            # Build abnormality details from simplified data if available
            abnorm_details = {}
            if simplified and simplified.get("abnormalities"):
                for ab in simplified["abnormalities"]:
                    key = ab.get("parameter", "").lower().strip()
                    abnorm_details[key] = ab

            st.markdown(f"""
            <div class="abnorm-section">
                <div class="abnorm-header">
                    <div class="abnorm-header-icon">🚨</div>
                    <div class="abnorm-header-text">Flagged Abnormalities</div>
                    <div class="abnorm-header-count">{abnormal_count} found</div>
                </div>
            """, unsafe_allow_html=True)

            for f in abnormal_findings:
                sev = f.get("status", "low")
                icon = SEVERITY_ICONS.get(sev, "⚠️")
                label = SEVERITY_LABELS.get(sev, sev.title())

                # Get simplified details if available
                detail = abnorm_details.get(f.get("parameter", "").lower().strip(), {})
                explanation = detail.get("explanation", f.get("interpretation", ""))
                recommendation = detail.get("recommendation", "")

                st.markdown(f"""
                <div class="abnorm-card sev-{sev}">
                    <div class="abnorm-param-row">
                        <div class="abnorm-param">{icon} {f['parameter']}</div>
                        <span class="sev-badge {sev}">{label}</span>
                    </div>
                    <div style="display:flex; align-items:baseline; gap:0.5rem; margin-top:0.3rem;">
                        <span class="abnorm-value">{f['value']}</span>
                        <span class="abnorm-unit">{f.get('unit','')}</span>
                    </div>
                    <div class="sev-bar-track">
                        <div class="sev-bar-fill {sev}"></div>
                    </div>
                    <div class="abnorm-ref">📏 Reference Range: {f.get('reference_range', 'N/A')}</div>
                    {"<div class='abnorm-explain'>💬 " + explanation + "</div>" if explanation else ""}
                    {"<div class='abnorm-rec'>💡 <span>" + recommendation + "</span></div>" if recommendation else ""}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="all-clear">
                <div class="all-clear-icon">🛡️</div>
                <div class="all-clear-title">All Clear!</div>
                <div class="all-clear-sub">No significant abnormalities were detected in your report.</div>
            </div>
            """, unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════
        # ══  TABBED DETAILED RESULTS  ════════════════════════════
        # ══════════════════════════════════════════════════════════

        st.markdown('<div class="neon-div"></div>', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📋 Summary & Simplified", "🔬 All Findings", "❓ Follow-Up Questions"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🧠 AI Analysis Summary")
                st.markdown(f'<div class="summary-box">{analysis.get("summary","N/A")}</div>', unsafe_allow_html=True)
            with c2:
                if simplified:
                    st.markdown("#### 💬 Simplified For You")
                    st.markdown(f'<div class="summary-box">{simplified.get("simplified_summary","N/A")}</div>', unsafe_allow_html=True)

            if analysis.get("medical_terms"):
                st.markdown("")
                st.markdown("#### 📖 Medical Terms Detected")
                pills = " ".join([f'<span class="pill">{t}</span>' for t in analysis["medical_terms"]])
                st.markdown(pills, unsafe_allow_html=True)

        with tab2:
            if findings:
                st.markdown("#### All Extracted Findings")
                for f in findings:
                    sev = f.get("status", "normal")
                    is_normal = sev == "normal"
                    if is_normal:
                        st.markdown(f"""
                        <div class="finding-card">
                            <div class="finding-row">
                                <div>
                                    <div class="finding-name">✅ {f['parameter']}</div>
                                    <div style="font-size:0.78rem; color:rgba(200,214,229,0.3); margin-top:2px;">
                                        Ref: {f.get('reference_range','N/A')} · {f.get('interpretation','')}
                                    </div>
                                </div>
                                <div style="text-align:right;">
                                    <div class="finding-val">{f['value']} <span style="font-size:0.75rem; color:rgba(200,214,229,0.3);">{f.get('unit','')}</span></div>
                                    <span class="badge-normal">Normal</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        icon = SEVERITY_ICONS.get(sev, "⚠️")
                        label = SEVERITY_LABELS.get(sev, sev.title())
                        st.markdown(f"""
                        <div class="abnorm-card sev-{sev}" style="margin-bottom:0.6rem;">
                            <div class="abnorm-param-row">
                                <div class="abnorm-param">{icon} {f['parameter']}</div>
                                <span class="sev-badge {sev}">{label}</span>
                            </div>
                            <div style="display:flex; align-items:baseline; gap:0.5rem; margin-top:0.2rem;">
                                <span class="abnorm-value">{f['value']}</span>
                                <span class="abnorm-unit">{f.get('unit','')}</span>
                            </div>
                            <div class="sev-bar-track"><div class="sev-bar-fill {sev}"></div></div>
                            <div class="abnorm-ref">📏 Ref: {f.get('reference_range','N/A')} · {f.get('interpretation','')}</div>
                        </div>
                        """, unsafe_allow_html=True)

        with tab3:
            if simplified and simplified.get("followup_questions"):
                st.markdown("#### 💡 Questions to Ask Your Doctor")
                st.markdown("")
                for i, q in enumerate(simplified["followup_questions"], 1):
                    st.markdown(f'<div class="q-card"><span class="q-num">Q{i}.</span> {q}</div>', unsafe_allow_html=True)
            else:
                st.info("Follow-up questions not available for this report.")

        # ── Final Disclaimer ───────────────────────
        st.markdown('<div class="neon-div"></div>', unsafe_allow_html=True)
        disclaimer = simplified.get("disclaimer", "") if simplified else ""
        if not disclaimer:
            disclaimer = ("⚠️ This AI-generated analysis is for informational purposes only. "
                         "It is NOT a substitute for professional medical advice, diagnosis, or treatment.")
        st.markdown(f'<div class="disclaimer-bar"><span>⚠️</span><span>{disclaimer}</span></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# ══  FOOTER  ═════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="site-footer">
    <div class="site-footer-brand">🏥 MedReport AI</div>
    <div class="site-footer-links">
        <span>Features</span> · <span>Documentation</span> · <span>About</span> · <span>Contact</span>
    </div>
    <div class="site-footer-copy">
        © {datetime.now().year} MedReport AI · Built with FastAPI, OpenAI GPT-4 & Streamlit ·
        For educational purposes only
    </div>
</div>
""", unsafe_allow_html=True)
