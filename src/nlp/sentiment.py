"""
VADER-based NLP Sentiment Analysis Module.

Performs linguistic sentiment scoring on optional child journal entries.

IMPORTANT DISCLAIMER:
    Sentiment scores are purely linguistic polarity measures derived from
    text valence. They do NOT constitute psychiatric evaluations, clinical
    affect assessments, or diagnostic outputs of any kind.

Reference:
    Hutto, C. J. & Gilbert, E. (2014). VADER: A Parsimonious Rule-based
    Model for Sentiment Analysis of Social Media Text. ICWSM-14.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Module-level singleton to avoid re-initialising the lexicon on every call
_analyzer: SentimentIntensityAnalyzer | None = None


def _get_analyzer() -> SentimentIntensityAnalyzer:
    """Return (or lazily initialise) the shared VADER analyser instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def analyze_sentiment(text: str) -> dict:
    """
    Compute VADER sentiment scores for a journal text entry.

    Parameters
    ----------
    text : str
        The child's optional reflective journal text. May be empty or None.

    Returns
    -------
    dict
        compound   : float  Normalised compound score in [-1.0, +1.0]
        pos        : float  Proportion of positive valence tokens
        neu        : float  Proportion of neutral valence tokens
        neg        : float  Proportion of negative valence tokens
        tone_tag   : str    "Positive" | "Neutral" | "Negative"
        tone_emoji : str    Visual indicator emoji
        tone_color : str    Hex color for UI rendering
    """
    if not text or not text.strip():
        return {
            "compound":    0.0,
            "pos":         0.0,
            "neu":         1.0,
            "neg":         0.0,
            "tone_tag":    "Neutral",
            "tone_emoji":  "😐",
            "tone_color":  "#7f8c8d",
        }

    analyzer = _get_analyzer()
    scores   = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        tone_tag   = "Positive"
        tone_emoji = "😊"
        tone_color = "#27ae60"
    elif compound <= -0.05:
        tone_tag   = "Negative"
        tone_emoji = "😔"
        tone_color = "#c0392b"
    else:
        tone_tag   = "Neutral"
        tone_emoji = "😐"
        tone_color = "#7f8c8d"

    return {
        "compound":    round(compound, 4),
        "pos":         round(scores["pos"], 4),
        "neu":         round(scores["neu"], 4),
        "neg":         round(scores["neg"], 4),
        "tone_tag":    tone_tag,
        "tone_emoji":  tone_emoji,
        "tone_color":  tone_color,
    }
