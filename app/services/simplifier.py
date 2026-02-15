"""
Simplifier Service — Transforms medical reports into patient-friendly language.

Uses Google Gemini 2.0 Flash for:
- Simplifying technical medical jargon into plain language
- Flagging abnormalities with severity levels and explanations
- Generating follow-up questions for the doctor
"""

import json
import google.generativeai as genai

from app.config import get_settings
from app.models.schemas import (
    SimplifiedReport,
    AbnormalityFlag,
    SeverityLevel,
)

settings = get_settings()


def _configure_gemini():
    """Configure the Gemini API client."""
    genai.configure(api_key=settings.GEMINI_API_KEY)


SIMPLIFY_SYSTEM_PROMPT = """You are a friendly medical communication expert. Your job is to take medical report analysis and transform it into language that a patient with no medical background can easily understand.

RULES:
1. Use simple, everyday language — avoid all medical jargon
2. Be empathetic and reassuring, but honest
3. Clearly highlight anything that is abnormal or concerning
4. Suggest practical, relevant follow-up questions the patient should ask their doctor
5. NEVER provide medical diagnosis or treatment recommendations
6. Always remind the patient to consult their doctor

Return a JSON response with this EXACT structure:
{
    "simplified_summary": "A clear, friendly 3-5 sentence summary of the report in simple language. Use analogies where helpful.",
    "abnormalities": [
        {
            "parameter": "Name of the test (use common name)",
            "value": "The value found",
            "severity": "normal" | "low" | "medium" | "high" | "critical",
            "explanation": "What this means in simple, everyday language",
            "recommendation": "What the patient should know or do about this"
        }
    ],
    "followup_questions": [
        "Question 1 the patient should ask their doctor",
        "Question 2 the patient should ask their doctor",
        "Question 3 the patient should ask their doctor"
    ]
}

Generate at least 3-5 follow-up questions that are specific and relevant to the findings.
Always respond with ONLY the JSON object, no additional text."""


def simplify_report(analysis_summary: str, findings_json: str, file_id: str) -> SimplifiedReport:
    """
    Simplify a medical report analysis into patient-friendly language.

    Args:
        analysis_summary: The AI-generated summary from the analyzer.
        findings_json: JSON string of the structured findings.
        file_id: Unique identifier for the file.

    Returns:
        SimplifiedReport with plain-language summary, flagged abnormalities,
        and suggested follow-up questions.
    """
    _configure_gemini()

    model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        system_instruction=SIMPLIFY_SYSTEM_PROMPT,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            response_mime_type="application/json",
        ),
    )

    user_prompt = f"""Please simplify the following medical report analysis for a patient:

SUMMARY:
{analysis_summary}

DETAILED FINDINGS:
{findings_json}

Transform this into simple, patient-friendly language. Flag any abnormalities and suggest follow-up questions."""

    response = model.generate_content(user_prompt)

    # Parse response
    result = json.loads(response.text)

    # Build abnormality flags
    abnormalities = []
    for ab in result.get("abnormalities", []):
        severity_str = ab.get("severity", "normal").lower().strip()
        try:
            severity = SeverityLevel(severity_str)
        except ValueError:
            # Map common AI variations
            fallback = {
                "borderline": SeverityLevel.LOW,
                "slightly elevated": SeverityLevel.LOW,
                "slightly low": SeverityLevel.LOW,
                "elevated": SeverityLevel.MEDIUM,
                "abnormal": SeverityLevel.MEDIUM,
                "moderate": SeverityLevel.MEDIUM,
                "mild": SeverityLevel.LOW,
                "severe": SeverityLevel.HIGH,
                "very high": SeverityLevel.CRITICAL,
                "very low": SeverityLevel.HIGH,
                "within range": SeverityLevel.NORMAL,
                "within normal limits": SeverityLevel.NORMAL,
            }
            severity = fallback.get(severity_str, SeverityLevel.LOW)

        abnormalities.append(
            AbnormalityFlag(
                parameter=ab.get("parameter", "Unknown"),
                value=ab.get("value", "N/A"),
                severity=severity,
                explanation=ab.get("explanation", ""),
                recommendation=ab.get("recommendation"),
            )
        )

    return SimplifiedReport(
        file_id=file_id,
        original_summary=analysis_summary,
        simplified_summary=result.get("simplified_summary", "Analysis complete."),
        abnormalities=abnormalities,
        followup_questions=result.get("followup_questions", []),
    )
