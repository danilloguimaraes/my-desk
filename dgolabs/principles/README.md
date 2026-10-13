# Principles (dgolabs)

| campo | valor |
|---|---|
| situacao | ativa |
| papel | Criador e Operador |
| estado | Em andamento — Épico 1 (Debt) mergeado; Ledger/Read Model pendente |

| campo | valor |
|---|---|
| situacao | ativa |
| papel | Criador e Operador |
| estado | Em andamento — Épico 1 (Debt) mergeado; Ledger/Read Model pendente |

Sistema pessoal de gestão do Capital Disponível — máquina consultiva de alocação entre Desobstrução de Fluxo (amortização de consignados) e Tese de Investimento (carteira de FIIs rumo a R$ 100k). Vocabulário ubíquo e fonte semântica única em `CONTEXT.md` do repo.

- **Repo:** `/home/danillo/workspace/dgolabs/principles` ([dgolabs/principles](https://github.com/dgolabs/principles))
- **Meu papel:** Criador e Operador do produto
- **Unidade de acompanhamento:** Épico (`level/epic` no GitHub), 6 épicos no roadmap (`docs/plans/README.md`)

## Contexto

Arquitetura event-driven com ports/adapters (ADR 0003), backend Python + FastAPI + SQLAlchemy Core + Kafka self-contained, frontend a portar do protótipo HTML para Vite. Ciclo EBS de 5 fases completo em `ebs/` (matriz PAT, guidelines, 3 ADRs). Homologação é por épico, com Operador validando critério de aceite antes de liberar o próximo.

Estado dos épicos:

| Épico | Tema | Issue | Estado |
| :--- | :--- | :--- | :--- |
| 0 | Fundação Event-Driven | #1 | Concluído (EventBus, DomainEvent, schema) |
| 1 | Passivos & Alforria | #2 | Em andamento — Debt mergeado (#10), Ledger/Read Model pendente |
| 2 | Alocação & Projeção | #3 | Não iniciado |
| 3 | Ingestão B3 + LLM | #4 | Não iniciado |
| 4 | Governança & Ideias | #5 | Não iniciado |
| 5 | Operação Completa (Kafka + Frontend + SSE) | #6 | Parcial — compose self-contained v0 entregue via #23 |

## Linha do tempo recente

- 26/09/2026 — Frente criada no my-desk; primeira sincronização a partir do estado do repo.
- 14/09/2026 — Self-contained v0 entregue: `docker compose up` sobe Kafka KRaft + FastAPI `/health` + bootstrap de schema + nginx servindo protótipo (#23).
- 13/09/2026 — Módulo Debt mergeado: Virada de Mês idempotente, amortização, ranking IDF, seed real com 13 contratos (R$ 3.291,86 de dreno consignado em 12 ativos) (#10). Fix posterior torna virada e amortização atômicas, publicando eventos só após commit.
- 12/09/2026 — Fundação event-driven: porta `EventBus`, `InMemoryEventBus`, testes de contrato reutilizáveis (#8); schema SQLAlchemy Core com 10 tabelas e engine factory SQLite (#9).
- Início de set/2026 — Conops, ciclo EBS completo (fases 1–5), ADRs 0001–0003, modelo C4, contrato de API (17 endpoints), protótipo web interativo com tema light/dark.
