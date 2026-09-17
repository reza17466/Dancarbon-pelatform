"""Lead generation form."""
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Request a Quote — DanCarbon Tech", page_icon="📩")

st.title("📩 Request a Free Consultation")
st.markdown("Tell us about your project. We respond within 24 hours.")

with st.form("quote_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name *")
    company = col2.text_input("Company / University")

    col1, col2 = st.columns(2)
    email = col1.text_input("Email *")
    phone = col2.text_input("Phone")

    country = st.text_input("Country", value="Denmark")

    service = st.multiselect(
        "Service of Interest *",
        ["DoE Starter", "Data Modeling Expert", "Process Audit (Gold)",
         "SaaS Subscription", "Other"]
    )

    description = st.text_area(
        "Brief Description of Your Needs",
        height=150,
        placeholder="Tell us about your process, data, or challenge..."
    )

    budget = st.selectbox(
        "Budget Range (optional)",
        ["Not sure yet", "< 10,000 DKK", "10,000 – 50,000 DKK",
         "50,000 – 200,000 DKK", "> 200,000 DKK"]
    )

    submitted = st.form_submit_button("Submit Request", type="primary")

if submitted:
    if not name or not email or not service:
        st.error("Please fill in all required fields (*)")
    else:
        # For MVP: store in database (or send email via API)
        st.success(
            f"✅ **Thank you, {name}!** "
            f"We've received your request and will respond within 24 hours."
        )
        st.info(
            "📌 For immediate assistance, contact us directly:\n\n"
            "📧 rezachash12@gmail.com\n"
            "🔗 [LinkedIn](https://www.linkedin.com/in/reza-chash-9735ab141)"
        )
        # TODO: Add email notification (SendGrid, Resend, etc.)
