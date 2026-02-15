"""
Simplifier Service — Transforms medical reports into patient-friendly language.

Features:
- Simplify technical medical jargon into plain language
- Flag abnormalities with severity levels and explanations
- Generate follow-up questions for the doctor
"""

import json
from openai import OpenAI

from app.config import get_settings
from app.models.schemas import (
    SimplifiedReport,
    AbnormalityFlag,
    SeverityLevel,
)

settings = get_settings()


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client instance."""
    return OpenAI(api_key=settings.OPENAI_API_KEY)


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
    client = _get_openai_client()

    user_prompt = f"""Please simplify the following medical report analysis for a patient:

SUMMARY:
{analysis_summary}

DETAILED FINDINGS:
{findings_json}

Transform this into simple, patient-friendly language. Flag any abnormalities and suggest follow-up questions."""

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SIMPLIFY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    # Parse response
    text = response.choices[0].message.content or "{}"
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    result = json.loads(text.strip())

    # Build abnormality flags
    abnormalities = []
    for ab in result.get("abnormalities", []):
        severity_str = ab.get("severity", "normal").lower().strip()
        try:
            severity = SeverityLevel(severity_str)
        except ValueError:
            # Map common GPT variations
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
