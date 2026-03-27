import os
import sqlite3
import pandas as pd
import streamlit as st

# =========================
# Configuration page
# =========================
st.set_page_config(page_title="MLOps Monitoring Dashboard", layout="wide")
st.title(" Dashboard global - Monitoring & Optimisation")

st.markdown("""
Ce dashboard centralise :
- les métriques opérationnelles de l’API,
- les résultats d’optimisation post-déploiement,
- les benchmarks de performance,
- les indicateurs de qualité du modèle.
""")

# =========================
# Chargement des logs API
# =========================
db_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "monitoring.db")
)

df = pd.DataFrame()

if os.path.exists(db_path):
    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM api_logs ORDER BY id DESC", con)
    except Exception as e:
        st.error(f"Erreur lors du chargement des logs API : {e}")
    finally:
        con.close()
else:
    st.warning("Base monitoring.db introuvable.")

# =========================
# 1. Monitoring opérationnel
# =========================
st.header("1. Monitoring opérationnel")

if not df.empty:
    nb_requetes = len(df)
    lat_mean = round(df["latency_ms"].mean(), 2)
    lat_median = round(df["latency_ms"].median(), 2)
    lat_max = round(df["latency_ms"].max(), 2)
    p95 = round(df["latency_ms"].quantile(0.95), 2)
    error_rate = round((df["status_code"] >= 400).mean() * 100, 2)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Nombre de requêtes", nb_requetes)
    c2.metric("Latence moyenne", f"{lat_mean} ms")
    c3.metric("Latence médiane", f"{lat_median} ms")
    c4.metric("Latence p95", f"{p95} ms")
    c5.metric("Taux d'erreur", f"{error_rate} %")

    # KPI par statut HTTP
    count_200 = int((df["status_code"] == 200).sum())
    count_422 = int((df["status_code"] == 422).sum())
    count_500 = int((df["status_code"] == 500).sum())

    st.subheader("Répartition des requêtes")
    k1, k2, k3 = st.columns(3)
    k1.metric("Succès (200)", count_200)
    k2.metric("Erreurs 422", count_422)
    k3.metric("Erreurs 500", count_500)

    # Alertes simples
    if error_rate > 5:
        st.error("⚠️ Alerte : le taux d’erreur dépasse 5 %.")
    elif lat_mean > 2000:
        st.warning("⚠️ Alerte : la latence moyenne est élevée.")
    else:
        st.success("✅ L’API est globalement stable.")

    # Évolution latence
    st.subheader("Évolution de la latence")
    chart_df = df.sort_values("id")[["id", "latency_ms"]].set_index("id")
    st.line_chart(chart_df)

    # Répartition des statuts HTTP
    st.subheader("Répartition des statuts HTTP")
    status_counts = df["status_code"].value_counts().sort_index()
    status_df = status_counts.rename_axis("status_code").reset_index(name="count")
    st.dataframe(status_df, width="stretch")
    st.bar_chart(status_counts)

    # Derniers logs
    st.subheader("Derniers logs API")
    st.dataframe(df, width="stretch")

else:
    st.info("Aucun log API disponible.")

# =========================
# 2. Résultats optimisation
# =========================
st.header("2. Optimisation post-déploiement")

results_df = pd.DataFrame([
    {
        "Version": "Baseline sklearn",
        "Latence API (ms)": 1227.96,
        "Temps inférence (s)": 3.3327,
        "Régression": "Non"
    },
    {
        "Version": "ONNX Runtime",
        "Latence API (ms)": 200.00,
        "Temps inférence (s)": 0.0674,
        "Régression": "Non"
    },
])

st.dataframe(results_df, width="stretch")

gain = 3.3327 / 0.0674
st.metric("Gain de performance ONNX", f"{gain:.2f}x plus rapide")
st.header("6. Performance interne du modèle")

st.metric("Temps sklearn (1000 prédictions)", "1.72 s")
st.metric("Temps ONNX (1000 prédictions)", "0.20 s")
st.metric("Gain", "8.5x") 

st.markdown("""
**Analyse :** la conversion du modèle vers **ONNX Runtime** réduit fortement le temps d’inférence.  
Cette optimisation améliore directement la **latence de réponse de l’API** et permet un déploiement plus performant.
""")

# =========================
# 3. Benchmark détaillé
# =========================
st.header("3. Benchmark sklearn vs ONNX")

benchmark_df = pd.DataFrame({
    "Backend": ["scikit-learn", "ONNX Runtime"],
    "Temps pour 1000 prédictions (s)": [3.3327, 0.0674]
})

st.dataframe(benchmark_df, width="stretch")
st.bar_chart(benchmark_df.set_index("Backend"))

# =========================
# 4. Détection du data drift
# =========================
st.header("4. Détection du data drift")

report_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "monitoring_reports",
        "data_drift_report.html"
    )
)

if os.path.exists(report_path):
    st.success("Rapport de data drift disponible")
    st.code(report_path)
else:
    st.warning("Rapport de data drift non trouvé.")

# =========================
# 5. Synthèse
# =========================
st.header("5. Synthèse")

st.markdown("""
### Points clés
- L’API est monitorée à travers les logs de latence et de statut HTTP.
- Les indicateurs principaux (moyenne, médiane, p95, taux d’erreur) sont regroupés dans un tableau de bord unique.
- La répartition des statuts HTTP permet de distinguer les requêtes réussies des erreurs de validation ou d’exécution.
- L’optimisation du modèle avec **ONNX Runtime** montre un gain significatif de performance.
- Le suivi du **data drift** complète le pilotage du système en production.

### Conclusion
Ce dashboard sert de point d’entrée unique pour surveiller la stabilité, la performance
et la robustesse du service de prédiction en production.
""")