
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///bank_app.db")

pd.read_csv("customer_profile_large.csv").to_sql("customers", engine, if_exists="replace", index=False)
pd.read_csv("loan_history_large.csv").to_sql("loans", engine, if_exists="replace", index=False)
pd.read_csv("repayment_records_cleaned.csv").to_sql("repayments", engine, if_exists="replace", index=False)
pd.read_csv("credit_score_large.csv").to_sql("credit_scores", engine, if_exists="replace", index=False)
pd.read_csv("economic_indicators_large.csv").to_sql("economic_data", engine, if_exists="replace", index=False)

print("✅ CSVs loaded into bank_app.db")
