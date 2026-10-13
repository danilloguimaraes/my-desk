# Pendências — Terminus

Formato: `- [ ] ação — @responsável — prazo — origem`

## Urgente

- [ ] Aplicar o ADR-0010 (status: proposto): subir o Pool (3 Servers + 2 Clients) e rodar os Jobs de Plataforma e Produção — @Danillo — sem prazo — origem: https://github.com/dgolabs/terminus/blob/main/docs/adr/0010-pool-nomad-plataforma-producao-ambientes-efemeros.md — crítica

## Em aberto

### Refundação Nomad (pós-PR #36)

- [ ] Fechar issue #1 (migração do trantor para api + worker foi absorvida pela refundação; confirmar e fechar) — @Danillo — 2026-10-03 — origem: https://github.com/dgolabs/terminus/issues/1
- [ ] Migrar dados de Plataforma (Kafka/Postgres) dos volumes compose para Host Volumes do Nomad — @Danillo — 2026-10-03 — origem: README.md
- [ ] CI de branch nos Produtos para viabilizar Ambientes Efêmeros (`jobs/ephemeral/` está vazio; exige imagem com tag de branch) — @Danillo — 2026-10-03 — origem: README.md

### Dores de operação (reavaliar à luz da refundação)

- [ ] **Versão rodando por ambiente**: Nomad (`nomad job status`) + Consul podem ser a fonte de verdade; reavaliar a dor após aplicar o Pool — @Danillo — 2026-10-03 — origem: reunioes/2026-09-22-dores-versoes-ambientes.md
- [ ] **Catálogo de versões por produto**: tags espalhadas em 5 repos + GHCR; nada cruza publicado × promovido × rodando — @Danillo — 2026-10-03 — origem: reunioes/2026-09-22-dores-versoes-ambientes.md
- [ ] **Implantar versão em ambiente específico**: parcialmente respondido por `jobs/prod/` vs `jobs/ephemeral/`; falta prática de Ambientes Efêmeros — @Danillo — 2026-10-03 — origem: reunioes/2026-09-22-dores-versoes-ambientes.md

### Releases e produtos fora do Pool

- [ ] Destravar sync do vault Obsidian do **noesis** (fix do syncthing em 24/09 tratou a restauração do cofre; confirmar com o Operador se o sync está resolvido ponta a ponta) — @Danillo — sem prazo — [noesis/PENDENCIAS](../noesis/PENDENCIAS.md)
- [ ] Destravar CI/publish de **prelecao**, **principles** (api + web) e **aurora** para tirá-los de `legacy/apps/` e entrar no Pool — @Danillo — sem prazo — [inventário](https://github.com/dgolabs/terminus/blob/main/docs/inventory.md)

### Operação do Pool

- [ ] Definir rotina de verificação de drift repo × Pool (o CONTEXT declara isso como escopo, ainda não há mecanismo) — @Danillo — sem prazo — [README](README.md)
- [ ] Documentar/automatizar atualização do DNS Cloudflare quando o IP Tailnet do `coxinha` mudar — @Danillo — sem prazo — [inventário](https://github.com/dgolabs/terminus/blob/main/docs/inventory.md)
- [ ] Limpeza periódica de worktrees do trantor e checagem da retenção Kafka (7 dias) — @Danillo — recorrente — [inventário](https://github.com/dgolabs/terminus/blob/main/docs/inventory.md)

### Futuro

- [ ] Decidir provedor dos Workers de burst e iniciar `provision/envs/burst/` — @Danillo — sem prazo — ADR-0002 (legado, pendências)
- [ ] Distribuir a Plataforma para além do `coxinha` quando os Produtos estiverem em Nomad (hoje `constraint` mantém ponto único de falha) — @Danillo — sem prazo — ADR-0010 (alternativas)

## Concluídas

<!-- mover para cá com data de conclusão -->

- [x] Migrar `apps/trantor/compose.homolog.yml` para o Trantor Go — resolvido pela refundação (PR #36): trantor roda como `jobs/prod/trantor.nomad` (api + worker), tag v0.11.0 — concluída em 24/09/2026
- [x] Destravar imagem publicada do **noesis** — resolvido: `ghcr.io/dgolabs/noesis:0.8.1` em `jobs/prod/noesis.nomad` — concluída em 24/09/2026
- [x] Workflows de deploy no runner self-hosted `karol1` e promoção `develop → main` (PR #30) — @Danillo — concluída em 21/09/2026
- [x] Release noesis 0.8.1 — concluída em 19/09/2026
- [x] Release trantor v0.6.0 — concluída em 18/09/2026
