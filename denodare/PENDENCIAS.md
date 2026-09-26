# Pendências — Denodare

Formato: `- [ ] ação — @responsável — prazo — origem`

## Urgente

- [ ] **#126** F1 Bloco F — decidir sobre os E2Es das Tasks 10 e 13: escrever agora (1–2h de infra) ou registrar como dívida técnica e seguir para Task 17 (ADRs `Accepted`) — @Danillo — próximo passo — [plano](/tmp/opencode/wt-126/docs/plans/2026-09-25-f1-multitenant-auth-tenants-rbac.md)
- [ ] **#207** Confirmar com Afonso quais dos 3 bloqueantes (map `publication`→news, `ValidateIf`, race de idempotência) seguem abertos após !401 — @Danillo — esta semana — [comentário de 08/09 na #207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207)

## Em aberto

### #126 — Multi-tenant (F0 encerrada; F1 em execução inline, Blocos A–E concluídos, F em execução)

- [ ] F1 Task 17: ADRs 0002/0003/0013/0014/0017 → `Accepted` com seção "Emendas F1" (D1–D10, inclui divergências 0005/0016/0018); acompanhamento e README de `rbac/` atualizados — @Danillo — próximo — [plano](/tmp/opencode/wt-126/docs/plans/2026-09-25-f1-multitenant-auth-tenants-rbac.md)
- [ ] F1 E2Es agrupados (Tasks 10 e 13) — pendência com escopo real: setup de infra E2E (usuário com bcrypt, papel em `roles`, tenants, atribuição em `tenant_role_assignments`, `BACKEND_TAG=develop`); cenários já cobertos por 4774 unit tests e pelo `news-leak.e2e-spec.ts` — @Danillo — sessão dedicada — [plano](/tmp/opencode/wt-126/docs/plans/2026-09-25-f1-multitenant-auth-tenants-rbac.md)
- [ ] Definir com Afonso o revisor dos ADRs e validar as divergências 0005/0016/0018 (agora via Emendas F1) — @Danillo com Afonso — antes de abrir MR
- [ ] Abrir MR a partir de `poc/126-multitenant` quando houver revisor — @Danillo — após Task 17
- [ ] Adequação do fluxo M2M (#207) ao ADR-0013 dentro da F1: token `client_credentials` emitindo `tenantId`, `oauth_clients.tenant_id`, remoção do fallback `clientId`, `ensureM2mEnvironment` e suíte `test/analysis-request-m2m` provisionando tenant interno — @Danillo — durante F1 — [plano](/tmp/opencode/wt-126/docs/plans/2026-09-25-f1-multitenant-auth-tenants-rbac.md)
- [ ] Propor a Afonso o enriquecimento da issue: mover o plano do anexo para `docs/` via MR, corrigir §5.1 (slug→uuid) e §0.4 (A+C→C+D) conforme ADRs 0016/0018, e abrir sub-issues por fase (F0–F6) e camada (bff, bChain, front) — @Danillo — durante F1 — [nota](reunioes/2026-09-22-analise-workitems.md)

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

- [x] #126 F1 Task 15 concluída — `src/modules/rbac/decorator-coverage.spec.ts` percorre 6 controllers com `Reflect.getMetadata` e falha se qualquer rota nova ficar sem `@IsPublic/@PreTenant/@Roles/@GlobalRoles` (`9f4cb533`); allowlist de 9 métodos de perfil/wallet/branding — @Danillo — 25/09/2026
- [x] #126 F1 Task 14 concluída — regra ESLint `local-rules/no-unscoped-querybuilder` (ADR-0015) detecta `createQueryBuilder`/`.query` em arquivos que importam `NewsEntity`/`RewardsEntity`; allowlist de 22 arquivos legados + spec de sincronia entre JSON e decorators reais (`f04a826b`) — @Danillo — 25/09/2026
- [x] #126 F1 Task 12 concluída — `TenantsAdminController` com `@GlobalRoles(superAdmin)` na classe (PATCH e invite também aceitam Admin do próprio tenant); `current/branding` lê do JWT; `TenantInvitationsController` com `POST /tenants/invitations/accept` marcado `@PreTenant`; máquina de estados corrigida para permitir reativação a partir de `deleted` limpando `deletedAt` (`e5623058`) — @Danillo — 25/09/2026
- [x] #126 F1 Bloco B concluído — Tasks 5–6 (`7a52c6ef`): decorators `@Roles/@GlobalRoles/@PreTenant/@AllowCrossTenant` + `RolesGuard` com precedência em `rbac/`, re-exports em `auth/guard/` — @Danillo — 25/09/2026
- [x] #126 F1 Bloco C concluído (exceto Task 10 E2E adiada para Bloco F) — Task 7 (`0a67a6e9`) JWT com `globalRoles/tenantRoles/tenantId`; Task 8 (`a36003dd`) `POST /auth/select-tenant`, `GET /auth/me`, refresh revalida tenant; Task 9 (`d5867013`) `TenantContext.enterWith` + `TenantContextGuard` global — @Danillo — 25/09/2026
- [x] #126 F1 Task 11 concluída — `TenantInvitationsService` com invite fora da transação e accept que atribui papel via `tenant_role_assignments` (`c3c6d4ed`); `TenantsService.create` refatorado — @Danillo — 25/09/2026
- [x] #126 F1 Task 4 concluída — `TenantRoleAssignmentEntity` + métodos `getTenantRoleNames`/`assignTenantRole`/`removeTenantRole`/`listMemberships`/`isMember` no `RbacService` (`7f7d631e`); 103/103 tests rbac passando — @Danillo — 25/09/2026
- [x] #126 F1 Bloco A concluído — migration M1 aplicada (`8d083a1c`), `scopedFind` revertido em `getForDashboard` (`e92425c3`), `MULTITENANT_POC` removido + `TenantsModule` incondicional + middleware/casca deletados (`8c44b6b6`); branch `poc/126-multitenant` mergeável; push com `--force-with-lease` para `origin` — @Danillo — 25/09/2026
- [x] #126 F0 encerrada — POC `TenantContext` + subscriber + `scopedFind` + E2E `news-leak` executado, 13 ADRs Proposed (0001–0006, 0013–0019), relatório POC v1.2 — @Danillo — 25/09/2026
- [x] #126 Escolha do modo de execução da F1 — inline nesta sessão, commits `--no-verify` + conventional + 1 linha em pt-BR — @Danillo — 25/09/2026
- [x] #207 Endpoints REST M2M com guard de allowlist (MR !399) — @Danillo — concluída em 08/09/2026
- [x] #207 Materialização da notícia fiel ao snapshot (MR !401) — @Danillo — concluída em 11/09/2026
- [x] #217 Sub-issues #221–#225 (limpeza de inativos, helpers de banco, conversão booleana, utilitários de score, log seguro de voto) — @Danillo — concluídas em 26/08/2026
