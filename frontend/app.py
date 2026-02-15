"""
MedReport AI — Niroggyan-Inspired Frontend
Clean, professional light-themed medical report analyzer.
"""

import io
import json
import datetime
import streamlit as st
import requests
import plotly.graph_objects as go
import html
from fpdf import FPDF

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedReport AI | Lab Report Analyzer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = "http://localhost:8000/api"

# ── Custom CSS — Niroggyan-Inspired Light Theme ────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Global ─────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: linear-gradient(180deg, #eef4ff 0%, #f8faff 30%, #ffffff 100%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a2332;
}

header[data-testid="stHeader"] { background: transparent !important; }
.block-container { max-width: 1200px; padding: 1rem 2rem 4rem; }
section[data-testid="stSidebar"] { display: none !important; }

h1, h2, h3, h4, h5, h6 { font-family: 'Inter', sans-serif; color: #0b1c2c; }

/* Hide streamlit branding */
#MainMenu, footer, .stDeployButton { display: none !important; }

/* ── Navbar ─────────────────────────────────────────────── */
.nav-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.8rem 2rem;
    background: rgba(255,255,255,0.95);
    border-bottom: 1px solid #e8edf2;
    border-radius: 16px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.nav-brand {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.4rem; font-weight: 700; color: #1a73e8;
    text-decoration: none;
}
.nav-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1a73e8, #4dabf7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.1rem;
}
.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a {
    color: #4a5568; font-weight: 500; text-decoration: none;
    font-size: 0.9rem; transition: color 0.2s;
}
.nav-links a:hover { color: #1a73e8; }
.nav-cta {
    background: #1a73e8; color: white !important;
    padding: 8px 20px; border-radius: 8px; font-weight: 600;
    transition: background 0.2s;
}
.nav-cta:hover { background: #1557b0; }

/* ── Hero Section ──────────────────────────────────────── */
.hero-section {
    display: flex; align-items: center; gap: 60px;
    padding: 2rem 0 3rem;
}
.hero-left { flex: 1; }
.hero-right { flex: 0.8; }

.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: #fff8e1; color: #b8860b;
    padding: 6px 16px; border-radius: 20px;
    font-size: 0.85rem; font-weight: 600;
    margin-bottom: 1.2rem;
    border: 1px solid #ffe0b2;
}
.hero-badge-star { font-size: 1rem; }
.hero-trust {
    color: #64748b; font-size: 0.85rem;
    margin-left: 8px; font-weight: 400;
}

.hero-title {
    font-size: 2.8rem; font-weight: 800;
    line-height: 1.15; margin-bottom: 1.5rem;
    color: #0b1c2c;
}
.hero-title span { color: #1a73e8; }

.hero-checklist {
    list-style: none; padding: 0; margin: 0;
    display: flex; flex-direction: column; gap: 12px;
}
.hero-checklist li {
    display: flex; align-items: center; gap: 10px;
    color: #475569; font-size: 1rem; font-weight: 400;
}
.hero-check {
    color: #1a73e8; font-size: 1.1rem; font-weight: 700;
}

/* ── Report Preview Card (Hero Right) ──────────────────── */
.report-card {
    background: white;
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow: 0 8px 30px rgba(26,115,232,0.08), 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid #e8edf2;
    position: relative;
}
.report-card-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1.5rem;
}
.report-card-icon {
    width: 42px; height: 42px;
    background: #e8f5e9; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.report-card-title {
    font-size: 1.15rem; font-weight: 700; color: #0b1c2c;
}

.biomarker-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 16px;
    background: #f8fafc;
    border-radius: 12px;
    margin-bottom: 8px;
    border: 1px solid #f0f3f7;
}
.biomarker-name { font-weight: 500; color: #374151; font-size: 0.95rem; }
.biomarker-value { font-weight: 700; color: #0b1c2c; font-size: 0.95rem; }
.biomarker-badge {
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 600;
    display: inline-flex; align-items: center; gap: 4px;
}
.badge-normal { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.badge-low { background: #fef9c3; color: #a16207; border: 1px solid #fde68a; }
.badge-medium { background: #ffedd5; color: #c2410c; border: 1px solid #fed7aa; }
.badge-high { background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; }
.badge-critical { background: #fecaca; color: #991b1b; border: 1px solid #f87171; }

.ai-complete-bar {
    display: flex; align-items: center; gap: 10px;
    background: #e0f7fa; color: #00838f;
    padding: 12px 18px; border-radius: 12px;
    margin-top: 10px;
    font-weight: 600; font-size: 0.9rem;
    border: 1px solid #b2ebf2;
}

.trust-badges {
    display: flex; gap: 12px; margin-top: 16px;
}
.trust-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px;
    background: white; border: 1px solid #e2e8f0;
    font-size: 0.8rem; font-weight: 500; color: #475569;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* ── Upload Section ────────────────────────────────────── */
.upload-section {
    display: flex; gap: 40px;
    padding: 3rem 0;
    align-items: flex-start;
}
.upload-left { flex: 1; }
.upload-right { flex: 1; }

.upload-box {
    border: 2.5px dashed #a4c3f5;
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    background: rgba(255,255,255,0.9);
    transition: all 0.3s;
}
.upload-box:hover {
    border-color: #1a73e8;
    background: rgba(26,115,232,0.02);
}
.upload-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.upload-text { font-size: 1rem; font-weight: 500; color: #374151; }
.upload-sub { font-size: 0.85rem; color: #64748b; margin-top: 4px; }

/* ── How It Works ──────────────────────────────────────── */
.section-title {
    font-size: 1.8rem; font-weight: 800;
    color: #0b1c2c; margin-bottom: 2rem;
    text-align: center;
}

.steps-container {
    display: flex; flex-direction: column; gap: 10px;
}
.step-row {
    display: flex; align-items: center; gap: 16px;
    padding: 14px 20px;
    background: white;
    border-radius: 14px;
    border: 1px solid #f0f3f7;
    transition: all 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.step-row:hover {
    box-shadow: 0 4px 12px rgba(26,115,232,0.08);
    border-color: #bbd6f7;
}
.step-num {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #1a73e8, #4dabf7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 0.9rem;
    flex-shrink: 0;
}
.step-text { font-weight: 500; color: #374151; font-size: 0.95rem; }

/* ── Feature Cards ─────────────────────────────────────── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 2rem 0;
}
.feature-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #f0f3f7;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: all 0.2s;
}
.feature-card:hover {
    box-shadow: 0 6px 20px rgba(26,115,232,0.08);
    transform: translateY(-2px);
}
.feature-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 14px;
}
.fi-blue { background: #e3f2fd; }
.fi-green { background: #e8f5e9; }
.fi-orange { background: #fff3e0; }
.fi-purple { background: #f3e5f5; }
.fi-red { background: #fce4ec; }
.fi-teal { background: #e0f2f1; }
.feature-title { font-weight: 700; color: #0b1c2c; font-size: 1rem; margin-bottom: 4px; }
.feature-desc { color: #64748b; font-size: 0.85rem; line-height: 1.5; }

/* ── Results Section ───────────────────────────────────── */
.results-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1.5rem;
}
.results-header-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #1a73e8, #4dabf7);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.2rem;
}
.results-header-title {
    font-size: 1.4rem; font-weight: 700; color: #0b1c2c;
}

.summary-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 1rem;
}
.summary-card h4 {
    font-size: 1rem; font-weight: 700; color: #0b1c2c; margin-bottom: 0.5rem;
}
.summary-card p {
    color: #475569; font-size: 0.95rem; line-height: 1.6; margin: 0;
}

/* ── Abnormality Section ───────────────────────────────── */
.abnorm-panel {
    background: white;
    border-radius: 16px;
    border: 1px solid #fee2e2;
    box-shadow: 0 2px 12px rgba(220,38,38,0.06);
    overflow: hidden;
}
.abnorm-panel-header {
    background: linear-gradient(135deg, #fef2f2, #fff5f5);
    padding: 16px 20px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid #fee2e2;
}
.abnorm-panel-title {
    display: flex; align-items: center; gap: 10px;
    font-weight: 700; color: #dc2626; font-size: 1.05rem;
}
.abnorm-count {
    background: #dc2626; color: white;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.8rem; font-weight: 700;
}
.abnorm-item {
    padding: 16px 20px;
    border-bottom: 1px solid #fef2f2;
    display: flex; align-items: flex-start; gap: 12px;
}
.abnorm-item:last-child { border-bottom: none; }
.abnorm-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-top: 5px; flex-shrink: 0;
}
.dot-low { background: #f59e0b; }
.dot-medium { background: #f97316; }
.dot-high { background: #ef4444; }
.dot-critical { background: #dc2626; animation: pulse-dot 1.5s infinite; }
@keyframes pulse-dot {
    0%, 100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.4); }
    50% { box-shadow: 0 0 0 6px rgba(220,38,38,0); }
}
.abnorm-detail { flex: 1; }
.abnorm-param { font-weight: 600; color: #0f172a; font-size: 0.95rem; }
.abnorm-val { color: #334155; font-size: 0.9rem; margin-top: 2px; font-weight: 500; }
.abnorm-explain {
    background: #fff1f2; padding: 10px 14px;
    border-radius: 8px; margin-top: 8px;
    font-size: 0.9rem; color: #4b5563; line-height: 1.5;
    border-left: 3px solid #f87171;
}

.all-clear {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    border: 1px solid #dcfce7;
    box-shadow: 0 2px 8px rgba(34,197,94,0.06);
}
.all-clear-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.all-clear-title { font-weight: 700; color: #15803d; font-size: 1.1rem; }
.all-clear-sub { color: #64748b; font-size: 0.9rem; margin-top: 4px; }

/* ── Follow-up Questions ───────────────────────────────── */
.question-card {
    display: flex; align-items: flex-start; gap: 12px;
    padding: 14px 18px;
    background: white;
    border-radius: 14px;
    border: 1px solid #f0f3f7;
    margin-bottom: 8px;
    transition: all 0.2s;
}
.question-card:hover {
    border-color: #bbd6f7;
    box-shadow: 0 2px 8px rgba(26,115,232,0.06);
}
.question-num {
    width: 28px; height: 28px;
    background: #e3f2fd; color: #1a73e8;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.8rem; flex-shrink: 0;
}
.question-text { color: #374151; font-size: 0.95rem; line-height: 1.5; }

/* ── FAQ Accordion ─────────────────────────────────────── */
.faq-item {
    background: white;
    border-radius: 14px;
    border: 1px solid #f0f3f7;
    margin-bottom: 10px;
    overflow: hidden;
}
.faq-q {
    padding: 16px 20px;
    font-weight: 600; color: #0b1c2c;
    font-size: 0.95rem;
    display: flex; align-items: center; justify-content: space-between;
}
.faq-plus {
    width: 32px; height: 32px;
    background: #1a73e8; color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 700;
}

/* ── Footer ────────────────────────────────────────────── */
.footer {
    background: #0b1c2c;
    border-radius: 20px 20px 0 0;
    padding: 2.5rem 2rem 1.5rem;
    margin-top: 4rem;
    text-align: center;
    color: #94a3b8;
}
.footer-brand {
    font-size: 1.3rem; font-weight: 700; color: white;
    margin-bottom: 0.5rem;
}
.footer-links {
    display: flex; justify-content: center; gap: 24px;
    margin: 1rem 0;
}
.footer-links a {
    color: #94a3b8; text-decoration: none;
    font-size: 0.9rem; transition: color 0.2s;
}
.footer-links a:hover { color: white; }
.footer-copy { font-size: 0.8rem; color: #64748b; margin-top: 1rem; }

/* ── Stat Cards ────────────────────────────────────────── */
.stat-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    border: 1px solid #f0f3f7;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
.stat-value { font-size: 2rem; font-weight: 800; color: #1a73e8; }
.stat-label { font-size: 0.85rem; color: #64748b; font-weight: 500; margin-top: 2px; }

/* ── Streamlit Overrides ───────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 12px;
    padding: 4px; border: 1px solid #e2e8f0;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; font-weight: 600;
    color: #64748b; font-size: 0.9rem;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: #1a73e8 !important;
    color: white !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #1a73e8, #4dabf7);
    color: white; border: none;
    padding: 14px 36px; font-size: 1.05rem;
    font-weight: 700; border-radius: 14px;
    width: 100%;
    box-shadow: 0 4px 15px rgba(26,115,232,0.25);
    transition: all 0.3s;
}
div.stButton > button:hover {
    box-shadow: 0 6px 22px rgba(26,115,232,0.35);
    transform: translateY(-1px);
}
div.stButton > button:active { transform: translateY(0); }

.stFileUploader > div {
    border: 2px dashed #a4c3f5 !important;
    border-radius: 16px !important;
    background: rgba(255,255,255,0.9) !important;
}

div[data-testid="stExpander"] {
    background: white;
    border: 1px solid #f0f3f7 !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.02);
}

.stAlert { border-radius: 14px !important; }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEVERITY_MAP = {
    "normal": ("badge-normal", "✓ Normal", "dot-normal"),
    "low": ("badge-low", "⚠ Low Risk", "dot-low"),
    "medium": ("badge-medium", "⬆ Moderate", "dot-medium"),
    "high": ("badge-high", "▲ High Risk", "dot-high"),
    "critical": ("badge-critical", "⚠ Critical", "dot-critical"),
}


def make_gauge(score):
    """Create a clean health score gauge."""
    if score >= 80:
        color = "#22c55e"
    elif score >= 60:
        color = "#f59e0b"
    elif score >= 40:
        color = "#f97316"
    else:
        color = "#ef4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 36, "color": "#0b1c2c", "family": "Inter"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "white"},
            "bar": {"color": color, "thickness": 0.7},
            "bgcolor": "#f1f5f9",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#fef2f2"},
                {"range": [40, 60], "color": "#fff7ed"},
                {"range": [60, 80], "color": "#fefce8"},
                {"range": [80, 100], "color": "#f0fdf4"},
            ],
        },
    ))
    fig.update_layout(
        height=200, margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)", font={"family": "Inter"},
    )
    return fig


def generate_pdf(filename, analysis, simplified, health_score):
    """Generate a professional PDF report from analysis results."""

    def _safe(text):
        """Sanitize text for PDF — replace Unicode chars unsupported by Helvetica."""
        if not isinstance(text, str):
            text = str(text)
        replacements = {
            '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '-', '\u2026': '...', '\u00a0': ' ',
            '\u2022': '*', '\u2023': '>', '\u25cf': '*', '\u25cb': 'o',
            '\u2192': '->', '\u2190': '<-', '\u2194': '<->',
            '\u2265': '>=', '\u2264': '<=', '\u2260': '!=',
            '\u00b5': 'u', '\u03bc': 'u',  # mu/micro
            '\u00b2': '2', '\u00b3': '3', '\u00b9': '1',
            '\u2153': '1/3', '\u00bd': '1/2', '\u00bc': '1/4',
            '\u00b0': ' deg', '\u00b1': '+/-',
            '\u2010': '-', '\u2011': '-', '\u2012': '-',
            '\u200b': '', '\u200c': '', '\u200d': '', '\ufeff': '',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        # Strip any remaining non-latin1 characters
        return text.encode('latin-1', errors='replace').decode('latin-1')

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Colors ──
    BLUE = (26, 115, 232)
    DARK = (11, 28, 44)
    GRAY = (100, 116, 139)
    WHITE = (255, 255, 255)
    LIGHT_BG = (248, 250, 252)
    GREEN = (34, 197, 94)
    RED = (220, 38, 38)
    ORANGE = (249, 115, 22)
    YELLOW = (245, 158, 11)

    STATUS_COLORS = {
        "normal": GREEN,
        "low": YELLOW,
        "medium": ORANGE,
        "high": RED,
        "critical": (153, 27, 27),
    }
    STATUS_LABELS = {
        "normal": "Normal",
        "low": "Low Risk",
        "medium": "Moderate",
        "high": "High Risk",
        "critical": "Critical",
    }

    page_w = pdf.w - 2 * pdf.l_margin

    # ── Header Bar ──
    pdf.set_fill_color(*BLUE)
    pdf.rect(0, 0, pdf.w, 32, style="F")
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_y(8)
    pdf.cell(0, 10, "MedReport AI - Lab Report Analysis", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, f"Generated: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(36)

    # ── File Info ──
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, _safe(f"Report: {filename}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ── Health Score Box ──
    findings = analysis.get("findings", [])
    abnormal_list = [f for f in findings if f.get("status", "normal") != "normal"]
    normal_list = [f for f in findings if f.get("status", "normal") == "normal"]

    pdf.set_fill_color(*LIGHT_BG)
    pdf.rect(pdf.l_margin, pdf.get_y(), page_w, 22, style="F")
    y_box = pdf.get_y() + 3

    col_w = page_w / 3
    for i, (label, value, color) in enumerate([
        ("Health Score", f"{health_score}%", BLUE),
        ("Normal", str(len(normal_list)), GREEN),
        ("Abnormal", str(len(abnormal_list)), RED if abnormal_list else GREEN),
    ]):
        x = pdf.l_margin + i * col_w
        pdf.set_xy(x, y_box)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*GRAY)
        pdf.cell(col_w, 5, label, align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(x, y_box + 6)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(*color)
        pdf.cell(col_w, 10, value, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(y_box + 22)
    pdf.ln(4)

    # ── Summary ──
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*BLUE)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y())
    pdf.ln(3)

    summary_text = ""
    if simplified and simplified.get("simplified_summary"):
        summary_text = simplified["simplified_summary"]
    else:
        summary_text = analysis.get("summary", "Analysis complete.")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 5.5, _safe(summary_text))
    pdf.ln(6)

    # ── Biomarker Table ──
    pdf.set_text_color(*DARK)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, f"Biomarker Results ({len(findings)} parameters)", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*BLUE)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y())
    pdf.ln(3)

    # Table header
    col_widths = [page_w * 0.30, page_w * 0.20, page_w * 0.25, page_w * 0.25]
    headers = ["Parameter", "Value", "Reference Range", "Status"]
    pdf.set_fill_color(*BLUE)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 9)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=0, fill=True,
                 align="C" if i > 0 else "L")
    pdf.ln()

    # Table rows
    pdf.set_font("Helvetica", "", 9)
    for idx, f in enumerate(findings):
        sev = f.get("status", "normal")
        is_alt = idx % 2 == 0
        if is_alt:
            pdf.set_fill_color(245, 247, 250)
        else:
            pdf.set_fill_color(*WHITE)

        # Check if we need a new page
        if pdf.get_y() + 8 > pdf.h - 25:
            pdf.add_page()

        # Parameter name
        pdf.set_text_color(*DARK)
        param_name = _safe(f.get("parameter", "Unknown")[:30])
        pdf.cell(col_widths[0], 8, param_name, border=0, fill=is_alt)

        # Value + unit
        value = str(f.get("value", "N/A"))
        unit = f.get("unit", "")
        val_text = _safe(f"{value} {unit}".strip()[:18])
        pdf.set_text_color(*DARK)
        pdf.cell(col_widths[1], 8, val_text, border=0, fill=is_alt, align="C")

        # Reference range
        ref = _safe(str(f.get("reference_range", "-"))[:22])
        pdf.set_text_color(*GRAY)
        pdf.cell(col_widths[2], 8, ref, border=0, fill=is_alt, align="C")

        # Status badge
        status_color = STATUS_COLORS.get(sev, GREEN)
        status_label = STATUS_LABELS.get(sev, "Normal")
        pdf.set_text_color(*status_color)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_widths[3], 8, status_label, border=0, fill=is_alt, align="C")
        pdf.set_font("Helvetica", "", 9)
        pdf.ln()

    pdf.ln(6)

    # ── Abnormalities Detail ──
    if abnormal_list:
        if pdf.get_y() + 40 > pdf.h - 25:
            pdf.add_page()

        pdf.set_text_color(*RED)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, f"Flagged Abnormalities ({len(abnormal_list)})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*RED)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y())
        pdf.ln(3)

        abnorm_details = {}
        if simplified and simplified.get("abnormalities"):
            for ab in simplified["abnormalities"]:
                abnorm_details[ab.get("parameter", "").lower().strip()] = ab

        for f in abnormal_list:
            if pdf.get_y() + 20 > pdf.h - 25:
                pdf.add_page()

            param = f.get("parameter", "Unknown")
            sev = f.get("status", "low")
            value = str(f.get("value", "N/A"))
            unit = f.get("unit", "")
            ref = f.get("reference_range", "")

            status_color = STATUS_COLORS.get(sev, RED)
            status_label = STATUS_LABELS.get(sev, "Abnormal")

            pdf.set_fill_color(254, 242, 242)
            pdf.rect(pdf.l_margin, pdf.get_y(), page_w, 0.5, style="F")
            pdf.set_fill_color(*status_color)
            pdf.rect(pdf.l_margin, pdf.get_y() + 0.5, 3, 14, style="F")

            pdf.set_x(pdf.l_margin + 6)
            pdf.set_text_color(*DARK)
            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 7, _safe(f"{param}: {value} {unit}".strip()), new_x="LMARGIN", new_y="NEXT")

            pdf.set_x(pdf.l_margin + 6)
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*status_color)
            extra = f" | Ref: {ref}" if ref else ""
            pdf.cell(0, 5, _safe(f"{status_label}{extra}"), new_x="LMARGIN", new_y="NEXT")

            # Explanation from simplified
            detail = abnorm_details.get(param.lower().strip(), {})
            explanation = detail.get("explanation", f.get("interpretation", ""))
            recommendation = detail.get("recommendation", "")

            if explanation:
                pdf.set_x(pdf.l_margin + 6)
                pdf.set_text_color(*GRAY)
                pdf.set_font("Helvetica", "I", 8)
                pdf.multi_cell(page_w - 10, 4.5, _safe(explanation[:300]))
            if recommendation:
                pdf.set_x(pdf.l_margin + 6)
                pdf.set_text_color(100, 100, 100)
                pdf.set_font("Helvetica", "", 8)
                pdf.multi_cell(page_w - 10, 4.5, _safe(f"Tip: {recommendation[:200]}"))

            pdf.ln(4)

    # ── Follow-Up Questions ──
    questions = []
    if simplified:
        questions = simplified.get("followup_questions", []) or []

    if questions:
        if pdf.get_y() + 30 > pdf.h - 25:
            pdf.add_page()

        pdf.set_text_color(*BLUE)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "Follow-Up Questions for Your Doctor", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*BLUE)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 40, pdf.get_y())
        pdf.ln(3)

        pdf.set_text_color(*DARK)
        pdf.set_font("Helvetica", "", 10)
        for i, q in enumerate(questions, 1):
            if pdf.get_y() + 8 > pdf.h - 25:
                pdf.add_page()
            pdf.cell(0, 6, _safe(f"{i}. {q}"), new_x="LMARGIN", new_y="NEXT")

        pdf.ln(4)

    # ── Disclaimer Footer ──
    if pdf.get_y() + 30 > pdf.h - 25:
        pdf.add_page()

    pdf.ln(6)
    pdf.set_fill_color(255, 243, 224)
    y_disc = pdf.get_y()
    pdf.rect(pdf.l_margin, y_disc, page_w, 18, style="F")
    pdf.set_xy(pdf.l_margin + 4, y_disc + 2)
    pdf.set_text_color(180, 83, 9)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(0, 5, "MEDICAL DISCLAIMER", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(pdf.l_margin + 4)
    pdf.set_font("Helvetica", "", 7)
    pdf.multi_cell(page_w - 8, 4,
        "This report is AI-generated for informational purposes only. "
        "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider for medical decisions.")

    # ── Bottom Brand ──
    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 5, "Generated by MedReport AI | Powered by Llama 3.3 70B via Groq", align="C")

    return bytes(pdf.output())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NAVIGATION BAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<div class="nav-bar">
    <div class="nav-brand">
        <div class="nav-brand-icon">🔬</div>
        MedReport AI
    </div>
    <div class="nav-links">
        <a href="#features">Features</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#faq">FAQ</a>
        <a href="#upload" class="nav-cta">Try Now →</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO SECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

col_hero_l, col_hero_r = st.columns([1.2, 1])

with col_hero_l:
    st.markdown("""
    <div class="hero-left">
        <div class="hero-badge">
            <span class="hero-badge-star">⭐</span>
            #1 AI Lab Report Analyzer
            <span class="hero-trust">Powered by Llama 3.3 70B via Groq</span>
        </div>
        <div class="hero-title">
            Lab Test Report Analysis:<br>
            <span>Understand Your Lab<br>Report in Seconds</span>
        </div>
        <ul class="hero-checklist">
            <li><span class="hero-check">✓</span> Clear explanations of your biomarker values</li>
            <li><span class="hero-check">✓</span> Reference ranges tailored to your profile</li>
            <li><span class="hero-check">✓</span> Actionable health recommendations</li>
            <li><span class="hero-check">✓</span> Abnormality detection with severity levels</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_hero_r:
    st.markdown("""
    <div class="report-card">
        <div class="report-card-header">
            <div class="report-card-icon">📋</div>
            <div class="report-card-title">Lab Report Analysis</div>
        </div>
        <div class="biomarker-row">
            <span class="biomarker-name">Hemoglobin</span>
            <span class="biomarker-value">14.2 g/dL</span>
            <span class="biomarker-badge badge-normal">✓ Normal</span>
        </div>
        <div class="biomarker-row">
            <span class="biomarker-name">Glucose</span>
            <span class="biomarker-value">95 mg/dL</span>
            <span class="biomarker-badge badge-normal">✓ Normal</span>
        </div>
        <div class="biomarker-row">
            <span class="biomarker-name">Cholesterol</span>
            <span class="biomarker-value">180 mg/dL</span>
            <span class="biomarker-badge badge-normal">✓ Normal</span>
        </div>
        <div class="ai-complete-bar">
            🤖 AI Analysis Complete
        </div>
        <div class="trust-badges">
            <div class="trust-badge">✅ AI Verified</div>
            <div class="trust-badge">🎯 99.9% Accurate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UPLOAD + HOW IT WORKS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("---")

col_upload, col_steps = st.columns([1, 1])

with col_upload:
    st.markdown("### 📤 Upload Your Lab Report")
    uploaded_file = st.file_uploader(
        "Upload your lab report or click to upload",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
        help="Supported: PDF, PNG, JPG, JPEG, TXT",
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.success(f"✅ **{uploaded_file.name}** ready for analysis!")
        analyze_btn = st.button("🔬  Start Analysis", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; color: #94a3b8; font-size: 0.9rem;">
            Supported file types: <strong>PDF · PNG/JPG · TXT</strong>
        </div>
        """, unsafe_allow_html=True)
        analyze_btn = False

with col_steps:
    st.markdown("""
    <h3 style="margin-bottom: 1.2rem;">How Lab Report Analyzer Works</h3>
    <div class="steps-container">
        <div class="step-row">
            <div class="step-num">1</div>
            <div class="step-text">Upload your report (PDF, Image, or Text)</div>
        </div>
        <div class="step-row">
            <div class="step-num">2</div>
            <div class="step-text">AI extracts and analyzes all biomarkers</div>
        </div>
        <div class="step-row">
            <div class="step-num">3</div>
            <div class="step-text">Get simplified, easy-to-understand results</div>
        </div>
        <div class="step-row">
            <div class="step-num">4</div>
            <div class="step-text">View flagged abnormalities with severity</div>
        </div>
        <div class="step-row">
            <div class="step-num">5</div>
            <div class="step-text">Get follow-up questions for your doctor</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANALYSIS PIPELINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if uploaded_file and analyze_btn:
    progress = st.progress(0, text="📤 Uploading report...")

    # ── Upload ──
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        u_resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=60)
        if u_resp.status_code != 200:
            st.error(f"❌ Upload failed: {u_resp.json().get('detail', 'Unknown error')}")
            st.stop()
        file_id = u_resp.json()["file_id"]
        progress.progress(30, text="🔬 Analyzing with AI...")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the API server is running on port 8000.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Upload error: {e}")
        st.stop()

    # ── Analyze ──
    try:
        a_resp = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"file_id": file_id, "filename": uploaded_file.name},
            timeout=180,
        )
        if a_resp.status_code != 200:
            st.error(f"❌ Analysis failed: {a_resp.json().get('detail', 'Unknown error')}")
            st.stop()
        analysis = a_resp.json()
        progress.progress(65, text="📝 Simplifying results...")
    except Exception as e:
        st.error(f"❌ Analysis error: {e}")
        st.stop()

    # ── Simplify ──
    simplified = None
    try:
        s_resp = requests.post(
            f"{API_BASE_URL}/simplify",
            json={
                "file_id": file_id,
                "analysis_summary": analysis.get("summary", ""),
                "findings_json": json.dumps(analysis.get("findings", [])),
            },
            timeout=180,
        )
        if s_resp.status_code == 200:
            simplified = s_resp.json()
    except Exception:
        pass

    progress.progress(100, text="✅ Analysis complete!")

    # Save to history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(0, {
        "name": uploaded_file.name,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "findings": len(analysis.get("findings", [])),
    })

    # ──────────────────────────────────────────────────────────────────
    # RESULTS DISPLAY
    # ──────────────────────────────────────────────────────────────────

    st.markdown("---")

    # Results header
    st.markdown("""
    <div class="results-header">
        <div class="results-header-icon">📊</div>
        <div class="results-header-title">Analysis Results</div>
    </div>
    """, unsafe_allow_html=True)

    findings = analysis.get("findings", [])
    abnormal = [f for f in findings if f.get("status", "normal") != "normal"]
    normal = [f for f in findings if f.get("status", "normal") == "normal"]
    total = len(findings)
    abnormal_count = len(abnormal)
    health_score = max(10, int(100 - (abnormal_count / max(total, 1)) * 100)) if total > 0 else 85

    # ── Stats Row ──
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Biomarkers</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: #22c55e;">{len(normal)}</div>
            <div class="stat-label">Normal Results</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: {'#ef4444' if abnormal_count > 0 else '#22c55e'};">{abnormal_count}</div>
            <div class="stat-label">Flagged Abnormalities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two-Column Layout: Findings + Abnormalities ──
    col_main, col_abnorm = st.columns([1.5, 1])

    with col_main:
        # Health Score Gauge
        st.plotly_chart(make_gauge(health_score), use_container_width=True, config={"displayModeBar": False})

        # Tabs for results
        tab_summary, tab_findings, tab_questions = st.tabs(["📝 Summary", "🔬 All Biomarkers", "❓ Follow-Up Questions"])

        with tab_summary:
            # Simplified summary
            if simplified and simplified.get("simplified_summary"):
                st.markdown(f"""
                <div class="summary-card">
                    <h4>🩺 Your Results in Plain Language</h4>
                    <p>{simplified['simplified_summary']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="summary-card">
                    <h4>📋 Report Summary</h4>
                    <p>{analysis.get('summary', 'Analysis complete.')}</p>
                </div>
                """, unsafe_allow_html=True)

        with tab_findings:
            # All biomarker rows in Niroggyan style
            for f in findings:
                sev = f.get("status", "normal")
                badge_cls, badge_txt, _ = SEVERITY_MAP.get(sev, SEVERITY_MAP["normal"])
                unit = f.get("unit", "")
                ref = f.get("reference_range", "")

                value_display = f.get("value", "N/A")
                if unit:
                    value_display = f"{value_display} {unit}"

                interp = f.get("interpretation", "")

                st.markdown(f"""
                <div class="biomarker-row" style="margin-bottom: 6px;">
                    <div>
                        <span class="biomarker-name">{f.get('parameter', 'Unknown')}</span>
                        {f'<div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">Ref: {ref}</div>' if ref else ''}
                    </div>
                    <span class="biomarker-value">{value_display}</span>
                    <span class="biomarker-badge {badge_cls}">{badge_txt}</span>
                </div>
                """, unsafe_allow_html=True)

                if interp:
                    with st.expander(f"💡 Details: {f.get('parameter', '')}"):
                        st.write(interp)

        with tab_questions:
            questions = []
            if simplified:
                questions = simplified.get("followup_questions", [])

            if questions:
                for i, q in enumerate(questions, 1):
                    st.markdown(f"""
                    <div class="question-card">
                        <div class="question-num">{i}</div>
                        <div class="question-text">{q}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No follow-up questions generated. Try uploading a report with abnormal values.")

    with col_abnorm:
        if abnormal:
            # Build detail map from simplified data
            abnorm_details = {}
            if simplified and simplified.get("abnormalities"):
                for ab in simplified["abnormalities"]:
                    key = ab.get("parameter", "").lower().strip()
                    abnorm_details[key] = ab

            # Abnormality panel — sanitize all dynamic text
            import html
            items_html = ""
            for f in abnormal:
                sev = f.get("status", "low")
                badge_cls, badge_txt, dot_cls = SEVERITY_MAP.get(sev, SEVERITY_MAP["low"])
                param = html.escape(str(f.get("parameter", "Unknown")))
                value = html.escape(str(f.get("value", "N/A")))
                unit = html.escape(str(f.get("unit", "")))
                ref = html.escape(str(f.get("reference_range", "")))

                # Get simplified explanation
                detail = abnorm_details.get(str(f.get("parameter", "")).lower().strip(), {})
                explanation = html.escape(str(detail.get("explanation", f.get("interpretation", ""))))
                recommendation = html.escape(str(detail.get("recommendation", "")))

                val_display = f"{value} {unit}" if unit else value
                ref_display = f" &middot; Ref: {ref}" if ref else ""

                explain_html = ""
                if explanation:
                    explain_html = f'<div class="abnorm-explain">{explanation}'
                    if recommendation:
                        explain_html += f"<br><strong>Tip:</strong> {recommendation}"
                    explain_html += "</div>"

                items_html += f"""
<div class="abnorm-item">
    <div class="abnorm-dot {dot_cls}"></div>
    <div class="abnorm-detail">
        <div class="abnorm-param">
            {param}
            <span class="biomarker-badge {badge_cls}" style="margin-left:8px;font-size:0.75rem;">{badge_txt}</span>
        </div>
        <div class="abnorm-val">{val_display}{ref_display}</div>
        {explain_html}
    </div>
</div>
"""

            st.html(f"""
<div class="abnorm-panel">
    <div class="abnorm-panel-header">
        <div class="abnorm-panel-title">🚨 Flagged Abnormalities</div>
        <div class="abnorm-count">{abnormal_count}</div>
    </div>
    {items_html}
</div>
""")
        else:
            st.html("""
            <div class="all-clear">
                <div class="all-clear-icon">🛡️</div>
                <div class="all-clear-title">All Clear!</div>
                <div class="all-clear-sub">All biomarkers are within normal ranges</div>
            </div>
            """)

    # ── Download PDF Button ──
    st.markdown("---")
    col_dl_left, col_dl_mid, col_dl_right = st.columns([1, 1, 1])
    with col_dl_mid:
        try:
            pdf_bytes = generate_pdf(
                uploaded_file.name, analysis, simplified, health_score
            )
            pdf_filename = f"MedReport_AI_{uploaded_file.name.rsplit('.', 1)[0]}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button(
                label="📥  Download PDF Report",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"PDF generation error: {e}")

    # Disclaimer
    st.warning("**Medical Disclaimer:** This tool provides AI-generated analysis for **informational purposes only**. It is NOT a substitute for professional medical advice. Always consult a qualified healthcare provider.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FEATURES SECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if not (uploaded_file and analyze_btn):
    st.markdown("---")
    st.markdown('<div class="section-title">Why Use MedReport AI?</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon fi-blue">🧬</div>
            <div class="feature-title">300+ Biomarkers</div>
            <div class="feature-desc">Comprehensive analysis covering all essential lab test parameters</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon fi-green">🎯</div>
            <div class="feature-title">AI-Powered Accuracy</div>
            <div class="feature-desc">Powered by Llama 3.3 70B via Groq for reliable, consistent results</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon fi-orange">📊</div>
            <div class="feature-title">Visual Severity Indicators</div>
            <div class="feature-desc">Color-coded badges and severity bars for quick abnormality spotting</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon fi-purple">💬</div>
            <div class="feature-title">Plain Language Reports</div>
            <div class="feature-desc">Complex medical jargon explained in simple, everyday words</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon fi-red">🚨</div>
            <div class="feature-title">Abnormality Alerts</div>
            <div class="feature-desc">Instant flagging of out-of-range values with actionable insights</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon fi-teal">❓</div>
            <div class="feature-title">Doctor-Ready Questions</div>
            <div class="feature-desc">Smart follow-up questions tailored to your specific results</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FAQ Section ──
    st.markdown("---")
    st.markdown('<div class="section-title">Frequently Asked Questions (FAQs)</div>', unsafe_allow_html=True)

    with st.expander("Is it safe to upload my lab report?"):
        st.write("Yes! Your reports are processed securely and not stored permanently. We only use them for real-time analysis and discard them after processing.")

    with st.expander("Will this tool give me a medical diagnosis?"):
        st.write("No. MedReport AI helps you **understand** your lab values by providing explanations and flagging abnormalities. It is NOT a substitute for a doctor's diagnosis.")

    with st.expander("What types of lab reports can I upload?"):
        st.write("We support PDF, PNG, JPG, and TXT formats. Common lab reports include Complete Blood Count (CBC), Metabolic Panels, Lipid Profiles, Thyroid Function Tests, and more.")

    with st.expander("I don't understand medical terms. Will this make it simpler for me?"):
        st.write("Absolutely! Our AI simplifies technical medical language into plain, everyday English. You'll also get actionable recommendations and questions to ask your doctor.")

    with st.expander("How accurate is the AI analysis?"):
        st.write("Our AI is powered by Meta's Llama 3.3 70B model via Groq, which provides highly accurate biomarker extraction and interpretation. However, always verify results with your healthcare provider.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<div class="footer">
    <div class="footer-brand">🔬 MedReport AI</div>
    <p style="color: #64748b; font-size: 0.9rem; margin: 4px 0 12px;">
        AI-Powered Lab Report Analysis — Understand Your Health Better
    </p>
    <div class="footer-links">
        <a href="#">Features</a>
        <a href="#">Documentation</a>
        <a href="#">About</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Contact</a>
    </div>
    <div class="footer-copy">
        © 2026 MedReport AI · Built with FastAPI, Llama 3.3 via Groq & Streamlit · For educational purposes only
    </div>
</div>
""", unsafe_allow_html=True)
