"""Evidence collection checklist UI."""

import streamlit as st

# Evidence items keyed by top-level category_id
EVIDENCE_BY_CATEGORY: dict[str, list[dict]] = {
    "online-social-media": [
        {"id": "screenshots_profiles", "label": "Screenshots of fake/offending profiles or posts"},
        {"id": "messages", "label": "Saved chat messages, comments, or emails"},
        {"id": "profile_urls", "label": "URLs or usernames of involved accounts"},
        {"id": "witness_info", "label": "Names/contact of witnesses who saw the content"},
    ],
    "online-financial-fraud": [
        {"id": "transaction_records", "label": "Bank/UPI transaction statements or screenshots"},
        {"id": "utr_references", "label": "UTR numbers or transaction reference IDs"},
        {"id": "call_sms_records", "label": "Call logs or SMS from fraudster"},
        {"id": "bank_correspondence", "label": "Emails or letters from your bank about the incident"},
    ],
    "hacking-damage-computer": [
        {"id": "system_logs", "label": "System logs, error messages, or ransom notes"},
        {"id": "affected_files", "label": "List or copies of affected files (do not alter originals)"},
        {"id": "access_records", "label": "Login history or unauthorized access notifications"},
        {"id": "backup_status", "label": "Note whether backups exist and their dates"},
    ],
    "other-categories": [
        {"id": "general_screenshots", "label": "Any relevant screenshots or recordings"},
        {"id": "communication_records", "label": "Messages, emails, or documents related to the incident"},
        {"id": "financial_records", "label": "Payment or transaction records if applicable"},
        {"id": "official_refs", "label": "Reference numbers from any reports already filed"},
    ],
}

GENERIC_EVIDENCE = [
    {"id": "incident_timeline", "label": "Written timeline of events (dates and times)"},
    {"id": "identity_docs", "label": "Copy of ID documents if identity theft is involved"},
    {"id": "device_info", "label": "Device model/OS and apps involved"},
]


def render_evidence_checklist(category_id: str) -> dict[str, bool]:
    """Render checklist; returns dict of item_id -> checked."""
    st.subheader("Evidence to Gather")
    st.caption("Check off evidence you have collected or plan to preserve before reporting.")

    items = EVIDENCE_BY_CATEGORY.get(category_id, EVIDENCE_BY_CATEGORY["other-categories"])
    items = items + GENERIC_EVIDENCE

    if "evidence_checked" not in st.session_state:
        st.session_state.evidence_checked = {}

    checked: dict[str, bool] = {}
    for item in items:
        key = f"evidence_{item['id']}"
        is_checked = st.session_state.evidence_checked.get(item["id"], False)
        checked[item["id"]] = st.checkbox(item["label"], value=is_checked, key=key)

    st.session_state.evidence_checked = checked
    return checked
