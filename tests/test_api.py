import pytest
from httpx import AsyncClient, ASGITransport
from app import app  

@pytest.mark.asyncio
async def test_predict():
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/predict",
            json={
                "age": 30,
                "annee_experience_totale": 5,
                "revenu_mensuel": 3000,
                "distance_domicile_travail": 10,
                "nb_formations_suivies": 2,
                "nombre_heures_travaillees": 160,
                "frequence_deplacement": "Rarement"
            }
        )

    assert response.status_code == 200
