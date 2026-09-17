"""Pricing page with plans and services."""
import streamlit as st

st.set_page_config(page_title="Pricing — DanCarbon Tech", page_icon="💰")

st.title("💰 Pricing")
st.markdown("Choose the plan that fits your needs.")

# Subscription plans
st.markdown("## Subscription Plans")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🆓 Free")
    st.markdown("**0 DKK / month**")
    st.markdown("""
    - 1 project
    - Up to 10 data points
    - Interactive predictor
    - Response-surface visualization
    - Community support
    """)
    if st.button("Start Free", key="free", use_container_width=True):
        st.switch_page("pages/1_🎯_Predictor.py")

with col2:
    st.markdown("### 💼 Starter")
    st.markdown("**500 DKK / month**")
    st.markdown("""
    - 3 projects
    - Up to 100 data points
    - Download as CSV
    - 1 PDF report / month
    - Environmental data
    - Email support
    """)
    if st.button("Start 14-day Trial", key="starter", use_container_width=True):
        st.info("Trial activation coming soon. Contact us for early access.")

with col3:
    st.markdown("### 🚀 Professional ⭐")
    st.markdown("**2,500 DKK / month**")
    st.markdown("""
    - 10 projects
    - Up to 1,000 data points
    - **AutoML** (auto model training)
    - **API access**
    - Unlimited PDF reports
    - Multi-user accounts
    - Priority support
    """)
    if st.button("Start 14-day Trial", key="pro", type="primary",
                 use_container_width=True):
        st.info("Trial activation coming soon. Contact us for early access.")

with col4:
    st.markdown("### 💎 Enterprise")
    st.markdown("**Contact us**")
    st.markdown("""
    - Unlimited projects & points
    - White-label reports
    - Federated learning
    - Custom SLA (99.5%)
    - Dedicated account manager
    - On-site training
    """)
    if st.button("Request a Quote", key="enterprise", use_container_width=True):
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")
st.caption("💡 Annual billing: get 2 months free (20% discount)")

# Consulting services
st.markdown("## Consulting Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📚 DoE Starter")
    st.markdown("**3,500 DKK** (one-time)")
    st.markdown("""
    Experimental design for researchers.
    - Box-Behnken design
    - Parameter selection
    - Reduce experiments by up to 40%
    - Delivery: 3–5 business days
    """)
    st.markdown(
        "*\"Save 40% on your lab budget. You don't need 100 experiments — "
        "you need the right 15.\"*"
    )

with col2:
    st.markdown("### 🧠 Data Modeling Expert")
    st.markdown("**from 8,000 DKK**")
    st.markdown("""
    Turn raw data into predictive models.
    - Regression modeling
    - Residual analysis
    - R² reporting
    - Deployable API endpoint
    - Delivery: 7–14 business days
    """)
    st.markdown(
        "*\"Turn your raw data into predictive power. "
        "Get a deployable model, not a spreadsheet.\"*"
    )

with col3:
    st.markdown("### 🏭 Process Audit (Gold)")
    st.markdown("**Custom pricing**")
    st.markdown("""
    Full-scale industrial optimization.
    - Process efficiency analysis
    - Thermodynamic assessment
    - Energy-saving recommendations
    - On-site visit included
    - Delivery: 4–8 weeks
    """)
    st.markdown(
        "*\"Where is your energy going? Past audits identified "
        "15–30% energy savings.\"*"
    )

st.markdown("---")
if st.button("📩 Request a Custom Quote", type="primary"):
    st.switch_page("pages/9_📩_Request_Quote.py")
