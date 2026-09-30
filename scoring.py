"""Cálculo do score de maturidade regulatória."""

from data import DIM_WEIGHTS, DIMENSIONS, MATURITY_LEVELS, QUESTIONS


def option_score(question: dict, index: int) -> float:
    """Converte a posição da opção (0 = menor maturidade) numa nota de 0 a 100."""
    return index / (len(question["options"]) - 1) * 100


def survey_question_score(question: dict) -> float:
    """Nota média da pesquisa para uma pergunta."""
    total = sum(question["counts"])
    return sum(option_score(question, i) * c for i, c in enumerate(question["counts"])) / total


def dimension_scores(question_scores: dict[str, float]) -> dict[str, float]:
    """Média simples das perguntas de cada dimensão."""
    result = {}
    for dim in DIMENSIONS:
        values = [question_scores[q["id"]] for q in QUESTIONS if q["dim"] == dim]
        result[dim] = sum(values) / len(values)
    return result


def overall_score(dim_scores: dict[str, float]) -> float:
    return sum(dim_scores[d] * DIM_WEIGHTS[d] for d in DIMENSIONS)


def maturity_level(score: float) -> tuple[str, str]:
    name, desc = MATURITY_LEVELS[0][1], MATURITY_LEVELS[0][2]
    for threshold, level_name, level_desc in MATURITY_LEVELS:
        if score >= threshold:
            name, desc = level_name, level_desc
    return name, desc


def survey_benchmark() -> tuple[dict[str, float], dict[str, float], float]:
    """Scores médios da pesquisa (por pergunta, por dimensão e geral)."""
    q_scores = {q["id"]: survey_question_score(q) for q in QUESTIONS}
    d_scores = dimension_scores(q_scores)
    return q_scores, d_scores, overall_score(d_scores)
