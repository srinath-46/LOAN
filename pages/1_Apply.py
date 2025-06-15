import streamlit as st
from utils import submit_loan_application, get_user_info

user = get_user_info()
if not user:
    st.warning("Login required")
    st.stop()

st.title("📝 Apply for a Loan")
with st.form("loan_form"):
    income = st.number_input("Your Income", step=1000)
    amount = st.number_input("Loan Amount", step=1000)
    term = st.selectbox("Term (Months)", [12, 24, 36, 60])
    submitted = st.form_submit_button("Apply")

if submitted:
    submit_loan_application(user["id"], income, amount, term)
    st.success("✅ Loan Application Submitted")
