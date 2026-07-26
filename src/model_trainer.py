import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from .loader import load_foods
from .preprocessing import clean_data

FEATURE_COLS = ["carbs", "glycemic_index", "protein", "fiber", "fat"]
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"


def compute_adjusted_glycemic_load(row: pd.Series) -> float:
    """Compute adjusted glycemic load accounting for protein and fat slowing."""
    net_carbs = max(row["carbs"] - row["fiber"], 0.0)
    gl = (row["glycemic_index"] * net_carbs) / 100
    buffer = row["protein"] * 0.05 + row["fat"] * 0.03
    return max(gl - buffer, 0.0)


def classify_risk(gl: float) -> str:
    if gl <= 10:
        return "Low"
    elif gl <= 19:
        return "Medium"
    return "High"


def generate_labels(df: pd.DataFrame) -> pd.Series:
    adjusted_gl = df.apply(compute_adjusted_glycemic_load, axis=1)
    return adjusted_gl.apply(classify_risk)


def train_model(data_path: str = str(BASE_DIR / "data" / "foods.csv"), model_path: str = str(MODEL_PATH)):
    df = load_foods(data_path)
    df = clean_data(df)
    df["risk_label"] = generate_labels(df)

    X = df[FEATURE_COLS]
    y = df["risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("=== Model performance on test set ===")
    print(classification_report(y_test, y_pred, zero_division=0))

    importances = pd.Series(model.feature_importances_, index=FEATURE_COLS)
    print("=== Feature importances ===")
    print(importances.sort_values(ascending=False).round(3))

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"\nModel saved: {model_path}")

    return model


if __name__ == "__main__":
    train_model()
