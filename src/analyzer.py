"""
Rule-based analyzer for DiaBalance.

This module evaluates nutritional values and generates human-readable
explanations for the prediction without using machine learning.
"""


def compute_net_carbs(carbs: float, fiber: float) -> float:
    return max(carbs - fiber, 0.0)


def compute_glycemic_load(carbs: float, glycemic_index: float, fiber: float) -> float:
    net_carbs = compute_net_carbs(carbs, fiber)
    gl = (glycemic_index * net_carbs) / 100
    return round(gl, 2)


def classify_risk(glycemic_load: float) -> str:
    if glycemic_load <= 10:
        return "Low"
    elif glycemic_load <= 19:
        return "Medium"
    return "High"


def explain_glycemic_index(glycemic_index: float) -> str:
    if glycemic_index >= 70:
        return "High Glycemic Index"
    if glycemic_index >= 56:
        return "Moderate Glycemic Index"
    return "Low Glycemic Index"


def explain_carbs(carbs: float) -> str:
    if carbs >= 30:
        return "High Carbohydrate Content"
    if carbs >= 15:
        return "Moderate Carbohydrate Content"
    return "Low Carbohydrate Content"


def explain_fiber(fiber: float) -> str:
    if fiber >= 6:
        return "High Fiber Content"
    if fiber >= 3:
        return "Good Fiber Content"
    return "Low Fiber Content"


def explain_protein(protein: float) -> str:
    if protein >= 10:
        return "Good Protein Content"
    if protein >= 5:
        return "Moderate Protein Content"
    return "Low Protein Content"


def explain_fat(fat: float) -> str:
    if fat >= 15:
        return "High Fat Content"
    if fat >= 5:
        return "Moderate Fat Level"
    return "Healthy Fat Level"


def explain_nutrition(food: dict) -> list[str]:
    return [
        explain_glycemic_index(food.get("glycemic_index", 0)),
        explain_carbs(food.get("carbs", 0)),
        explain_fiber(food.get("fiber", 0)),
        explain_protein(food.get("protein", 0)),
        explain_fat(food.get("fat", 0)),
    ]


def evaluate_food(food: dict) -> dict:
    """
    food: dictionary with keys carbs, glycemic_index, fiber,
          and optionally protein, fat, name
    Returns a basic rule-based risk evaluation.
    """
    if not food or "carbs" not in food or "glycemic_index" not in food:
        return {"error": "Invalid data"}

    carbs = food.get("carbs", 0)
    glycemic_index = food.get("glycemic_index", 0)
    fiber = food.get("fiber", 0)
    protein = food.get("protein", 0)
    fat = food.get("fat", 0)

    gl = compute_glycemic_load(carbs, glycemic_index, fiber)

    return {
        "name": food.get("name", "?"),
        "glycemic_load": gl,
        "risk_label": classify_risk(gl),
        "explanations": explain_nutrition(
            {
                "carbs": carbs,
                "glycemic_index": glycemic_index,
                "fiber": fiber,
                "protein": protein,
                "fat": fat,
            }
        ),
    }
