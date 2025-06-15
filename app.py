import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator setup
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    expiry_days=config['cookie']['expiry_days']
)

# Show login form
auth_status = authenticator.login()

# ✅ If login is successful, show the app
if auth_status:
    st.sidebar.success(f"Welcome, {authenticator.name}")
    authenticator.logout("Logout", "sidebar")

    # Store role in session
    if authenticator.username == "alice":
        st.session_state["user"] = {"username": "alice", "role": "admin", "id": 1}
    else:
        st.session_state["user"] = {"username": "bob", "role": "user", "id": 2}

    # 🎯 MAIN APP CONTENT
    st.title("🏦 StreamBank – Loan Risk App")
    st.markdown("✅ You are now logged in.")
    st.markdown("### 🧭 Use the sidebar to:")
    st.markdown("- 📝 Apply for a loan")
    st.markdown("- 📊 Admin dashboard (if you're admin)")
    st.markdown("- 📁 View your application history")

# ❌ Wrong password
elif auth_status is False:
    st.error("❌ Invalid username or password")

# ⏳ Login form not yet submitted
elif auth_status is None:
    st.warning("Please enter your login credentials")
