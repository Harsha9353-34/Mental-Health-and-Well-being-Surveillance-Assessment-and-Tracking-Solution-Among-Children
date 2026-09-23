"""
Crisis Support & Referral Resources Page.

Displays verified Indian national helplines, step-by-step emergency
protocol, and key warning signs for caregivers.

All contact information is verified as of September 2026.
Always confirm availability directly with the helpline provider.

DISCLAIMER:
    This platform does not provide clinical crisis intervention.
    In any acute or life-threatening situation, contact emergency
    services (112) immediately.
"""

import streamlit as st
from src.data.schema import CRISIS_RESOURCES


# ---------------------------------------------------------------------------
# Page Renderer
# ---------------------------------------------------------------------------

def render() -> None:
    st.markdown("## 🆘 Crisis Support & Helpline Resources")

    st.error(
        "⚠️ **IMMEDIATE DANGER?** If a child is in immediate danger or a "
        "life-threatening situation, **call Emergency Services: 112** right now. "
        "Do not wait."
    )

    st.markdown("""
    The following verified helplines provide free, confidential, and professional
    support for children and families in distress. All numbers marked **toll-free**
    can be dialled without any call charges.
    """)

    st.divider()

    _helpline_cards()
    st.divider()
    _emergency_protocol()
    st.divider()
    _warning_signs()
    st.divider()
    _disclaimer()


# ---------------------------------------------------------------------------
# Component Renderers
# ---------------------------------------------------------------------------

def _helpline_cards() -> None:
    st.markdown("### 📞 Verified National Helplines")

    for r in CRISIS_RESOURCES:
        alt = f"  /  **{r['alt_number']}**" if "alt_number" in r else ""

        st.markdown(
            f"""
            <div style="
                border: 2px solid {r['color']};
                border-radius: 14px;
                padding: 18px 22px;
                margin: 12px 0;
                background: {r['color']}0e;
            ">
                <h3 style="color: {r['color']}; margin: 0 0 6px 0; font-size: 19px;">
                    {r['emoji']} &nbsp; {r['name']}
                </h3>
                <p style="font-size: 26px; font-weight: 900; margin: 4px 0; color: #1a252f; letter-spacing: 1px;">
                    📲 &nbsp; {r['number']}{alt}
                </p>
                <p style="color: #555; margin: 6px 0 0 0; font-size: 14.5px; line-height: 1.55;">
                    {r['description']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _emergency_protocol() -> None:
    st.markdown("### 🛡️ What To Do In a Crisis — Step-by-Step Protocol")

    steps = [
        (
            "🚨 Step 1: Stay Calm",
            "Take a slow breath. Your calm presence is critical — it helps the child "
            "feel safer and more able to communicate. Do not panic or raise your voice.",
        ),
        (
            "👥 Step 2: Do Not Leave the Child Alone",
            "Stay with the child or ensure a trusted and familiar adult is present "
            "at all times until the situation is resolved.",
        ),
        (
            "👂 Step 3: Listen Without Judgment",
            "Allow the child to express themselves fully. Avoid dismissing, minimising, "
            "or immediately problem-solving. Active, empathetic listening is the priority.",
        ),
        (
            "📞 Step 4: Contact a Helpline",
            "Call **Childline 1098** or **Tele-MANAS 14416** for immediate, confidential "
            "guidance from trained mental health professionals available 24/7.",
        ),
        (
            "🏥 Step 5: Arrange Professional Consultation",
            "Schedule an appointment with a qualified paediatrician, licensed child "
            "psychologist, or psychiatrist. NIMHANS (+91-80-46110007) provides specialist "
            "child and adolescent outpatient services.",
        ),
        (
            "📝 Step 6: Document and Follow Up",
            "Keep brief written notes of observed behavioural changes, dates, and actions taken. "
            "Follow up with the mental health professional at all recommended intervals.",
        ),
    ]

    for title, description in steps:
        with st.expander(title, expanded=False):
            st.markdown(description)


def _warning_signs() -> None:
    st.markdown("### ⚠️ Warning Signs to Watch For")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🧠 Behavioural Signs:**
        - Sudden withdrawal from friends, family, or activities
        - Drastic decline in school attendance or academic performance
        - Giving away prized or meaningful possessions
        - Talking about feeling hopeless, worthless, or like a burden
        - Visible self-harm marks, bruises, or unexplained injuries
        - Extreme irritability, aggression, or sudden mood swings
        """)

    with col2:
        st.markdown("""
        **🏥 Physical Signs:**
        - Significant and unexplained changes in sleep (too much or too little)
        - Notable changes in appetite or weight
        - Persistent headaches, stomachaches, or physical complaints without clear cause
        - Extreme fatigue, loss of energy, or inability to concentrate
        - Neglect of personal hygiene or appearance
        - Substance use or risky behaviours
        """)


def _disclaimer() -> None:
    st.markdown(
        """
        > ⚕️ **Medical & Ethical Disclaimer**
        >
        > This platform is a **non-clinical academic prototype** developed for educational
        > well-being surveillance research at Presidency University, Bengaluru.
        >
        > - It does **NOT** provide clinical crisis intervention, psychiatric diagnosis, or therapy.
        > - All helpline numbers are verified as of September 2026. Always confirm availability directly.
        > - In all psychiatric emergencies, immediately contact qualified healthcare professionals
        >   and/or emergency services (**112**).
        >
        > *Team: Harsha R (20231CSE0261) · Arjun M (20231CSE0277) · Abhishek MR (20231CSE0268)*
        > *Guide: Mr. Jetti Satya Sai Kumar | Presidency University, Bengaluru*
        """
    )
