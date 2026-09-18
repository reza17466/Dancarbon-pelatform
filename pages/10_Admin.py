"""Admin Dashboard — review and integrate contributions."""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
import pickle
from datetime import datetime

st.set_page_config(page_title="Admin — DanCarbon Tech", page_icon="📊")

st.title("📊 Admin Dashboard")
st.caption("Review contributions and integrate them into the shared model.")

# ------------------------------------------------------------------
# Load contributions
# ------------------------------------------------------------------
DB_PATH = "data/dancarbon.db"
EXTRACTED_CSV = "data/extracted_data.csv"


def load_contributions():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM contributions ORDER BY created_at DESC", conn
        )
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df


def update_status(contrib_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE contributions SET status = ? WHERE contrib_id = ?",
              (new_status, contrib_id))
    conn.commit()
    conn.close()


def append_extracted_data(contrib_id, pressure, temperature, concentration, absorption):
    """Append manually entered data to the extracted CSV."""
    new_row = pd.DataFrame([{
        'contrib_id': contrib_id,
        'pressure': pressure,
        'temperature': temperature,
        'concentration': concentration,
        'absorption': absorption,
        'added_at': datetime.now().isoformat()
    }])
    if os.path.exists(EXTRACTED_CSV):
        existing = pd.read_csv(EXTRACTED_CSV)
        combined = pd.concat([existing, new_row], ignore_index=True)
    else:
        combined = new_row
    combined.to_csv(EXTRACTED_CSV, index=False)


def retrain_global_model():
    """Retrain the global model with box_behnken + extracted data."""
    # Load baseline data
    baseline = pd.read_csv('data/box_behnken.csv')
    baseline = baseline.rename(columns={
        'P_bar': 'pressure', 'T_K': 'temperature',
        'TiO2_wt': 'concentration', 'X_vv': 'absorption'
    })[['pressure', 'temperature', 'concentration', 'absorption']]

    # Add extracted data if exists
    if os.path.exists(EXTRACTED_CSV):
        extra = pd.read_csv(EXTRACTED_CSV)[
            ['pressure', 'temperature', 'concentration', 'absorption']
        ]
        combined = pd.concat([baseline, extra], ignore_index=True)
    else:
        combined = baseline

    # Train quadratic model
    def build_design_matrix(P, T, C):
        P = np.asarray(P).ravel().astype(float)
        T = np.asarray(T).ravel().astype(float)
        C = np.asarray(C).ravel().astype(float)
        return np.column_stack([
            np.ones_like(P), P, T, C,
            P**2, T**2, C**2, P*T, P*C, T*C
        ])

    A = build_design_matrix(combined['pressure'], combined['temperature'],
                            combined['concentration'])
    y = combined['absorption'].values.astype(float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    y_pred = A @ coef
    r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)

    model = {'coef': coef, 'r2': float(r2), 'n_points': len(combined)}

    os.makedirs('models', exist_ok=True)
    with open('models/rsm_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return model


# ------------------------------------------------------------------
# Main layout
# ------------------------------------------------------------------
df = load_contributions()

if df.empty:
    st.info("No contributions yet.")
else:
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(df))
    col2.metric("✅ Accepted",
                len(df[df['status'] == 'accepted']))
    col3.metric("⏳ Review",
                len(df[df['status'] == 'review']))
    col4.metric("❌ Rejected",
                len(df[df['status'] == 'rejected']))

    st.markdown("---")

    # Filter tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["✅ Accepted", "⏳ Review", "❌ Rejected", "📦 All"]
    )

    def show_contributions(subset, tab_key):
        if subset.empty:
            st.info("No items in this category.")
            return
        for _, row in subset.iterrows():
            cid = int(row['contrib_id'])
            title = row['title']
            score = row['ai_score']
            with st.expander(f"**{title}** — Score: {score}/100"):
                st.write(row['description'])
                st.caption(
                    f"Type: {row['contribution_type']} | "
                    f"Source: {row.get('source', '—')} | "
                    f"Email: {row.get('email', '—')} | "
                    f"Submitted: {row['created_at']}"
                )

                # Manual data entry for integration
                if row['status'] in ('accepted', 'review'):
                    st.markdown("**Integrate into model** (manual data entry)")
                    with st.form(f"integrate_{cid}_{tab_key}"):
                        c1, c2, c3, c4 = st.columns(4)
                        p = c1.number_input("P (bar)", 0.0, 100.0, 17.7,
                                             key=f"ip_{cid}_{tab_key}")
                        t = c2.number_input("T (K)", 200.0, 500.0, 297.0,
                                             key=f"it_{cid}_{tab_key}")
                        cc = c3.number_input("C (wt%)", 0.0, 1.0, 0.05,
                                              key=f"ic_{cid}_{tab_key}")
                        a = c4.number_input("Absorption (v/v)", 0.0, 100.0, 19.0,
                                             key=f"ia_{cid}_{tab_key}")

                        col_a, col_b = st.columns(2)
                        if col_a.form_submit_button("📥 Add to Training Data"):
                            append_extracted_data(cid, p, t, cc, a)
                            st.success(f"✅ Data point added to training set")

                        if col_b.form_submit_button("✅ Mark as Integrated"):
                            update_status(cid, 'integrated')
                            st.success(f"Contribution #{cid} marked as integrated")
                            st.rerun()

                # Status change buttons
                col_x, col_y, col_z = st.columns(3)
                if col_x.button(f"✅ Accept", key=f"acc_{cid}_{tab_key}"):
                    update_status(cid, 'accepted')
                    st.rerun()
                if col_y.button(f"⏳ Review", key=f"rev_{cid}_{tab_key}"):
                    update_status(cid, 'review')
                    st.rerun()
                if col_z.button(f"❌ Reject", key=f"rej_{cid}_{tab_key}"):
                    update_status(cid, 'rejected')
                    st.rerun()

    with tab1:
        show_contributions(df[df['status'] == 'accepted'], "acc")
    with tab2:
        show_contributions(df[df['status'] == 'review'], "rev")
    with tab3:
        show_contributions(df[df['status'] == 'rejected'], "rej")
    with tab4:
        show_contributions(df, "all")

# ------------------------------------------------------------------
# Model retraining section
# ------------------------------------------------------------------
st.markdown("---")
st.markdown("## 🔄 Model Retraining")

col_a, col_b = st.columns([2, 1])

with col_a:
    st.write(
        "Combine the original 17-point Box-Behnken design with all "
        "integrated contributions and retrain the global model."
    )
    if os.path.exists(EXTRACTED_CSV):
        extra_df = pd.read_csv(EXTRACTED_CSV)
        st.info(f"📦 {len(extra_df)} additional data points ready for training")
    else:
        st.warning("⚠️ No integrated contributions yet")

with col_b:
    if st.button("🔄 Retrain Model", type="primary", use_container_width=True):
        with st.spinner("Training model..."):
            try:
                model = retrain_global_model()
                st.success(
                    f"✅ Model retrained — "
                    f"R² = {model['r2']:.4f}, "
                    f"points = {model['n_points']}"
                )
                st.balloons()
            except Exception as e:
                st.error(f"Training failed: {e}")

# Existing model status
if os.path.exists('models/rsm_model.pkl'):
    with open('models/rsm_model.pkl', 'rb') as f:
        current = pickle.load(f)
    st.caption(
        f"Current model: R² = {current['r2']:.4f}, "
        f"trained on {current.get('n_points', 17)} points"
    )
