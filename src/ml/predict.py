"""
ML Inference Wrapper — Loads the serialised pipeline and runs predictions.

Usage:
    from src.ml.predict import predict

    result = predict(
        mood_score=3, sleep_hours=6.0,
        screen_time=5.0, physical_play=0.5, school_stress=4
    )
    # result["risk_tier"]   → 2
    # result["risk_label"]  → "Elevated Risk / Action Advised"
"""

import os
import joblib
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE      = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.normpath(os.path.join(_HERE, "..", "..", "models", "risk_classifier.pkl"))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FEATURE_NAMES: list[str] = [
    "mood_score", "sleep_hours", "screen_time", "physical_play", "school_stress"
]

TIER_LABELS: dict[int, str] = {
    0: "Low Risk / Healthy",
    1: "Moderate Risk / Monitoring",
    2: "Elevated Risk / Action Advised",
}

# Module-level singleton
_pipeline = None


def _load_model():
    """Lazily load and cache the serialised pipeline."""
    global _pipeline
    if _pipeline is None:
        if not os.path.exists(MODEL_FILE):
            raise FileNotFoundError(
                f"Model not found at: {MODEL_FILE}\n"
                "Please run:  python src/ml/train.py"
            )
        _pipeline = joblib.load(MODEL_FILE)
    return _pipeline


def predict(
    mood_score:    int | float,
    sleep_hours:   float,
    screen_time:   float,
    physical_play: float,
    school_stress: int | float,
) -> dict:
    """
    Predict the well-being risk tier for a single check-in.

    Parameters
    ----------
    mood_score    : int   1–6  (from emoji picker, 6=Joyful, 1=Frustrated)
    sleep_hours   : float 4.0–12.0
    screen_time   : float 0.0–8.0
    physical_play : float 0.0–4.0
    school_stress : int   1–5

    Returns
    -------
    dict
        risk_tier      : int      Predicted tier (0, 1, or 2)
        risk_label     : str      Human-readable tier label
        probabilities  : dict     {tier_label: probability} for all 3 tiers
        confidence     : float    Max class probability
        feature_vector : list     Input features in canonical order
    """
    pipeline = _load_model()

    X     = np.array([[mood_score, sleep_hours, screen_time, physical_play, school_stress]], dtype=float)
    tier  = int(pipeline.predict(X)[0])
    proba = pipeline.predict_proba(X)[0]

    # Map class probabilities to tier labels (classes_ may not always be [0,1,2])
    classes  = pipeline.classes_
    prob_dict = {
        TIER_LABELS[int(c)]: round(float(p), 4)
        for c, p in zip(classes, proba)
    }
    # Ensure all three tiers are present (even with zero probability)
    for t in range(3):
        prob_dict.setdefault(TIER_LABELS[t], 0.0)

    return {
        "risk_tier":     tier,
        "risk_label":    TIER_LABELS[tier],
        "probabilities": prob_dict,
        "confidence":    round(float(max(proba)), 4),
        "feature_vector": [
            float(mood_score), float(sleep_hours), float(screen_time),
            float(physical_play), float(school_stress),
        ],
    }
