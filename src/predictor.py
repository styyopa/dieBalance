import joblib
import pandas as pd

from src.model_trainer import FEATURE_COLS, MODEL_PATH


def load_model(model_path: str = MODEL_PATH):
    return joblib.load(model_path)


def _build_feature_frame(food_row: dict) -> pd.DataFrame:
    return pd.DataFrame([{col: food_row.get(col, 0.0) for col in FEATURE_COLS}])


def predict_risk(model, food_row: dict) -> str:
    features = _build_feature_frame(food_row)
    return model.predict(features)[0]


def predict_risk_and_confidence(model, food_row: dict) -> tuple[str, float]:
    features = _build_feature_frame(food_row)
    prediction = model.predict(features)[0]
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        confidence = float(proba.max())
    else:
        confidence = 0.0
    return prediction, confidence
