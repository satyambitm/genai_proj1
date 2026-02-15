# 🏥 MedReport AI — Medical Report Analyzer & Simplifier

An **AI-powered medical report analysis tool** built with **FastAPI**, **OpenAI GPT-4/Vision**, **ChromaDB**, and **Streamlit**. Upload medical reports (lab tests, radiology reports, prescriptions) and get:

- ✅ **Structured analysis** — extracts key findings, values, and reference ranges
- ✅ **Patient-friendly summaries** — translates medical jargon into plain language
- ✅ **Abnormality flagging** — highlights out-of-range values with severity levels
- ✅ **Follow-up questions** — suggests relevant questions to ask your doctor
- ✅ **RAG-enhanced accuracy** — uses medical knowledge base for context-aware responses

> ⚠️ **Disclaimer**: This tool is for **informational purposes only** and is NOT a substitute for professional medical advice.

---

## 🏗️ Architecture

```
medreport-ai/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # App configuration
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── upload.py            # File upload endpoints
│   │   ├── analyze.py           # AI analysis endpoints
│   │   └── simplify.py          # Simplification endpoints
│   ├── services/
│   │   ├── parser.py            # PDF/image/text parsing
│   │   ├── analyzer.py          # OpenAI GPT-4 analysis
│   │   ├── simplifier.py        # Report simplification
│   │   └── rag_engine.py        # RAG with ChromaDB
│   ├── prompts/
│   │   └── medical_prompts.py   # AI prompt templates
│   └── data/
│       └── medical_references/  # RAG knowledge base docs
├── frontend/
│   └── app.py                   # Streamlit dashboard
├── tests/                       # Unit & integration tests
├── uploads/                     # Uploaded report files
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd genai_proj1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run Backend

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run Frontend

```bash
streamlit run frontend/app.py
```

### 5. API Docs

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | *required* |
| `OPENAI_MODEL` | Model for text analysis | `gpt-4o` |
| `OPENAI_VISION_MODEL` | Model for image analysis | `gpt-4o` |
| `MAX_FILE_SIZE_MB` | Max upload file size | `10` |

---

## 🌿 Branch Strategy

| Branch | Feature |
|--------|---------|
| `main` | Project setup & base structure |
| `feature/report-upload` | File upload & PDF/image parsing |
| `feature/ai-analysis` | OpenAI GPT-4 / Vision analysis |
| `feature/report-simplifier` | Patient-friendly output & abnormality flags |
| `feature/rag-knowledge` | ChromaDB RAG knowledge base |
| `feature/frontend` | Streamlit UI dashboard |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **AI**: OpenAI GPT-4o / GPT-4 Vision, LangChain
- **Vector DB**: ChromaDB
- **Document Parsing**: PyMuPDF, Pillow
- **Frontend**: Streamlit
- **Testing**: Pytest, HTTPX

---

## 📄 License

This project is for educational purposes. MIT License.
