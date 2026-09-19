"""DanCarbon Tech — Main Application with professional styling."""
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

# Apply global styling
try:
    from utils.styles import (
        apply_global_styles, hero_section,
        feature_card, stat_card, custom_footer
    )
    apply_global_styles()
    STYLES_OK = True
except Exception:
    STYLES_OK = False


# ==================================================================
# AUTO-TRAIN MODEL (pure numpy, no sklearn)
# ==================================================================
@st.cache_resource
def ensure_model():
    model_path = 'models/rsm_model.pkl'
    data_path = 'data/box_behnken.csv'

    # Try loading existing model
    model = None
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                loaded = pickle.load(f)
            # Verify it's the correct format (dict with 'coef')
            if isinstance(loaded, dict) and 'coef' in loaded:
                model = loaded
        except Exception:
            model = None

    # If no valid model, train a fresh one
    if model is None:
        os.makedirs('models', exist_ok=True)
        df = pd.read_csv(data_path)
        P = df['P_bar'].values.astype(float)
        T = df['T_K'].values.astype(float)
        C = df['TiO2_wt'].values.astype(float)
        y = df['X_vv'].values.astype(float)

        A = np.column_stack([
            np.ones_like(P), P, T, C,
            P**2, T**2, C**2, P*T, P*C, T*C
        ])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        y_pred = A @ coef
        r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)

        model = {'coef': coef, 'r2': float(r2), 'n_points': len(df)}
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

    return model


try:
    model = ensure_model()
    MODEL_READY = True
except Exception as e:
    MODEL_READY = False
    st.error(f"Model setup error: {e}")


# ==================================================================
# HERO
# ==================================================================
if STYLES_OK:
    hero_section(
        title="From Data to Decision — in Minutes",
        subtitle="The first data platform built specifically for CO₂ "
                 "separation in biogas upgrading.",
        badges=[
            "✓ Built on 100+ experiments",
            "✓ Multi-project AutoML",
            "✓ GDPR-compliant"
        ]
    )
else:
    st.title("From Data to Decision — in Minutes")
    st.markdown("*The first data platform built specifically for CO₂ separation.*")

st.markdown("")

# ==================================================================
# CTA BUTTONS
# ==================================================================
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("🚀 Start Free", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🎯_Predictor.py")
with col2:
    if st.button("💰 See Pricing", use_container_width=True):
        st.switch_page("pages/8_💰_Pricing.py")

st.markdown("---")

# ==================================================================
# FEATURES
# ==================================================================
st.markdown("## What You Can Do")

col1, col2, col3 = st.columns(3)

if STYLES_OK:
    with col1:
        feature_card("🎯", "Predict Solubility",
                     "Enter temperature, pressure, and nanoparticle "
                     "concentration — get instant CO₂ solubility prediction.")
    with col2:
        feature_card("🔬", "Multi-Project AutoML",
                     "Create projects for any gas, solvent, or nanoparticle. "
                     "The platform trains models automatically.")
    with col3:
        feature_card("📄", "Automated Reports",
                     "Generate monthly ESG and performance reports with "
                     "environmental data and AI insights.")
else:
    with col1:
        st.markdown("### 🎯 Predict Solubility")
        st.write("Enter temperature, pressure, and concentration.")
    with col2:
        st.markdown("### 🔬 Multi-Project AutoML")
        st.write("Create projects for any gas or solvent.")
    with col3:
        st.markdown("### 📄 Automated Reports")
        st.write("Generate monthly ESG reports.")

st.markdown("")

col1, col2, col3 = st.columns(3)

if STYLES_OK:
    with col1:
        feature_card("🌍", "Crowdsourced Knowledge",
                     "Contribute observations and data. AI filters and "
                     "integrates the useful ones.")
    with col2:
        feature_card("🌤️", "Environmental Intelligence",
                     "Live weather and air quality data for context and "
                     "ESG reporting.")
    with col3:
        feature_card("📊", "Interactive Dashboard",
                     "Explore experimental data, response surfaces, and "
                     "correlations.")
else:
    with col1:
        st.markdown("### 🌍 Crowdsourced Knowledge")
    with col2:
        st.markdown("### 🌤️ Environmental Intelligence")
    with col3:
        st.markdown("### 📊 Interactive Dashboard")

st.markdown("---")

# ==================================================================
# LIVE DEMO (no experimental data shown)
# ==================================================================
if MODEL_READY:
    st.markdown("## Try It Now — Live Demo")
    st.markdown("Move the sliders and see the prediction update instantly.")

    col_in, col_out = st.columns([1, 2])

    with col_in:
        demo_T = st.slider("Temperature (K)", 290.0, 304.0, 297.0, 0.5,
                           key="home_T")
        demo_P = st.slider("Pressure (bar)", 10.0, 25.0, 17.7, 0.1,
                           key="home_P")
        demo_C = st.slider("TiO₂ (wt%)", 0.0, 0.1, 0.05, 0.01, key="home_C")

    with col_out:
        A = np.column_stack([[
            1, demo_P, demo_T, demo_C,
            demo_P**2, demo_T**2, demo_C**2,
            demo_P*demo_T, demo_P*demo_C, demo_T*demo_C
        ]])
        demo_pred = float((A @ model['coef']).ravel()[0])

        st.metric("Predicted CO₂ solubility", f"{demo_pred:.3f} v/v")
        st.caption(f"Model R² = {model['r2']:.4f} on design points")

st.markdown("---")

# ==================================================================
# STATS
# ==================================================================
st.markdown("## Built on Real Science")

col1, col2, col3, col4 = st.columns(4)

if STYLES_OK:
    with col1:
        stat_card("100+", "Experimental runs")
    with col2:
        stat_card("17", "Box-Behnken points")
    with col3:
        stat_card("290–304 K", "Validated T range")
    with col4:
        stat_card("10–25 bar", "Validated P range")
else:
    col1.metric("Experimental runs", "100+")
    col2.metric("Design points", "17")
    col3.metric("Validated T range", "290–304 K")
    col4.metric("Validated P range", "10–25 bar")

st.markdown("---")

# ==================================================================
# CTA BOX
# ==================================================================
if STYLES_OK:
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
else:
    st.markdown("## Ready to get started?")
    st.write("Whether you're a student or a plant operator, we have a plan for you.")

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🚀 Start Free", use_container_width=True,
                 type="primary", key="cta_free"):
        st.switch_page("pages/1_🎯_Predictor.py")
with col2:
    if st.button("📩 Talk to Sales", use_container_width=True,
                 key="cta_sales"):
        st.switch_page("pages/9_📩_Request_Quote.py")

# ==================================================================
# FOOTER
# ==================================================================
if STYLES_OK:
    custom_footer()
else:
    st.markdown("---")
    st.caption(
        f"DanCarbon Tech Platform — MVP v0.3 | "
        f"© {datetime.now().year} DanCarbon Tech ApS | "
        f"rezachash12@gmail.com"
    )
