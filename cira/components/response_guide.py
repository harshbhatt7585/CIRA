"""Playbook response guide rendering."""

import streamlit as st

from utils.playbook_loader import load_playbook


def render_response_guide(subcategory_id: str) -> None:
    """Load and display the playbook for the classified subcategory."""
    st.subheader("Response Playbook")
    playbook = load_playbook(subcategory_id)

    if not playbook.get("available"):
        st.info(playbook.get("message", "Playbook not yet available."))
        sections = playbook.get("sections", {})
        if sections:
            with st.expander("Placeholder structure (pending content)"):
                for title, body in sections.items():
                    st.markdown(f"**{title}**")
                    st.markdown(body)
        return

    st.success(f"Guidance for: **{playbook.get('subcategory_name', subcategory_id)}**")
    for title, body in playbook["sections"].items():
        st.markdown(f"### {title}")
        st.markdown(body)
