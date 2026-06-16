"""Emergency Actions Card component for CIRA / CFRO."""

import streamlit as st

def render_emergency_actions(category_id: str | None = None) -> None:
    """Render the emergency helpline CTA and category-specific immediate actions."""

    st.markdown("""
        <style>
        /* ── Helpline CTA ─────────────────────────────────── */
        .helpline-cta {
            background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
            border: none;
            border-radius: 14px;
            padding: 16px 18px;
            color: #FFFFFF !important;
            margin-bottom: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 16px rgba(220, 38, 38, 0.35);
            text-decoration: none;
            display: block;
        }
        .helpline-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(220, 38, 38, 0.45);
        }
        .cta-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .cta-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .cta-icon-box {
            background-color: rgba(255,255,255,0.2);
            padding: 8px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .cta-text-group { display: flex; flex-direction: column; gap: 2px; }
        .cta-title {
            font-size: 1.1rem !important;
            font-weight: 900 !important;
            color: #FFFFFF !important;
            letter-spacing: 0.5px;
            text-decoration: underline;
            margin: 0 !important;
        }
        .cta-desc {
            font-size: 0.7rem !important;
            color: rgba(255,255,255,0.88) !important;
            line-height: 1.3;
            margin: 0 !important;
        }
        .cta-arrow { color: rgba(255,255,255,0.7); }

        /* ── Section header ───────────────────────────────── */
        .ea-section-hdr {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 12px;
            margin-top: 4px;
        }
        .ea-bell-icon {
            width: 28px; height: 28px;
            background: #FEF2F2;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .ea-section-title {
            font-size: 0.72rem !important;
            font-weight: 800 !important;
            color: #111827 !important;
            text-transform: uppercase;
            letter-spacing: 1.6px;
            margin: 0 !important;
        }

        /* ── Action cards ─────────────────────────────────── */
        .ea-card {
            background: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 13px 14px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: box-shadow 0.15s ease;
        }
        .ea-card:hover { box-shadow: 0 3px 8px rgba(0,0,0,0.09); }
        .ea-card-top {
            display: flex;
            align-items: center;
            gap: 9px;
            margin-bottom: 5px;
        }
        .ea-badge {
            font-size: 0.58rem !important;
            font-weight: 800 !important;
            padding: 3px 7px;
            border-radius: 6px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            flex-shrink: 0;
            color: #FFFFFF !important;
        }
        .ea-badge-red    { background: #EF4444; }
        .ea-badge-blue   { background: #3B82F6; }
        .ea-badge-orange { background: #F97316; }
        .ea-badge-green  { background: #22C55E; }
        .ea-card-title {
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            color: #111827 !important;
            margin: 0 !important;
            letter-spacing: 0.1px;
        }
        .ea-card-desc {
            font-size: 0.71rem !important;
            color: #6B7280 !important;
            line-height: 1.5 !important;
            margin: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── 1. Helpline CTA ──────────────────────────────────────────────────────
    st.markdown(
        '<a href="tel:1930" class="helpline-cta">'
        '<div class="cta-inner">'
        '<div class="cta-left">'
        '<div class="cta-icon-box">'
        '<svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">'
        '<path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"></path>'
        '</svg>'
        '</div>'
        '<div class="cta-text-group">'
        '<div class="cta-title">DIAL 1930</div>'
        '<div class="cta-desc">Immediate Financial Fraud Reporting (24/7 Helpline)</div>'
        '</div>'
        '</div>'
        '<div class="cta-arrow">'
        '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">'
        '<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"></path>'
        '</svg>'
        '</div>'
        '</div>'
        '</a>',
        unsafe_allow_html=True
    )

    # ── 2. Section header ────────────────────────────────────────────────────
    st.markdown(
        '<div class="ea-section-hdr">'
        '<div class="ea-bell-icon">'
        '<svg width="14" height="14" fill="#EF4444" viewBox="0 0 20 20">'
        '<path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"></path>'
        '</svg>'
        '</div>'
        '<span class="ea-section-title">Emergency Actions</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # ── 3. Action cards (category-aware) ─────────────────────────────────────
    if category_id == "online-financial-fraud":
        actions = [
            ("1930",  "ea-badge-red",    "GOLDEN HOUR",        "Call the financial fraud helpline at 1930 immediately to freeze funds."),
            ("BANK",  "ea-badge-blue",   "BLOCK CREDENTIALS",  "Contact bank branch to freeze cards, net banking, and UPI IDs."),
            ("STOP",  "ea-badge-orange", "STOP TRANSFERS",     "Do not send processing fees or security deposits to recover money."),
            ("SAVE",  "ea-badge-green",  "PRESERVE DETAILS",   "Save screenshots of UPI transaction IDs (UTR) and recipient bank names."),
        ]
    elif category_id == "online-social-media":
        actions = [
            ("BLOCK", "ea-badge-red",    "REPORT & BLOCK",     "Use the social platform's internal reporting tools to flag offending profiles."),
            ("ALERT", "ea-badge-blue",   "WARN NETWORK",       "Alert friends, family, and contacts that a fake account is impersonating you."),
            ("SAVE",  "ea-badge-orange", "LOG EVIDENCE",       "Take screenshots of chats, comments, profile URLs, and timestamps. Do not delete."),
            ("2FA",   "ea-badge-green",  "SECURE ACCESS",      "Change account credentials and enable 2-Factor Authentication immediately."),
        ]
    elif category_id == "hacking-damage-computer":
        actions = [
            ("OFF",  "ea-badge-red",    "GO OFFLINE",         "Disconnect the compromised system from the network/Wi-Fi immediately."),
            ("KEYS", "ea-badge-blue",   "CHANGE PASSWORDS",   "Update credentials of your bank, mail, and accounts from a clean device."),
            ("LOGS", "ea-badge-orange", "KEEP SYSTEM STATE",  "Do not run cleaner programs or format the system; keep files intact."),
            ("BACK", "ea-badge-green",  "CHECK BACKUPS",      "Assess the date and status of the latest offline restore backups."),
        ]
    else:
        actions = [
            ("1930", "ea-badge-red",    "REPORT FRAUD",  "Call the national helpline at 1930 immediately to freeze financial losses."),
            ("NET",  "ea-badge-blue",   "GO OFFLINE",    "Disconnect compromised systems or mobile phones from Wi-Fi / Mobile Data."),
            ("KEEP", "ea-badge-orange", "DON'T DELETE",  "Preserve all communication logs, chats, SMS alert texts, and transaction screens."),
            ("SAFE", "ea-badge-green",  "NEVER SHARE",   "Never share passwords, bank OTPs, or click on files received from unknown actors."),
        ]

    cards_html = ""
    for badge_text, badge_cls, title, desc in actions:
        cards_html += (
            '<div class="ea-card">'
            '<div class="ea-card-top">'
            f'<span class="ea-badge {badge_cls}">{badge_text}</span>'
            f'<span class="ea-card-title">{title}</span>'
            '</div>'
            f'<p class="ea-card-desc">{desc}</p>'
            '</div>'
        )

    st.markdown(cards_html, unsafe_allow_html=True)
