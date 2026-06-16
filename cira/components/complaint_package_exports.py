"""FIR / Complaint Package Exports component for CIRA / CFRO."""

import streamlit as st
import datetime
from utils.pdf_generator import generate_pdf_report

def generate_complaint_package_markdown(case_data: dict) -> str:
    classification = case_data.get("classification") or {}
    subcat = classification.get("subcategory_name") or "Unclassified Incident"
    cat = classification.get("category_name") or "Other"
    summary = case_data.get("summary") or ""
    
    md = f"# CIRA Cyber Incident Report\n\n"
    md += f"**Date:** {datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')}  \n"
    md += f"**Classification:** {subcat} ({cat})\n\n"
    md += f"## Incident Summary\n{summary}\n\n"
    md += "## Timeline\n"
    for item in (case_data.get("timeline") or []):
        md += f"- **{item.get('time', '')}**: {item.get('event', '')}\n"
    md += "\n## Evidence\n"
    evidence = case_data.get("evidence") or {}
    for item_id, label in (case_data.get("evidence_labels") or {}).items():
        status = "x" if evidence.get(item_id, False) else " "
        md += f"- [{status}] {label}\n"
    return md

def generate_complaint_package_text(case_data: dict) -> str:
    classification = case_data.get("classification") or {}
    subcat = classification.get("subcategory_name") or "Unclassified Incident"
    cat = classification.get("category_name") or "Other Main Categories"
    summary = case_data.get("summary") or ""
    
    text = "=== NATIONAL CYBER CRIME PORTAL REPORTING PACKAGE ===\n"
    text += "Use the structured details below to file your complaint on cybercrime.gov.in\n"
    text += f"Report Compiled on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += "--- FIELD 1: CATEGORY OF INCIDENT ---\n"
    text += f"Category: {cat}\n"
    text += f"Subcategory: {subcat}\n\n"
    
    text += "--- FIELD 2: INCIDENT DATE & TIME ---\n"
    followup_answers = case_data.get("followup_answers") or {}
    incident_date = followup_answers.get("incident_date", "Refer to Timeline")
    text += f"Approximate Date/Time: {incident_date}\n\n"
    
    text += "--- FIELD 3: INCIDENT DETAILS (COMPLAINT TEXT) ---\n"
    text += "Copy-paste the paragraph below into the 'Additional Information' text box on the portal:\n\n"
    text += f"{summary}\n\n"
    
    text += "--- FIELD 4: CHRONOLOGICAL TIMELINE ---\n"
    timeline = case_data.get("timeline") or []
    if timeline:
        for i, item in enumerate(timeline, 1):
            text += f"Event #{i}: [{item.get('time', '')}] {item.get('event', '')}\n"
    else:
        text += "No timeline entries.\n"
    text += "\n"
    
    text += "--- FIELD 5: EVIDENCE PRESERVED ---\n"
    evidence = case_data.get("evidence") or {}
    evidence_labels = case_data.get("evidence_labels") or {}
    if evidence_labels:
        for item_id, label in evidence_labels.items():
            status = "Collected" if evidence.get(item_id, False) else "Missing/Pending"
            text += f"- {label}: {status}\n"
    else:
        text += "No evidence listed.\n"
    
    return text

def generate_printable_summary_html(case_data: dict) -> str:
    classification = case_data.get("classification") or {}
    subcat = classification.get("subcategory_name") or "Unclassified Incident"
    cat = classification.get("category_name") or "Other Main Categories"
    summary = case_data.get("summary") or ""
    
    timeline_rows = ""
    timeline = case_data.get("timeline") or []
    for item in timeline:
        timeline_rows += f"<tr><td>{item.get('time', '')}</td><td>{item.get('event', '')}</td></tr>"
        
    evidence_rows = ""
    evidence = case_data.get("evidence") or {}
    evidence_labels = case_data.get("evidence_labels") or {}
    for item_id, label in evidence_labels.items():
        status = "<span style='color:green;'>Collected</span>" if evidence.get(item_id, False) else "<span style='color:red;'>Missing</span>"
        evidence_rows += f"<tr><td>{label}</td><td>{status}</td></tr>"
        
    html = f"""
    <html>
    <head>
        <title>CIRA Cyber Incident Report</title>
        <style>
            body {{ font-family: sans-serif; margin: 40px; color: #333; }}
            h1 {{ color: #0b3c5d; border-bottom: 2px solid #0b3c5d; padding-bottom: 10px; }}
            h2 {{ color: #1d2731; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .summary-box {{ background-color: #f9fafb; border-left: 4px solid #0b3c5d; padding: 15px; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <h1>CFRO — Cyber Incident Response Summary</h1>
        <p><strong>Report Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Category:</strong> {subcat} ({cat})</p>
        
        <h2>1. Incident Summary</h2>
        <div class="summary-box">{summary}</div>
        
        <h2>2. Chronological Timeline</h2>
        <table>
            <tr><th>Date/Time</th><th>Event Description</th></tr>
            {timeline_rows}
        </table>
        
        <h2>3. Evidence Status</h2>
        <table>
            <tr><th>Evidence Description</th><th>Status</th></tr>
            {evidence_rows}
        </table>
        
        <script>window.print();</script>
    </body>
    </html>
    """
    return html

