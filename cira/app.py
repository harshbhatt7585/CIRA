"""
CIRA — Cyber Incidence Response Assistant
Main Streamlit entry point.
"""

import json
from pathlib import Path

import streamlit as st

from components.chat_intake import render_chat_intake
from components.evidence_checklist import render_evidence_checklist
from components.intake_wizard import render_intake_wizard
from components.response_guide import render_response_guide
from utils.classification_mapper import (
    get_all_subcategories,
    get_subcategory_names,
    map_to_official_category,
)
from utils.groq_client import generate_summary_and_timeline, understand_incident
from utils.rule_engine import get_followup_questions

# --- Session state keys ---
STEPS = [
    "intake",
    "classification",
    "confirmation",
    "followup",
    "evidence",
    "playbook",
    "summary",
]

DEFAULT_SESSION = {
    "step": "intake",
    "intake_mode": None,  # "chat" | "wizard"
    "incident_description": "",
    "ai_understanding": None,
    "classification": None,
    "followup_answers": {},
    "evidence_checked": {},
    "case_summary": "",
    "case_timeline": [],
    "summary_generated": False,
}


def init_session():
    for key, val in DEFAULT_SESSION.items():
        if key not in st.session_state:
            st.session_state[key] = val


def load_categories_meta() -> dict:
    path = Path(__file__).parent / "data" / "categories.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def step_index(step: str) -> int:
    return STEPS.index(step) if step in STEPS else 0


def render_progress():
    current = step_index(st.session_state.step)
    labels = ["Intake", "AI Analysis", "Confirm Type", "Follow-Up", "Evidence", "Playbook", "Summary"]
    st.progress((current + 1) / len(STEPS))
    st.caption(" → ".join(f"**{l}**" if i == current else l for i, l in enumerate(labels)))


def render_intake_step():
    st.header("Step 1: Tell Us What Happened")
    mode = st.radio(
        "How would you like to describe your incident?",
        ["Free text", "Guided wizard"],
        horizontal=True,
        key="intake_mode_radio",
    )

    description = None
    if mode == "Free text":
        st.session_state.intake_mode = "chat"
        description = render_chat_intake()
    else:
        st.session_state.intake_mode = "wizard"
        description = render_intake_wizard()

    if description:
        st.session_state.incident_description = description
        st.session_state.step = "classification"
        st.rerun()


