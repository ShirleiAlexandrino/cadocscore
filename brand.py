"""Identidade visual do CadocScore: logo, estilos e componentes de cabeçalho."""

from pathlib import Path

import streamlit as st

ASSETS = Path(__file__).parent / "assets"

NAVY = "#0B2545"      # Marinho regulador: marca, sidebar, hero
BLUE = "#1C5CAB"      # Azul score: ações e links
TEAL = "#1BAF7A"      # Verde conformidade: destaque, evolução
INK = "#0B1B2E"
INK_2 = "#5B6B80"
LINE = "#D5DEE9"

CSS = f"""
<style>
[data-testid="stMetric"] {{
    background: #FFFFFF; border: 1px solid {LINE}; border-radius: 0.8rem; padding: 14px 16px;
}}
[data-testid="stMetricLabel"] p {{ color: {INK_2}; font-weight: 600; }}
.cs-header {{ margin: 0 0 0.5rem 0; }}
.cs-kicker {{
    display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 999px;
    background: #E3F4EE; color: #0B7A54; font: 700 0.72rem/1.4 Inter, sans-serif; letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.cs-title {{
    font: 800 2.1rem/1.15 "Plus Jakarta Sans", sans-serif; color: {INK}; margin: 10px 0 6px 0;
    letter-spacing: -0.02em;
}}
.cs-sub {{ font: 400 1.02rem/1.55 Inter, sans-serif; color: {INK_2}; margin: 0; max-width: 60rem; }}
.cs-hero {{
    background: linear-gradient(120deg, {NAVY} 0%, #123A6B 65%, #17507F 100%); border-radius: 1rem;
    padding: 36px 40px; color: #FFFFFF; position: relative; overflow: hidden;
}}
.cs-hero::after {{
    content: ""; position: absolute; right: -60px; top: -60px; width: 260px; height: 260px; border-radius: 50%;
    border: 28px solid rgba(27, 175, 122, 0.18);
}}
.cs-hero h1 {{
    font: 800 2.4rem/1.1 "Plus Jakarta Sans", sans-serif; margin: 12px 0 10px 0; color: #FFFFFF;
    letter-spacing: -0.02em; padding: 0;
}}
.cs-hero h1 span {{ color: {TEAL}; }}
.cs-hero p {{ font: 400 1.05rem/1.6 Inter, sans-serif; color: #C9D6E8; margin: 0; max-width: 46rem; }}
.cs-hero .cs-kicker {{ background: rgba(27, 175, 122, 0.18); color: #7FE0BC; }}
.cs-problem {{
    border-left: 4px solid {TEAL}; background: #FFFFFF; border-radius: 0 0.6rem 0.6rem 0; padding: 14px 18px;
    color: {INK}; font: 400 0.98rem/1.6 Inter, sans-serif; margin-top: 18px;
}}
.cs-pillar-num {{
    display: inline-flex; width: 30px; height: 30px; border-radius: 8px; align-items: center; justify-content: center;
    background: {NAVY}; color: #FFFFFF; font: 800 0.95rem "Plus Jakarta Sans", sans-serif; margin-right: 8px;
}}
.cs-pillar-title {{ font: 700 1.15rem "Plus Jakarta Sans", sans-serif; color: {INK}; vertical-align: middle; }}
.cs-footer {{ color: {INK_2}; font: 400 0.8rem Inter, sans-serif; margin-top: 2rem; }}
</style>
"""


def apply():
    """Aplica logo e estilos. Chamar uma vez por execução, antes das páginas."""
    st.logo(str(ASSETS / "logo_sidebar.png"), icon_image=str(ASSETS / "icon.png"), size="large")
    st.html(CSS)


def page_header(kicker: str, title: str, subtitle: str = ""):
    sub = f'<p class="cs-sub">{subtitle}</p>' if subtitle else ""
    st.html(f'<div class="cs-header"><span class="cs-kicker">{kicker}</span>'
            f'<div class="cs-title">{title}</div>{sub}</div>')


def hero(kicker: str, title_html: str, text: str, problem_html: str):
    st.html(f'<div class="cs-hero"><span class="cs-kicker">{kicker}</span><h1>{title_html}</h1><p>{text}</p></div>'
            f'<div class="cs-problem">{problem_html}</div>')


def pillar_title(number: int, title: str):
    st.html(f'<span class="cs-pillar-num">{number}</span><span class="cs-pillar-title">{title}</span>')


def footer():
    st.html('<div class="cs-footer">CadocScore · Protótipo do TCC FIAP MBA Arquitetura de Soluções · Turma 8ASOR · '
            'Erika Regina Brunelli, Nauana Kelly Lima Nonato e Shirlei Alexandrino</div>')
