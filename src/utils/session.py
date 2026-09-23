"""
Streamlit session state management helpers.

Centralises all session-state key definitions so that UI modules
reference a single source of truth rather than raw string literals.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Default Values
# ---------------------------------------------------------------------------
_DEFAULTS: dict = {
    "selected_mood":      None,   # str — currently selected mood label
    "last_checkin":       None,   # dict — full record of most recent check-in
    "last_risk_tier":     None,   # int 0/1/2
    "last_risk_label":    None,   # str
    "last_sentiment":     None,   # dict from nlp.sentiment.analyze_sentiment
    "grounding_step":     0,      # int — current step in grounding exercise
    "grounding_started":  False,  # bool
    "affirmation_index":  0,      # int — rotating affirmation index
    "current_page":       None,   # str — override sidebar navigation
}


def init_session_state() -> None:
    """Initialise all session-state keys with defaults (idempotent)."""
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def set_last_checkin(checkin_data: dict) -> None:
    """
    Cache the most recent check-in payload in session state for use
    by the sidebar status indicator and other UI components.

    Parameters
    ----------
    checkin_data : dict
        Must include 'risk_tier', 'risk_label', and 'sentiment' keys.
    """
    st.session_state.last_checkin   = checkin_data
    st.session_state.last_risk_tier  = checkin_data.get("risk_tier")
    st.session_state.last_risk_label = checkin_data.get("risk_label")
    st.session_state.last_sentiment  = checkin_data.get("sentiment")


def navigate_to(page: str) -> None:
    """
    Set the current_page override and trigger a rerun.

    Parameters
    ----------
    page : str
        Must match one of the sidebar radio option strings.
    """
    st.session_state.current_page = page
    st.rerun()
