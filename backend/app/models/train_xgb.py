import pandas as pd
from xgboost import XGBRegressor
import joblib

FEATURES = [
    "calories", "protein_g", "fat_g", "carbs_g", "fiber_g",
    "iron_mg", "sodium_mg",
    "low_gi_candidate", "high_fiber",
    "protein_dense", "iron_rich", "low_sodium"
]

def train():
    df = pd.read_csv("app/data/nutriwise_food_core.csv")

    X = df[FEATURES].astype(float)

    # heuristic target
    y = (
        df["high_fiber"].astype(int) * 2 +
        df["protein_dense"].astype(int) * 2 +
        df["low_gi_candidate"].astype(int) * 3 +
        df["iron_rich"].astype(int)
    )

    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05
    )

    model.fit(X, y)
    joblib.dump(model, "app/models/xgb_model.pkl")

if __name__ == "__main__":
    train()
