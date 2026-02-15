"""
MedReport AI — Streamlit Frontend Dashboard.

A modern, clean UI for uploading medical reports and viewing AI analysis results.
Connects to the FastAPI backend API.
"""

import streamlit as st
import requests
import json
import time

# ── Page Config ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="MedReport AI — Medical Report Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0d9488 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(13, 148, 136, 0.2);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }
    .main-header p {
        font-size: 1rem;
        opacity: 0.85;
        margin: 0;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        color: #92400e;
    }

    /* Cards */
    .result-card {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Severity badges */
    .severity-normal { color: #065f46; background: #d1fae5; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .severity-low { color: #92400e; background: #fef3c7; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .severity-medium { color: #9a3412; background: #ffedd5; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .severity-high { color: #991b1b; background: #fee2e2; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .severity-critical { color: #ffffff; background: #dc2626; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }

    /* Upload area */
    .upload-area {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Findings table */
    .findings-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 1rem;
    }

    /* Question list */
    .question-item {
        background: #f0f9ff;
        border-left: 3px solid #0ea5e9;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.95rem;
    }

    /* Stats cards */
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0d9488;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.3rem;
    }

    /* Sidebar */
    .sidebar-info {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ── API Config ─────────────────────────────────────────────────────────

API_BASE_URL = "http://localhost:8000/api"


# ── Sidebar ────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Settings")

    api_url = st.text_input(
        "Backend API URL",
        value="http://localhost:8000",
        help="URL of the FastAPI backend server"
    )
    API_BASE_URL = f"{api_url}/api"

    st.markdown("---")

    st.markdown("### 📋 How It Works")
    st.markdown("""
    <div class="sidebar-info">
    <strong>1.</strong> Upload a medical report (PDF, image, or text)<br>
    <strong>2.</strong> AI extracts and analyzes key findings<br>
    <strong>3.</strong> Get simplified explanations in plain language<br>
    <strong>4.</strong> View flagged abnormalities with severity<br>
    <strong>5.</strong> Get follow-up questions for your doctor
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Supported Formats")
    st.markdown("- 📄 PDF (text or scanned)")
    st.markdown("- 🖼️ Images (PNG, JPG, JPEG)")
    st.markdown("- 📝 Text files (TXT)")

    st.markdown("---")
    st.markdown("### 🔬 Report History")

    if "history" in st.session_state and st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"📄 {item['filename']}", expanded=False):
                st.caption(f"Type: {item.get('report_type', 'N/A')}")
                st.caption(f"Findings: {item.get('findings_count', 0)}")
    else:
        st.caption("No reports analyzed yet.")


# ── Session State ──────────────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = []


# ── Main Content ───────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>🏥 MedReport AI</h1>
    <p>AI-Powered Medical Report Analyzer & Simplifier — Upload your medical reports and get instant, easy-to-understand analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-box">
    ⚠️ <strong>Medical Disclaimer:</strong> This tool is for <strong>informational purposes only</strong>.
    AI-generated analysis is NOT a substitute for professional medical advice, diagnosis, or treatment.
    Always consult a qualified healthcare provider for medical decisions.
</div>
""", unsafe_allow_html=True)


# ── Upload Section ─────────────────────────────────────────────────────

st.markdown("### 📤 Upload Medical Report")

uploaded_file = st.file_uploader(
    "Upload your medical report",
    type=["pdf", "png", "jpg", "jpeg", "txt"],
    help="Supported formats: PDF, PNG, JPG, JPEG, TXT (max 10MB)",
    label_visibility="collapsed",
)

col_upload, col_info = st.columns([2, 1])

with col_info:
    st.markdown("""
    <div class="result-card">
        <strong>💡 Tips for best results:</strong>
        <ul style="font-size: 0.9rem; margin-top: 0.5rem;">
            <li>Ensure the report is clear and readable</li>
            <li>For scanned reports, use high-resolution images</li>
            <li>Crop out unnecessary margins</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ── Analysis Pipeline ─────────────────────────────────────────────────

if uploaded_file is not None:
    with col_upload:
        st.success(f"📄 **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

    analyze_btn = st.button("🔬 Analyze Report", type="primary", use_container_width=True)

    if analyze_btn:
        # ── Step 1: Upload ─────────────────────────────────────────
        with st.spinner("📤 Uploading report..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                upload_resp = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)

                if upload_resp.status_code != 200:
                    st.error(f"❌ Upload failed: {upload_resp.json().get('detail', 'Unknown error')}")
                    st.stop()

                upload_data = upload_resp.json()
                file_id = upload_data["file_id"]
                st.success("✅ Report uploaded successfully!")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the backend API. Make sure the server is running at: " + api_url)
                st.info("💡 Run: `uvicorn app.main:app --reload --port 8000`")
                st.stop()
            except Exception as e:
                st.error(f"❌ Upload error: {str(e)}")
                st.stop()

        # ── Step 2: Analyze ────────────────────────────────────────
        with st.spinner("🧠 AI is analyzing your report... This may take a moment."):
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

            except Exception as e:
                st.error(f"❌ Analysis error: {str(e)}")
                st.stop()

        # ── Step 3: Simplify ───────────────────────────────────────
        with st.spinner("📝 Generating simplified report..."):
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

                if simplify_resp.status_code == 200:
                    simplified_data = simplify_resp.json()
                else:
                    simplified_data = None

            except Exception:
                simplified_data = None

        # ── Save to history ────────────────────────────────────────
        st.session_state.history.append({
            "filename": uploaded_file.name,
            "file_id": file_id,
            "report_type": analysis_data.get("report_type", "N/A"),
            "findings_count": len(analysis_data.get("findings", [])),
        })

        # ── Display Results ────────────────────────────────────────
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        # Stats Row
        findings = analysis_data.get("findings", [])
        abnormal_count = sum(1 for f in findings if f.get("status", "normal") != "normal")

        stat_cols = st.columns(4)
        with stat_cols[0]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(findings)}</div>
                <div class="stat-label">Total Findings</div>
            </div>
            """, unsafe_allow_html=True)
        with stat_cols[1]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: {'#dc2626' if abnormal_count > 0 else '#065f46'};">{abnormal_count}</div>
                <div class="stat-label">Abnormalities</div>
            </div>
            """, unsafe_allow_html=True)
        with stat_cols[2]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{analysis_data.get('report_type', 'N/A').replace('_', ' ').title()}</div>
                <div class="stat-label">Report Type</div>
            </div>
            """, unsafe_allow_html=True)
        with stat_cols[3]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(analysis_data.get('medical_terms', []))}</div>
                <div class="stat-label">Medical Terms</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")

        # Two Column Layout
        result_col1, result_col2 = st.columns([3, 2])

        with result_col1:
            # Summary
            st.markdown("### 📋 Summary")
            st.markdown(f"""<div class="result-card">{analysis_data.get('summary', 'N/A')}</div>""", unsafe_allow_html=True)

            # Simplified Summary
            if simplified_data:
                st.markdown("### 💬 Simplified Explanation")
                st.markdown(f"""<div class="result-card">{simplified_data.get('simplified_summary', 'N/A')}</div>""", unsafe_allow_html=True)

            # Findings Table
            if findings:
                st.markdown("### 🔬 Detailed Findings")
                for f in findings:
                    severity = f.get("status", "normal")
                    icon = {"normal": "✅", "low": "⚠️", "medium": "🟠", "high": "🔴", "critical": "🚨"}.get(severity, "ℹ️")
                    with st.expander(f"{icon} **{f['parameter']}** — {f['value']} {f.get('unit', '')}", expanded=(severity != "normal")):
                        st.markdown(f"**Reference Range:** {f.get('reference_range', 'N/A')}")
                        st.markdown(f"**Status:** `{severity.upper()}`")
                        st.markdown(f"**Interpretation:** {f.get('interpretation', 'N/A')}")

        with result_col2:
            # Abnormalities
            if simplified_data and simplified_data.get("abnormalities"):
                st.markdown("### 🚩 Flagged Abnormalities")
                for ab in simplified_data["abnormalities"]:
                    severity = ab.get("severity", "normal")
                    if severity == "normal":
                        continue
                    st.markdown(f"""
                    <div class="result-card">
                        <strong>{ab['parameter']}</strong>: {ab['value']}
                        <span class="severity-{severity}">{severity.upper()}</span>
                        <p style="margin-top: 0.5rem; font-size: 0.9rem;">{ab.get('explanation', '')}</p>
                        <p style="font-size: 0.85rem; color: #64748b;"><em>{ab.get('recommendation', '')}</em></p>
                    </div>
                    """, unsafe_allow_html=True)

            # Follow-up Questions
            if simplified_data and simplified_data.get("followup_questions"):
                st.markdown("### 💡 Questions for Your Doctor")
                for q in simplified_data["followup_questions"]:
                    st.markdown(f"""<div class="question-item">❓ {q}</div>""", unsafe_allow_html=True)

            # Medical Terms
            if analysis_data.get("medical_terms"):
                st.markdown("### 📖 Medical Terms Found")
                terms_html = " ".join(
                    [f'<span style="background: #e0f2fe; padding: 3px 10px; border-radius: 15px; font-size: 0.85rem; margin: 3px; display: inline-block;">{term}</span>'
                     for term in analysis_data["medical_terms"]]
                )
                st.markdown(terms_html, unsafe_allow_html=True)

        # Disclaimer
        st.markdown("---")
        if simplified_data:
            st.warning(simplified_data.get("disclaimer", ""))
        else:
            st.warning(
                "⚠️ DISCLAIMER: This AI-generated analysis is for informational purposes only. "
                "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
                "Always consult a qualified healthcare provider for medical decisions."
            )
