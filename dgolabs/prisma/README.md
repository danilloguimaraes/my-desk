# Prisma (dgolabs)

| campo | valor |
|---|---|
| situacao | ativa |
| papel | Criador e Operador |
| estado | Setup metodológico concluído; 7 épicos mapeados (#1–#7), 14 tasks `agent/ready` (#8–#21); nenhuma task iniciada |

**Meu papel:** Criador e Operador — defino épicos, homologo gates de qualidade e executo via agentes HITL
**Status:** Setup metodológico concluído; 7 épicos mapeados (#1–#7), 14 tasks `agent/ready` (#8–#21); nenhuma task iniciada

## Contexto

[`dgolabs/prisma`](https://github.com/dgolabs/prisma) é uma **plataforma de gestão de especializações autodidatas** (Prisma = *Platform for Research-Integrated Specialization Management & Autodidact Autonomy*).

Criei o projeto porque **consolidar uma especialização exige método, não só disciplina**. O Prisma estrutura trilhas de estudo com excelência técnica, cobre a engenharia e a utilização do tema, e conduz o aprendizado até a fronteira do conhecimento do domínio — usando a metodologia S0–S10 Research-to-Expertise como espinha dorsal.

**A unidade de acompanhamento é o épico** (`level/epic`). Cada épico registra problema, sub-issues (`level/task`) e rastreabilidade N/RF/RNF/UX/UI. Os agentes executam as folhas via `/issue N` ou `/epic N`; esta bandeja acompanha os épicos como unidades de trabalho e registra as decisões de produto e priorização.

### Arquitetura em uma linha

Go binário único + SQLite embarcado (sem CGO) + HTMX + `embed.FS` + CSS nativo (tokens). Interface em dois eixos: Administrador (design-time, S0–S10) e Autodidata (run-time).

### Épicos em aberto (26/09/2026)

| Épico | Tema | Sub-issues | Situação |
|---|---|---|---|
| [E1 #1](https://github.com/dgolabs/prisma/issues/1) | Design System, Tokens e Shell de Interface (UX/UI Base) | #8, #9, #10, #11 | **Pronto para iniciar** — plano de paralelismo Fase C definido |
| [E2 #2](https://github.com/dgolabs/prisma/issues/2) | Fundação do Sistema e Modelo Relacional (Backend Base) | #13, #15, #16, #18 | Pronto — Fase A/B1∥B2/C |
| [E3 #3](https://github.com/dgolabs/prisma/issues/3) | Portfólio de Especializações (Dashboard & Listagem) | #12, #14, #17 | Pronto |
| [E4 #4](https://github.com/dgolabs/prisma/issues/4) | Navegador Curricular e Acervo Bibliográfico | #19, #20, #21 | Pronto |
| [E5 #5](https://github.com/dgolabs/prisma/issues/5) | Diário de Execução, Evidências e Dúvidas (Run-Time) | a detalhar | Aguardando detalhamento |
| [E6 #6](https://github.com/dgolabs/prisma/issues/6) | Orquestrador Metodológico e Gates (S0–S10) | a detalhar | Aguardando detalhamento |
| [E7 #7](https://github.com/dgolabs/prisma/issues/7) | Interoperabilidade Markdown / SQLite | a detalhar | Aguardando detalhamento |

### Dependências entre épicos

E1 (UX/UI base) e E2 (backend base) são fundacionais e independentes entre si. E3 depende de E1+E2. E4 depende de E3. E5/E6 dependem de E4. E7 é transversal e fecha o ciclo.

### Referências no repositório

- `AGENTS.md` — governança de agentes HITL, fluxo issue/épico/híbrido, gates de verificação
- `docs/epicos/README.md` — mapa épico → issue GitHub → rastreabilidade
- `docs/epicos/EPICO_N-sub-issues.md` — decomposição de E1–E4 com ordem de execução e paralelismo
- `docs/matriz-rastreabilidade.md` — N01–N10 × RF01–RF18 × RNF01–RNF12 × UX/UI
- `docs/visao_e_requisitos.md` — visão do produto
- `@00-protocol.md` — metodologia S0–S10 Research-to-Expertise Advisor

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Atores (Administrador, Autodidata, Agente) |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto, por épico |
| [DECISOES.md](DECISOES.md) | Decisões de produto/priorização (arquitetura fica no repo) |
| [reunioes/](reunioes/) | Notas de sessões de trabalho e homologação |
| [rascunhos/](rascunhos/) | Épicos, issues e specs em preparação |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 26/09/2026 | Bandeja criada; setup metodológico concluído (docs, épicos E1–E4 decompostos, CI, governança HITL) |
| 20/09/2026 | Épico 1 planejado com paralelismo controlado (Fase C: tasks #10 ∥ #11) |
| 19/09/2026 | Sub-issues de E2, E3, E4 mapeadas; Project V2 #11 vinculado |
| 19/09/2026 | Catálogo de épicos (#1–#7) criado no GitHub com rastreabilidade |
| 19/09/2026 | Documentação granular organizada: N01–N10, RF01–RF18, RNF01–RNF12, UX01–UX03, UI01–UI03 |
