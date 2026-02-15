"""
Pydantic models for API request and response schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ── Enums ──────────────────────────────────────────────────────────────

class ReportType(str, Enum):
    LAB_TEST = "lab_test"
    RADIOLOGY = "radiology"
    PRESCRIPTION = "prescription"
    GENERAL = "general"


class SeverityLevel(str, Enum):
    NORMAL = "normal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Upload Schemas ─────────────────────────────────────────────────────

class UploadResponse(BaseModel):
    file_id: str = Field(..., description="Unique identifier for the uploaded file")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="Detected file type (pdf/image/text)")
    file_size_bytes: int = Field(..., description="File size in bytes")
    extracted_text: Optional[str] = Field(None, description="Text extracted from the file")
    upload_time: datetime = Field(default_factory=datetime.now)
    message: str = "File uploaded successfully"


# ── Analysis Schemas ───────────────────────────────────────────────────

class Finding(BaseModel):
    parameter: str = Field(..., description="Name of the medical parameter/test")
    value: str = Field(..., description="Measured value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    reference_range: Optional[str] = Field(None, description="Normal reference range")
    status: SeverityLevel = Field(SeverityLevel.NORMAL, description="Severity status")
    interpretation: Optional[str] = Field(None, description="Brief interpretation")


class AnalysisResponse(BaseModel):
    file_id: str
    report_type: ReportType = ReportType.GENERAL
    summary: str = Field(..., description="Overall summary of the report")
    findings: list[Finding] = Field(default_factory=list, description="List of extracted findings")
    medical_terms: list[str] = Field(default_factory=list, description="Medical terminology found")
    raw_text: Optional[str] = Field(None, description="Extracted raw text")
    analysis_time: datetime = Field(default_factory=datetime.now)


# ── Simplification Schemas ─────────────────────────────────────────────

class AbnormalityFlag(BaseModel):
    parameter: str
    value: str
    severity: SeverityLevel
    explanation: str = Field(..., description="Patient-friendly explanation of the abnormality")
    recommendation: Optional[str] = Field(None, description="What this could mean")


class SimplifiedReport(BaseModel):
    file_id: str
    original_summary: str
    simplified_summary: str = Field(..., description="Patient-friendly summary")
    abnormalities: list[AbnormalityFlag] = Field(default_factory=list)
    followup_questions: list[str] = Field(
        default_factory=list,
        description="Suggested questions to ask the doctor"
    )
    disclaimer: str = Field(
        default="⚠️ DISCLAIMER: This AI-generated analysis is for informational purposes only. "
                "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
                "Always consult a qualified healthcare provider for medical decisions."
    )


# ── General ────────────────────────────────────────────────────────────

class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    app_name: str
    version: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
