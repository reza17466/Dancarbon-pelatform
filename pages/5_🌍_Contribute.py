"""Crowdsourced knowledge contribution page."""
import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Contribute — DanCarbon Tech", page_icon="🌍")

st.title("🌍 Contribute to Climate Research")
st.markdown(
    "Your knowledge matters. Help us accelerate CO₂ separation for a cleaner "
    "future. Every contribution — from a scientific observation to a raw data "
    "point — is filtered by AI and integrated into our shared model."
)

CONTRIB_FILE = "data/contributions.json"


def load_contribs():
    if not os.path.exists(CONTRIB_FILE):
        return []
    try:
        with open(CONTRIB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def save_contrib(entry):
    os.makedirs('data', exist_ok=True)
    contribs = load_contribs()
    contribs.append(entry)
    with open(CONTRIB_FILE, 'w') as f:
        json.dump(contribs, f, indent=2, ensure_ascii=False)


def score_contribution(title, description):
    text = (title + " " + description).lower()
    keywords = [
        'co2', 'carbon', 'methane', 'ch4', 'biogas', 'biomethane',
        'meg', 'glycol', 'solvent', 'absorption', 'solubility',
        'tio2', 'nanoparticle', 'nanofluid', 'amine', 'pressure',
        'temperature', 'bar', 'kelvin', 'separation', 'upgrading',
        'ccs', 'capture', 'gas', 'equilibrium', 'modeling'
    ]
    spam_words = ['buy now', 'click here', 'casino', 'lottery', 'viagra']
    spam_count = sum(1 for w in spam_words if w in text)
    if spam_count >= 2:
        return {'score': 0.0, 'status': 'rejected',
                'reasons': ['Spam detected']}

    hits = sum(1 for k in keywords if k in text)
    has_numbers = any(c.isdigit() for c in text)
    has_units = any(u in text for u in ['bar', 'k ', 'kelvin', 'mol', 'wt%', 'v/v'])
    has_ref = any(r in text for r in ['thesis', 'doi', 'journal', 'reference', 'study'])

    score = 0
    score += min(hits * 8, 40)
    score += 15 if has_numbers else 0
    score += 10 if has_units else 0
    score += 10 if has_ref else 0
    score += min(len(description) / 200, 1.0) * 20
    score = min(score, 100)

    if score >= 70:
        status = 'accepted'
    elif score >= 40:
        status = 'review'
    else:
        status = 'rejected'

    return {'score': round(score, 1), 'status': status,
            'reasons': ['keyword-based scoring']}


def send_email_to_admin(title, description, ctype, source, email, score, status):
    try:
        from utils.email_sender import notify_contribution
        notify_contribution(title, description, ctype, source, email, score, status)
    except Exception:
        pass


def send_email_to_user(email, title, description, score, status, reasons):
    if not email or '@' not in email:
        return
    try:
        from utils.email_to_user import (
            send_accepted_email, send_review_email, send_rejected_email
        )
        if status == 'accepted':
            send_accepted_email(email, title, description, score)
        elif status == 'review':
            send_review_email(email, title, score)
        else:
            reason = reasons[0] if reasons else None
            send_rejected_email(email, title, score, reason)
    except Exception:
        pass


# Stats
contribs = load_contribs()
total = len(contribs)
accepted = sum(1 for c in contribs if c.get('status') == 'accepted')
pending = sum(1 for c in contribs if c.get('status') == 'pending')

col1, col2, col3 = st.columns(3)
col1.metric("Contributions received", total)
col2.metric("Accepted by AI", accepted)
col3.metric("Under review", pending)

st.markdown("---")

st.markdown("### Submit Your Contribution")

with st.form("contribution_form"):
    title = st.text_input(
        "Title *",
        placeholder="e.g., CO₂ solubility in MEG at 310 K and 20 bar"
    )
    ctype = st.selectbox(
        "Type of contribution",
        ["Experimental data", "Operational observation", "Scientific reference",
         "Personal experience", "Question", "Suggestion"]
    )
    description = st.text_area(
        "Description *",
        placeholder="Describe your contribution in detail. Include numbers, "
                    "units, and references if possible.",
        height=200
    )
    source = st.text_input(
        "Source (optional)",
        placeholder="e.g., DOI, journal name, or URL"
    )
    email = st.text_input("Your email (optional — for follow-up)")
    agree = st.checkbox(
        "I agree to the Terms of Use and confirm this contribution is my own."
    )
    submitted = st.form_submit_button("Submit Contribution", type="primary")

if submitted:
    if not title or not description:
        st.error("Please fill in the required fields (title and description).")
    elif not agree:
        st.error("Please accept the Terms of Use.")
    else:
        result = score_contribution(title, description)

        entry = {
            'timestamp': datetime.now().isoformat(),
            'title': title,
            'description': description,
            'contribution_type': ctype,
            'source': source,
            'email': email,
            'ai_score': result['score'],
            'status': result['status']
        }
        save_contrib(entry)

        # Email to admin
        send_email_to_admin(title, description, ctype, source, email,
                            result['score'], result['status'])

        # Email to user
        send_email_to_user(email, title, description,
                           result['score'], result['status'],
                           result.get('reasons', []))

        # Show result
        if result['status'] == 'accepted':
            st.success(
                f"✅ **Accepted!** AI score: {result['score']}/100. "
                f"This contribution will be integrated into our shared model."
            )
            if email:
                st.info(f"📧 A confirmation email was sent to {email}")
            st.balloons()
        elif result['status'] == 'review':
            st.info(
                f"⏳ **Under review.** AI score: {result['score']}/100. "
                f"A team member will review your contribution within 48 hours."
            )
            if email:
                st.info(f"📧 A notification email was sent to {email}")
        else:
            st.warning(
                f"⚠️ **Not accepted.** AI score: {result['score']}/100. "
                f"Reason: {result['reasons'][0]}"
            )
            if email:
                st.info(f"📧 An email with feedback was sent to {email}")

st.markdown("---")
st.markdown("### Recent Public Contributions")

accepted_list = [c for c in contribs if c.get('status') == 'accepted']
if not accepted_list:
    st.info("No accepted contributions yet — be the first!")
else:
    for c in accepted_list[-10:][::-1]:
        with st.expander(f"**{c['title']}** — score {c['ai_score']}/100"):
            st.write(c['description'])
            st.caption(
                f"Type: {c['contribution_type']} | "
                f"Submitted: {c.get('timestamp', '—')[:19]}"
            )
