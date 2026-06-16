"""Map AI classification output to official taxonomy entries."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_CATEGORIES_FILE = _DATA_DIR / "categories.json"

CONFIDENCE_THRESHOLD = 0.75


def _load_categories_data() -> dict:
    with open(_CATEGORIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


def _confidence_to_score(confidence: str) -> float:
    mapping = {"high": 0.95, "medium": 0.7, "low": 0.4}
    return mapping.get(confidence.lower(), 0.5)


def map_to_official_category(ai_output: dict) -> dict:
    """
    Fuzzy-match AI classification to official subcategory names.

    ai_output keys: summary, suggested_category, confidence (high|medium|low)
    """
    data = _load_categories_data()
    suggested = ai_output.get("suggested_category", "")
    ai_confidence = ai_output.get("confidence", "low")

    best_match: dict | None = None
    best_score = 0.0

    for sub in data["subcategories"]:
        score = _similarity(suggested, sub["name"])
        if score > best_score:
            best_score = score
            best_match = sub

    if best_match is None:
        return {
            "category_id": "other-categories",
            "category_name": "Other Main Categories",
            "subcategory_id": "any-other-cyber-crime",
            "subcategory_name": "Any Other Cyber Crime",
            "match_confidence": 0.0,
            "needs_confirmation": True,
        }

    category = next(
        (c for c in data["categories"] if c["id"] == best_match["category_id"]),
        None,
    )

    combined_score = (best_score + _confidence_to_score(ai_confidence)) / 2
    needs_confirmation = combined_score < CONFIDENCE_THRESHOLD or ai_confidence.lower() == "low"

    return {
        "category_id": best_match["category_id"],
        "category_name": category["name"] if category else None,
        "subcategory_id": best_match["id"],
        "subcategory_name": best_match["name"],
        "match_confidence": round(combined_score, 3),
        "needs_confirmation": needs_confirmation,
    }


def get_all_subcategories() -> list[dict]:
    """Return all subcategories for manual selection dropdowns."""
    data = _load_categories_data()
    return data["subcategories"]


def get_subcategory_names() -> list[str]:
    """Return official subcategory display names for AI classification prompt."""
    return [sub["name"] for sub in get_all_subcategories()]
