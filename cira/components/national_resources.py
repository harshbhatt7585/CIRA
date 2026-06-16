"""National Resources directory component for CIRA / CFRO."""

import json
from pathlib import Path
import streamlit as st

def _load_resources_data() -> dict:
    path = Path(__file__).resolve().parent.parent / "data" / "workspace_config.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def render_national_resources() -> None:
    """Render the official list of national cyber security resources loaded from config."""
    
    st.markdown("""
        <style>
        .resources-card-custom {
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 16px;
            background-color: #FFFFFF;
            box-shadow: 0 1px 6px rgba(0, 0, 0, 0.06);
            margin-top: 0;
            margin-bottom: 12px;
        }
        .resources-header-custom {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            border-bottom: 1px solid #F3F4F6;
            padding-bottom: 10px;
        }
        .resources-icon-box {
            padding: 5px;
            background-color: #EFF6FF;
            color: #2563EB;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .resources-title-custom {
            font-size: 0.7rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #374151 !important;
            margin: 0 !important;
        }
        .resources-list-custom {
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .resource-item-custom {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            border-bottom: 1px solid #F9FAFB;
            padding-bottom: 12px;
        }
        .resource-item-custom:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .resource-text-group {
            display: flex;
            flex-direction: column;
        }
        .resource-title-item {
            font-size: 0.74rem !important;
            font-weight: 600 !important;
            color: #111827 !important;
            margin: 0 0 2px 0 !important;
        }
        .resource-desc-item {
            font-size: 0.67rem;
            color: #6B7280;
            margin-top: 2px;
            line-height: 1.4;
            margin-bottom: 0;
        }
        .resource-link-custom {
            font-size: 0.67rem;
            font-weight: 600;
            color: #2563EB;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            flex-shrink: 0;
            white-space: nowrap;
        }
        .resource-link-custom:hover {
            text-decoration: underline;
            color: #1D4ED8;
        }
        </style>
    """, unsafe_allow_html=True)

    try:
        data = _load_resources_data()
        resources = data.get("national_resources", [])

        # Build all resource items HTML first
        items_html = ""
        for res in resources:
            name = res.get('name', '')
            description = res.get('description', '')
            url = res.get('url', '#')
            helpline = res.get('helpline', '')
            items_html += (
                '<div class="resource-item-custom">'
                '<div class="resource-text-group">'
                f'<h3 class="resource-title-item">{name}</h3>'
                f'<p class="resource-desc-item">{description}</p>'
                '</div>'
                f'<a href="{url}" target="_blank" class="resource-link-custom">'
                f'{helpline}'
                '<svg width="10" height="10" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">'
                '<path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>'
                '</svg>'
                '</a>'
                '</div>'
            )

        # Render everything in a single call so items stay inside the card div
        st.markdown(
            '<div class="resources-card-custom">'
            '<div class="resources-header-custom">'
            '<div class="resources-icon-box">'
            '<svg width="14" height="14" fill="currentColor" viewBox="0 0 20 20">'
            '<path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12V12a1 1 0 00.12.478l.997 1.896a1 1 0 001.062.5l2.158-.719 2.159.719a1 1 0 001.062-.5l.997-1.896A1 1 0 0014 12V10.12l1.69-.723a1 1 0 011.31 1.285l-7 11a1 1 0 01-1.614 0l-7-11a1 1 0 011.31-1.285z"></path>'
            '</svg>'
            '</div>'
            '<h2 class="resources-title-custom">National Resources</h2>'
            '</div>'
            '<div class="resources-list-custom">'
            + items_html +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Failed to load national resources: {str(e)}")

