# Pendências — Trantor

Formato: `- [ ] ação — @responsável — prazo — origem`

Regra desta bandeja: a unidade de acompanhamento é o **épico**. Sub-issues só aparecem quando exigem decisão ou intervenção minha (falha, veredito, bloqueio).

## Urgente

- [ ] Atualizar homologação (coxinha) de v0.11.0 para v0.13.0 no Terminus — @Danillo — sem prazo — crítica

## Em aberto

### Release e homologação

- [ ] Resolver #74 (`TRANTOR_TRUSTED_HOSTS`) para a SPA funcionar atrás do Caddy no Home — @Danillo — sem prazo — [#74](https://github.com/dgolabs/trantor/issues/74)

### Priorização de épicos (ordem proposta, ver DECISOES)

- [ ] **E19** Resiliência do motor e retomada de sub-issue — @Danillo (via Trantor) — próximo — [#130](https://github.com/dgolabs/trantor/issues/130)
- [ ] **E20** Veredito de épico com granularidade de sub-issue — @Danillo (via Trantor) — depois de E19 — [#159](https://github.com/dgolabs/trantor/issues/159)
- [ ] **#144** Legibilidade de identificadores — @Danillo — sem prazo — [#144](https://github.com/dgolabs/trantor/issues/144)

### Higiene

- [ ] Corrigir flaky `TestVerifyTopicsIntegration` (#72) — @Danillo (via Trantor) — sem prazo — [#72](https://github.com/dgolabs/trantor/issues/72)
- [ ] Investigar nil pointer em `TestPostPubCIFailureReopensDecision` — @Danillo — sem prazo — run [35860828310](https://github.com/dgolabs/trantor/actions/runs/35860828310)
- [ ] Abrir issue para dedup de execuções por alvo (repo, número, kind) na intake — @Danillo — sem prazo
- [ ] Considerar `upload-artifact` do `trantor-api.log` no job e2e da CI para diagnóstico de falhas em `karol2` — @Danillo — sem prazo — [.github/workflows/ci.yml](https://github.com/dgolabs/trantor/blob/develop/.github/workflows/ci.yml)
- [ ] Ativar branch protection em `develop` exigindo CI verde — @Danillo — sem prazo
- [ ] Corrigir `scripts/assess.py` da skill `repo-llm-readiness` para varrer subdiretórios de manifesto — @Danillo — sem prazo — TODO em `dgolabs/my-skills/skill/repo-llm-readiness/TODO.md`

## Concluídas

- [x] Cortar v0.13.0 em `develop` (Repository Readiness + ADR-0027) — concluída em 2026-09-26
- [x] Avaliação de prontidão do repositório para agentes (Repository Readiness) — nota 70/100; PRs #167 e #168 aplicados — concluída em 2026-09-26
- [x] Remediar barreira de descoberta do `.env.example` e pin de Node 20 (`.nvmrc` + `engines`) — PR #167 — concluída em 2026-09-26
- [x] Tornar `make lint` obrigatório (falha sem `golangci-lint`; `make lint-install`; bootstrap Ubuntu) — PR #167 — concluída em 2026-09-26
- [x] Decompor `ExecutionPage.tsx` (511 → 140 linhas) em hook + arquivos por estado, sem mudança de comportamento — PR #167 — concluída em 2026-09-26
- [x] ADR-0027 · portão local idêntico ao remoto (formaliza a decisão de gate obrigatório) — PR #168 — concluída em 2026-09-26
- [x] Simulação de uso por 12 personas (método Elicitron) em modo validação — material bruto em `/tmp/opencode/trantor-simulation/`; achados descartados como acionáveis — concluída em 2026-09-26
- [x] E14 Observabilidade (Live Tail, prévia do PR) — concluída em 2026-09-26
- [x] E16 Verificação em container — concluída em 2026-09-26
- [x] E17 Catálogo declarativo de atividades — concluída em 2026-09-26
- [x] E18 Confiança e clareza na SPA — concluída em 2026-09-26
- [x] E19 parcial (PR #166): retomada de épico retido, recusa em falha de qualificação, cauda de baseline vermelha, snapshot de auto-merge — concluída em 2026-09-26
- [x] Registrar post-mortem da execução `01a0c5c4` (E12) em `reunioes/` — concluída em 2026-09-26

<!-- mover para cá com data de conclusão -->

- [x] Fechar/atualizar issues de E12 e E13 — todas já fechadas no GitHub; #84 entregue via PR #134 em 22/09/2026 — concluída em 2026-09-25
- [x] Refazer #84 (E12 · Interface & E2E) — o trabalho foi recuperado e incluído no PR #134; issue fechada como completed em 24/09/2026 — concluída em 2026-09-25
- [x] E13 Autonomia pós-publicação mesclado (PR #142) — concluída em 2026-09-22
- [x] E12 Pós-publicação mesclado parcialmente (PR #134, 4/5) — 5/5 entregues — concluída em 2026-09-22
- [x] E15 Forge Least Privilege — concluída em 2026-09-17
- [x] E1–E10 (MVP) — concluída em 2026-09-14
