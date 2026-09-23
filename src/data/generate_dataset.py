"""
Synthetic Training Data Generator for the ML Risk Classifier.

Generates ~2,000 labelled check-in records using domain-informed scoring
rules derived from the Phase 1 literature review.

DISCLAIMER:
    This is purely synthetic data generated for academic prototype evaluation.
    No real patient or child data is used at any stage of this project.

Run:
    python src/data/generate_dataset.py

Output:
    data/synthetic_checkins.csv
"""

import os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SEED      = 42
N_SAMPLES = 2000

_HERE       = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.normpath(os.path.join(_HERE, "..", "..", "data", "synthetic_checkins.csv"))


# ---------------------------------------------------------------------------
# Risk Scoring Logic (domain-informed by Phase 1 literature)
# ---------------------------------------------------------------------------

def _composite_risk(
    mood_score:    np.ndarray,
    sleep_hours:   np.ndarray,
    screen_time:   np.ndarray,
    physical_play: np.ndarray,
    school_stress: np.ndarray,
) -> np.ndarray:
    """
    Compute a composite risk score ∈ [0, 1] per sample.
    Higher score → higher well-being risk.

    Feature weights informed by:
      - Burke et al. (2019): mood & sleep are strongest predictors
      - Bitsko et al. (2022): screen time & stress are secondary factors
      - WHO (2022): physical activity is a protective factor
    """
    mood_risk  = (6 - mood_score)  / 5.0                          # 0=Joyful → 1=Frustrated
    sleep_risk = np.clip((8.0 - sleep_hours)  / 4.0, 0.0, 1.0)   # 0 if ≥8 hrs, 1 if 4 hrs
    scrn_risk  = np.clip(screen_time           / 6.0, 0.0, 1.0)   # 0 if 0 hrs, 1 if ≥6 hrs
    play_risk  = np.clip((2.0 - physical_play) / 2.0, 0.0, 1.0)   # 0 if ≥2 hrs, 1 if 0 hrs
    strss_risk = (school_stress - 1) / 4.0                         # 0 if stress=1, 1 if stress=5

    return (
        0.28 * mood_risk
        + 0.27 * sleep_risk
        + 0.20 * scrn_risk
        + 0.13 * play_risk
        + 0.12 * strss_risk
    )


def _assign_tier(composite: np.ndarray, noise: np.ndarray) -> np.ndarray:
    """
    Map composite risk + Gaussian noise → discrete tier {0, 1, 2}.

    Thresholds:
        Tier 0 (Low / Healthy):            composite < 0.33
        Tier 1 (Moderate / Monitoring):    0.33 ≤ composite < 0.67
        Tier 2 (Elevated / Action):        composite ≥ 0.67
    """
    score = composite + noise
    tiers = np.where(score < 0.33, 0, np.where(score < 0.67, 1, 2))
    return np.clip(tiers, 0, 2).astype(int)


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)

    # Feature sampling (independent, bounded ranges from Phase 1 spec)
    mood_score    = rng.integers(1, 7,    size=N_SAMPLES)       # 1–6 inclusive
    sleep_hours   = rng.uniform(4.0, 12.0, size=N_SAMPLES)
    screen_time   = rng.uniform(0.0, 8.0,  size=N_SAMPLES)
    physical_play = rng.uniform(0.0, 4.0,  size=N_SAMPLES)
    school_stress = rng.integers(1, 6,    size=N_SAMPLES)       # 1–5 inclusive

    # Small Gaussian noise to blur the deterministic boundary
    noise = rng.normal(0.0, 0.07, size=N_SAMPLES)

    composite = _composite_risk(mood_score, sleep_hours, screen_time, physical_play, school_stress)
    risk_tier = _assign_tier(composite, noise)

    _tier_labels = {
        0: "Low / Healthy",
        1: "Moderate / Monitoring",
        2: "Elevated / Action Advised",
    }

    df = pd.DataFrame({
        "mood_score":     mood_score,
        "sleep_hours":    sleep_hours.round(1),
        "screen_time":    screen_time.round(1),
        "physical_play":  physical_play.round(1),
        "school_stress":  school_stress,
        "composite_risk": composite.round(4),
        "risk_tier":      risk_tier,
        "risk_label":     [_tier_labels[t] for t in risk_tier],
    })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    counts   = {t: (risk_tier == t).sum() for t in [0, 1, 2]}
    percents = {t: counts[t] / N_SAMPLES * 100 for t in [0, 1, 2]}

    print(f"✅  Generated {N_SAMPLES} synthetic records  →  {OUTPUT_FILE}")
    print(f"    Tier 0 (Low/Healthy):         {counts[0]:4d}  ({percents[0]:.1f}%)")
    print(f"    Tier 1 (Moderate/Monitoring): {counts[1]:4d}  ({percents[1]:.1f}%)")
    print(f"    Tier 2 (Elevated/Action):     {counts[2]:4d}  ({percents[2]:.1f}%)")

    return df


if __name__ == "__main__":
    generate()
