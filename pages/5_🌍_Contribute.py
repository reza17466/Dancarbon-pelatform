"""Crowdsourced knowledge contribution page."""
import streamlit as st
import sys
sys.path.append('.')
from utils.db import add_contribution, list_contributions
from utils.ai_filter import score_contribution

st.set_page_config(page_title="Contribute — DanCarbon Tech", page_icon="🌍")

st.title("🌍 Contribute to Climate Research")
st.markdown(
    "Your knowledge matters. Help us accelerate CO₂ separation for a cleaner "
    "future. Every contribution — from a scientific observation to a raw data "
    "point — is filtered by AI and integrated into our shared model."
)

# Stats
contributions = list_contributions()
total = len(contributions)
accepted = len(contributions[contributions['status'] == 'accepted']) if total else 0
pending = len(contributions[contributions['status'] == 'pending']) if total else 0

col1, col2, col3 = st.columns(3)
col1.metric("📊 Contributions received", total)
col2.metric("✅ Accepted by AI", accepted)
col3.metric("⏳ Under review", pending)

st.markdown("---")

# Form
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

    email = st.text_input(
        "Your email (optional — for follow-up)"
    )

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
        # AI filter
        result = score_contribution(title, description)

        # Save
        add_contribution(
            title, description, ctype, source, email,
            result['score'], result['status']
        )

        # Show result
        if result['status'] == 'accepted':
    st.success(
        f"✅ **Accepted!** AI score: {result['score']}/100. "
        f"This contribution will be integrated into our shared model."
    )
    st.balloons()
    st.rerun()
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

# Recent contributions (public feed)
st.markdown("---")
st.markdown("### Recent Public Contributions")

if not contributions.empty:
    public = contributions[contributions['status'] == 'accepted'].head(10)
    if public.empty:
        st.info("No accepted contributions yet — be the first!")
    else:
        for _, c in public.iterrows():
            with st.expander(f"**{c['title']}** — score {c['ai_score']}/100"):
                st.write(c['description'])
                st.caption(f"Type: {c['contribution_type']} | "
                           f"Submitted: {c['created_at']}")
else:
    st.info("Be the first to contribute!")
