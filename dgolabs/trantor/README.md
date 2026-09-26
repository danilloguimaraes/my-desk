# Trantor (dgolabs)

**Meu papel:** Criador e Operador — defino o backlog (épicos), dou os vereditos e uso o produto no dia a dia
**Status:** Ativo — v0.11.0 implantada em homologação (coxinha); E12–E19 mesclados em `develop`; 2 épicos abertos (E19 parcialmente, E20) + débito contínuo #144

## Contexto

[`dgolabs/trantor`](https://github.com/dgolabs/trantor) transforma uma URL de issue, PR/MR ou épico (GitHub/GitLab) em uma entrega verificada e revisável sem sair da máquina do operador. Um Worker isola branch e worktree, planeja e implementa com um motor de IA (OpenCode), roda build/lint/test do próprio repositório, repara um número limitado de vezes e consolida tudo num **dossiê**. Nada chega ao remoto sem **veredito** humano.

Criei o projeto porque **desenvolvimento de features e revisão de entregas são as minhas maiores dragas de energia e atenção**. O Trantor existe para absorver esse trabalho e me devolver a decisão, não a digitação. É também o produto que consome as demais frentes dgolabs: as issues de [noesis](../noesis/), prelecao etc. são executadas por ele.

**Os épicos são a fonte primária do backlog.** Cada épico (`level/epic`) registra problema, proposta, invariantes, sub-issues (`level/task`) e a ordem de orquestração; o próprio Trantor os executa (Epic Delivery, ADR-0005/0007). Esta bandeja acompanha os épicos como unidades de trabalho, não as sub-issues.

### Arquitetura em uma linha

Event-sourced (Kafka fonte de verdade, SQLite projeção), Go, dois processos locais: `trantor-api` (SPA React + JSON API) e `trantor-worker` (sistemas de entrega). Forge (`gh`/`glab`) e motor (`opencode`) são subprocessos; o Trantor nunca lê um token.

### Épicos em aberto (26/09/2026)

| Épico | Tema | Sub-issues | Situação |
|---|---|---|---|
| [E19 #130](https://github.com/dgolabs/trantor/issues/130) | Resiliência: erros transitórios do motor e retomada de sub-issue | #131–#133 | **Parcial**: PR [#166](https://github.com/dgolabs/trantor/pull/166) mesclado em 26/09 (E19.1–E19.3: retomada de épico, recusa em falha de qualificação, cauda de baseline); restam #131–#133 |
| [E20 #159](https://github.com/dgolabs/trantor/issues/159) | Veredito de épico com granularidade de sub-issue | — | Aberto em 25/09; disparo após E19 |

E12–E18 concluídos (12–26/09/2026). Épicos E1–E10 e E15 concluídos (14 a 17/09/2026).

### Bugs e dívidas fora de épico

| Issue | Assunto | Relação |
|---|---|---|
| [#91](https://github.com/dgolabs/trantor/issues/91) | Motor alterou o host fora da worktree e a verificação aceitou | Segurança; resolvido estruturalmente por E16 |
| [#74](https://github.com/dgolabs/trantor/issues/74) | Sessão da SPA atrás de proxy (`TRANTOR_TRUSTED_HOSTS`) | **Bloqueia uso via Caddy no Terminus** |
| [#72](https://github.com/dgolabs/trantor/issues/72) | `TestVerifyTopicsIntegration` flaky no CI | Ruído em todo PR |
| [#78](https://github.com/dgolabs/trantor/issues/78) | JSON inválido do modelo eficiente descarta a execução | Parcialmente tratado em PR #116; resto vai para E19 |

### Referências no repositório

- `CONTEXT.md` — vocabulário (Worker, dossiê, veredito, Kind, Activity)
- `docs/adr/` — ADR-0001 a 0023 (0001 Local-Only Autonomy; 0006 Refuse Broken Baseline; 0020 Progress-Bounded Repair; 0022 Pós-publicação; 0023 Autonomia graduada)
- `docs/auditorias/2026-09-21-plano-auditoria-ux-spa.md` — origem de E18
- `docs/design/ux-proposal.md` — proposta de UX da SPA

Operação em homologação (compose, release, deploy) fica na bandeja [dgolabs/terminus/](../terminus/).

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Atores e repositórios consumidores |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto, por épico |
| [DECISOES.md](DECISOES.md) | Decisões de produto/priorização (as arquiteturais ficam nos ADRs) |
| [reunioes/](reunioes/) | Notas de sessões de trabalho e post-mortems de execuções |
| [rascunhos/](rascunhos/) | Épicos, issues e ADRs em preparação |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 26/09/2026 | PR #166 (retomada de épico retido, recusa em falha de qualificação, cauda de baseline, snapshot de auto-merge) mesclado a `develop`; CI do e2e caiu por pressão no karol2 e passou no re-run |
| 26/09/2026 | E14, E16, E17, E18 mesclados a `develop` (PRs #155, #156, #158, #165); #130 solicitado duas vezes (duas execuções coexistiram) e ficou retido por baseline vermelha intermitente |
| 25/09/2026 | Bandeja atualizada: #84 (E12) confirmada como entregue via PR #134; todas as issues de E12 e E13 fechadas |
| 22/09/2026 | Bandeja criada a partir do estado do repositório (issues, PRs, ADRs, releases) |
| 22/09/2026 | E13 mesclado em `develop` (PR #142, 6/6 sub-issues); E12 mesclado com entrega parcial (PR #134, 4/5 — #84 falhou por `model_overloaded` mas foi recuperada e incluída no merge) |
| 22/09/2026 | Release v0.9.0 (só docs: auditoria UX); homologação atualizada via Terminus (PR #34) |
| 21/09/2026 | E19 aberto a partir da falha de #84; auditoria de UX da SPA (PR #119) gera E18; E17 stepwise implementation (PR #114); CI migra para runner próprio arm64 `karol2` (PR #115) |
| 17/09/2026 | E15 Forge Least Privilege concluído; E16 Bounded Self-Repair por progresso (PR #111, ADR-0020) |
| 14/09/2026 | E1–E10 fechados: MVP completo (fundação, bus, ports, worker, API/Web, review, epic delivery, operação, stages, correções do primeiro uso) |
