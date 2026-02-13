# src/app/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base  # Base vient de models.py (ModelInput / ModelOutput)

#  user / mot de passe / nom de base si besoin
DATABASE_URL = "postgresql+psycopg://churn_user:Anna2025@localhost:5432/churn_db"



# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Fabriquer les sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Créer toutes les tables définies dans Base.metadata (model_inputs, model_outputs)."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # Si tu l'exécutes directement: python -m src.app.db
    init_db()
    print("Tables créées dans la base PostgreSQL.")


