import os
import sys
import time
import cProfile
import pstats
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app.ml_model import predict_from_dict

sample_input = {
    "age": 30,
    "annee_experience_totale": 5,
    "revenu_mensuel": 3000,
    "distance_domicile_travail": 10,
    "nb_formations_suivies": 2,
    "nombre_heures_travaillees": 160,
    "frequence_deplacement": "Rarement"
}

def run_pipeline():
    for _ in range(100):
        predict_from_dict(sample_input)

start = time.perf_counter()

pr = cProfile.Profile()
pr.enable()

run_pipeline()

pr.disable()
end = time.perf_counter()

total_time = end - start
avg_time = total_time / 100

print(f"Temps total pour 100 prédictions : {total_time:.4f} s")
print(f"Temps moyen par prédiction : {avg_time:.6f} s")

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
ps.print_stats(20)

print(s.getvalue())