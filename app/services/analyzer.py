"""
Analyzer Service — Core AI engine for medical report analysis.

Uses Groq API (Llama 3.3 70B for text, Llama 3.2 90B Vision for images).
Returns structured findings with severity classification.
"""

import json
import base64
import time
from typing import Optional
from pathlib import Path

from groq import Groq

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


def _get_client() -> Groq:
    """Get a configured Groq client."""
    return Groq(api_key=settings.GROQ_API_KEY, timeout=120.0)


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


def _generate_with_retry(
    system_prompt: str,
    user_content,
    model_name: str | None = None,
    max_retries: int = 3,
) -> str:
    """
    Generate content with automatic retry and model fallback.
    Handles 429 rate limit errors by waiting and falling back to alternative models.
    """
    client = _get_client()

    models_to_try = [
        model_name or settings.GROQ_MODEL,
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
    ]

    for model in models_to_try:
        for attempt in range(max_retries):
            try:
                # Build messages — user_content is always a string for text
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ]

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=4096,
                    response_format={"type": "json_object"},
                )
                return response.choices[0].message.content

            except Exception as e:
                error_str = str(e).lower()
                if "429" in str(e) or "rate" in error_str or "quota" in error_str or "limit" in error_str:
                    wait_time = (attempt + 1) * 3  # 3s, 6s, 9s
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        break  # try next model
                else:
                    raise e

    raise Exception(
        "All models and retries exhausted. "
        "Please check your Groq API key at https://console.groq.com/keys"
    )


def _generate_vision_with_retry(
    system_prompt: str,
    text_prompt: str,
    image_data: bytes,
    mime_type: str,
    max_retries: int = 3,
) -> str:
    """
    Generate content from image using Groq Vision model with retry.
    """
    client = _get_client()
    b64_image = base64.b64encode(image_data).decode("utf-8")

    models_to_try = [
        settings.GROQ_VISION_MODEL,
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview",
    ]

    for model in models_to_try:
        for attempt in range(max_retries):
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{b64_image}",
                                },
                            },
                        ],
                    },
                ]

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.1,
                    max_tokens=4096,
                )
                return response.choices[0].message.content

            except Exception as e:
                error_str = str(e).lower()
                if "429" in str(e) or "rate" in error_str or "limit" in error_str:
                    wait_time = (attempt + 1) * 3
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        break
                else:
                    raise e

    raise Exception(
        "All vision models and retries exhausted. "
        "Please check your Groq API key at https://console.groq.com/keys"
    )


def analyze_text_report(report_text: str, file_id: str) -> AnalysisResponse:
    """
    Analyze a text-based medical report using Groq.

    Args:
        report_text: Extracted text content from the medical report.
        file_id: Unique identifier for the uploaded file.

    Returns:
        AnalysisResponse with structured findings.
    """
    user_prompt = TEXT_ANALYSIS_USER_PROMPT.format(report_text=report_text)
    response_text = _generate_with_retry(TEXT_ANALYSIS_SYSTEM_PROMPT, user_prompt)

    result = _parse_ai_response(response_text)
    return _build_analysis_response(result, file_id, report_text)


def analyze_image_report(image_path: str, file_id: str) -> AnalysisResponse:
    """
    Analyze an image-based medical report using Groq Vision.

    Args:
        image_path: Path to the image file.
        file_id: Unique identifier for the uploaded file.

    Returns:
        AnalysisResponse with structured findings.
    """
    image_path_obj = Path(image_path)
    image_data = image_path_obj.read_bytes()

    ext = image_path_obj.suffix.lower().lstrip(".")
    mime_map = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}
    mime_type = mime_map.get(ext, "image/png")

    response_text = _generate_vision_with_retry(
        IMAGE_ANALYSIS_SYSTEM_PROMPT,
        IMAGE_ANALYSIS_USER_PROMPT,
        image_data,
        mime_type,
    )

    result = _parse_ai_response(response_text)
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

    # Fuzzy matching
    for key, level in mapping.items():
        if key in raw or raw in key:
            return level

    return SeverityLevel.LOW


def _build_analysis_response(
    result: dict, file_id: str, raw_text: Optional[str] = None
) -> AnalysisResponse:
    """Build a structured AnalysisResponse from the parsed AI output."""

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
