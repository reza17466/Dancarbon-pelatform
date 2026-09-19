"""Experimental Validation — scientific transparency."""
import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Validation — DanCarbon Tech",
                   page_icon="🔬", layout="wide")

st.title("🔬 Experimental Validation")
st.markdown(
    "Scientific transparency: comparison of model predictions "
    "with experimental data."
)

st.markdown("---")

# ==================================================================
# LOAD MODEL AND DATA
# ==================================================================
@st.cache_resource
def load_model():
    model_path = 'models/rsm_model.pkl'
    if not os.path.exists(model_path):
        return None
    with open(model_path, 'rb') as f:
        return pickle.load(f)


@st.cache_data
def load_data():
    return pd.read_csv('data/box_behnken.csv')


try:
    model = load_model()
    df = load_data()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

if model is None:
    st.warning("Model not found. Please run the app first.")
    st.stop()

# Build design matrix
def build_design(P, T, C):
    P = np.asarray(P).ravel().astype(float)
    T = np.asarray(T).ravel().astype(float)
    C = np.asarray(C).ravel().astype(float)
    return np.column_stack([
        np.ones_like(P), P, T, C,
        P**2, T**2, C**2, P*T, P*C, T*C
    ])

A = build_design(df['P_bar'], df['T_K'], df['TiO2_wt'])
y_exp = df['X_vv'].values.astype(float)
y_pred = A @ model['coef']

# Compute residuals
residuals = y_exp - y_pred
r2 = model.get('r2', 0)

st.markdown("### 1. Model Performance Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("R²", f"{r2:.4f}")
col2.metric("Experimental points", len(df))
col3.metric("RMSE", f"{np.sqrt(np.mean(residuals**2)):.4f} v/v")
col4.metric("Max residual", f"{np.max(np.abs(residuals)):.4f} v/v")

st.caption(
    "Model: second-order response surface fitted with least-squares "
    "regression. R² is computed on the 17 Box-Behnken design points."
)

st.markdown("---")

# ==================================================================
# PARITY PLOT
# ==================================================================
st.markdown("### 2. Predicted vs Experimental")

col_a, col_b = st.columns([2, 1])

with col_a:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_exp, y=y_pred,
        mode='markers',
        marker=dict(size=12, color='#2E74B5',
                    line=dict(width=1, color='white')),
        name='Design points',
        text=[f"Run #{r}" for r in df['run']],
        hovertemplate=(
            "<b>Run %{text}</b><br>"
            "Experimental: %{x:.3f}<br>"
            "Predicted: %{y:.3f}<extra></extra>"
        )
    ))
    # Diagonal line
    lo = min(min(y_exp), min(y_pred)) * 0.95
    hi = max(max(y_exp), max(y_pred)) * 1.05
    fig.add_trace(go.Scatter(
        x=[lo, hi], y=[lo, hi],
        mode='lines',
        line=dict(dash='dash', color='#9CA3AF'),
        name='Perfect prediction'
    ))
    fig.update_layout(
        xaxis_title="Experimental solubility (v/v)",
        yaxis_title="Predicted solubility (v/v)",
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_xaxes(showgrid=True, gridcolor='#E5E7EB')
    fig.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.markdown("#### Interpretation")
    st.markdown(f"""
    - **Points on diagonal:** perfect prediction
    - **Spread around diagonal:** model error
    - **R² = {r2:.4f}:** model explains {r2*100:.1f}% of variance
    - **RMSE = {np.sqrt(np.mean(residuals**2)):.4f} v/v:** typical error
    """)
    st.info(
        "The model is designed to **interpolate** within the design "
        "space, not extrapolate. Predictions outside 290–304 K, "
        "10–25 bar, or 0–0.1 wt% TiO₂ are not supported."
    )

st.markdown("---")

# ==================================================================
# RESIDUAL ANALYSIS
# ==================================================================
st.markdown("### 3. Residual Analysis")

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("#### Residuals vs Predicted")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=y_pred, y=residuals,
        mode='markers',
        marker=dict(size=10, color='#ED7D31'),
        name='Residuals'
    ))
    fig.add_hline(y=0, line_dash="dash", line_color='#6B7280')
    fig.update_layout(
        xaxis_title="Predicted solubility (v/v)",
        yaxis_title="Residual (exp − pred)",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_yaxes(showgrid=True, gridcolor='#E5E7EB')
    st.plotly_chart(fig, use_container_width=True)

with col_d:
    st.markdown("#### Residual Distribution")
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=residuals,
        nbinsx=8,
        marker_color='#1B365D'
    ))
    fig.update_layout(
        xaxis_title="Residual value",
        yaxis_title="Count",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

st.info(
    "Residuals should be randomly distributed around zero. "
    "Systematic patterns would indicate model misspecification."
)

st.markdown("---")

# ==================================================================
# FULL DATA TABLE
# ==================================================================
st.markdown("### 4. Design Points and Predictions")

results_df = pd.DataFrame({
    'Run': df['run'],
    'P (bar)': df['P_bar'],
    'T (K)': df['T_K'],
    'TiO₂ (wt%)': df['TiO2_wt'],
    'Experimental (v/v)': y_exp,
    'Predicted (v/v)': np.round(y_pred, 3),
    'Residual': np.round(residuals, 4),
})
st.dataframe(results_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ==================================================================
# LITERATURE COMPARISON
# ==================================================================
st.markdown("### 5. Literature Comparison")

st.markdown("""
Our experimental data is consistent with published solubility studies
of CO₂ in glycol-based solvents:

| Source | Solvent | T range | P range | X range | Method |
|--------|---------|---------|---------|---------|--------|
| **This work** | 70 wt% MEG + TiO₂ | 290–304 K | 10–25 bar | 5.8–34.0 v/v | Pressure decay |
| Tang et al. (2011) | Pure MEG | 288–318 K | 5–60 bar | 3–20 v/v | Static cell |
| Wang et al. (2010) | AMP + Sulfolane | 313–373 K | ≤ 193 kPa | — | Equilibrium cell |
| Bohloul et al. (2014) | NMP | 293–333 K | 0.84–1.47 MPa | — | Static method |

**Key observation:** Our values fall within the same order of magnitude
as Tang et al. for pure MEG at comparable conditions, but our
nanoparticle-enhanced system extends the achievable solubility at low
temperature and high pressure.
""")

st.markdown("---")

# ==================================================================
# REPRODUCIBILITY
# ==================================================================
st.markdown("### 6. Reproducibility")

st.markdown("""
All 17 design points were measured under the following protocol:

- **Gas purity:** >99.9 mol% CO₂
- **Equilibrium criterion:** pressure stable ≥30 minutes
- **Cell volume:** 1820 cm³ (loading) + 295 cm³ (absorption)
- **Sensor precision:** ±0.3 K temperature, ±0.1 bar pressure
- **Repeatability check:** centre-point run replicated 5 times

The centre-point replicates showed a standard deviation of less than
0.5% of the mean, confirming that the apparatus is stable and the
dataset is reproducible.
""")

st.markdown("---")

# ==================================================================
# DOWNLOAD
# ==================================================================
st.download_button(
    "📥 Download Full Validation Report (CSV)",
    results_df.to_csv(index=False),
    file_name="DanCarbon_Validation_Report.csv",
    mime="text/csv",
    type="primary"
)

st.caption(
    "Full experimental data, raw pressure-temperature time series, "
    "and calibration files are available under NDA to qualified "
    "partners and grant reviewers."
)
