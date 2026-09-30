"""Gráficos Altair com a paleta do app (categórica validada para daltonismo)."""

import altair as alt
import pandas as pd

BLUE = "#2a78d6"      # série 1
ORANGE = "#eb6834"    # série 2
AQUA = "#1baf7a"      # série 3
YELLOW = "#eda100"    # série 4
CRITICAL = "#d03b3b"  # status: fora da tolerância
GRID = "#E3E9F1"
SURFACE = "#F7F9FC"   # fundo do app (anel entre marcas sobrepostas)
INK = "#0B1B2E"
INK_2 = "#5B6B80"


def _style(chart: alt.Chart) -> alt.Chart:
    return (
        chart.configure(font="Inter, Segoe UI, sans-serif")
        .configure_axis(gridColor=GRID, domainColor="#C4CFDD", labelColor=INK_2, titleColor=INK_2,
                        tickColor="#C4CFDD", labelFontSize=12, titleFontSize=12, titleFontWeight=600)
        .configure_legend(orient="top", labelColor=INK_2, titleColor=INK_2, labelFontSize=12)
        .configure_view(strokeWidth=0)
    )


def dimension_comparison(df: pd.DataFrame, bar: str = "Sua instituição", tick: str = "Média da pesquisa",
                         target: str | None = "Meta do porte") -> alt.Chart:
    """df: Dimensão + coluna da barra, coluna do traço e (opcional) coluna da meta."""
    long = df.melt("Dimensão", var_name="Série", value_name="Score")
    color = alt.Color("Série:N", title=None, scale=alt.Scale(domain=[bar, tick], range=[BLUE, ORANGE]))
    y = alt.Y("Dimensão:N", title=None, sort=list(df["Dimensão"]), axis=alt.Axis(labelLimit=260))
    x = alt.X("Score:Q", title="Score (0–100)", scale=alt.Scale(domain=[0, 100]))
    tooltip = [alt.Tooltip("Dimensão:N"), alt.Tooltip("Série:N"), alt.Tooltip("Score:Q", format=".0f")]

    base = alt.Chart(long)
    bars = base.transform_filter(alt.datum["Série"] == bar).mark_bar(
        height=18, cornerRadiusEnd=4).encode(x=x, y=y, color=color, tooltip=tooltip)
    labels = base.transform_filter(alt.datum["Série"] == bar).mark_text(
        align="left", dx=6, color=INK).encode(x=x, y=y, text=alt.Text("Score:Q", format=".0f"))
    ticks = base.transform_filter(alt.datum["Série"] == tick).mark_tick(
        thickness=3, size=28).encode(x=x, y=y, color=color, tooltip=tooltip)
    layers = bars + labels + ticks
    if target:
        layers += base.transform_filter(alt.datum["Série"] == target).mark_rule(
            strokeDash=[4, 3], color=INK_2, strokeWidth=2).encode(
            x=alt.X("mean(Score):Q"), tooltip=[alt.Tooltip("mean(Score):Q", title=target, format=".0f")])
    return _style(layers.properties(height=240))


def score_trend(df: pd.DataFrame, target: float) -> alt.Chart:
    """df: Rótulo, Score (em ordem cronológica)."""
    x = alt.X("Rótulo:N", sort=list(df["Rótulo"]), title=None, axis=alt.Axis(labelAngle=0))
    y = alt.Y("Score:Q", title="Score geral (0–100)", scale=alt.Scale(domain=[0, 100]))
    base = alt.Chart(df).encode(x=x, y=y, tooltip=["Rótulo", alt.Tooltip("Score:Q", format=".0f")])
    line = base.mark_line(color=BLUE, strokeWidth=2)
    points = base.mark_point(filled=True, size=80, color=BLUE, stroke=SURFACE, strokeWidth=2, opacity=1)
    labels = base.mark_text(dy=-14, color=INK).encode(text=alt.Text("Score:Q", format=".0f"))
    rule = alt.Chart(pd.DataFrame({"t": [target]})).mark_rule(strokeDash=[4, 3], color=INK_2).encode(
        y="t:Q", tooltip=[alt.Tooltip("t:Q", title="Meta do porte")])
    return _style((rule + line + points + labels).properties(height=280))


def dimension_trend(df: pd.DataFrame, dimensions: list[str]) -> alt.Chart:
    """df: Rótulo + uma coluna por dimensão (em ordem cronológica)."""
    order = list(df["Rótulo"])
    long = df.melt("Rótulo", value_vars=dimensions, var_name="Dimensão", value_name="Score")
    color = alt.Color("Dimensão:N", title=None, scale=alt.Scale(domain=dimensions, range=[BLUE, ORANGE, AQUA, YELLOW]),
                      legend=alt.Legend(orient="top", columns=2, labelLimit=260))
    x = alt.X("Rótulo:N", sort=order, title=None, axis=alt.Axis(labelAngle=0))
    y = alt.Y("Score:Q", title="Score (0–100)", scale=alt.Scale(domain=[0, 100]))
    base = alt.Chart(long).encode(x=x, y=y, color=color,
                                  tooltip=["Rótulo", "Dimensão", alt.Tooltip("Score:Q", format=".0f")])
    lines = base.mark_line(strokeWidth=2)
    points = base.mark_point(filled=True, size=70, stroke=SURFACE, strokeWidth=2, opacity=1)
    last = base.transform_filter(alt.datum["Rótulo"] == order[-1]).mark_text(
        align="left", dx=8, color=INK).encode(text=alt.Text("Score:Q", format=".0f"))
    return _style((lines + points + last).properties(height=300))


def divergence_bars(df: pd.DataFrame, tolerance: float) -> alt.Chart:
    """df: Mês, Divergência (%), Situação."""
    color = alt.Color("Situação:N", title=None,
                      scale=alt.Scale(domain=["Dentro da tolerância", "Fora da tolerância"], range=[BLUE, CRITICAL]))
    chart = alt.Chart(df).encode(
        x=alt.X("Mês:N", sort=list(df["Mês"]), title=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Divergência (%):Q", title="Divergência absoluta (%)"),
        tooltip=["Mês", alt.Tooltip("Divergência (%):Q", format=".2f"), "Situação"],
    )
    bars = chart.mark_bar(size=22, cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(color=color)
    rule = alt.Chart(pd.DataFrame({"t": [tolerance]})).mark_rule(strokeDash=[4, 3], color=INK_2).encode(
        y="t:Q", tooltip=[alt.Tooltip("t:Q", title="Tolerância (%)")])
    return _style((bars + rule).properties(height=280))
