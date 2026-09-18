"""
DanCarbon Tech — Main Application
Data-driven CO₂ separation for biogas upgrading.

This version auto-trains the baseline model on first load using pickle,
so no manual setup or joblib dependency is required.
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
from datetime import datetime

# ------------------------------------------------------------------
# Page configuration (MUST be the first Streamlit command)
# ------------------------------------------------------------------
st.set_page_config(
    page_title="DanCarbon Tech — CO₂ Separation Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------
# Auto-train model on first load (uses pickle, no joblib)
# ------------------------------------------------------------------
@st.cache_resource
def ensure_model():
    """Load model, or auto-train if it doesn't exist."""
    model_path = 'models/rsm_model.pkl'
    data_path = 'data/box_behnken.csv'

    if not os.path.exists(model_path):
        os.makedirs('models', exist_ok=True)

        # Load data
        df = pd.read_csv(data_path)

        # Train
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import Pipeline

        X = df[['P_bar', 'T_K', 'TiO2_wt']].values
        y = df['X_vv'].values

        model = Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('linear', LinearRegression())
        ])
        model.fit(X, y)

        # Save with pickle
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

    # Load with pickle
    with open(model_path, 'rb') as f:
        return pickle.load(f)


try:
    model = ensure_model()
    MODEL_READY = True
except Exception as e:
    MODEL_READY = False
    st.error(f"⚠️ Model setup error: {e}")
    st.info("Please check that `data/box_behnken.csv` exists in your repository.")

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------
st.markdown("""
<style>
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1F3864;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #2E74B5;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #DEEAF6 0%, #F2F8FD 100%);
        padding: 1.25rem;
        border-radius: 0.75rem;
        border-left: 5px solid #2E74B5;
        height: 100%;
    }
    .feature-card h3 {
        color: #1F3864;
        margin-top: 0;
        font-size: 1.1rem;
    }
    .feature-card p {
        font-size: 0.95rem;
        color: #333;
    }
    .cta-box {
        background: linear-gradient(135deg, #1F3864 0%, #2E74B5 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-top: 2rem;
    }
    .cta-box h2 {
        color: white;
        margin-top: 0;
    }
    .cta-box p {
        color: #DEEAF6;
        font-size: 1.05rem;
    }
    .badge {
        display: inline-block;
        background: #2E74B5;
        color: white;
        padding: 0.3rem 0.85rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# HERO SECTION
# ------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">From Data to Decision — in Minutes</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="hero-subtitle">'
    'The first data platform built specifically for CO₂ separation in biogas upgrading.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="badge">✓ Built on 100+ validated experiments</span>'
    '<span class="badge">✓ Multi-project AutoML</span>'
    '<span class="badge">✓ GDPR-compliant</span>',
    unsafe_allow_html=True
)

st.markdown("")

# CTA buttons
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("🚀 Start Free", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Predictor.py")
with col2:
    if st.button("💰 See Pricing", use_container_width=True):
        st.switch_page("pages/8_💰_Pricing.py")

st.markdown("---")

# ------------------------------------------------------------------
# FEATURES
# ------------------------------------------------------------------
st.markdown("## What You Can Do")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Predict Solubility</h3>
        <p>Enter temperature, pressure, and nanoparticle concentration — get instant CO₂ solubility prediction based on a validated response-surface model.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🔬 Multi-Project AutoML</h3>
        <p>Create projects for any gas, solvent, or nanoparticle. The platform trains a model automatically when enough data is collected.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Automated Reports</h3>
        <p>Generate monthly ESG and performance reports for your plant — including environmental data and AI-generated insights.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🌍 Crowdsourced Knowledge</h3>
        <p>Contribute observations, data, or insights. AI filters contributions and integrates the useful ones into the shared model.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🌤️ Environmental Intelligence</h3>
        <p>Live weather and air quality data to correct predictions for ambient conditions and support ESG reporting.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Interactive Dashboard</h3>
        <p>Explore all experimental data, response surfaces, and correlations — with full export capability.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------
# LIVE DEMO — embedded predictor
# ------------------------------------------------------------------
if MODEL_READY:
    st.markdown("## Try It Now — Live Demo")
    st.markdown("Move the sliders and see the prediction update instantly.")

    col_in, col_out = st.columns([1, 2])

    with col_in:
        demo_T = st.slider("Temperature (K)", 290.0, 304.0, 297.0, 0.5, key="home_T")
        demo_P = st.slider("Pressure (bar)", 10.0, 25.0, 17.7, 0.1, key="home_P")
        demo_C = st.slider("TiO₂ (wt%)", 0.0, 0.1, 0.05, 0.01, key="home_C")

    with col_out:
        demo_pred = float(model.predict(np.array([[demo_P, demo_T, demo_C]]))[0])
        st.metric(
            label="Predicted CO₂ solubility",
            value=f"{demo_pred:.3f} v/v",
            delta="validated range"
        )
        st.caption(
            "Based on the 17-run Box-Behnken design from the founder's MSc thesis. "
            "Model accuracy: R² > 0.90 on design points."
        )

st.markdown("---")

# ------------------------------------------------------------------
# STATS
# ------------------------------------------------------------------
st.markdown("## Built on Real Science")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Experimental runs", "100+")
col2.metric("Design points (Box-Behnken)", "17")
col3.metric("Validated T range", "290–304 K")
col4.metric("Validated P range", "10–25 bar")

st.markdown("---")

# ------------------------------------------------------------------
# CTA BOX
# ------------------------------------------------------------------
st.markdown("""
<div class="cta-box">
    <h2>Ready to get started?</h2>
    <p>
    Whether you're a student designing your first experiment
    or a plant operator optimizing a million-kroner process —
    DanCarbon Tech has a plan for you.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🚀 Start Free", use_container_width=True, type="primary", key="cta_free"):
        st.switch_page("pages/1_🎯_Predictor.py")
with col2:
    if st.button("📩 Talk to Sales", use_container_width=True, key="cta_sales"):
        st.switch_page("pages/9_📩_Request_Quote.py")

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown("---")
st.caption(
    f"DanCarbon Tech Platform — MVP v0.2 | "
    f"© {datetime.now().year} DanCarbon Tech ApS | "
    f"Contact: rezachash12@gmail.com"
)
