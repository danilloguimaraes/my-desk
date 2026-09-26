# Pendências — Noesis

Formato: `- [ ] ação — @responsável — prazo — origem`

Regra desta bandeja: a unidade de acompanhamento é o **épico**. Sub-issues só aparecem quando exigem decisão ou intervenção minha (falha, veredito, bloqueio).

## Urgente

_(vazio)_

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

- [ ] **E10.2 #44** Homologar hipótese de rigor: validar que o pipeline S1–S4 produz saídas com rigor científico suficiente antes de escalar throughput — @Danillo — sem prazo — [issue #44](https://github.com/dgolabs/noesis/issues/44)

### Higiene

- [ ] **#88** Rodapé com direitos — compliance básico — @Danillo — sem prazo — [issue #88](https://github.com/dgolabs/noesis/issues/88)

## Concluídas

<!-- mover para cá com data de conclusão -->

- [x] E1–E10 (MVP Guided) — concluídas em 16/09/2026
- [x] Release 0.8.1 — concluída em 19/09/2026
- [x] **#84** Domínio: TriageFailed como Fato — concluída em 26/09/2026 (commits `fato TriageFailed`, `fan-out … → TriageRequested/TriageFailed`)
