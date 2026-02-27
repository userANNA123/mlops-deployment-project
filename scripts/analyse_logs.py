import os
import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.getcwd(), "monitoring.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

print("📌 DB_PATH =", DB_PATH)

with engine.connect() as conn:
    tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
print("📌 Tables =", tables)

df = pd.read_sql("SELECT * FROM api_logs", engine)
print("📌 Rows =", len(df))
print(df.tail(5))
