import os
from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.getcwd(), "monitoring.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

with engine.connect() as conn:
    tables = conn.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )).fetchall()

print("Tables trouvées :", tables)
