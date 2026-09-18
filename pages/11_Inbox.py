"""
Private Inbox — only accessible with password.
Shows all submitted contributions and quote requests.
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Inbox — DanCarbon", page_icon="🔒", layout="centered")

st.title("🔒 Private Inbox")

# ------------------------------------------------------------------
# Password protection
# ------------------------------------------------------------------
def check_password():
    """Simple password check using secrets."""
    try:
        expected = st.secrets.get("inbox", {}).get("password", "dancarbon2026")
    except Exception:
        expected = "dancarbon2026"

    if "inbox_authed" not in st.session_state:
        st.session_state.inbox_authed = False

    if not st.session_state.inbox_authed:
        st.markdown("### Enter password to access the inbox")
        pwd = st.text_input("Password", type="password", key="inbox_pwd")
        if st.button("Login", type="primary"):
            if pwd == expected:
                st.session_state.inbox_authed = True
                st.rerun()
            else:
                st.error("❌ Wrong password")
        return False
    return True


if not check_password():
    st.stop()

st.success("✅ Logged in")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
DATA_DIR = 'data'

def load_csv(path, columns=None):
    if not os.path.exists(path):
        return pd.DataFrame(columns=columns or [])
    return pd.read_csv(path)


# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📩 Quote Requests", "🌍 Contributions", "⚙️ Settings"])

with tab1:
    st.markdown("### 📩 All Quote Requests")
    quotes = load_csv(
        f'{DATA_DIR}/quote_requests.csv',
        columns=['timestamp', 'name', 'company', 'email', 'phone',
                 'country', 'service', 'description', 'budget']
    )
    if quotes.empty:
        st.info("No quote requests yet.")
    else:
        st.metric("Total Requests", len(quotes))
        st.dataframe(quotes.sort_values('timestamp', ascending=False),
                     use_container_width=True, height=500)

        # Download button
        st.download_button(
            "📥 Download CSV",
            quotes.to_csv(index=False),
            file_name=f"quote_requests_{datetime.now().strftime('%Y%m%d')}.csv"
        )

        # Show emails of requesters
        st.markdown("### 📧 Email addresses")
        emails = quotes['email'].dropna().unique()
        st.code("\n".join(emails))

with tab2:
    st.markdown("### 🌍 All Contributions")
    # Try JSON first
    contribs_path = f'{DATA_DIR}/contributions.json'
    if os.path.exists(contribs_path):
        import json
        with open(contribs_path, 'r') as f:
            contribs_data = json.load(f)
        contribs = pd.DataFrame(contribs_data)
        if not contribs.empty:
            st.metric("Total Contributions", len(contribs))
            st.dataframe(contribs, use_container_width=True, height=500)
            st.download_button(
                "📥 Download JSON",
                contribs.to_json(indent=2),
                file_name=f"contributions_{datetime.now().strftime('%Y%m%d')}.json"
            )
        else:
            st.info("No contributions yet.")
    else:
        st.info("No contributions data yet.")

with tab3:
    st.markdown("### ⚙️ Settings")
    st.write("**Data folder:**", os.path.abspath(DATA_DIR))
    st.write("**Files present:**")
    for f in os.listdir(DATA_DIR):
        full = os.path.join(DATA_DIR, f)
        size = os.path.getsize(full) if os.path.isfile(full) else 0
        st.write(f"- `{f}` — {size} bytes")

    if st.button("🚪 Logout"):
        st.session_state.inbox_authed = False
        st.rerun()
