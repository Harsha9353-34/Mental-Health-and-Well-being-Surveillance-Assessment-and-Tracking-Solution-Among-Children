"""
Local CSV-based check-in history storage.

Privacy Design (DPDP Act 2023, Section 9):
- No personally identifiable information (PII) is stored.
- Journal text is NEVER persisted — only aggregate sentiment scores.
- Session tokens are ephemeral and anonymised.
- All data remains on the local machine; nothing is transmitted externally.
"""

import os
import pandas as pd
from datetime import datetime

# Resolve path relative to project root (two levels up from this file)
_HERE = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.normpath(os.path.join(_HERE, "..", "..", "data", "checkin_history.csv"))

COLUMNS: list[str] = [
    "timestamp",
    "mood_label",
    "mood_score",
    "sleep_hours",
    "screen_time",
    "physical_play",
    "school_stress",
    "sentiment_compound",
    "sentiment_tone",
    "risk_tier",
    "risk_label",
]


def save_checkin(record: dict) -> None:
    """
    Append a single check-in record to the history CSV.

    Parameters
    ----------
    record : dict
        Must contain all keys defined in COLUMNS (except 'timestamp',
        which is auto-populated).
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    record = {**record, "timestamp": datetime.now().isoformat(timespec="seconds")}

    df_new = pd.DataFrame([record])
    # Reorder columns to canonical order (fill missing with NaN)
    for col in COLUMNS:
        if col not in df_new.columns:
            df_new[col] = None
    df_new = df_new[COLUMNS]

    write_header = not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0
    df_new.to_csv(HISTORY_FILE, mode="a", header=write_header, index=False)


def load_history() -> pd.DataFrame:
    """
    Load the complete check-in history.

    Returns
    -------
    pd.DataFrame
        Empty DataFrame with correct columns if no history exists yet.
    """
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(HISTORY_FILE, parse_dates=["timestamp"])
    return df.sort_values("timestamp", ascending=True).reset_index(drop=True)


def has_history() -> bool:
    """Return True if at least one check-in record has been saved."""
    return os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 100


def get_recent_checkins(n: int = 7) -> pd.DataFrame:
    """Return the n most recent check-in records (newest first)."""
    df = load_history()
    if df.empty:
        return df
    return df.sort_values("timestamp", ascending=False).head(n)


def check_distress_alert(consecutive_threshold: int = 3) -> bool:
    """
    Return True if the last `consecutive_threshold` check-ins were all
    Elevated Risk (Tier 2).  Used to trigger guardian distress alerts.
    """
    df = load_history()
    if len(df) < consecutive_threshold:
        return False
    recent_tiers = df["risk_tier"].tail(consecutive_threshold).astype(int)
    return bool((recent_tiers >= 2).all())


def clear_history() -> None:
    """Delete the check-in history file (used for testing / reset)."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
