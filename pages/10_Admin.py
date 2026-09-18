"""Complete Admin Dashboard with full control panel."""
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import pickle
from datetime import datetime

st.set_page_config(page_title="Admin — DanCarbon Tech",
                   page_icon="📊", layout="wide")

st.title("📊 Admin Dashboard")
st.caption("Full control panel — contributions, requests, users, model.")

CONTRIB_FILE = "data/contributions.json"
QUOTE_FILE = "data/quote_requests.csv"
EXTRACTED_CSV = "data/extracted_data.csv"


def load_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_csv_safe(path, columns=None):
    if not os.path.exists(path):
        return pd.DataFrame(columns=columns or [])
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=columns or [])


def delete_contribution_by_title(title):
    contribs = load_json(CONTRIB_FILE, [])
    new = [c for c in contribs if c.get('title') != title]
    save_json(CONTRIB_FILE, new)
    return len(contribs) - len(new)


def update_contribution_status(title, new_status):
    contribs = load_json(CONTRIB_FILE, [])
    for c in contribs:
        if c.get('title') == title:
            c['status'] = new_status
    save_json(CONTRIB_FILE, contribs)


def edit_contribution(title, new_title=None, new_description=None,
                       new_score=None, new_status=None):
    contribs = load_json(CONTRIB_FILE, [])
    for c in contribs:
        if c.get('title') == title:
            if new_title:
                c['title'] = new_title
            if new_description:
                c['description'] = new_description
            if new_score is not None:
                c['ai_score'] = new_score
            if new_status:
                c['status'] = new_status
    save_json(CONTRIB_FILE, contribs)


tabs = st.tabs([
    "🏠 Overview",
    "🌍 Contributions",
    "📩 Quote Requests",
    "👥 Users",
    "🤖 Model",
    "📊 Analytics",
    "⚙️ Settings",
])

# ==================================================================
# TAB 1: Overview
# ==================================================================
with tabs[0]:
    st.markdown("## 🏠 Overview")
    contribs = load_json(CONTRIB_FILE, [])
    quotes = load_csv_safe(QUOTE_FILE)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Contributions", len(contribs))
    col2.metric("Accepted",
                sum(1 for c in contribs if c.get('status') == 'accepted'))
    col3.metric("Quote Requests", len(quotes))
    col4.metric("Rejected",
                sum(1 for c in contribs if c.get('status') == 'rejected'))

    st.markdown("---")
    st.markdown("### 📌 Recent Activity")
    all_items = []
    for c in contribs[-10:]:
        all_items.append({
            'time': c.get('timestamp', '—')[:19],
            'type': '🌍 Contribution',
            'detail': c.get('title', '—')[:60],
            'status': c.get('status', '—')
        })
    if not quotes.empty:
        for _, q in quotes.tail(5).iterrows():
            all_items.append({
                'time': str(q.get('timestamp', '—'))[:19],
                'type': '📩 Quote',
                'detail': f"{q.get('name', '—')} ({q.get('company', '—')})",
                'status': 'new'
            })
    if all_items:
        df_activity = pd.DataFrame(all_items)
        st.dataframe(df_activity, use_container_width=True, height=400)
    else:
        st.info("No activity yet.")

