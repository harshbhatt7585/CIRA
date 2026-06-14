"""Free-text incident intake UI."""

import streamlit as st


def render_chat_intake() -> str | None:
    """
    Render free-text 'describe what happened' intake.
    Returns incident description when submitted, else None.
    """
    st.subheader("Describe Your Incident")
    st.caption(
        "Tell us what happened in your own words. Include dates, platforms, "
        "amounts, and any contact from the perpetrator."
    )

    default = st.session_state.get("incident_description", "")
    user_text = st.text_area(
        "What happened?",
        value=default,
        height=200,
        placeholder=(
            "Example: Yesterday I got a WhatsApp message about a job offer. "
            "They asked me to pay a registration fee via UPI and I lost ₹15,000..."
        ),
        key="chat_intake_text",
    )

    if st.button("Analyze my incident", type="primary"):
        if not user_text.strip():
            st.warning("Please describe your incident before continuing.")
            return None
        st.session_state.incident_description = user_text.strip()
        return user_text.strip()

    return None
