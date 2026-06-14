"""Rule engine for dynamic follow-up questions by incident type."""

from pathlib import Path
import json

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_CATEGORIES_FILE = _DATA_DIR / "categories.json"

# Generic questions applicable to most incident types
GENERIC_QUESTIONS = [
    {
        "id": "incident_date",
        "text": "When did this incident occur?",
        "type": "date",
        "options": [],
    },
    {
        "id": "loss_occurred",
        "text": "Was any money, data, or personal information lost or compromised?",
        "type": "select",
        "options": ["Yes — financial loss", "Yes — data/personal info", "Yes — both", "No", "Unsure"],
    },
    {
        "id": "evidence_saved",
        "text": "Do you have any screenshots, messages, or other evidence saved?",
        "type": "select",
        "options": ["Yes", "Partially", "No"],
    },
    {
        "id": "already_contacted",
        "text": "Have you already contacted your bank, platform, or any authority?",
        "type": "select",
        "options": ["Bank", "Platform/Website", "Police/Cyber Crime Portal", "Multiple", "Not yet"],
    },
]

# One to two category-specific questions per top-level category
CATEGORY_SPECIFIC_QUESTIONS: dict[str, list[dict]] = {
    "online-social-media": [
        {
            "id": "platform_name",
            "text": "Which social media or online platform was involved?",
            "type": "text",
            "options": [],
        },
        {
            "id": "attacker_profile_url",
            "text": "Do you have the URL or username of the attacker's profile?",
            "type": "text",
            "options": [],
        },
    ],
    "online-financial-fraud": [
        {
            "id": "transaction_amount",
            "text": "What was the approximate amount involved (INR)?",
            "type": "number",
            "options": [],
        },
        {
            "id": "utr_number",
            "text": "Do you have a UTR/transaction reference number?",
            "type": "text",
            "options": [],
        },
    ],
    "hacking-damage-computer": [
        {
            "id": "affected_systems",
            "text": "Which systems or devices were affected?",
            "type": "text",
            "options": [],
        },
        {
            "id": "data_breach_scope",
            "text": "Was any sensitive data accessed or exfiltrated?",
            "type": "select",
            "options": ["Yes — confirmed", "Suspected", "No", "Unsure"],
        },
    ],
    "other-categories": [
        {
            "id": "incident_nature",
            "text": "Briefly describe the nature of the incident in your own words.",
            "type": "text",
            "options": [],
        },
        {
            "id": "ongoing_threat",
            "text": "Is there an ongoing or immediate threat to safety?",
            "type": "select",
            "options": ["Yes — immediate", "Possible", "No"],
        },
    ],
}

# Subcategory-specific extras (optional, 1 per notable type)
SUBCATEGORY_SPECIFIC_QUESTIONS: dict[str, list[dict]] = {
    "upi-related-frauds": [
        {
            "id": "upi_app",
            "text": "Which UPI app or payment service was used?",
            "type": "select",
            "options": ["Google Pay", "PhonePe", "Paytm", "BHIM", "Bank app", "Other"],
        },
    ],
    "fraud-call-vishing": [
        {
            "id": "caller_number",
            "text": "Do you have the phone number the fraudster called from?",
            "type": "text",
            "options": [],
        },
    ],
    "ransomware": [
        {
            "id": "ransom_note",
            "text": "Did you receive a ransom note or demand? Can you describe it?",
            "type": "text",
            "options": [],
        },
    ],
}


def _load_categories_data() -> dict:
    with open(_CATEGORIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _get_category_id_for_subcategory(subcategory_id: str) -> str | None:
    data = _load_categories_data()
    for sub in data["subcategories"]:
        if sub["id"] == subcategory_id:
            return sub["category_id"]
    return None


def get_followup_questions(subcategory_id: str, known_data: dict) -> list[dict]:
    """
    Return follow-up questions for the given subcategory.

    Skips questions whose id already appears in known_data with a non-empty value.
    """
    category_id = _get_category_id_for_subcategory(subcategory_id)
    if category_id is None:
        return [q for q in GENERIC_QUESTIONS if q["id"] not in known_data or not known_data[q["id"]]]

    questions: list[dict] = []
    seen_ids: set[str] = set()

    for q in GENERIC_QUESTIONS:
        if q["id"] not in known_data or not known_data.get(q["id"]):
            questions.append(q)
            seen_ids.add(q["id"])

    for q in CATEGORY_SPECIFIC_QUESTIONS.get(category_id, []):
        if q["id"] not in seen_ids and (q["id"] not in known_data or not known_data.get(q["id"])):
            questions.append(q)
            seen_ids.add(q["id"])

    for q in SUBCATEGORY_SPECIFIC_QUESTIONS.get(subcategory_id, []):
        if q["id"] not in seen_ids and (q["id"] not in known_data or not known_data.get(q["id"])):
            questions.append(q)
            seen_ids.add(q["id"])

    return questions
