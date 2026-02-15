"""
Analyzer Service — Core AI engine for medical report analysis.

Uses Google Gemini 2.0 Flash for text reports and image/scanned reports.
Returns structured findings with severity classification.
"""

import json
import base64
from typing import Optional
from pathlib import Path

import google.generativeai as genai

from app.config import get_settings
from app.prompts.medical_prompts import (
    TEXT_ANALYSIS_SYSTEM_PROMPT,
    TEXT_ANALYSIS_USER_PROMPT,
    IMAGE_ANALYSIS_SYSTEM_PROMPT,
    IMAGE_ANALYSIS_USER_PROMPT,
)
from app.models.schemas import (
    AnalysisResponse,
    Finding,
    ReportType,
    SeverityLevel,
)

settings = get_settings()


def _configure_gemini():
    """Configure the Gemini API client."""
    genai.configure(api_key=settings.GEMINI_API_KEY)


def _parse_ai_response(response_text: str) -> dict:
    """
    Parse the AI response JSON string into a dictionary.
    Handles cases where the model wraps JSON in markdown code blocks.
    """
    text = response_text.strip()

    # Remove markdown code block wrappers if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())


def analyze_text_report(report_text: str, file_id: str) -> AnalysisResponse:
    """
    Analyze a text-based medical report using Google Gemini.

    Args:
        report_text: Extracted text content from the medical report.
        file_id: Unique identifier for the uploaded file.

    Returns:
        AnalysisResponse with structured findings.
    """
    _configure_gemini()

    model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        system_instruction=TEXT_ANALYSIS_SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    user_prompt = TEXT_ANALYSIS_USER_PROMPT.format(report_text=report_text)
    response = model.generate_content(user_prompt)

    result = _parse_ai_response(response.text)
    return _build_analysis_response(result, file_id, report_text)


def analyze_image_report(image_path: str, file_id: str) -> AnalysisResponse:
    """
    Analyze an image-based medical report using Google Gemini Vision.

    Args:
        image_path: Path to the image file.
        file_id: Unique identifier for the uploaded file.

    Returns:
        AnalysisResponse with structured findings.
    """
    _configure_gemini()

    model = genai.GenerativeModel(
        model_name=settings.GEMINI_VISION_MODEL,
        system_instruction=IMAGE_ANALYSIS_SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )

    # Read the image file
    image_path_obj = Path(image_path)
    image_data = image_path_obj.read_bytes()

    # Determine MIME type
    ext = image_path_obj.suffix.lower().lstrip(".")
    mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
    mime_type = mime_map.get(ext, "image/png")

    # Create image part for Gemini
    image_part = {
        "mime_type": mime_type,
        "data": image_data,
    }

    response = model.generate_content([IMAGE_ANALYSIS_USER_PROMPT, image_part])

    result = _parse_ai_response(response.text)
    return _build_analysis_response(result, file_id)


def _normalize_severity(raw: str) -> SeverityLevel:
    """
    Normalize AI severity string to a valid SeverityLevel.
    Handles unexpected values like 'borderline', 'slightly elevated', etc.
    """
    raw = raw.lower().strip()

    # Direct match
    try:
        return SeverityLevel(raw)
    except ValueError:
        pass

    # Map common AI variations to valid levels
    mapping = {
        "borderline": SeverityLevel.LOW,
        "slightly elevated": SeverityLevel.LOW,
        "slightly low": SeverityLevel.LOW,
        "elevated": SeverityLevel.MEDIUM,
        "abnormal": SeverityLevel.MEDIUM,
        "mildly abnormal": SeverityLevel.LOW,
        "moderately abnormal": SeverityLevel.MEDIUM,
        "severely abnormal": SeverityLevel.HIGH,
        "moderate": SeverityLevel.MEDIUM,
        "mild": SeverityLevel.LOW,
        "severe": SeverityLevel.HIGH,
        "very high": SeverityLevel.CRITICAL,
        "very low": SeverityLevel.HIGH,
        "extremely high": SeverityLevel.CRITICAL,
        "extremely low": SeverityLevel.CRITICAL,
        "out of range": SeverityLevel.MEDIUM,
        "within range": SeverityLevel.NORMAL,
        "within normal limits": SeverityLevel.NORMAL,
        "ok": SeverityLevel.NORMAL,
        "fine": SeverityLevel.NORMAL,
        "good": SeverityLevel.NORMAL,
        "warning": SeverityLevel.MEDIUM,
        "danger": SeverityLevel.HIGH,
        "urgent": SeverityLevel.CRITICAL,
    }

    if raw in mapping:
        return mapping[raw]

    # Fuzzy matching — check if any keyword is contained in the string
    for key, level in mapping.items():
        if key in raw or raw in key:
            return level

    # Default fallback
    return SeverityLevel.LOW


def _build_analysis_response(
    result: dict, file_id: str, raw_text: Optional[str] = None
) -> AnalysisResponse:
    """Build a structured AnalysisResponse from the parsed AI output."""

    # Map findings
    findings = []
    for f in result.get("findings", []):
        findings.append(
            Finding(
                parameter=f.get("parameter", "Unknown"),
                value=f.get("value", "N/A"),
                unit=f.get("unit"),
                reference_range=f.get("reference_range"),
                status=_normalize_severity(f.get("status", "normal")),
                interpretation=f.get("interpretation"),
            )
        )

    # Map report type
    report_type_str = result.get("report_type", "general")
    try:
        report_type = ReportType(report_type_str)
    except ValueError:
        report_type = ReportType.GENERAL

    return AnalysisResponse(
        file_id=file_id,
        report_type=report_type,
        summary=result.get("summary", "Analysis complete."),
        findings=findings,
        medical_terms=result.get("medical_terms", []),
        raw_text=raw_text,
    )
