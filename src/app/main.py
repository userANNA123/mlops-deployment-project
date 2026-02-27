import time
import uuid
import json
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from loguru import logger

from .schemas import PredictionRequest, PredictionResponse
from .ml_model import predict_from_dict
from .db import SessionLocal
from .models import ModelInput, ModelOutput
from .storage import save_prediction_to_csv

from .monitoring_db import init_db, SessionLocalMonitoring, APILog
from .monitoring_db import DB_PATH
print(" Monitoring DB path used by API:", DB_PATH)

app = FastAPI(
    title="Churn Prediction API",
    description="API pour exposer le modèle RandomForest du projet 4",
    version="1.0.0",
)

MODEL_VERSION = "1.0.0"
init_db()

# Dependency pour la session DB (ton DB existante)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Middleware monitoring (SQLite monitoring.db)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    # Lire le body (si JSON)
    body = None
    if request.method in {"POST", "PUT", "PATCH"}:
        try:
            body = await request.json()
        except Exception:
            body = None

    status_code = 500
    error_type = None
    error_message = None
    response = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)[:500]
        raise
    finally:
        latency_ms = int((time.perf_counter() - start) * 1000)

        dbm = SessionLocalMonitoring()
        try:
            log_entry = APILog(
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=status_code,
                latency_ms=latency_ms,
                model_version=MODEL_VERSION,
                input_json=body,
                output_json=None,  # on le mettra dans /predict
                error_type=error_type,
                error_message=error_message,
            )
            dbm.add(log_entry)
            dbm.commit()
        except Exception as e:
            logger.warning(f"Monitoring DB write failed: {e}")
        finally:
            dbm.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(payload: PredictionRequest, db: Session = Depends(get_db)):
    data = payload.model_dump()
    result = predict_from_dict(data)

    # (A)  stockage actuel (ModelInput/ModelOutput) + fallback CSV
    try:
        input_row = ModelInput(payload=json.dumps(data, ensure_ascii=False))
        db.add(input_row)
        db.commit()
        db.refresh(input_row)

        output_row = ModelOutput(input_id=input_row.id, prediction=result)
        db.add(output_row)
        db.commit()

    except Exception as e:
        db.rollback()
        logger.warning(f"DB unavailable, fallback to CSV. Error: {e}")
        try:
            save_prediction_to_csv(data, result)
        except Exception as e2:
            logger.warning(f"CSV fallback failed: {e2}")

    # (B) mise à jour du dernier log monitoring pour ajouter output_json
    # PoC simple: on met à jour le plus récent /predict
    dbm = SessionLocalMonitoring()
    try:
        last = (
            dbm.query(APILog)
            .filter(APILog.endpoint == "/predict")
            .order_by(APILog.id.desc())
            .first()
        )
        if last:
            last.output_json = {"prediction": result}
            dbm.commit()
    except Exception as e:
        logger.warning(f"Monitoring output update failed: {e}")
    finally:
        dbm.close()

    return PredictionResponse(prediction=result)
