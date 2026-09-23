# Pendências — Denodare

Formato: `- [ ] ação — @responsável — prazo — origem`

## Urgente

- [ ] **#126** Ler `plano-multitenant-daurora.md` (anexo da issue; download só pelo navegador — API de uploads exige Maintainer) e registrar parecer na issue: estratégia de isolamento (banco/schema/linha), JWT com contexto de tenant, impactos em serviços/APIs/persistência — @Danillo — esta semana — [work item #126](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/126), [README](README.md)
- [ ] **#207** Confirmar com Afonso quais dos 3 bloqueantes (map `publication`→news, `ValidateIf`, race de idempotência) seguem abertos após !401 — @Danillo — esta semana — [comentário de 08/09 na #207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207)

## Em aberto

### #126 — Multi-tenant

- [ ] Propor a Afonso o enriquecimento da issue: mover o plano do anexo para `docs/` via MR, explicitar no corpo as decisões em aberto (isolamento por banco/schema/linha, tenant no JWT, tenant default para dados legados) e abrir sub-issues por camada (bff, bChain, front) — @Danillo — junto com o parecer — [nota](reunioes/2026-09-22-analise-workitems.md)
- [ ] Verificar se o modelo de tenant do plano é o mesmo que já nasceu no fluxo M2M da #207 (`oauth_clients` com org/tenant; `m2m_organization`/`m2m_tenant` na V2) para evitar dois modelos de tenant — @Danillo — junto com o parecer — [nota](reunioes/2026-09-22-analise-workitems.md)
- [ ] Após o parecer, propor decomposição em sub-issues por camada (bff, bChain, front) e alinhar com Afonso — @Danillo — após o parecer — [README](README.md)

### #207 — Solicitações de análise M2M (Guaia)

- [ ] Fechar os bloqueantes restantes em MR único (`ValidateIf` allegation/reproduction; ledger/SAVEPOINT + `23505` → replay; `publicationHash` na resposta; `insertNews` dentro do `QueryRunner`) — @Danillo — após confirmação com Afonso — [comentário de 08/09 na #207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207)
- [ ] Revisar o hotfix de migrações aplicado por Afonso em develop e entender a causa — @Danillo — sem prazo — [comentário de 08/09 na #207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207)
- [ ] Acordar escopo dos gaps maiores (timeline, dossiê/PDF, provisioning org/tenant, pricing, outbox M2M): dentro da #207 ou issues novas — @Danillo com Afonso — sem prazo — [README](README.md)

### #217 — Refatoração (sub-issues abertas)

- [ ] #226 Padronização de datas para enriquecimento de IA — @Danillo — sem prazo — [work item #226](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/226)
- [ ] #227 Padronização da paginação para busca de checadores — @Danillo — sem prazo — [work item #227](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/227)
- [ ] #228 Unificação de representações de pedidos sob análise — @Danillo — sem prazo — [work item #228](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/228)
- [ ] #229 Unificação de estruturas de resultados de votação — @Danillo — sem prazo — [work item #229](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/229)
- [ ] #230 Padronização de constantes globais e documentação de migrações — @Danillo — sem prazo — [work item #230](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/230)
- [ ] Decidir o destino das branches paradas `feat-217-refatoracao` e `feature-217-refatoracao` (aproveitar ou apagar) — @Danillo — sem prazo — [README](README.md)

### #154 — Débito residual do épico #138

- [ ] 12.2 `syncRewards`: substituir polling de 30s por evento/claim atômico (escolher opção A, B ou C na MR) — @Danillo — sem prazo — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)
- [ ] 12.1 Pedir acesso ao Grafana para provisionar dashboards das filas (rewards, media_es, configuration_blockchain) — @Danillo — sem prazo — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)
- [ ] 12.1 Dashboard `deploy/grafana/dashboards/async-queues.json` + alertas + seção "Dashboards" no runbook — @Danillo — após acesso ao Grafana — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)
- [ ] 12.3 Claim atômico (`claimNext`) no cron `syncWithElasticsearch` de mídia — @Danillo — sem prazo — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)
- [ ] 12.4 Atualizar status do ADR para Adotado após 12.1–12.3 — @Danillo — após 12.1–12.3 — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)
- [ ] (opcional, fase 2) 12.5 Decidir sobre outbox persistente vs `registerAfterCommit` + EventEmitter — @Danillo com Afonso — sem prazo — [work item #154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154)

## Concluídas

<!-- mover para cá com data de conclusão -->

- [x] #207 Endpoints REST M2M com guard de allowlist (MR !399) — @Danillo — concluída em 08/09/2026
- [x] #207 Materialização da notícia fiel ao snapshot (MR !401) — @Danillo — concluída em 11/09/2026
- [x] #217 Sub-issues #221–#225 (limpeza de inativos, helpers de banco, conversão booleana, utilitários de score, log seguro de voto) — @Danillo — concluídas em 26/08/2026