def render_complaint_package_exports(case_data_package: dict) -> None:
    """Render the lock-status indicators and download actions for case exports."""

    st.markdown("""
        <style>
        /* ── Complaint Package section ─────────────────────── */
        .cp-section-wrap {
            border-top: 1px solid #E5E7EB;
            padding-top: 18px;
            margin-top: 16px;
        }
        .cp-section-hdr {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
        }
        .cp-folder-icon {
            width: 28px; height: 28px;
            background: #FEF9C3;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .cp-section-title {
            font-size: 0.72rem !important;
            font-weight: 800 !important;
            color: #111827 !important;
            text-transform: uppercase;
            letter-spacing: 1.6px;
            margin: 0 !important;
        }
        /* Status rows */
        .cp-status-list {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .cp-status-row {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .cp-circle-ok {
            width: 18px; height: 18px;
            border-radius: 50%;
            background: #DCFCE7;
            border: 2px solid #22C55E;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .cp-circle-pending {
            width: 18px; height: 18px;
            border-radius: 50%;
            background: transparent;
            border: 2px solid #3B82F6;
            flex-shrink: 0;
        }
        .cp-circle-clock {
            width: 18px; height: 18px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .cp-status-text-ok {
            font-size: 0.74rem !important;
            font-weight: 500 !important;
            color: #374151 !important;
        }
        .cp-status-text-pending {
            font-size: 0.74rem !important;
            font-weight: 400 !important;
            color: #9CA3AF !important;
        }
        .cp-export-label {
            font-size: 0.65rem !important;
            font-weight: 700 !important;
            color: #9CA3AF !important;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-bottom: 8px;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    classification = case_data_package.get("classification")
    cls_ok  = classification is not None
    sum_ok  = bool((case_data_package.get("summary") or "").strip())
    tl_ok   = bool(case_data_package.get("timeline"))
    ev_ok   = any((case_data_package.get("evidence") or {}).values())

    def _row(ok: bool, label: str, pending_label: str, is_classification: bool = False) -> str:
        if ok:
            return (
                '<div class="cp-status-row">'
                '<div class="cp-circle-ok">'
                '<svg width="10" height="10" fill="none" stroke="#22C55E" stroke-width="3" viewBox="0 0 24 24">'
                '<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>'
                '</svg>'
                '</div>'
                f'<span class="cp-status-text-ok">{label}</span>'
                '</div>'
            )
        if is_classification:
            return (
                '<div class="cp-status-row">'
                '<div class="cp-circle-clock">'
                '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
                '<circle cx="12" cy="12" r="10"></circle>'
                '<polyline points="12 6 12 12 16 14"></polyline>'
                '</svg>'
                '</div>'
                f'<span class="cp-status-text-pending">{pending_label}</span>'
                '</div>'
            )
        return (
            '<div class="cp-status-row">'
            '<div class="cp-circle-pending"></div>'
            f'<span class="cp-status-text-pending">{pending_label}</span>'
            '</div>'
        )

    rows_html = (
        _row(cls_ok,  "Classification",       "Classification — pending", is_classification=True) +
        _row(sum_ok,  "Summary Generated",     "Summary Generated — pending") +
        _row(tl_ok,   "Timeline Compiled",     "Timeline Compiled — pending") +
        _row(ev_ok,   "Evidence Logged",       "Evidence Logged — pending")
    )

    st.markdown(
        '<div class="cp-section-wrap">'
        '<div class="cp-section-hdr">'
        '<div class="cp-folder-icon">'
        '<svg width="14" height="14" fill="#EAB308" viewBox="0 0 20 20">'
        '<path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"></path>'
        '</svg>'
        '</div>'
        '<span class="cp-section-title">Complaint Package</span>'
        '</div>'
        '<div class="cp-status-list">'
        + rows_html +
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Export buttons — only when summary is ready
    if sum_ok:
        st.markdown('<div class="cp-export-label">Export Report Package</div>', unsafe_allow_html=True)

        try:
            pdf_bytes = generate_pdf_report(case_data_package)
            st.download_button("📄 Download PDF Report", data=pdf_bytes,
                file_name="CFRO_FIR.pdf", mime="application/pdf",
                use_container_width=True, key="dl_pdf_left")
        except Exception:
            pass

        pkg_txt = generate_complaint_package_text(case_data_package)
        st.download_button("📋 Download TXT File", data=pkg_txt,
            file_name="CFRO_Complaint.txt", mime="text/plain",
            use_container_width=True, key="dl_txt_left")

        pkg_md = generate_complaint_package_markdown(case_data_package)
        st.download_button("📝 Download Markdown", data=pkg_md,
            file_name="CFRO_Report.md", mime="text/markdown",
            use_container_width=True, key="dl_md_left")

        pkg_html = generate_printable_summary_html(case_data_package)
        st.download_button("🖨️ Print Layout View", data=pkg_html,
            file_name="CFRO_Print.html", mime="text/html",
            use_container_width=True, key="dl_html_left")

