import joblib
import pandas as pd

FEATURES = [
    "calories", "protein_g", "fat_g", "carbs_g", "fiber_g",
    "iron_mg", "sodium_mg",
    "low_gi_candidate", "high_fiber",
    "protein_dense", "iron_rich", "low_sodium"
]

model = joblib.load("app/models/xgb_model.pkl")

def predict_base_scores(df: pd.DataFrame):
    return model.predict(df[FEATURES].astype(float))