# ==================================================================
# TAB 2: Contributions
# ==================================================================
with tabs[1]:
    st.markdown("## 🌍 Contributions Management")
    contribs = load_json(CONTRIB_FILE, [])

    if not contribs:
        st.info("No contributions yet.")
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search = st.text_input("🔍 Search title or description")
        with col2:
            filter_status = st.selectbox(
                "Status", ["All", "accepted", "review", "rejected"])
        with col3:
            sort_by = st.selectbox(
                "Sort", ["Newest first", "Oldest first",
                         "Score high→low", "Score low→high"])

        filtered = contribs.copy()
        if search:
            filtered = [c for c in filtered
                        if search.lower() in c.get('title', '').lower()
                        or search.lower() in c.get('description', '').lower()]
        if filter_status != "All":
            filtered = [c for c in filtered
                        if c.get('status') == filter_status]

        if sort_by == "Newest first":
            filtered = sorted(filtered,
                              key=lambda x: x.get('timestamp', ''),
                              reverse=True)
        elif sort_by == "Oldest first":
            filtered = sorted(filtered,
                              key=lambda x: x.get('timestamp', ''))
        elif sort_by == "Score high→low":
            filtered = sorted(filtered,
                              key=lambda x: x.get('ai_score', 0),
                              reverse=True)
        else:
            filtered = sorted(filtered,
                              key=lambda x: x.get('ai_score', 0))

        st.markdown(f"**{len(filtered)} items found**")
        st.markdown("---")

        for i, c in enumerate(filtered):
            title = c.get('title', 'Untitled')
            score = c.get('ai_score', 0)
            status = c.get('status', 'unknown')
            emoji = {'accepted': '✅', 'review': '⏳',
                     'rejected': '❌'}.get(status, '❓')

            with st.expander(f"{emoji} **{title}** — Score: {score}/100"):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(c.get('description', '—'))
                    st.caption(
                        f"Type: {c.get('contribution_type', '—')} | "
                        f"Source: {c.get('source', '—')} | "
                        f"Email: {c.get('email', '—')} | "
                        f"Time: {c.get('timestamp', '—')[:19]}"
                    )
                with col_b:
                    st.metric("Score", f"{score}")
                    st.write(f"**Status:** {emoji} {status}")

                st.markdown("**Actions:**")
                a1, a2, a3, a4 = st.columns(4)
                if a1.button("✅ Approve", key=f"app_{i}"):
                    update_contribution_status(title, 'accepted')
                    st.success("Approved"); st.rerun()
                if a2.button("❌ Reject", key=f"rej_{i}"):
                    update_contribution_status(title, 'rejected')
                    st.success("Rejected"); st.rerun()
                if a3.button("⏳ Review", key=f"rev_{i}"):
                    update_contribution_status(title, 'review')
                    st.success("Marked review"); st.rerun()
                if a4.button("🗑️ Delete", key=f"del_{i}"):
                    delete_contribution_by_title(title)
                    st.success("Deleted"); st.rerun()

                with st.form(f"edit_{i}"):
                    st.markdown("**Edit:**")
                    new_title = st.text_input("Title", value=title,
                                               key=f"et_{i}")
                    new_desc = st.text_area("Description",
                                             value=c.get('description', ''),
                                             height=100, key=f"ed_{i}")
                    new_score = st.number_input("Score", 0.0, 100.0,
                                                 float(score), key=f"es_{i}")
                    new_status = st.selectbox(
                        "Status", ['accepted', 'review', 'rejected'],
                        index=['accepted', 'review', 'rejected'].index(status)
                        if status in ['accepted', 'review', 'rejected'] else 1,
                        key=f"est_{i}")
                    if st.form_submit_button("💾 Save"):
                        edit_contribution(title, new_title, new_desc,
                                           new_score, new_status)
                        st.success("Saved"); st.rerun()

                st.markdown("**Integrate into model:**")
                with st.form(f"integ_{i}"):
                    c1, c2, c3, c4 = st.columns(4)
                    p = c1.number_input("P (bar)", 0.0, 100.0, 17.7,
                                         key=f"ip_{i}")
                    t = c2.number_input("T (K)", 200.0, 500.0, 297.0,
                                         key=f"it_{i}")
                    cc = c3.number_input("C (wt%)", 0.0, 1.0, 0.05,
                                          key=f"ic_{i}")
                    a = c4.number_input("Abs", 0.0, 100.0, 19.0,
                                         key=f"ia_{i}")
                    if st.form_submit_button("📥 Add to Training Data"):
                        new_row = pd.DataFrame([{
                            'pressure': p, 'temperature': t,
                            'concentration': cc, 'absorption': a,
                            'added_at': datetime.now().isoformat()
                        }])
                        if os.path.exists(EXTRACTED_CSV):
                            existing = pd.read_csv(EXTRACTED_CSV)
                            combined = pd.concat([existing, new_row],
                                                  ignore_index=True)
                        else:
                            combined = new_row
                        os.makedirs('data', exist_ok=True)
                        combined.to_csv(EXTRACTED_CSV, index=False)
                        st.success("✅ Added to training data")

