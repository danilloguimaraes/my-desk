# Specification-Guided Multiagent AI for Context-Governed SDLC Automation and Repository-Aware Software Generation

**Autores:** João Campista Bello Junior, Vitor Mesaque Alves de Lima, Taciana Novo Kudo, Anderson da Silva Soares (CEIA/UFG e UFMS)
**Venue:** submetido ao ICTAI 2026 — **EM AVALIAÇÃO. CONFIDENCIAL. NÃO DIVULGAR EXTERNAMENTE.**
**Status de leitura:** fichado a partir do PDF; leitura crítica pendente
**Artefatos anônimos:** anonymous.4open.science `sdlc-agentico-E2D7` e `sdlc-context-platform-7658`
**Recebido em:** reunião de [onboarding 11/09](../reunioes/2026-09-11-onboarding-frente-2.md)

## Em uma frase

Formaliza a Context Platform como espaço de conhecimento tipado com grafo multigrafo atribuído, define a montagem de contexto como seleção de evidência sob orçamento, e mostra em estudo A/B/C (Django CSP) que contexto curado do repositório leva a taxa de testes de 0,04 → 0,97 mantendo executor e revisão fixos.

## Contribuições declaradas

1. Arquitetura implementada: 16 agentes especializados em LangGraph hub-and-spoke, guards de roteamento determinísticos, gates G1–G5, fronteiras MCP tipadas (15 tools, envelope `mcp.context.v1`, payload `context.pack.v1`).
2. Formalização do contexto de repositório como seleção orçada sobre espaço tipado, com proximidade em grafo, evidência obrigatória, proveniência, cobertura, frescor e redundância.
3. Estudo exploratório com oráculo separado (testes do projeto), comparando intent-only (A), spec-only (B), spec + contexto curado congelado (C).

## Distinção metodológica central

**Suficiência de informação** (o contexto certo muda o resultado do executor?) vs **eficácia de recuperação** (a plataforma consegue encontrar esse contexto sozinha?). O estudo mede só a primeira: o pacote C é curado manualmente e congelado. A recuperação ao vivo (substituir X^C por X*) fica como trabalho futuro.

## Modelo formal (Sec. III) — núcleo para o grupo de grafo

**Espaço de conhecimento:** K_r = ⟨Ω_r, G_r, Π_r⟩, com Ω_r = F_r ⊎ D_r ⊎ P_r ⊎ B_r (código, docs, padrões aprovados, baselines), G_r relações tipadas, Π_r proveniência/frescor.

**Proveniência por item:** π(x) = ⟨r, rev, path, span, kind, extractor, t⟩. Permite rejeitar itens stale ou de outra revisão.

**Grafo tipado (Eq. 2):** G_r = (V_r, E_r, τ_V, τ_E, φ_r), multigrafo atribuído.
- Tipos de nó: file, symbol, test, document, pattern.
- Relações: contains, declares, imports, calls, references, tests, documents, constrains.
- Atributos: revisão, span, linguagem, proveniência, frescor. Arestas paralelas permitidas.

**Proximidade (Eq. 3):** g(v | A) = max_{a∈A} exp[−λ·d_ω(a,v)], onde A são âncoras extraídas de símbolos/arquivos/requisitos da intenção e da spec, d_ω é caminho mínimo ponderado por tipo de relação. Expansão limitada a distância k. Pesos ω permitem que aresta test→symbol ou call valha mais que co-ocorrência em documento.

**Seleção (Eq. 4–5):**

    q(x) = α·d(x) + β·ℓ(x) + γ·g(x) + δ·m(x) + η·p(x) + ζ·f(x)
    X* = argmax Σ q(x) + ν·cov(X,s) − μ·Σ sim(x,y)   s.t. cost(X) ≤ B, M ⊆ X

(dense, lexical, grafo, padrão obrigatório, proveniência, frescor; cobertura de itens da spec; penalidade de redundância; itens obrigatórios sempre incluídos.)

**Implementação real (Tabela III):** não resolve o objetivo combinatório online. Faz: classificar request → recuperar dense + lexical com reciprocal-rank fusion → boost limitado por matches no grafo canônico → inserir padrões da baseline → caps por fonte e truncamento → emitir pacote validado por schema.

**Diagnóstico de falha:** pacote sem símbolo → falhou recuperação/extração do grafo; pacote com símbolo ignorado → falha do executor; passa testes mas viola regra → problema de aderência.

## Estudo empírico

| Repo | Alvo | Contrato | A | B | C |
|---|---|---|---|---|---|
| Django | CSP | privado (middleware–decorator) | 0,00 | 0,04 | 0,97 |
| Django | numberformat | utilitário antigo | 0,00 | 0,00 | 0,33 |
| Django | cache middleware | comportamento novo em shell antigo | 0,07 | 0,06 | – |
| Kafka | ACL value classes | público documentado | 0,00 | 1,00 | – |

k = 3, single-shot, sem acesso a arquivo/shell/web além do pacote, referência humana oculta. Sem testes de significância. Só Django CSP tem matriz A/B/C completa. Um dos runs C violou regra de direção de import presente no pacote: evidência disponível não garante aderência.

Leitura: regimes distintos — contrato público pode ser resolvido por spec precisa; contrato privado exige evidência de código/grafo; alvo contaminado não serve para inferência.

## Ameaças reconhecidas

Catálogo pequeno; pacotes não pareados por tokens (efeito pode ser de tamanho/estrutura, não só relevância); curadoria manual; leakage de repositórios públicos; um executor, single-shot.

## Pontos de atenção / oportunidades para o grupo de grafo

1. **Recall de evidência crítica** do grafo ao vivo é o gap explícito do paper: medir se a extração + g(x) recupera os símbolos privados que a curadoria manual incluiu (Tabela VI). Candidato direto a linha de pesquisa.
2. Pesos ω por tipo de relação e λ, k não têm valores reportados — investigar no código e propor calibração.
3. Comunidades (Leiden) não aparecem no modelo; poderiam servir para bounded expansion alternativa à distância k, ou para sumarização de regiões.
4. Enriquecimento LLM do grafo (mencionado no paper 1) não é formalizado aqui; onde entra em τ_E / φ_r?
5. Controles token-matched e irrelevant-context são pedidos explícitos para trabalho futuro.

## Relação com o paper 1

Mesmo sistema; este aprofunda a formalização (grafo tipado, proveniência, orçamento com cobertura e redundância) e adiciona avaliação. O paper 1 (ICSME) é a descrição da ferramenta. Ver [bello-2026-spec-driven-ai.md](bello-2026-spec-driven-ai.md).

## Referências úteis para revisão de literatura do grupo

LocAgent (Chen et al., ACL 2025) — grafo heterogêneo de repositório para localização multi-hop; RepoCoder (EMNLP 2023); Athale & Vaddina 2025 (KG para geração repo-level); Lost in the Middle (Liu et al., TACL 2024) e Context Rot (Chroma 2025) — por que orçamento importa; RRF (Cormack et al., SIGIR 2009).
