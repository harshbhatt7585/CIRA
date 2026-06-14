"""Guided step-by-step intake wizard UI."""

import streamlit as st


WIZARD_STEPS = [
    {
        "id": "what_happened",
        "prompt": "In a few sentences, describe what happened to you.",
        "type": "text_area",
        "placeholder": "e.g. I received a call claiming to be from my bank and was tricked into sharing my UPI PIN...",
    },
    {
        "id": "when_happened",
        "prompt": "Approximately when did this occur?",
        "type": "date",
    },
    {
        "id": "platform_or_channel",
        "prompt": "How did the incident start? (phone call, message, email, social media, website, etc.)",
        "type": "select",
        "options": [
            "Phone call",
            "SMS / WhatsApp",
            "Email",
            "Social media",
            "Website / App",
            "In person / Other",
            "Unsure",
        ],
    },
    {
        "id": "financial_loss",
        "prompt": "Was any money lost or attempted to be taken?",
        "type": "select",
        "options": ["Yes — money was lost", "Attempt was made but blocked", "No financial aspect", "Unsure"],
    },
]


def render_intake_wizard() -> str | None:
    """
    Render guided wizard; returns combined incident description or None if incomplete.
    """
    st.subheader("Guided Intake")
    st.caption("Answer a few questions to help us understand your incident.")

    if "wizard_answers" not in st.session_state:
        st.session_state.wizard_answers = {}

    answers = st.session_state.wizard_answers

    for step in WIZARD_STEPS:
        key = f"wizard_{step['id']}"
        if step["type"] == "text_area":
            answers[step["id"]] = st.text_area(
                step["prompt"],
                value=answers.get(step["id"], ""),
                placeholder=step.get("placeholder", ""),
                key=key,
            )
        elif step["type"] == "date":
            answers[step["id"]] = st.date_input(
                step["prompt"],
                value=answers.get(step["id"]),
                key=key,
            )
        elif step["type"] == "select":
            options = step["options"]
            current = answers.get(step["id"], options[0])
            idx = options.index(current) if current in options else 0
            answers[step["id"]] = st.selectbox(step["prompt"], options, index=idx, key=key)

    st.session_state.wizard_answers = answers

    if st.button("Submit guided intake", type="primary"):
        narrative_parts = []
        if answers.get("what_happened"):
            narrative_parts.append(f"Description: {answers['what_happened']}")
        if answers.get("when_happened"):
            narrative_parts.append(f"When: {answers['when_happened']}")
        if answers.get("platform_or_channel"):
            narrative_parts.append(f"Channel: {answers['platform_or_channel']}")
        if answers.get("financial_loss"):
            narrative_parts.append(f"Financial impact: {answers['financial_loss']}")

        if not answers.get("what_happened", "").strip():
            st.warning("Please describe what happened before continuing.")
            return None

        combined = "\n".join(narrative_parts)
        st.session_state.incident_description = combined
        return combined

    return None
