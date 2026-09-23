"""
Feature vector schema, constants, and reference data for the
Mental Health and Well-being Surveillance Platform.

Academic Prototype | Presidency University, Bengaluru
Author: Harsha R (20231CSE0261)
"""

# ---------------------------------------------------------------------------
# Emoji Mood States → Integer Scores
# ---------------------------------------------------------------------------
MOOD_LABELS: dict[str, int] = {
    "😄 Joyful":     6,
    "😌 Calm":       5,
    "😐 Neutral":    4,
    "😟 Worried":    3,
    "😢 Sad":        2,
    "😤 Frustrated": 1,
}

MOOD_SCORE_TO_LABEL: dict[int, str] = {v: k for k, v in MOOD_LABELS.items()}

# ---------------------------------------------------------------------------
# ML Feature Names (order must match training data columns)
# ---------------------------------------------------------------------------
FEATURE_NAMES: list[str] = [
    "mood_score",     # int  1–6  (from emoji picker)
    "sleep_hours",    # float 4.0–12.0
    "screen_time",    # float 0.0–8.0
    "physical_play",  # float 0.0–4.0
    "school_stress",  # int  1–5
]

# ---------------------------------------------------------------------------
# Risk Tier Definitions
# ---------------------------------------------------------------------------
RISK_TIERS: dict[int, dict] = {
    0: {
        "label":       "Low Risk / Healthy",
        "color":       "#27ae60",
        "bg_color":    "#eafaf1",
        "emoji":       "🟢",
        "description": "Your well-being indicators look healthy. Keep up the great habits!",
        "action":      "Explore a breathing exercise to maintain your calm.",
    },
    1: {
        "label":       "Moderate Risk / Monitoring",
        "color":       "#e67e22",
        "bg_color":    "#fef9e7",
        "emoji":       "🟡",
        "description": "Some areas of your lifestyle could use a little attention. "
                       "Small changes can make a big difference.",
        "action":      "Try a coping activity to help you feel better.",
    },
    2: {
        "label":       "Elevated Risk / Action Advised",
        "color":       "#c0392b",
        "bg_color":    "#fdedec",
        "emoji":       "🔴",
        "description": "Your indicators suggest you may benefit from additional support. "
                       "Please talk to a trusted adult.",
        "action":      "We strongly recommend speaking with a parent, teacher, or counselor. "
                       "See Crisis Resources for immediate helplines.",
    },
}

# ---------------------------------------------------------------------------
# Positive Affirmation Cards
# ---------------------------------------------------------------------------
AFFIRMATIONS: list[str] = [
    "You are brave, strong, and capable of getting through tough times. 💙",
    "It's okay to feel what you're feeling. Your emotions are valid. 🌟",
    "Every day is a new chance to grow and feel better. 🌱",
    "You are loved and you matter more than you know. 💛",
    "Asking for help is a sign of strength, not weakness. 🤝",
    "Take it one breath at a time. You've got this! 🌬️",
    "Small steps forward still count as progress. 🐾",
    "You are not alone. There are people who care about you. 🌈",
    "Your feelings are temporary, but your strength is lasting. ⭐",
    "Be kind to yourself today — you deserve it. 🦋",
    "Believe in yourself — you have overcome challenges before. 🏆",
    "You don't have to be perfect to be wonderful. 🌸",
]

# ---------------------------------------------------------------------------
# Verified Indian Crisis Helpline Resources
# ---------------------------------------------------------------------------
CRISIS_RESOURCES: list[dict] = [
    {
        "name":        "Childline / Child Helpline India",
        "number":      "1098",
        "description": (
            "24/7 toll-free emergency phone service for children in distress. "
            "Operated under Mission Vatsalya, Ministry of Women & Child Development, "
            "Government of India."
        ),
        "emoji": "📞",
        "color": "#c0392b",
    },
    {
        "name":       "Tele-MANAS",
        "number":     "14416",
        "alt_number": "1800-891-4416",
        "description": (
            "24/7 toll-free national tele-mental health counseling service. "
            "Led by NIMHANS as the apex nodal centre under the National Mental Health "
            "Programme (NMHP), Ministry of Health and Family Welfare."
        ),
        "emoji": "🧠",
        "color": "#2980b9",
    },
    {
        "name":   "NIMHANS Child & Adolescent Guidance Services",
        "number": "+91-80-46110007",
        "description": (
            "National Institute of Mental Health and Neuro Sciences, Bengaluru. "
            "Tertiary clinical outpatient services for formal psychiatric consultation "
            "for children and adolescents."
        ),
        "emoji": "🏥",
        "color": "#8e44ad",
    },
    {
        "name":   "iCall (TISS)",
        "number": "9152987821",
        "description": (
            "Psychosocial helpline operated by the Tata Institute of Social Sciences (TISS). "
            "Provides counseling and referral services by trained psychologists "
            "(Mon–Sat, 8 AM – 10 PM)."
        ),
        "emoji": "💬",
        "color": "#16a085",
    },
]

# ---------------------------------------------------------------------------
# School Stress Level Labels
# ---------------------------------------------------------------------------
STRESS_LABELS: dict[int, str] = {
    1: "😌 Not at all stressed",
    2: "🙂 A little stressed",
    3: "😐 Somewhat stressed",
    4: "😟 Quite stressed",
    5: "😰 Very stressed",
}
