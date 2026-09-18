"""Interactive Predictor page."""
import streamlit as st
import numpy as np
import pandas as pd
import os
import pickle
import plotly.graph_objects as go

st.set_page_config(page_title="Predictor — DanCarbon Tech", page_icon="🎯")

st.title("🎯 Interactive Predictor")
st.markdown("Adjust parameters and get an instant prediction of CO₂ solubility.")


@st.cache_resource
def load_model():
    """Load model, or auto-train if missing."""
    model_path = 'models/rsm_model.pkl'
    data_path = 'data/box_behnken.csv'

    if not os.path.exists(model_path):
        os.makedirs('models', exist_ok=True)

        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import Pipeline

        df = pd.read_csv(data_path)
        X = df[['P_bar', 'T_K', 'TiO2_wt']].values
        y = df['X_vv'].values

        model = Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('linear', LinearRegression())
        ])
        model.fit(X, y)

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

# Layout
col_input, col_output = st.columns([1, 2])

with col_input:
    st.markdown("### Input Parameters")
    T = st.slider("Temperature (K)", 290.0, 304.0, 297.0, 0.5)
    P = st.slider("Pressure (bar)", 10.0, 25.0, 17.7, 0.1)
    C = st.slider("TiO₂ concentration (wt%)", 0.0, 0.1, 0.05, 0.01)

    st.markdown("---")
    st.caption(
        "The operating window is bounded by the validated experimental "
        "design. Predictions outside this range are not supported."
    )

with col_output:
    X = np.array([[P, T, C]])
    pred = float(model.predict(X)[0])

    # Nearest experimental point
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
    col_b.metric("Nearest experimental",
                 f"{nearest['X_vv']:.3f} v/v",
                 delta=f"Δ {pred - nearest['X_vv']:+.3f}")

    st.markdown("### Confidence")
    d = nearest['distance']
    if d < 0.1:
        st.success(f"✅ High confidence — near run #{int(nearest['run'])}")
    elif d < 0.3:
        st.info("ℹ️ Moderate confidence — within design space")
    else:
        st.warning("⚠️ Lower confidence — edge of validated window")

    # Mini comparison chart
    st.markdown("### Context")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['X_vv'], y=df['T_K'],
        mode='markers',
        name='Experimental data',
        marker=dict(size=10, color=df['X_vv'], colorscale='Viridis',
                    showscale=True)
    ))
    fig.add_trace(go.Scatter(
        x=[pred], y=[T],
        mode='markers',
        name='Your prediction',
        marker=dict(size=20, color='red', symbol='star')
    ))
    fig.update_layout(
        xaxis_title="CO₂ solubility (v/v)",
        yaxis_title="Temperature (K)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Download CSV
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
