a"""Crowdsourced knowledge contribution page."""
import streamlit as st
import sys
import os
sys.path.append('.')

# Try importing local utilities; if unavailable, use fallbacks
try:
    from utils.db import add_contribution, list_contributions
    from utils.ai_filter import score_contribution
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

st.set_page_config(page_title="Contribute — DanCarbon Tech", page_icon="🌍")

st.title("🌍 Contribute to Climate Research")
st.markdown(
    "Your knowledge matters. Help us accelerate CO₂ separation for a cleaner "
    "future. Every contribution — from a scientific observation to a raw data "
    "point — is filtered by AI and integrated into our shared model."
)

# ------------------------------------------------------------------
# Fallback: simple JSON-based storage if utils.db not available
# ------------------------------------------------------------------
CONTRIB_FILE = "data/contributions.json"


def _load_contribs():
    if not os.path.exists(CONTRIB_FILE):
        return []
    import json
    with open(CONTRIB_FILE, 'r') as f:
        return json.load(f)


def _save_contrib(entry):
    import json
    os.makedirs('data', exist_ok=True)
    contribs = _load_contribs()
    contribs.append(entry)
    with open(CONTRIB_FILE, 'w') as f:
        json.dump(contribs, f, indent=2)


def _score_fallback(title, description):
    """Simple keyword-based scoring if ai_filter not available."""
    text = (title + " " + description).lower()
    keywords = [
        'co2', 'carbon', 'methane', 'ch4', 'biogas', 'biomethane',
        'meg', 'glycol', 'solvent', 'absorption', 'solubility',
        'tio2', 'nanoparticle', 'nanofluid', 'amine', 'pressure',
        'temperature', 'bar', 'kelvin', 'separation', 'upgrading',
        'ccs', 'capture', 'gas', 'equilibrium', 'modeling'
    ]
    hits = sum(1 for k in keywords if k in text)
    has_numbers = any(c.isdigit() for c in text)
    has_units = any(u in text for u in ['bar', 'k ', 'kelvin', 'mol', 'wt%', 'v/v'])
    score = min(hits * 8, 40) + (15 if has_numbers else 0) + (10 if has_units else 0)
    score = min(score, 100)
    if score >= 70:
        status = 'accepted'
    elif score >= 40:
        status = 'review'
    else:
        status = 'rejected'
    return {'score': float(score), 'status': status,
            'reasons': ['keyword-based fallback']}


# ------------------------------------------------------------------
# Stats
# ------------------------------------------------------------------
if DB_AVAILABLE:
    try:
        contributions = list_contributions()
        total = len(contributions)
        accepted = len(contributions[contributions['status'] == 'accepted']) if total else 0
        pending = len(contributions[contributions['status'] == 'pending']) if total else 0
    except Exception:
        contributions = None
        total = accepted = pending = 0
else:
    contributions = _load_contribs()
    total = len(contributions)
    accepted = sum(1 for c in contributions if c.get('status') == 'accepted')
    pending = sum(1 for c in contributions if c.get('status') == 'pending')

col1, col2, col3 = st.columns(3)
col1.metric("📊 Contributions received", total)
col2.metric("✅ Accepted by AI", accepted)
col3.metric("⏳ Under review", pending)

st.markdown("---")

# ------------------------------------------------------------------
# Form
# ------------------------------------------------------------------
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
        # Score with AI filter or fallback
        if DB_AVAILABLE:
            try:
                result = score_contribution(title, description)
            except Exception:
                result = _score_fallback(title, description)
        else:
            result = _score_fallback(title, description)

        # Save
        if DB_AVAILABLE:
            try:
                add_contribution(
                    title, description, ctype, source, email,
                    result['score'], result['status']
                )
            except Exception:
                _save_contrib({
                    'title': title, 'description': description,
                    'contribution_type': ctype, 'source': source,
                    'email': email, 'ai_score': result['score'],
                    'status': result['status']
                })
        else:
            _save_contrib({
                'title': title, 'description': description,
                'contribution_type': ctype, 'source': source,
                'email': email, 'ai_score': result['score'],
                'status': result['status']
            })

        # Show result
        if result['status'] == 'accepted':
            # ارسال ایمیل
try:
    from utils.email_sender import notify_contribution
    notify_contribution(title, description, ctype, source, email,
                        result['score'], result['status'])
except Exception:
    pass
            st.success(
                f"✅ **Accepted!** AI score: {result['score']}/100. "
                f"This contribution will be integrated into our shared model."
            )
            st.balloons()
        elif result['status'] == 'review':
            st.info(
                f"⏳ **Under review.** AI score: {result['score']}/100. "
                f"A team member will review your contribution within 48 hours."
            )
        else:
            st.warning(
                f"⚠️ **Not accepted.** AI score: {result['score']}/100. "
                f"Reason: {result['reasons'][0]}"
            )

# ------------------------------------------------------------------
# Recent contributions
# ------------------------------------------------------------------
st.markdown("---")
st.markdown("### Recent Public Contributions")

if DB_AVAILABLE and contributions is not None and not contributions.empty:
    public = contributions[contributions['status'] == 'accepted'].head(10)
    if public.empty:
        st.info("No accepted contributions yet — be the first!")
    else:
        for _, c in public.iterrows():
            with st.expander(f"**{c['title']}** — score {c['ai_score']}/100"):
                st.write(c['description'])
                st.caption(
                    f"Type: {c['contribution_type']} | "
                    f"Submitted: {c['created_at']}"
                )
elif not DB_AVAILABLE:
    accepted_list = [c for c in contributions if c.get('status') == 'accepted']
    if not accepted_list:
        st.info("No accepted contributions yet — be the first!")
    else:
        for c in accepted_list[:10]:
            with st.expander(f"**{c['title']}** — score {c['ai_score']}/100"):
                st.write(c['description'])
                st.caption(f"Type: {c['contribution_type']}")
