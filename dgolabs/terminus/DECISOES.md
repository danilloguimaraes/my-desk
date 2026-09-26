# Decisões — Terminus

Registro cronológico, mais recente primeiro. Cada entrada: contexto → decisão → consequências.

As decisões **arquiteturais** do projeto vivem nos ADRs do repositório ([`docs/adr/`](https://github.com/dgolabs/terminus/tree/main/docs/adr)) e não são duplicadas aqui. Este arquivo registra decisões de **organização e operação** minhas como Operador.

Resumo dos ADRs para referência rápida:

| ADR | Assunto |
|---|---|
| 0010 | Pool Nomad para Plataforma, Produção e Ambientes Efêmeros (proposto, 23/09/2026) |
| 0001–0009 | Legados em `docs/adr/legacy/` — modelo anterior (Home fixo + compose + deploy.yml); não refletem o estado atual |

---

## 26/09/2026 — Bandeja reescrita após a refundação Nomad

**Contexto:** Em 24/09/2026 o PR #36 refundou o repositório: o modelo Home fixo + compose + `deploy.yml` foi substituído por um Pool Nomad de 5 máquinas (ADR-0010), com Jobs de Plataforma, Produção e Ambientes Efêmeros. A bandeja ainda descrevia o modelo anterior como estado atual, e duas pendências centrais (migração do trantor, imagem do noesis) tinham sido resolvidas pela refundação sem registro.

**Decisão:** Reescrever o README e o PENDENCIAS da bandeja para refletir o Pool Nomad. Pendências resolvidas pela refundação foram movidas para Concluídas com a data do PR, e não apagadas. As três dores de operação de 22/09 foram mantidas em aberto, marcadas para reavaliação após a aplicação do Pool — a arquitetura mudou, mas as dores só se encerram quando houver mecanismo funcionando.

**Consequências:** A próxima ação crítica da frente deixa de ser "migrar compose do trantor" e passa a ser "aplicar o ADR-0010" (todo `apply` é humano). A issue #1 continua aberta no GitHub e vira pendência explícita de fechamento. O resumo de ADRs acima passa a refletir apenas o ADR-0010 como vigente.

---

## 22/09/2026 — Terminus vira frente própria no my-desk

**Contexto:** Implantações e acompanhamento de versões dos produtos dgolabs eram feitos de forma dispersa, sem registro. O repositório resolve a parte técnica (IaC, releases por PR), mas faltava um lugar para acompanhar pendências operacionais, bloqueios de cada produto e o histórico de releases junto com as demais frentes.

**Decisão:** Criar a bandeja `terminus/` com o mesmo padrão das outras frentes. Decisões arquiteturais ficam nos ADRs do repo; aqui só organização/operação.

**Consequências:** Cada release e cada bloqueio de produto passa a ter linha na linha do tempo e em `PENDENCIAS.md`; o painel raiz passa a mostrar a próxima ação crítica desta frente.
