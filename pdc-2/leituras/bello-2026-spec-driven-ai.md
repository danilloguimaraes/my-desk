# Spec-Driven AI: A Multiagent Framework for Specification-Centric SDLC Automation

**Autores:** João Campista Bello Junior, Daniel Fazzioni, Vitor Mesaque Alves de Lima, Taciana Novo Kudo, Anderson da Silva Soares (CEIA/UFG e UFMS)
**Venue:** ICSME 2026 (tool paper, camera-ready, aceito)
**Status de leitura:** fichado a partir do PDF; leitura crítica pendente
**Screencast:** https://youtu.be/w4QT-nrRgNo
**Recebido em:** reunião de [onboarding 11/09](../reunioes/2026-09-11-onboarding-frente-2.md)

## Em uma frase

Apresenta o ecossistema de duas ferramentas do projeto — SDLC Orchestrator e SDLC Context Platform (Pattern Manager) — que trata especificações como contratos verificáveis e entrega contexto governado a agentes de código via MCP.

## Problema

Assistentes de código são code-centric: fracamente conectados a requisitos, decisões arquiteturais, padrões organizacionais e quality gates. Em manutenção/evolução isso gera drift, perda de rastreabilidade e violação de padrões.

## Arquitetura

| Componente | Stack | Responsabilidade |
|---|---|---|
| SDLC Orchestrator | TypeScript, schemas para validar saída dos agentes | Agentes de discovery, risco, tiering, PM, UX/UI, arquitetura (solução/software/dados), segurança, DevOps, compliance, QA, tech lead, crítico, auditor. Gates HITL, eventos de auditoria, export de bundle de artefatos Markdown (`spec.md`, `design.md`, `plan.md`, `tasks.md`) |
| SDLC Context Platform | Fastify + TypeScript + Zod; PostgreSQL + pgvector; MinIO; Redis/BullMQ | Registro de projetos/repos, ingestão de artefatos, indexação de docs e código, grafo, governança de padrões, baselines, validação de aderência, jobs em background, MCP/HTTP. Dashboard "PatternOps" |

Ferramenta MCP principal: `context.prepare_for_agent(company, project, repository, stage, request, change_type, budget)` → JSON estruturado com padrões, arquivos, chunks, quality gates e avisos de frescor.

## Knowledge Graph (relevante ao meu grupo)

- Grafo "LLM-enriched" construído a partir de código, docs, padrões e artefatos de governança.
- **Nós:** arquivos, módulos, elementos arquiteturais, padrões, especificações.
- **Arestas:** dependências estruturais, relações semânticas, evidência de aderência, links de rastreabilidade.
- **Usos:** sumarização do repositório, análise de impacto, descoberta de arquivos relacionados, expansão de contexto.
- O rebuild de contexto do repositório orquestra: indexação → embeddings → **execução do Graphify** → import do grafo → validação de aderência. Ou seja, a construção do grafo depende de uma ferramenta externa chamada Graphify (verificar no código).
- Estados do repositório: `pending`, `indexing`, `indexed`, `failed`, `stale`.
- Embeddings: modo local usa hash determinístico; produção usa provider OpenAI-compatible.

## Formalização (Sec. IV.F)

Score de recuperação por item x ∈ D ∪ F ∪ P:

    s(q,x) = α·sim(q,x) + β·m(q,x) + γ·g(x,G)

sim = similaridade de embedding; m = compatibilidade de metadados (stage, tipo de mudança, stack, categoria); g = relevância derivada do grafo (vizinhança).

Seleção sob orçamento B de tokens: maximizar Σ s(q,x) sujeito a Σ tokens(x) ≤ B.

Payload MCP: M(q) = ⟨π, b, P_q, D_q, F_q, G_q, A_q, R_q⟩ (perfil, baseline, padrões, docs, arquivos, grafo, aderência, regras/gates).

Aderência determinística: adh(r,b) = 100·(1 − Σ w_p·v(p,r) / Σ w_p), w_p por severidade e obrigatoriedade.

## Governança de padrões

Padrões: default, organização, projeto. Origem: biblioteca padrão, docs, criação humana, inferência do repositório. Baselines definem o conjunto efetivo. Validação de aderência é **determinística** (regras estruturais: camadas service/repository, migrations, testes, logging). Análise estática, checagem semântica e explicação via LLM ficam como trabalho futuro.

## Pontos de atenção / dúvidas para o grupo

1. Como g(x,G) é calculado de fato na implementação? O paper não detalha (o segundo paper detalha mais: distância ponderada + decaimento exponencial).
2. O que é o Graphify e qual formato de grafo ele exporta? Como o "enriquecimento com LLM" é feito e onde persiste?
3. O grafo é global por repositório; não há menção a detecção de comunidades (Leiden), mencionada na reunião como direção. Possível ponto de contribuição.
4. Sem avaliação empírica — é tool paper com demonstração (adicionar campo `status` a uma entidade `order`).

## Relação com outros trabalhos

Spec Kit, Kiro, Tessl (SDD industrial); MetaGPT, ChatDev, AgentCoder, SWE-agent (multiagente); RepoAgent e Athale & Vaddina 2025 (KG para geração repo-level) — este último é referência direta para o grupo de grafo.
