"""
Simplify Router — Full pipeline: upload → analyze → simplify.

- POST /api/simplify — Accepts analysis results and returns simplified report
"""

import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.schemas import SimplifiedReport, Finding
from app.services.simplifier import simplify_report

router = APIRouter(prefix="/api", tags=["Simplification"])


class SimplifyRequest(BaseModel):
    file_id: str = Field(..., description="File ID of the report")
    summary: str = Field(..., description="Analysis summary from the analyze endpoint")
    findings: list[Finding] = Field(..., description="List of findings from the analyze endpoint")


@router.post("/simplify", response_model=SimplifiedReport)
async def simplify_medical_report(request: SimplifyRequest):
    """
    Simplify a medical report analysis into patient-friendly language.

    Takes the output of /api/analyze and returns:
    - A simplified summary in plain language
    - Flagged abnormalities with explanations
    - Suggested follow-up questions for the doctor
    """
    try:
        # Convert findings to JSON string for the simplifier
        findings_json = json.dumps(
            [f.model_dump() for f in request.findings], indent=2, default=str
        )

        result = simplify_report(
            analysis_summary=request.summary,
            findings_json=findings_json,
            file_id=request.file_id,
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simplification failed: {str(e)}",
        )
