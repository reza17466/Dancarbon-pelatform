ص"""Interactive Predictor — pure numpy."""
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
        np.ones_like(P),
        P, T, C,
        P**2, T**2, C**2,
        P*T, P*C, T*C
    ])


def train_rsm(df):
    A = build_design_matrix(df['P_bar'], df['T_K'], df['TiO2_wt'])
    y = df['X_vv'].values.astype(float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    y_pred = A @ coef
    r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)
    return {'coef': coef, 'r2': r2}


def predict(model, P, T, C):
    A = build_design_matrix([P], [T], [C])
    return float((A @ model['coef']).item())


@st.cache_resource
def load_model():
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


@st.cache_data
def load_data():
    return pd.read_csv('data/box_behnken.csv')


try:
    model = load_model()
    df = load_data()
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

    df_temp = df.copy()
    df_temp['distance'] = np.sqrt(
        ((df_temp['P_bar'] - P) / 15) ** 2 +
        ((df_temp['T_K'] - T) / 14) ** 2 +
        ((df_temp['TiO2_wt'] - C) / 0.1) ** 2
    )
    nearest = df_temp.loc[df_temp['distance'].idxmin()]

    st.markdown("### Prediction")
    col_a, col_b = st.columns(2)
    col_a.metric("Predicted CO₂ solubility", f"{pred:.3f} v/v")
    col_b.metric("Nearest experimental", f"{nearest['X_vv']:.3f} v/v",
                 delta=f"Δ {pred - nearest['X_vv']:+.3f}")

    st.markdown("### Confidence")
    d = nearest['distance']
    if d < 0.1:
        st.success(f"✅ High confidence — near run #{int(nearest['run'])}")
    elif d < 0.3:
        st.info("ℹ️ Moderate confidence — within design space")
    else:
        st.warning("⚠️ Lower confidence — edge of validated window")

    st.markdown(f"**Model quality:** R² = {model['r2']:.4f}")

    st.markdown("### Experimental dataset")
    df_display = df[['run', 'P_bar', 'T_K', 'TiO2_wt', 'X_vv']].copy()
    df_display.columns = ['Run', 'P (bar)', 'T (K)', 'TiO₂ (wt%)', 'X (v/v)']
    st.dataframe(df_display, use_container_width=True, height=250)

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
