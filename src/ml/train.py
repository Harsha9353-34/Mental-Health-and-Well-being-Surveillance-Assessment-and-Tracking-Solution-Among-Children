"""
ML Risk Classifier — Training Script.

Algorithm:  Random Forest (Shatte et al., 2019; Burke et al., 2019)
Pipeline:   StandardScaler → RandomForestClassifier
Validation: 5-fold stratified cross-validation

Run:
    python src/ml/train.py

Prerequisite:
    python src/data/generate_dataset.py   (creates data/synthetic_checkins.csv)

Output:
    models/risk_classifier.pkl
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble        import RandomForestClassifier
from sklearn.preprocessing   import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline        import Pipeline
from sklearn.metrics         import classification_report, confusion_matrix

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE        = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.normpath(os.path.join(_HERE, "..", "..", "data", "synthetic_checkins.csv"))
MODEL_FILE   = os.path.normpath(os.path.join(_HERE, "..", "..", "models", "risk_classifier.pkl"))

FEATURE_COLS = ["mood_score", "sleep_hours", "screen_time", "physical_play", "school_stress"]
TARGET_COL   = "risk_tier"


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train() -> tuple[Pipeline, float]:
    """
    Train the risk classification pipeline and serialise to disk.

    Returns
    -------
    pipeline   : fitted sklearn Pipeline
    cv_mean    : float — mean 5-fold cross-validation accuracy
    """
    # ------------------------------------------------------------------
    # 1. Load dataset
    # ------------------------------------------------------------------
    if not os.path.exists(DATASET_FILE):
        print(
            f"❌  Dataset not found: {DATASET_FILE}\n"
            "    Run `python src/data/generate_dataset.py` first.",
            file=sys.stderr,
        )
        sys.exit(1)

    df = pd.read_csv(DATASET_FILE)
    X  = df[FEATURE_COLS].values.astype(float)
    y  = df[TARGET_COL].values.astype(int)

    print(f"📊  Dataset loaded: {X.shape[0]} samples, {X.shape[1]} features")
    unique, counts = np.unique(y, return_counts=True)
    for cls, cnt in zip(unique, counts):
        print(f"    Tier {cls}: {cnt} samples ({cnt/len(y)*100:.1f}%)")

    # ------------------------------------------------------------------
    # 2. Build pipeline
    # ------------------------------------------------------------------
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators   = 200,
            max_depth      = 8,
            min_samples_split = 5,
            min_samples_leaf  = 2,
            class_weight   = "balanced",
            random_state   = 42,
            n_jobs         = -1,
        )),
    ])

    # ------------------------------------------------------------------
    # 3. 5-fold stratified cross-validation
    # ------------------------------------------------------------------
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("\n📈  5-Fold Stratified Cross-Validation …")
    cv_scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy")
    print(f"    Fold accuracies: {[round(s, 4) for s in cv_scores]}")
    print(f"    Mean ± Std:      {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # ------------------------------------------------------------------
    # 4. Fit on full dataset
    # ------------------------------------------------------------------
    pipeline.fit(X, y)
    y_pred = pipeline.predict(X)

    print("\n📋  Classification Report (full training set):")
    print(classification_report(
        y, y_pred,
        target_names=["Low/Healthy", "Moderate/Monitoring", "Elevated/Action"],
    ))

    print("🔢  Confusion Matrix:")
    print(confusion_matrix(y, y_pred))

    # ------------------------------------------------------------------
    # 5. Feature importances
    # ------------------------------------------------------------------
    rf          = pipeline.named_steps["classifier"]
    importances = rf.feature_importances_
    print("\n🔍  Feature Importances:")
    for feat, imp in sorted(zip(FEATURE_COLS, importances), key=lambda x: -x[1]):
        bar = "█" * int(imp * 40)
        print(f"    {feat:<20s}  {imp:.4f}  {bar}")

    # ------------------------------------------------------------------
    # 6. Serialise
    # ------------------------------------------------------------------
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\n✅  Model saved → {MODEL_FILE}")

    return pipeline, float(cv_scores.mean())


if __name__ == "__main__":
    train()
