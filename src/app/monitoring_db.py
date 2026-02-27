from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# Racine projet: .../Projet 8
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "monitoring.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocalMonitoring = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseMonitoring = declarative_base()

class APILog(BaseMonitoring):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    request_id = Column(String, index=True)
    endpoint = Column(String)
    method = Column(String)

    status_code = Column(Integer)
    latency_ms = Column(Integer)

    model_version = Column(String)

    input_json = Column(Text, nullable=True)
    output_json = Column(Text, nullable=True)

    error_type = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

def init_db():
    BaseMonitoring.metadata.create_all(bind=engine)
