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
model = joblib.load(MODEL_PATH)


def salary_category_from_value(value):
    """
    Version plus légère que qcut/pd.cut pour une seule ligne.
    Adapte les seuils selon ton projet / ton entraînement.
    """
    if pd.isna(value):
        return "low"

    if value < 3000:
        return "low"
    elif value < 5000:
        return "medium"
    elif value < 8000:
        return "high"
    else:
        return "very_high"


# =========================
# 2) Feature engineering
# =========================
def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()

    # 1) experience_to_age
    age = df2["age"].replace(0, np.nan)
    df2["experience_to_age"] = (
        df2["annee_experience_totale"] / age
    ).replace([np.inf, -np.inf], np.nan)

    # 2) salary_category
    df2["salary_category"] = df2["revenu_mensuel"].apply(salary_category_from_value)

    # 3) long_commute
    # بما أن التنبؤ غالبًا على صف واحد، median هنا = نفس القيمة
    # إذا كنتِ تريدين منطقًا أفضل، استعملي seuil ثابت من التدريب
    df2["long_commute"] = (df2["distance_domicile_travail"] > 15).astype(int)

    # 4) training_hours_per_year
    df2["training_hours_per_year"] = df2["nb_formations_suivies"].fillna(0) * 8

    # 5) work_life_balance
    freq = df2["frequence_deplacement"].map(FREQ_NUM_MAP).fillna(0)
    df2["work_life_balance"] = df2["nombre_heures_travaillees"] / (freq + 1)

    # 6) One-hot encoding manuel au lieu de get_dummies
    df2["frequence_deplacement_Jamais"] = (df2["frequence_deplacement"] == "Jamais").astype(int)
    df2["frequence_deplacement_Rarement"] = (df2["frequence_deplacement"] == "Rarement").astype(int)
    df2["frequence_deplacement_Souvent"] = (df2["frequence_deplacement"] == "Souvent").astype(int)

    # Optionnel: supprimer la colonne texte d'origine
    df2 = df2.drop(columns=["frequence_deplacement"], errors="ignore")

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
    df = pd.DataFrame([data])

    df_feat = make_features(df)

    if hasattr(model, "feature_names_in_"):
        X = df_feat.reindex(columns=model.feature_names_in_, fill_value=0)
    else:
        X = df_feat

    X = X.fillna(0)

    y_pred = model.predict(X)
    return int(y_pred[0])