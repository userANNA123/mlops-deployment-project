from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import json

from .schemas import PredictionRequest, PredictionResponse
from .ml_model import predict_from_dict
from .db import SessionLocal
from .models import ModelInput, ModelOutput  
from loguru import logger
from .storage import save_prediction_to_csv

app = FastAPI(
    title="Churn Prediction API",
    description="API pour exposer le modèle RandomForest du projet 4",
    version="1.0.0",
)


# Dependency pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(
    payload: PredictionRequest,
    db: Session = Depends(get_db),
):
    # 1) convertir le payload Pydantic en dict
    data = payload.model_dump()

    # 2) appeler le modèle (✅ لا نعتمد على DB)
    result = predict_from_dict(data)

    # 3) محاولة تخزين في DB (اختياري)
    try:
        input_row = ModelInput(payload=json.dumps(data, ensure_ascii=False))
        db.add(input_row)
        db.commit()
        db.refresh(input_row)

        output_row = ModelOutput(
            input_id=input_row.id,
            prediction=result,
        )
        db.add(output_row)
        db.commit()

    except Exception as e:
        # ✅ لا نكسر الـ API
        db.rollback()
        logger.warning(f"DB unavailable, fallback to CSV. Error: {e}")

        # 4) fallback CSV (ممتاز للمشروع 8 + screenshots)
        try:
            save_prediction_to_csv(data, result)
        except Exception as e2:
            logger.warning(f"CSV fallback failed: {e2}")

    # 5) retourner la réponse API
    return PredictionResponse(prediction=result)



