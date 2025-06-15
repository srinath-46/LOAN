import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import joblib

# Connect to SQLite database
engine = create_engine("sqlite:///bank_app.db")

# Load trained model
model = joblib.load("xgb_model.pkl")

# -----------------------
# Session & Role Helpers
# -----------------------

def get_user_info():
    """Returns currently logged-in user from session."""
    return st.session_state.get("user")

def is_admin():
    """Checks if the current user is an admin."""
    user = get_user_info()
    return user and user.get("role") == "admin"

# -----------------------
# Loan Application Logic
# -----------------------

def submit_loan_application(user_id, income, amount, term):
    """Insert a new loan application submitted by the user."""
    with engine.begin() as conn:
        conn.execute(text('''
            INSERT INTO loan_applications (user_id, income, loan_amount, term, status)
            VALUES (:uid, :inc, :amt, :term, 'pending')
        '''), {"uid": user_id, "inc": income, "amt": amount, "term": term})

def get_user_loans(user_id):
    """Get all loan applications by a specific user."""
    return pd.read_sql(f"SELECT * FROM loan_applications WHERE user_id = {user_id}", engine)

# -----------------------
# Admin Decision Logic
# -----------------------

def get_pending_loans():
    """Get all loan applications that are pending review."""
    return pd.read_sql("SELECT * FROM loan_applications WHERE status = 'pending'", engine)

def save_decision(app_id, decision, note):
    """Save admin decision to the loan application."""
    with engine.begin() as conn:
        conn.execute(text('''
            UPDATE loan_applications
            SET status = :status, decision_note = :note
            WHERE id = :id
        '''), {"status": decision.lower(), "note": note, "id": app_id})

# -----------------------
# Model Prediction Logic
# -----------------------

def predict_and_decide(row):
    """Predict default risk and return risk score & category."""
    # Placeholder feature set — match to your model training
    features = pd.DataFrame([{
        "age": 35,
        "annual_income": row["income"],
        "credit_score": 700,
        "num_inquiries": 2,
        "open_credit_lines": 3,
        "total_accounts": 5,
        "delinquent_accounts": 0,
        "debt_to_income": row["loan_amount"] / row["income"],
        "credit_utilization": 0.3,
        "payment_ratio": 0.9,
        "loan_age_months": 12,
        "gender_encoded": 1,
        "marital_status_encoded": 0
    }])

    # Predict
    score = model.predict_proba(features)[0][1] * 100
    category = "High" if score >= 70 else "Medium" if score >= 40 else "Low"
    return round(score, 2), category
