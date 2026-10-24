"""Interactive Predictor — no experimental data shown."""
import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle

st.set_page_config(page_title="Predictor — DanCarbon Tech", page_icon="🎯")

st.title("🎯 Interactive Predictor")
st.markdown("Adjust parameters and get an instant prediction of CO₂ solubility.")


def build_design_matrix(P, T, C):
    P = np.asarray(P).ravel().astype(float)
    T = np.asarray(T).ravel().astype(float)
    C = np.asarray(C).ravel().astype(float)
    return np.column_stack([
        np.ones_like(P), P, T, C,
        P**2, T**2, C**2, P*T, P*C, T*C
    ])


def predict(model, P, T, C):
    A = build_design_matrix([P], [T], [C])
    result = A @ model['coef']
    return float(np.ravel(result)[0])


@st.cache_resource
def load_model():
    coef = np.array([
        -756.75895,  # Intercept
        -0.642721,   # P
        5.43370,     # T
        494.50100,   # C (TiO2 wt%)
        -0.015591,   # P^2
        -0.009776,   # T^2
        374.20000,   # C^2
        0.007495,    # P*T
        -6.38000,    # P*C
        -1.56857     # T*C
    ])
    return {
        'coef': coef,
        'r2': 0.9969,
        'n_points': 17
    }




try:
    model = load_model()
except Exception as e:
    st.error(f"Setup error: {e}")
    st.stop()

col_input, col_output = st.columns([1, 2])

with col_input:
    st.markdown("### Input Parameters")
    T = st.slider("Temperature (K)", 290.0, 304.0, 297.0, 0.5)
    P = st.slider("Pressure (bar)", 10.0, 25.0, 17.7, 0.1)
    C = st.slider("TiO₂ concentration (wt%)", 0.0, 0.1, 0.05, 0.01)
    st.caption("Predictions are bounded by the validated experimental window.")

with col_output:
    pred = predict(model, P, T, C)

    st.markdown("### Prediction")
    st.metric("Predicted CO₂ solubility", f"{pred:.3f} v/v")

    st.markdown("### Model Quality")
    r2 = model.get('r2', 0)
    if r2 >= 0.9:
        st.success(f"✅ R² = {r2:.4f} — High confidence")
    elif r2 >= 0.8:
        st.info(f"ℹ️ R² = {r2:.4f} — Moderate confidence")
    else:
        st.warning(f"⚠️ R² = {r2:.4f} — Lower confidence")

    st.caption(
        "Predictions are based on a validated response-surface model. "
        "The underlying experimental dataset is proprietary and not "
        "displayed publicly."
    )

st.markdown("---")
result_df = pd.DataFrame([{
    'Temperature_K': T, 'Pressure_bar': P, 'TiO2_wt': C,
    'Predicted_solubility_vv': pred
}])
st.download_button(
    "📥 Download result as CSV",
    result_df.to_csv(index=False),
    file_name=f"prediction_{P}bar_{T}K.csv"
)
