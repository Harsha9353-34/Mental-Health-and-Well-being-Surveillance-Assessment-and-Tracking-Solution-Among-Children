"""
Feature Attribution & Explainability Module.

Uses the Random Forest's built-in feature importances (no external SHAP
dependency) to generate interpretable visualisations and plain-English
explanations for individual predictions.

This supports the explainability goal referenced in:
  Le Glaz et al. (2021) — interpretability in NLP/ML health applications.
"""

import os
import joblib
import numpy as np
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Paths & Constants
# ---------------------------------------------------------------------------
_HERE      = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.normpath(os.path.join(_HERE, "..", "..", "models", "risk_classifier.pkl"))

FEATURE_NAMES: list[str] = [
    "mood_score", "sleep_hours", "screen_time", "physical_play", "school_stress"
]

FEATURE_DISPLAY: dict[str, str] = {
    "mood_score":    "😊 Mood Score",
    "sleep_hours":   "🌙 Sleep (hrs)",
    "screen_time":   "📱 Screen Time (hrs)",
    "physical_play": "🏃 Physical Play (hrs)",
    "school_stress": "📚 School Stress (1–5)",
}


# ---------------------------------------------------------------------------
# Global Feature Importances
# ---------------------------------------------------------------------------

def get_feature_importances() -> dict[str, float]:
    """Return global RF feature importances as {feature_name: importance}."""
    if not os.path.exists(MODEL_FILE):
        return {}
    pipeline    = joblib.load(MODEL_FILE)
    rf          = pipeline.named_steps["classifier"]
    importances = rf.feature_importances_
    return {name: float(imp) for name, imp in zip(FEATURE_NAMES, importances)}


def plot_feature_importance() -> go.Figure | None:
    """
    Return a Plotly horizontal bar chart of global feature importances.
    Returns None if the model has not been trained yet.
    """
    importances = get_feature_importances()
    if not importances:
        return None

    sorted_items  = sorted(importances.items(), key=lambda x: x[1])  # ascending for horizontal bar
    names         = [FEATURE_DISPLAY[k] for k, _ in sorted_items]
    values        = [v for _, v in sorted_items]

    colors = [
        "#c0392b" if v > 0.25 else "#e67e22" if v > 0.15 else "#2980b9"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x             = values,
        y             = names,
        orientation   = "h",
        marker_color  = colors,
        text          = [f"{v * 100:.1f}%" for v in values],
        textposition  = "outside",
        cliponaxis    = False,
    ))

    fig.update_layout(
        title       = "Risk Factor Importance (Global)",
        xaxis_title = "Importance Score",
        xaxis       = dict(range=[0, max(values) * 1.25]),
        height      = 300,
        margin      = dict(l=10, r=60, t=40, b=10),
        plot_bgcolor  = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",
        font          = dict(size=13),
    )

    return fig


# ---------------------------------------------------------------------------
# Plain-English Prediction Explanation
# ---------------------------------------------------------------------------

def explain_prediction(feature_vector: list[float], risk_tier: int) -> str:
    """
    Generate a plain-English explanation for a risk tier prediction.

    Parameters
    ----------
    feature_vector : list[float]
        [mood_score, sleep_hours, screen_time, physical_play, school_stress]
    risk_tier : int
        Predicted tier (0, 1, or 2).

    Returns
    -------
    str : Markdown-formatted explanation string.
    """
    mood, sleep, screen, play, stress = feature_vector

    concerns:  list[str] = []
    strengths: list[str] = []

    # Mood
    if mood <= 2:
        concerns.append("low reported mood")
    elif mood >= 5:
        strengths.append("positive mood")

    # Sleep (WHO recommended 9–11 hrs for children)
    if sleep < 7.0:
        concerns.append(f"insufficient sleep ({sleep:.1f} hrs — WHO recommends 9–11 hrs)")
    elif sleep >= 9.0:
        strengths.append("adequate sleep duration")

    # Screen time
    if screen >= 4.0:
        concerns.append(f"high screen exposure ({screen:.1f} hrs/day)")
    elif screen <= 2.0:
        strengths.append("healthy screen time limits")

    # Physical play
    if play < 1.0:
        concerns.append("minimal physical activity")
    elif play >= 2.0:
        strengths.append("good physical play")

    # Stress
    if stress >= 4:
        concerns.append("elevated school stress")
    elif stress <= 2:
        strengths.append("low academic stress")

    parts: list[str] = []
    if concerns:
        parts.append(f"Contributing factors: **{', '.join(concerns)}**.")
    if strengths:
        parts.append(f"Positive indicators: **{', '.join(strengths)}**.")
    if not concerns and not strengths:
        parts.append("Lifestyle indicators are well-balanced overall.")

    return " ".join(parts)
