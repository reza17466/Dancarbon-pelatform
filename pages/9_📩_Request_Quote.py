"""Request a Quote — lead generation form."""
import streamlit as st
from datetime import datetime
import os
import csv

st.set_page_config(page_title="Request a Quote — DanCarbon Tech",
                   page_icon="📩", layout="centered")

st.title("📩 Request a Free Consultation")
st.markdown("Tell us about your project. We respond within 24 hours.")

# Pre-select plan if user came from Pricing
preselected = st.session_state.get('requested_plan', '')

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
        ["Free Plan", "Starter (500 DKK/month)",
         "Professional (2,500 DKK/month)", "Enterprise",
         "DoE Starter (3,500 DKK)",
         "Data Modeling Expert (from 8,000 DKK)",
         "Process Audit (Gold)", "Pilot Demonstration",
         "ESG Report Service", "Other"],
        default=[preselected] if preselected else []
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
        # Save locally
        os.makedirs('data', exist_ok=True)
        path = 'data/quote_requests.csv'
        file_exists = os.path.exists(path)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    'timestamp', 'name', 'company', 'email',
                    'phone', 'country', 'service', 'description', 'budget'
                ])
            service_str = ", ".join(service)
            writer.writerow([
                datetime.now().isoformat(), name, company, email,
                phone, country, service_str, description, budget
            ])

        # Send email to admin
        try:
            from utils.email_sender import notify_quote_request
            service_str = ", ".join(service)
            notify_quote_request(name, company, email, phone, country,
                                 service_str, description, budget)
        except Exception:
            pass

        st.success(f"✅ Thank you, {name}! We received your request.")
        st.info(f"📧 We'll respond to {email} within 24 hours.")
        st.balloons()

        # Clear preselected plan
        if 'requested_plan' in st.session_state:
            del st.session_state['requested_plan']

st.markdown("---")
st.markdown("### 📞 Or contact us directly")
st.markdown("""
- 📧 **Email:** rezachash12@gmail.com
- 🔗 **LinkedIn:** [Reza Chash](https://www.linkedin.com/in/reza-chash-9735ab141)
- 🌐 **Platform:** https://dancarbon-techa-oceee8umnrb6ywynapwuzw.streamlit.app
""")
