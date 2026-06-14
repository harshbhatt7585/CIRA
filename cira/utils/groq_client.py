"""Groq API client for incident understanding and summary generation."""

import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Model name — change here if needed
GROQ_MODEL = "llama-3.3-70b-versatile"

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_client: Groq | None = None


def _get_api_key() -> str | None:
    return os.getenv("GROQ_API_KEY")


def _ensure_client() -> Groq:
    global _client
    api_key = _get_api_key()
    if not api_key or api_key == "your_key_here":
        raise ValueError(
            "GROQ_API_KEY is missing or not set. Copy .env.example to .env and add your key."
        )
    if _client is None:
        _client = Groq(api_key=api_key)
    return _client


def _extract_json(text: str) -> dict:
    """Extract JSON object from model response, handling markdown fences."""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            return json.loads(brace_match.group())
        raise ValueError(f"Could not parse JSON from model response: {text[:200]}")


def _safe_groq_call(prompt: str) -> dict:
    """Call Groq and return parsed JSON, or error dict on failure."""
    try:
        client = _ensure_client()
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        if not content:
            return {"error": "Empty response from Groq API."}
        return _extract_json(content)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower() or "rate" in err.lower():
            return {"error": "Groq API rate limit reached. Please wait and try again."}
        if "API key" in err or "401" in err or "403" in err or "invalid" in err.lower():
            return {"error": "Invalid or unauthorized GROQ_API_KEY."}
        return {"error": f"Groq API error: {err}"}


def understand_incident(user_text: str, category_list: list[str]) -> dict:
    """
    Analyze victim's account and suggest an official subcategory.

    Returns dict with keys: summary, suggested_category, confidence
    Or: error key on failure
    """
    categories_formatted = "\n".join(f"- {name}" for name in category_list)
    prompt = f"""You are CIRA (Cyber Incidence Response Assistant) helping cybercrime victims in India.

The victim describes their incident:
\"\"\"
{user_text}
\"\"\"

Official subcategory names (choose exactly one):
{categories_formatted}

Respond with ONLY valid JSON (no markdown):
{{
  "summary": "2-3 sentence plain-language summary of what happened",
  "suggested_category": "exact subcategory name from the list above",
  "confidence": "high" | "medium" | "low"
}}

Use confidence:
- high: clear match to one subcategory
- medium: likely match but some ambiguity
- low: unclear or could fit multiple categories
"""
    result = _safe_groq_call(prompt)
    if "error" in result:
        return result

    required = {"summary", "suggested_category", "confidence"}
    if not required.issubset(result.keys()):
        return {"error": "Incomplete response from Groq.", "raw": result}

    return {
        "summary": result["summary"],
        "suggested_category": result["suggested_category"],
        "confidence": result.get("confidence", "low"),
    }


def generate_summary_and_timeline(case_data: dict) -> dict:
    """
    Generate editable case summary and timeline from full case data.

    case_data should include: incident description, classification, follow-up answers.
    Returns: {summary, timeline: [{time, event}, ...]} or {error: ...}
    """
    prompt = f"""You are CIRA generating a case summary and timeline for a cybercrime victim in India.

Full case data (JSON):
{json.dumps(case_data, indent=2, default=str)}

Create a clear, victim-friendly summary and chronological timeline for reporting on cybercrime.gov.in.

Respond with ONLY valid JSON:
{{
  "summary": "Structured paragraph summarizing the incident, losses, and key facts",
  "timeline": [
    {{"time": "approximate date/time or order", "event": "what happened"}},
    ...
  ]
}}
"""
    result = _safe_groq_call(prompt)
    if "error" in result:
        return result

    if "summary" not in result or "timeline" not in result:
        return {"error": "Incomplete summary/timeline from Groq.", "raw": result}

    return {
        "summary": result["summary"],
        "timeline": result.get("timeline", []),
    }
