# Denodare

**Meu papel:** Desenvolvedor (backend, `fakenews-bff`)
**Status:** Ativo — 4 work items em paralelo; foco atual em #126 (multi-tenant), F1 em execução inline

## Contexto

Plataforma dAurora de checagem de notícias (fake news). Trabalho no repositório [`fakenews-bff`](https://gitlab.com/daurora-fakenews/fakenews-bff) (NestJS/TypeScript, PostgreSQL, integração blockchain e Elasticsearch). Demandas chegam via work items do GitLab, abertos em geral por Afonso Ueslei, e frequentemente misturam comunicação, débito técnico e continuação de branches já em andamento. Milestones em curso: **1.7.0** (#154) e **1.8.0** (#207, #217, #126).

### Ambiente de desenvolvimento

O maior custo do projeto não é o código, é rodar o sistema. O BFF depende de um nó blockchain (`fakenews-bChain`) para praticamente todo fluxo relevante (votos, rewards, custódia, configuração), e **ninguém da equipe consegue executar esse nó localmente**. Consequências práticas:

| Aspecto | Situação |
|---|---|
| Executar o BFF | Exige conectar à VPN para alcançar a blockchain compartilhada e, ainda assim, subir o resto da infraestrutura (PostgreSQL, Elasticsearch, Redis, serviços auxiliares) na máquina. Setup pesado e lento |
| Testes exploratórios | Muito difíceis: cada verificação manual passa por VPN + infra completa + estado compartilhado da chain |
| Testes automatizados | Unitários e E2E são o caminho viável de validação (`yarn lint`, `yarn check-types`, `npm run test:ci`); os E2E que tocam a chain dependem do ambiente remoto |
| Ambiente `develop` | Compartilhado; já foi derrubado por migrações com erro (#207, 08/09/2026), o que reforça o risco de validar só lá |

Efeito nas frentes: refatorações (#217) e mudanças em crons/eventos (#154) precisam de cobertura unitária forte porque a validação manual é cara; a decisão de isolamento da #126 (multi-tenant) precisa levar em conta que a blockchain é um recurso único e compartilhado. Um mock/stub do nó bChain para desenvolvimento local seria o investimento de maior retorno, mas não é escopo de nenhum work item atual.

### Work items atribuídos a mim

| # | Título | Milestone | Natureza | Situação real (22/09/2026) | Próximo passo |
|---|---|---|---|---|---|
| [#126](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/126) | Arquitetura multi-tenant | 1.8.0 | Arquitetura (bff + bChain + front) | **Bola da vez.** F0 encerrada (POC testada com E2E, 13 ADRs Proposed). F1 em execução inline por plano de 17 tarefas em 6 blocos (A–F): **A, B e C concluídos, D em andamento (Tasks 11–12 entregues)**. Bloco A tornou a branch mergeável (migration M1, `TenantsModule` incondicional). Bloco B entregou `TenantRoleAssignmentEntity` + membership via `tenant_role_assignments`, decorators `@GlobalRoles/@PreTenant/@AllowCrossTenant` e `RolesGuard` com precedência em `rbac/`. Bloco C entregou JWT com `globalRoles/tenantRoles/tenantId`, `POST /auth/select-tenant`, `GET /auth/me`, `TenantContextGuard` global; Task 10 (E2E) adiada para o Bloco F. Bloco D já tem `TenantInvitationsService` (invite/accept) e Admin API com `@GlobalRoles(superAdmin)`; falta Task 13 (E2E), adiada para o Bloco F. 704/704 unit tests em `tenants\|rbac\|auth`. Push com `--force-with-lease` para `origin/poc/126-multitenant`; nenhum commit em `develop`. Aceitação dos ADRs (com Emendas F1, D1–D10) fica no Bloco F | Fechar Bloco D com o commit da Task 12; encadear Bloco E (lint rule + cobertura de decorators) e Bloco F (E2Es agrupados de C+D, ADRs `Accepted`) ([plano](/tmp/opencode/wt-126/docs/plans/2026-09-25-f1-multitenant-auth-tenants-rbac.md)) |
| [#207](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/207) | Recebimento de solicitações de análise do Guaia (M2M) | 1.8.0 | Feature, grande parte entregue | MRs !399 e !401 merged. Afonso aprovou mas listou em 08/09 o que develop ainda deve à "V2" — 3 bloqueantes: mapeamento `publication`→news (parcialmente atacado em !401), `ValidateIf` allegation/reproduction, race de idempotência (unique → 500 em vez de replay). Houve hotfix de migrações que derrubaram develop | Confirmar com Afonso o que dos 3 bloqueantes ainda está aberto após !401 e fechar em MR único; gaps maiores (timeline, dossiê, org/tenant de domínio) só com escopo acordado |
| [#217](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/217) | Refatoração de duplicações e código morto | 1.8.0 | Débito técnico, fatiado em sub-issues | Sub-issues #221–#225 **concluídas** (MRs !377–!381, 26/08). Sub-issues **#226–#230 abertas** e também atribuídas a mim. Branches `feat-217-refatoracao` / `feature-217-refatoracao` paradas desde 21/08 | Seguir uma sub-issue por MR (#226 datas IA, #227 paginação checadores, #228 pedidos sob análise, #229 resultados de votação, #230 constantes/migrações). Regra bloqueante: `analise-obrigatoria-bff.mdc`, sem quebra de contrato |
| [#154](https://gitlab.com/daurora-fakenews/fakenews-bff/-/work_items/154) | Débito residual do épico #138 (eventos + fallback) | 1.7.0 | Débito técnico, 5 itens | Nenhum MR aberto. Itens: 12.1 dashboards Grafana (alta), 12.2 `syncRewards` sem polling 30s (alta), 12.3 claim atômico no sync de mídia ES (média), 12.4 status do ADR → Adotado (baixa), 12.5 outbox persistente (opcional) | Começar por 12.2 (código, sem dependência externa); 12.1 depende de acesso ao Grafana — pedir acesso já |

Outras issues abertas comigo: #226–#230 (sub-issues de #217, listadas acima).

### Referências no repositório

- `.cursor/rules/analise-obrigatoria-bff.mdc` — regra obrigatória em qualquer MR
- `docs/architecture-decisions.md`, `docs/runbooks/async-processing.md`, `docs/entrega-branch-138-async-processing.md` — base do #154
- `src/common/helpers/claim-next.helper.ts` — padrão de claim atômico reutilizado em #154

## Navegação

| Arquivo | Conteúdo |
|---|---|
| [PESSOAS.md](PESSOAS.md) | Quem é quem, papéis, contatos |
| [PENDENCIAS.md](PENDENCIAS.md) | Ações em aberto, responsáveis, prazos |
| [DECISOES.md](DECISOES.md) | Registro de decisões |
| [reunioes/](reunioes/) | Atas datadas |
| [rascunhos/](rascunhos/) | Mensagens e textos em preparação |

## Linha do tempo recente

| Data | Registro |
|---|---|
| 25/09/2026 | #126: Blocos B e C da F1 concluídos e Bloco D em andamento (Tasks 11–12 entregues). Bloco B (`7a52c6ef`): decorators `@Roles/@GlobalRoles/@PreTenant/@AllowCrossTenant` e `RolesGuard` com precedência em `rbac/` (re-exports em `auth/guard/`). Bloco C: JWT com `globalRoles/tenantRoles/tenantId` (`0a67a6e9`); `POST /auth/select-tenant` + `GET /auth/me` + refresh que revalida tenant e membership (`a36003dd`); `TenantContext.enterWith` + `TenantContextGuard` global (`d5867013`). Bloco D: `TenantInvitationsService` com invite fora da transação + accept que atribui papel (`c3c6d4ed`); Admin API com `@GlobalRoles(superAdmin)`, `current/branding` do JWT e aceite pré-tenant (pronto para commit). Tasks 10 e 13 (E2Es) adiadas para o Bloco F para agrupar setup. 704/704 unit tests. Push com `--force-with-lease`; nenhum commit em `develop` ([decisão](DECISOES.md)) |
| 25/09/2026 | #126: F0 encerrada (POC testada, E2E `news-leak` executado, L5 fechada; 13 ADRs Proposed) e F1 iniciada por plano de 17 tarefas em 6 blocos. **Bloco A concluído** — migration M1 aplicada em `10.215.0.31/fakenews-dev` (`8d083a1c`), `scopedFind` revertido em `getForDashboard` (`e92425c3`), `MULTITENANT_POC` removido + `TenantsModule` incondicional + middleware e casca `select-tenant` deletados (`8c44b6b6`); branch `poc/126-multitenant` mergeável e sincronizada com `origin` via `--force-with-lease`. **Task 4 do Bloco B concluída** (`TenantRoleAssignmentEntity` + métodos de tenant no `RbacService`, 103/103 tests rbac, `7f7d631e`). Execução inline com commits `--no-verify` + conventional em pt-BR ([decisão](DECISOES.md)) |
| 22/09/2026 | Bandeja montada: mapeados os 4 work items atribuídos (#126, #207, #217, #154) com situação real a partir do GitLab (MRs, branches, sub-issues); #126 definido como foco ([nota](reunioes/2026-09-22-analise-workitems.md), [decisão](DECISOES.md)) |
| 22/09/2026 | Registrada a complexidade do ambiente de dev (blockchain sem execução local, VPN + infra completa) e identificado o ponto de enriquecimento da #126: plano em anexo, sem decomposição, possível conflito com o tenant do fluxo M2M da #207 ([nota](reunioes/2026-09-22-analise-workitems.md)) |
| 11/09/2026 | #207: MR !401 merged (materialização da notícia fiel ao snapshot) |
| 08/09/2026 | #207: MR !399 merged (endpoints REST M2M). Afonso aprovou e publicou análise develop x V2 com 3 bloqueantes em aberto; hotfix de migrações que derrubaram develop |
| 01/09/2026 | #207: fundação merged (MRs !383, !385–!388: migrations, DTOs/máquina de estados, SLA, evento dispatch, materialização atômica) |
| 26/08/2026 | #217: sub-issues #221–#225 concluídas (MRs !377–!381) |
| 21/08/2026 | #217 aberta por Afonso (518 clones, ~4,9% duplicação) |
| 22/05/2026 | #154 aberta por Afonso (débito residual do épico #138) |
