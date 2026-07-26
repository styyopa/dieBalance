"""
Prediction history stored in JSON format.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

HISTORY_PATH = Path("data/history.json")


def _ensure_data_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _read_history(path: Path = HISTORY_PATH) -> list[dict]:
    _ensure_data_dir(path)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []


def _write_history(records: list[dict], path: Path = HISTORY_PATH) -> None:
    _ensure_data_dir(path)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)


def save_prediction(
    prediction: str,
    confidence: float,
    nutritional_values: dict,
    timestamp: str | None = None,
    path: Path = HISTORY_PATH,
) -> None:
    record = {
        "timestamp": timestamp or datetime.now().isoformat(timespec="seconds"),
        "prediction": prediction,
        "confidence": float(confidence),
        "nutritional_values": nutritional_values,
    }

    records = _read_history(path)
    records.append(record)
    _write_history(records, path)


def load_history(path: Path = HISTORY_PATH, limit: int = 50) -> list[dict]:
    records = _read_history(path)
    records.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
    return records[:limit]


def clear_history(path: Path = HISTORY_PATH) -> None:
    _write_history([], path)


def log_meal(
    food_name: str,
    grams: float,
    risk_label: str,
    glycemic_load: float,
    confidence: float = 0.0,
    path: Path = HISTORY_PATH,
) -> None:
    nutritional_values = {
        "food_name": food_name,
        "grams": float(grams),
        "risk_label": risk_label,
        "glycemic_load": float(glycemic_load),
    }
    save_prediction(
        prediction=risk_label,
        confidence=confidence,
        nutritional_values=nutritional_values,
        path=path,
    )


def get_history(path: Path = HISTORY_PATH, limit: int = 50) -> list[dict]:
    return load_history(path, limit)


def weekly_summary(path: Path = HISTORY_PATH) -> dict:
    records = load_history(path, limit=1000)
    week_ago = datetime.now() - timedelta(days=7)
    summary = {}

    for record in records:
        timestamp = record.get("timestamp")
        try:
            record_time = datetime.fromisoformat(timestamp)
        except (TypeError, ValueError):
            continue

        if record_time >= week_ago:
            risk = record.get("prediction", "Unknown")
            summary[risk] = summary.get(risk, 0) + 1

    return summary
