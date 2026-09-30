"""Dados de referência do CadocScore: questionário, benchmark da pesquisa, pesos, metas e ações."""

# ---------------------------------------------------------------------------
# Questionário de maturidade regulatória (mesmas perguntas do Entregável 1).
# As opções estão em ordem crescente de maturidade: índice 0 = menor maturidade.
# "counts" = respostas da pesquisa de validação (n = 7), usadas como benchmark.
# ---------------------------------------------------------------------------
QUESTIONS = [
    {
        "id": "Q1",
        "dim": "Visão executiva e governança",
        "text": "A instituição possui uma visão consolidada do nível geral de aderência regulatória?",
        "options": ["Não possui", "Parcial e descentralizada", "Consolidada manualmente",
                    "Consolidada com apoio sistêmico", "Totalmente automatizada e atualizada"],
        "counts": [1, 3, 2, 1, 0],
    },
    {
        "id": "Q2",
        "dim": "Visão executiva e governança",
        "text": "Existe dashboard executivo acessível à diretoria?",
        "options": ["Não", "Sim, mas não consolidado", "Sim, consolidado parcialmente",
                    "Sim, consolidado e estruturado"],
        "counts": [3, 1, 2, 1],
    },
    {
        "id": "Q3",
        "dim": "Visão executiva e governança",
        "text": "Há indicadores estratégicos de compliance apresentados ao conselho?",
        "options": ["Não", "Apenas operacionais", "Indicadores estratégicos não padronizados",
                    "Indicadores estratégicos formais e recorrentes"],
        "counts": [1, 3, 2, 1],
    },
    {
        "id": "Q4",
        "dim": "Gestão de críticas e reincidência",
        "text": "O histórico de críticas ou rejeições regulatórias é registrado de forma estruturada?",
        "options": ["Não", "Parcialmente", "Sim, mas sem análise histórica", "Sim, com análise de tendência"],
        "counts": [0, 2, 4, 1],
    },
    {
        "id": "Q5",
        "dim": "Gestão de críticas e reincidência",
        "text": "É possível medir reincidência por tipo de obrigação?",
        "options": ["Não", "Manualmente", "Parcialmente automatizado", "Totalmente estruturado"],
        "counts": [0, 4, 3, 0],
    },
    {
        "id": "Q6",
        "dim": "Confiabilidade e risco regulatório",
        "text": "A instituição possui algum índice de confiabilidade regulatória?",
        "options": ["Não", "Em construção", "Sim, interno", "Sim, formalizado e acompanhado pela gestão"],
        "counts": [2, 2, 2, 1],
    },
    {
        "id": "Q7",
        "dim": "Confiabilidade e risco regulatório",
        "text": "Existe visão consolidada do maior risco regulatório atual?",
        "options": ["Não", "Baseada em percepção", "Baseada em dados históricos",
                    "Baseada em modelo estruturado de risco"],
        "counts": [1, 5, 1, 0],
    },
    {
        "id": "Q8",
        "dim": "Gestão de críticas e reincidência",
        "text": "Há priorização automática baseada em histórico de falhas?",
        "options": ["Não", "Priorização manual", "Priorização com critérios definidos",
                    "Modelo estruturado com apoio sistêmico"],
        "counts": [2, 3, 2, 0],
    },
    {
        "id": "Q9",
        "dim": "Confiabilidade e risco regulatório",
        "text": "O sistema utilizado vai além de calendário e validação técnica?",
        "options": ["Não", "Parcialmente", "Sim, inclui análise de risco", "Sim, inclui inteligência analítica"],
        "counts": [2, 3, 2, 0],
    },
    {
        "id": "Q10",
        "dim": "Visão executiva e governança",
        "text": "É possível visualizar a evolução da performance regulatória ao longo dos anos?",
        "options": ["Não", "Apenas relatórios isolados", "Sim, com indicadores comparativos",
                    "Sim, com metas e acompanhamento estratégico"],
        "counts": [2, 2, 3, 0],
    },
    {
        "id": "Q11",
        "dim": "Confiabilidade e risco regulatório",
        "text": "Existe algum score formal de maturidade regulatória?",
        "options": ["Não", "Em desenvolvimento", "Sim, interno", "Sim, validado pela governança"],
        "counts": [5, 1, 1, 0],
    },
    {
        "id": "Q12",
        "dim": "Qualidade e integração dos dados",
        "text": "As obrigações regulatórias estão conectadas aos processos internos e sistemas de origem?",
        "options": ["Não", "Parcialmente mapeadas", "Mapeadas formalmente", "Integradas à arquitetura corporativa"],
        "counts": [1, 5, 1, 0],
    },
    {
        "id": "Q13",
        "dim": "Qualidade e integração dos dados",
        "text": ("Existe mecanismo estruturado de cruzamento de dados entre obrigações regulatórias "
                 "e validações semânticas (consistência lógica) e de confiabilidade das informações?"),
        "options": ["Não existe", "Existe apenas validação técnica de layout", "Existe cruzamento manual entre arquivos",
                    "Existe cruzamento automatizado parcial",
                    "Existe validação estruturada com controles de qualidade e reconciliação de dados"],
        "counts": [2, 2, 3, 0, 0],
    },
]

