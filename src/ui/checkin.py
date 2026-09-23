"""
Child Daily Check-in Page.

Provides a child-friendly interface with:
  - Emoji mood picker (6 primary affective states)
  - Lifestyle parameter sliders (sleep, screen time, play, stress)
  - Optional reflective journal textarea (text NOT stored)
  - ML risk tier prediction display
  - VADER sentiment analysis display
  - Navigation links to coping tools and crisis resources

Design principles from Phase 1 literature:
  - Low-cognitive-load visual interactions (Hollis et al., 2017)
  - Age-appropriate emoji-based input (Grist et al., 2017)
  - Non-stigmatising, encouraging language throughout
"""

import random
import streamlit as st

from src.data.schema  import MOOD_LABELS, RISK_TIERS, AFFIRMATIONS, STRESS_LABELS
from src.ml.predict   import predict
from src.nlp.sentiment import analyze_sentiment
from src.utils.storage import save_checkin
from src.utils.session import set_last_checkin


# ---------------------------------------------------------------------------
# Page Renderer
# ---------------------------------------------------------------------------

def render() -> None:
    st.markdown("## 😊 Daily Well-being Check-in")
    st.markdown(
        "*Take a moment to check in with yourself. "
        "There are no right or wrong answers — just be honest!* 🌟"
    )
    st.divider()

    _mood_section()
    st.divider()
    sleep_hours, screen_time, physical_play, school_stress = _lifestyle_section()
    st.divider()
    journal_text = _journal_section()
    st.divider()
    _submit_section(sleep_hours, screen_time, physical_play, school_stress, journal_text)


# ---------------------------------------------------------------------------
# Section Renderers
# ---------------------------------------------------------------------------

def _mood_section() -> None:
    st.markdown("### 1️⃣ How are you feeling right now?")
    st.markdown("*Tap the emoji that best matches your mood:*")

    emoji_items = list(MOOD_LABELS.items())  # [(label, score), …]

    cols = st.columns(6)
    for i, (label, _score) in enumerate(emoji_items):
        emoji, text = label.split(" ", 1)
        is_selected = st.session_state.get("selected_mood") == label
        with cols[i]:
            st.button(
                f"{emoji}\n{text}",
                key=f"mood_btn_{i}",
                type="primary" if is_selected else "secondary",
                use_container_width=True,
                on_click=_select_mood,
                args=(label,),
            )

    if st.session_state.get("selected_mood"):
        st.success(f"✅ Selected: **{st.session_state.selected_mood}**")
    else:
        st.info("👆 Please tap one of the emojis above.")


def _select_mood(label: str) -> None:
    st.session_state.selected_mood = label


def _lifestyle_section() -> tuple:
    st.markdown("### 2️⃣ Tell us about your day:")

    col1, col2 = st.columns(2)

    with col1:
        sleep_hours = st.slider(
            "🌙 How many hours did you sleep last night?",
            min_value=4.0, max_value=12.0, value=8.0, step=0.5,
            help="WHO recommends 9–11 hours for school-age children.",
        )
        screen_time = st.slider(
            "📱 How many hours did you spend on screens today?",
            min_value=0.0, max_value=8.0, value=2.0, step=0.5,
            help="Includes phone, TV, video games, and computers.",
        )

    with col2:
        physical_play = st.slider(
            "🏃 How many hours did you play or exercise today?",
            min_value=0.0, max_value=4.0, value=1.0, step=0.5,
            help="Any physical activity: sports, running, dancing, outdoor play.",
        )
        school_stress = st.slider(
            "📚 How stressed did school make you feel today?",
            min_value=1, max_value=5, value=2,
            help="1 = Not stressed at all  |  5 = Very stressed",
        )

    st.caption(f"School stress: **{STRESS_LABELS[school_stress]}**")

    return sleep_hours, screen_time, physical_play, school_stress


def _journal_section() -> str:
    st.markdown("### 3️⃣ ✏️ Anything you want to share? *(optional)*")
    st.markdown(
        "*This is your private space. Write anything you're thinking or feeling. "
        "It's completely optional and helps us understand your mood better.*"
    )
    return st.text_area(
        "Your thoughts…",
        height=130,
        placeholder=(
            "Today I felt… Something that made me happy was… "
            "Something that worried me was…"
        ),
        label_visibility="collapsed",
    )


