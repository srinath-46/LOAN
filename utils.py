
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import joblib

# Load your model and connect to database
engine = create_engine('sqlite:///bank_app.db')
model = joblib.load("xgb_model.pkl")

# ----------------------------
# Session & Role Helpers
# ----------------------------

def get_user_info():
    """Returns currently logged in user from session."""
    return st.session_state.get("user")

def is_admin():
    user = get_user_info()
    return user and user.get("role") == "admin"

# ----------------------------
# User Application Logic
# ----------------------------

def submit_loan_application(user_id, income, amount, term):
    """Insert loan application submitted by user."""
    with engine.begin() as conn:
        conn.execute(text('''
            INSERT INTO loan_applications (user_id, income, loan_amount, term, status)
            VALUES (:uid, :inc, :amt, :term, 'pending')
        '''), {"uid": user_id, "inc": income, "amt": amount, "term": term})

def get_user_loans(user_id):
    """Get past applications for the logged-in user."""
    with engine.begin() as conn:
        result = conn.execute(text('''
            SELECT * FROM loan_applications WHERE user_id = :uid ORDER BY id DESC
        '''), {"uid": user_id})
        return pd.DataFrame(result.fetchall(), columns=result.keys())