DIMENSIONS = [
    "Visão executiva e governança",
    "Gestão de críticas e reincidência",
    "Confiabilidade e risco regulatório",
    "Qualidade e integração dos dados",
]

# Pesos das dimensões no score geral. Qualidade e integração dos dados pesa mais
# por ser o foco da Resolução Conjunta sobre qualidade de dados.
DIM_WEIGHTS = {
    "Visão executiva e governança": 0.25,
    "Gestão de críticas e reincidência": 0.20,
    "Confiabilidade e risco regulatório": 0.25,
    "Qualidade e integração dos dados": 0.30,
}

# Meta de score por porte (calibração proporcional ao porte). Valores ilustrativos,
# a calibrar com especialistas e dados reais.
TARGET_BY_SEGMENT = {
    "Banco S3": 75,
    "Banco S4": 65,
    "Cooperativa de crédito S3": 70,
    "Cooperativa de crédito S4": 60,
    "Cooperativa de crédito S5": 50,
    "Fintech regulada": 60,
}

MATURITY_LEVELS = [
    (0, "Inicial", "Processos ad hoc, sem visão consolidada."),
    (20, "Reativo", "Foco em prazo; problemas percebidos após o regulador."),
    (40, "Estruturado", "Controles definidos, mas manuais ou parciais."),
    (60, "Gerenciado", "Indicadores formais e automação relevante."),
    (80, "Otimizado", "Governança contínua, preditiva e integrada à arquitetura."),
]

# Ações de evolução. Cada ação está ligada à pergunta que ela faz avançar um nível
# na escala de maturidade; o plano de evolução usa isso para projetar o score.
ACTIONS = [
    {"q": "Q1", "acao": "Consolidar a visão geral de aderência regulatória numa fonte única, com apoio sistêmico."},
    {"q": "Q2", "acao": "Disponibilizar dashboard executivo consolidado para a diretoria."},
    {"q": "Q3", "acao": "Definir indicadores estratégicos padrão de aderência e apresentá-los ao conselho."},
    {"q": "Q10", "acao": "Registrar metas anuais e acompanhar a evolução histórica do score."},
    {"q": "Q4", "acao": "Centralizar o registro de críticas e rejeições do regulador por documento e tipo de erro."},
    {"q": "Q5", "acao": "Medir a taxa de reincidência por obrigação e responsável de forma automatizada."},
    {"q": "Q8", "acao": "Priorizar correções por impacto e recorrência, com critérios definidos."},
    {"q": "Q6", "acao": "Formalizar um índice de confiabilidade regulatória acompanhado pela gestão."},
    {"q": "Q7", "acao": "Substituir a avaliação de risco por percepção por uma matriz baseada em dados históricos."},
    {"q": "Q9", "acao": "Ampliar o sistema atual para além de calendário e validação de layout."},
    {"q": "Q11", "acao": "Instituir o score formal de maturidade regulatória, validado pela governança."},
    {"q": "Q12", "acao": "Mapear cada campo dos CADOCs até o sistema de origem (data lineage)."},
    {"q": "Q13", "acao": "Automatizar o cruzamento entre documentos (ex.: balancete × SCR) antes do envio."},
]

ACTION_STATUS = ["Não iniciada", "Em andamento", "Concluída"]

# Histórico fictício de uma cooperativa S4 para demonstrar o monitoramento.
DEMO_HISTORY = [
    {"Data": "2025-12-31", "Rótulo": "4º tri 2025", "Visão executiva e governança": 33.3,
     "Gestão de críticas e reincidência": 44.4, "Confiabilidade e risco regulatório": 25.0,
     "Qualidade e integração dos dados": 25.0, "Críticas do regulador": 14, "Consistência entre CADOCs (%)": 78},
    {"Data": "2026-03-31", "Rótulo": "1º tri 2026", "Visão executiva e governança": 41.7,
     "Gestão de críticas e reincidência": 55.6, "Confiabilidade e risco regulatório": 33.3,
     "Qualidade e integração dos dados": 33.3, "Críticas do regulador": 11, "Consistência entre CADOCs (%)": 84},
    {"Data": "2026-06-30", "Rótulo": "2º tri 2026", "Visão executiva e governança": 50.0,
     "Gestão de críticas e reincidência": 55.6, "Confiabilidade e risco regulatório": 41.7,
     "Qualidade e integração dos dados": 45.8, "Críticas do regulador": 9, "Consistência entre CADOCs (%)": 90},
    {"Data": "2026-09-30", "Rótulo": "3º tri 2026", "Visão executiva e governança": 50.0,
     "Gestão de críticas e reincidência": 66.7, "Confiabilidade e risco regulatório": 50.0,
     "Qualidade e integração dos dados": 58.3, "Críticas do regulador": 6, "Consistência entre CADOCs (%)": 94},
]
