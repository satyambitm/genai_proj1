"""
MedReport AI — FastAPI Application Entry Point.

An AI-powered medical report analyzer that extracts key findings,
simplifies them into patient-friendly language, flags abnormalities,
and suggests follow-up questions for the doctor.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models.schemas import HealthCheckResponse

settings = get_settings()

# ── App Instance ───────────────────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-Powered Medical Report Analyzer & Simplifier. "
        "Upload medical reports (lab tests, radiology, prescriptions) and get "
        "AI-driven analysis, simplified explanations, abnormality flags, "
        "and follow-up question suggestions."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS Middleware ────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ───────────────────────────────────────────────────────

@app.get("/", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """Health check endpoint — verifies the API is running."""
    return HealthCheckResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health():
    """Alias for health check."""
    return HealthCheckResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
