
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Load config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Setup authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    expiry_days=config['cookie']['expiry_days']
)

# Show login form
auth_status = authenticator.login()

# Handle login outcomes
if auth_status:
    st.sidebar.success(f"Welcome {authenticator.name}")
    authenticator.logout("Logout", "sidebar")

    # Assign user role to session
    if authenticator.username == "alice":
        st.session_state["user"] = {
            "username": "alice",
            "role": "admin",
            "id": 1
        }
    else:
        st.session_state["user"] = {
            "username": "bob",
            "role": "user",
            "id": 2
        }

    # Main app interface
    st.title("🏦 StreamBank – Loan Risk Predictor")
    st.write("✅ You are now logged in.")
    st.markdown("### 📌 Use the sidebar to access:")
    st.markdown("- 📝 Apply for a loan")
    st.markdown("- 📁 View application history")
    st.markdown("- 📊 Admin review panel (if admin)")

elif auth_status is False:
    st.error("❌ Invalid username or password")

elif auth_status is None:
    st.warning("Please enter your login credentials")
