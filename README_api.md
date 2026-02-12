<!-- PROJECT SHIELDS -->
![Contributors](https://img.shields.io/github/contributors/userANNA123/deploy-ml-model?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/userANNA123/deploy-ml-model?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/userANNA123/deploy-ml-model?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/userANNA123/deploy-ml-model?style=for-the-badge)
![MIT License](https://img.shields.io/github/license/userANNA123/deploy-ml-model?style=for-the-badge)
![CI/CD](https://img.shields.io/github/actions/workflow/status/userANNA123/deploy-ml-model/ci-cd.yml?label=CI%2FCD&style=for-the-badge)

<br/>

<!-- PROJECT LOGO -->
<p align="center">
  <img src="https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/images/logo.png" alt="Logo" width="120">
</p>

<h3 align="center">Déploiement d’un Modèle de Machine Learning avec FastAPI & CI/CD 🚀</h3>

<p align="center">
  Un pipeline complet pour tester, valider et déployer automatiquement un modèle de Machine Learning.
</p>

---

## 🧭 Table des matières
- [📌 Présentation du projet](#-présentation-du-projet)
- [🎯 Objectifs](#-objectifs)
- [🏗 Architecture du projet](#-architecture-du-projet)
- [⚙️ Installation](#️-installation)
- [▶️ Lancer l’API](#️-lancer-lapi)
- [🔮 Endpoint `/predict`](#-endpoint-predict)
- [🗄️ Base de données PostgreSQL](#️-base-de-données-postgresql)
- [🧪 Tests](#-tests)
- [🧰 Technologies utilisées](#-technologies-utilisées)
- [👩‍💻 Auteure](#-auteure)

---

## 📌 Présentation du projet
Ce projet déploie un modèle de Machine Learning (**Random Forest**) via une API REST **FastAPI**.
L’API prédit le **churn (attrition)** à partir de caractéristiques professionnelles.

Le projet inclut :
- API FastAPI + documentation Swagger
- Validation des entrées/sorties avec **Pydantic**
- Modèle ML sérialisé (joblib)
- Traçabilité (optionnel) avec **PostgreSQL**
- Tests unitaires & fonctionnels (**Pytest**)
- Workflow **CI/CD GitHub Actions**

---

## 🎯 Objectifs
- Mettre en place un pipeline CI/CD complet
- Automatiser les tests
- Exposer le modèle via une API documentée
- Faciliter le déploiement (ex. Hugging Face Spaces)

---

## 🏗 Architecture du projet
```text
project/
│── src/
│   └── app/
│       ├── main.py
│       ├── schemas.py
│       ├── services.py
│       ├── database.py
│       └── models.py
│── model/
│   └── churn_model.joblib
│── tests/
│   ├── test_api.py
│   └── test_model.py
│── requirements.txt
│── .env.example
│── README.md

⚙️ Installation
git clone https://github.com/userANNA123/deploy-ml-model.git
cd deploy-ml-model

python -m venv .venv
source .venv/bin/activate    # Linux / Mac
.\.venv\Scripts\activate     # Windows

pip install -r requirements.txt
▶️ Lancer l’API
uvicorn src.app.main:app --reload


API : http://127.0.0.1:8000

Swagger : http://127.0.0.1:8000/docs

Redoc : http://127.0.0.1:8000/redoc

POST http://127.0.0.1:8000/predic
{
  "age": 30,
  "annee_experience_totale": 5,
  "revenu_mensuel": 3000,
  "distance_domicile_travail": 10,
  "nb_formations_suivies": 2,
  "nombre_heures_travaillees": 160,
  "frequence_deplacement": "Rarement"
}
repons
{
  "prediction": 1
}
Les identifiants ne doivent pas être écrits en clair dans le code.

Créer un fichier .env (non versionné) :

DATABASE_URL=postgresql+psycopg://<USER>:<PASSWORD>@localhost:5432/churn_db

test
pytest -v

🧰 Technologies utilisées

FastAPI, Uvicorn

Pydantic v2

Scikit-learn, Pandas, Numpy, Joblib

SQLAlchemy, PostgreSQL (optionnel)

Pytest, HTTPX

GitHub Actions

Anna Harba
Projet OpenClassrooms
