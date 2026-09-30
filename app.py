"""CadocScore: protótipo para medir, monitorar e evoluir a maturidade regulatória (TCC FIAP 8ASOR)."""

from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st

import brand
import charts
from data import (ACTION_STATUS, ACTIONS, DEMO_HISTORY, DIM_WEIGHTS, DIMENSIONS, MATURITY_LEVELS, QUESTIONS,
                  TARGET_BY_SEGMENT)
from scoring import dimension_scores, maturity_level, option_score, overall_score, survey_benchmark

st.set_page_config(page_title="CadocScore · Maturidade regulatória", page_icon=str(brand.ASSETS / "favicon.png"),
                   layout="wide")

SURVEY_Q, SURVEY_DIM, SURVEY_OVERALL = survey_benchmark()
QUESTION_BY_ID = {q["id"]: q for q in QUESTIONS}
KPI_COLUMNS = ["Críticas do regulador", "Consistência entre CADOCs (%)"]
HISTORY_COLUMNS = ["Data", "Rótulo", *DIMENSIONS, *KPI_COLUMNS]
PROBLEM = ("Ausência de um modelo estruturado que permita **medir, monitorar e evoluir** a maturidade regulatória "
           "das instituições financeiras, considerando aspectos como **qualidade, confiabilidade e integração** "
           "dos dados regulatórios.")


def quarter_label(d: date) -> str:
    return f"{(d.month - 1) // 3 + 1}º tri {d.year}"


def evaluate(levels: dict[str, int]) -> tuple[dict[str, float], dict[str, float], float]:
    """levels: índice da opção escolhida por pergunta. Retorna scores por pergunta, dimensão e geral."""
    q_scores = {qid: option_score(QUESTION_BY_ID[qid], i) for qid, i in levels.items()}
    d_scores = dimension_scores(q_scores)
    return q_scores, d_scores, overall_score(d_scores)


def current_levels() -> dict[str, int] | None:
    result = st.session_state.get("result")
    if not result:
        return None
    return {q["id"]: q["options"].index(result["answers"][q["id"]]) for q in QUESTIONS}


def current_segment() -> str:
    result = st.session_state.get("result")
    return result["segment"] if result else "Cooperativa de crédito S4"


def typical_levels() -> dict[str, int]:
    """Resposta mais frequente da pesquisa em cada pergunta (perfil típico da amostra)."""
    return {q["id"]: int(np.argmax(q["counts"])) for q in QUESTIONS}


def read_user_csv(upload) -> pd.DataFrame:
    """Lê CSV com separador , ou ; e com ou sem BOM (como o Excel salva)."""
    df = pd.read_csv(upload, sep=None, engine="python", encoding="utf-8-sig", dtype=str)
    df.columns = df.columns.str.strip()
    return df


