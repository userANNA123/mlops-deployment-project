from pathlib import Path
import joblib
import pandas as pd
import numpy as np

# Mapping texte → numérique pour frequence_deplacement
FREQ_NUM_MAP = {"Jamais": 0, "Rarement": 1, "Souvent": 2}

# chemin vers le modèle entraîné
MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.joblib"

# =========================
# 1) Chargement du modèle AU NIVEAU GLOBAL
# =========================
#  Le modèle est chargé UNE SEULE FOIS quand le module est importé
model = joblib.load(MODEL_PATH)


# =========================
# 2) Feature engineering
# =========================
def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()

    # 1) experience_to_age
    df2["experience_to_age"] = (
        df2["annee_experience_totale"] / df2["age"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan)

    # 2) salary_category
    try:
        df2["salary_category"] = pd.qcut(
            df2["revenu_mensuel"],
            q=4,
            labels=["low", "medium", "high", "very_high"],
        )
    except Exception:
        df2["salary_category"] = pd.cut(
            df2["revenu_mensuel"],
            bins=4,
            labels=["low", "medium", "high", "very_high"],
            include_lowest=True,
        )

    # 3) long_commute
    med_dist = df2["distance_domicile_travail"].median()
    df2["long_commute"] = (df2["distance_domicile_travail"] > med_dist).astype(int)

    # 4) training_hours_per_year
    df2["training_hours_per_year"] = df2["nb_formations_suivies"].fillna(0) * 8

    # 5) work_life_balance
    freq = df2["frequence_deplacement"].map(FREQ_NUM_MAP).fillna(0)
    df2["work_life_balance"] = df2["nombre_heures_travaillees"] / (freq + 1)

    # 6) One-hot encoding de frequence_deplacement
    df2 = pd.get_dummies(df2, columns=["frequence_deplacement"], drop_first=False)

    return df2


# pour les tests unitaires de make_features
X_COLUMNS = [
    "age",
    "annee_experience_totale",
    "revenu_mensuel",
    "distance_domicile_travail",
    "nb_formations_suivies",
    "nombre_heures_travaillees",
    "experience_to_age",
    "salary_category",
    "long_commute",
    "training_hours_per_year",
    "work_life_balance",
]


# =========================
# 3) Prédiction à partir d'un dict
# =========================
def predict_from_dict(data: dict) -> int:
    """
    data vient de PredictionRequest.model_dump()
    """

    # On ne recharge plus le modèle ici
    # On n'appelle plus load_model()
    # On utilise le modèle global : model

    # dict → DataFrame
    df = pd.DataFrame([data])

    # features manuelles
    df_feat = make_features(df)

    # alignement sur les colonnes vues par le modèle
    if hasattr(model, "feature_names_in_"):
        X = df_feat.reindex(columns=model.feature_names_in_)
    else:
        X = df_feat

    # remplacer NaN
    X = X.fillna(0)

    y_pred = model.predict(X)
    return int(y_pred[0])