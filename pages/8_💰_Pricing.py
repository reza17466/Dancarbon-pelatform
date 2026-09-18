"""Pricing page with working CTAs."""
import streamlit as st

st.set_page_config(page_title="Pricing — DanCarbon Tech", page_icon="💰")

st.title("💰 Pricing")
st.markdown("Choose the plan that fits your needs. All prices in DKK.")

# ==================================================================
# Subscription Plans
# ==================================================================
st.markdown("## Subscription Plans")

col1, col2, col3, col4 = st.columns(4)

# --- FREE ---
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
    if st.button("Start Free", key="free_btn",
                 use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Predictor.py")

# --- STARTER ---
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
    if st.button("Start 14-day Trial", key="starter_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'Starter'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- PROFESSIONAL ---
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
    if st.button("Start 14-day Trial", key="pro_btn",
                 use_container_width=True, type="primary"):
        st.session_state['requested_plan'] = 'Professional'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- ENTERPRISE ---
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
    if st.button("Contact Sales", key="ent_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'Enterprise'
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")
st.caption("💡 Annual billing available — get 2 months free (20% discount)")

# ==================================================================
# Consulting Services
# ==================================================================
st.markdown("## Consulting Services")
st.markdown("One-time engagements, delivered by our process-engineering team.")

col1, col2, col3 = st.columns(3)

# --- DoE Starter ---
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
        "*\"Save 40% on your lab budget. You don't need 100 "
        "experiments — you need the right 15.\"*"
    )
    if st.button("Order Now", key="doe_btn", use_container_width=True):
        st.session_state['requested_plan'] = 'DoE Starter (3,500 DKK)'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- Data Modeling ---
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
    if st.button("Request Quote", key="data_btn", use_container_width=True):
        st.session_state['requested_plan'] = 'Data Modeling Expert (from 8,000 DKK)'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- Process Audit ---
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
    if st.button("Request Free Consultation", key="audit_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'Process Audit (Gold)'
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")

# ==================================================================
# FAQ
# ==================================================================
st.markdown("## Frequently Asked Questions")

with st.expander("How do I activate my 14-day trial?"):
    st.write(
        "Click 'Start 14-day Trial' on any plan, fill in the short "
        "form, and our team will activate your account within 24 hours. "
        "No credit card required during the trial."
    )

with st.expander("Can I change plans later?"):
    st.write(
        "Yes. You can upgrade or downgrade at any time. Changes take "
        "effect at the start of your next billing cycle."
    )

with st.expander("What payment methods do you accept?"):
    st.write(
        "We accept bank transfer, credit card, and MobilePay (Denmark). "
        "Invoicing is available for Enterprise customers."
    )

with st.expander("Is there a discount for academic users?"):
    st.write(
        "Yes. Universities and research institutions receive a 50% "
        "discount on all plans. Contact us for details."
    )

with st.expander("Do you offer a money-back guarantee?"):
    st.write(
        "Yes. If you are not satisfied within the first 30 days, "
        "we offer a full refund — no questions asked."
    )

st.markdown("---")

# ==================================================================
# CTA
# ==================================================================
st.markdown("### Still not sure which plan fits?")
st.write("Talk to our team — we'll help you choose.")

col_a, col_b = st.columns([1, 3])
with col_a:
    if st.button("📩 Contact Sales", type="primary",
                 use_container_width=True, key="bottom_contact"):
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")
st.caption(
    "All prices in DKK, excluding VAT. "
    "Subscription plans can be cancelled at any time. "
    "Consulting services are quoted individually."
)
