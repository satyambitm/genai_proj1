"""
Analyze Router — Triggers AI analysis on uploaded reports.

- POST /api/analyze — Analyze an uploaded medical report
"""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import get_settings
from app.models.schemas import AnalysisResponse
from app.services.parser import detect_file_type, extract_text
from app.services.analyzer import analyze_text_report, analyze_image_report

router = APIRouter(prefix="/api", tags=["Analysis"])
settings = get_settings()


class AnalyzeRequest(BaseModel):
    file_id: str = Field(..., description="File ID returned from the upload endpoint")
    filename: str = Field(..., description="Original filename")


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_report(request: AnalyzeRequest):
    """
    Analyze an uploaded medical report using AI.

    - For text/PDF reports: uses GPT-4 for structured text analysis
    - For image/scanned reports: uses GPT-4 Vision for visual analysis
    """
    # ── Locate the uploaded file ───────────────────────────────────────
    upload_dir = settings.UPLOAD_DIR
    safe_filename = f"{request.file_id}_{request.filename}"
    file_path = os.path.join(upload_dir, safe_filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found. Please upload the file first using /api/upload",
        )

    # ── Determine analysis method ──────────────────────────────────────
    file_type = detect_file_type(request.filename)
    extracted_text = extract_text(file_path, request.filename)

    try:
        if extracted_text:
            # Text-based analysis (PDF with text or .txt files)
            result = analyze_text_report(extracted_text, request.file_id)
        else:
            # Image-based analysis (scanned PDFs, images)
            result = analyze_image_report(file_path, request.file_id)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}",
        )
