from pathlib import Path
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Toy dataset
X = pd.DataFrame({
    "age": [25, 40, 35, 50, 29, 60],
    "income": [30000, 80000, 50000, 90000, 42000, 120000],
})
y = [0, 1, 0, 1, 0, 1]

model = LogisticRegression()
model.fit(X, y)

model_path = Path(__file__).resolve().parent / "src" / "app" / "models" / "model.joblib"
model_path.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, model_path)
print(f"✅ Saved model to: {model_path}")
