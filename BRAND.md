# Identidade visual CadocScore

## Conceito

**"Da obrigação à maturidade regulatória."**

O CadocScore transforma o envio de CADOCs, hoje uma obrigação operacional, em governança mensurável. A marca
comunica três ideias:

- **Medição confiável:** o símbolo é um medidor (gauge) com o ponteiro na zona alta.
- **Evolução:** o medidor vai do cinza-azulado (reativo) ao verde (maduro), como os três pilares Medir → Monitorar → Evoluir.
- **Solidez institucional:** a base em azul-marinho, a cor do universo regulatório e financeiro, transmite seriedade e estabilidade.

## Logo

| Arquivo | Uso |
|---|---|
| `assets/logo_dark.svg` / `.png` | Logo completo com o descritor "Maturidade regulatória", sobre fundo escuro |
| `assets/logo_light.svg` / `.png` | Logo completo sobre fundo claro (documentos, slides) |
| `assets/logo_sidebar.svg` / `.png` | Versão sem descritor para tamanhos pequenos (barra lateral do app) |
| `assets/icon.svg` / `.png` | Símbolo isolado (avatar, ícone da sidebar recolhida) |
| `assets/favicon.png` | Favicon 64 × 64 |

**Regras:**
- O nome é sempre escrito junto, com as duas palavras destacadas: **Cadoc** (branco ou marinho) + **Score** (verde).
- Mantenha ao redor do logo uma área livre equivalente à metade da altura do símbolo.
- Não distorça, não mude as cores do medidor e não aplique o logo sobre fotos ou fundos com pouco contraste.
- Abaixo de 120 px de largura, use a versão sem descritor ou só o símbolo.

## Cores

### Marca

| Nome | Hex | Uso |
|---|---|---|
| Marinho regulador | `#0B2545` | Símbolo, barra lateral, faixa de destaque (hero) |
| Azul score | `#1C5CAB` | Botões, links, ações principais (contraste 6,6:1 com branco) |
| Verde conformidade | `#1BAF7A` | "Score" no logo, destaques sobre fundo escuro, evolução |
| Verde texto | `#0B7A54` | Verde para textos sobre fundo claro (contraste ≥ 4,5:1) |

### Neutras

| Nome | Hex | Uso |
|---|---|---|
| Fundo | `#F7F9FC` | Fundo das páginas |
| Superfície | `#FFFFFF` | Cartões e indicadores |
| Fundo secundário | `#EAF0F7` | Campos, cabeçalhos de tabela |
| Linha | `#D5DEE9` | Bordas e divisórias |
| Texto | `#0B1B2E` | Texto principal (16,5:1) |
| Texto secundário | `#5B6B80` | Legendas e rótulos (5,2:1) |

### Gráficos

Paleta categórica validada para daltonismo (usar sempre nesta ordem):
`#2a78d6` · `#eb6834` · `#1baf7a` · `#eda100` · `#e87ba4` · `#008300` · `#4a3aa7` · `#e34948`

- Uma série: azul `#2a78d6`. Comparação (atual × referência): azul + laranja `#eb6834`.
- Status: crítico `#d03b3b`, sempre acompanhado de ícone e texto, nunca só a cor.
- O verde e o amarelo da paleta ficam abaixo de 3:1 sobre o fundo, por isso os gráficos que os usam levam rótulos diretos ou uma tabela.

## Tipografia

| Uso | Fonte | Peso |
|---|---|---|
| Títulos e logo | **Plus Jakarta Sans** | 800 (títulos), 700 (subtítulos) |
| Textos, números e interface | **Inter** | 400 (texto), 600 (rótulos), 700 (indicadores) |

As duas fontes são gratuitas (Google Fonts). A alternativa no Windows é Segoe UI.

## Elementos da interface

- **Selo (kicker):** pílula verde-clara em caixa alta acima do título da página, indicando o pilar (ex.: "PILAR 1 · MEDIR").
- **Hero:** faixa em gradiente marinho com um anel verde translúcido, só na página inicial.
- **Bloco do problema:** cartão branco com borda esquerda verde.
- **Cartões dos pilares:** número em quadrado marinho + título em Plus Jakarta Sans.
- **Indicadores:** cartões brancos com borda fina e cantos de 0,8 rem. Minigráficos mostram a tendência no monitoramento.
- **Ícones:** Material Symbols (traço simples), como velocímetro para Medir, gráfico para Monitorar e tendência para Evoluir.

## Tom de voz

Direto, técnico sem ser burocrático, orientado a ação. Fale em "sua instituição", use verbos
(medir, monitorar, evoluir) e evite jargão sem explicação.

## Onde está no código

- Tema do Streamlit (cores, fontes, raios, barra lateral): `.streamlit/config.toml`
- Estilos e componentes (hero, selo, cartões, rodapé): `brand.py`
- Cores dos gráficos: `charts.py`
