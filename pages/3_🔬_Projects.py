"""Multi-project management with AutoML."""
import streamlit as st
import pandas as pd
import sys
sys.path.append('.')
from utils.db import (
    create_project, list_projects, get_project,
    add_data_point, get_project_data, update_project_status
)
from utils.automl import train_project_model

st.set_page_config(page_title="Projects — DanCarbon Tech", page_icon="🔬")

st.title("🔬 Multi-Project Workspace")
st.markdown(
    "Create projects for any gas, solvent, or nanoparticle combination. "
    "The platform trains a model automatically when enough data is collected."
)

# Sidebar: Create new project
with st.sidebar:
    st.header("Create New Project")
    with st.form("new_project"):
        name = st.text_input("Project name", placeholder="e.g., CO₂ / MEG / Al₂O₃")
        gas = st.selectbox("Gas", ["CO₂", "CH₄", "H₂S", "H₂", "N₂", "Other"])
        solvent = st.selectbox("Solvent",
                               ["MEG", "Amine (MEA)", "Amine (MDEA)",
                                "Water", "Methanol", "Other"])
        nanoparticle = st.selectbox("Nanoparticle",
                                     ["TiO₂", "GO", "Al₂O₃", "SiO₂", "None", "Other"])
        email = st.text_input("Owner email (optional)")
        submitted = st.form_submit_button("Create Project", type="primary")

        if submitted:
            if name:
                pid = create_project(name, gas, solvent, nanoparticle, email or None)
                st.success(f"✅ Project created (ID: {pid})")
                st.rerun()
            else:
                st.error("Please enter a project name")

# List projects
st.markdown("### Your Projects")
projects = list_projects()

if projects.empty:
    st.info("No projects yet. Create one from the sidebar.")
else:
    for _, proj in projects.iterrows():
        with st.expander(
            f"**{proj['project_name']}** — {proj['gas']} / "
            f"{proj['solvent']} / {proj['nanoparticle']} "
            f"({proj['status']})"
        ):
            pid = int(proj['project_id'])
            data = get_project_data(pid)
            n_points = len(data)

            col1, col2, col3 = st.columns(3)
            col1.metric("Data points", n_points)
            col2.metric("Min. required", proj['min_points'])
            col3.metric("Model R²",
                        f"{proj['model_r2']:.3f}" if pd.notna(proj['model_r2']) else "—")

            # Add data point
            st.markdown("**Add a new data point**")
            with st.form(f"add_point_{pid}"):
                c1, c2, c3, c4 = st.columns(4)
                p = c1.number_input("P (bar)", 0.0, 100.0, 17.7, key=f"p_{pid}")
                t = c2.number_input("T (K)", 200.0, 500.0, 297.0, key=f"t_{pid}")
                cc = c3.number_input("C (wt%)", 0.0, 1.0, 0.05, key=f"c_{pid}")
                a = c4.number_input("Absorption (v/v)", 0.0, 100.0, 19.0, key=f"a_{pid}")

                if st.form_submit_button("Add Point"):
                    add_data_point(pid, p, t, cc, a)
                    st.success("✅ Data point added")
                    st.rerun()

            # Show data
            if n_points > 0:
                st.dataframe(data[['pressure', 'temperature', 'concentration',
                                   'absorption', 'created_at']],
                             use_container_width=True)

            # Train model button
            if n_points >= proj['min_points']:
                if st.button(f"🤖 Train Model (Project {pid})", key=f"train_{pid}"):
                    result = train_project_model(pid, data)
                    if result['success']:
                        update_project_status(pid, 'active', result['r2'])
                        st.success(
                            f"✅ Model trained — R² = {result['r2']:.3f}, "
                            f"RMSE = {result['rmse']:.3f}"
                        )
                        st.rerun()
                    else:
                        st.error(result['error'])
            else:
                remaining = proj['min_points'] - n_points
                st.warning(
                    f"⏳ Need {remaining} more data points "
                    f"to enable AutoML training"
                )