def to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Converte números no formato brasileiro (1.234,56) ou internacional (1234.56)."""
    for col in columns:
        text = df[col].astype(str).str.strip()
        brazilian = text.str.contains(",", regex=False)
        text = text.where(~brazilian, text.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
        df[col] = pd.to_numeric(text, errors="coerce")
    return df.dropna(subset=columns)


def go_to(key: str, label: str):
    if st.button(label, key=f"go_{key}_{label}"):
        st.switch_page(PAGES[key])


# ---------------------------------------------------------------------------
# Início
# ---------------------------------------------------------------------------
def page_home():
    brand.hero(
        "Protótipo · Governança de dados regulatórios",
        "Da obrigação à <span>maturidade regulatória</span>",
        "Hoje as instituições enviam os CADOCs ao BACEN no prazo, mas a validação é só técnica (layout), não há "
        "cruzamento estruturado entre documentos e os problemas aparecem depois do questionamento do regulador. "
        "Com a Resolução Conjunta sobre qualidade de dados, isso deixou de ser suficiente.",
        "<b>Problema endereçado:</b> ausência de um modelo estruturado que permita <b>medir, monitorar e evoluir</b> "
        "a maturidade regulatória das instituições financeiras, considerando <b>qualidade, confiabilidade e "
        "integração</b> dos dados regulatórios.",
    )

    st.markdown("#### Como o CadocScore endereça o problema")
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        brand.pillar_title(1, "Medir")
        st.write("Diagnóstico com 13 perguntas em 4 dimensões, que gera um score formal de 0 a 100, "
                 "um nível de maturidade e a comparação com a meta do porte da instituição.")
        go_to("diag", "Fazer diagnóstico")
    with c2.container(border=True):
        brand.pillar_title(2, "Monitorar")
        st.write("Histórico de avaliações com a evolução do score, das dimensões e dos indicadores de "
                 "qualidade dos dados (críticas do regulador e consistência entre CADOCs).")
        go_to("monitor", "Ver monitoramento")
    with c3.container(border=True):
        brand.pillar_title(3, "Evoluir")
        st.write("Plano de ação priorizado pelo ganho no score, com responsável, prazo e status. "
                 "O score projetado mostra aonde a instituição chega ao concluir as ações.")
        go_to("plan", "Abrir plano de evolução")

    st.markdown("#### Aspectos dos dados regulatórios cobertos")
    st.markdown(
        "- **Qualidade:** validação semântica entre CADOCs antes do envio, com índice de consistência "
        "acompanhado ao longo do tempo.\n"
        "- **Confiabilidade:** índice de confiabilidade regulatória, score formal, análise de risco baseada em dados "
        "e registro e reincidência das críticas do regulador.\n"
        "- **Integração:** mapeamento das obrigações até os sistemas de origem (data lineage) e cruzamento "
        "automatizado entre documentos."
    )

    brand.footer()


# ---------------------------------------------------------------------------
# 1. Medir: diagnóstico
# ---------------------------------------------------------------------------
def page_diagnostic():
    brand.page_header("Pilar 1 · Medir", "Diagnóstico de maturidade",
                      "Responda pensando na situação atual da instituição. "
                      "As opções vão da menor para a maior maturidade.")

    c1, c2 = st.columns(2)
    institution = c1.text_input("Nome da instituição", placeholder="Ex.: Cooperativa Exemplo")
    segment = c2.selectbox("Porte / segmento", list(TARGET_BY_SEGMENT), index=3)

    with st.form("diagnostico"):
        answers = {}
        for dim in DIMENSIONS:
            st.markdown(f"#### {dim}")
            for q in (q for q in QUESTIONS if q["dim"] == dim):
                answers[q["id"]] = st.radio(f"**{q['id']}.** {q['text']}", q["options"], index=None, key=q["id"])
        submitted = st.form_submit_button("Calcular score", type="primary")

    if submitted:
        missing = [qid for qid, a in answers.items() if a is None]
        if missing:
            st.warning(f"Responda todas as perguntas. Faltam: {', '.join(missing)}.")
            return
        st.session_state["result"] = {"answers": answers, "institution": institution, "segment": segment}

    if st.session_state.get("result"):
        show_result(st.session_state["result"])


def show_result(result: dict):
    segment = result["segment"]
    name = result["institution"] or "Sua instituição"
    q_scores, d_scores, score = evaluate(current_levels())
    level, level_desc = maturity_level(score)
    target = TARGET_BY_SEGMENT[segment]

    st.divider()
    st.header(f"Resultado: {name}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score geral", f"{score:.0f} / 100")
    c2.metric("Nível de maturidade", level)
    c3.metric("Meta do porte", f"{target}", delta=f"{score - target:+.0f} pts", help=segment)
    c4.metric("Média da pesquisa", f"{SURVEY_OVERALL:.0f}", delta=f"{score - SURVEY_OVERALL:+.0f} pts")
    st.caption(f"**{level}:** {level_desc}")

    st.markdown("#### Score por dimensão")
    df = pd.DataFrame({
        "Dimensão": DIMENSIONS,
        "Sua instituição": [d_scores[d] for d in DIMENSIONS],
        "Média da pesquisa": [SURVEY_DIM[d] for d in DIMENSIONS],
        "Meta do porte": [target] * len(DIMENSIONS),
    })
    st.altair_chart(charts.dimension_comparison(df), width="stretch")
    st.caption("Barra azul: sua instituição. Traço laranja: média da pesquisa. "
               "Linha tracejada: meta do porte (valor ilustrativo, a calibrar).")
    with st.expander("Ver tabela"):
        st.dataframe(df.round(0), hide_index=True, width="stretch")

    below = [d for d in sorted(DIMENSIONS, key=lambda d: d_scores[d]) if d_scores[d] < target]
    if below:
        st.warning("⚠️ Dimensões abaixo da meta do porte: " + "; ".join(f"{d} ({d_scores[d]:.0f})" for d in below))
    else:
        st.success("✅ Todas as dimensões atingem a meta do porte.")

    st.markdown("#### Registrar esta avaliação no monitoramento")
    st.write("Registre o resultado com os indicadores de qualidade de dados do período para acompanhar a evolução.")
    with st.form("registrar"):
        c1, c2, c3, c4 = st.columns(4)
        ref_date = c1.date_input("Data de referência", date.today(), format="DD/MM/YYYY")
        label = c2.text_input("Rótulo do período", quarter_label(date.today()))
        criticas = c3.number_input("Críticas do regulador no período", 0, 10_000, 0)
        consistency = c4.number_input("Consistência entre CADOCs (%)", 0.0, 100.0,
                                      float(st.session_state.get("last_consistency", 0.0)), 1.0,
                                      help="Preenchido com o último resultado da página Validação entre CADOCs.")
        if st.form_submit_button("Registrar no histórico"):
            row = {"Data": ref_date.isoformat(), "Rótulo": label, **{d: round(d_scores[d], 1) for d in DIMENSIONS},
                   "Críticas do regulador": criticas, "Consistência entre CADOCs (%)": consistency}
            st.session_state.setdefault("history", []).append(row)
            st.success(f"✅ Avaliação “{label}” registrada no monitoramento.")

    c1, c2, c3 = st.columns(3)
    with c1:
        go_to("monitor", "Ir para o monitoramento")
    with c2:
        go_to("plan", "Montar plano de evolução")
    report = build_report(name, segment, result["answers"], q_scores, d_scores, score, level, target)
    c3.download_button("Baixar relatório (Markdown)", report, file_name="cadocscore_relatorio.md",
                       mime="text/markdown")


def build_report(name, segment, answers, q_scores, d_scores, score, level, target) -> str:
    lines = [f"# Relatório CadocScore: {name}", "",
             f"- Data: {date.today():%d/%m/%Y}", f"- Segmento: {segment}",
             f"- Score geral: {score:.0f}/100 (nível {level})", f"- Meta do porte: {target}",
             f"- Média da pesquisa de referência: {SURVEY_OVERALL:.0f}", "", "## Score por dimensão", ""]
    lines += [f"- {d}: {d_scores[d]:.0f} (pesquisa: {SURVEY_DIM[d]:.0f})" for d in DIMENSIONS]
    lines += ["", "## Respostas", ""]
    lines += [f"- {q['id']}. {q['text']} **{answers[q['id']]}** ({q_scores[q['id']]:.0f})" for q in QUESTIONS]
    lines += ["", "## Ações recomendadas (por ganho no score)", ""]
    plan = build_plan(current_levels())
    lines += [f"- [{r['Pergunta']}] {r['Ação']} (+{r['Ganho no score']:.1f} pts)" for _, r in plan.iterrows()]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. Monitorar
# ---------------------------------------------------------------------------
def page_monitor():
    brand.page_header("Pilar 2 · Monitorar", "Evolução da maturidade",
                      "Acompanhe o score, as dimensões e os indicadores de qualidade dos dados a cada avaliação.")

    history = st.session_state.get("history", [])
    c1, c2, c3 = st.columns(3)
    if c1.button("Carregar histórico de exemplo"):
        st.session_state["history"] = [dict(r) for r in DEMO_HISTORY]
        st.rerun()
    upload = c2.file_uploader("Importar histórico (CSV)", type="csv", label_visibility="collapsed")
    if upload:
        imported = read_user_csv(upload)
        if not set(HISTORY_COLUMNS) <= set(imported.columns):
            st.error("O CSV precisa das colunas: " + ", ".join(HISTORY_COLUMNS))
        else:
            imported = to_numeric(imported, [*DIMENSIONS, *KPI_COLUMNS])
            imported["Data"] = imported["Data"].astype(str)
            st.session_state["history"] = imported[HISTORY_COLUMNS].to_dict("records")
            history = st.session_state["history"]
    if history and c3.button("Limpar histórico"):
        st.session_state["history"] = []
        st.rerun()

    if not history:
        st.info("Nenhuma avaliação registrada. Faça o diagnóstico e registre o resultado, importe um CSV "
                "exportado anteriormente ou carregue o histórico de exemplo.", icon="ℹ️")
        go_to("diag", "Fazer diagnóstico")
        return

    df = pd.DataFrame(history).sort_values("Data").reset_index(drop=True)
    df["Score"] = [overall_score({d: row[d] for d in DIMENSIONS}) for _, row in df.iterrows()]
    segment = st.selectbox("Meta de referência (porte)", list(TARGET_BY_SEGMENT),
                           index=list(TARGET_BY_SEGMENT).index(current_segment()))
    target = TARGET_BY_SEGMENT[segment]

    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else None
    level, _ = maturity_level(last["Score"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"Score ({last['Rótulo']})", f"{last['Score']:.0f}", chart_data=df["Score"].round(1).tolist(),
              delta=f"{last['Score'] - prev['Score']:+.0f} pts" if prev is not None else None)
    c2.metric("Nível de maturidade", level, delta=f"Meta do porte: {target}", delta_color="off", delta_arrow="off")
    c3.metric("Críticas do regulador", f"{last['Críticas do regulador']:.0f}", delta_color="inverse",
              chart_data=df["Críticas do regulador"].tolist(), chart_type="bar",
              delta=f"{last['Críticas do regulador'] - prev['Críticas do regulador']:+.0f}" if prev is not None else None)
    c4.metric("Consistência CADOCs", f"{last['Consistência entre CADOCs (%)']:.0f}%",
              chart_data=df["Consistência entre CADOCs (%)"].tolist(),
              delta=(f"{last['Consistência entre CADOCs (%)'] - prev['Consistência entre CADOCs (%)']:+.0f} p.p."
                     if prev is not None else None))

    if prev is not None:
        drops = [d for d in DIMENSIONS if last[d] < prev[d]]
        if drops:
            st.warning("⚠️ Dimensões que regrediram desde a avaliação anterior: " + ", ".join(drops))
    gaps = [d for d in DIMENSIONS if last[d] < target]
    if gaps:
        st.info(f"🎯 Abaixo da meta ({target}): " + ", ".join(f"{d} ({last[d]:.0f})" for d in gaps), icon="ℹ️")

    st.markdown("#### Score geral ao longo do tempo")
    st.altair_chart(charts.score_trend(df[["Rótulo", "Score"]], target), width="stretch")
    st.caption("Linha tracejada: meta do porte selecionado.")

    st.markdown("#### Evolução por dimensão")
    st.altair_chart(charts.dimension_trend(df[["Rótulo", *DIMENSIONS]], DIMENSIONS), width="stretch")

    with st.expander("Ver tabela do histórico", expanded=False):
        st.dataframe(df[["Data", "Rótulo", "Score", *DIMENSIONS, *KPI_COLUMNS]].round(1), hide_index=True,
                     width="stretch")
    st.download_button("Exportar histórico (CSV)", df[HISTORY_COLUMNS].to_csv(index=False).encode("utf-8-sig"),
                       file_name="cadocscore_historico.csv", mime="text/csv")
    st.caption("O protótipo não tem banco de dados: exporte o histórico em CSV e importe-o na próxima sessão.")


# ---------------------------------------------------------------------------
# 3. Evoluir
# ---------------------------------------------------------------------------
def build_plan(levels: dict[str, int]) -> pd.DataFrame:
    """Ações para as perguntas que ainda não estão no nível máximo, ordenadas pelo ganho no score."""
    _, _, base = evaluate(levels)
    rows = []
    for action in ACTIONS:
        q = QUESTION_BY_ID[action["q"]]
        i = levels[q["id"]]
        if i >= len(q["options"]) - 1:
            continue
        _, _, bumped = evaluate({**levels, q["id"]: i + 1})
        rows.append({"Pergunta": q["id"], "Dimensão": q["dim"], "Ação": action["acao"],
                     "Nível atual": q["options"][i], "Próximo nível": q["options"][i + 1],
                     "Ganho no score": round(bumped - base, 1)})
    plan = pd.DataFrame(rows).sort_values("Ganho no score", ascending=False).reset_index(drop=True)
    today = date.today()
    plan["Responsável"] = ""
    plan["Prazo"] = [today + timedelta(days=90 * (1 + i // 4)) for i in range(len(plan))]
    plan["Status"] = ACTION_STATUS[0]
    return plan[["Pergunta", "Ação", "Ganho no score", "Status", "Responsável", "Prazo", "Dimensão",
                 "Nível atual", "Próximo nível"]]


def page_plan():
    brand.page_header("Pilar 3 · Evoluir", "Plano de evolução",
                      "As ações vêm das lacunas do diagnóstico e estão ordenadas pelo <b>ganho estimado no "
                      "score</b>. Cada ação concluída faz a pergunta correspondente subir um nível na escala.")

    levels = current_levels()
    if levels is None:
        st.info("Nenhum diagnóstico nesta sessão. Faça o diagnóstico ou use o perfil típico da pesquisa "
                "(resposta mais frequente em cada pergunta).", icon="ℹ️")
        c1, c2 = st.columns([1, 3])
        with c1:
            go_to("diag", "Fazer diagnóstico")
        if not c2.toggle("Usar o perfil típico da pesquisa"):
            return
        levels = typical_levels()

    _, d_now, score_now = evaluate(levels)
    target = TARGET_BY_SEGMENT[current_segment()]
    plan = build_plan(levels)
    if plan.empty:
        st.success("✅ Todas as perguntas já estão no nível máximo.")
        return

    edited = st.data_editor(
        plan, hide_index=True, width="stretch", key="plan_" + "".join(str(levels[q["id"]]) for q in QUESTIONS),
        disabled=["Pergunta", "Dimensão", "Ação", "Nível atual", "Próximo nível", "Ganho no score"],
        column_config={
            "Ação": st.column_config.TextColumn(width="large"),
            "Responsável": st.column_config.TextColumn(width="small"),
            "Ganho no score": st.column_config.NumberColumn(format="+%.1f pts"),
            "Prazo": st.column_config.DateColumn(format="DD/MM/YYYY"),
            "Status": st.column_config.SelectboxColumn(options=ACTION_STATUS, required=True),
        },
    )

    def project(statuses: set[str]) -> tuple[dict[str, float], float]:
        new = dict(levels)
        for qid in edited.loc[edited["Status"].isin(statuses), "Pergunta"]:
            new[qid] = min(new[qid] + 1, len(QUESTION_BY_ID[qid]["options"]) - 1)
        _, d, s = evaluate(new)
        return d, s

    d_done, score_done = project({"Concluída"})
    _, score_all = project(set(ACTION_STATUS))
    done = int((edited["Status"] == "Concluída").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score atual", f"{score_now:.0f}")
    c2.metric("Score com ações concluídas", f"{score_done:.0f}", delta=f"{score_done - score_now:+.1f} pts")
    c3.metric("Potencial com o plano completo", f"{score_all:.0f}", delta=f"{score_all - score_now:+.1f} pts")
    c4.metric("Ações concluídas", f"{done} de {len(edited)}")
    st.progress(done / len(edited))

    level_done, _ = maturity_level(score_done)
    if score_done >= target:
        st.success(f"✅ Com as ações concluídas, a instituição atinge a meta do porte ({target}), nível {level_done}.")
    else:
        st.info(f"🎯 Faltam {target - score_done:.0f} pts para a meta do porte ({target}).", icon="ℹ️")

    st.markdown("#### Atual × projetado por dimensão")
    df = pd.DataFrame({"Dimensão": DIMENSIONS, "Projetado": [d_done[d] for d in DIMENSIONS],
                       "Atual": [d_now[d] for d in DIMENSIONS], "Meta do porte": [target] * len(DIMENSIONS)})
    st.altair_chart(charts.dimension_comparison(df, bar="Projetado", tick="Atual"), width="stretch")
    st.caption("Barra azul: score projetado com as ações concluídas. Traço laranja: score atual. "
               "Linha tracejada: meta do porte.")

    st.download_button("Exportar plano (CSV)", edited.to_csv(index=False).encode("utf-8-sig"),
                       file_name="cadocscore_plano.csv", mime="text/csv")
    st.caption("O score projetado é uma estimativa. Depois de concluir as ações, refaça o diagnóstico e "
               "registre o resultado no monitoramento para confirmar a evolução.")


# ---------------------------------------------------------------------------
# Validação entre CADOCs (qualidade dos dados)
# ---------------------------------------------------------------------------
MONTHS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def sample_crosscheck() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    base = np.linspace(480, 560, 12) * 1_000_000
    doc_a = base * (1 + rng.normal(0, 0.002, 12))
    doc_b = doc_a * (1 + rng.normal(0, 0.001, 12))
    doc_b[3] *= 1.018   # divergência injetada em abril
    doc_b[8] *= 0.975   # divergência injetada em setembro
    return pd.DataFrame({"Mês": MONTHS, "Documento A": doc_a.round(2), "Documento B": doc_b.round(2)})


def page_crosscheck():
    brand.page_header(
        "Qualidade dos dados", "Validação entre CADOCs",
        "A validação técnica só confere se o arquivo está no layout correto. O CadocScore cruza <b>informações "
        "equivalentes em documentos diferentes</b> antes do envio. Exemplo: o saldo da carteira de crédito no "
        "balancete (Doc 4010) deve ser coerente com a soma das operações informadas ao SCR (Doc 3040). "
        "O índice de consistência resultante alimenta o monitoramento."
    )
    st.info("Demonstração com dados fictícios. Você pode enviar um CSV com as colunas "
            "`Mês`, `Documento A` e `Documento B`.", icon="ℹ️")

    c1, c2, c3 = st.columns(3)
    label_a = c1.text_input("Documento A", "Doc 4010: carteira de crédito (balancete)")
    label_b = c2.text_input("Documento B", "Doc 3040: soma das operações (SCR)")
    tolerance = c3.slider("Tolerância de divergência (%)", 0.1, 5.0, 1.0, 0.1)

    upload = st.file_uploader("CSV (opcional)", type="csv")
    if upload:
        df = read_user_csv(upload)
        if not {"Mês", "Documento A", "Documento B"} <= set(df.columns):
            st.error("O CSV precisa das colunas Mês, Documento A e Documento B.")
            return
        df = to_numeric(df, ["Documento A", "Documento B"])
    else:
        df = sample_crosscheck()

    df["Diferença (R$)"] = df["Documento B"] - df["Documento A"]
    df["Divergência (%)"] = (df["Diferença (R$)"].abs() / df["Documento A"] * 100).round(2)
    df["Situação"] = np.where(df["Divergência (%)"] > tolerance, "Fora da tolerância", "Dentro da tolerância")
    out = df[df["Situação"] == "Fora da tolerância"]
    consistency = (1 - len(out) / len(df)) * 100
    st.session_state["last_consistency"] = round(consistency, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Períodos analisados", len(df))
    c2.metric("Inconsistências encontradas", len(out))
    c3.metric("Índice de consistência", f"{consistency:.0f}%")

    st.altair_chart(charts.divergence_bars(df, tolerance), width="stretch")
    st.caption("Linha tracejada: tolerância configurada.")

    if len(out):
        st.error(f"⚠️ {len(out)} período(s) com divergência acima de {tolerance:.1f}% entre "
                 f"“{label_a}” e “{label_b}”: {', '.join(out['Mês'].astype(str))}. "
                 "Investigue a origem antes do envio ao regulador.")
    else:
        st.success("✅ Nenhuma divergência acima da tolerância.")

    show = df.assign(Situação=df["Situação"].map({"Fora da tolerância": "⚠️ Fora", "Dentro da tolerância": "✅ Ok"}))
    show = show.rename(columns={"Documento A": label_a, "Documento B": label_b})
    st.dataframe(show, hide_index=True, width="stretch",
                 column_config={label_a: st.column_config.NumberColumn(format="%.2f"),
                                label_b: st.column_config.NumberColumn(format="%.2f"),
                                "Diferença (R$)": st.column_config.NumberColumn(format="%.2f")})


# ---------------------------------------------------------------------------
# Metodologia
# ---------------------------------------------------------------------------
def page_method():
    brand.page_header("Transparência", "Metodologia do score",
                      "Cada resposta vira uma nota de 0 a 100 conforme sua posição na escala da pergunta. "
                      "A nota da dimensão é a média das perguntas; o score geral é a média ponderada das dimensões.")
    st.dataframe(pd.DataFrame({"Dimensão": DIMENSIONS,
                               "Perguntas": [", ".join(q["id"] for q in QUESTIONS if q["dim"] == d) for d in DIMENSIONS],
                               "Peso": [f"{DIM_WEIGHTS[d]:.0%}" for d in DIMENSIONS]}),
                 hide_index=True, width="stretch")
    st.markdown("#### Níveis de maturidade")
    bounds = [t for t, _, _ in MATURITY_LEVELS] + [101]
    st.dataframe(pd.DataFrame({"Faixa": [f"{bounds[i]}–{bounds[i + 1] - 1}" for i in range(len(MATURITY_LEVELS))],
                               "Nível": [n for _, n, _ in MATURITY_LEVELS],
                               "Descrição": [d for _, _, d in MATURITY_LEVELS]}),
                 hide_index=True, width="stretch")
    st.markdown("#### Metas por porte")
    st.dataframe(pd.DataFrame({"Segmento": list(TARGET_BY_SEGMENT), "Meta": list(TARGET_BY_SEGMENT.values())}),
                 hide_index=True, width="stretch")
    st.markdown("#### Plano de evolução")
    st.write("Cada ação está ligada a uma pergunta. O ganho estimado é a diferença no score geral se aquela "
             "pergunta subir um nível; por isso, o plano prioriza as ações de maior impacto.")
    st.caption("Pesos e metas são hipóteses do protótipo, a calibrar com especialistas e referenciais "
               "como COBIT, IBGC e as normas do BACEN.")


PAGES = {
    "home": st.Page(page_home, title="Início", icon=":material/home:", default=True),
    "diag": st.Page(page_diagnostic, title="Medir · Diagnóstico", icon=":material/speed:", url_path="diagnostico"),
    "monitor": st.Page(page_monitor, title="Monitorar · Evolução", icon=":material/monitoring:", url_path="monitoramento"),
    "plan": st.Page(page_plan, title="Evoluir · Plano de ação", icon=":material/trending_up:", url_path="plano"),
    "cross": st.Page(page_crosscheck, title="Validação entre CADOCs", icon=":material/fact_check:", url_path="validacao"),
    "method": st.Page(page_method, title="Metodologia", icon=":material/menu_book:", url_path="metodologia"),
}

if __name__ == "__main__":
    brand.apply()
    st.navigation(list(PAGES.values())).run()
