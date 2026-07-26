"""
DiaBalance entry point.

This module coordinates the full pipeline with minimal business logic:
- load dataset
- preprocess dataset
- train or load the model
- accept food nutritional values from the user
- predict using the trained model
- analyze the prediction
- generate recommendations
- save prediction history
- display the final report
"""
from pathlib import Path

from src.loader import load_foods
from src.preprocessing import clean_data
from src.model_trainer import train_model
from src.predictor import load_model, predict_risk_and_confidence
from src.analyzer import evaluate_food
from src.recommender import generate_dietary_recommendation
from src.history import save_prediction

DATA_PATH = Path("data/foods.csv")
MODEL_PATH = Path("models/model.pkl")


def load_and_prepare_dataset(data_path: Path = DATA_PATH):
    df = load_foods(str(data_path))
    return clean_data(df)


def get_or_train_model(model_path: Path = MODEL_PATH):
    if model_path.exists() and model_path.stat().st_size > 0:
        return load_model(str(model_path))
    return train_model(model_path=str(model_path))


def parse_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except ValueError:
        return default


def prompt_food_values() -> dict:
    print("Enter nutritional values for a food item.")
    return {
        "name": input("Food name: ").strip() or "Custom food",
        "carbs": parse_float(input("Carbohydrates (g): ").strip() or "0"),
        "glycemic_index": parse_float(input("Glycemic index: ").strip() or "0"),
        "protein": parse_float(input("Protein (g): ").strip() or "0"),
        "fiber": parse_float(input("Fiber (g): ").strip() or "0"),
        "fat": parse_float(input("Fat (g): ").strip() or "0"),
    }

def find_food_in_database(df):
    name = input("Enter food name: ").strip()

    matches = df[
        df["name"].str.lower() == name.lower()
    ]

    if matches.empty:
        print("Food not found. Please enter values manually.")
        return prompt_food_values()

    food = matches.iloc[0]

    return {
        "name": str(food["name"]),
        "carbs": float(food["carbs"]),
        "glycemic_index": float(food["glycemic_index"]),
        "protein": float(food["protein"]),
        "fiber": float(food["fiber"]),
        "fat": float(food["fat"]),
    }

def report_prediction(
    food: dict,
    risk: str,
    confidence: float,
    analysis: dict,
    recommendation: dict,
) -> None:
    risk_label_text = f"{risk} Glycemic Risk" if risk in {"Low", "Medium", "High"} else risk
    risk_score = int(confidence * 100)

    print(f"\n--- Prediction report for {food.get('name', 'food')} ---")
    print(f"Carbs: {food['carbs']} g | Fiber: {food['fiber']} g | GI: {food['glycemic_index']}")
    print(f"Protein: {food['protein']} g | Fat: {food['fat']} g")
    print(f"Prediction: {risk_label_text}")
    print(f"Confidence: {confidence:.0%}")
    print(f"Risk score: {risk_score} / 100")
    print(f"Recommendation: {recommendation['recommendation']}")

    if recommendation.get("details"):
        print("Details:")
        for detail in recommendation["details"]:
            print(f"- {detail}")

    if analysis.get("explanations"):
        print("Rule-based analysis:")
        for explanation in analysis["explanations"]:
            print(f"- {explanation}")


def main() -> None:
    foods_df = load_and_prepare_dataset()
    model = get_or_train_model()

    food = find_food_in_database(foods_df)
    risk, confidence = predict_risk_and_confidence(model, food)
    analysis = evaluate_food(food)
    recommendation = generate_dietary_recommendation(risk, analysis.get("explanations"))

    save_prediction(
        prediction=risk,
        confidence=confidence,
        nutritional_values=food,
    )

    report_prediction(food, risk, confidence, analysis, recommendation)


if __name__ == "__main__":
    main()
