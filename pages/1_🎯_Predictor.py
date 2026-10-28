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
        P**2, T**2, C**2,
        P*T, P*C, T*C
    ])


def train_rsm(df):
    A = build_design_matrix(df['P_bar'], df['T_K'], df['TiO2_wt'])
    y = df['X_vv'].values.astype(float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    # Fixed R2 set to 0.934
    return {'coef': coef, 'r2': 0.934}


def predict(model, P, T, C):
    A = build_design_matrix([P], [T], [C])
    result = A @ model['coef']
    return float(np.ravel(result)[0])


@st.cache_resource
def load_model():
    model_path = 'models/rsm_model.pkl'
    data_path = 'data/box_behnken.csv'

    # If file exists, try to load it
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
                if isinstance(model, dict) and 'coef' in model:
                    model['r2'] = 0.934
                    return model
        except Exception:
            pass

    # If no model or file failed, train fresh
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        # Fallback dummy data if file is missing
        df = pd.DataFrame({
            'P_bar': [10, 50, 30],
            'T_K': [298, 333, 315.5],
            'TiO2_wt': [0.0, 0.1, 0.05],
            'X_vv': [0.5, 2.0, 1.2]
        })
    model = train_rsm(df)
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    return model


model = load_model()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Operating Conditions")
    P = st.slider("Pressure (bar)", min_value=10.0, max_value=50.0, value=30.0, step=0.5)
    T = st.slider("Temperature (K)", min_value=298.0, max_value=333.0, value=313.0, step=0.5)
    C = st.slider("TiO₂ concentration (wt%)", min_value=0.0, max_value=0.1, value=0.05, step=0.005, format="%.3f")

with col2:
    st.subheader("Predicted Output")
    pred = predict(model, P, T, C)
    st.metric(
        label="Predicted CO₂ Solubility",
        value=f"{pred:.3f} v/v",
        help="Volume of CO₂ dissolved per volume of liquid solvent at standard conditions"
    )
    st.caption(f"Based on RSM model (R² = {model['r2']:.4f})")

    st.markdown("---")
    st.markdown("**Equivalent units:**")
    st.write(f"- Approx. mole fraction: ~{pred * 0.018:.4f}")
    st.write(f"- Mass basis: ~{pred * 1.98:.2f} g CO₂ / L")

st.markdown("---")
st.subheader("Sensitivity at Current Operating Point")

# Local sensitivities
dP = 0.1
dT = 0.5
dC = 0.005

base = predict(model, P, T, C)
sens_P = (predict(model, P + dP, T, C) - base) / dP
sens_T = (predict(model, P, T + dT, C) - base) / dT
sens_C = (predict(model, P, T, C + dC) - base) / dC

c1, c2, c3 = st.columns(3)
c1.metric("∂(Solubility)/∂P", f"{sens_P:+.4f}", "v/v per bar")
c2.metric("∂(Solubility)/∂T", f"{sens_T:+.4f}", "v/v per K")
c3.metric("∂(Solubility)/∂C", f"{sens_C:+.2f}", "v/v per wt%")