def _submit_section(
    sleep_hours: float,
    screen_time: float,
    physical_play: float,
    school_stress: int,
    journal_text: str,
) -> None:
    if not st.button("✅ Submit My Check-in", type="primary", use_container_width=True):
        return

    if not st.session_state.get("selected_mood"):
        st.error("⚠️ Please select your mood emoji before submitting!")
        return

    mood_label = st.session_state.selected_mood
    mood_score = MOOD_LABELS[mood_label]

    with st.spinner("🔍 Analysing your check-in…"):
        prediction = predict(
            mood_score=mood_score,
            sleep_hours=sleep_hours,
            screen_time=screen_time,
            physical_play=physical_play,
            school_stress=school_stress,
        )
        sentiment = analyze_sentiment(journal_text)

    # Build storage record (journal text excluded — never persisted)
    record = {
        "mood_label":         mood_label,
        "mood_score":         mood_score,
        "sleep_hours":        sleep_hours,
        "screen_time":        screen_time,
        "physical_play":      physical_play,
        "school_stress":      school_stress,
        "sentiment_compound": sentiment["compound"],
        "sentiment_tone":     sentiment["tone_tag"],
        "risk_tier":          prediction["risk_tier"],
        "risk_label":         prediction["risk_label"],
    }

    save_checkin(record)
    set_last_checkin({**record, "sentiment": sentiment, "prediction": prediction})

    _show_results(prediction, sentiment, journal_text)


# ---------------------------------------------------------------------------
# Results Display
# ---------------------------------------------------------------------------

def _show_results(prediction: dict, sentiment: dict, journal_text: str) -> None:
    tier      = prediction["risk_tier"]
    tier_info = RISK_TIERS[tier]

    st.markdown("---")
    st.markdown("## 📊 Your Well-being Assessment")

    # --- Risk Tier Card ---
    st.markdown(
        f"""
        <div style="
            border-left: 6px solid {tier_info['color']};
            background:  {tier_info['bg_color']};
            border-radius: 10px;
            padding: 18px 22px;
            margin: 10px 0 18px 0;
        ">
            <h3 style="color: {tier_info['color']}; margin: 0 0 8px 0;">
                {tier_info['emoji']} Well-being Status: {tier_info['label']}
            </h3>
            <p style="margin: 4px 0; font-size: 16px;">{tier_info['description']}</p>
            <p style="margin: 6px 0 0 0; font-style: italic; color: #555;">
                💡 {tier_info['action']}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Probability Breakdown ---
    with st.expander("📈 View detailed probability breakdown & factor analysis"):
        for label, prob in sorted(prediction["probabilities"].items(), key=lambda x: -x[1]):
            col_lbl, col_bar = st.columns([1, 3])
            with col_lbl:
                st.markdown(f"**{label.split('/')[0].strip()}**")
            with col_bar:
                st.progress(float(prob), text=f"{prob * 100:.1f}%")

        st.divider()

        from src.ml.explainer import explain_prediction, plot_feature_importance
        explanation = explain_prediction(prediction["feature_vector"], tier)
        st.markdown(f"🔍 **Factor Summary:** {explanation}")

        fig = plot_feature_importance()
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # --- NLP Sentiment (only if journal entry provided) ---
    if journal_text.strip():
        st.markdown("### 📝 Journal Sentiment Analysis")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(
                f"""
                <div style="
                    text-align: center;
                    padding: 15px;
                    border-radius: 10px;
                    background: {sentiment['tone_color']}22;
                    border: 2px solid {sentiment['tone_color']};
                ">
                    <div style="font-size: 40px;">{sentiment['tone_emoji']}</div>
                    <div style="font-size: 20px; font-weight: bold; color: {sentiment['tone_color']};">
                        {sentiment['tone_tag']}
                    </div>
                    <div style="font-size: 14px; color: #555;">
                        Score: {sentiment['compound']:+.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("""
            **About this score:**

            The sentiment analyser reads the *emotional tone* of the words you
            used in your journal entry.

            - **+1.0** = Very positive language
            - **0.0**  = Neutral language
            - **−1.0** = Very negative language

            > ⚕️ *This is a linguistic measure, NOT a medical or psychiatric evaluation.*
            """)

    # --- Affirmation ---
    st.divider()
    affirmation = random.choice(AFFIRMATIONS)
    st.info(f"💙 **Daily Affirmation:** {affirmation}")

    # --- Navigation ---
    if tier >= 1:
        st.markdown("### 🌬️ Would you like some support right now?")
        if st.button("🌬️ Open Coping Toolkit", type="primary", use_container_width=True):
            st.session_state.current_page = "🌬️ Coping Tools"
            st.rerun()

    if tier >= 2:
        st.error(
            "🆘 **Important:** If you feel very upset or unsafe, "
            "please tell a trusted adult immediately, or call "
            "**Childline 1098** (toll-free, 24/7)."
        )
        if st.button("🆘 View Crisis Resources →", use_container_width=True):
            st.session_state.current_page = "🆘 Crisis Resources"
            st.rerun()
