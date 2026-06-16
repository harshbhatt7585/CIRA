"""Playbook response guide rendering component for CIRA / CFRO."""

import streamlit as st
from utils.playbook_loader import load_playbook

def render_response_guide(subcategory_id: str | None = None) -> None:
    """Load and display the playbook sections in the Right Column as accordions."""
    
    st.markdown("""
        <style>
        .playbook-container {
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 16px;
            background-color: #FFFFFF;
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
            margin-bottom: 12px;
        }
        .playbook-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
        }
        .playbook-title-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .playbook-icon-box {
            padding: 5px;
            background-color: #EFF6FF;
            color: #2563EB;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .playbook-title {
            font-size: 0.7rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #374151 !important;
            margin: 0 !important;
        }
        .playbook-inactive-card {
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 14px;
            display: flex;
            gap: 14px;
            align-items: center;
        }
        .playbook-inactive-text {
            font-size: 0.73rem !important;
            font-weight: 400 !important;
            color: #6B7280 !important;
            line-height: 1.55 !important;
            margin: 0 !important;
        }
        .playbook-lock-illustration {
            width: 60px;
            height: 72px;
            background-color: #F3F4F6;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            padding: 8px;
            flex-shrink: 0;
        }
        .playbook-badge {
            font-size: 0.63rem;
            background-color: #2563EB;
            color: white;
            padding: 2px 8px;
            border-radius: 20px;
            font-weight: 600;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if not subcategory_id:
        st.markdown("""
            <div class="playbook-container">
                <div class="playbook-header">
                    <div class="playbook-title-group">
                        <div class="playbook-icon-box">
                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20"><path d="M9 4.804A7.993 7.993 0 002 12a5 5 0 008 4h.01c1.49 0 2.802-.6 3.744-1.566A12.037 12.037 0 0018 10a12.037 12.037 0 00-4.246-4.434A7.993 7.993 0 009 4.804z"></path></svg>
                        </div>
                        <h2 class="playbook-title">Incident Playbook</h2>
                    </div>
                </div>
                <div class="playbook-inactive-card">
                    <div class="playbook-inactive-text">
                        Playbook actions will activate automatically once the AI Case Officer classifies your incident.
                    </div>
                    <div class="playbook-lock-illustration">
                        <div style="display: flex; flex-direction: column; gap: 4px; width: 100%; opacity: 0.3;">
                            <div style="height: 3px; background-color: #CBD5E1; width: 100%; border-radius: 2px;"></div>
                            <div style="height: 3px; background-color: #CBD5E1; width: 100%; border-radius: 2px;"></div>
                            <div style="height: 3px; background-color: #CBD5E1; width: 75%; border-radius: 2px;"></div>
                        </div>
                        <div style="position: absolute; bottom: 8px; right: 8px; background-color: #FEF2F2; padding: 4px; border-radius: 6px; border: 1px solid #FEE2E2; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center;">
                            <svg width="12" height="12" fill="currentColor" style="color: #F87171;" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path></svg>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        return
        
    playbook = load_playbook(subcategory_id)
    subcat_name = playbook.get("subcategory_name", subcategory_id)
    
    st.markdown(f"""
        <div class="playbook-container" style="margin-bottom: 8px;">
            <div class="playbook-header" style="margin-bottom: 0;">
                <div class="playbook-title-group">
                    <div class="playbook-icon-box">
                        <svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20"><path d="M9 4.804A7.993 7.993 0 002 12a5 5 0 008 4h.01c1.49 0 2.802-.6 3.744-1.566A12.037 12.037 0 0018 10a12.037 12.037 0 00-4.246-4.434A7.993 7.993 0 009 4.804z"></path></svg>
                    </div>
                    <h2 class="playbook-title">Incident Playbook</h2>
                </div>
                <span class="playbook-badge">{subcat_name}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    sections = playbook.get("sections", {})
    
    # Map raw markdown sections to the 4 spec accordions
    immediate_text = ""
    evidence_text = ""
    reporting_text = ""
    recovery_text = ""
    
    # 1. Immediate Remediation
    immediate_text += sections.get("Immediate Actions (0-30 Minutes)", "") + "\n\n"
    immediate_text += sections.get("Containment Actions", "")
    
    # 2. Evidence Preservation Rules
    evidence_text += sections.get("Evidence Preservation", "")
    
    # 3. Statutory Reporting Authorities
    reporting_text += sections.get("Reporting Resources", "") + "\n\n"
    reporting_text += sections.get("Official Links", "")
    
    # 4. Recovery Guidance
    recovery_text += sections.get("Recovery Actions", "") + "\n\n"
    recovery_text += sections.get("Prevention Guidance", "") + "\n\n"
    recovery_text += sections.get("Notes", "")
    
    # Helper to clean empty section content
    def clean_section(text: str) -> str:
        text = text.strip()
        if not text or text == "_Content pending — to be added by operator._" or text.isspace():
            return "No specific instructions available for this section yet."
        return text

    # Render Expanders (Accordions)
    with st.expander("🔽 Immediate Remediation", expanded=True):
        st.markdown(clean_section(immediate_text))
        
    with st.expander("🔽 Evidence Preservation Rules", expanded=False):
        st.markdown(clean_section(evidence_text))
        
    with st.expander("🔽 Statutory Reporting Authorities", expanded=False):
        st.markdown(clean_section(reporting_text))
        
    with st.expander("🔽 Recovery Guidance", expanded=False):
        st.markdown(clean_section(recovery_text))
