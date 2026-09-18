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
        # ذخیره در فایل محلی
        import csv, os
        from datetime import datetime
        os.makedirs('data', exist_ok=True)
        path = 'data/quote_requests.csv'
        file_exists = os.path.exists(path)
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'name', 'company', 'email',
                                 'phone', 'country', 'service', 'description', 'budget'])
            service_str = ", ".join(service) if isinstance(service, list) else service
            writer.writerow([datetime.now().isoformat(), name, company, email,
                             phone, country, service_str, description, budget])

        # ارسال ایمیل
        try:
            from utils.email_sender import notify_quote_request
            service_str = ", ".join(service) if isinstance(service, list) else service
            sent = notify_quote_request(name, company, email, phone, country,
                                         service_str, description, budget)
            if sent:
                st.success(f"✅ Thank you, {name}! We received your request and sent you a confirmation email.")
            else:
                st.success(f"✅ Thank you, {name}! Your request has been saved.")
        except Exception as e:
            st.success(f"✅ Thank you, {name}! Your request has been saved.")

        st.info(f"📧 We'll respond to {email} within 24 hours.")
