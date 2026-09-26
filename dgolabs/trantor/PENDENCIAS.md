# Pendências — Trantor

Formato: `- [ ] ação — @responsável — prazo — origem`

Regra desta bandeja: a unidade de acompanhamento é o **épico**. Sub-issues só aparecem quando exigem decisão ou intervenção minha (falha, veredito, bloqueio).

## Urgente

_(vazio)_

## Em aberto

### Release e homologação

- [ ] Cortar release v0.10.0 com E12 + E13 (v0.9.0 só levou docs) e abrir `release/trantor-0.10.0` no Terminus — @Danillo — sem prazo — [terminus/PENDENCIAS](../terminus/PENDENCIAS.md)
- [ ] Resolver #74 (`TRANTOR_TRUSTED_HOSTS`) para a SPA funcionar atrás do Caddy no Home — @Danillo — sem prazo — [#74](https://github.com/dgolabs/trantor/issues/74)

### Priorização de épicos (ordem proposta, ver DECISOES)

- [ ] **E19** Resiliência do motor e retomada de sub-issue — restam #131–#133 após PR #166; reabrir solicitação (duas execuções coexistiram em 26/09) — @Danillo (via Trantor) — próximo — [#130](https://github.com/dgolabs/trantor/issues/130)
- [ ] **E20** Veredito de épico com granularidade de sub-issue — @Danillo (via Trantor) — depois de E19 — [#159](https://github.com/dgolabs/trantor/issues/159)
- [ ] **#144** Legibilidade de identificadores — épico de débito contínuo; manter o plano em `docs/plans/2026-09-23-naming-readability-debt.md` — @Danillo — sem prazo — [#144](https://github.com/dgolabs/trantor/issues/144)

### Higiene

- [ ] Corrigir flaky `TestVerifyTopicsIntegration` (#72) — @Danillo (via Trantor) — sem prazo — [#72](https://github.com/dgolabs/trantor/issues/72)
- [ ] Abrir issue para dedup de execuções por alvo (repo, número, kind) na intake — duas execuções do #130 coexistiram retidas em 26/09 — @Danillo — sem prazo
- [ ] Considerar `upload-artifact` do `trantor-api.log` no job e2e da CI para diagnóstico de falhas em `karol2` — @Danillo — sem prazo — [.github/workflows/ci.yml](https://github.com/dgolabs/trantor/blob/develop/.github/workflows/ci.yml)

## Concluídas

- [x] E14 Observabilidade (Live Tail, prévia do PR) — mesclado em 26/09/2026 (PR #155)
- [x] E16 Verificação em container — mesclado em 26/09/2026 (PR #165)
- [x] E17 Catálogo declarativo de atividades — mesclado em 26/09/2026 (PR #156)
- [x] E18 Confiança e clareza na SPA — mesclado em 26/09/2026 (PR #158); decisões R-3 e R-10 tomadas na sessão de 26/09
- [x] E19 parcial (PR #166): retomada de épico retido, recusa em falha de qualificação, cauda de baseline vermelha, snapshot de auto-merge — mesclado em 26/09/2026
- [x] Registrar post-mortem da execução `01a0c5c4` (E12) em `reunioes/` — substituído pelo pós-mortem da retomada de épico retido (26/09/2026) em `docs/plans/` do repositório

<!-- mover para cá com data de conclusão -->

- [x] Fechar/atualizar issues de E12 e E13 — todas já fechadas no GitHub; #84 entregue via PR #134 em 22/09/2026 — concluída em 25/09/2026
- [x] Refazer #84 (E12 · Interface & E2E) — **não precisou**: o trabalho foi recuperado e incluído no PR #134; issue fechada como completed em 24/09/2026 — concluída em 25/09/2026
- [x] E13 Autonomia pós-publicação mesclado (PR #142) — concluída em 22/09/2026
- [x] E12 Pós-publicação mesclado parcialmente (PR #134, 4/5) — **#84 incluída depois; 5/5 entregues** — concluída em 22/09/2026
- [x] E15 Forge Least Privilege — concluída em 17/09/2026
- [x] E1–E10 (MVP) — concluídas em 14/09/2026
