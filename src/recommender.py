"""
Rule-based recommender for DiaBalance.

This module generates dietary guidance based on a predicted risk level and
analyzer explanations. It does not perform any machine learning itself.
"""

RISK_RECOMMENDATIONS = {
    "Low": "Suitable as part of a balanced diet.",
    "Medium": "Consume in moderation and monitor portion size.",
    "High": "Consider replacing with foods that have lower glycemic impact.",
}


def generate_dietary_recommendation(
    risk_label: str,
    analyzer_explanations: list[str] | None = None,
) -> dict:
    """Create a clear dietary recommendation from AI risk and analyzer output."""
    recommendation = RISK_RECOMMENDATIONS.get(
        risk_label,
        "Monitor nutritional values and choose foods carefully.",
    )

    details = []
    if analyzer_explanations:
        details = [f"{explanation}." for explanation in analyzer_explanations]

    return {
        "risk_label": risk_label,
        "recommendation": recommendation,
        "details": details,
    }


def format_recommendation(recommendation: dict) -> str:
    lines = [f"Recommendation: {recommendation['recommendation']}" ]
    if recommendation.get("details"):
        lines.append("Details:")
        lines.extend([f"- {detail}" for detail in recommendation["details"]])
    return "\n".join(lines)