def render_classification_step():
    st.header("Step 2: Understanding Your Incident")
    st.write("Analyzing your account with AI...")

    if st.session_state.ai_understanding is None:
        with st.spinner("Contacting Groq..."):
            result = understand_incident(
                st.session_state.incident_description,
                get_subcategory_names(),
            )
        if "error" in result:
            st.error(result["error"])
            if st.button("Back to intake"):
                st.session_state.step = "intake"
                st.rerun()
            return
        st.session_state.ai_understanding = result

    understanding = st.session_state.ai_understanding
    st.info(f"**AI Summary:** {understanding.get('summary', '')}")
    st.write(
        f"**Suggested category:** {understanding.get('suggested_category', 'Unknown')} "
        f"_(confidence: {understanding.get('confidence', 'low')})_"
    )

    if st.session_state.classification is None:
        st.session_state.classification = map_to_official_category(understanding)

    classification = st.session_state.classification
    st.write(
        f"**Mapped to:** {classification.get('subcategory_name')} "
        f"under {classification.get('category_name')} "
        f"_(match confidence: {classification.get('match_confidence')})_"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Accept classification", type="primary"):
            st.session_state.step = "confirmation" if classification.get("needs_confirmation") else "followup"
            st.rerun()
    with col2:
        if st.button("Choose category manually"):
            st.session_state.step = "confirmation"
            st.rerun()


def render_confirmation_step():
    st.header("Step 3: Confirm Incident Type")
    st.caption("Please confirm or select the correct category for reporting on cybercrime.gov.in.")

    subcategories = get_all_subcategories()
    options = {sub["id"]: f"{sub['name']} ({sub['category_id']})" for sub in subcategories}
    id_list = list(options.keys())

    current = st.session_state.classification or {}
    default_idx = id_list.index(current.get("subcategory_id", id_list[0])) if current.get("subcategory_id") in id_list else 0

    selected_id = st.selectbox(
        "Official subcategory",
        id_list,
        index=default_idx,
        format_func=lambda x: options[x],
        key="confirm_subcategory",
    )

    meta = load_categories_meta()
    selected_sub = next(s for s in meta["subcategories"] if s["id"] == selected_id)
    selected_cat = next(c for c in meta["categories"] if c["id"] == selected_sub["category_id"])

    st.session_state.classification = {
        "category_id": selected_sub["category_id"],
        "category_name": selected_cat["name"],
        "subcategory_id": selected_sub["id"],
        "subcategory_name": selected_sub["name"],
        "match_confidence": 1.0,
        "needs_confirmation": False,
    }

    if st.button("Confirm and continue", type="primary"):
        st.session_state.step = "followup"
        st.rerun()


def render_followup_step():
    st.header("Step 4: Follow-Up Questions")
    classification = st.session_state.classification
    if not classification:
        st.session_state.step = "confirmation"
        st.rerun()
        return

    subcategory_id = classification["subcategory_id"]
    known = {**st.session_state.followup_answers}
    questions = get_followup_questions(subcategory_id, known)

    if not questions:
        st.success("All follow-up questions answered.")
        if st.button("Continue to evidence checklist", type="primary"):
            st.session_state.step = "evidence"
            st.rerun()
        return

    answers = st.session_state.followup_answers
    for q in questions:
        qid = q["id"]
        if q["type"] == "text":
            answers[qid] = st.text_input(q["text"], value=answers.get(qid, ""), key=f"fq_{qid}")
        elif q["type"] == "number":
            answers[qid] = st.number_input(q["text"], value=answers.get(qid, 0) or 0, key=f"fq_{qid}")
        elif q["type"] == "date":
            answers[qid] = st.date_input(q["text"], value=answers.get(qid), key=f"fq_{qid}")
        elif q["type"] == "select":
            opts = q["options"]
            cur = answers.get(qid, opts[0])
            idx = opts.index(cur) if cur in opts else 0
            answers[qid] = st.selectbox(q["text"], opts, index=idx, key=f"fq_{qid}")

    st.session_state.followup_answers = answers

    if st.button("Save answers and continue", type="primary"):
        st.session_state.step = "evidence"
        st.rerun()


def render_evidence_step():
    st.header("Step 5: Evidence Collection")
    classification = st.session_state.classification
    if not classification:
        st.session_state.step = "followup"
        st.rerun()
        return

    checked = render_evidence_checklist(classification["category_id"])
    st.session_state.evidence_checked = checked

    if st.button("Continue to playbook", type="primary"):
        st.session_state.step = "playbook"
        st.rerun()


def render_playbook_step():
    st.header("Step 6: Response Playbook")
    classification = st.session_state.classification
    if not classification:
        st.session_state.step = "evidence"
        st.rerun()
        return

    render_response_guide(classification["subcategory_id"])

    if st.button("Generate summary & timeline", type="primary"):
        st.session_state.step = "summary"
        st.session_state.summary_generated = False
        st.rerun()


def render_summary_step():
    st.header("Step 7: Case Summary & Timeline")
    classification = st.session_state.classification

    if not st.session_state.summary_generated:
        case_data = {
            "incident_description": st.session_state.incident_description,
            "classification": classification,
            "followup_answers": st.session_state.followup_answers,
            "evidence_collected": st.session_state.evidence_checked,
            "ai_understanding": st.session_state.ai_understanding,
        }
        with st.spinner("Generating summary and timeline..."):
            result = generate_summary_and_timeline(case_data)
        if "error" in result:
            st.error(result["error"])
            return
        st.session_state.case_summary = result.get("summary", "")
        st.session_state.case_timeline = result.get("timeline", [])
        st.session_state.summary_generated = True

    st.subheader("Editable Case Summary")
    st.session_state.case_summary = st.text_area(
        "Summary",
        value=st.session_state.case_summary,
        height=200,
        key="editable_summary",
    )

    st.subheader("Timeline")
    timeline = st.session_state.case_timeline
    if timeline:
        for i, entry in enumerate(timeline):
            cols = st.columns([1, 3])
            with cols[0]:
                timeline[i]["time"] = st.text_input(
                    f"Time #{i+1}",
                    value=entry.get("time", ""),
                    key=f"tl_time_{i}",
                )
            with cols[1]:
                timeline[i]["event"] = st.text_input(
                    f"Event #{i+1}",
                    value=entry.get("event", ""),
                    key=f"tl_event_{i}",
                )
        st.session_state.case_timeline = timeline
    else:
        st.info("No timeline events generated.")

    st.divider()
    st.subheader("Reporting")
    st.markdown(
        "Use this summary when filing on the "
        "[National Cyber Crime Reporting Portal](https://cybercrime.gov.in)."
    )

    if st.button("Start over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session()
        st.rerun()


def main():
    st.set_page_config(page_title="CIRA — Cyber Incidence Response Assistant", layout="wide")
    init_session()

    st.title("CIRA — Cyber Incidence Response Assistant")
    st.caption("Immediate guidance for cybercrime victims in India")

    render_progress()

    step = st.session_state.step
    if step == "intake":
        render_intake_step()
    elif step == "classification":
        render_classification_step()
    elif step == "confirmation":
        render_confirmation_step()
    elif step == "followup":
        render_followup_step()
    elif step == "evidence":
        render_evidence_step()
    elif step == "playbook":
        render_playbook_step()
    elif step == "summary":
        render_summary_step()
    else:
        st.session_state.step = "intake"
        st.rerun()


if __name__ == "__main__":
    main()
