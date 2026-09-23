"""
Coping Toolkit Page.

Three evidence-aligned psychoeducational tools:
  1. 4-7-8 Breathing Pacer — animated HTML/JS circle (parasympathetic activation)
  2. 5-4-3-2-1 Grounding Exercise — sensory awareness for present-moment anchoring
  3. Affirmation Cards — positive self-talk cards with rotation

These are non-clinical psychoeducational exercises only, not therapeutic interventions.
"""

import streamlit as st
import streamlit.components.v1 as components
from src.data.schema import AFFIRMATIONS

# ---------------------------------------------------------------------------
# 4-7-8 Breathing Pacer — HTML/CSS/JavaScript
# ---------------------------------------------------------------------------
_BREATHING_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 460px;
    background: transparent;
    padding: 20px;
    gap: 16px;
  }

  .phase-text {
    font-size: 26px;
    font-weight: 700;
    color: #2c3e50;
    text-align: center;
    min-height: 36px;
    letter-spacing: 0.5px;
  }

  .count-text {
    font-size: 52px;
    font-weight: 900;
    color: #2980b9;
    min-height: 68px;
    text-align: center;
    font-variant-numeric: tabular-nums;
  }

  .circle-container {
    width: 200px;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .breath-circle {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #74b9ff, #0984e3);
    box-shadow: 0 0 30px rgba(9, 132, 227, 0.35), 0 0 60px rgba(9, 132, 227, 0.15);
    transition: width 0.4s ease, height 0.4s ease, background 0.6s ease, box-shadow 0.6s ease;
  }

  .instruction-text {
    font-size: 15px;
    color: #636e72;
    text-align: center;
    max-width: 310px;
    line-height: 1.55;
    font-style: italic;
    min-height: 44px;
  }

  .cycles-text {
    font-size: 13px;
    color: #b2bec3;
    text-align: center;
    min-height: 20px;
  }

  .btn {
    padding: 13px 36px;
    font-size: 16px;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    font-weight: 700;
    letter-spacing: 0.5px;
    transition: transform 0.15s ease, opacity 0.15s ease;
    outline: none;
  }
  .btn:active { transform: scale(0.96); }
  .btn:hover  { opacity: 0.88; }
  .btn-start  { background: #0984e3; color: #fff; }
  .btn-stop   { background: #d63031; color: #fff; }
</style>
</head>
<body>

<div class="phase-text"  id="phaseText">Press Start to Begin</div>
<div class="count-text"  id="countText">–</div>
<div class="circle-container">
  <div class="breath-circle" id="circle"></div>
</div>
<div class="instruction-text" id="instrText">
  Inhale for <strong>4</strong> seconds &rarr;
  Hold for <strong>7</strong> seconds &rarr;
  Exhale for <strong>8</strong> seconds
</div>
<div class="cycles-text" id="cyclesText"></div>
<button class="btn btn-start" id="mainBtn" onclick="toggle()">▶ Start Breathing</button>

<script>
const phases = [
  {
    name: "🫁 Inhale",
    dur: 4,
    instruction: "Breathe in slowly and deeply through your nose…",
    bg: "radial-gradient(circle at 35% 35%, #74b9ff, #0984e3)",
    shadow: "0 0 35px rgba(9,132,227,0.45), 0 0 70px rgba(9,132,227,0.2)",
    size: 175
  },
  {
    name: "⏸️ Hold",
    dur: 7,
    instruction: "Hold your breath gently. Stay still and calm…",
    bg: "radial-gradient(circle at 35% 35%, #55efc4, #00b894)",
    shadow: "0 0 35px rgba(0,184,148,0.45), 0 0 70px rgba(0,184,148,0.2)",
    size: 175
  },
  {
    name: "💨 Exhale",
    dur: 8,
    instruction: "Breathe out slowly through your mouth. Let it all go…",
    bg: "radial-gradient(circle at 35% 35%, #fd79a8, #e84393)",
    shadow: "0 0 35px rgba(232,67,147,0.35), 0 0 70px rgba(232,67,147,0.15)",
    size: 90
  }
];

let phase = 0, timeLeft = 0, running = false, timer = null, cycles = 0;

function toggle() {
  running ? stop() : start();
}

function start() {
  running = true; cycles = 0; phase = 0;
  document.getElementById("mainBtn").textContent = "⏹ Stop";
  document.getElementById("mainBtn").className = "btn btn-stop";
  beginPhase();
}

function stop() {
  running = false;
  clearInterval(timer);
  document.getElementById("phaseText").textContent = "Great job! You did " + cycles + " cycle(s).";
  document.getElementById("countText").textContent = "✅";
  document.getElementById("instrText").textContent = "Notice how you feel now. Calmer? More grounded?";
  document.getElementById("cyclesText").textContent = "";
  document.getElementById("mainBtn").textContent = "▶ Start Again";
  document.getElementById("mainBtn").className = "btn btn-start";
  const c = document.getElementById("circle");
  c.style.width = c.style.height = "90px";
  c.style.background = "radial-gradient(circle at 35% 35%, #74b9ff, #0984e3)";
  c.style.boxShadow = "0 0 30px rgba(9,132,227,0.35)";
}

function beginPhase() {
  if (!running) return;
  const p = phases[phase];
  timeLeft = p.dur;
  document.getElementById("phaseText").textContent = p.name;
  document.getElementById("instrText").textContent = p.instruction;
  const c = document.getElementById("circle");
  c.style.width = c.style.height = p.size + "px";
  c.style.background  = p.bg;
  c.style.boxShadow   = p.shadow;
  tick();
  timer = setInterval(tick, 1000);
}

function tick() {
  document.getElementById("countText").textContent = timeLeft;
  if (timeLeft-- > 0) return;
  clearInterval(timer);
  phase = (phase + 1) % phases.length;
  if (phase === 0) {
    cycles++;
    document.getElementById("cyclesText").textContent = "Completed: " + cycles + " cycle(s)";
  }
  setTimeout(() => { if (running) beginPhase(); }, 350);
}
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Grounding Steps
# ---------------------------------------------------------------------------
_GROUNDING_STEPS: list[tuple[str, str, str]] = [
    (
        "👁️ 5 Things You Can SEE",
        "Look around slowly. Name 5 things you can see right now.",
        "Maybe a wall, a book, your hands, a window, or a light.",
    ),
    (
        "🤚 4 Things You Can TOUCH",
        "Touch 4 different objects near you. Notice the texture.",
        "Smooth, rough, soft, cold — just notice without judging.",
    ),
    (
        "👂 3 Things You Can HEAR",
        "Listen carefully. Identify 3 sounds in your environment.",
        "Maybe distant traffic, your own breathing, birds, or music.",
    ),
    (
        "👃 2 Things You Can SMELL",
        "Notice 2 scents around you right now.",
        "Fresh air, soap, food, pencils — anything you can detect.",
    ),
    (
        "👅 1 Thing You Can TASTE",
        "Notice 1 taste in your mouth.",
        "Water, toothpaste, or simply nothing — that's fine too!",
    ),
]


# ---------------------------------------------------------------------------
# Page Renderer
# ---------------------------------------------------------------------------

def render() -> None:
    st.markdown("## 🌬️ Coping Toolkit")
    st.markdown(
        "*These activities are designed to help you feel calmer and more grounded. "
        "Try whichever feels right for you today.* 💙"
    )

    tab1, tab2, tab3 = st.tabs([
        "🫁 4-7-8 Breathing",
        "🌿 Grounding Exercise",
        "💙 Affirmations",
    ])

    with tab1:
        _render_breathing()

    with tab2:
        _render_grounding()

    with tab3:
        _render_affirmations()


# ---------------------------------------------------------------------------
# Tab Renderers
# ---------------------------------------------------------------------------

def _render_breathing() -> None:
    st.markdown("### 🫁 4-7-8 Breathing Pacer")
    st.markdown("""
    The **4-7-8 technique** activates the parasympathetic nervous system,
    helping to calm racing thoughts and reduce anxiety.

    | Phase | Duration | What to do |
    |---|---|---|
    | **Inhale** | 4 seconds | Breathe in through your nose |
    | **Hold** | 7 seconds | Hold your breath gently |
    | **Exhale** | 8 seconds | Breathe out through your mouth |
    """)

    components.html(_BREATHING_HTML, height=490, scrolling=False)

    st.info(
        "💡 **Tip:** Aim for 3–4 complete cycles for best effect. "
        "You can use this technique anytime you feel anxious, overwhelmed, or find it hard to sleep."
    )


def _render_grounding() -> None:
    st.markdown("### 🌿 5-4-3-2-1 Grounding Exercise")
    st.markdown(
        "This technique uses your **five senses** to bring your attention to the "
        "present moment — helping to reduce anxiety and racing thoughts."
    )

    if not st.session_state.get("grounding_started"):
        st.markdown("*Take three slow breaths, then click Start when you are ready.*")
        if st.button("🌿 Start Grounding Exercise", type="primary"):
            st.session_state.grounding_started = True
            st.session_state.grounding_step    = 0
            st.rerun()
        return

    step  = st.session_state.grounding_step
    total = len(_GROUNDING_STEPS)

    # --- Completed ---
    if step >= total:
        st.success(
            "🎉 **Well done!** You have completed all 5 steps of the grounding exercise."
        )
        st.markdown("""
        Take a moment to notice how you feel now compared to when you started.
        Regular practice strengthens this technique — use it anytime, anywhere.
        """)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Do it again", use_container_width=True):
                st.session_state.grounding_step = 0
                st.rerun()
        with c2:
            if st.button("✅ I'm done", use_container_width=True):
                st.session_state.grounding_started = False
                st.session_state.grounding_step    = 0
                st.rerun()
        return

    # --- Active step ---
    st.progress(step / total, text=f"Step {step + 1} of {total}")

    title, main_instr, sub_instr = _GROUNDING_STEPS[step]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #667eea18, #764ba218);
            border: 2px solid #667eea44;
            border-radius: 16px;
            padding: 28px 30px;
            text-align: center;
            margin: 14px 0;
        ">
            <h2 style="color: #2c3e50; margin: 0 0 14px 0;">{title}</h2>
            <p style="font-size: 18px; color: #444; margin: 0 0 8px 0; font-weight: 500;">
                {main_instr}
            </p>
            <p style="font-size: 14px; color: #777; font-style: italic; margin: 0;">
                {sub_instr}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("*Take your time. When you are ready, move to the next step.*")

    nav_l, nav_r = st.columns([1, 3])
    with nav_l:
        if step > 0:
            if st.button("◀ Back", use_container_width=True):
                st.session_state.grounding_step -= 1
                st.rerun()
    with nav_r:
        if st.button("Next Step ➡️", type="primary", use_container_width=True):
            st.session_state.grounding_step += 1
            st.rerun()


def _render_affirmations() -> None:
    st.markdown("### 💙 Positive Affirmation Cards")
    st.markdown(
        "*Affirmations are positive statements that help shift your mindset. "
        "Read them slowly and let the words sink in.* ✨"
    )

    idx        = st.session_state.get("affirmation_index", 0)
    affirmation = AFFIRMATIONS[idx % len(AFFIRMATIONS)]

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #a29bfe, #6c5ce7, #fd79a8);
            border-radius: 22px;
            padding: 44px 36px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(108, 92, 231, 0.25);
        ">
            <p style="
                font-size: 22px;
                color: #fff;
                font-weight: 700;
                line-height: 1.65;
                margin: 0;
                text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
            ">{affirmation}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("✨ Next Affirmation", type="primary", use_container_width=True):
            st.session_state.affirmation_index = (idx + 1) % len(AFFIRMATIONS)
            st.rerun()

    st.markdown("---")
    st.info("💡 **Tip:** Read your favourite affirmation out loud, 3 times, slowly — first thing in the morning.")
    st.markdown("""
    **How to make affirmations work for you:**
    - 📖 Say them out loud in a calm, quiet moment
    - 🔄 Repeat your favourite one throughout the day
    - 📝 Write it on a sticky note and put it somewhere you'll see it
    - 🌅 Use them first thing in the morning or just before bed
    """)
