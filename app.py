import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Load credentials from config.yaml ---
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- Initialize the authenticator ---
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    expiry_days=config['cookie']['expiry_days']
)

# --- Display login form ---
auth_status = authenticator.login()

# --- Evaluate authentication result ---
if auth_status:
    st.sidebar.success(f"Welcome, {authenticator.name}")
    authenticator.logout("Logout", "sidebar")

    # Role-based session assignment
    if authenticator.username == "alice":
        st.session_state["user"] = {"username": "alice", "role": "admin", "id": 1}
    else:
        st.session_state["user"] = {"username": "bob", "role": "user", "id": 2}

    # --- Main UI after login ---
    st.title("🏦 StreamBank – Loan Risk App")
    st.markdown("✅ You are now logged in.")
    st.markdown("### 🔍 Use the sidebar to:")
    st.markdown("- 📝 Apply for a loan")
    st.markdown("- 📊 Admin dashboard (if you're an admin)")
    st.markdown("- 📁 View your loan application history")

elif auth_status is False:
    st.error("❌ Invalid username or password")

elif auth_status is None:
    st.warning("Please enter your username and password.")
