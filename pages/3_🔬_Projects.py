"""Multi-project workspace — pure Python, no sklearn, no SQLite."""
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import pickle
from datetime import datetime

st.set_page_config(page_title="Projects — DanCarbon Tech", page_icon="🔬")

st.title("🔬 Multi-Project Workspace")
st.markdown(
    "Create projects for any gas, solvent, or nanoparticle combination. "
    "The platform trains a model automatically when enough data is collected."
)

PROJECTS_INDEX = 'data/projects_index.json'
PROJECTS_DIR = 'data/projects'
os.makedirs(PROJECTS_DIR, exist_ok=True)
MIN_POINTS = 15


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
    A = build_design_matrix(df['pressure'], df['temperature'], df['concentration'])
    y = df['absorption'].values.astype(float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    y_pred = A @ coef
    r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)
    return {'coef': coef, 'r2': float(r2)}


def load_projects():
    if not os.path.exists(PROJECTS_INDEX):
        return []
    with open(PROJECTS_INDEX, 'r') as f:
        return json.load(f)


def save_projects(projects):
    with open(PROJECTS_INDEX, 'w') as f:
        json.dump(projects, f, indent=2)


def create_project(name, gas, solvent, nanoparticle, email=None):
    projects = load_projects()
    pid = len(projects) + 1
    project = {
        'id': pid,
        'name': name,
        'gas': gas,
        'solvent': solvent,
        'nanoparticle': nanoparticle,
        'email': email or '',
        'status': 'collecting',
        'model_r2': None,
        'created_at': datetime.now().isoformat()
    }
    projects.append(project)
    save_projects(projects)
    return pid


def get_project_data_path(pid):
    return os.path.join(PROJECTS_DIR, f'project_{pid}.csv')


def load_project_data(pid):
    path = get_project_data_path(pid)
    if not os.path.exists(path):
        return pd.DataFrame(columns=['pressure', 'temperature', 'concentration', 'absorption'])
    return pd.read_csv(path)


def save_project_data(pid, df):
    df.to_csv(get_project_data_path(pid), index=False)


def get_project_model_path(pid):
    return os.path.join(PROJECTS_DIR, f'project_{pid}_model.pkl')


def model_exists(pid):
    return os.path.exists(get_project_model_path(pid))


with st.sidebar:
    st.header("Create New Project")
    with st.form("new_project"):
        name = st.text_input("Project name", placeholder="e.g., CO₂ / MEG / Al₂O₃")
        gas = st.selectbox("Gas", ["CO₂", "CH₄", "H₂S", "H₂", "N₂", "Other"])
        solvent = st.selectbox(
            "Solvent",
            ["MEG", "Amine (MEA)", "Amine (MDEA)", "Water", "Methanol", "Other"]
        )
        nanoparticle = st.selectbox(
            "Nanoparticle",
            ["TiO₂", "GO", "Al₂O₃", "SiO₂", "None", "Other"]
        )
        email = st.text_input("Owner email (optional)")
        submitted = st.form_submit_button("Create Project", type="primary")

        if submitted:
            if name:
                pid = create_project(name, gas, solvent, nanoparticle, email or None)
                st.success(f"✅ Project created (ID: {pid})")
                st.rerun()
            else:
                st.error("Please enter a project name")


st.markdown("### Your Projects")
projects = load_projects()

if not projects:
    st.info("No projects yet. Create one from the sidebar.")
else:
    for proj in projects:
        pid = proj['id']
        df = load_project_data(pid)
        n_points = len(df)
        has_model = model_exists(pid)
        status_emoji = "🟢" if has_model else "🟡"
        status_text = "active" if has_model else "collecting"

        with st.expander(
            f"{status_emoji} **{proj['name']}** — {proj['gas']} / "
            f"{proj['solvent']} / {proj['nanoparticle']} ({status_text})"
        ):
            col1, col2, col3 = st.columns(3)
            col1.metric("Data points", n_points)
            col2.metric("Min. required", MIN_POINTS)
            col3.metric(
                "Model R²",
                f"{proj['model_r2']:.3f}" if proj['model_r2'] else "—"
            )

            st.markdown("**Add a new data point**")
            with st.form(f"add_point_{pid}"):
                c1, c2, c3, c4 = st.columns(4)
                p = c1.number_input("P (bar)", 0.0, 100.0, 17.7, key=f"p_{pid}")
                t = c2.number_input("T (K)", 200.0, 500.0, 297.0, key=f"t_{pid}")
                cc = c3.number_input("C (wt%)", 0.0, 1.0, 0.05, key=f"c_{pid}")
                a = c4.number_input("Absorption (v/v)", 0.0, 100.0, 19.0, key=f"a_{pid}")

                if st.form_submit_button("Add Point"):
                    new_row = pd.DataFrame([{
                        'pressure': p,
                        'temperature': t,
                        'concentration': cc,
                        'absorption': a
                    }])
                    df_new = pd.concat([df, new_row], ignore_index=True)
                    save_project_data(pid, df_new)
                    st.success("✅ Data point added")
                    st.rerun()

            if n_points > 0:
                st.markdown("**Current data**")
                st.dataframe(df, use_container_width=True, height=200)

            if n_points >= MIN_POINTS:
                if st.button(f"🤖 Train Model", key=f"train_{pid}", type="primary"):
                    try:
                        model = train_rsm(df)
                        with open(get_project_model_path(pid), 'wb') as f:
                            pickle.dump(model, f)

                        for p in projects:
                            if p['id'] == pid:
                                p['status'] = 'active'
                                p['model_r2'] = model['r2']
                        save_projects(projects)

                        st.success(f"✅ Model trained — R² = {model['r2']:.3f}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Training failed: {e}")
            else:
                remaining = MIN_POINTS - n_points
                st.warning(
                    f"⏳ Need {remaining} more data point"
                    f"{'s' if remaining > 1 else ''} to enable model training"
                )

            with st.form(f"delete_{pid}"):
                if st.form_submit_button("🗑️ Delete Project"):
                    projects = [p for p in projects if p['id'] != pid]
                    save_projects(projects)
                    data_path = get_project_data_path(pid)
                    model_path = get_project_model_path(pid)
                    if os.path.exists(data_path):
                        os.remove(data_path)
                    if os.path.exists(model_path):
                        os.remove(model_path)
                    st.success("Project deleted")
                    st.rerun()
