"""
Guardian / Educator Dashboard Page.

Displays longitudinal well-being trend analytics for caregivers.

Privacy Design (DPDP Act 2023, Section 9):
  - Child journal text is NEVER displayed or accessible from this view.
  - Only aggregate behavioural metrics and computed risk scores are shown.
  - No personally identifiable information (PII) is stored or presented.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.utils.storage import load_history, check_distress_alert, has_history
from src.data.schema   import RISK_TIERS


# ---------------------------------------------------------------------------
# Page Renderer
# ---------------------------------------------------------------------------

def render() -> None:
    st.markdown("## 📊 Guardian & Educator Dashboard")

    st.warning(
        "🔒 **Privacy Notice:** This dashboard shows aggregated well-being trend data only. "
        "The child's private journal entries are **never** displayed here, "
        "in accordance with DPDP Act 2023 (Section 9) privacy-by-design principles."
    )

    if not has_history():
        st.info(
            "📭 **No check-in history found yet.**\n\n"
            "Once the child completes their first daily check-in, "
            "longitudinal trend data will appear here automatically."
        )
        return

    df = load_history()
    if df.empty:
        st.info("No check-in records available.")
        return

    df = df.sort_values("timestamp", ascending=True).reset_index(drop=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Distress Alert ---
    if check_distress_alert(consecutive_threshold=3):
        st.error(
            "🚨 **DISTRESS ALERT:** This child has received an **Elevated Risk (Tier 2)** "
            "assessment for **3 or more consecutive check-ins**. "
            "Immediate caregiver attention and professional consultation are strongly recommended."
        )

    st.divider()
    _summary_metrics(df)
    st.divider()
    _mood_trend_chart(df)
    st.divider()

    col_pie, col_life = st.columns([1, 1])
    with col_pie:
        _risk_distribution_chart(df)
    with col_life:
        _lifestyle_averages(df)

    st.divider()
    if len(df) >= 4:
        _lifestyle_trend_chart(df)
        st.divider()

    _sentiment_trend_chart(df)
    st.divider()
    _recent_checkins_table(df)


# ---------------------------------------------------------------------------
# Component Renderers
# ---------------------------------------------------------------------------

def _summary_metrics(df: pd.DataFrame) -> None:
    st.markdown("### 📋 Overview")

    n            = len(df)
    avg_mood     = df["mood_score"].mean()
    avg_sleep    = df["sleep_hours"].mean()
    tier_counts  = df["risk_tier"].value_counts()
    elev_pct     = tier_counts.get(2, 0) / n * 100
    last_tier    = int(df["risk_tier"].iloc[-1])
    last_info    = RISK_TIERS[last_tier]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Check-ins",   n)
    c2.metric("Avg Mood (1–6)",    f"{avg_mood:.1f}")
    c3.metric("Avg Sleep (hrs)",   f"{avg_sleep:.1f}")
    c4.metric("Elevated Risk Days",f"{tier_counts.get(2, 0)}", delta=f"{elev_pct:.0f}% of days", delta_color="inverse")
    c5.metric(
        "Latest Status",
        f"{last_info['emoji']} Tier {last_tier}",
        delta=last_info["label"].split("/")[0].strip(),
        delta_color="normal" if last_tier == 0 else "inverse",
    )


def _mood_trend_chart(df: pd.DataFrame) -> None:
    st.markdown("### 📈 Mood Score Over Time")

    # Rolling average
    window = min(7, max(1, len(df) // 2))
    df["mood_rolling"] = df["mood_score"].rolling(window=window, min_periods=1).mean()

    tier_color_map = {0: "#27ae60", 1: "#e67e22", 2: "#c0392b"}
    marker_colors  = [tier_color_map[int(t)] for t in df["risk_tier"]]

    fig = go.Figure()

    # Coloured zones (background bands)
    fig.add_hrect(y0=0.5, y1=2.5, fillcolor="#c0392b", opacity=0.06, layer="below", line_width=0)
    fig.add_hrect(y0=2.5, y1=4.5, fillcolor="#e67e22", opacity=0.06, layer="below", line_width=0)
    fig.add_hrect(y0=4.5, y1=6.5, fillcolor="#27ae60", opacity=0.06, layer="below", line_width=0)

    # Daily mood dots
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["mood_score"],
        mode="markers+lines",
        name="Daily Mood",
        marker=dict(color=marker_colors, size=12, line=dict(width=1.5, color="white")),
        line=dict(color="#bdc3c7", width=1, dash="dot"),
    ))

    # Rolling average
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["mood_rolling"],
        mode="lines",
        name=f"{window}-Day Rolling Avg",
        line=dict(color="#2980b9", width=3),
    ))

    fig.update_layout(
        yaxis=dict(title="Mood Score (1=Low → 6=High)", range=[0.5, 6.5], dtick=1),
        xaxis_title="Date",
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(245,246,250,1)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "🟢 Green = Low Risk  |  🟡 Yellow = Moderate  |  🔴 Red = Elevated Risk  "
        f"|  Blue line = {window}-day rolling average"
    )


def _risk_distribution_chart(df: pd.DataFrame) -> None:
    st.markdown("### 🥧 Risk Tier Distribution")

    tier_counts  = df["risk_tier"].value_counts().sort_index()
    labels       = [RISK_TIERS[t]["label"] for t in tier_counts.index]
    colors       = [RISK_TIERS[t]["color"] for t in tier_counts.index]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=tier_counts.values,
        marker_colors=colors,
        hole=0.42,
        textinfo="percent+label",
        textfont=dict(size=13),
    ))
    fig.update_layout(
        height=300,
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def _lifestyle_averages(df: pd.DataFrame) -> None:
    st.markdown("### 📊 Average Lifestyle Metrics")

    metrics = {
        "🌙 Sleep (hrs)":        df["sleep_hours"].mean(),
        "📱 Screen Time (hrs)":  df["screen_time"].mean(),
        "🏃 Physical Play (hrs)":df["physical_play"].mean(),
        "📚 School Stress (1–5)":df["school_stress"].mean(),
    }
    for label, val in metrics.items():
        st.metric(label, f"{val:.1f}")


def _lifestyle_trend_chart(df: pd.DataFrame) -> None:
    st.markdown("### 🔗 Lifestyle Factor Trends")

    fig = go.Figure()
    traces = [
        ("sleep_hours",   "🌙 Sleep (hrs)",          "#2980b9",  "solid"),
        ("screen_time",   "📱 Screen Time (hrs)",    "#c0392b",  "solid"),
        ("physical_play", "🏃 Physical Play (hrs)",  "#27ae60",  "solid"),
        ("school_stress", "📚 School Stress (1–5)",  "#8e44ad",  "dash"),
    ]
    for col, name, color, dash in traces:
        fig.add_trace(go.Scatter(
            x=df["timestamp"], y=df[col],
            name=name,
            line=dict(color=color, width=2, dash=dash),
        ))

    fig.update_layout(
        height=340,
        xaxis_title="Date",
        yaxis_title="Value",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(245,246,250,1)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def _sentiment_trend_chart(df: pd.DataFrame) -> None:
    has_sentiment = "sentiment_compound" in df.columns and df["sentiment_compound"].notna().any()
    if not has_sentiment:
        return

    df_sent = df[df["sentiment_compound"].notna() & (df["sentiment_compound"] != 0.0)]
    if df_sent.empty:
        return

    st.markdown("### 📝 Journal Sentiment Trend")

    colors = df_sent["sentiment_compound"].apply(
        lambda s: "#27ae60" if s >= 0.05 else ("#c0392b" if s <= -0.05 else "#7f8c8d")
    )

    fig = go.Figure(go.Bar(
        x=df_sent["timestamp"],
        y=df_sent["sentiment_compound"],
        marker_color=colors,
        name="Sentiment Score",
    ))
    fig.add_hline(y=0.05,  line_dash="dot", line_color="#27ae60", annotation_text="Positive threshold")
    fig.add_hline(y=-0.05, line_dash="dot", line_color="#c0392b", annotation_text="Negative threshold")

    fig.update_layout(
        yaxis=dict(title="Compound Sentiment Score", range=[-1.05, 1.05]),
        xaxis_title="Date",
        height=280,
        plot_bgcolor="rgba(245,246,250,1)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("⚕️ Sentiment scores are linguistic measures only — NOT psychiatric evaluations.")


def _recent_checkins_table(df: pd.DataFrame) -> None:
    st.markdown("### 📅 Recent Check-ins (Last 10)")

    display_cols = [
        "timestamp", "mood_label", "sleep_hours", "screen_time",
        "physical_play", "school_stress", "risk_label", "sentiment_tone",
    ]
    available = [c for c in display_cols if c in df.columns]

    df_disp = df.sort_values("timestamp", ascending=False).head(10)[available].copy()
    df_disp["timestamp"] = df_disp["timestamp"].dt.strftime("%Y-%m-%d  %H:%M")

    rename = {
        "timestamp":        "Date / Time",
        "mood_label":       "Mood",
        "sleep_hours":      "Sleep (hrs)",
        "screen_time":      "Screen (hrs)",
        "physical_play":    "Play (hrs)",
        "school_stress":    "Stress (1–5)",
        "risk_label":       "Well-being Status",
        "sentiment_tone":   "Journal Tone",
    }
    df_disp.rename(columns=rename, inplace=True)

    st.dataframe(df_disp, use_container_width=True, hide_index=True)
