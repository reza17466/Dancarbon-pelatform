"""
DanCarbon Tech — Main Application
Pure-numpy model — no scikit-learn dependency.
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
from datetime import datetime

st.set_page_config(
    page_title="DanCarbon Tech — CO₂ Separation Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------------
# Pure-numpy quadratic regression
# ------------------------------------------------------------------
def build_design_matrix(P, T, C):
    """Quadratic design matrix for response surface."""
    P = np.asarray(P).ravel().astype(float)
    T = np.asarray(T).ravel().astype(float)
    C = np.asarray(C).ravel().astype(float)
    return np.column_stack([
        np.ones_like(P),
        P, T, C,
        P**2, T**2, C**2,
        P*T, P*C, T*C
    ])


def train_rsm(df):
    """Train quadratic model with least squares."""
    A = build_design_matrix(df['P_bar'], df['T_K'], df['TiO2_wt'])
    y = df['X_vv'].values.astype(float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    # Compute R²
    y_pred = A @ coef
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    return {'coef': coef, 'r2': r2}


def predict(model, P, T, C):
    A = build_design_matrix([P], [T], [C])
    return float(A @ model['coef'])


@st.cache_resource
def ensure_model():
    """Load model, or auto-train if it doesn't exist."""
    model_path = 'models/rsm_model.pkl'
    data_path = 'data/box_behnken.csv'

    if not os.path.exists(model_path):
        os.makedirs('models', exist_ok=True)
        df = pd.read_csv(data_path)
        model = train_rsm(df)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

    with open(model_path, 'rb') as f:
        return pickle.load(f)


try:
    model = ensure_model()
    MODEL_READY = True
except Exception as e:
    MODEL_READY = False
    st.error(f"⚠️ Model setup error: {e}")


# ------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------
st.markdown("""
<style>
    .hero-title {
        font-size: 2.8rem; font-weight: 800; color: #1F3864;
        line-height: 1.1; margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem; color: #2E74B5; margin-bottom: 1.5rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #DEEAF6 0%, #F2F8FD 100%);
        padding: 1.25rem; border-radius: 0.75rem;
        border-left: 5px solid #2E74B5; height: 100%;
    }
    .feature-card h3 { color: #1F3864; margin-top: 0; font-size: 1.1rem; }
    .feature-card p { font-size: 0.95rem; color: #333; }
    .cta-box {
        background: linear-gradient(135deg, #1F3864 0%, #2E74B5 100%);
        color: white; padding: 2rem; border-radius: 1rem;
        text-align: center; margin-top: 2rem;
    }
    .cta-box h2 { color: white; margin-top: 0; }
    .cta-box p { color: #DEEAF6; font-size: 1.05rem; }
    .badge {
        display: inline-block; background: #2E74B5; color: white;
        padding: 0.3rem 0.85rem; border-radius: 1rem;
        font-size: 0.85rem; margin-right: 0.5rem; margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
st.markdown('<div class="hero-title">From Data to Decision — in Minutes</div>',
            unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">'
            'The first data platform built specifically for CO₂ separation in biogas upgrading.'
            '</div>', unsafe_allow_html=True)
st.markdown(
    '<span class="badge">✓ Built on 100+ validated experiments</span>'
    '<span class="badge">✓ Multi-project AutoML</span>'
    '<span class="badge">✓ GDPR-compliant</span>',
    unsafe_allow_html=True
)
st.markdown("")

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
        <p>Enter temperature, pressure, and nanoparticle concentration — get instant CO₂ solubility prediction.</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🔬 Multi-Project AutoML</h3>
        <p>Create projects for any gas, solvent, or nanoparticle. Models train automatically.</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 Automated Reports</h3>
        <p>Monthly ESG and performance reports — including environmental data and AI insights.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🌍 Crowdsourced Knowledge</h3>
        <p>Contribute observations and data. AI filters and integrates the useful ones.</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🌤️ Environmental Intelligence</h3>
        <p>Live weather and air quality data for context and ESG reporting.</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Interactive Dashboard</h3>
        <p>Explore experimental data, response surfaces, and correlations.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------
# LIVE DEMO
# ------------------------------------------------------------------
if MODEL_READY:
    st.markdown("## Try It Now — Live Demo")

    col_in, col_out = st.columns([1, 2])
    with col_in:
        demo_T = st.slider("Temperature (K)", 290.0, 304.0, 297.0, 0.5, key="home_T")
        demo_P = st.slider("Pressure (bar)", 10.0, 25.0, 17.7, 0.1, key="home_P")
        demo_C = st.slider("TiO₂ (wt%)", 0.0, 0.1, 0.05, 0.01, key="home_C")

    with col_out:
        demo_pred = predict(model, demo_P, demo_T, demo_C)
        st.metric("Predicted CO₂ solubility", f"{demo_pred:.3f} v/v")
        st.caption(f"Model R² = {model['r2']:.4f} on design points")

st.markdown("---")

st.markdown("## Built on Real Science")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Experimental runs", "100+")
col2.metric("Design points", "17")
col3.metric("Validated T range", "290–304 K")
col4.metric("Validated P range", "10–25 bar")

st.markdown("---")

st.markdown("""
<div class="cta-box">
    <h2>Ready to get started?</h2>
    <p>Whether you're a student or a plant operator — DanCarbon Tech has a plan for you.</p>
</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🚀 Start Free", use_container_width=True, type="primary", key="cta_free"):
        st.switch_page("pages/1_🎯_Predictor.py")
with col2:
    if st.button("📩 Talk to Sales", use_container_width=True, key="cta_sales"):
        st.switch_page("pages/9_📩_Request_Quote.py")

st.markdown("---")
st.caption(f"DanCarbon Tech Platform — MVP v0.3 | © {datetime.now().year} | Contact: rezachash12@gmail.com")
