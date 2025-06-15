import streamlit as st
from utils import is_admin, get_pending_loans, predict_and_decide, save_decision

if not is_admin():
    st.warning("Admin only")
    st.stop()

st.title("📊 Admin Dashboard")
pending = get_pending_loans()
for idx, row in pending.iterrows():
    st.subheader(f"App #{row['id']}, User #{row['user_id']}")
    st.write(row)
    score, risk = predict_and_decide(row)
    st.write(f"Risk: {score:.2f}% ({risk})")
    decision = st.radio("Decision", ["Approve", "Decline"], key=row['id'])
    note = st.text_input("Note", key=f"note_{row['id']}")
    if st.button("Submit Decision", key=f"btn_{row['id']}"):
        save_decision(row["id"], decision, note)
        st.success("Decision submitted")
