"""Pricing page — completely transparent, no confusion."""
import streamlit as st

st.set_page_config(page_title="Pricing — DanCarbon Tech", page_icon="💰",
                   layout="wide")

# ==================================================================
# HEADER
# ==================================================================
st.title("💰 Pricing")
st.markdown("### Know exactly what you get before you pay.")
st.markdown(
    "We offer two types of services. Pick the one that fits how you work."
)
st.markdown("---")

# ==================================================================
# TWO OPTIONS EXPLAINED
# ==================================================================
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 📦 Software Plans")
    st.markdown("**You use it yourself.**")
    st.markdown("""
    - Get instant access
    - Enter your own data
    - Train your own models
    - Download your own reports
    - Cancel anytime
    """)

with col_b:
    st.markdown("### 🎓 Professional Services")
    st.markdown("**We do the work for you.**")
    st.markdown("""
    - You send us your data
    - We analyze, model, and deliver
    - Fixed price per project
    - You receive ready-to-use results
    - No subscription needed
    """)

st.markdown("---")

# ==================================================================
# PART 1: SOFTWARE PLANS
# ==================================================================
st.markdown("## 📦 Software Plans")
st.markdown("*Self-service tools. You stay in control.*")

c1, c2, c3, c4 = st.columns(4)

# --- FREE ---
with c1:
    st.markdown("### 🆓 Free")
    st.markdown("# 0 DKK")
    st.caption("forever")
    st.markdown("---")

    st.markdown("**✅ What you get:**")
    st.markdown("""
    - 1 project workspace
    - Up to 10 data points
    - Interactive CO₂ solubility predictor
    - Response-surface visualization
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Create a project
    - Enter your data
    - Get instant predictions
    """)

    st.markdown("**🎯 Best for:**")
    st.caption("Students, curious researchers")

    if st.button("Start Free", key="free_btn",
                 use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Predictor.py")

# --- STARTER ---
with c2:
    st.markdown("### 💼 Starter")
    st.markdown("# 500 DKK")
    st.caption("per month")
    st.markdown("---")

    st.markdown("**✅ What you get:**")
    st.markdown("""
    - 3 project workspaces
    - Up to 100 data points per project
    - Download data as CSV
    - 1 PDF report per month
    - Environmental data integration
    - Email support (48h)
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Create your projects
    - Enter experimental data
    - Train simple models
    - Export reports
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.caption("Save 20-30% on lab budget by reducing blind experiments")

    st.markdown("**👥 Best for:**")
    st.caption("PhD students, small R&D teams")

    if st.button("Start 14-day Trial", key="starter_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'Starter (500 DKK/month)'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- PROFESSIONAL ---
with c3:
    st.markdown("### 🚀 Professional ⭐")
    st.markdown("# 2,500 DKK")
    st.caption("per month")
    st.markdown("---")

    st.markdown("**✅ What you get:**")
    st.markdown("""
    - 10 project workspaces
    - Up to 1,000 data points per project
    - **AutoML** — train models without coding
    - **API access** — connect your own systems
    - **Unlimited** PDF reports
    - Multi-user accounts (up to 5 users)
    - Priority support (24h)
    - Weather + air quality data
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Enter data once
    - Let AutoML train the model
    - Compare operating scenarios
    - Generate compliance reports
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.caption("Reduce energy costs 5-15%, save 4-6 months of trial-and-error")

    st.markdown("**👥 Best for:**")
    st.caption("Engineering firms, R&D departments")

    if st.button("Start 14-day Trial", key="pro_btn",
                 use_container_width=True, type="primary"):
        st.session_state['requested_plan'] = 'Professional (2,500 DKK/month)'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- ENTERPRISE ---
with c4:
    st.markdown("### 💎 Enterprise")
    st.markdown("# Custom")
    st.caption("contact us")
    st.markdown("---")

    st.markdown("**✅ What you get:**")
    st.markdown("""
    - Unlimited projects & data points
    - Unlimited users
    - **White-label** reports
    - **Federated learning** across sites
    - Custom SLA (99.5% uptime)
    - Dedicated account manager
    - On-site training
    - Priority phone support
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - You run the platform
    - Your team uses it
    - We support you
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.caption("Enterprise-wide optimization, multi-site data intelligence")

    st.markdown("**👥 Best for:**")
    st.caption("Nature Energy, BioCirc, large operators")

    if st.button("Contact Sales", key="ent_btn", use_container_width=True):
        st.session_state['requested_plan'] = 'Enterprise'
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")
st.caption("💡 All software plans: Annual billing = 20% discount")

# ==================================================================
# PART 2: PROFESSIONAL SERVICES
# ==================================================================
st.markdown("## 🎓 Professional Services")
st.markdown("*You send us data. We deliver results.*")

s1, s2, s3 = st.columns(3)

# --- DoE Starter ---
with s1:
    st.markdown("### 📚 DoE Starter")
    st.markdown("# 3,500 DKK")
    st.caption("one-time project")
    st.markdown("---")

    st.markdown("**✅ What you receive:**")
    st.markdown("""
    - Custom Box-Behnken design
    - Optimized experiment list (usually 15-17 runs)
    - Parameter selection guide
    - Statistical analysis plan
    - Ready-to-use lab protocol
    - Delivered as PDF in 3-5 business days
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Tell us your research goal
    - List the parameters you can vary
    - Tell us your budget/time constraints
    - **That's it.**
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.success("Reduce experiments by up to 40% → Save DKK 20,000+ on lab costs")

    st.markdown("**👥 Best for:**")
    st.caption("MSc/PhD students, small research groups")

    if st.button("Order DoE Design", key="doe_btn",
                 use_container_width=True, type="primary"):
        st.session_state['requested_plan'] = 'DoE Starter (3,500 DKK)'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- Data Modeling ---
with s2:
    st.markdown("### 🧠 Data Modeling Expert")
    st.markdown("# from 8,000 DKK")
    st.caption("based on complexity")
    st.markdown("---")

    st.markdown("**✅ What you receive:**")
    st.markdown("""
    - Cleaned and validated dataset
    - Statistical model (regression, RSM, or hybrid)
    - R², RMSE, and residual analysis
    - Interactive visualization dashboard
    - Deployable API endpoint
    - Full technical report
    - Delivered in 7-14 business days
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Send us your raw data (CSV, Excel, PDF)
    - Tell us what you want to predict
    - Tell us the operating window
    - **That's it.**
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.success("Turn scattered data into a predictive model you can use daily")

    st.markdown("**👥 Best for:**")
    st.caption("R&D companies, tech startups")

    if st.button("Request Modeling Quote", key="data_btn",
                 use_container_width=True, type="primary"):
        st.session_state['requested_plan'] = 'Data Modeling Expert'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- Process Audit ---
with s3:
    st.markdown("### 🏭 Process Audit (Gold)")
    st.markdown("# from 100,000 DKK")
    st.caption("project-based")
    st.markdown("---")

    st.markdown("**✅ What you receive:**")
    st.markdown("""
    - On-site visit (2-3 days)
    - Full process thermodynamic analysis
    - Energy consumption breakdown
    - Identification of waste points
    - Optimization recommendations
    - ROI roadmap
    - 40-60 page report
    - Delivered in 4-8 weeks
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Give us site access
    - Share technical documents
    - Arrange operator interviews
    - **That's it.**
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.success("Past audits found 15-30% energy savings → ROI in months")

    st.markdown("**👥 Best for:**")
    st.caption("Petrochemical, biogas, industrial plants")

    if st.button("Request Free Consultation", key="audit_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'Process Audit (Gold)'
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")

# ==================================================================
# PART 3: INDUSTRIAL SOLUTIONS
# ==================================================================
st.markdown("## 🏭 Industrial Solutions")
st.markdown("*For plants installing new systems or seeking CCS compliance.*")

i1, i2 = st.columns(2)

# --- Pilot ---
with i1:
    st.markdown("### 🔬 Pilot Demonstration")
    st.markdown("# from 600,000 DKK")
    st.caption("project-based")
    st.markdown("---")

    st.markdown("**✅ What you receive:**")
    st.markdown("""
    - Skid-mounted pilot unit (5-10 Nm³/h)
    - On-site installation and commissioning
    - 3-6 month validation campaign
    - Real gas performance data
    - Operator training
    - Industrial reference certificate
    - Published case study (optional)
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Provide installation site
    - Supply real biogas feed
    - Assign one operator
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.success("Validated performance on your real gas → Compliance-ready evidence")

    st.markdown("**👥 Best for:**")
    st.caption("Biogas plants with CCS commitments")

    if st.button("Request Pilot Quote", key="pilot_btn",
                 use_container_width=True, type="primary"):
        st.session_state['requested_plan'] = 'Pilot Demonstration'
        st.switch_page("pages/9_📩_Request_Quote.py")

# --- ESG Reports ---
with i2:
    st.markdown("### 📄 ESG Report Service")
    st.markdown("# 25,000 DKK")
    st.caption("per report")
    st.markdown("---")

    st.markdown("**✅ What you receive:**")
    st.markdown("""
    - Monthly automated ESG report
    - CO₂ captured calculation
    - Energy saved metrics
    - Weather and air quality context
    - Compliance-ready format
    - Investor-grade documentation
    - Delivered automatically
    """)

    st.markdown("**📋 What you do:**")
    st.markdown("""
    - Connect your plant to our platform
    - **That's it.**
    """)

    st.markdown("**🎯 Expected outcome:**")
    st.success("Investor-ready ESG documentation every month")

    st.markdown("**👥 Best for:**")
    st.caption("Plants with investor or regulatory reporting needs")

    if st.button("Subscribe to ESG Reports", key="esg_btn",
                 use_container_width=True):
        st.session_state['requested_plan'] = 'ESG Report Service'
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")

# ==================================================================
# PART 4: DECISION GUIDE
# ==================================================================
st.markdown("## 🤔 Not sure which one fits?")

st.markdown("### Answer these 3 questions:")

q1, q2, q3 = st.columns(3)

with q1:
    st.markdown("**1. Do you have in-house engineers?**")
    st.markdown("""
    - ✅ Yes → **Software Plans**
    - ❌ No → **Professional Services**
    """)

with q2:
    st.markdown("**2. Do you want to control everything yourself?**")
    st.markdown("""
    - ✅ Yes → **Software Plans**
    - ❌ No → **Professional Services**
    """)

with q3:
    st.markdown("**3. Do you need a finished result?**")
    st.markdown("""
    - ✅ Yes → **Professional Services**
    - ❌ No → **Software Plans**
    """)

st.markdown("---")

# ==================================================================
# PART 5: FAQ
# ==================================================================
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("What's the difference between Software and Services?"):
    st.write("""
    **Software Plans:** You get access to the platform. You log in, enter
    data, run models, and download reports yourself.

    **Professional Services:** You send us your data or give us site
    access. We do the work and deliver a finished result (design, model,
    report, or validated pilot).
    """)

with st.expander("Can I use both?"):
    st.write("""
    Yes, and many customers do. A typical path:
    1. Start with **Data Modeling** to get a working model
    2. Then subscribe to **Professional** to use it daily
    3. Later, order a **Pilot** to validate at industrial scale
    """)

with st.expander("How do I activate the 14-day trial?"):
    st.write("""
    Click 'Start 14-day Trial' on any plan. Fill in the short form.
    Our team activates your account within 24 hours. No credit card
    required during the trial.
    """)

with st.expander("What payment methods do you accept?"):
    st.write("""
    Bank transfer, credit card, and MobilePay (Denmark). Invoicing is
    available for Enterprise customers and consulting projects.
    """)

with st.expander("Is there a discount for academic users?"):
    st.write("""
    Yes. Universities and research institutions receive 50% discount
    on all Software Plans. Contact us with your academic email.
    """)

with st.expander("What if I'm not satisfied?"):
    st.write("""
    Software plans: 30-day money-back guarantee, no questions asked.
    Professional Services: milestone-based payment, so you pay only
    for completed work.
    """)

# ==================================================================
# PART 6: FINAL CTA
# ==================================================================
st.markdown("---")
st.markdown("## Ready to start?")

col_x, col_y, col_z = st.columns([1, 1, 2])
with col_x:
    if st.button("📩 Contact Sales", type="primary",
                 use_container_width=True, key="bottom_contact"):
        st.switch_page("pages/9_📩_Request_Quote.py")

with col_y:
    if st.button("🚀 Start Free", use_container_width=True,
                 key="bottom_free"):
        st.switch_page("pages/1_🎯_Predictor.py")

st.markdown("---")
st.caption(
    "All prices in DKK, excluding VAT. Software plans can be cancelled "
    "at any time. Consulting projects are quoted individually based on "
    "scope."
)
