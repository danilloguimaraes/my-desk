# Pendências — Noesis

Formato: `- [ ] ação — @responsável — prazo — origem`

Regra desta bandeja: a unidade de acompanhamento é o **épico**. Sub-issues só aparecem quando exigem decisão ou intervenção minha (falha, veredito, bloqueio).

## Urgente

- [ ] Reconciliar status de **E10.2 #44** — @Danillo — 2026-09-26 — crítica

## Em aberto

### Bloqueio de infraestrutura (Terminus)

- [ ] **#87** Publicar imagem multi-arch no GHCR — workflow de publish no repo do produto — @Danillo — sem prazo — [issue #87](https://github.com/dgolabs/noesis/issues/87) — bloqueia [terminus/PENDENCIAS](../terminus/PENDENCIAS.md)

### Bugs críticos (núcleo do pipeline)

- [ ] **#79** LlmClient: `remote_processing_consented` nunca propagado por S1/S2/S3 — modo Delegated remoto sempre rejeitado — @Danillo (via Trantor) — sem prazo — [issue #79](https://github.com/dgolabs/noesis/issues/79)
- [ ] **#82** SDK: `EventStore.load` trava quando LSO de `reading.events` está presa por transação órfã — @Danillo (via Trantor) — sem prazo — [issue #82](https://github.com/dgolabs/noesis/issues/82)
- [ ] **#83** SDK: modo "plain" para consumidores de fan-out somente-leitura (Edge com grupo efêmero) — @Danillo (via Trantor) — sem prazo — [issue #83](https://github.com/dgolabs/noesis/issues/83)
- [ ] **#85** Vault: WriteConflict inalcançável — permitir re-render explícito ("Regravar no cofre") após Closed — @Danillo (via Trantor) — sem prazo — [issue #85](https://github.com/dgolabs/noesis/issues/85)
- [ ] **#86** Homologação com provedor LLM real (Copilot/OpenRouter): prompts nunca exercitados fora do mock — @Danillo — sem prazo — [issue #86](https://github.com/dgolabs/noesis/issues/86)

### Épico E11 — Backlog Pós-MVP (bloqueado por E10.2/#44)

Ordem sugerida por valor (ver [épico #47](https://github.com/dgolabs/noesis/issues/47)):

1. [ ] **E11.1 #48** Modos Delegated e Deep na esteira e na UI — autonomia do pipeline — @Danillo (via Trantor) — após E10.2 — [issue #48](https://github.com/dgolabs/noesis/issues/48)
2. [ ] **E11.5 #52** Heartbeat de foco humano, `human_minutes` e OverReadingWarning — ética/UX anti-robô — @Danillo (via Trantor) — após E10.2 — [issue #52](https://github.com/dgolabs/noesis/issues/52)
3. [ ] **E11.2 #49** Linha do Tempo Epistêmica (Seminal) e reconstrução de taxonomia (Survey) — análise historiográfica — @Danillo (via Trantor) — após E10.2 — [issue #49](https://github.com/dgolabs/noesis/issues/49)
4. [ ] **E11.3 #50** Ollama como provedor local e `provider_override` por reading — privacidade local-first — @Danillo (via Trantor) — após E10.2 — [issue #50](https://github.com/dgolabs/noesis/issues/50)
5. [ ] **E11.4 #51** Inbound adapters: inbox de filesystem e export do Zotero — conveniência de ingestão — @Danillo (via Trantor) — após E10.2 — [issue #51](https://github.com/dgolabs/noesis/issues/51)
6. [ ] **E11.6 #53** OCR para PDFs escaneados — cobertura de acervo físico — @Danillo (via Trantor) — após E10.2 — [issue #53](https://github.com/dgolabs/noesis/issues/53)
7. [ ] **E11.7 #54** Sugestão de backlinks por embeddings com confirmação individual — descoberta de conexões — @Danillo (via Trantor) — após E10.2 — [issue #54](https://github.com/dgolabs/noesis/issues/54)

### Gate de qualidade (pré-requisito para E11)

### Achados da simulação de uso (26/09/2026, hipóteses — validar antes de virar escopo)

Relatório completo: `rascunhos/2026-09-26-simulacao-uso-elicitron.md` (a mover de `/tmp/opencode/noesis-simulacao-uso.md`).

- [ ] Abrir issue: escapes de impasse — Descartar em `Inbox`, "seguir sem objeções" com Fato quando `InterrogationFailed` definitivo, exibir `last_error` no Gate 1 — @Danillo — sem prazo — simulação P6/P7 (2 abandonos)
- [ ] Abrir issue: evidência textual da âncora (trecho do Paginated Text Store ao redor do bbox no cartão do claim) — acessibilidade e conteúdo matemático — @Danillo — sem prazo — simulação P5/P10
- [ ] Avaliar prompts de S3 por gênero epistêmico (qualitativo/histórico/teórico); Prompt Registry já suporta tipologia — @Danillo — sem prazo — simulação P2/P6/P10
- [ ] Rascunho Local nas réplicas do Gate 3 e alerta de custódia em qualquer estado parado — @Danillo — sem prazo — simulação P8
- [ ] Decidir se "leitor não-autor" (fechar reading sem Nota Permanente, com Fato explícito) entra no escopo — exige ADR; tensiona Human Authoring Lock — @Danillo — sem prazo — simulação P4

### LLM Readiness do repositório (Ondas 2–3)

- [ ] Verificar estabilidade de `vars.CI_RUNNER` (9 das 10 falhas de CI foram em 19/09 durante migração para karol2, jobs sem step executado) — @Danillo — sem prazo — avaliação 26/09
- [ ] Branch protection em `develop`/`main` + CODEOWNERS (backbone / web / infra) — @Danillo — sem prazo — avaliação 26/09
- [ ] Mover relatório da simulação para `rascunhos/` desta bandeja — @Danillo — próxima sessão

### Higiene

- [ ] **#88** Rodapé com direitos — compliance básico — @Danillo — sem prazo — [issue #88](https://github.com/dgolabs/noesis/issues/88)

## Concluídas

<!-- mover para cá com data de conclusão -->

- [x] **E10.2 #44** Homologar hipótese de rigor: validar que o pipeline S1–S4 produz saídas com rigor científico suficiente antes de escalar throughput — @Danillo — concluída em 2026-09-26

- [x] LLM Readiness Onda 1 (AGENTS.md, CONTRIBUTING, PR template, .env.example) — concluída em 2026-09-26
- [x] E1–E10 (MVP Guided) — concluída em 2026-09-16
- [x] Release 0.8.1 — concluída em 2026-09-19
- [x] **#84** Domínio: TriageFailed como Fato — concluída em 2026-09-26