# ==================================================================
# TAB 3: Quote Requests
# ==================================================================
with tabs[2]:
    st.markdown("## 📩 Quote Requests")
    quotes = load_csv_safe(QUOTE_FILE)

    if quotes.empty:
        st.info("No quote requests yet.")
    else:
        st.metric("Total Requests", len(quotes))
        st.download_button(
            "📥 Download CSV",
            quotes.to_csv(index=False),
            file_name=f"quote_requests_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        st.markdown("---")

        for i, q in quotes.iterrows():
            name = q.get('name', 'Unknown')
            company = q.get('company', '')
            with st.expander(f"📩 **{name}** — {company or 'N/A'} "
                             f"({q.get('service', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {name}")
                    st.write(f"**Company:** {company or '—'}")
                    st.write(f"**Email:** {q.get('email', '—')}")
                    st.write(f"**Phone:** {q.get('phone', '—')}")
                with col2:
                    st.write(f"**Country:** {q.get('country', '—')}")
                    st.write(f"**Service:** {q.get('service', '—')}")
                    st.write(f"**Budget:** {q.get('budget', '—')}")
                    st.write(f"**Time:** {str(q.get('timestamp', '—'))[:19]}")
                st.markdown("**Description:**")
                st.info(q.get('description', '—'))
                if st.button("🗑️ Delete", key=f"dq_{i}"):
                    new_quotes = quotes.drop(i)
                    new_quotes.to_csv(QUOTE_FILE, index=False)
                    st.success("Deleted"); st.rerun()

# ==================================================================
# TAB 4: Users
# ==================================================================
with tabs[3]:
    st.markdown("## 👥 Users")
    contribs = load_json(CONTRIB_FILE, [])
    quotes = load_csv_safe(QUOTE_FILE)

    emails = set()
    for c in contribs:
        if c.get('email'):
            emails.add(c['email'])
    if not quotes.empty and 'email' in quotes.columns:
        for e in quotes['email'].dropna():
            emails.add(e)

    st.metric("Total Unique Users", len(emails))
    st.markdown("---")

    if not emails:
        st.info("No users yet.")
    else:
        user_data = []
        for e in emails:
            n_contribs = sum(1 for c in contribs if c.get('email') == e)
            n_quotes = 0
            if not quotes.empty and 'email' in quotes.columns:
                n_quotes = (quotes['email'] == e).sum()
            user_data.append({
                'Email': e,
                'Contributions': n_contribs,
                'Quote Requests': n_quotes,
                'Total': n_contribs + n_quotes
            })
        df_users = pd.DataFrame(user_data).sort_values(
            'Total', ascending=False)
        st.dataframe(df_users, use_container_width=True)

# ==================================================================
# TAB 5: Model
# ==================================================================
with tabs[4]:
    st.markdown("## 🤖 Model Management")
    model_path = 'models/rsm_model.pkl'

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            current = pickle.load(f)
        col1, col2, col3 = st.columns(3)
        col1.metric("Current R²", f"{current.get('r2', 0):.4f}")
        col2.metric("Training Points", current.get('n_points', '—'))
        col3.metric("Status", "✅ Active")
    else:
        st.warning("No model found.")

    st.markdown("---")
    st.markdown("### 🔄 Retrain Model")
    st.write("Combines original Box-Behnken data with integrated contributions.")

    if st.button("🔄 Retrain Now", type="primary"):
        with st.spinner("Training..."):
            try:
                baseline = pd.read_csv('data/box_behnken.csv')
                baseline = baseline.rename(columns={
                    'P_bar': 'pressure', 'T_K': 'temperature',
                    'TiO2_wt': 'concentration', 'X_vv': 'absorption'
                })[['pressure', 'temperature', 'concentration', 'absorption']]

                if os.path.exists(EXTRACTED_CSV):
                    extra = pd.read_csv(EXTRACTED_CSV)[
                        ['pressure', 'temperature', 'concentration', 'absorption']
                    ]
                    combined = pd.concat([baseline, extra], ignore_index=True)
                else:
                    combined = baseline

                def build_X(P, T, C):
                    P = np.asarray(P).ravel().astype(float)
                    T = np.asarray(T).ravel().astype(float)
                    C = np.asarray(C).ravel().astype(float)
                    return np.column_stack([
                        np.ones_like(P), P, T, C,
                        P**2, T**2, C**2, P*T, P*C, T*C
                    ])

                A = build_X(combined['pressure'], combined['temperature'],
                            combined['concentration'])
                y = combined['absorption'].values.astype(float)
                coef, *_ = np.linalg.lstsq(A, y, rcond=None)
                y_pred = A @ coef
                r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)

                model = {'coef': coef, 'r2': float(r2),
                         'n_points': len(combined)}
                os.makedirs('models', exist_ok=True)
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
                st.success(f"✅ Model retrained — R² = {r2:.4f}, "
                           f"points = {len(combined)}")
            except Exception as e:
                st.error(f"Error: {e}")

# ==================================================================
# TAB 6: Analytics
# ==================================================================
with tabs[5]:
    st.markdown("## 📊 Analytics")
    contribs = load_json(CONTRIB_FILE, [])

    if not contribs:
        st.info("No data to analyze yet.")
    else:
        df = pd.DataFrame(contribs)

        if 'status' in df.columns:
            st.markdown("### Status Distribution")
            st.bar_chart(df['status'].value_counts())

        if 'contribution_type' in df.columns:
            st.markdown("### Contribution Types")
            st.bar_chart(df['contribution_type'].value_counts())

        if 'ai_score' in df.columns:
            st.markdown("### Score Distribution")
            scores = df['ai_score'].dropna().astype(float)
            if len(scores) > 0:
                bins = {
                    'Rejected (0-40)': [(scores < 40).sum()],
                    'Review (40-70)': [((scores >= 40) & (scores < 70)).sum()],
                    'Accepted (70-100)': [(scores >= 70).sum()],
                }
                st.bar_chart(bins)

# ==================================================================
# TAB 7: Settings
# ==================================================================
with tabs[6]:
    st.markdown("## ⚙️ Settings")

    st.markdown("### 📁 Data Files")
    if os.path.exists('data'):
        for f in sorted(os.listdir('data')):
            full = os.path.join('data', f)
            if os.path.isfile(full):
                st.write(f"`{f}` — {os.path.getsize(full)} bytes")

    st.markdown("---")
    st.markdown("### 🗑️ Danger Zone")

    if st.button("🗑️ Clear ALL Contributions"):
        if st.checkbox("I confirm — delete all contributions"):
            save_json(CONTRIB_FILE, [])
            st.success("Cleared"); st.rerun()

    if st.button("🗑️ Clear ALL Quote Requests"):
        if st.checkbox("I confirm — delete all quote requests"):
            if os.path.exists(QUOTE_FILE):
                os.remove(QUOTE_FILE)
            st.success("Cleared"); st.rerun()
