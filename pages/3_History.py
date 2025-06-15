import streamlit as st
from utils import get_user_info, get_user_loans

user = get_user_info()
if not user:
    st.warning("Login required")
    st.stop()

st.title("📁 My Loan Applications")
loans = get_user_loans(user["id"])
st.dataframe(loans)
