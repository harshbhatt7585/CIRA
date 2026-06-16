"""Threat Intelligence scam models component for CIRA / CFRO."""

import json
from pathlib import Path
import streamlit as st

def _load_threat_data() -> dict:
    path = Path(__file__).resolve().parent.parent / "data" / "workspace_config.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def render_threat_intelligence() -> None:
    """Load scam trends from JSON config and render high-density alert cards."""
    
    st.markdown("""
        <style>
        .scam-section-custom {
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 16px;
            background-color: #FFFFFF;
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
            margin-top: 0;
            margin-bottom: 12px;
        }
        .scam-header-custom {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            border-bottom: 1px solid #F3F4F6;
            padding-bottom: 10px;
        }
        .scam-icon-box-custom {
            padding: 5px;
            background-color: #FEF2F2;
            color: #EF4444;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .scam-title-custom {
            font-size: 0.7rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #374151 !important;
            margin: 0 !important;
        }
        .scam-list-custom {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .scam-card-custom {
            background-color: #FAFAFA;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            transition: all 0.15s ease;
        }
        .scam-card-custom:hover {
            border-color: #D1D5DB;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }
        .scam-card-title-row-custom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 7px;
        }
        .scam-card-title-custom {
            font-size: 0.76rem !important;
            font-weight: 700 !important;
            color: #111827 !important;
            margin: 0 !important;
        }
        .scam-severity-badge-custom {
            font-size: 0.6rem;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 800;
            color: white;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            line-height: 1;
        }
        .scam-severity-critical-custom {
            background-color: #EF4444;
        }
        .scam-severity-high-custom {
            background-color: #F59E0B;
        }
        .scam-desc-custom {
            font-size: 0.7rem;
            color: #4B5563;
            line-height: 1.45;
            margin-bottom: 8px;
            margin-top: 0;
        }
        .scam-script-box-custom {
            font-family: monospace;
            font-size: 0.66rem;
            background-color: #F8FAFC;
            border-left: 3px solid #3B82F6;
            padding: 7px 9px;
            margin-bottom: 8px;
            color: #374151;
            border-radius: 4px;
        }
        .scam-defense-box-custom {
            font-size: 0.67rem;
            background-color: #F0FDF4;
            border-left: 3px solid #16A34A;
            padding: 7px 9px;
            color: #14532D;
            font-weight: 500;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    try:
        data = _load_threat_data()
        scams = data.get("threat_intelligence", [])

        # Build all scam card items first
        items_html = ""
        for scam in scams:
            sev = scam.get("severity", "HIGH").upper()
            sev_class = "scam-severity-critical-custom" if sev == "CRITICAL" else "scam-severity-high-custom"
            scam_name = scam.get('scam_name', '')
            description = scam.get('description', '')
            example_script = scam.get('example_script', '')
            defense_step = scam.get('defense_step', '')
            items_html += (
                '<div class="scam-card-custom">'
                '<div class="scam-card-title-row-custom">'
                f'<h3 class="scam-card-title-custom">{scam_name}</h3>'
                f'<span class="scam-severity-badge-custom {sev_class}">{sev}</span>'
                '</div>'
                f'<p class="scam-desc-custom">{description}</p>'
                '<div class="scam-script-box-custom">'
                f'<strong>Example Phishing Script:</strong><br>{example_script}'
                '</div>'
                '<div class="scam-defense-box-custom">'
                f'<strong>Victim Defense Step:</strong><br>{defense_step}'
                '</div>'
                '</div>'
            )

        # Render in a single call so all cards stay inside the outer section div
        st.markdown(
            '<div class="scam-section-custom">'
            '<div class="scam-header-custom">'
            '<div class="scam-icon-box-custom">'
            '<svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20">'
            '<path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"></path>'
            '</svg>'
            '</div>'
            '<h2 class="scam-title-custom">Trending Scam Alerts</h2>'
            '</div>'
            '<div class="scam-list-custom">'
            + items_html +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Failed to load scam intelligence: {str(e)}")
