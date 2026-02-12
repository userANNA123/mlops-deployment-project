import os
import sys
from pathlib import Path
import pandas as pd

# On ajoute le dossier RACINE du projet au PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.app.ml_model import model, make_features, predict_from_dict, X_COLUMNS



VALID_DATA = {
    "age": 30,
    "annee_experience_totale": 5,
    "revenu_mensuel": 3000.0,
    "distance_domicile_travail": 10.0,
    "nb_formations_suivies": 2,
    "nombre_heures_travaillees": 160.0,
    "frequence_deplacement": "Rarement",
}


def test_model_has_predict():
    assert hasattr(model, "predict")


def test_make_features_creates_all_x_columns():
    df = pd.DataFrame([VALID_DATA])
    df_feat = make_features(df)

    for col in X_COLUMNS:
        assert col in df_feat.columns


def test_predict_from_dict_returns_0_or_1():
    y = predict_from_dict(VALID_DATA)
    assert isinstance(y, int)
    assert y in [0, 1]


