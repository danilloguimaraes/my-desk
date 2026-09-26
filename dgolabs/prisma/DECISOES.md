# Decisões — Prisma

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

As decisões **arquiteturais e de governança de agentes** vivem no repositório (`AGENTS.md`, `docs/specs/`, `docs/epicos/`) e não são duplicadas aqui. Este arquivo registra decisões de **produto, priorização e operação** minhas como criador e operador.

---

## 26/09/2026 — Prisma vira frente própria no my-desk

**Contexto:** O Prisma concluiu o setup metodológico (docs granulares, 7 épicos cadastrados, E1–E4 decompostos, CI, governança HITL) e está pronto para entrar em execução. A complexidade (7 épicos, 14 tasks prontas, paralelismo controlado) justifica acompanhamento dedicado ao lado das outras frentes dgolabs.

**Decisão:** Criar a bandeja `dgolabs/prisma/`. Unidade de acompanhamento é o **épico**, alinhado com a convenção das outras frentes. A sequência de ataque começa pelos fundacionais: **E1 (UX/UI) e E2 (Backend)** podem rodar em paralelo porque escrevem arquivos disjuntos; E3 só inicia após ambos.

**Consequências:** A bandeja reflete a ordem de ataque por épico, não a lista de tasks. Tasks individuais só aparecem em `PENDENCIAS.md` quando exigem decisão minha. O paralelismo E1∥E2 exige 2 agentes simultâneos em branches separadas — risco gerenciável via HITL por PR.
