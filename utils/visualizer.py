"""
visualizer.py
All Plotly charts used in the Streamlit dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px


# ──────────────────────────────────────────────────────────────
# COLOR PALETTE
# ──────────────────────────────────────────────────────────────
C_GREEN  = "#22c55e"
C_ORANGE = "#f97316"
C_RED    = "#ef4444"
C_BLUE   = "#3b82f6"
C_PURPLE = "#8b5cf6"
C_DARK   = "#1e293b"
C_CARD   = "#0f172a"


def score_gauge(score: float, title: str = "Match Score") -> go.Figure:
    """Speedometer-style gauge for any 0-100 score."""
    if score >= 75:
        color = C_GREEN
    elif score >= 50:
        color = C_ORANGE
    else:
        color = C_RED

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        title={"text": title, "font": {"size": 16, "color": "white"}},
        delta={"reference": 70, "increasing": {"color": C_GREEN},
               "decreasing": {"color": C_RED}},
        number={"suffix": "%", "font": {"size": 30, "color": "white"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "white",
                     "tickfont": {"color": "white"}},
            "bar":  {"color": color, "thickness": 0.3},
            "bgcolor": C_DARK,
            "bordercolor": "#334155",
            "steps": [
                {"range": [0,  35], "color": "#1c0a0a"},
                {"range": [35, 65], "color": "#1c1208"},
                {"range": [65, 85], "color": "#0a1c10"},
                {"range": [85,100], "color": "#0a1a0a"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 2},
                "thickness": 0.75,
                "value": 70,
            },
        },
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


def skills_bar_chart(matched: list, missing: list) -> go.Figure:
    """Horizontal bar showing matched vs missing skills count."""
    categories = ["Matched Skills", "Missing Skills"]
    values     = [len(matched), len(missing)]
    colors     = [C_GREEN, C_RED]

    fig = go.Figure(go.Bar(
        x=values,
        y=categories,
        orientation="h",
        marker_color=colors,
        text=values,
        textposition="inside",
        textfont={"color": "white", "size": 14},
    ))
    fig.update_layout(
        title={"text": "Skill Coverage", "font": {"color": "white", "size": 14}},
        xaxis={"showgrid": False, "color": "white"},
        yaxis={"color": "white"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=180,
        margin=dict(l=10, r=20, t=40, b=20),
        font={"color": "white"},
    )
    return fig


def score_breakdown_radar(
    match_score: float,
    skill_pct: float,
    ats_rate: float,
) -> go.Figure:
    """Radar / spider chart for the 3 scoring dimensions."""
    categories = ["Content Match", "Skill Alignment", "ATS Optimization"]
    values     = [match_score, skill_pct, ats_rate]

    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(59, 130, 246, 0.25)",
        line={"color": C_BLUE, "width": 2},
        marker={"color": C_BLUE, "size": 6},
    ))
    fig.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "color": "#64748b",
                "gridcolor": "#334155",
            },
            "angularaxis": {"color": "white"},
            "bgcolor": "rgba(0,0,0,0)",
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=40, r=40, t=40, b=40),
        font={"color": "white"},
        showlegend=False,
    )
    return fig


def ats_donut(hit_rate: float) -> go.Figure:
    """Donut chart showing ATS hit rate vs miss rate."""
    fig = go.Figure(go.Pie(
        values=[hit_rate, 100 - hit_rate],
        labels=["Keywords Found", "Keywords Missing"],
        hole=0.65,
        marker_colors=[C_PURPLE, "#334155"],
        textinfo="none",
    ))
    fig.add_annotation(
        text=f"{hit_rate}%",
        x=0.5, y=0.5,
        font={"size": 26, "color": "white"},
        showarrow=False,
    )
    fig.update_layout(
        title={"text": "ATS Keyword Hit Rate", "font": {"color": "white", "size": 14}},
        paper_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": "white"}},
        height=260,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def skill_tags_html(skills: list, color: str = "#22c55e") -> str:
    """Return HTML for colored skill pill badges."""
    bg = {
        "#22c55e": "rgba(34,197,94,0.15)",
        "#ef4444": "rgba(239,68,68,0.15)",
        "#3b82f6": "rgba(59,130,246,0.15)",
        "#f97316": "rgba(249,115,22,0.15)",
    }.get(color, "rgba(255,255,255,0.1)")

    tags = " ".join(
        f'<span style="background:{bg};color:{color};border:1px solid {color}33;'
        f'padding:3px 10px;border-radius:20px;font-size:12px;margin:3px 2px;'
        f'display:inline-block;">{s}</span>'
        for s in skills
    )
    return tags if tags else '<span style="color:#64748b;font-size:13px;">None detected</span>'
