# CadocScore

Protótipo da plataforma de maturidade regulatória para instituições financeiras
(TCC FIAP · MBA Arquitetura de Soluções · Turma 8ASOR).

## Problema endereçado

Ausência de um modelo estruturado que permita **medir, monitorar e evoluir** a maturidade regulatória das
instituições financeiras, considerando **qualidade, confiabilidade e integração** dos dados regulatórios.

## Páginas

- **Início:** o problema e como o protótipo o endereça.
- **1. Medir (diagnóstico):** 13 perguntas em 4 dimensões, score de 0 a 100, nível e comparação com a meta do porte e com o benchmark da pesquisa. O resultado pode ser registrado no monitoramento.
- **2. Monitorar (evolução):** histórico de avaliações, evolução do score e das dimensões, críticas do regulador e consistência entre CADOCs. Há um histórico de exemplo e importação/exportação em CSV.
- **3. Evoluir (plano de ação):** ações priorizadas pelo ganho no score, com responsável, prazo e status, e score projetado conforme as ações são concluídas.
- **Qualidade (validação entre CADOCs):** demonstração do cruzamento entre documentos. O índice de consistência alimenta o monitoramento.
- **Metodologia do score:** dimensões, pesos, níveis, metas e lógica do plano.

O protótipo não tem banco de dados: o histórico fica na sessão e é salvo e carregado por CSV.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub e envie o conteúdo desta pasta (`app.py`, `brand.py`, `data.py`, `scoring.py`, `charts.py`, `requirements.txt`, `assets/` e `.streamlit/`).
2. Acesse https://share.streamlit.io, entre com a conta do GitHub e clique em **Create app**.
3. Escolha o repositório e a branch e informe `app.py` como arquivo principal.
4. Clique em **Deploy**. O app fica disponível num endereço `*.streamlit.app`.

## Onde ajustar

- Perguntas, benchmark da pesquisa, pesos, metas por porte, ações e histórico de exemplo: `data.py`.
- Regras de cálculo do score: `scoring.py`.
- Gráficos: `charts.py`.
- Identidade visual (logo, cores, fontes, componentes): `BRAND.md`, `brand.py`, `assets/` e `.streamlit/config.toml`.

Pesos e metas por porte são hipóteses do grupo e devem ser validados.
